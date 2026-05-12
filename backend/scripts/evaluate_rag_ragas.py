"""
离线 RAGAS 评测：LangChain Chat + OpenAI 向量，对齐本仓库检索与索引流程。

流程：
  1) 解析并索引 KNOWLEDGE_BASE PDF（与 demo 相同的 Faiss + 分页窗口）。
  2) 用 ``DefaultKnowledgeRetrievalTool`` 检索后，再走 LangChain 生成答案。
  3) 组装 Hugging Face ``datasets.Dataset`` 列：``question``, ``answer``, ``contexts``, ``ground_truth``。
  4) 调用 ``ragas.evaluate``（默认 **不含** ``answer_relevancy``，中文语料上该项常失真）。
  5) 额外打印 **问题–答案向量余弦相似度**（与索引用同一 OpenAI embedding），作 relevancy 对照。

用法（在 backend/ 目录下）：

  OPENAI_API_KEY=... \\
  PYTHONPATH=. python scripts/evaluate_rag_ragas.py /path/to/kb.pdf

可选：``--with-answer-relevancy`` 仍跑 RAGAS 自带 answer_relevancy（与向量对照并列参考）。

环境变量：
  FLASHRANK_MODEL_NAME — 可选，覆盖 FlashRank 重排序模型。
"""

from __future__ import annotations

import argparse
import asyncio
import math
from dataclasses import replace
from pathlib import Path
from uuid import UUID, uuid4

from datasets import Dataset
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import OpenAIEmbeddings

from ragas import evaluate
from ragas.embeddings.base import LangchainEmbeddingsWrapper
from ragas.llms.base import LangchainLLMWrapper
from ragas.metrics._context_precision import context_precision
from ragas.metrics._context_recall import context_recall
from ragas.metrics._faithfulness import faithfulness

from app.config.settings import Settings, load_settings
from app.domain.models import DocumentType
from app.providers.embeddings import OpenAIEmbeddingProvider
from app.providers.llm import build_chat_model
from app.tools.chunking import RecursiveTextChunkingTool
from app.tools.document_parsing import LocalDocumentParsingTool
from app.tools.faiss_vector_store import FaissVectorStore
from app.tools.knowledge_retrieval import DefaultKnowledgeRetrievalTool
from app.tools.windowed_knowledge_indexer import WindowedKnowledgeBaseIndexer

# 请按自身语料改写问题与参考答案；严肃的 context_recall 需要与 PDF 一致的 ground_truth。
EVAL_SAMPLES: list[dict[str, str]] = [
    {
        "question": "技术面试里前端方向应该优先准备哪些知识点？请结合资料简要说明。",
        "ground_truth": "请将 PDF 中与「前端」「面试」「重点」对应的原文摘录或概括为参考答案。",
    },
    {
        "question": "如何准备行为面或偏系统设计类问题的答题思路？资料里怎么说？",
        "ground_truth": "请将 PDF 中与行为面或系统设计备考相关的较短段落改写为标准答案要点。",
    },
]


RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一位严谨的中文助手，只能依据下面编号的上下文片段作答；不要用常识补全。"
            "若上下文不足以回答，明确说明依据所给上下文无法得出结论。",
        ),
        (
            "human",
            "上下文：\n{context}\n\n问题：{question}",
        ),
    ]
)


async def _index_kb(
    pdf_path: Path,
    *,
    settings: Settings,
    session_id: UUID,
) -> FaissVectorStore:
    embedding_provider = OpenAIEmbeddingProvider(api_key=settings.openai_api_key)

    vector_store = FaissVectorStore()
    parser_tool = LocalDocumentParsingTool()
    indexer = WindowedKnowledgeBaseIndexer(
        document_parser=parser_tool,
        chunking_tool=RecursiveTextChunkingTool(chunk_size=900, chunk_overlap=120),
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )
    parsed = await parser_tool.parse_document(
        file_path=pdf_path,
        document_type=DocumentType.KNOWLEDGE_BASE,
    )
    parsed = replace(
        parsed,
        metadata={**parsed.metadata, "source_file_path": str(pdf_path.resolve())},
    )
    await indexer.index_documents(session_id=session_id, documents=[parsed])
    return vector_store


async def _run_langchain_rag_batch(
    pdf_path: Path,
    *,
    samples: list[dict[str, str]],
) -> Dataset:
    settings = load_settings()
    if settings.openai_api_key is None:
        raise ValueError("需要配置 OPENAI_API_KEY（环境变量或 .env）。")

    llm = build_chat_model(settings)
    retrieval_embedding = OpenAIEmbeddingProvider(api_key=settings.openai_api_key)

    session_id = uuid4()
    vector_store = await _index_kb(pdf_path, settings=settings, session_id=session_id)
    retriever = DefaultKnowledgeRetrievalTool(
        embedding_provider=retrieval_embedding,
        vector_store=vector_store,
    )

    chain = RAG_PROMPT | llm | StrOutputParser()
    rows = {"question": [], "answer": [], "contexts": [], "ground_truth": []}

    for sample in samples:
        q = sample["question"].strip()
        gt = sample["ground_truth"].strip()
        retr = await retriever.retrieve_knowledge(
            session_id=session_id,
            query=q,
            top_k=5,
            prefetch_k=20,
            document_types=[DocumentType.KNOWLEDGE_BASE],
        )
        ctx_list = [c.chunk.text for c in retr.chunks]
        numbered = "\n\n".join(f"【{i + 1}】{t}" for i, t in enumerate(ctx_list))
        answer_text = await chain.ainvoke({"context": numbered, "question": q})

        rows["question"].append(q)
        rows["answer"].append(answer_text.strip())
        rows["contexts"].append(ctx_list)
        rows["ground_truth"].append(gt)

    return Dataset.from_dict(rows)


async def _build_dataset_with_qa_scores(
    pdf_path: Path,
    *,
    samples: list[dict[str, str]],
) -> tuple[Dataset, list[float], float]:
    """单事件循环：建库 + RAG + 问题–答案相似度，避免 async 客户端在二次 asyncio.run 下清理报错。"""
    dataset = await _run_langchain_rag_batch(pdf_path, samples=samples)
    settings = load_settings()
    if settings.openai_api_key is None:
        raise ValueError("需要配置 OPENAI_API_KEY（环境变量或 .env）。")

    qa_scores, qa_mean = await _compute_qa_embedding_similarities(
        list(dataset["question"]),
        list(dataset["answer"]),
        api_key=settings.openai_api_key,
    )
    return dataset, qa_scores, qa_mean


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


async def _compute_qa_embedding_similarities(
    questions: list[str],
    answers: list[str],
    *,
    api_key: str,
    model: str = "text-embedding-3-small",
) -> tuple[list[float], float]:
    """与索引一致的 OpenAI embedding，中英文均可；取值约 [-1, 1]，越接近 1 表示方向越一致。"""
    if len(questions) != len(answers):
        raise ValueError("questions 与 answers 条数不一致。")
    prov = OpenAIEmbeddingProvider(api_key=api_key, model=model)
    q_emb = await prov.embed_texts(questions)
    a_emb = await prov.embed_texts(answers)
    scores = [_cosine_similarity(q, a) for q, a in zip(q_emb, a_emb, strict=True)]
    mean_score = sum(scores) / len(scores) if scores else 0.0
    return scores, mean_score


def main() -> None:
    parser = argparse.ArgumentParser(description="最简单的 RAG + RAGAS 评测（知识库 PDF）。")
    parser.add_argument(
        "knowledge_pdf",
        type=Path,
        help="要先解析并入库的 KNOWLEDGE_BASE PDF 路径。",
    )
    parser.add_argument(
        "--with-answer-relevancy",
        action="store_true",
        help=(
            "同时计算 RAGAS 的 answer_relevancy（对中文 QA 往往失真，默认关闭）；"
            "默认用下方的「问题–答案向量相似度」作对照。"
        ),
    )
    args = parser.parse_args()

    pdf = args.knowledge_pdf.expanduser().resolve()
    if not pdf.is_file():
        raise FileNotFoundError(str(pdf))

    dataset, qa_scores, qa_mean = asyncio.run(
        _build_dataset_with_qa_scores(pdf, samples=EVAL_SAMPLES)
    )
    settings = load_settings()
    chat = build_chat_model(settings)
    emb = OpenAIEmbeddings(api_key=settings.openai_api_key, model="text-embedding-3-small")

    metrics = [faithfulness, context_precision, context_recall]
    if args.with_answer_relevancy:
        from ragas.metrics._answer_relevance import answer_relevancy

        metrics.insert(1, answer_relevancy)

    result = evaluate(
        dataset,
        metrics=metrics,
        llm=LangchainLLMWrapper(chat),
        embeddings=LangchainEmbeddingsWrapper(emb),
    )
    print("RAGAS 聚合分数:", result)

    print(
        "\n对照指标 — 问题与答案向量余弦相似度（embedding=text-embedding-3-small，与知识库索引一致）："
    )
    for i, s in enumerate(qa_scores):
        print(f"  样本 {i + 1}: {s:.4f}")
    print(f"  均值: {qa_mean:.4f}")

    pd_mod = None
    try:
        import pandas as pd

        pd_mod = pd
    except ImportError:
        pass

    if pd_mod is not None:
        df = result.to_pandas()
        df["qa_cosine_similarity"] = qa_scores
        print("\n逐条分数与样本：\n", df)


if __name__ == "__main__":
    main()
