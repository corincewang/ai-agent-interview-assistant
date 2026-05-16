#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Temporary runtime workaround for OpenMP duplicate initialization in local dev.
export KMP_DUPLICATE_LIB_OK=TRUE
export OMP_NUM_THREADS=1

# Toggle to false when you do not need LangSmith traces.
export LANGSMITH_TRACING="${LANGSMITH_TRACING:-true}"

python -m uvicorn app.api.main:app --reload --port 8000
