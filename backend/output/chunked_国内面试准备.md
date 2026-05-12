# Chunked Markdown: 国内面试准备.pdf
- source: `/Users/wanghan/Desktop/国内面试准备.pdf`
- parser: `unstructured.partition.auto.partition` / `fast-page-windowed`
- chunks: **538**

---
## Chunk 0 — 自我介绍

自我介绍

你好，我是王涵，目前在 Carnegie Mellon University 读信息系统，是26届应届毕业生。我的方向是全栈偏向前端开发，同时最近也在做一些 AI Native 的探索。  
我最近在做一个关于家电的电商场景的 AI Agent，这是一个我从 0 到 1 独立主导落地的项目，不只是实现多轮对话和工具调用，更关注交互本身，比如流式输出、结构化卡片，以及通过“下一步” 一步步引导用户完成任务。这让我觉得，AI 不是一个单独的能力，而是需要和产品体验结合，才能真正落地。  
同时我也从 0 到 1 做了一个 iOS 应用 Pawse，从产品，设计到工程实现和测试都完整参与。之前在 Menu 的实习中，我更多是在高频交互场景下做性能优化。  
我自己比较感兴趣的，也跟MOVA非常契合的一点是，我希望去探索怎么用ai和最新的技术去做有“思考能力”的产品，把人从重复性的操作中解放出来，就像mova的一些智能家电产品。我认为这才是ai在这个时代真正的使命。再加上我同时有设计和美术背景，很认同mova的科技+美学的概念，以及海外留学和多语言工作的经验，也比较希望参与到面向全球市场的产品中去。最后，我也看了校招的直播，感觉整体是一家很青春有活力的公司，新人有很多机会。
---
## Chunk 1 — Mova：主攻欧美高端市场

Mova：主攻欧美高端市场

我自己比较感兴趣的是，怎么用技术去做有“思考能力”的产品，对出海业务也比较感兴趣。再加上我有海外学习和多语言背景，也比较希望参与到面向全球用户、长期打磨产品体验的团队中。
---
## Chunk 2 — 为啥选前端？

为啥选前端？

我一开始接触前端其实是因为对交互和设计比较感兴趣，但后来在做项目的过程中，我发现前端不仅是“界面”，而是直接决定用户体验和产品效果的核心一层。  
比如在 Menu 的实习中，我做的埋点系统其实是一个典型例子。前端不仅负责展示，还决定了用户行为如何被记录、如何被分析，最后这些数据会反过来影响产品决策。  
所以我选择前端，是因为它处在一个很有意思的位置：一边是用户体验，一边是工程实现，中间还能连接数据和产品决策/我觉得这个交叉点是最有挑战、也最有成长空间的。  
为什么Menu用redux？ Menu里，购物车、取餐方式、店铺、用户与活动信息会在首页、店铺页、Bottom Sheet、确认订单之间来回跳，同一份数据被很多屏幕读写。用 Redux 可以把这些当成单一数据源：状态集中、更新路径清晰（action → reducer/saga），避免靠 props 层层透传或各页面各自 useState 导致不同步、难排查。配合 useSelector 按模块订阅，组件只拿自己要的 slice；异步加车、下单等用 saga 集中处理副作用，UI 只负责 dispatch。整体上是为了跨页面一致、可预测、好协作。
---
## Chunk 3 — 为什么不用Context或者Zustand？

为什么不用Context或者Zustand？

Context 适合低频更新和简单状态，但在 Menu 这种高频更新（购物车金额、优惠券、活动）场景下，会导致大范围 re-render，而 Redux 可以通过 selector 精细订阅，避免无关组件更新。  
Zustand 本身是很好的轻量状态库，但因为 Zustand 是“哪里都可以直接改 store”，在Menu这种状态复杂的情况下，如果没有额外规范，很容易出现状态变更分散、难以追踪的问题。
---
## Chunk 4 — Menu中做需求的时候，你是怎么的优化性能？

Menu中做需求的时候，你是怎么的优化性能？

（3个优化）  
在 Menu 实习中，我主要负责店铺广告推广模块，购物车和优惠券相关功能，性能优化主要是在开发过程中围绕“减少不必要渲染”和“控制列表加载成本”两方面来做。  
第一块是避免不必要的 re-render。我会对纯展示组件使用 React.memo，比如购物车里的 CouponLabel，这种组件只依赖少量 props，比如剩余金额，如果父级列表更新但这些 props 没变，就可以跳过渲染。  
同时在状态管理上，我会通过自定义 selector 精细订阅 state，比如优惠券进度条是通过一个专门的 selector 计算出进度和剩余金额，而不是订阅整个 cart 或 promotion，这样可以避免无关状态变化导致组件更新。  
第二块是列表渲染优化。我们使用 FlatList 来做购物车和优惠券列表，利用它的虚拟化机制，只渲染当前视口附近的 item，并在滚动时复用 cell，从而降低内存和滚动卡顿。同时会通过 keyExtractor 保证 key 稳定，避免复用错误和不必要的 diff。  
第三块是控制加载和请求节奏。在开发中也观察到，列表性能不仅和 re-render 有关，还和图片加载和请求频率有关。所以我们在一些列表场景中做了分批加载和缓存处理，比如通过控制 FlatList 的 initialNumToRender 和批次渲染数量，避免首屏挂载过多组件；在分页加载时，通过 loading 和 hasMore 状态控制，。在图片加载上则利用组件自带的分层缓存能力（expo-image），并让靠近视口的图片优先加载，从而减少滚动时的卡顿。  
整体上，这些优化的核心思路是：减少无效渲染、控制一次性加载量，以及让关键内容优先展示，从而提升列表的流畅度和用户体验。
---
## Chunk 5 — Flatlist为什么有时候还是会卡？

Flatlist为什么有时候还是会卡？

可能原因：  
1. renderItem 太重，2. key 不稳定导致复用失败，3. 图片加载阻塞。我会用 React DevTools 看 re-render，用性能工具（Flipper/profiling）看帧率，并逐步定位是 JS 计算还是 UI 渲染问题。
---
## Chunk 6 — Menu中的埋点（origin tracking）是怎么设计的？

Menu中的埋点（origin tracking）是怎么设计的？

在 Menu 项目中，我设计了一套基于用户来源（origin）的埋点方案，这个方案的核心目标，是把用户从不同入口进入店铺，到加购、再到下单尝试的链路打通，跟数分部门合作，用于做归因和转化漏斗分析。  
前端这边我主要做了三件事：第一是定义统一的 origin schema，解决多入口参数格式不一致的问题；第二是做链路传递，把origin data存储在localStorage中，让 origin 能在店铺页、商品页、购物车和下单流程中持续保留；第三是在关键节点做埋点上报，比如下单尝试事件，保证能还原完整路径。  
最后是关于localStorage，他的好处是能跨页面和刷新保留 origin，适合我们这种从入口到 checkout 的长链路追踪。但它的缺点是不会自动过期。所以我会给 origin 数据加 timestamp sessionId，并设计清理时机。比如下单成功后清理；用户进入新的店铺时覆盖；如果超过一定时间也视为过期清理。
---
## Chunk 7 — 如果让你进一步提升这个埋点的可靠性，该怎么做？

如果让你进一步提升这个埋点的可靠性，该怎么做？

（埋点丢失）  
当时我们是把 origin 先持久化在 localStorage 里，在用户点击下单按钮时读取并直接上报到 Firebase。但由于埋点是在点击下单按钮时触发的，但它本质上还是一次网络上报，只要走网络，就存在弱网、页面切换、请求失败或 SDK 异步发送未完成的风险，所以如果要提升可靠性，如果要进一步提升可靠性，我会考虑在埋点 SDK 层加一个本地事件队列，让事件先入队，再异步上报，失败时做有限重试。
---
## Chunk 8 — localStorage的一致性问题

localStorage的一致性问题

如果有多个入口、多种购物车类型、多 tab 或多页面并行，客户端本地状态可能不一致。实际上这是一个困难的点，外卖购物车一套 origin，自取购物车一套 origin，中途切换店铺覆盖掉原值,但是这个值也没有丢，如果切换回原来的购物车模式还是能看见那个origin的，因为他是和 cart_id和 shop_id绑定的。
---
## Chunk 9 — 遇到的困难：

遇到的困难：

第一是多入口来源结构不统一，不同页面的参数格式不一样，所以我在设计时做了统一的 origin schema，保证后续可以扩展新的入口而不影响现有逻辑。  
第二是购物车数据的生命周期管理，比如什么时候清理 origin，什么时候保留，这里通过 success/fail 分支来保证数据既准确又完整。
---
## Chunk 10 — Menu中埋点的数据怎么计算的？

Menu中埋点的数据怎么计算的？

把订单日志作为基准，去匹配对应的埋点事件，比如下单尝试或下单成功事件，统计 origin 字段的覆盖率和正确率，比如有多少订单能匹配到 origin，以及其中有多少是正确的。  
Menu中为什么要做E2E测试？单元测试主要验证单个函数或组件逻辑是否正确，而 E2E 测试是从用户视角出发，验证完整业务流程，比如登录、搜索、加购到下单这一整条链路是否正常。比如从搜索页进入店铺、再加购物车，这中间涉及多个页面和全局状态，如果某个环节出问题，单测很难覆盖，但 E2E 可以发现。
---
## Chunk 11 — Detox是怎么工作的？

Detox是怎么工作的？

Detox 是一个基于灰盒测试（gray-box testing）的 E2E 测试框架，它可以直接和 React Native 应用的运行时进行交互，而不是像传统黑盒测试那样仅仅模拟用户操作。  
它的核心优势在于自动同步机制（synchronization），Detox 能感知 JS 线程和 Native 线程的状态，自动等待异步任务完成，比如网络请求、动画、定时器等，只有在这些任务完成后才会继续执行测试，从而避免 flaky test，提高测试稳定性。  
相比其他 E2E 测试方案，我选择 Detox 的主要原因是它对 React Native 支持非常好，执行速度更快，而且测试结果更稳定。  
你具体测了什么流程？我主要覆盖了核心路径，比如登录、搜索商品、加入购物车到下单这一整条流程。因为这些是核心转化路径，一旦出问题影响最大。  
什么是 flaky test？你遇到过吗？ flaky test 指的是不稳定的测试，有时候通过有时候失败，通常是因为异步没处理好、等待时机不对或者依赖外部状态。在 Detox 里如果不正确等待网络请求或动画结束，就容易出现这种问题。我们一般通过显式等待或者保证状态稳定来减少 flaky。
---
## Chunk 12 — Menu里怎么用到了MCP

Menu里怎么用到了MCP

在 Menu 项目里，我把 MCP 接进了 Cursor 的 AI 辅助开发流程，这样能够“让 AI 能拿到更真实的项目上下文”。  
接入 MCP 之后，像 Figma，设计文档这类外部资源可以通过标准方式暴露给模型，模型能按需读取设计稿节点或相关上下文，而不是完全依赖我手动复制粘贴。  
我负责的部分主要是开发环境里的集成和鉴权，比如配置 Figma/GitHub 相关 server，让这些资源能在 Cursor 里被模型稳定调用。最终效果是减少了 AI 生成代码和设计稿、接口命名不一致带来的返工。
---
## Chunk 13 — Pawse中图片做了哪些优化？

Pawse中图片做了哪些优化？

（上传&展示）  
在 Pawse 项目中，图片处理我主要从上传和展示两个阶段做了优化。  
在上传阶段，我主要做了客户端压缩和AWS S3存储解耦。在客户端会对图片进行预处理，比如将 UIImage 等比缩放。存储方面，我使用 AWS S3 来存储用户上传的图片，将文件存储从后端服务中解耦。这样可以避免后端服务器承受大文件 IO 压力，同时提升系统的可扩展性和稳定性，也方便后续接入 CDN 做分发优化。  
在图片展示阶段，我主要做了缓存和加载策略优化。图片加载后会进入内存缓存和磁盘缓存，同一个 key 会优先命中缓存，减少重复网络请求。在列表场景中，我会做分批预加载，提前加载即将进入视口的图片，同时控制并发数量，避免一次性请求过多导致卡顿。
---
## Chunk 14 — Image I/O Cache 是什么

Image I/O Cache 是什么

我理解的 Image I/O Cache，不只是把图片文件缓存下来，而是围绕图片展示整条链路做复用优化。在 Pawse 里，我主要关注两层：一层是磁盘缓存，减少重复下载；另一层是内存缓存，优先复用当前页面高频展示的图片结果。同时会尽量按展示尺寸处理图片，避免列表滚动时反复从大图解码，从而提升 Feed 的稳定性和滚动流畅度。  
追问 1：缓存 key 怎么设计  
一般会以图片 URL 或资源唯一标识为主，如果存在不同尺寸版本，也会把尺寸信息纳入 key，避免错用。
---
## Chunk 15 — 追问 2：缓存什么时候失效

追问 2：缓存什么时候失效

最基础的是 URL 变化即失效；另外也可以结合容量限制和 LRU 做淘汰。对更新频繁的资源，还可以通过版本号或更新时间控制失效。
---
## Chunk 16 — 追问 3：为什么不能全放内存

追问 3：为什么不能全放内存

内存快，但容量有限。图片是非常吃内存的资源，如果都放内存，很容易造成内存压力甚至被系统回收，所以需要内存和磁盘分层。  
你怎么lead的团队在 Pawse 这个 3 人团队里，我的角色更像小团队里的技术 owner。我的 leadership 不在于传统管理，而在于把主路径优先级定清楚、做关键技术取舍，并推动核心模块落地。主要做了两点：第一，判断主路径优先级，比如先把 Feed、Contest、S3 这些核心闭环跑通；第二，做关键技术取舍，比如 SwiftUI、Firebase+REST API、S3 和 Lambda 的边界怎么定；  
Pawse 里feed的性能优化  
我在 Pawse 里做的 Feed 优化主要有三类。  
第一类是更新策略优化。像点赞、参与活动、发帖返回列表这类操作，如果每次都全量重拉 Feed，会造成明显的性能浪费，所以我们会根据场景做局部更新和乐观更新。比如点赞后只更新当前 item 的点赞状态和计数，不会把整个列表重新请求一遍；乐观更新则是先让用户看到 UI 变化，再和后端结果对齐，失败时再回滚。  
第二类是列表加载策略。Feed 不会一次性拉太多数据，而是分页加载，控制首屏和单次请求的数据量，避免内存压力随着滚动不断增大。  
第三类是图片展示优化。因为 Feed 是图片密集型页面，我们做了内存和磁盘两级缓存，并且对预加载数量做控制，避免一次性触发太多图片请求和解码，影响滚动流畅度。  
整体上，我的思路是减少全量刷新、控制单次加载量、并把图片加载成本尽量提前和复用掉。
---
## Chunk 17 — 自适应排序算法

自适应排序算法
---
## Chunk 18 — 自适应排序算法

Pawse 里的排序更接近轻量级规则排序，不是复杂的推荐模型。我们没有完全按时间倒序展示，而是综合考虑了几个信号，比如内容新鲜度、互动情况，以及和用户关系的相关性。 “自适应”主要体现在两个地方：一是帖子本身的表现会影响排序，比如互动更高的内容会适当靠前；二是会结合用户最近的一些行为做轻量调整，而不是所有人都看完全一样的 Feed。  
但我们当时没有把它做成一个复杂的机器学习系统，而是先用规则方式在新鲜度、质量和相关性之间做平衡，这对早期产品更可控，也更容易调。  
为什么选择 SwiftUI，而不是 UIKit？主要是因为项目阶段偏早期，团队规模小，需要高迭代效率。SwiftUI 在声明式 UI、组件复用和快速搭界面上效率很高。另外 SwiftUI 很像前端里的 React，都是状态驱动视图更新，所以我在做项目的时候会很自然地用组件化和状态管理的思路去设计。  
为什么是 Firebase+自定义 RESTful API，不是只用 Firebase？基础数据和实时性较强的部分放 Firebase，利用它 NoSQL 和快速集成的优势；而更偏业务规则、需要统一控制和更清晰接口边界的部分，我们通过自定义 RESTful API 暴露出去。这样客户端侧就不会直接承担过多业务判断，后期也更容易维护。  
为什么选择firebase？  
我们当时选择 Firebase 和 NoSQL，核心原因其实就两个：快，还有适合我们那个阶段。  
选nosql是因为，pawse核心数据主要是用户、宠物、帖子、活动这些对象，它们天然更接近文档型数据，而且很多页面读取都是按照业务对象直接取，不太依赖特别复杂的多表 join。用 NoSQL 的话，数据结构会更灵活。  
选Firebase 对我们来说有一个很大的好处，就是它把很多基础能力整合得比较完整，比如数据存储、云服务这些，能够让我们在项目早期先把核心功能跑通，而不是花很多时间在底层基础设施搭建上。
---
## Chunk 19 — 自适应排序算法

选Firebase 对我们来说有一个很大的好处，就是它把很多基础能力整合得比较完整，比如数据存储、云服务这些，能够让我们在项目早期先把核心功能跑通，而不是花很多时间在底层基础设施搭建上。  
当然它也不是没有代价。NoSQL 在复杂查询、多表关系上没有传统关系型数据库那么自然，所以我们没有把所有业务逻辑都直接压在 Firebase 上，而是结合了一部分自定义 RESTful API，把更复杂的业务规则和接口边界独立出来。这样既保留了早期开发效率，也避免后面项目变复杂时完全被 Firebase 的数据模型限制住。  
你们为什么用 AWS Lambda 做每周活动和动态推送？因为这类任务天然是事件驱动或定时触发型的，不需要一直开着一个常驻服务。Lambda 比较适合做周期性活动生成。
---
## Chunk 20 — 为什么用fastlane？

为什么用fastlane？

Fastlane 主要解决了发布链路手工步骤多、容易出错的问题。比如构建、签名、打包、上传 Beta、版本管理这些流程，如果全靠手工做，不仅慢，还容易漏步骤。引入 Fastlane 后，我们可以把重复流程标准化，其实就是CICD，一方面提升发布效率，另一方面减少人为失误，让团队把精力更多放在功能和体验优化上。
---
## Chunk 21 — 你觉得这个项目做得最好的地方是什么？

你觉得这个项目做得最好的地方是什么？

我觉得最好的地方不是功能堆得多，而是我们比较早就抓住了核心主路径： Feed、图片、活动、推送，这几个模块是围绕用户留存和互动来搭的，不是零散拼功能。从工程上看，我也比较满意我们没有把所有逻辑都糊在客户端，而是逐步把数据层、接口层、媒体存储和异步任务分开，这让项目后期更容易扩展。  
你现在回头看，哪里还能做得更好？如果重新做，这个项目我本身优先时间和范围上我优先把核心功能闭环（Auth、Feed、Contest、 S3）跑通，没有上正式埋点——更多是 print 和 Xcode 控制台排错，够用但不能量化、也不能线上定责。  
但是如果这是要交付真实用户的产品，我会第一步就把可观测性补上：结构化日志+关键路径事件（首屏耗时、上传成功/失败、Feed 空态原因），并和 Crashlytics 的非致命错误对齐，这样『慢』 和『挂』都能变成可排序的 backlog，而不是靠感觉争论。
---
## Chunk 22 — Q0. 介绍一下你的项目

Q0. 介绍一下你的项目

这个项目是一个面向家电配件电商的 AI Agent，主要解决用户在选购、故障排查和配件兼容性上的复杂决策问题。本质上是把传统电商的“搜索+FAQ+客服”整合成一个任务驱动的对话系统。因为美国这边人工服务比较贵，所以制作客服智能体能够有效减少电商的人工成本开销，整体架构是：  
前端：Next.js+fetch 流式读取 ● 后端：Function Calling+Node.js+几个轮次的工具调用 ● 数据：MySql，整体数据的结构性很强  
● 部署到了vercel  
整个项目是我从 0 到 1 独立完成的，包括技术选型、Agent 架构设计、Prompt优化和检索策略优化，以及流式交互体验的实现。
---
## Chunk 23 — Tool和skill的区别是啥？

Tool和skill的区别是啥？

Tool和skill的区别在于抽象层级和责任。  
Tool主要面向 OpenAI Chat Completions 的 tools 接口，相当于是给模型点的按钮。 Skill主要面向工程/产品/运维：这条能力怎么上线。通常是元数据+指针：指向底层哪一个Tool/内部函数；有时候还带业务策略（例如「只有 gold 客户才能用某个tool）。  
为什么没做skills？  
我们的 tool 就是能力边界；能力面比较小：就6条目录相关 Tool（normalize/lookup/compat/symptom/catalog_search 等），用一份 openaiTools.ts+toolExecutor 就能管清楚，再上Skill 层是重复劳动。
---
## Chunk 24 — 对市面上不同ai工具的看法？

对市面上不同ai工具的看法？

当前主流大模型其实差异更多在优化方向上。GPT 更偏工程落地，比如工具调用、多轮对话和 API 生态比较成熟，所以我在项目里用它作为核心模型；Claude 更擅长长文本处理和稳定推理，我更多是在开发阶段，比如用 Cursor 调 Claude Sonnet 来辅助写代码和做分析；Codex 是早期专门做代码生成的模型，比较像agent。  
我个人开发的话最近基本都是codex做high level planning，cursor辅助开发，perplexity和 chatgpt去检索信息，查一些库等等。
---
## Chunk 25 — 多模态有没有做？

多模态有没有做？

只是纯文本吗？  
目前版本主要是文本对话为主，没有做真正的图片识别类多模态。因为这个项目的核心目标不是识别图片，而是解决配件选购、兼容性查询和故障排查这类任务，所以我优先把多轮对话、工具调用、结构化卡片和检索链路做完整。  
但从产品形态上，后续可以扩展多模态，比如用户上传冰箱型号铭牌、损坏零件照片，模型先识别型号或零件特征，再进入现有的 compatibility/troubleshooting 工具链。并且，如果加上多模态，就可以做成skills。
---
## Chunk 26 — Q1. 你怎么写prompt的？

Q1. 你怎么写prompt的？

每一轮用户发问之后，请求是怎么组装的、模型被调了几次、每次输入长什么样？我们的prompt由两部分组成，第一是high level的系统prompt，第二是经过工具调用之后拿着上下文信息去给调用LLM的时候的prompt，也是重点部分。这个prompt是一个参数化 template，里面包含系统指令、历史、本轮输入、工具证据和可选的检索快照。  
1. system：PARTSelect 风格的系统提示词」，关于领域、安全边界、工具策略、语气和输出形态。  
2. history：多轮 user/assistant（纯文本），不含本轮。 3. 当前发送信息 — 本轮 user。 4. tool — 工具回合：assistant（可带 tool_calls）+多条 role: "tool"（JSON）；可能循环多轮。 5. retrieval（grounding） — 内容是 [SERVER_RETRIEVAL_CONTEXT …]+JSON。本质是如果没有调用任何工具的fallback，至少给出一些上下文信息。  
Q2. 十万级零件目录检索优化？在十万级零件数据的检索上，我做的是“精确匹配+文本召回”的组合：对于零件号、兼容关系这些强结构化字段，用 B+树索引做快速精确查找；对于用户的自然语言描述，用 FULLTEXT 倒排索引先召回一批候选。然后在应用层，按照做一次轻量重排序，取 Top-3 结果。这样优化之后的数据一方面用于前端卡片展示，另一方面作为模型上下文输入，这样在保证相关性的同时，也控制了整体延迟。  
FULLTEXT倒排索引是啥？  
倒排索引不是“从文档找词”，而是“从词找文档”。实现上其实是把“词 → 文档”的映射提前建好，查询时直接根据关键词快速召回相关结果，而不是逐条扫描数据。
---
## Chunk 27 — 你的重排序怎么设计的？

你的重排序怎么设计的？

首先，MySQL FULLTEXT 先各拉一批上限 48 条的候选，避免全表扫。其次，重排是在小候选集上做加权计数。比如说如果用户询问了某个症状，那么首先针对症状找可能候选的零件，然后对每条零件看它 symptoms 里有多少条短语和用户话里对得上（子串匹配），也就是『和用户描述重合的症状证据越多越好，命中越多分越高，排序后取 Top‑3，等价于『和用户描述重合的症状证据  
越多越好』。本质上是：召回宽松、重排保守，用少量结构化字段把『更像用户在找的东西』排到前面。  
另外，不同的用户问题有不同的重排序规则差异，询问症状的计数方式和寻找特定零件的规则不同，但是大体都是加权计数。
---
## Chunk 28 — Q2.5. 怎么做的Grounding？

Q2.5. 怎么做的Grounding？

Grounding 本质是：让模型“基于真实数据说话”，而不是瞎编。我的项目里，我用了结构化数据+工具调用+后端控制  
1. 商品信息、价格、兼容性 → 来自 MySQL/catalog 2. 通过 Function Calling 调工具拿数据 3. 前端卡片只渲染工具返回结果（不是 LLM 自己编）
---
## Chunk 29 — 这其实是：工具驱动的 grounding

这其实是：工具驱动的 grounding

项目中如何减少AI幻觉？核心是禁止 LL 直接生成事实数据，流程分层： 1.商品兼容性、库存、型号等事实数据：来自检索、结构化搜索、规则引擎。 2.LLM 仅负责总结、对话回复生成。 3.规则：无检索依据时禁止生成属性，从源头减少幻觉。
---
## Chunk 30 — 怎么做的多模态？

怎么做的多模态？

多模态有没有做，只是纯文本吗  
当前版本主要是文本对话为主，没有做真正的图片或语音多模态，因为这个项目核心是解决配件选购、兼容性和故障排查这类结构化决策问题，我优先把多轮对话、工具调用和检索链路做完整。不过从产品形态上是可以扩展多模态的，比如用户上传设备铭牌或损坏零件图片，先通过视觉模型识别型号或特征，再接入现有的工具链去做检索和诊断。  
为什么做单体agent？我们是很垂直的领域，窄域单 agent+multi-tool；多 agent 更适合长链路、并行分工；对我们这种以目录 grounding 为核心的场景，把能力拆成工具和服务器侧卡片生成更划算，多 agent 不会让事实更真，但会让系统更难控。  
具体哪个地方做了 AI，都扮演什么角色  
AI 在这个系统里主要承担两大角色，我们是 tool-calling agent loop+最终生成，调用次数随任务深度变化。具体讲的话，第一个链路是理解用户意图，然后根据用户意图编排工具调用。举个例子的话，ai先判断用户是在找零件、查兼容性还是做故障排查；然后通过 function calling 决定调用哪个工具，工具链的轮次以及参数；第二的链路是组织成自然语言回复，也就是把把工具返回的结构化结果转换成自然语言回复。关键的商品数据、价格和兼容关系都是来自数据库和工具，而不是模型生成，这样可以避免 hallucination。
---
## Chunk 31 — 如何定的域？

如何定的域？

域是在三层上同时锁定的：第一，产品入口在路由的注释与行为里就声明只覆盖冰箱与洗碗机配件，并在进入昂贵路径前用闲聊、词汇表、域外回复等闸门把大量无关请求挡掉；第二，模型层则在顶层 prompt 里再次声明唯一领域——仅限冰箱/洗碗机的找件、安装、型号兼容与相关故障排查，并明确域外必须礼貌拒绝且不调工具，域内则禁止凭记忆编造目录事实、必须通过 function calling 走 normalize_part_number、lookup_part、 check_compatibility 等在 openaiTools 里注册的能力边界。第三，实际可调用的工具（查件、兼容、症状检索、目录搜索等）本身就构成实现层面的域约束：模型即使「想」答微波炉，也没有对应工具与 grounded 数据链路。
---
## Chunk 32 — 为什么不做embedding？

为什么不做embedding？

（为什么不做RAG？）  
我有考虑过 embedding和RAG，但这个场景里我没有把它作为主检索方式，主要有3个原因。  
1. 数据是强结构化的（最关键）。零件号、型号兼容关系这些是精确匹配问题，不是语义问题。而电商配件是一个高 precision 场景，如果推荐错型号，用户体验和成本都很高，所以我优先保证精确匹配。  
2. embedding 检索需要向量计算和向量索引，在十万级数据下引入额外复杂度，而倒排索引已经能满足大部分需求。  
3. 我把 embedding 当作“补充”而不是主路径，对于 FAQ 或安装说明，甚至用户评价这类文本内容，我会用 embedding 做语义召回，但核心商品检索还是以结构化索引为主。  
Q3. 流式对话实现为什么用fetch NDJSON streaming，不用 SSE或者websocket？  
我当时对比过 WebSocket、SSE 和 fetch streaming，最后选择 fetch+NDJSON streaming，主要是因为这个场景是一个请求驱动的单向流式返回，而不是实时双向通信。用户发起一次请求（带上下文），服务端按 token 流式返回结果，本质还是 HTTP request-response，只是 response 是分块返回的。  
具体实现上，我用的是 fetch+ReadableStream+NDJSON（每行一个 JSON），这样既能支持 POST 传递多轮对话上下文和自定义 header，又能做结构化数据流式渲染。相比 SSE，EventSource 只能 GET、扩展性差；相比 WebSocket，它是长连接双向通信，工程复杂度更高，在这个场景下有点 overkill。所以 fetch streaming 在灵活性和实现成本之间是一个更合适的选择。  
本质上三者底层都是在做流式传输，但我更倾向选择和业务模型最匹配、而不是最强的技术方案。
---
## Chunk 33 — Q4. CDN/浏览器缓存导致 SSE 延迟，怎么解决的

Q4. CDN/浏览器缓存导致 SSE 延迟，怎么解决的

在做流式返回的时候，一个很容易被忽略的问题其实是中间链路，比如我项目里用的是 Vercel，它底层会经过 CDN 和 proxy，这些层默认可能会对响应做缓存、压缩或者 buffering，导致原本应该逐步返回的 chunk 被“攒一波再发”，用户看到的就是先卡住一段时间，然后内容一次性出来。  
解决办法是我在服务端通过设置 Cache-Control: no-cache, no-transform，来避免 CDN 或浏览器对响应做额外处理，保证数据可以按 chunk 实时传输到前端。
---
## Chunk 34 — 怎么发现的这个问题？

怎么发现的这个问题？

本地是流式的，但线上会延迟一段再一起返回，说明中间被 buffer 了。
---
## Chunk 35 — Q5. Chunk的数据结构？

Q5. Chunk的数据结构？
---
## Chunk 36 — Q5. Chunk的数据结构？

我把流式返回设计成基于 NDJSON 的结构化 chunk，每一行是一个 JSON，并通过 type 字段区分不同语义，比如 token 用于逐步追加文本、replace 用于整段替换已有内容、done 用于标记结束并携带结构化数据（比如卡片和推荐操作）。前端根据这些类型分别做拼接、替换或渲染 UI，而不是直接依赖 LLM 的原始文本，从而保证可控性和稳定性。  
Q6. 你的 tool calling 是怎么设计的？  
Tool calling的主要目的是让用户可以通过对话一步步完成任务，让agent主导用户去完成任务，而不是自己去找页面。  
整体流程是模型先解析用户意图，然后根据用户输入的信息里是否有特定词条决定调用哪个工具并生成参数，服务端执行工具后再把json结构化结果返回给模型做最终表达。为了保证稳定性，我限制了最多六轮工具调用，避免出现无限循环，同时通过工具调用，把复杂的用户问题拆成多个步骤，比如先根据症状定位可能问题，再找到对应零件并返回结果。  
然后我设计的这些工具，比如查件、查兼容性、查安装信息和根据症状匹配零件。这些信息都是非常精确，非常细节的，并且这些工具的输入输出都是结构化的，这样可以保证模型调用时更稳定，同时也方便前端做结构化展示。  
tool calling 和 RAG 的区别？  
RAG 是通过检索相关文本作为上下文，让模型基于这些文本生成回答，适合知识型问题  
tool calling 是直接调用函数获取结构化数据，适合需要精确结果或执行操作的场景，比如查商品、判断兼容性。  
在实际系统中，两者可以结合使用，比如先用 RAG 获取候选信息，再用 tool 做精确查询  
Q7. 选的啥模型？选型阶段优先考虑的是对话式导购+函数调用这条路径能不能稳定落地。openai的模型偏「工程落地、接口丰富、Agent 样板多」。而像Claude偏向长文与细致指令：历史上常被提的是长上下文、长文档里跟指令（「按格式写、别漏约束」），适合报告、合规类长稿、复杂 prompt
---
## Chunk 37 — Q5. Chunk的数据结构？

我现在测试阶段用 mini，是为了快速验证链路和控制成本。如果上线，我会优先选择 gpt-4.1 或 GPT-5这类低延迟、工具调用能力比较稳定的模型作为主链路，因为我的系统关键数据都来自工具和数据库，模型主要负责理解意图、编排工具和组织回复。  
Q8. 越域拦截是怎么做的？  
我没有只依赖 system prompt 去约束模型，因为 prompt 本身不是强约束。我的做法是在服务端先做一层确定性的意图识别：先判断用户问题是否属于冰箱/洗碗机配件相关场景，比如查件、兼容性、安装指导、故障排查这些 intent。如果明显是无关问题，比如闲聊、代码、新闻、其他品类，就直接返回固定的拒答模板，不进入后续 tool calling 流程。  
对于一些模糊但可能相关的问题，我不会直接拒绝，而是让 agent 追问关键信息，比如 appliance type、part number 或 model number。也就是说，我把问题分成三类：明确相关就进入工具链，明确无关就拒答，信息不足但可能相关就澄清。这样比单纯靠模型自己判断更稳定，也更符合这个 case study 里要求 agent 保持在 PartSelect 配件场景内的要求。  
Q8. 多轮对话是怎么处理的？  
每一轮都是 POST/api/chat，没有服务端会话库；多轮信息全靠请求里带过来。  
发当前这句 message；最近 10 条 user/assistant 保持原文放进 history；更早的对话压成一段 conversation_summary（滚动摘要）一起发。一轮回复结束后，更新摘要，摘要存在 localStorage，和聊天记录一起持久化。
---
## Chunk 38 — RAG是什么

RAG是什么

RAG = Retrieval-Augmented Generation（检索增强生成），可以记成两句话：  
先检索：从一堆「资料片段」里，找出和用户问题最相关的几段文字。再生成：把这几段文字塞进给模型的上下文里，让模型照着资料回答，减少瞎编。重点是找出上下文，答案要 grounded（有依据）时，先把依据找出来再给模型。  
我这块主流程其实是本地目录里的结构化检索，不算典型 RAG。更像 RAG 的一层是可选的轻语义检索：离线用脚本把评价故事、FAQ、安装说明切成小段，用 text-embedding-3-small 打成向量，存进 embeddings.json。用户一问，同一模型给问句也打个向量，在内存里和每一段算相似度，过个分数门槛，取最相关的几条短摘录交给模型参考。
---
## Chunk 39 — Q9. 为什么更注重精确率

Q9. 为什么更注重精确率

这里是真实电商场景，售卖的不是虚拟的玩具而是可执行的决策：用户会依据你的回答去下单、备货、拆机。一旦错一个订货好吗、错一条兼容结论、错一段安装顺序，直接后果是买错件、装不上、退货、安全风险，非常影响用户体验和信任。所以从产品目标上，「说错」的代价远高于「没说全」。  
精确率对应的就是：宁可少说、少推，也不要把错误信息包装得很自信。例如：型号没对齐就先问清楚；本地目录没命中就走澄清或兜底抓取，而不是硬凑三个「看起来像」的件；语义检索里还  
有相似度阈值，低相关片段宁可不喂给模型，避免「引用了一段其实不靠谱的客评」去支撑结论。
---
## Chunk 40 — 召回率？

召回率？

召回不是不要，而是放在对的地方、用对的形式。症状类、浏览类本身就需要多候选，你会用候选列表、排序、建议追问（chips）让用户缩小范围——这是有边界的召回：可以列出几条「可能相关」，但每条仍应能对应到目录或明确来源，并避免把不确定的兼容说成确定。  
精确率 vs 召回率（先严后宽在干什么）召回率：用户该找的东西里，有多少被你们找回来（找全了吗）。精确率：你们找回来的东西里，有多少真的是对的（乱的多不多）。
---
## Chunk 41 — 答案：

答案：

我把 UI 分成三层：自然语言回复、结构化卡片和下一步建议。自然语言负责回答问题，卡片负责展示结构化信息，比如商品详情或兼容结果，而 suggestions 用来引导用户下一步操作，比如查看安装步骤或检查兼容性。这种设计可以避免长文本，同时让用户更容易完成任务，比纯聊天体验更接近真实电商场景。  
Q10. 如果扩展到生产环境，你会怎么做？  
数据与系统：用真实商品、库存、价格、订单、物流接口的数据库替换本地 catalog.json  
检索与 RAG：文档和数据库（也就是知识库）规模扩大以后，把现在的内存暴力扫换成向量数据库，做更真实的rag；结构化字段（PS、型号、SKU）仍保留精确匹配优先，向量检索主要承接模糊的问题、来自顾客的评价等等。  
AI agent 怎么帮到「真的下单」：现在 demo 里已经有模拟购物车，上生产我会把它升级成一条清晰的任务型 agent 路径：识别用户是在找件 → 核对兼容 → 比价/库存 → 加购 → 结算，和嵌入式结账组件打通，减少「聊完还要自己找页面」的断点。对高风险话术（保修承诺、到货时间、法律条款）用模板+规则或只引用接口返回字段，不让模型自由发挥。  
人与兜底：人工客服接复杂纠纷、大额或多次失败下单；agent 负责摘要上下文、预填工单、标优先级。
---
## Chunk 42 — 答案： > 0. React为什么快？

答案： > 0. React为什么快？

（三个原因）  
1. Virtual DOM 本质上是 React 在内存中维护的一棵 UI 描述树。React 在状态变化后，先生成新的 Virtual DOM，再和旧树比较，最后只把必要的变化同步到真实 DOM，从而减少高成本的 DOM 操作。 2. diff 算法的作用是比较新旧 Virtual DOM，找出最小变更集合。React于同层比较和 key优化，尽量复用已有节点，只更新真正变化的部分，从而减少更新范围。 3. Batching 指的是 React 会把同一时机内的多次 state 更新合并处理，而不是每次 setState 都立刻触发一次完整渲染流程。这样可以减少 render、diff 和 commit 的次数，从而降低整体更新成本。
---
## Chunk 43 — 答案： > 1. State

答案： > 1. State

定义：state 是组件内部维护的数据，会随着用户交互或逻辑变化而更新，state 变化会触发组件重新渲染。  
setState是同步还是异步：看场景，但通常表现为异步（批处理）React 会对多个 state 更新做 batching，合并后再统一更新，提高性能
---
## Chunk 44 — 答案： > 2. Props

答案： > 2. Props

定义：props 是组件的输入参数，来源是外部，用于从外部向组件传递数据，本质是一个对象。 React 的设计是单向数据流，props 是数据从父到子的传递方式。  
不可变性：props 是只读，不可变的（immutable），组件不能修改自己的输入，否则会破坏数据流的可预测性  
Props变化会发生什么：组件重新渲染（React.memo可以跳过rerender如果props不变）  
Props VS State: props 是外部传入的，只读；state 是组件内部维护的，可修改。 props 用来做数据传递，state 用来做组件内部状态管理。
---
## Chunk 45 — 答案： > 3. JSX

答案： > 3. JSX

JSX 是 JavaScript 的语法扩展，本质会被编译成 React.createElement 调用
---
## Chunk 46 — 答案： > 4. 组件

答案： > 4. 组件

组件本质是一个函数，输入 props，输出 UI，是最小UI复用单元。
---
## Chunk 47 — 答案： > 5. 受控组件VS非受控组件（表单问题）

答案： > 5. 受控组件VS非受控组件（表单问题）

受控组件是指表单的值由 React 的 state 控制，用户输入的每一次变化都会同步到 state，例如 <input><select><textearea>等元素都要绑定一个change事件，当表单的状态发生变化，就会触发onChange事件，更新组件的state。这种组件在React中被称为受控组件，适合表单的复杂交互。
---
## Chunk 48 — 啥时候用：

啥时候用：

1. 实时校验（密码强度，邮箱格式，输入限制） 2. 表单联动（输入国家，自动选城市） 3. 动态UI控制（按钮disable，显示错误提示） 4. 数据需要同步到别的地方（redux，表单预填）  
受控组件缺陷：表单元素的值都是由React组件进行管理，当有多个输入框，或者多个这种组件时，如果想同时获取到全部的值就必须每个都要编写事件处理函数，这会让代码看着很臃肿，所以为了解决这种情况，出现了非受控组件。  
非受控组件是由 DOM 自己管理数据，React 通过 ref 获取值。适合简单输入。啥时候用：  
1. 简单表单 2. 文件上传（因为浏览器出于安全考虑，不允许通过 JS 设置文件内容。） 3. 性能敏感，大表单（避免每输入一个字 → render）  
JavaScript//受控 <input value={value} onChange={e => setValue(e.target.value)}/>
---
## Chunk 49 — 啥时候用： > 6. 单向数据流

啥时候用： > 6. 单向数据流

React 是单向数据流，数据从父组件通过 props 传递到子组件，子组件不能直接修改数据，只能通过回调通知父组件更新。
---
## Chunk 50 — 啥时候用： > 7. 事件、原生事件、合成事件、事件委托、事件冒泡

啥时候用： > 7. 事件、原生事件、合成事件、事件委托、事件冒泡

在浏览器中，事件指的是用户交互或系统触发的行为，比如 click、input 等，这些由浏览器原生提供的事件称为原生事件，通常通过 addEventListener 绑定。而在 React 中使用的是合成事件（SyntheticEvent），它是对原生事件的一层封装，提供统一的 API（如 preventDefault、 stopPropagation），并屏蔽不同浏览器之间的差异，同时也方便 React 将事件系统与自身的更新机制（如批量更新、调度）结合。
---
## Chunk 51 — 为什么React不用原生事件？

为什么React不用原生事件？

1. 兼容性：屏蔽不同浏览器差异 2. 性能：通过事件委托减少事件绑定数量 3. 统一API：开发体验更一致
---
## Chunk 52 — 事件委托：

事件委托：

React 使用事件委托机制，在 root container 上统一绑定事件监听器。当浏览器事件从目标元素冒泡到 root 时，React 会根据 event.target 在 Fiber 树中找到对应的组件，并构建一条从子到父的事件链路，然后按照这个路径依次调用组件的事件处理函数，从而实现类似冒泡的效果。这样可以减少事件监听器数量，同时通过 SyntheticEvent 统一不同浏览器的行为。
---
## Chunk 53 — 事件委托： > 8. Children

事件委托： > 8. Children

children 是 React 提供的一个特殊 props，表示组件的子节点内容。
---
## Chunk 54 — 事件委托： > 9. 组件通信方式总结

事件委托： > 9. 组件通信方式总结

父 → 子：props ● 子 → 父：回调函数 ● 兄弟组件之间：提升到共同父组件（A → Parent → B） ● 跨层级组件：Context ● 全局状态：Redux
---
## Chunk 55 — 选择原则：

选择原则：

简单场景：props  
● 跨层级：Context ● 多组件共享复杂状态：Redux  
一、组件树、Virtual DOM、真实DOM 组件树： React 组件树是由 React 组件按父子关系组成的树状结构，描述的是应用的组件层级关系，React 组件树 ≠ DOM，也 ≠ Virtual DOM。  
组件树（函数结构） ↓ render Virtual DOM（描述UI） ↓ commit 真实 DOM（浏览器）
---
## Chunk 56 — body ├── root

body ├── root

│ └── App
---
## Chunk 57 — └── Modal

└── Modal

Virtual DOM Virtual DOM 是 React 在内存中维护的一棵轻量级 JavaScript 对象树，本质是JS对象用来描述 UI 的结构和状态。  
通过diff算法对比新旧 Virtual DOM，计算出最小变更，再更新真实 DOM，从而提升性能和开发体验。虚拟 DOM 不会进行排版与重绘操作，而真实 DOM 会频繁重排与重绘。Virtual DOM在更新时快，在应用初始时不一定快。
---
## Chunk 58 — 优点：

优点：

● 简单方便：如果使用手动操作真实 DOM来完成页面，繁琐又容易出错，在大规模应用下维
---
## Chunk 59 — 护起来也很困难

护起来也很困难

性能方面：使用 Virtual DOM，能够有效避免真实 DOM 数频繁更新，减少多次引起重绘与重排，提高性能  
跨平台：React 借助虚拟 DOM，带来了跨平台的能力，一套代码多端运行
---
## Chunk 60 — 缺点：

缺点：

首次渲染大量 DOM 时，由于多了一层虚拟 DOM 的计算，所以初始的时候速度比正常稍慢  
真实DOM 真实DOM 是浏览器将 HTML 文档解析成的一棵树状对象结构，是页面最终渲染在屏幕上的结构。
---
## Chunk 61 — 二、React生命周期

二、React生命周期

https://juejin.cn/post/6871728918643081230
---
## Chunk 62 — 二、React生命周期 > 1. Class Component 类组件生命周期

二、React生命周期 > 1. Class Component 类组件生命周期

a. 三个阶段：创建时，更新时，卸载时 b. componentDidMount，componentDidUpdate，componentWillUnmount c. shouldComponentUpdate判断当前是否需要更新，重新渲染
---
## Chunk 63 — 二、React生命周期 > 2. Function Component 函数组件生命周期

二、React生命周期 > 2. Function Component 函数组件生命周期

a. useEffect：使用 useEffect 相当于告诉 React 组件需要在渲染后执行某些操作，  
React 将在执行 DOM 更新完成之后调用它。
---
## Chunk 64 — ■ 浅比较依赖数组里的内容，只要内存地址没变就不重新执行effect

■ 浅比较依赖数组里的内容，只要内存地址没变就不重新执行effect

基本类型：值比较 ● 引用类型：比较地址（如果依赖数组里有普通函数，那么函数在每次 render 时都会重新创建）  
■ 因此：每次新建对象/函数 → 会触发effect，需要用useCallback包装过的函
---
## Chunk 65 — 数/useMemo保证引用稳定

数/useMemo保证引用稳定

■ 只传入[ ]就是只mount时候render一次 ■  
useEffect本质上是一个闭包，会捕获定义时的变量，如果依赖数组没有写全，就可能出现 stale closure，导致使用定义时候的旧的 state。  
useCallBack  
■ useCallBac，useMemo也里都有依赖数组，如下图query
---
## Chunk 66 — function Parent(){

function Parent(){

const [query,setQuery] = useState('q');
---
## Chunk 67 — const fetchData = useCallback(()=>{

const fetchData = useCallback(()=>{

...省略函数体的具体实现  
},[query]);  
return <Child fetchData={fetchData}/>  
}
---
## Chunk 68 — function Child({fetchData}){

function Child({fetchData}){

const [data,setData] = useState(null);
---
## Chunk 69 — useEffect(()=>{

useEffect(()=>{

fetchData().then(setData);  
},[fetchData])//经过 useCallback 包装过的函数fetchData，可以当作普通变量作为 useEffect 的依赖 }
---
## Chunk 70 — useEffect(()=>{ > 1. 调和阶段

useEffect(()=>{ > 1. 调和阶段

a. render阶段执行组件函数，计算Virtual DOM（纯计算，不操作DOM） b. diff阶段 shouldComponentUpdate/React.memo
---
## Chunk 71 — useEffect(()=>{ > 2. 提交阶段

useEffect(()=>{ > 2. 提交阶段

a. commit阶段：真正更新DOM，不可中断，commit之后异步执行useEffect
---
## Chunk 72 — setState之后发生了什么？

setState之后发生了什么？

setState ↓ 【调和阶段（可中断）】 ↓ 1. 执行 render（函数组件执行） 2. 生成新 Virtual DOM 3. diff（比较新旧） ↓ 【提交阶段（不可中断）】 ↓ 4. 更新真实 DOM 5. 执行 layout effects（useLayoutEffect） ↓ 6. 异步执行 useEffect
---
## Chunk 73 — setState之后发生了什么？ > 四、React渲染机制

setState之后发生了什么？ > 四、React渲染机制

React 渲染机制的核心是：状态变化 →重新执行组件函数（类组件，函数组件） → 生成新的 Virtual DOM → diff → commit。即使最终 DOM 没变化，组件函数执行本身也有开销（hooks、计算、子组件递归）  
性能优化的关键是控制re-render 次数，比如通过 memo、useMemo、useCallback 等方式减少不必要的组件执行。  
re-render触发条件 ● state变化 ● props变化 ● 父组件render，默认情况下子组件默认重新渲染（可以通过React.memo阻止） ● 如果组件订阅了 context、Redux store 等外部状态，那这些订阅值变化时也会触发更新  
React.Memo优化：通过 props 的浅比较，如果props没变则可以跳过子组件重新渲染，避免子组件不必要的重新渲染。  
传对象/函数 → 每次都是新引用 → memo失效 ● 需要 useMemo/useCallback 保持稳定  
React.Memo VS useEffect React.Memo是浅比较传进来的props，控制“组件是否重新执行，重新渲染”，发生在render前。 useEffect里比较比较依赖数组的值，控制的是是否执行副作用函数，发生在commit后。虽然他俩都是浅比较，但是目的完全不同。  
如果React.memo生效，那组件根本没 render，更不会commit，那么useEffect 不会执行，但反过来useEffect 不执行 ≠ 组件没 render。
---
## Chunk 74 — JavaScript

JavaScript

const Child = React.memo((props) => {
---
## Chunk 75 — console.log("render")

console.log("render")

})
---
## Chunk 76 — console.log("effect")

console.log("effect")

}, [a])  
Key优化： key 是 React 在 diff 阶段用来标识节点身份的，用于判断节点是否可以复用。如果 key 相同且类型相同，React 会复用已有 DOM，否则会重新创建节点。推荐使用稳定且唯一的 id。
---
## Chunk 77 — 为什么不能用index？

为什么不能用index？

如果使用 index（位置）作为 key，在列表发生插入或删除时会导致 key 变化，从而引发错误的节点复用。如果是静态列表，没有增加/删除/排序操作，那么可以用index。
---
## Chunk 78 — 为什么不能不写key？

为什么不能不写key？

不写 key 的问题：默认等于把index当key，React 按位置比较，列表变化时会错位复用
---
## Chunk 79 — flatlist与虚拟化列表

flatlist与虚拟化列表

FlatList 的是react native的虚拟化列表，只渲染可见区域，相比 ScrollView 更适合长列表，降低内存占用和滚动卡顿。  
执行方式：它只渲染当前视口附近的 item，并维护一个渲染窗口。在滚动过程中，已经离开视口的 item 对应的原生视图会被回收，然后复用这些视图去渲染新的数据，而不是不断创建新的 view。在Menu中我主要用flatlist来做了购物车列表和优惠卷列表。要注意用 keyExtractor 保证 key 稳定，避免diff重渲染问题或者复用错误等问题。
---
## Chunk 80 — 五、diff算法

五、diff算法

diff就是比较react的新老虚拟DOM的过程。  
1. Tree diff优化。react使用分层对比策略，只对对相同层级节点进行比较。如果发生跨级操作，React 不能复用已有节点，可能会导致 React 进行大量重新创建操作，这会影响性能。尽量避免跨层级的操作。  
2. Component diff优化。如果是同类型组件，首先使用 shouldComponentUpdate()方法判断是否需要进行比较，如果返回true，继续按照比较。如果是不同类型的组件，则将该组件判断为 dirty component，从而替换整个组件下的所有子节点。  
3. Element diff优化，用唯一key优化。React 首先会对新集合进行遍历，通过唯一 key 来判断老集合中是否存在相同的节点。然后复用已有节点，减少节点的删除和创建操作。 a. key的作用：帮助diff识别节点，实现复用 b. 不写key的问题：状态错乱+不必要的重渲染 c. 为什么不能用index：顺序变化会导致复用错误
---
## Chunk 81 — 六、Fiber

六、Fiber

Fiber： Fiber主要解决渲染复杂组件时卡顿的问题。在旧版本 React 中，diff 是同步递归执行的，一旦开始就不能中断，如果组件树很大就会导致页面卡顿。而Fiber 把 diff 过程拆成很多小任务，并且可以根据任务优先级进行调度也可以中断，在需要的时候让出主线程，比如优先处理用户输入（用户输入>动画>请求），从而提升页面的响应性。实现： React 实现了一个类似链表的数据结构，将原来的递归diff 变成了现在的遍历diff，这样就能做到异步可更新了  
触发更新时，Fiber分为调和（调度）阶段（可以中断）和提交阶段（不可中断）。  
第一步：调和阶段（Reconciliation）：  
计算新旧 Virtual DOM 的差异（diff） ● 找出哪些组件要更新 ● 生成“更新计划” ● 调和阶段可以中断，假设页面很大，有 1000 个组件要 diff，那么React不会一次性算完，而是算一点停一下（让浏览器处理点击/输入），再继续
---
## Chunk 82 — 第二步：提交阶段（Commit）

第二步：提交阶段（Commit）

修改真实 DOM ● 执行生命周期/useEffect  
Scheduler：调度优先级的执行时机。（是否打断/是否让出主线程）用浏览器的时间片异步执行 Fiber的工作单元 Lane：管理/判断各个任务优先级。各个Fiber工作单元也可以比较优先级，相同优先级的任务可以一起更新。
---
## Chunk 83 — 七、React的CSR和SSR

七、React的CSR和SSR

CSR： CSR 是浏览器先拿到一个空壳 HTML，再下载并执行 JS，通过请求接口获取数据，然后由 React 在客户端完成页面渲染。csr的出现实现了前后端架构分离。一般后台系统/交互多的用 CSR。缺点：不利于seo（爬虫是空html）和首次渲染时间长（要等JS下载+执行+请求数据）  
SSR：SSR 是在服务器完成数据获取和页面渲染，直接返回完整 HTML 给浏览器，浏览器只需要做 hydrate 就可以变成可交互页面。一般内容展示类网站用SSR。缺点: 会增加项目整体复杂度，对服务器压力大  
SSR页面怎么变成可交互的？要让页面支持交互需要搭配 hydrate 使用。此外，hydrate 也会检查服务端与客户端的内容是否匹配。
---
## Chunk 84 — 八、React及前端相关性能优化

八、React及前端相关性能优化

前端性能优化本质是：减少网络请求+资源加载优化+React优化+减少渲染开销。  
1. 网络层优化：HTTP缓存（强缓存+协商缓存），减少请求数量（合并/缓存），debounce/throttle（减少频率）  
2. 资源加载优化：代码分割（code splitting），路由懒加载（import()），首屏资源优先加载 3. 渲染开销优化：减少回流（reflow），避免频繁 DOM 操作 4. React 层优化：React.memo避免子组件重复渲染，基于 props 浅比较，useMemo/useCallback，selector（只订阅必要数据），拆组件，缩小更新范围
---
## Chunk 85 — 九、Hooks钩子函数

九、Hooks钩子函数
---
## Chunk 86 — 九、Hooks钩子函数

Hooks是React的逻辑复用和函数组件状态管理。 Hooks 解决了函数组件也能用 state/生命周期的问题。Hook只能写在函数组件里。  
为什么Hook不能写if里 React 并不是通过变量名来识别 Hook，而是依赖每次 render 时 Hook 的调用顺序来绑定 state。如果 Hook 在条件/循环语句中调用，会导致顺序变化，从而引起 state 错乱，所以必须在顶层调用。  
状态管理：useState useState会重新渲染，因为React察觉state change后会schedule update，render，diff，commit  
数据获取：useEffect useEffect处理副作用，包括请求API，订阅/取消订阅，监听state变化，注册事件，清理定时器， render → commit → effect  
useEffect 本身不参与渲染过程，它是在组件渲染并提交到 DOM 之后执行的副作用逻辑。但是它的执行是由 render 阶段决定的，比如依赖数组的变化是在 render 时比较的，因此它和渲染是有关联的。  
useEffect 会不会导致重新渲染？ useEffect 本身不会触发 render，但如果在 effect 里调用了 setState，就会触发新的 render。  
useEffect 执行时机 useEffect 会在组件 render 完成并 commit 到 DOM之后执行。它是异步执行，属于副作用阶段（effect phase），不会阻塞浏览器UI渲染。如果定义了 cleanup 函数，那么在下一次 effect 执行之前，或者组件卸载时，会先执行 cleanup。  
useEffect VS useLayoutEffect 这俩都是在commit到DOM之后执行的。  
useEffect是异步执行，不会阻塞页面渲染。会先看到旧位置再闪一下出来新的；render → commit DOM → 浏览器绘制 → useEffect
---
## Chunk 87 — 九、Hooks钩子函数

useEffect是异步执行，不会阻塞页面渲染。会先看到旧位置再闪一下出来新的；render → commit DOM → 浏览器绘制 → useEffect  
useLayoutEffect 是同步执行，会阻塞渲染，用户看到的是“执行完 effect 后的结果”，常用于DOM测量。render → commit DOM → useLayoutEffect → 浏览器绘制  
非UI的跨渲染保存可变值：useRef useRef可以在组件多次渲染之间保存一个可变的值，他不是响应式的，修改这个值不会触发重新渲染。它常见的用途是获取 DOM 节点，比如 input focus，或者保存一些不需要参与 UI 渲染的数据，比如定时器、上一次的值等。和 useState 的区别是，useState 会触发更新，而 useRef 不会。  
性能优化：useCallback&useMemo&React.Memo（不是hook） useMemo → 缓存计算结果。由于每次state change React都要component re-render，所有组件里的代码都要重新执行，如果代码里有很重的计算（排序、filter），那算这些很慢，就会影响性能，因此React使用useMemo包裹这个组件来缓存计算结果，只有dependency变化才重新计算。  
useCallback → 缓存函数，让函数不要每次rerender都变成新的（在依赖不变时，返回同一个函数引用。）  
useMemo VS useCallback useMemo 和 useCallback 都可以通过缓存引用，来避免之后传入到props的引用变化，从而配合 React.memo 减少子组件的重新渲染。useMemo 用于缓存值，比如对象或数组，而 useCallback 用于缓存函数引用，本质上是 useMemo 的语法糖，但语义更清晰。用 useCallback的话在很多传递点击事件的时候，比如点击购物车，能保证函数的props引用稳定
---
## Chunk 88 — 九、Hooks钩子函数

React.memo VS useMemo React.memo 本质是减少重新渲染。会对组件的 props 做浅比较。如果新旧 props 没有变化， React 可以跳过这个子组件的重新渲染。useMemo是避免组件函数重新执行时，里面很大的计算开销重复执行。  
shouldComponentUpdate VS React.memo shouldComponentUpdate 是类组件中控制是否重新渲染的生命周期方法，可以根据 props 和 state 自定义判断逻辑。React.memo 是函数组件的优化方式，默认对 props 做浅比较来避免不必要的渲染，也可以传入自定义比较函数。相比之下，shouldComponentUpdate 更灵活，而 React.memo 更简洁。
---
## Chunk 89 — 啥时候需要自定义Hooks？

啥时候需要自定义Hooks？

1. 多个组件用同一套逻辑，比如获取数据useUser 2. 逻辑复杂：loading/error/data 三状态，debounce/throttle 3. 需要封装“行为”，useDebounce，useLocalStorage，useAuth 4. 状态+副作用强绑定，比如state+useEffect+cleanup  
在项目中，如果多个页面都需要请求用户信息或处理类似的副作用逻辑，我会封装成自定义 Hook，比如 useUser 或 useFetch，来避免重复代码并统一逻辑。
---
## Chunk 90 — 啥时候需要自定义Hooks？ > 十、Context系统

啥时候需要自定义Hooks？ > 十、Context系统

Context用来实现跨组件共享数据，防止prop drilling。Context对象包括currentValue，Provider和 Consumer。Context不适合高频率更新，因为Provider更新会导致所有Consumer重新render。解决方法是分多个Context，或使用Redux/selector减少更新范围。
---
## Chunk 91 — 原理：

原理：

Provider 存 value ● Consumer/useContext 订阅 ● Provider更新，context value 变化 → 所有Consumer组件重新 render
---
## Chunk 92 — 十一、React Router

十一、React Router

路由的本质是根据 URL 决定渲染哪个组件，比如/home → 渲染 Home组件，/about → 渲染 About组件。  
React Router 用于实现前端路由，让单页应用在不刷新页面（也就是不触发浏览器重新请求页面）的情况下切换视图组件。（普通的方式加一个路由就要重新请求页面）  
核心原理：通过监听 URL 变化（history API 或 hash），匹配对应组件进行渲染，而不是重新请求页面。  
hash 模式是通过 URL 中的#来实现路由，比如/#/home，它通过监听 hashchange 事件来感知路由变化。他不会触发页面刷新，是因为 hash 部分不会发送给服务器。  
history 模式是基于 HTML5 的 History API，比如 pushState 和 replaceState。他也是可以在不刷新页面的情况下修改 URL，比如/home。另外，它通过监听 popstate 事件来处理浏览器前进后退。相比 hash 模式，history 模式 URL 更干净，但需要服务端配置 fallback，把未知路径都返回 index.html，否则刷新子路由时可能出现 404。  
两者的主要区别是：hash 模式不需要后端支持但 URL 不美观，而 history 模式 URL 更像真实路径，但需要后端做统一路由处理，否则直接刷新xxx/home会 404。
---
## Chunk 93 — 前端路由为什么不会刷新？

前端路由为什么不会刷新？

前端路由之所以不会刷新，是因为它使用了 history.pushState 这种方式来修改 URL，这个 API 只会改变地址栏和历史记录，不会触发浏览器重新请求页面
---
## Chunk 94 — 前端路由为什么不会刷新？ > 十二、Error Boundary

前端路由为什么不会刷新？ > 十二、Error Boundary

Error Boundary：React某个局部组件报错了，不要把整个应用带死，而是只让这一块显示“出错了” 的兜底界面。它把“整页崩溃”变成了“局部降级”，提升应用稳定性。
---
## Chunk 95 — Error Boundary能捕获什么错误？

Error Boundary能捕获什么错误？

只要是 React 在“渲染组件树”这个过程中发生的错误，它比较擅长兜住。
---
## Chunk 96 — Error Boundary不擅长捕获什么错误？

Error Boundary不擅长捕获什么错误？

1. 事件处理相关，比如onClick 2. 异步代码里的错误，因为异步代码不是在 React 同步渲染子树时抛出来的，要自己  
try/catch
---
## Chunk 97 — 十三、Portal

十三、Portal

portal：让一个子组件在 React 组件树里还是原来的位置，但生成出来的真实 DOM 可以插到别的地方去。用于modal，dropdown，解决明明想让 Modal 遮住整个屏幕，结果它被某个父容器裁掉了。  
api是ReactDOM.createPortal(child, container)。child：你要渲染的内容，container：你想把这段 DOM 插到哪个真实 DOM 节点里。一般在 index.html 里预先定义一个 DOM 节点，比如 modal-root，然后通过 document.getElementById 获取。
---
## Chunk 98 — 十四、React其他

十四、React其他

StrictMode StrictMode 是 React 开发模式下的检查工具，只在开发环境生效，用来检测副作用是否安全，比如是否有未清理的 effect、是否有不安全的生命周期逻辑等。比如开发环境下 useEffect 可能执行两次。  
React 18 并发更新 React 18（最新）引入并发更新（Concurrent Rendering），可以让渲染任务“可打断”。核心能力是自动批处理（automatic batching）。它扩大了自动批处理范围，异步回调中的多个 state 更新也可以合并。  
React 在 16 引入 Fiber 架构后具备了可中断渲染的能力，但在 18 之前默认仍然是同步渲染。 React 18 通过 Concurrent Rendering 真正启用了这些能力，比如可中断渲染、优先级调度和自动批处理。Fiber 是实现并发能力的基础，而 Concurrent Rendering 是对这些能力的真正使用。
---
## Chunk 99 — 任务切片VS时间切片

任务切片VS时间切片

任务切片是把任务拆小，而时间切片是让任务可以被中断并分时间执行，避免长时间阻塞主线程。
---
## Chunk 100 — MVVM

MVVM

MVVM解耦了 UI 和数据。Model是数据层，View是UI层，ViewModel 作为中间层负责管理状态和业务逻辑，并通过数据绑定机制（双向绑定）让 View 和 Model 自动同步。  
React本质不是MVVM，他是一个专注于 View 层的 UI 库（View Library）。Vue是MVVM。
---
## Chunk 101 — React VS React Native

React VS React Native

React 和 React Native 的核心思想是一样的，都是基于组件化和 Virtual DOM，但它们的渲染目标和底层实现完全不同。React渲染到浏览器 DOM，React native渲染到原生组件，React Native 通过 Bridge 或 JSI 把 JS 逻辑和原生 UI 连接起来。React是事件委托，React native直接就使用原生事件。React native的性能瓶颈是JS ↔ Native 通信成本（Bridge）。  
Bridge/JSI React Native 以前通过 Bridge 做异步通信，现在新架构通过 JSI 直接调用，减少序列化开销。  
React Native三线程模型 React Native 的三线程模型主要包括 JS 线程、UI 线程和 Shadow 线程，分别负责业务逻辑、界面渲染和布局计算，它们之间通过异步机制协作完成界面更新。
---
## Chunk 102 — 十六、Redux

十六、Redux

Redux解决多组件共享状态的问题，通过单一数据源和单向数据流，让状态变化可预测 Action：在Redux中使用 Action的时候， Action文件里尽量保持 Action文件的纯净，传入什么数据就返回什么数据，最好把请求的数据和 Action方法分离开，以保持 Action的纯净。
---
## Chunk 103 — Redux 三大原则

Redux 三大原则

1. 单一数据源：整个应用的共享状态，放在一个统一的 store 里管理。 2. state 是只读的：组件不能直接去改 store 里的状态，必须通过 dispatch 一个 action 来表达“我要发生什么变化”。  
3. 使用纯函数修改状态：state 怎么变，交给 reducer 这个纯函数来计算。纯函数的意思是同样输入一定得到同样输出，不依赖外部环境，不直接改原数据。不做副作用
---
## Chunk 104 — Redux 三大原则 > 1. 多组件共享复杂状态

Redux 三大原则 > 1. 多组件共享复杂状态

用户登录信息 ● 购物车 ● 全局筛选条件
---
## Chunk 105 — Redux 三大原则 > 2. 状态流转复杂

Redux 三大原则 > 2. 状态流转复杂

点击 → 请求 → 成功 → 更新多个模块
---
## Chunk 106 — 为什么 reducer 不能直接原地修改 state（i.e.为什么immutable)

为什么 reducer 不能直接原地修改 state（i.e.为什么immutable)

reducer 不能直接改 state，是因为 Redux 依赖“不可变更新”来保证状态变化可追踪、可比较、可调试。不要修改原对象，而是应该返回一个新对象。  
1. 方便判断“数据有没有变”，React 和 Redux 很多优化都依赖浅比较。 2. 状态变化更可预测，如果 reducer 里可以随便改原 state，就会出现很多副作用式写法。这样状态到底是谁改的、什么时候改的，会很乱。  
3. 支持调试工具：Redux DevTools 能回放 action、看每一步 state 变化，本质上就依赖每次都生成一个新的状态快照。如果你原地修改，就很难回看历史。
---
## Chunk 107 — Redux 单向数据流有什么好处？

Redux 单向数据流有什么好处？

Redux 的数据流是：dispatch → reducer → new state → UI update，整个过程是单向的。单向数据流的本质是把“状态修改入口收敛到一个地方”，保证可预测性，方便debug。双向绑定（Vue）在复杂应用中容易出现状态不一致的问题。  
React-Redux：Provider/useSelector/useDispatch  
Provider：把 store 注入到 React 组件树里，让子组件都能访问到它。 useSelector: 从 store 里读取你需要的那一部分状态。 useDispatch: 拿到 dispatch 函数，用来派发 action。
---
## Chunk 108 — useSelector 为什么会触发重渲染，怎么优化

useSelector 为什么会触发重渲染，怎么优化

useSelector 会在 store 更新时重新执行 selector。然后拿本次 selector 返回值和上次返回值做比较。默认比较方式是严格相等 ===。如果结果不相等，组件才会重新渲染。
---
## Chunk 109 — 优化：

优化：

1. useSelector 最好只选择当前组件真正需要的最小字段，减少无意义的引用变化带来的重渲染。比如写user.name就比写user好  
2. 避免在 selector 里直接返回新对象，会导致===一定跟之前值不想等。从而重新执行 selector  
3. 手动使用使用浅比较，比如 React-Redux 提供 shallowEqual。而shallowEqual 会做一层浅比较是比较对象里每个key和value是否相等。比如只要prev.name === next.name&&prev.age === next.age就认为没变。
---
## Chunk 110 — Redux-thunk vs Redux-saga

Redux-thunk vs Redux-saga

他们都是Redux 中处理异步逻辑和副作用的中间件方案。因为 Redux 原生 reducer 必须是纯函数，不能在 reducer 里发请求。所以异步逻辑得放外面。  
Redux-thunk 是通过让 action 返回函数来处理异步逻辑，适合简单请求。 Redux-saga 则基于 generator，可以更优雅地处理复杂异步流程，比如并发控制、请求取消、防抖节流等，因此在复杂业务场景中更适合使用 saga。
---
## Chunk 111 — 结合实习的Cart为什么选用Saga？

结合实习的Cart为什么选用Saga？

在购物车场景里，我觉得 saga 比 thunk 更适合，因为购物车不只是简单拉一次数据，它往往会涉及多个异步动作的协调，比如获取购物车、更新商品数量、删除商品、重新计算总价，以及处理用户快速连续操作。Saga 更适合做这种流程控制，比如只保留最后一次请求、统一处理错误、或者在更新后串行触发后续请求，所以我在项目里用了像 fetchCartSaga，fetchOriginSaga这样的方式来集中管理购物车/埋点副作用。
---
## Chunk 112 — View（组件）

View（组件）

↓ dispatch(action) Action（对状态变化的抽象描述，而不是具体操作，携带payload） ↓ Middleware/Saga（可选：处理异步/副作用，因为Redux原生无法处理异步） ↓ Reducer（纯函数，计算新 state。不修改原 state） ↓ Store（保存 state，Store 是唯一数据源） ↓ View 更新
---
## Chunk 113 — Saga 是流程控制型 async

Saga 是流程控制型 async

监听某些 action ● 执行异步任务（API） ● 再 dispatch 新 action  
Redux-Saga 是一个Redux 中间件（middleware），用于管理异步逻辑和副作用，比如：API 请求、延迟任务、websocket、定时器、多请求协调。Redux-Saga = 用 generator 在 JS 里模拟 Algebraic Effects理论模型。  
useReducer 是 React 提供的一个状态管理 Hook（Redux轻量版）
---
## Chunk 114 — Redux Toolkit（RTK）

Redux Toolkit（RTK）

Redux Toolkit 是 Redux 官方推荐的写法，通过 createSlice 等 API 简化样板代码，并借助 Immer 实现不可变更新，使 Redux 更易用、更符合现代开发习惯。  
前端各种面经
---
## Chunk 115 — 浏览器从输入url到页面渲染发生了什么

浏览器从输入url到页面渲染发生了什么

浏览器从输入 URL 到页面渲染，首先会进行 DNS 解析获取 IP，然后建立 TCP 连接(TCP的三次握手，如果是 HTTPS 还会进行 TLS 握手）。接着浏览器发送 HTTP 请求，服务器返回 HTML。浏览器拿到 HTML 后会构建 DOM 树，同时解析 CSS 构建 CSSOM，然后合成 Render Tree，经过布局和绘制最终渲染到页面。
---
## Chunk 116 — TCP三次握手

TCP三次握手

TCP 三次握手的核心是双方确认彼此的收发能力并同步序列号。第一次客户端发送 SYN 表示要建立连接，第二次服务器返回 SYN+ACK 表示收到并同意连接，同时发送自己的序列号，第三次客户端再发送 ACK 进行最终确认。只有客户端确认后，服务器才认为连接有效。  
为什么不能是两次？如果只有两次握手，客户端无法确认服务器是否已经准备好接收数据，同时可能因为历史延迟的 SYN 请求导致服务器误建立连接。第三次握手通过客户端的确认，保证连接是双方都认可的，从而避免假连接问题。
---
## Chunk 117 — TCP四次挥手

TCP四次挥手

1. Client → FIN (Finish) 2. Server → ACK（只是server知道client向自己发完了，但server自己可能还没发完） 3. Server → FIN 4. Client → ACK  
四次挥手的本质是：TCP 的两个方向必须独立关闭，而不是一次性关闭整个连接。
---
## Chunk 118 — DNS域名解析的过程

DNS域名解析的过程

DNS 域名解析是把域名转换成 IP 地址的过程，大致分为两步：本地查询+递归查询。先查浏览器和本地缓存，如果没有，DNS会开始递归+迭代查询。客户端 → 本地 DNS：递归（帮你查到底），然后DNS 服务器之间：迭代。最终返回 IP，并进行缓存。通常用UDP协议。
---
## Chunk 119 — HTTP VS WebSocket

HTTP VS WebSocket

HTTP 是基于请求-响应的无状态协议，客户端发起请求，服务器返回响应，无法实现真正的实时通信。而 WebSocket是长连接，客户端和服务器可以进行全双工通信（用于让浏览器和服务器建立双向、持续的连接。支持服务器主动推送数据。相比 HTTP，WebSocket 更适用于实时性要求高的场景，如聊天、实时通知和在线游戏。这俩都是基于TCP的。
---
## Chunk 120 — tcp udp在应用层的协议有哪些，场景有哪些

tcp udp在应用层的协议有哪些，场景有哪些

TCP 和 UDP 是传输层协议，应用层协议会选择建立在它们之上。像 HTTP、HTTPS、FTP、SSH、 MySQL 通信这类对可靠性要求高的协议，通常基于 TCP，因为它能保证数据不丢失、不乱序。像 DNS、DHCP、实时音视频、游戏状态同步这类更强调低延迟的场景，通常会用 UDP，因为它开销更小、速度更快，但不保证可靠性。补充一点，HTTP/3 是基于 QUIC，而 QUIC 是跑在 UDP 上的。
---
## Chunk 121 — Tcp可靠传输怎么实现的

Tcp可靠传输怎么实现的

TCP 的可靠传输主要靠三个机制一起实现：首先通过三次握手建立连接；然后通过序列号保证数据有序，通过 ACK 确认对方已经收到的数据范围。
---
## Chunk 122 — HTTPS的加密过程

HTTPS的加密过程

HTTPS 本质上是在 HTTP 下面加了一层 TLS握手，然后通过非对称加密和对称加密结合来保证通信安全。客户端先获取服务器证书并验证合法性，然后使用服务器公钥加密 pre-master secret 发送给服务器。双方基于该 secret 和随机数推导出对称加密的 session key，后续通信使用对称加密完成。
---
## Chunk 123 — Http两种缓存（强缓存/协商缓存）

Http两种缓存（强缓存/协商缓存）

强缓存是浏览器直接根据缓存策略（比如 Cache-Control 或 Expires）判断资源是否过期，如果没过期就直接使用本地资源，不会发请求。如果强缓存失效，浏览器会发请求走协商缓存，通过 ETag 或 Last-Modified 和服务器确认资源是否变化。如果资源没变返回 304，浏览器继续用缓存，否则返回新资源。
---
## Chunk 124 — HTTP1/2/3的区别

HTTP1/2/3的区别

HTTP/1.1 的主要问题是队头阻塞和连接利用率低。  
HTTP/2 引入多路复用，提升了并发能力，但因为还是基于 TCP，TCP是一个流，所以一旦丢包，所有流都会被阻塞。  
HTTP/3 通过引入基于 UDP 的 QUIC 协议，QUIC 将多路复用能力从 HTTP 层下沉到更接近传输层的位置，使不同流之间互不影响，从而避免 TCP 层的队头阻塞问题。从而解决了 TCP 的队头  
阻塞问题，同时还能减少握手延迟。
---
## Chunk 125 — 2xx：成功 3xx：重定向

2xx：成功 3xx：重定向

301 Moved Permanently，永久重定向，浏览器会缓存重定向，下次直接访问新地址，比如域名变更、HTTP→HTTPS 302 Found，临时重定向，每次都会重新请求原地址，常用于登录跳转或临时页面切换
---
## Chunk 126 — 4xx：客户端错误

4xx：客户端错误

401 Unauthorized，未认证（没登录/token 失效） 403 Forbidden，没权限（登录了但不允许）
---
## Chunk 127 — 5xx：服务端错误

5xx：服务端错误

502 Bad Gateway，网关错误，后端挂了 504 Gateway Timeout，网关超时，后端响应太慢  
SSE 是标准 HTTP 吗？和普通请求区别 SSE 本质上是基于 HTTP 协议的一种长连接机制，因此它是标准 HTTP 请求的一种扩展形式。区别在于 SSE 是服务器持续向客户端推送数据的流式响应，连接不会立即关闭，客户端会持续接收数据，而不是等待一次完整返回。而普通 HTTP 请求是一次请求一次响应。  
流式输出的实现，前后端分别怎么做，用到什么协议流式输出的核心是让数据一边生成一边传输给前端，而不是等全部生成完再返回。后端通常会使用流式响应。前端可以通过 EventSource（SSE）来逐步读取数据并更新 UI。常用协议包括 HTTP 的 chunked 传输、SSE，以及更复杂场景下的 WebSocket）。SSE原生是只能发 GET请求的，不能方便地带复杂 body，比如message和chat history。适合服务端主动推送。
---
## Chunk 128 — 我的agent为啥不是SSE

我的agent为啥不是SSE

SSE 的浏览器原生 API EventSource 主要基于 GET 请求，而我的 chat 接口需要用 POST 传用户消息、多轮历史和上下文，所以我没有用原生 SSE。这个项目采用 POST+fetch streaming 的方式，通过 ReadableStream 逐块读取后端返回的 NDJSON，本质上还是 HTTP 流式传输，底层依赖 chunked response，只是协议格式不是标准 SSE。  
前端如何接收 SSE 流，支持哪些操作，连接数限制前端通常使用 EventSource 来接收 SSE 流，创建连接后可以监听 message、open、error 等事件，从而处理服务器推送的数据。SSE 支持自动重连机制，并且可以通过 id 字段实现断点续传。浏览器对同一域名下的 SSE 连接数量是有限制的，一般在 6 个左右，这与 HTTP/1.1 的连接限制有关。
---
## Chunk 129 — SSE VS Websocket

SSE VS Websocket

SSE 是服务器单向推送，基于 HTTP，主要用于通知推送，AI对话流；WebSocket 是双向通信，建立一次连接后是长连接，基于独立协议。主要用于共同编辑，实时游戏。  
进程VS线程进程：cpu资源分配的最小单位（进程之间相互独立，是能拥有资源和独立运行的最小单位）线程：cpu调度的最小单位（线程建立在进程基础上的一次程序运行单位，一个进程中可以有多个线程，同一进程下的各个线程之间共享程序的内存空间）
---
## Chunk 130 — 重排（回流）和重绘，什么时候触发，如何减少？

重排（回流）和重绘，什么时候触发，如何减少？

浏览器渲染页面时，如果元素的几何属性（如宽高、位置）发生变化，这会导致浏览器重新计算布局，会触发回流；如果只是视觉属性（如颜色）发生变化，那就只触发重绘。回流一定会导致重绘，但重绘不一定回流。在优化上，最重要的是避免频繁触发回流。  
首屏优化首屏优化的目标是让用户尽快看到页面的主要内容，从而提升用户体验。常见方法包括减少首屏资源体积（如压缩代码和图片）、使用代码切分按需加载资源、将静态资源部署到 CDN、以及通过服务端渲染或预渲染提前生成 HTML 内容。这些手段本质上都是在减少首屏需要加载和执行的资源量。
---
## Chunk 131 — 如果用户反应页面加载慢，排查思路是什么

如果用户反应页面加载慢，排查思路是什么

我一般按链路分阶段排查：先用DevTools看网络耗时（DNS/TCP握手时间），再看后端接口（比如数据库查询慢，api返回慢），再看前端资源加载，然后分析 JS 执行和渲染性能，最后考虑用户设备和网络环境。  
懒加载  
懒加载是指资源在“真正需要使用时才加载”，而不是一开始就全部加载，从而提升性能和首屏速度。三类：图片懒加载，代码懒加载，路由懒加载。图片懒加载通常通过 IntersectionObserver 或浏览器原生 loading="lazy" 实现。代码懒加载通过 React.lazy 和动态 import 实现，本质是代码分割。路由懒加载也是只有访问某个路由的时候才加载。
---
## Chunk 132 — 懒加载VS预加载

懒加载VS预加载

懒加载用于降低首屏压力，比如图片或路由组件；只渲染一开始的图，后面的滑倒再说。预加载用于优化关键资源或用户即将访问的内容，比如首屏图片或 hover 时预加载下一页代码。 pawse：在 Feed 页面中，我对图片做了懒加载，避免一次性加载大量图片；同时对用户可能点击的详情页做了预加载，提高跳转速度。
---
## Chunk 133 — WebWorker

WebWorker

浏览器在Renderer进程中创造一个新线程运行JS文件，用来解决大量计算问题，避免JS引擎执行时间过长阻塞页面。只属于某个页面，不和其他页面的Render进程共享。
---
## Chunk 134 — 分片上传&断点续传

分片上传&断点续传

分片上传是指将大文件拆分成多个小块（chunk）分别上传，最后在服务器端进行合并的一种上传方式。执行方式是前端会先对文件进行切片，并生成文件 hash，然后并发上传每个 chunk。上传完成后通知后端进行合并，由于有hash，可以进行断点续传（中断，继续）/秒传（不上传文件内容，只根据hash查看，服务器发现已有相同文件，直接返回成功，压根不传）。一般用于大文件上传/网络不稳定上传容易失败（pawse不需要，因为pawse只是要上传几mb的图片，没必要分片，主要优化的是图片压缩和S3存储优化）
---
## Chunk 135 — 如何取消请求？

如何取消请求？

为什么要取消请求？  
在前端中，请求取消主要用于避免无效请求占用资源，以及防止组件卸载后更新状态。在 React 中，通常在 useEffect 的 cleanup 里取消请求，避免组件卸载后仍然更新状态。还可以，使用防抖节流，或者最新请求覆盖旧请求（竞态控制）用 requestId。
---
## Chunk 136 — 取消请求原因：

取消请求原因：

1. 防止内存泄漏。组件已经unMount但请求回来还setState 2. 节省性能，减少无效请求
---
## Chunk 137 — 前端缓存可以分为多个层级，从网络到本地：

前端缓存可以分为多个层级，从网络到本地：

1 ⃣ HTTP 缓存（最重要）：浏览器自动处理。强缓存：Cache-Control，Expires。协商缓存：ETag， Last-Modified。优点：最优先（不用发请求）  
2 ⃣ 浏览器存储缓存：手动控制，有localStorage，sessionStorage，IndexDB。用于API 数据缓存，离线能力。  
浏览器常见存储有 localStorage、sessionStorage 和 IndexedDB。localStorage 是长期存储，同源共享，但容量小而且同步 API，会阻塞js现线程；sessionStorage 是会话级别，tab 关闭就失效； IndexedDB 是异步的本地数据库，支持大容量和复杂数据。实际项目中缓存不只用这些，还会结合 HTTP 缓存和内存缓存来提升性能。  
3 ⃣ 内存缓存（JS 变量）：const cache = new Map(); 最快，但刷新就没
---
## Chunk 138 — Javascript数据类型

Javascript数据类型

基本类型7个：一般存的是值本身 (Number, String, Boolean,Null, Undefined, Symbol, BigInt， symbol和bigInt是ES6新增的）  
Symbol代表创建后独一无二且不可变的数据类型，它主要是为了解决可能出现的全局变量冲突的问题。应用：防止对象属性冲突。  
BigInt 是一种数字类型的数据，它可以表示任意精度格式的整数，使用 BigInt 可以安全地存储和操作大整数，即使这个数已经超出了 Number 能够表示的安全整数范围。  
引用类型1个：就是Object，变量里存的是地址/引用，但可以包括Array, Function, Set, Object…
---
## Chunk 139 — What?

What?

es6新增的原始数据类型，具有唯一性和不可变性。
---
## Chunk 140 — Why?

Why?

主要作用是作为属性的唯一标识符，防止对象属性发生冲突。  
不能和new一起使用，是为了避免创造出包装对象。  
堆 VS 栈  
堆：存放引用数据类型，引用数据类型占据空间大、大小不固定。如果存储在栈中，将会影响程序运行的性能；引用数据类型在栈中存储了指针，该指针指向堆中该实体的起始地址，如Object、 Array、Function。  
栈：存放原始数据类型，栈中的简单数据段，占据空间小，属于被频繁使用的数据，如String、 Number、Null、Boolean。
---
## Chunk 141 — Null跟undefined区别

Null跟undefined区别

undefined 表示“未定义”的值，通常是 JS 自动产生的，应用场景：判断变量是否初始化，判断属性是否存在。  
null 表示“有意赋值为空”，通常由开发者主动设置。（表示“我知道这里有值，但现在是空的”）。常见场景：null主要用于赋值给一些可能会返回对象的变量，作为初始化，或者主动清空数据（比如断开引用）  
在比较上，null 和 undefined 用 == 相等，但 === 不相等。  
===和==区别  
=== 是严格相等，不会做类型转换，只有在类型和数值都相同的情况下才返回 true， == 是宽松相等，会先做类型转换再比较。 [ ] == 0 [ ] → "" → 0，true  
[ ] ==![ ] （0 = 0，true）右边因为有!，在表达式计算阶段先转成 boolean，又因为对象都是true，所以右边是false，即0；左边没有参与这个运算，在 == 比较阶段才按对象 → 原始值 → 数字的规则转换，就是转空字符串然后是0。
---
## Chunk 142 — call，apply，bind的区别

call，apply，bind的区别

call、bind和apply都是JavaScript中用来改变函数内部this指向的方法。但也有一些区别：  
传参方式：call和apply在传参方式上有所不同。call方法是依次传入参数，每个参数作为一个独立的参数。而apply方法则将所有参数打包成一个数组传递。  
返回值：call和apply方法都会执行函数并返回结果，而bind方法不会立即执行函数，而是返回一个新的函数。  
This指向：使用bind方法时，如果省略了第一个参数（this），那么bind会绑定当前函数运行时所在的环境（即全局作用域或函数作用域），而不是指定的上下文。  
柯里化：fn.bind(thisArg, arg1, arg2,...)。做了两件事：1. 固定 this，2. 预填一部分参数（partial application）
---
## Chunk 143 — addEventListener

addEventListener

addEventListener 是用来给 DOM 元素注册事件监听的，当指定事件发生时执行回调函数。它支持多个监听器。如果写成普通函数，那么this === dom，如果写的是箭头函数，那么this指向外层作用域。
---
## Chunk 144 — 直接绑定和事件监听有哪些区别

直接绑定和事件监听有哪些区别

直接绑定：dom.onclick = fn（只能绑定一个）事件监听：addEventListener（可以绑定多个，更灵活）  
直接绑定是给 DOM 的事件属性赋值，只能绑定一个处理函数；addEventListener 是事件监听机制，支持多个回调、事件捕获/冒泡阶段控制，并且可以单独移除监听，更灵活。
---
## Chunk 145 — 回调函数

回调函数

回调函数 = 作为参数传进去，被别人“以后再调用”的函数（也就是，不是我主动去调用）  
JavaScript xxx.onSomething = fn//fn是回调函数
---
## Chunk 146 — function handleClick() {

function handleClick() {

doSomething()  
}  
button.onclick = handleClick//handleClick是回调函数  
evtSource.onmessage = (event) => {//浏览器每当收到message之后，调用 (event) => {}这个回调函数 renderer.onChunk(event.data)//onCHunk是“手动调用”一个方法 }  
dom.addEventListener('click',function () {}//这个fn也是回调函数  
Typeof和instanceof区别  
typeof 主要用来判断基本类型，返回一个类型字符串，但它对 null 判断不准确，会返回object； instanceof 用来判断对象是否属于某个构造函数，是通过原型链实现的。一般来说，基本类型用 typeof，引用类型用 instanceof。  
typeof true//"boolean" [] instanceof Array//true
---
## Chunk 147 — new操作符具体干了什么呢?

new操作符具体干了什么呢?

创建一个空的简单 JavaScript 对象（即{}）；为新创建的对象添加属性__proto__，将该属性链接至构造函数的原型对象；将新创建的对象作为this的上下文；如果该函数没有返回对象，则返回this。
---
## Chunk 148 — WeakMap

WeakMap

说说WeakMap, 为什么WeakMap不可以遍历t WeakMap的键只能是对象类型(包括数组), 而且对键是弱引用的。即当键不存在强引用时，该键的内存可以在GC时被回收。  
由于键是弱引用的，随时可能被回收，所以ES6规定WeakMap不可遍历。应用：在DOM对象上保存数据和数据缓存（当我们想要在不修改原对象的情况下给其存储一些数据或计算值时，WeakMap非常合适。）
---
## Chunk 149 — Js垃圾回收

Js垃圾回收

标记清除（Mark-and-sweep）：这是JavaScript中主流的垃圾回收算法。在标记清除过程中，垃圾收集器会定期扫描内存中的对象，将可达对象和不可达对象分别标记为“存活”和“垃圾”。然后，垃圾收集器从内存中清除被标记为“垃圾”的对象，从而释放它们所占用的内存空间。  
引用计数（Reference counting）：这是JavaScript中较少使用的垃圾回收算法。引用计数是通过计算对象在内存中的位置，决定垃圾的数量，然后决定是否回收该对象。每当一个对象被引用时，其引用计数会增加；每当一个对象的引用被解除时，其引用计数会减少。当一个对象的引用计数为0 时，表示没有任何引用指向该对象，该对象变为不可达，因此可以将其回收。  
什么会导致内存泄漏
---
## Chunk 150 — Js垃圾回收 > 1. 全局变量，一直可达导致一直不回收

Js垃圾回收 > 1. 全局变量，一直可达导致一直不回收

2. 闭包引用 3. 计时器引用 4. DOM 删除但 JS 还引用。想释放内存必须满足2点：1. Dom删除（remove），2. Js没有引用他  
let el = document.getElementById('app') el.remove() El = null (必须要有这个设null)
---
## Chunk 151 — Js垃圾回收 > 5. 事件监听没移除

Js垃圾回收 > 5. 事件监听没移除

怎么定位内存泄漏我一般会用 Chrome DevTools 的 Heap Snapshot，对比操作前后的内存对象，然后通过 Retainer chain 去看是谁还在引用这个对象，这样可以一步步定位到具体哪段代码没释放，比如事件监听或者定时器。
---
## Chunk 152 — for … in VS for … of

for … in VS for … of

For in遍历的是key。主要是遍历对象用的。会遍历整个原型链（遍历数组不推荐使用因为效率比较低），如果不想要原型链上的东西需要加hasOwnProperty，for key in obj, 必须 obj.hasOwnProperty(key)  
For of遍历的是value。他的本质是iterator迭代器，可以直接遍历所有可迭代的东西比如array，list，map。不可以直接遍历obj，要想遍历object的化需要const key of Object.keys(obj)。for of 只遍历自己的属性，不管原型链，更好
---
## Chunk 153 — hasOwnProperty

hasOwnProperty

hasOwnProperty 用来判断一个属性是不是对象“自己”的，而不是从原型链继承来的。
---
## Chunk 154 — setTimeout和setInterval

setTimeout和setInterval

setTimeout (fn, interval) （不是1秒后直接执行）
---
## Chunk 155 — setInterval (fn, interval)

setInterval (fn, interval)

无限循环，每隔 1 秒把 fn 放入任务队列
---
## Chunk 156 — Js为啥是单线程

Js为啥是单线程

JS是单线程，由于最早设计是为了操作DOM，由于需要避免两个线程同时修改DOM造成状态冲突，同一时间只能执行一段代码。如果JS只有同步执行那么可能会造成页面完全卡死，因此引入了异步机制。  
JS 会阻塞渲染吗，为什么这么设计 JavaScript 的执行是单线程的，会阻塞 DOM 渲染，因为浏览器需要保证 DOM 和 JS 操作的一致性。如果在 JS 执行过程中 DOM 被修改，而渲染同时进行，可能会导致状态不一致。因此浏览器采用了这种设计，在 JS 执行完成后再进行渲染，从而保证页面状态的正确性。
---
## Chunk 157 — var，let，const区别

var，let，const区别

作用域：var在声明变量时有函数级作用域，而let和const有块级作用域。  
重声明：在同一个作用域内，你可以多次使用var来声明同一个变量，但不能用let或const多次声明同一个变量。  
提升：var声明的变量会被提升到作用域顶层，意味着你可以在声明之前可以访问（值是 undefined）。let和const声明的变量虽然也会被提升，但是你不能在声明之前访问它们，否则会报错。从提升到真正声明这个区间被称为“暂时性死区”。  
赋值：let和cons不能重新声明（对于let和const）。但是var可以。  
全局作用域行为：在全局作用域中声明的变量，var和let会成为全局对象（在浏览器中是window对象）的属性，但const不会。
---
## Chunk 158 — 变量提升

变量提升

js会把变量声明部分和函数声明部分提升到函数作用域或全局作用域顶端，变量会有一个初始值 undefined。  
编译阶段，同名的函数会选择最后声明的那个，如果变量和函数同名，会优先选择函数而不是变量。但是执行阶段，变量赋值照常进行。
---
## Chunk 159 — ES6的新特性

ES6的新特性

块级作用域（Let，Const）。ES6引入了块级作用域的概念，这意味着你可以使用let和const关键字来声明变量和常量，它们只在声明它们的代码块内可见。  
定义类的语法糖（Class）。ES6引入了定义类的语法糖，这使得创建和管理对象变得更加简单和直观。  
一种基本数据类型（Symbol）。ES6引入了一种新的基本数据类型——Symbol，它是一种唯一的、不可变的、不可打印的特殊类型。  
模块化（Import/Export）。ES6引入了模块化的概念，使得JavaScript代码可以以模块的形式进行编写和组织，增强了代码的可维护性和可重用性。  
新增了Set和Map数据结构。ES6引入了Set和Map数据结构，它们都是基于JavaScript对象，用于存储和操作键值对的集合。
---
## Chunk 160 — 讲一下js的作用域有哪几种

讲一下js的作用域有哪几种

作用域就是一个变量在什么范围内可以被访问。JavaScript 里常见的作用域主要有全局作用域、函数作用域、块级作用域和模块作用域。传统的 var 主要是函数作用域；而 let 和 const 是块级作用域，通常用在 if、for、while 等代码块中。  
Js如何实现继承 JS 继承本质是原型链，常见有原型链继承、构造函数继承和组合继承。  
原型链继承通过让 Child.prototype 指向 Parent 实例，可以继承实原型方法，但存在引用共享和无法传参的问题。  
构造函数继承通过 call/apply调用父类构造函数，可以继承实例属性并支持传参，但拿不到原型方法。组合继承结合两者优点，但会调用父类两次。  
寄生组合继承通过在子类构造函数中调用父类构造函数继承实例属性，并使用 Object.create 建立原型链继承父类原型方法，从而避免了组合继承中多次调用父类构造函数的问题。  
实际开发一般用 ES6 class，也就是用extends，extends 本质是原型链+构造函数继承的封装。
---
## Chunk 161 — forEach和map方法区别

forEach和map方法区别

两个方法都是用来遍历循环数组，区别如下： forEach()对数据的操作会改变原数组，该方法没有返回值； map()方法不会改变原数组的值，返回一个新数组，新数组中的值为原数组调用函数处理之后的值；  
原型链  
在JavaScript中，每个对象都有一个原型对象proto，指向其构造函数的原型对象prototype。  
当我们创建一个新的实例对象时，这个对象会从其构造函数的原型对象prototype中继承属性和方法。如果实例对象自身没有某个属性或方法，但是其构造函数原型对象prototype中存在，那么这个对象会从其构造函数的原型对象prototype中查找并继承这个属性或方法。  
我们访问一个对象的属性或方法时，如果该对象没有这个属性或方法，JavaScript引擎会在原型链（也就是，通过 __proto__）一层一层向上进行查找，直到找到这个属性或方法或者到达原型链的末尾。js的原型链是在运行的时候形成的。
---
## Chunk 162 — 作用域链

作用域链

作用域链指的是变量查找的路径。当一个函数内部访问某个变量时，会先在当前作用域查找，如果找不到，就沿着外层作用域一层一层向上查找，直到全局作用域，这个查找过程形成的链条就叫作用域链。JavaScript 中作用域链在函数定义时就已经确定，而不是调用时确定。  
闭包及应用场景  
闭包本质上就是：函数可以记住并访问它定义时的外层作用域变量。应用场景最主要的是封装私有变量比如Counter，还有就是像防抖函数。因为我们需要在多次调用之间共享一个 timer，但又不希望它成为全局变量，所以通过闭包把它封装在函数内部。
---
## Chunk 163 — 闭包陷阱

闭包陷阱

闭包陷阱的本质是：函数记住的是某一次创建时的作用域，而不是你脑子里想象的“永远最新的值”。经典的闭包陷阱是for循环+var，react的闭包陷阱是useEffect的依赖数组写空数组，这样 useEffect就只在第一次render后执行一次，里面的count一直不变。
---
## Chunk 164 — this，箭头函数和普通函数的区别

this，箭头函数和普通函数的区别

箭头函数和普通函数最核心的区别在于 this 的绑定方式不同。普通函数的 this 是在调用时决定的，也就是说谁调用这个函数，this 就指向谁，因此它的指向是动态的；而箭头函数没有自己的 this，它会在定义时就从外层作用域“继承”this，并且之后无法被改变。这也导致箭头函数不能用作构造函数、没有 prototype，也不能通过 call、apply、bind 改变 this。在实际开发中，普通函数更适合作为对象方法，而箭头函数更适合用于回调函数，尤其是在需要避免 this 丢失的场景中。
---
## Chunk 165 — 事件循环 EventLoop

事件循环 EventLoop

JavaScript 是单线程的，所以需要事件循环来调度同步和异步任务。执行时会先跑同步代码，然后清空所有微任务，如 Promise.then，再poll一个宏任务出来执行，如 setTimeout，然后继续循环。
---
## Chunk 166 — 4 ⃣ 再清空微任务

4 ⃣ 再清空微任务

5 ⃣ 循环...  
宏任务和微任务执行规则，会死循环吗事件循环中，每执行完一个宏任务，会清空当前所有微任务队列，然后再进入下一个宏任务。如果一个微任务不断生成新的微任务，就可能导致宏任务无法执行，从而出现“饥饿”问题，类似死循环，但本质上是微任务队列一直不为空。  
什么是回调地狱，如何解决  
回调地狱指的是多个异步操作嵌套在一起形成深层回调结构，使代码难以阅读和维护，例如一个请求完成后再发起另一个请求，层层嵌套。解决这个问题通常有几种方式：首先是使用 Promise 将嵌套结构改写为链式调用，其次是使用 async/await 将异步代码写成类似同步代码的形式，提升可读性，最后是通过更高级的抽象如事件流或状态管理来组织复杂异步逻辑。在实际项目中， async/await 是最常用也是最推荐的解决方案。
---
## Chunk 167 — 4 ⃣ 再清空微任务 > Promise 是用来解决什么问题的

4 ⃣ 再清空微任务 > Promise 是用来解决什么问题的

Promise 主要是为了解决传统回调函数嵌套带来的“回调地狱”问题。在早期的 JavaScript 中，多个异步操作往往需要层层嵌套回调，导致代码结构混乱且难以维护，Promise 通过链式调用then 把异步流程串联起来，使代码更加线性和可读。同时，Promise 引入了统一的状态管理（pending、fulfilled、rejected），并且可以通过 catch 实现集中错误处理，提升了代码的可维护性。  
Promise 是 JavaScript 中处理异步操作的一种方式，它代表一个未来才会完成的值，通过 then/catch 或 async/await 来获取结果，并避免回调地狱。  
对async/await 的理解 async/await其实是Generator 的语法糖，它能实现的效果都能用then链来实现，它是为优化then 链而开发出来的。通过async关键字声明一个异步函数， await 用于等待一个异步方法执行完成，并且会阻塞执行。 async 函数返回的是一个 Promise 对象，如果在函数中 return 一个变量， async 会把这个直接量通过 Promise.resolve() 封装成 Promise 对象。如果没有返回值，返回 Promise.resolve(undefined)  
异常如何统一处理  
在异步编程中，异常统一处理主要依赖 Promise 的 catch/then 或 async/await 配合 try-catch。使用 Promise 时，可以在链的末尾统一使用 catch 捕获整个链中的错误，而使用 async/await 时，可以通过 try-catch 包裹异步代码，使错误处理看起来和同步代码一致。
---
## Chunk 168 — 防抖VS节流

防抖VS节流

防抖：一直输入请求，只在最后一次请求结束后空一段时间才真的发送请求（适合搜索输入）节流：固定时间内最多执行一次（适合滚动、resize）
---
## Chunk 169 — AJAX

AJAX

AJAX：使用 JavaScript 在后台异步地和服务器通信，用来局部更新。在不刷新整个网页的情况下，通过 JavaScript 向服务器发送异步 HTTP 请求并更新页面数据的技术。例如：搜索建议（Google 输入自动提示）、聊天消息刷新、点赞、表单提交。
---
## Chunk 170 — 如何设计可以复用的表单组件

如何设计可以复用的表单组件

设计可复用表单组件时，我会把字段做成 schema 配置化，而不是手写大量 JSX。schema 本质上是一份字段配置，比如字段名、类型、label、默认值、校验规则和选项等，表单组件根据 schema 动态渲染输入项。  
架构上我会拆成 Form、FormItem、Field 三层组件：Form 负责统一管理表单状态、提交和校验； FormItem 负责一行UI， label、错误提示；Field 负责具体控件渲染，比如 input、select、checkbox。  
状态管理上会集中存储整张表单的数据form和setForm，但是每个 Field 只接收自己需要的 value 和 error。字段更新时只更新对应字段。性能优化的重点是局部更新，比如通过 memo 化 Field，避免一个字段变化导致整张表单所有控件都重渲染。这样可以兼顾复用性、可维护性和性能。
---
## Chunk 171 — TS基本类型

TS基本类型

TypeScript 的基本类型主要包括7个跟js一样的类型：number、string、boolean、null、undefined、 symbol、bigint，以及比较特殊的 any、unknown、void、never。
---
## Chunk 172 — Symbol

Symbol

在 TypeScript 里，symbol 是一种基本类型，表示唯一且不可变的值，常用于作为对象的 key，避免属性冲突。TS还加了unique symbol，用于定义唯一的常量类型。
---
## Chunk 173 — Any VS unknown

Any VS unknown

any 可以直接操作任何属性，不做类型检查（由于any会关闭类型检查，所以他不是很安全）； unknown 更安全，必须先判断类型才能使用。
---
## Chunk 174 — TS中extends和implement区别

TS中extends和implement区别

Extends，子类继承父类的属性、方法、类型。 Implements，必须符合接口结构，但不会继承实现，Dog必须实现interface Animal的所有属性和方法，否则编译错误。
---
## Chunk 175 — 为什么项目中使用 TypeScript？

为什么项目中使用 TypeScript？

用了哪些 TS 技术？在项目中使用 TypeScript主要是为了提升代码的可维护性和可扩展性。相比 JavaScript， TypeScript提供了静态类型检查，可以在编译阶段提前发现潜在错误，比如接口字段缺失或类型  
不匹配，这在多人协作和复杂业务中非常重要。在我的项目中，我主要使用了 interface 和 type 来定义数据结构，比如接口返回的数据格式，同时也用到了泛型来提升函数和组件的复用性，比如封装通用请求函数时用泛型约束返回类型。另外在 React 中我会为 props 和 state 明确标注类型，这可以提升开发体验并减少运行时错误。
---
## Chunk 176 — 允许在定义函数、接口或类时不指定具体类型，而在使用时指定类型

允许在定义函数、接口或类时不指定具体类型，而在使用时指定类型

提高代码复用性：用泛型创建可重用的组件，使一个组件可以支持多种数据类型。比如一个泛型的数组反转函数，可以同样适用于字符串数组或数字数组，而无需为每种类型写单独的版本。  
保证类型安全，避免使用any类型  
JavaScript//echo函数就是泛型 function echo<T>(arg: T): T {  
return arg  
}  
echo<string>('Hello')//明确传入类型参数 echo('Hello')
---
## Chunk 177 — Interface和type的区别

Interface和type的区别

interface 更适合描述对象结构，并且支持 extends 和声明合并，扩展性更好。在大型项目中，多个模块可以对同一个 interface 进行扩展，方便维护。所以在描述数据结构（如 API response、 props）时，通常优先使用 interface。  
但在需要联合类型、交叉类型或函数类型时，我会用 type，因为 interface 无法表达这些复杂类型。
---
## Chunk 178 — Interface和abstract class区别

Interface和abstract class区别

interface 更偏向定义规范，只描述结构，强调“能做什么”，不包含实现；而 abstract class 既可以定义抽象方法，也可以提供部分实现，用于代码复用。  
抽象方法  
抽象方法不包含具体的实现，必须在子类中实现抽象方法。
---
## Chunk 179 — 类型断言

类型断言

类型断言告诉编译器，我们自己确切的知道变量的类型，而不需要进行类型检查。as语法或者<> 语法
---
## Chunk 180 — TypeScript编译链路

TypeScript编译链路

TypeScript的编译器主要做两件事，一是类型检查，二是把部分 TS 语法降级成 JS；真正项目里通常不是单独只靠 tsc （TypeScript compiler）完成所有事情，而是 TypeScript 负责类型信息， Babel/SWC/esbuild/bundler 也可能一起参与语法转换和打包。也就是说，npm start 的时候并不是“浏览器直接运行 TS”，而是开发服务器先把源码编译/转换，再把浏览器能执行的 JS 提供出去。类型信息主要存在于编译期，最终跑到浏览器里的代码基本已经没有类型。
---
## Chunk 181 — Webpack：两种打包方式

Webpack：两种打包方式
---
## Chunk 182 — Webpack：两种打包方式

流程：构建依赖关系 -> loader转译 -> 打包统一：编译时确认依赖关系，并且打包所有的代码（过程中用loader把浏览器不能理解的部分jsx， tsx转译成能理解的部分，如js和css）  
区别：  
1. 打包成一个整体的bundle。静态import，同步加载。他支持静态分析，也因此只有这个支持tree shaking（要在生产模式下打包，而不是开发模式，因为生产模式webpack默认开启了压缩和优化）  
2. 进行代码分割，打包成不同的chunk。动态import，运行时按需加载（路由懒加载）  
由于Webpack一定有打包过程，所以可以支持ESModule和CommonJS  
Vite: 与Webpack的区别：Vite不打包，直接在运行是按需加载。由于没有打包过程，因此开发阶段只能依赖浏览器原生模块，也就是ESModule，因此不支持CommonJS  
webpack 如何进行代码分割，有几种方式 Webpack 的代码分割本质是将一个大的 bundle 拆分成多个小的 chunk，从而减少首屏加载体积。常见方式主要有三种：第一种是通过入口配置进行多入口打包，不同入口生成不同 bundle；第二种是使用动态导入 import()，这是最常用的方式，它会在运行时按需加载模块，从而实现懒加载，比如路由懒加载；第三种是通过 SplitChunksPlugin 抽离公共依赖，例如把多个页面共享的库（如 React）提取到单独的 chunk 中，从而避免重复加载。在实际项目中，动态 import 和 SplitChunks 是最常用的组合。  
代码切分和路由懒加载代码切分是通过将代码拆分成多个 bundle 来减少初始加载体积，而路由懒加载是其中最常见的应用场景，即在用户访问某个路由时才加载对应的代码。通常通过 import() 或框架提供的懒加载机制实现。这样可以显著减少首屏加载时间，提高应用性能。  
Treeshaking是啥？webpack 如何进行 tree shaking 的配置？
---
## Chunk 183 — Webpack：两种打包方式

Treeshaking是啥？webpack 如何进行 tree shaking 的配置？  
Tree Shaking 是一种在打包阶段移除未使用代码（dead code）的优化技术，从而减小最终 bundle 体积，他是基于ES module的静态分析的。  
在 webpack 中，首先需要确保使用的是ES module import/export 而不是CommonJS的 require，因为ES Module（import/export）是编译时确定依赖关系，可以分析哪些代码被使用和哪些没被使用；其次需要在生产模式（production）下打包，因为生产模式webpack默认开启了压缩和优化；另外需要在 package.json 中正确标记 sideEffects，告诉 webpack 哪些文件是有副作用的不能被删除。最终通过压缩工具（如 Terser）将未使用的代码移除。需要注意的是，tree shaking 并不是 import 自动带来的，而是构建工具结合静态分析实现的。
---
## Chunk 184 — 为什么 ES6 import 不能减少打包体积

为什么 ES6 import 不能减少打包体积

ES6 的静态 import 本身不会自动实现懒加载，所以不保证一定减少首包体积；它主要的价值是让打包器能基于静态结构做 tree shaking，删除未使用的导出。真正实现按需加载和代码分割的是动态 import()。所以，静态 import 更偏向“帮助删死代码”，动态 import() 更偏向“把代码拆出去，等需要时再加载”。  
CommonJS 和 ES Module 区别 CommonJS 和 ES Module 的主要区别在于加载方式和执行时机。CommonJS 是运行时加载，使用 require 导入模块，模块导出的是值的拷贝；而 ES Module 是编译时加载，使用 import/export，支持静态分析，因此可以进行 tree shaking。ES Module 的导出是引用（live binding），也就是说导出的值如果变化，引用方也会同步更新。此外，ES Module 是异步加载的，更适合浏览器环境，而 CommonJS 更常用于 Node.js。  
Webpack 入口是什么？依赖图怎么构建？loader 和 plugin 有什么区别？开发时 npm start 到底发生了什么？  
开发时执行 npm start，脚手架会启动 dev server，Webpack 从 entry 出发递归分析 import/require，形成依赖图，用 loader 转换 JSX/TS/CSS 等内容，在内存中打包成 bundle，再通过本地服务提供给浏览器。保存代码后，构建工具会增量编译并通过 HMR 更新页面。  
生产时执行 npm run build，它会生成真正的静态资源文件，并做压缩、分包、Tree Shaking 和缓存优化，然后这些产物被部署到服务器或 CDN。
---
## Chunk 185 — Cookie VS Session

Cookie VS Session

Cookie = 存在浏览器的身份凭证，安全性低（可被篡改） Session = 存在服务器的用户状态（安全性高）  
用户登录后，服务器会生成一个 session 并返回 sessionId，浏览器通过 cookie 保存这个 sessionId，后续请求自动携带，服务器通过它识别用户。
---
## Chunk 186 — Cookie有什么安全问题？

Cookie有什么安全问题？

XSS：攻击者用恶意js读取cookie CSRF：利用浏览器自动带cookie发请求
---
## Chunk 187 — XSS 攻击及防御

XSS 攻击及防御

XSS是跨站脚本攻击。攻击者把恶意 JS 注入到页面里，让用户浏览器执行，从而窃取信息或进行恶意操作。防御方式主要包括对用户输入进行转义处理、防止直接插入inner HTML、使用 CSP 限制脚本执行来源。在实际开发中，最重要的是不要信任用户输入。  
一个常见的 XSS 攻击例子是留言板或评论区。如果网站没有对用户提交的评论内容进行转义或过滤，攻击者可以在评论中插入一段恶意的 JavaScript 代码，比如 <script>alert('Your session is hacked!');</script>。当其他用户查看这条评论时，这段脚本会在他们的浏览器中执行，可能会窃取他们的 Cookie（从而劫持他们的账户），或者重定向他们到钓鱼网站。因此，XSS 不仅损害用户隐私，还可能导致数据泄露和账户被盗。
---
## Chunk 188 — CSRF攻击及防御

CSRF攻击及防御

Cross-Site Request Forgery（跨站请求伪造），攻击者利用浏览器“自动带 cookie”，伪造用户请求，只要用户登陆恶意网站，就会自动发起请求，比如“转账”。CSRF关键条件：用户已登录，浏览器自动带 cookie，服务器没做校验。所以CSRF防御：1. CSRF Token，原理是每个请求带 token，然后服务器验证，2. 判断请求来源。
---
## Chunk 189 — 跨域&同源策略

跨域&同源策略

跨域本质上是浏览器中的网页去请求一个和自己不同源的资源时，受到浏览器同源策略限制的现象。一般来说请求已经发出去了，只是响应被浏览器拦截住了。  
同源策略：协议、域名和端口必须一致，这是浏览器的安全机制，限制一个源的脚本随意读取另一个源的资源。它的核心目的就是防止恶意网站偷你的数据。比如前端跑在：http://localhost:3000，后端跑在http://localhost:8080，由于端口不同所以跨域，于是前端代码的 fetch("http://localhost:8080/api/user")，浏览器就会检查是否允许跨域访问。  
Axios Axios 是一个基于 Promise 的 HTTP请求库，用于在浏览器或 Node.js 中发送请求。  
支持PromiseAPI 从浏览器中创建XMLHttpRequest 从 node.js 创建 http 请求支持请求拦截和响应拦截自动转换JSON数据客服端支持防止CSRF/XSRF
---
## Chunk 190 — fetch

fetch

浏览器原生实现的请求方式。基于标准 Promise 实现，支持async/await fetchtch只对网络请求报错，对400，500都当做成功的请求，需要封装去处理默认不会带cookie，需要添加配置项 fetch没有办法原生监测请求的进度，而XHR可以。
---
## Chunk 191 — 跨域限制的是谁

跨域限制的是谁

跨域限制的是“浏览器里的脚本”，浏览器里用 fetch/axios/XMLHttpRequest 会受同源策略影响。Postman和后端请求一般不会有跨域问题。  
跨域限制的是什么  
浏览器限制的重点是：脚本读取跨域响应的内容，也就是说，某些跨域资源其实是可以“发起”的，只是不能随便读。比如说<img src="https://other.com/a.png"/>是ok的，因为浏览器允许你“用”这个资源，但不代表允许你的js去读取任意返回内容。
---
## Chunk 192 — 跨域解决方式

跨域解决方式

CORS 是浏览器基于同源策略的一种跨域解决方案。浏览器在发送请求时会带上 Origin，服务器通过返回 Access-Control-Allow-Origin 等响应头来声明是否允许该源访问。浏览器收到响应后会校验这些头，如果匹配就把数据交给前端，否则会拦截。对于复杂请求，浏览器还会先发送一个 OPTIONS 预检请求，确认服务器允许后才会发真正请求。
---
## Chunk 193 — 为什么我明明服务端返回 200，浏览器还是报跨域错误？

为什么我明明服务端返回 200，浏览器还是报跨域错误？

因为 HTTP 成功不代表 CORS 成功。可能情况是：请求已经到服务器了，服务器也返回了 200，但响应头里没有正确的 CORS 头，浏览器还是不让 JS 读结果，所以前端控制台会报跨域错误。这也是为什么后端经常说“我接口明明通了”。
---
## Chunk 194 — Flex是啥

Flex是啥

Flex：让 container 里的所有子元素按照“弹性布局规则”排列 flex-direction：弹性布局规则下的主轴是row/col，row是默认 CSS默认情况下：div 是纵向排列（一个一个往下），然后开启flex默认变成横向排列  
Flex: 1 flex:1 表示元素会忽略自身内容大小，从剩余空间中按比例分配空间。多个 flex:1 的元素会平分父容器空间。如果比例不同，比如 flex:2，就会按比例分配
---
## Chunk 195 — Justify-content和align items

Justify-content和align items

控制主方向上的对齐方式，“主轴”取决于 flex-direction，如果 flex-direction: row，主轴 = 横向，如果 flex-direction: column，主轴 = 纵向。 Align-items（副轴）
---
## Chunk 196 — 如何实现水平和垂直居中用 flex，通过主轴 justify-content 和交叉轴 align-items 都设置成center实现水平垂直居中。如果需要精

如何实现水平和垂直居中用 flex，通过主轴 justify-content 和交叉轴 align-items 都设置成center实现水平垂直居中。如果需要精

确控制位置（不是“居中”），那用transform，从中点中心计算比较好。  
BFC 是什么，如何形成 BFC（Block Formatting Context，块级格式化上下文）是一个独立的布局区域，内部元素不会影响外部布局。常见触发方式包括 overflow 不为 visible、display 为 flex 或 inline-block、position 为 absolute 或 fixed 等。BFC 可以用于解决 margin 重叠和清除浮动等问题。  
CSS 样式优先级  
CSS 的优先级是根据选择器的权重来决定的，通常遵循从低到高为标签选择器（div）、类选择器、 ID 选择器、行内样式，以及最高的!important。当多个样式同时作用于一个元素时，浏览器会根据权重计算最终应用的样式。如果权重相同，则后定义的样式会覆盖前面的。在实际开发中，应该尽量避免使用!important，因为它会破坏样式层级结构，降低代码可维护性。  
CSS position 属性及绝对定位影响 CSS 的 position 包括 static、relative、absolute、fixed 和 sticky。 static 是默认布局，不参与定位； relative 相对于自身原位置偏移，不脱离文档流； absolute 会脱离文档流，相对于最近的已定位祖先元素定位，如果没有则相对于初始包含块； fixed 也是脱离文档流，但始终相对于视口定位； sticky 是一种混合定位，在滚动到阈值前表现为 relative，之后表现为 fixed。  
由于 absolute 和 fixed 会脱离文档流，它们不会撑开父容器，可能导致布局塌陷问题。
---
## Chunk 197 — CSS 实现宽高等比

CSS 实现宽高等比

实现宽高等比最常见的方式是使用 padding 百分比技巧，因为 padding 的百分比是相对于宽度计算的。例如可以设置一个元素的 width 为 100%，padding-top 为 56.25%，从而实现 16:9 的比例。此外，现代浏览器还支持 aspect-ratio 属性，可以直接设置元素的宽高比，例如 aspect-ratio: 16/9，这种方式更加直观且易维护。
---
## Chunk 198 — React和React Native的区别

React和React Native的区别

React Native 和 React最大的区别在于渲染目标不同。React最终生成的是浏览器 DOM，而 React Native 不依赖浏览器，它会把组件树转换成原生组件，例如 iOS 的 UIView 或 Android 的 View。在实现上，React Native 会在 JS 线程生成组件描述，然后通过 Bridge 和 Native 线程通信  
，由 Native 去创建和更新 UI。这种方式的好处是可以复用 React 的开发模式，但缺点是跨线程通信会带来性能开销，所以在列表或高频更新场景需要特别注意优化。  
JSI 是“JS 和 Native 怎么通信”的新接口层在旧架构里，React Native 主要靠异步 Bridge 把 JS 和 Native 之间的数据序列化后再传过去；新架构用 JSI 取代了这条异步 Bridge 路径，让 JavaScript 可以直接持有 C++对象引用、C++也能持有 JS 侧对象引用，从而避免大量序列化和跨层复制的成本。React Native 官方文档把 JSI 描述成一种把 JavaScript 引擎嵌入到 C++程序中的轻量接口；新架构也明确说它移除了旧的异步 Bridge，并以 JSI 作为新的互操作基础。  
这件事为什么重要，可以用一个很实际的例子理解：如果 JS 和 Native 之间传的是小字符串、小数字，旧 Bridge 的序列化开销可能还能接受；但如果你在做相机、音视频、实时图像处理，数据量会非常大。官方就拿 VisionCamera 举例，单帧缓冲区可能是几十 MB，按高帧率算每秒要传很多数据，这时候旧 Bridge 的序列化成本就会成为瓶颈，而 JSI 更适合这种高吞吐的场景。
---
## Chunk 199 — 序列化是什么

序列化是什么

序列化就是把内存中的对象转换成可以传输的格式，比如 JSON。在 React Native 旧架构中，JS 和 Native 不在同一内存空间，所以需要通过序列化把数据传过去，再在 Native 侧反序列化。 const obj = { name: "Alice", age: 20 }; 序列化后（JSON）JSON.stringify(obj)//'{"name":"Alice","age":20}' 变成纯字符串（可以跨语言传输）反序列化 JSON.parse('{"name":"Alice","age":20}')
---
## Chunk 200 — 为什么需要序列化

为什么需要序列化

因为不同环境之间不能直接共享内存。在 React Native中，JS 运行在 JS Engine（Hermes/JSCore），Native 是 Objective-C/Java/C++。它们不在同一内存空间，不同语言，不能直接传对象。
---
## Chunk 201 — 为什么Bridge会成为性能瓶颈

为什么Bridge会成为性能瓶颈

因为Bridge是JS 和 Native 之间的“中转站”，它异步执行，为了减少通信次数有批处理（batch）因此有延迟，尤其是在序列化成本很大的情况下。跨语言+跨线程+序列化 = 性能损耗。例如场景：滚动一个列表（FlatList），如果你写得不好：每一帧滚动 → JS算布局 → 传给Native，结果：60fps → 需要每16ms更新一次，Bridge根本跟不上，就会：卡顿、掉帧。JSI相较于Bridge不再“传数据”，而是“共享引用”，相比于Bridge：JS → JSON → Native → parse，JSI让JS 直接调用 C++对象，因此更快更实时更适用于大数据。
---
## Chunk 202 — JS 线程、渲染线程、原生 UI 线程

JS 线程、渲染线程、原生 UI 线程

JS 线程负责业务逻辑，渲染线程负责布局和绘制，原生 UI 线程负责真正把界面渲染到屏幕并响应用户交互，这三者通过异步通信协作完成界面更新。
---
## Chunk 203 — 为什么 RN 比 Web 更容易卡

为什么 RN 比 Web 更容易卡

Web 页面更新主要发生在浏览器环境里，React DOM 直接面向 DOM 和浏览器渲染管线；而 React Native 的 UI 最终要落到原生视图系统上，JS 逻辑、布局、动画、手势、图片、列表这些事情经常会牵涉 JS 线程、渲染线程、原生 UI 线程之间的配合。Web 的这些线程在浏览器内部高度协同，而 RN 的 JS 和 Native UI 需要跨系统通信，导致调度和通信成本更高，因此更容易卡。旧架构下，频繁跨 Bridge 通信、序列化和批量异步传递会带来明显开销；新架构虽然通过 JSI/Fabric 显著改善了这一点，但如果你的组件本身 re-render 很多、列表很多、图片很多、动画很多，依然会卡。官方也明确说了，新架构不是“自动变快按钮”，很多性能问题仍然来自应用代码本身。  
你可以把 RN 比 Web 更容易卡理解成三类典型问题。第一类是列表和长页面：移动端屏幕小，但滚动频率高，如果一次性渲染太多项、每个 item 又很重，就容易掉帧。第二类是图片和媒体：高分辨率图片、相机、视频、地图，都会给内存和渲染带来很大压力。第三类是高频更新：例如滚动时不断 setState、频繁 useEffect、副作用里做重计算、动画跑在 JS 线程上，这些都很容易让 JS 主线程忙不过来，最终表现成卡顿、掉帧、点击延迟。
---
## Chunk 204 — FlatList 为什么快

FlatList 为什么快

FlatList 为什么快，本质上是因为它不是把所有列表项一次性都渲染出来，而是做了虚拟化：只渲染当前可见区域附近的一小部分 item，并维护一个“渲染窗口”。当你滚动时，已经离开视口的 item 会被回收或复用，新进入视口的 item 再被渲染。这样能显著降低首屏渲染量、内存占用和滚动时的更新压力。所以 FlatList 比 ScrollView 更适合长列表，因为 ScrollView 倾向于把所有子节点都挂上去。你面试时可以直接说：FlatList 快，不是因为它渲染更快，而是因为它“少渲染了很多本来没必要现在渲染的东西”。FlatList需要KeyExtract，因为 keyExtractor 是为了保证每个 item 有稳定的 key，这样 React 在 diff 时可以正确复用组件，避免不必要的重新渲染。
---
## Chunk 205 — useEffect 为什么可能导致卡顿

useEffect 为什么可能导致卡顿

useEffect 为什么可能导致卡顿，不是因为它这个 hook 本身慢，而是因为很多人把重逻辑塞进了 effect。比如组件一挂载就发多个请求、做复杂数据处理、注册很多监听、开 interval、在依赖变化时又不断重复执行。更糟的是，依赖数组写不好还会导致 effect 反复触发，形成“render → effect → setState → render → effect”的循环。RN 里这类问题更容易被放大，因为移动设备性能更有限，而且 effect 往往还会牵涉网络、布局、手势或原生模块交互。你可以把它理解成：useEffect 本来是“副作用管理工具”，但如果你把大量重活都放进去，它就会变成性能问题入口。  
RN 如何优化首屏  
第一，减少首屏必须渲染的内容。首屏不要一次把很多模块都拉下来，尤其不要一打开页面就全量加载长列表、高清图和复杂卡片。第二，尽量让 JS 启动更快。Hermes 是官方默认并且官方明确推荐的引擎，它通常能改善启动时间、降低内存占用，并且在 release build 中以更高效的方式加载 JS。第三，把非关键内容延后。比如首屏先展示基础骨架和关键卡片，评论、次级列表、历史记录、复杂图表延迟加载。第四，控制图片和资源。首屏图片数量要少，尺寸要合理，优先压缩和使用缓存。第五，列表首屏只渲一小段，用 FlatList 并合理控制 initialNumToRender 之类的窗口参数思路。官方关于 Hermes 和 JS 加载优化也明确强调了这一方向。
---
## Chunk 206 — RN性能优化

RN性能优化
---
## Chunk 207 — RN性能优化

启动性能、渲染性能、列表性能、图片性能、JS/Native 通信、动画与交互、包体与运行时 React Native 的性能优化我通常分成几层来看。第一层是启动性能，我会优先确认 Hermes 已开启，因为它会改善启动时间、降低内存占用、缩小包体，而且现在是默认引擎。第二层是渲染性能，核心是减少不必要的 re-render，比如对列表 item 做 memo、保持 props 稳定、避免父组件状态变化把大面积子树带着更新。但在 RN 里这件事更重要，因为每次 render 后可能还要触发 JS 到 Native 的更新链路，尤其在旧架构里更明显。新架构虽然降低了通信成本，但“无意义更新”本身仍然是浪费。官方也提醒过，启用新架构不意味着你的 app 会自动更快，很多性能收益仍然取决于你的代码是否真的利用了这些能力。第三层是列表性能，大数据量场景优先 FlatList 而不是 ScrollView，并合理控制初始渲染数量和渲染窗口。第四层是图片和资源性能，避免一次加载过多大图，结合压缩、CDN 和缓存。第五层是 JS 与 Native 的交互成本，尤其在旧架构下要避免高频大体积跨 Bridge 通信；新架构里的 JSI 和 Fabric 可以降低这部分开销，但代码层面仍然需要减少无意义更新和不必要的数据传输。总体上，新架构给了更好的上限，但真正的性能还是要靠组件设计、列表策略和资源管理来做。
---
## Chunk 208 — RN性能优化

Fabric 是“React Native 怎么渲染 UI”的新渲染系统。官方把 Fabric 定义为 React Native 的新 rendering system，也就是新的渲染器。它的核心目标之一是把更多渲染逻辑统一到 C++，增强和宿主平台的互操作性，并解锁新能力。换句话说，JSI 更偏“通信基础设施”，Fabric 更偏“UI 渲染引擎”。你可以把它们理解成：JSI 解决“怎么高效沟通”， Fabric 解决“UI 怎么更现代、更高效地渲染”。 Fabric 是新的渲染系统，它让 RN 更接近现代 React 的渲染模型，同时新架构并不会自动让应用变快，真正性能还得靠列表、渲染和资源优化。  
再细一点讲，Fabric 把 React Native 的渲染流程拆成类似 React 的 render、commit、mount 三个阶段。Render 阶段根据 props/state 计算出新的树；commit 阶段确定要应用哪些变更；mount 阶段把这些变更真正应用到平台 UI 上。官方文档明确把这叫作 render pipeline。Fabric 不是简单 “更快”，它本质上是让 RN 的渲染架构更接近现代 React，能更好支持 Suspense、Transitions、 automatic batching、useLayoutEffect 等新能力。React Native 官方在 0.76 的新架构介绍里也明确强调，新架构带来了对现代 React 特性的完整支持。  
现在 React Native 新架构已经主流了，React Native 0.76 起新架构默认开启；而且 0.74 开始在新架构下 Bridgeless 默认启用，说明社区方向已经非常明确。
---
## Chunk 209 — 为什么 Flutter 比 RN 更流畅

为什么 Flutter 比 RN 更流畅

Flutter 是 Google 的跨平台 UI 框架，和 React Native 最大的区别在于它不依赖原生组件，而是通过自己的渲染引擎（Skia）直接绘制 UI。相比之下，React Native 是通过 JS 控制原生组件来渲染界面，因此需要 JS 和 Native 之间的通信，这在某些高频场景下可能带来性能开销。Flutter 因为没有这层通信，动画和滚动通常更流畅，但代价是它不是完全使用原生 UI，平台一致性和生态会有一些差异。
---
## Chunk 210 — 为什么 Flutter 比 RN 更流畅 > 10. 数据库

为什么 Flutter 比 RN 更流畅 > 10. 数据库

1. INNER JOIN 是什么？只返回两张表中匹配的记录（交集）。  
2. LEFT JOIN 是什么？返回左表全部数据，右表匹配不到用 NULL 补。
---
## Chunk 211 — 为什么 Flutter 比 RN 更流畅 > 3. RIGHT JOIN 是什么？

为什么 Flutter 比 RN 更流畅 > 3. RIGHT JOIN 是什么？

返回右表全部数据，左表匹配不到用 NULL 补。（实际上right join很少用）  
4. LEFT JOIN 和 INNER JOIN 区别？ INNER 只要交集，LEFT 会保留左表全部。  
5. WHERE 和 HAVING 区别？ WHERE 在分组前过滤行；HAVING 在分组后过滤结果，可用聚合函数。  
6. GROUP BY 是干嘛的？按某个字段分组，通常配合 COUNT/SUM 等聚合函数使用。  
7. 常见聚合函数有哪些？ COUNT、SUM、AVG、MAX、MIN。  
8. 索引是什么？用于提高查询效率的数据结构，通常是 B+树。  
9. 索引有什么作用？加快查询速度，减少全表扫描。
---
## Chunk 212 — 答：不一定，写操作会变慢

答：不一定，写操作会变慢

10. 什么情况下用索引？ WHERE、JOIN、ORDER BY、GROUP BY 的字段。  
11. 索引什么时候失效？ like '%xx'、对字段做函数/计算、类型不匹配。  
12. 主键和唯一索引区别？主键唯一且不为 NULL，一个表只能一个；唯一索引可以多个且允许 NULL。  
13. 什么是事务？一组操作要么全部成功，要么全部失败。  
14. 事务的 ACID 是什么？ 1. Atomicity 原子性：一个事务里的操作，要么全部成功，要么全部失败。  
2. Consistency 一致性：事务执行前后，数据库都必须是合法状态。比如账户余额不能为负、订单必须对应一个真实用户、主键不能重复。  
3. Isolation 隔离性：多个事务同时执行时，彼此不要互相干扰。  
比如事务 A 正在改余额，还没提交，事务 B 不应该随便读到这个未提交的数据。
---
## Chunk 213 — 幻读：范围查询两次，行数变了

幻读：范围查询两次，行数变了

隔离级别越高，越安全，但性能越低。  
4. Durability 持久性：事务一旦提交，数据就应该永久保存。比如你转账成功，数据库 COMMIT 了，即使服务器突然宕机，数据也不应该丢。数据库一般通过日志机制保证，比如 MySQL 的 redo log。  
15. 常见隔离级别有哪些？读未提交、读已提交、可重复读、串行化。  
16. SELECT 执行顺序？ FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT。  
👉 追问：为什么 SELECT 最后？  
👉 答：因为要先确定数据再选字段  
17. LIMIT 是干嘛的？限制返回数据条数（分页）。  
18. 什么是回表？通过索引查到主键后，再回主表查完整数据。
---
## Chunk 214 — 👉 答：多一次 IO

👉 答：多一次 IO

19. 什么是覆盖索引？查询字段全部在索引中，不需要回表。  
20. DELETE 和 TRUNCATE 区别？ DELETE 可回滚逐行删除；TRUNCATE 清空表、不可回滚、速度更快。
---
## Chunk 215 — 👉 答：多一次 IO > 11. 其他

👉 答：多一次 IO > 11. 其他

了解的设计模式单例模式：保证类只有一个实例，并提供一个访问它的全局访问点。  
工厂模式：用来创建对象，根据不同的参数返回不同的对象实例。  
策略模式：定义一系列的算法，把它们一个个封装起来，并且使它们可以相互替换。  
装饰器模式：在不改变对象原型的基础上，对其进行包装扩展。  
观察者模式：定义了对象间一种一对多关系，当目标对象状态发生改变时，所有依赖它对对象都会得到通知。  
发布订阅模式：基于一个主题/事件通道，希望接收通知的对象通过自定义事件订阅主题，被激活事件的对象（通过发布主题事件的方式被通知)。  
OSI七层模型（好像比较后端）  
物理层：通过媒介传输比特,确定机械及电气规范（比特Bit）数据链路层：将比特组装成帧和点到点的传递（帧Frame）网络层：负责数据包从源到宿的传递和网际互连（包PackeT）传输层：提供端到端的可靠报文传递和错误恢复（段Segment）会话层：建立、管理和终止会话（会话协议数据单元SPDU）  
表示层：对数据进行翻译、加密和压缩（表示协议数据单元PPDU）应用层：允许访问OSI环境的手段（应用协议数据单元APDU）
---
## Chunk 216 — 内存缓存和磁盘缓存分别做什么

内存缓存和磁盘缓存分别做什么

内存缓存速度最快，适合存最近用过、马上可能再用的图片，例如用户往上回刷，命中内存缓存会非常快。磁盘缓存的容量更大，适合存已经下载过但不适合一直放内存的资源，防止重新走网络。一般先查内存再去查字盘。
---
## Chunk 217 — 以下是我觉得考的概率比较低的/没怎么在网上的前端面经里看到过的

以下是我觉得考的概率比较低的/没怎么在网上的前端面经里看到过的
---
## Chunk 218 — 以下是我觉得考的概率比较低的/没怎么在网上的前端面经里看到过的

NPM 依赖版本号 ~ 和 ^ 的区别在 NPM 中，^ 和 ~ 都用于控制依赖版本的升级范围。^ 表示允许升级 minor 和 patch 版本，例如 ^1.2.3 可以升级到 1.x.x，但不会升级到 2.0.0；而 ~ 只允许升级 patch 版本，例如 ~1.2.3 只能升级到 1.2.x。换句话说，^ 更宽松，适合大多数情况，而 ~ 更保守，适合对稳定性要求较高的场景。  
如果用户能拿到请求 URL，如何防止被爬取或滥用如果用户可以获取到接口 URL，前端本身无法真正保护接口安全，必须依赖后端措施。常见方法包括鉴权机制（如 token、JWT）、请求签名、防止重放攻击（timestamp+nonce）、接口限流（rate limiting）、以及通过 Referer 或 IP 白名单限制访问。同时可以结合 HTTPS 防止中间人攻击。前端可以做的更多是减少暴露，比如避免直接暴露敏感参数，但核心安全必须在服务端实现。  
TypeScript 项目中 ESLint 是否支持子路径导入 ESLint 本身可以支持子路径导入，但需要配合解析器和插件，例如使用 eslint-import-resolver-typescript 来解析 tsconfig 中的 paths 配置。通过配置后，ESLint 就可以正确识别类似 @/components 这样的路径别名，并进行校验和提示。  
Git merge 和 rebase 区别，对历史的影响 merge 是将两个分支的历史合并，会生成一个新的 merge commit，保留原有提交历史；而 rebase 是将当前分支的提交“移动”到目标分支之后，相当于重写提交历史，使历史更加线性。merge 不会改变历史，适合多人协作；rebase 会改变 commit hash，因此不适合对已经共享的分支使用。
---
## Chunk 219 — 以下是我觉得考的概率比较低的/没怎么在网上的前端面经里看到过的

命令模式 vs 数据快照，如何优化回滚到很久之前命令模式的优点是存储成本低，但回滚时需要逐步执行所有反操作，效率较低；而数据快照可以快速回滚，但占用空间较大。如果需要回滚到很久之前，可以采用“checkpoint”策略，即定期保存完整快照，中间记录增量操作，这样回滚时可以先回到最近的快照，再执行少量操作，从而兼顾性能和空间。  
WeakMap 和 Map 区别 WeakMap 的 key 必须是对象，并且是弱引用，不会阻止垃圾回收，因此适合存储临时数据或私有属性；而 Map 的 key 可以是任意类型，并且是强引用，需要手动删除。WeakMap 不可遍历，这也是为了避免影响垃圾回收机制。  
requestAnimationFrame 和 requestIdleCallback requestAnimationFrame 是在浏览器下一次重绘之前执行回调，适合做动画更新；而 requestIdleCallback 是在浏览器空闲时执行任务，适合低优先级任务，例如数据预加载或日志处理。  
为什么使用 requestAnimationFrame，有什么特性 requestAnimationFrame 的优势在于它与浏览器刷新频率同步，通常是 60fps，从而保证动画流畅，同时在页面不可见时会自动暂停，节省性能。但它不能保证一定执行，因为如果主线程被阻塞或帧率下降，回调可能延迟执行。
---
## Chunk 220 — 如何让对象不可变可以使用 Object.freeze 将对象冻结，使其属性不可修改；如果需要深层不可变，可以递归冻结所有嵌套对象。在实际项目中，也常通过不可变数

如何让对象不可变可以使用 Object.freeze 将对象冻结，使其属性不可修改；如果需要深层不可变，可以递归冻结所有嵌套对象。在实际项目中，也常通过不可变数

据结构或浅拷贝来保证数据不被直接修改，例如 Redux 中的状态更新。  
简历+后端八股
---
## Chunk 221 — 一、网络编程

一、网络编程

1. 网络分层应用层协议（HTTP/DNS）传输层协议（TCP/UDP）网络层协议（IP）  
HTTP（应用层）GET/index.html ↓ TCP（传输层）负责建立连接，确保送到和顺序 ↓ IP（网络层）找到目标地址  
2. TCP与UDP 的核心区别有哪些？ TCP 是面向连接的（会先建立连接）、可靠的传输协议（必须确认收到），提供顺序保证（即使2先到 Receiver也会先等1再按顺序排好）、重传机制（丢了会补发）和拥塞控制； UDP 是无连接的、不可靠的协议，不保证顺序和重传，但开销更小、延迟更低。
---
## Chunk 222 — 一、网络编程 > 3. TCP 的三次握手和四次挥手三次握手

一、网络编程 > 3. TCP 的三次握手和四次挥手三次握手

1. 客户端发送 SYN (Synchronize) 2. 服务端返回 SYN+ACK 3. 客户端发送 ACK (Acknowledgement)，连接建立  
核心是同步双方序列号不是两次 - 防止旧的连接请求影响新连接（避免历史 SYN 包）第三次 ACK 丢失或根本没有设计第三次确认，会导致服务端误以为连接已经建立。
---
## Chunk 223 — 四次挥手

四次挥手
---
## Chunk 224 — 四次挥手

1. Client → FIN (Finish) 2. Server → ACK（只是server知道client向自己发完了，但server自己可能还没发完） 3. Server → FIN 4. Client → ACK  
四次挥手的本质是：TCP 的两个方向必须独立关闭，而不是一次性关闭整个连接。  
TCP 是全双工通信，连接的两个方向是独立的。当主动关闭方发送 FIN 时，只表示自己不再发送数据，但仍然可以接收数据。被动方在收到 FIN 后，可能还有未发送完成的数据，因此需要先发送 ACK 确认，再在数据发送完毕后发送 FIN，从而导致四次挥手。  
如果四次挥手时，主动方发送的最后一个ACK 丢失，被动方会因未收到ACK 超时重传FIN 报文，主动方在TIME_WAIT 状态下会重新发送ACK。若超过重传次数，被动方会关闭连接；主动方TIME_WAIT 超时后也会关闭连接，确保连接最终释放。  
4. DNS 解析 DNS 解析是将域名（如www.qq.com）转换为IP 地址的过程浏览器缓存（客户端先查询本地缓存，命中则返回IP） ↓ 操作系统缓存 ↓ 本地 DNS 服务器（本地DNS 负责全程递归查询） ↓ 根域名服务器（问谁管.com，返回.com的服务器地址） ↓ 顶级域名服务器（问谁管google.com，返回权威DNS地址） ↓ 权威 DNS 服务器 ↓ 返回 IP
---
## Chunk 225 — 四次挥手

5. HTTP/1.1、HTTP/2、HTTP/3 的主要区别 HTTP/2 的多路复用机制是如何实现的？ HTTP/1.1 是文本协议（长连接+管线化），存在队头阻塞 HTTP/2 是二进制协议，支持多路复用（并发请求 - 将请求/响应拆分为二进制帧，每个帧标记流ID，同一连接中多个流并行传输，互不干扰）+头部压缩 (HPACK)，但还是基于TCP，由于TCP是一个流因此无法完全解决队头阻塞问题 - 若TCP层出现丢包，整个连接会堵塞，所有流都受影响。 HTTP/3 基于QUIC（UDP）从根本上解决TCP 队头阻塞 - 为每个流分配独立的UDP 数据包，丢包仅影响对应流，其他流正常传输，握手延迟低（1RTT），支持0-RTT 重连。HTTP/2  
6. HTTPS的加密流程 SSL/TLS协议的作用 HTTP+SSL/TLS，用于在客户端和服务器之间建立加密、安全的通信通道。 SSL/TLS 提供加密通信(Confidentiality)、身份认证 (Authentication)和数据完整性 (Integrity)保护。  
SSL (Secure Sockets Layer) 用于加密网络通信的安全协议，现在已废用 ● TLS (Transport Layer Security) SSL的升级版本，握手过程被优化，可以减少RTT  
加密流程 1. SSL/TLS 握手：客户端发起请求 2. 服务端回CA 证书（防止中间人攻击）、共钥（锁）、域名  
3. 客户端验证证书有效后，生成一个随机key，并用服务器共钥加密（把key放进箱子用锁锁住）。通过服务端公钥加密传输，即使被拦截，无服务端私钥也无法解密，能进一步提升密钥安全性，避免会话密钥直接暴露。 4. 服务器用私钥（钥匙）解密得到key，双方生成对称密钥 5. HTTP 数据传输：用会话密钥（对称加密）加密数据，MAC 校验完整性。
---
## Chunk 226 — 四次挥手

7. TCP 和UDP 的应用层协议（实际用的功能规则） TCP: HTTP（网页传输）\ HTTPS（加密网页）\ FTP（文件传输） UDP: DNS（域名解析）\ DHCP（地址分配） \ 视频/语音（如 RTP）  
HTTP 是用于客户端与服务器之间进行资源请求和响应的应用层协议（浏览网页、请求数据、调用 API） HTTP不能基于UDP是因为网页加载数据量大，且顺序必须对 FTP 是用于在客户端和服务器之间传输文件的协议，支持上传和下载（传大文件） SMTP 用于发送邮件，从客户端到服务器，或服务器之间传输邮件。基于 TCP（可靠）  
DNS 用于将域名解析为 IP 地址，是互联网访问的第一步（上网时计算器只认IP） DNS 基于UDP 是因查询请求数据量小，UDP 低延迟能提升解析速度。若数据量过大，DNS 会自动切换为TCP协议传输，确保数据完整传输。DNS丢包会重新发请求，不依赖TCP的重传机制。它会设置timeout，如果没收到响应再重新发送请求。这就是把可靠性从传输层上移到应用层，保证可靠的同时更轻量（没有三次握手延迟更低） DHCP 用于动态分配 IP 地址，使设备无需手动配置即可接入网络（连接WIFI自动获得IP地址） RTP Real-time Transport Protocol用于实时音视频传输，强调低延迟而非完全可靠（视频通话、直播、游戏语音，强调快而非可靠）
---
## Chunk 227 — 四次挥手 > 8. RESTful API

四次挥手 > 8. RESTful API

RESTful API 是一种基于 HTTP 的接口设计风格，用“资源+HTTP 方法”来描述系统操作。  
传统写法：/getUser，把行为写进URL ● RESTful API：/users，操作靠HTTP方法
---
## Chunk 228 — 核心原则

核心原则

1. 资源导向：URL 表示资源（如/users/123，而非/getUser?id=123） 2. HTTP 方法语义化：GET 查询、POST 创建、PUT 全量更新、PATCH局部更新、DELETE 删除。（如DELETE/users/1，而非/deleteUser） 3. 无状态：请求包含所有必要信息，不依赖会话； 4. 统一接口：用标准HTTP 状态码（200 成功、404 未找到）和响应格式； 5. 可缓存：支持GET 请求缓存，提升性能； 6. 资源分层：客户端无需了解服务
---
## Chunk 229 — 优点：URL简洁、方法语义准确、响应格式统一

优点：URL简洁、方法语义准确、响应格式统一
---
## Chunk 230 — 优点：URL简洁、方法语义准确、响应格式统一

9. 粘包和拆包粘包：多个数据包合并接收（发送Hello和World，接受端收到HelloWorld）拆包：单个数据包拆分接收（发送Hello，接受端收到He和llo）原因  
TCP 是流式传输，没有消息边界 ● 发送端缓冲区未满时把多个小包合并发送（提高效率），接受端缓冲区有限，拆分接收 ● Nagle算法让小数据被合并发送，更容易粘包  
解决方案 1. 固定消息长度（如每个消息1024 字节，不足补零） 2. 分隔符标记（如用“\r\n”结尾），适用于文本数据，需要通过转译处理避免冲突 3. 消息头+消息体（头中包含消息长度），通用且可靠，适用于二进制数据  
12. 网络IO 模型程序如何等待和处理网络数据的方式，一次网络IO实际执行等待数据到达和把数据拷贝到用户空间，IO模型的区别在于怎么等+谁来通知+是否阻塞  
同步阻塞 (BIO Blocking IO)：BIO 中，线程在 read/write 时会一直阻塞，直到 IO 完成，因此实现简单，但在高并发下需要大量线程，扩展性较差。（如小型TCP 服务器）  
同步非阻塞 (NIO Non-Blocking IO)：同步非阻塞 IO 中，线程不会在单次 read 上阻塞，  
但需要不断轮询数据是否就绪，因此会增加 CPU 开销，适用于低并发、对延迟敏感场景。 IO多路复用 (select/poll/epoll)：一个线程监听多个IO 事件，数据准备好后通知应用层，阻塞于select/poll/epoll，适用于高并发（如百万级连接） ○ select - 有数量限制（1024），每次都要遍历 ○ poll - 无数量限制，仍然遍历 ○ epoll - 事件驱动，不需要便利，高性能，是高并发服务器的基础  
异步IO (AIO)：内核完成数据准备和拷贝后通知应用层，应用层无需阻塞，适用于高并发、低延迟场景（如磁盘IO、网络IO）  
高并发网络编程优先用IO 多路复用（epoll），磁盘IO 密集场景用异步IO；通过合理选型平衡性能和开发复杂度，提升系统并发能力。
---
## Chunk 231 — 优点：URL简洁、方法语义准确、响应格式统一 > 二、OS 操作系统与进程通讯

优点：URL简洁、方法语义准确、响应格式统一 > 二、OS 操作系统与进程通讯
---
## Chunk 232 — 优点：URL简洁、方法语义准确、响应格式统一 > 二、OS 操作系统与进程通讯

1. 进程与线程进程和线程的本质区别是什么？线程共享进程的哪些资源？又有哪些独立的资源？进程是资源分配单位，线程是调度执行单位，这是核心区别；线程共享进程的核心资源，仅保留执行相关的独立资源，实现轻量级并发。本质区别：进程拥有独立地址空间，线程共享进程地址空间，线程切换开销远低于进程。共享资源：代码段、数据段、堆、文件描述符、信号处理方式等。独立资源：线程栈（存储局部变量）、程序计数器（记录执行位置）、寄存器组（保存执行状态）、线程私有数据（如线程局部存储TLS）。正因为共享资源多，线程通信更高效，但也需同步保护临界资源。  
开发中我会根据并发需求选型，高并发场景用线程减少开销，需资源隔离时用进程；同时做好线程同步，避免共享资源竞争导致的问题。  
追问1：为什么线程切换开销比进程小？具体体现在哪些方面？进程切换需切换地址空间（更新页表、刷新TLB），而线程共享地址空间，无需此操作；其次线程仅需保存/恢复自身独立资源（栈、寄存器等），数据量远少于进程的完整上下文，因此切换速度更快。  
2. 进程的上下文切换什么是进程的上下文切换？上下文切换的开销主要体现在哪些方面？如何减少上下文切换？  
上下文切换是CPU 保存当前进程状态、加载新进程状态的过程，开销体现在多方面；减少切换需从进程管理、调度等层面综合优化。开销体现：1. 时间开销：保存/恢复寄存器、程序计数器等状态； 2. 资源开销：内核占用CPU 处理切换；3. 缓存失效：新进程替换缓存，导致缓存命中率下降。  
减少方法：1. 用线程替代进程（线程切换开销低）；2. 合理设置线程池大小（避免过多线程竞争）；3. 优化锁机制（如用自旋锁减少阻塞）；4. 调整进程优先级，避免频繁抢占。开发中我会合理设计并发模型，用线程池控制并发数，通过细粒度锁减少线程阻塞；同时关注系统调度状态，避免不必要的上下文切换，提升性能。
---
## Chunk 233 — 优点：URL简洁、方法语义准确、响应格式统一 > 二、OS 操作系统与进程通讯

追问1：为什么线程上下文切换的开销比进程小？具体小在哪些环节？因为线程共享进程的地址空间，而进程有独立地址空间。线程切换无需切换地址空间（省去更新页表、刷新TLB 的开销），仅需保存/恢复线程自身的独立资源（栈、寄存器、程序计数器），这些数据量远少于进程的完整上下文（包含地址空间信息），因此切换开销显著降低。  
3. 死锁什么是死锁？死锁产生的四个必要条件是什么？如何预防和解决死锁问题？  
死锁定义：多个进程持有部分资源，同时等待对方持有的资源，形成循环等待而无法推进的状态。四个必要条件：互斥、持有并等待、不可剥夺、环路等待。预防措施：按顺序分配资源（破坏环路等待）、一次性申请所有资源（破坏持有并等待）。
---
## Chunk 234 — 解决方法：

解决方法：

1. 检测：用资源分配图判断死锁 ● 2. 恢复：终止优先级低的进程、剥夺部分进程资源，释放后打破循环。  
开发中我会采用“按顺序申请资源”等预防策略，同时在系统中设计死锁检测机制，定期检查资源分配状态，避免死锁导致系统不可用。  
追问：“按顺序分配资源”为什么能破坏环路等待条件？实际开发中如何落地？按顺序分配要求所有进程按统一资源序号申请，比如资源A 序号1、资源B 序号2，进程必须先申请A 再申请B，无法出现“进程1持B 等A，进程2 持A 等B”的环路。落地时需给系统资源编号，在代码中强制按序号申请，避免乱序请求。
---
## Chunk 235 — 解决方法： > 4. 临界区 "什么是临界区？

解决方法： > 4. 临界区 "什么是临界区？
---
## Chunk 236 — 解决方法： > 4. 临界区 "什么是临界区？

如何保证多个线程对临界区资源的安全访问？（请举例说明实现方式）  
临界区是访问共享资源的代码段，多线程并发访问易导致数据不一致；需通过互斥、原子操作等机制保证安全，常用锁和信号量实现。  
1. 互斥锁（如Java 的synchronized）：线程进入临界区前获取锁，执行完释放，未获取到则阻塞，适合复杂临界区 2. 自旋锁：线程获取不到锁时循环等待，不放弃CPU，适合临界区执行时间短的场景；3. 原子操作（如C++的std::atomic）：通过CPU 指令保证操作原子性，无需锁，适合简单变量修改（如计数器递增）。开发中我会根据临界区特性选型，简单操作用原子类，复杂逻辑用互斥锁；同时避免锁粒度过大，通过细粒度锁减少线程阻塞，提升并发效率。  
追问：自旋锁和互斥锁的核心区别是什么？为什么“临界区执行时间短”适合用自旋锁？核心区别是获取不到锁时的行为：自旋锁循环等待（忙等），互斥锁阻塞线程（放弃CPU）。临界区执行时间短时，自旋等待的时间远小于线程阻塞-唤醒的开销，用自旋锁能减少上下文切换，提升效率；若执行时间长，自旋会浪费CPU 资源，此时互斥锁更合适。  
5. 内存分页，分段机制，虚拟内存请解释内存分页和分段机制的原理，它们的区别是什么？虚拟内存的实现依赖于哪些技术？分页按固定大小拆分物理内存，分段按逻辑模块拆分地址空间，二者定位不同；虚拟内存依赖地址转换、分页等技术，实现内存扩容与隔离。原理与区别：  
分页：将物理内存和虚拟内存均划分为固定大小页（如4KB），通过页表映射地址，优点内存利用率高，缺点无逻辑关联。分段：按代码、数据等逻辑模块拆分为段，段大小不固定，优点逻辑清晰，缺点易产生内存碎片。虚拟内存依赖技术：虚拟地址与物理地址转换、分页机制、缺页中断（触发页面加载）、交换（页面与磁盘交互）。  
开发中我会关注内存使用效率，比如避免内存碎片（参考分页思想），通过合理分配内存减少缺页次数，提升程序在虚拟内存环境下的性能。
---
## Chunk 237 — 解决方法： > 4. 临界区 "什么是临界区？

开发中我会关注内存使用效率，比如避免内存碎片（参考分页思想），通过合理分配内存减少缺页次数，提升程序在虚拟内存环境下的性能。  
追问1：分页机制中的“页表”作用是什么？为了解决页表过大的问题，操作系统采用了什么优化方案？页表用于存储虚拟页号到物理页号的映射关系，实现地址转换。优化页表过大的方案是多级页表（如二级、三级），只将常用的页表项加载到内存，不常用的存放在磁盘，减少内存占用；还可结合TLB（快表）加速地址查找。  
6. 进程间通信的方式、优缺点及应用场景进程间通信的方式有管道、消息队列、共享内存、信号量、Socket等。进程间通信分数据传输和同步两类，管道、消息队列等侧重数据传输，信号量侧重同步；需根据性能、场景需求选择，共享内存是本地最快方式。优缺点及场景： 1. 匿名管道：优点简单，缺点仅父子进程用，适合本地简单数据传输 2. 消息队列：优点有消息边界，缺点开销比管道大，适合本地非实时数据交换 3. 共享内存：优点速度最快，缺点需同步保护，适合本地高吞吐场景 4. 信号量：无数据传输，用于同步互斥 5. Socket：支持跨网络，缺点开销大，适合跨主机通信。  
开发中本地高并发用共享内存+信号量，简单本地通信用管道，跨网络用Socket；通过合理选型平衡性能与开发成本，确保进程间协作高效可靠。  
追问1：共享内存为什么是最快的IPC 方式？使用时必须搭配什么机制？为什么？共享内存让进程直接访问同一块物理内存，无需内核中转（如管道需拷贝数据到内核缓冲区），省去两次数据拷贝，故速度最快。必须搭配同步机制（如信号量、互斥锁），否则多个进程同时读写会导致数据竞争，破坏数据一致性。  
7. 操作系统的进程调度算法有哪些？  
进程调度算法围绕公平性和效率设计，FCFS、短作业优先、时间片轮转等各有侧重，分别适配批处理、实时、交互式等不同场景。  
1. 时间片轮转：为进程分配固定时间片，轮转执行，抢占式，响应快，适合交互式系统 2. 优先级调度：按优先级分配CPU，抢占式，需搭配“老化机制”缓解饥饿，适合实时系统。
---
## Chunk 238 — 三、数据结构与算法

三、数据结构与算法

1. 数组与链表数组和链表的区别是什么？在实际开发中如何根据场景选择使用数组或链表？  
数组和链表的核心区别在存储结构，数组连续存储支持随机访问，链表离散存储适合灵活增删  
具体区别：数组内存连续，可通过下标O(1)随机访问，增删中间元素需移动数据（O(n)），栈/堆均可分配，内存碎片少。链表节点离散，靠指针关联，只能顺序访问（O(n)），增删节点仅改指针（O(1)），仅存堆上，易产生碎片。查多改少用数组（如配置列表），增删频繁且在首尾用链表（如消息队列）。
---
## Chunk 239 — Java 中的ArrayList 和LinkedList 分别对应数组和链表，为什么遍历LinkedList 时用迭代器比 for 循环快？

Java 中的ArrayList 和LinkedList 分别对应数组和链表，为什么遍历LinkedList 时用迭代器比 for 循环快？

LinkedList 用for 循环遍历会通过get(i)每次从头节点开始查找（O(n)），n 次遍历总复杂度O(n²)；迭代器通过指针记录当前节点，每次next()仅移动一步（O(1)），总复杂度O(n)，因此迭代器更高效。  
2. 单链表的反转，环检测，中间节点查找这三个操作均可通过指针控制实现，环检测和中间节点查找用快慢指针能优化空间，反转需关注前驱节点的保存，均要处理空链表等边界。  
反转：初始化前驱null、当前节点为头节点，循环中用临时变量存后继节点，再将当前节点指针指向前驱，依次移动三者，最终前驱为新头。环检测：快慢指针同时从头出发，快指针每次走两步，慢指针一步，若相遇则有环。中间节点：快慢指针同起点，快指针到尾时，慢指针恰好到中间（偶数节点取左中），均需先判断头节点是否为null。
---
## Chunk 240 — 环检测中，快慢指针相遇后，如何找到环的入口节点？

环检测中，快慢指针相遇后，如何找到环的入口节点？

相遇后将慢指针重置为头节点，快慢指针改为每次都走一步，再次相遇的节点就是环入口。原理是相遇时快指针走的距离是慢指针的2 倍，通过距离公式可推导出头节点到入口的距离等于相遇点到入口的距离。  
3. 栈和队列 45. "栈和队列的定义及特点是什么？请用数组或链表实现一个栈和一个队列。" 栈是先进后出的线性结构，队列是先进先出的线性结构；数组实现栈高效，链表实现队列灵活，均需处理边界和操作逻辑。栈仅允许栈顶操作（push/pop），队列仅允许队尾入、队头出（enqueue/dequeue）。数组实现栈：用下标top 记录栈顶，push 时top++存值，pop 时返回top--对应值，满时扩容（如2 倍）。链表实现队列  
：设头尾指针，enqueue 时尾指针指向新节点，dequeue 时头指针后移，空时返回异常，无需考虑扩容。  
开发中我会按需选择，高频操作的用数组栈（如表达式计算），动态增删的用链表队列（如任务排队）；同时添加空判断，避免操作异常。
---
## Chunk 241 — 追问1：用两个栈如何实现一个队列？

追问1：用两个栈如何实现一个队列？

核心逻辑是什么？用“入栈”和“出栈”两个栈实现。enqueue 时直接压入入栈；dequeue 时若出栈为空，将入栈所有元素弹出并压入出栈（反转顺序），再从出栈弹出顶部元素，这样就模拟了队列的先进先出特性。  
4. 哈希表哈希表的实现原理是什么？如何解决哈希冲突？常见的哈希函数有哪些？  
哈希表通过“键-哈希值-地址”的映射快速存取数据。哈希表实现原理：用哈希函数将键转换为哈希值，通过取模等方式映射到数组下标（存储地址），实现O(1)的存取。  
冲突解决： 1. 链地址法：数组下标对应链表，冲突键存链表中 2. 开放定址法：冲突时按规则找下一个空地址（如线性探测）。常见哈希函数：直接定址法（键直接作地址）、除留余数法（键%素数）、折叠法（键分段相加）。  
设计哈希表时，我会选素数作为数组大小，用链地址法解决冲突（易实现），搭配除留余数法哈希函数，控制负载因子在0.7 以下减少冲突。
---
## Chunk 242 — 追问1：链地址法和开放定址法相比，各自的优缺点是什么？

追问1：链地址法和开放定址法相比，各自的优缺点是什么？
---
## Chunk 243 — 追问1：链地址法和开放定址法相比，各自的优缺点是什么？

什么场景下选开放定址法？链地址法优点是冲突处理简单、负载因子高时仍高效，缺点是需额外存储指针；开放定址法优点是内存连续、无指针开销，缺点是易产生聚集（如线性探测）、删除需标记。内存紧张且数据量不大时，选开放定址法更合适。  
5. 二叉树二叉树的前序、中序、后序遍历的递归和非递归实现方法是什么？三种遍历的核心是根节点访问时机不同，递归实现依赖递归栈，非递归需手动用栈管理节点，需明确入栈出栈逻辑和边界处理。递归实现：前序（根→左→右）、中序（左→根→右）、后序（左→右→根），均先判断节点是否为null，再按顺序递归左右子树。非递归：前序先压右子树再压左子树（栈先进后出），弹出即访问；中序先压左子树，左空后弹出访问根，再压右子树；后序用栈存节点和访问标记，未访问则标已访问并压右左子树，已访问则弹出。实现时我会先写递归（简洁易读），非递归用注释标注“压栈顺序原因”（如前序压右左是为了左先弹出）；同时处理空树，确保代码健壮。追问1：已知二叉树的前序和中序遍历结果，如何重建该二叉树？核心逻辑是什么？  
核心逻辑是前序首元素为根节点，中序中根节点左侧是左子树、右侧是右子树。通过前序确定根，中序划分左右子树范围，再递归重建左子树（前序左段+中序左段）和右子树（前序右段+中序右段），需处理空树和单节点情况。  
6. 二叉搜索树什么是二叉搜索树？它的查找、插入、删除操作的时间复杂度是多少？  
二叉搜索树是左子树节点值≤根≤右子树节点值的二叉树，中序遍历为升序；操作复杂度依赖树高，平衡时高效，失衡时性能下降。定义：左子树所有节点值不大于根，右子树所有节点值不小于根，且左右子树均为BST。操作：查找时按值与根比较，小则查左、大则查右。插入时类似查找，找到空位置插入。删除时，叶子节点直接删，单孩子节点用孩子替代，双孩子节点用中序后继（右子树最小）替代。平衡时时间复杂度O(logn)，失衡（如链状）时O(n)。  
开发中若用BST，我会关注树的平衡，避免插入有序数据导致失衡；若需稳定性能，会选择红黑树等平衡BST，确保操作复杂度稳定在O(logn)。
---
## Chunk 244 — 二叉搜索树中，“中序后继”指什么？

二叉搜索树中，“中序后继”指什么？

如何快速找到一个节点的中序后继？中序后继是中序遍历中该节点的下一个节点。查找方法：1. 若节点有右子树，后继是右子树的最左节点（右子树中最小节点）；2. 若无右子树，向上追溯祖先，找到第一个“该节点是其左子树”的祖先，该祖先即为后继，若无则无后继。  
7. 红黑树，AVL树红黑树的核心特性是什么？它与AVL 树的区别是什么？红黑树的插入和删除过程是怎样的？  
红黑树是通过颜色规则保证近似平衡的BST，核心特性约束树高，与AVL 树平衡标准不同；插入删除靠变色和旋转调整，旋转频率更低。核心特性：1. 节点非红即黑；2. 根和叶子（NIL）为黑；3. 红节点子节点为黑；4. 任意节点到叶子的黑节点数相同。与AVL 树区别：AVL 树按高度差（≤1）严格平衡，旋转多；红黑树按颜色规则近似平衡，旋转少。插入删除：先按BST 操作，再通过变色（优先）和旋转（左/右/双旋）修复颜色违规，维持特性。  
开发中我会根据场景选树，需要稳定查找性能的用AVL树，增删频繁的用红黑树（旋转少效率高）；理解其调整逻辑，避免使用时因特性破坏导致问题。
---
## Chunk 245 — 追问1：红黑树的“黑高”是什么？

追问1：红黑树的“黑高”是什么？

为什么说红黑树的高度不会超过2log₂(n+1)？黑高是节点到叶子节点的路径上黑色节点的数量（含自身）。根据特性，任意路径的黑高相同，且红色节点不相邻，最长路径（红黑交替）的长度不会超过最短路径（全黑）的2 倍，而最短路径长度为黑高h，故树高≤2h，结合节点数与黑高的关系可推导出高度上限。  
8. B树和B+树 B 树和B+树的结构及特点是什么？为什么数据库索引通常使用B+树？ B 树和B+树都是多叉平衡树，核心区别在数据存储位置和叶子节点特性；B+树因适配磁盘IO 和范围查询，成为数据库索引的首选。结构特点：m 阶B 树每个节点最多m 个子节点、存m-1个数据，非叶子和叶子都存数据；m 阶B+树非叶子仅存索引（指引子节点），叶子节点存全部数据且按顺序双向连接（叶子结点之间是双向链表）。数据库选型原因：1. 树高矮（多叉），减少磁盘IO（一次读一个节点）；2. 叶子有序连接，范围查询（如between）无需回溯；3. 索引与数据分离，查询更高效。  
设计数据存储系统时，我会借鉴B+树思想，比如日志索引用B+树结构，通过有序叶子节点优化范围查询；同时控制节点大小匹配磁盘页，减少IO 开销。  
B 树和B+树在单值查询时性能差异不大，为什么范围查询B+树更有优势？ B 树范围查询时，找到起始数据后，需回溯父节点找下一个数据的位置（因非叶子节点存数据，叶子节点无序）；而B+树叶子节点按顺序双向连接，找到起始数据后，直接沿叶子节点链表依次遍历即可获取所有范围内数据，无需回溯，效率显著更高。  
9. 各种排序算法（冒泡，选择，插入，快排，归并，堆排） 1. 交换类：冒泡（时间O(n²)/O(n)，空间O(1)，稳定），相邻比较，大的往后“冒”（swap）快排（O(nlogn)/O(n²)，O(logn)，不稳定）
---
## Chunk 246 — 追问1：红黑树的“黑高”是什么？ > 2. 插入类：

追问1：红黑树的“黑高”是什么？ > 2. 插入类：

插入（O(n²)/O(n)，O(1)，稳定）。维护一个“已排序区间”（左边），每次取一个新元素，向前
---
## Chunk 247 — 追问1：红黑树的“黑高”是什么？ > 3. 选择类：

追问1：红黑树的“黑高”是什么？ > 3. 选择类：

选择（O(n²)，O(1)，不稳定）。每一轮：在未排序区间找最小值，然后和当前起点交换堆排（O(nlogn)，O(1)，不稳定）。先建一个大顶堆(O(n))，然后把堆顶（最大值）和最后一  
个元素交换，再对根节点重新 heapify（下沉），下沉n次每次logn，所以一共是O(nlogn) 4. 归并（O(nlogn)，O(n)，稳定）  
开发中我会按数据场景选型，小数据用插入排序（简单高效），大数据用快排（平均性能好），需稳定排序的用归并排序；避免在大数据场景用冒泡等低效算法。
---
## Chunk 248 — 追问1：为什么快排的平均时间复杂度是O(nlogn)，但最坏会退化到O(n²)？

追问1：为什么快排的平均时间复杂度是O(nlogn)，但最坏会退化到O(n²)？

如何避免这种退化？快排通过基准值划分区间，平均每次将数组分为两等份，递归深度O(logn)，每层操作O(n)，故平均O(nlogn)；若基准值选极值（如有序数组选首元素），划分后区间为1 和n-1，递归深度O(n)，退化到O(n²)。避免方法：随机基准值，减少极值选择概率。  
10. 实现快排，解释优化思路快排核心是“基准划分+递归排序”，通过优化基准值和处理重复元素提升性能，实现时需明确划分逻辑和递归边界。 1. 递归边界：若low≥high 直接返回；2.选基准值（如三数取中法：取low、mid、high 对应值的中值，交换到low 位置）；3. 双路划分：左指针找比基准大的，右指针找比基准小的，交换后继续，直到指针相遇，将基准值放到分界处；4. 递归排序左右区间。优化：重复元素用三路快排（分小于、等于、大于三区），避免重复元素聚集；递归深度大时改用堆排。
---
## Chunk 249 — 追问1：三路快排的核心思想是什么？

追问1：三路快排的核心思想是什么？
---
## Chunk 250 — 追问1：三路快排的核心思想是什么？

相比双路快排，它在处理重复元素时有什么优势？三路快排将数组分为“小于基准”“等于基准”“大于基准”三个区间，核心是用两个指针lt 和gt 分别标记小于区的尾和大于区的头，遍历数组时将元素归到对应区间。优势：重复元素集中在“等于区”，无需参与后续递归排序，减少递归处理的数据量，避免双路快排中重复元素分散导致的多次划分，提升性能。  
11. 动态规划动态规划是通过存储子问题最优解解决复杂问题的方法，核心是利用重叠子问题和最优子结构； LIS 问题可用DP 高效求解，分基础和优化解法。  
DP 定义：将问题拆为重叠子问题，存储子问题最优解（避免重复计算），通过最优子结构推导全局最优。LIS 解法：1. 基础O(n²)：状态dp[i]为以i 结尾的LIS 长度，转移方程dp[i] = max(dp[j]+1)（j<i 且nums[j]<nums[i]），初始化dp[i]=1，结果取max(dp)；2. 优化O(nlogn)：用数组tails 存LIS，遍历nums 时二分找插入位置，tails 长度即LIS 长度。解决DP 问题时，我会先明确状态定义（如LIS 的dp[i]含义），再推导转移方程；复杂问题先写基础解法，再结合场景优化时间空间，提升效率。  
追问1：0-1 背包问题和完全背包问题的核心区别是什么？它们的动态规划转移方程有何不同？核心区别是物品是否可重复选取：0-1 背包物品仅选一次，完全背包物品可选多次。0-1 背包转移方程：dp[j] = max(dp[j], dp[j-weight[i]]+value[i])，遍历背包容量需从大到小（避免重复选）；完全背包转移方程相同，但容量从左到右遍历（允许重复选）。
---
## Chunk 251 — 追问1：三路快排的核心思想是什么？

12. 贪心算法、它与动态规划的区别贪心算法是每次选局部最优解以推导全局最优的方法，需满足贪心选择性质；它与动态规划的核心区别在子问题处理和适用前提。定义：贪心需满足“贪心选择性质”（局部最优可导出全局最优）和最优子结构。与DP 区别：1. 子问题：DP 处理所有重叠子问题，贪心仅选当前子问题最优，不回溯；2. 前提：DP 无特殊前提，贪心需满足贪心选择性质；3. 效率：贪心更高（O(n)或O(nlogn)），DP 相对低。应用场景：活动选择（选最多不重叠活动）、哈夫曼编码（最优前缀码）、零钱兑换（面额满足贪心条件时）。  
开发中我会先判断问题是否满足贪心条件，如活动排期用贪心（选结束早的）；不满足时用DP（如普通零钱兑换），避免因误用贪心导致结果错误。
---
## Chunk 252 — 为什么“活动选择问题”能用贪心算法解决，而“旅行商问题”不能？

为什么“活动选择问题”能用贪心算法解决，而“旅行商问题”不能？
---
## Chunk 253 — 为什么“活动选择问题”能用贪心算法解决，而“旅行商问题”不能？

核心原因是什么？参考回答：面试官您好，活动选择问题满足贪心选择性质：选当前结束最早的活动，剩余时间最多，可容纳更多活动，局部最优能导出全局最优。旅行商问题（找经过所有城市的最短回路）不满足该性质：当前选最近的下一个城市，可能导致后续路线极长，局部最优无法导出全局最优，故需用动态规划或其他算法，不能用贪心。  
13. BFS与DFS DFS 和BFS 是图遍历的基础算法，DFS 用栈或递归实现深度优先，BFS 用队列实现广度优先，均需通过访问标记避免重复访问。DFS 优先访问当前节点的邻接节点，直到无未访问邻接节点再回溯。BFS 按“层”遍历，先访问当前节点的所有邻接节点，再依次访问邻接节点的邻接节点，用队列实现。实现关键：用数组visited 标记访问状态（true 为已访问），基于邻接表遍历（如节点u 的邻接表是所有相连节点v）。开发中我会按需选择，找路径是否存在用DFS（递归简洁），找最短路径（无权图）用BFS；实现时先初始化访问标记，避免因未标记导致死循环。  
追问1：在无向图中，如何用DFS 判断图中是否存在环？核心逻辑是什么？核心逻辑是追踪“父节点”，避免将回边误认为环。DFS 遍历中，对当前节点u 的邻接节点v：1. 若v 未访问，标记v 的父节点为u，递归遍历v；2. 若v 已访问且v 不是u 的父节点，说明存在环（u-v 是回边，形成环）。遍历结束未发现则无环。  
14. Dijkstra算法，Flyod算法什么是迪杰斯特拉算法和弗洛伊德算法？它们分别用于解决什么问题？时间复杂度是多少？  
迪杰斯特拉解决单源最短路径（从一个起点到所有节点），弗洛伊德解决多源最短路径（所有节点对之间），两者时间复杂度和适用场景不同。迪杰斯特拉：核心是“选未确定最短路径的节点中距离最小的，松弛其邻接边”，用邻接矩阵时间 O(n²)，邻接表+优先队列O(mlogn)，不能处理负权边（会导致松弛错误）。弗洛伊德：核心是“动态规划，通过中间节点k 更新i 到j 的最短路径”，时间O(n³)，可处理负权边（不能有负权环），实现简洁。
---
## Chunk 254 — 为什么“活动选择问题”能用贪心算法解决，而“旅行商问题”不能？

开发中我会按场景选型，单源且无负权用迪杰斯特拉（邻接表+优先队列高效），多源或有负权用弗洛伊德；避免在负权边场景用迪杰斯特拉导致结果错误。
---
## Chunk 255 — 为什么迪杰斯特拉算法不能处理含负权边的图？

为什么迪杰斯特拉算法不能处理含负权边的图？

如何修改算法使其能处理负权边？迪杰斯特拉算法假设“已确定最短路径的节点不会再被松弛”，但负权边会打破该假设（如已确定的节点u，其邻接边有负权，后续节点v 的更短路径可能通过u）。修改方法用贝尔曼-福特算法，通过n-1 次松弛所有边，可处理负权边；或用SPFA 算法（贝尔曼-福特的队列优化）提升效率。  
15. Top K问题在海量数据处理场景中，如何利用哈希分治、堆排序等思想解决“Top K”问题？  
海量数据Top K 问题无法一次性加载内存，需用哈希分治拆分数据，结合堆排序筛选局部和全局 Top K，核心是“分而治之+高效筛选”。解决步骤：1. 哈希分治：用哈希函数（如取模）将海量数据均匀分片到多个小文件（如1000 个），确保相同数据在同一文件，单个文件可加载内存；2. 局部Top K：对每个小文件，用小根堆（容量K）筛选TopK（遍历数据，比堆顶大则替换堆顶并调整）；3. 全局Top K：收集所有小文件的Top K，用小根堆再次筛选，最终堆内元素即为全局Top K。  
处理时我会优化哈希函数（选素数模）避免数据倾斜，若某文件仍过大则二次分片；用小根堆而非大根堆（减少调整次数），提升筛选效率。
---
## Chunk 256 — 如果海量数据中存在大量重复元素，如何优化上述方案进一步提升效率？

如果海量数据中存在大量重复元素，如何优化上述方案进一步提升效率？

可在哈希分治后增加“计数”步骤：对每个小文件，先用哈希表统计元素出现次数（键为元素，值为次数），再基于次数筛选Top K（此时比较的是次数而非元素本身）。这样避免重复遍历相同元素，减少堆调整次数；同时计数后数据量更小，进一步提升内存利用率和处理速度。
---
## Chunk 257 — 四、数据库

四、数据库

1. MySQL的索引类型（B+树）索引 = 快速定位数据的有序结构，默认基于B+树实现主键索引：唯一、非空、聚簇索引二级索引：非主键字段的索引，用非主键字段找到主键，再用主键索引找整行数据（回表）联合索引：多字段组合建索引，遵循最左前缀。最左前缀原则指联合索引（a,b,c）仅对“a”，“a,b”， “a,b,c”的查询条件生效，不满足则索引失效（如“b”“b,c”查询）。若查询条件含最左前缀但中间字段缺失（如“a,c”），仅a 字段索引生效，c字段需全表扫描。 B+树非叶子仅存索引（指引子节点），叶子节点存全部数据且按顺序双向连接（叶子结点之间是双向链表）。数据库选型原因：1. 树高矮（多叉），减少磁盘IO（一次读一个节点）；2. 叶子有序连接，范围查询（如between）无需回溯；3. 索引与数据分离，查询更高效。
---
## Chunk 258 — 四、数据库 > 2. 索引失效索引失效 = MySQL 没用索引，而是走了全表扫描

四、数据库 > 2. 索引失效索引失效 = MySQL 没用索引，而是走了全表扫描

SQL SELECT * FROM user WHERE name = 'Alice'; --索引  
SELECT * FROM user WHERE name LIKE '%Alice'; --全表扫描  
1. 函数操作索引字段（如where DATE(create_time)='2024'） 2. 隐式类型转换（字符串索引配数字值） 3. like%前缀（如like '%name'） 4. or 连接未索引字段 5. 联合索引不满足最左前缀避免方法：避免索引字段函数操作、显式类型转换、用like xxx%或覆盖索引、避免OR，用UNION 建立索引、按最左前缀设计查询。  
3. MySQL 的事务隔离级别事务隔离 = 多个事务同时操作数据库时，如何避免互相干扰三个经典并发问题  
1. 脏读 (Dirty Read)：读到了别人还没提交的数据 2. 不可重复读 (Non-Repeatable Read)：同一个事务里，两次读同一条数据，结果不同 3. 幻读 (Phantom Read)：同一个事务里，两次查询“行数”不同
---
## Chunk 259 — 四种隔离级别（从低到高）

四种隔离级别（从低到高）

1. 读未提交 (Read Uncommitted, RU) 可以读未提交数据，存在脏读/不可重复读/幻读 2. 读已提交 (Read Committed, RC) 只能读已提交数据，解决脏读 3. 可重复读（RR）：同一事务内读取结果一致，解决前两者，允许并发，性能高 a. MVCC 多版本并发控制，每个事物看到的是一个历史快照，就算别人改了数据看
---
## Chunk 260 — 到的还是旧版本

到的还是旧版本

b. Next-Key Lock 间隙锁+行锁，防止别人插入新数据 4. 串行化 (Serializable)：事务一个个执行，解决所有问题，性能低。  
事务隔离级别用于控制多个事务并发执行时彼此可见的数据范围，从而避免并发问题。常见并发问题包括：脏读，即读到其他事务未提交的数据；不可重复读，即同一事务中两次读取同一行结果不同；幻读，即同一事务中两次范围查询得到的记录数不同。  
MySQL 常见的四种隔离级别从低到高依次是：Read Uncommitted、Read Committed、 Repeatable Read 和 Serializable。RU 允许读取未提交数据，三种问题都可能发生；RC 只能读已提交数据，解决脏读；RR 在 MySQL InnoDB 中是默认级别，利用 MVCC 保证快照读一致，并结合 Next-Key Lock 在当前读场景下避免幻读；Serializable 则通过事务一个个执行解决所有并发问题，但性能最差。  
其中 MVCC 的核心思想是为数据保留多个版本，让事务读取自己开始时可见的快照版本； Next-Key Lock 是行锁和间隙锁的组合，用来防止其他事务在查询范围内插入新记录。
---
## Chunk 261 — 到的还是旧版本 > 4. MySQL的锁按粒度分

到的还是旧版本 > 4. MySQL的锁按粒度分

表锁：锁整张表，实现简单，并发差  
● 行锁：锁某一行，并发高，更精细。InnoDB 的行锁是基于索引实现的。如果没有索引， MySQL不知道哪一行是target，因此需要一行行扫描+一行行加锁，结果等于把表锁
---
## Chunk 262 — 按模式分

按模式分

共享锁 (S锁 Shared lock)：读锁，多个事务可以同时加，只能读，不能写 ● 排他锁 (X锁 exclusive lock)：写锁，只能一个事务持有，其他全部阻塞。SELECT... FOR UPDATE 会将查询从快照读转为当前读，并对命中的记录加排他锁（X锁）  
5. MVCC（多版本并发控制）机制 MVCC 是InnoDB 实现非阻塞读的核心机制。通过数据的多个版本，让读操作不加锁也能保证一致性。实现原理  
1. 每行数据含事务ID（DB_TRX_ID）和回滚指针（DB_ROLL_PTR） 2. 数据修改时，旧版本写入undo 日志，形成版本链 3. 事务开启时生成Read View，通过事务ID 判断版本链中数据是否可见（仅读已提交或未开始的事务数据）  
作用：实现快照读，读写不冲突，提升并发性能。
---
## Chunk 263 — 按模式分 > 15. NoSQL 数据库与关系型数据库的区别

按模式分 > 15. NoSQL 数据库与关系型数据库的区别
---
## Chunk 264 — 按模式分 > 15. NoSQL 数据库与关系型数据库的区别

NoSQL 和关系型数据库的主要区别在数据模型、事务支持和扩展方式。关系型数据库采用表结构，具有严格的 schema，并支持 ACID 事务（原子性，一致性，隔离性，持久性），适合强一致性和复杂查询场景；而 NoSQL 数据库通常是无固定 schema 的，支持非结构化或半结构化数据，强调高并发和可扩展性。  
在扩展方面，关系型数据库主要依赖垂直扩展，而 NoSQL 更适合水平扩展。根据数据模型的不同，NoSQL 可以分为键值型（如 Redis）、文档型（如 MongoDB）、列族型（如 HBase）和图数据库（如 Neo4j），分别适用于缓存、内容存储、大数据和关系分析等场景。  
7. SQL 语句的优化方法 SQL 优化 = 减少扫描数据量+减少 IO 次数 1. 索引优化：select from order where user_id=100 优化为给user_id 建索引。合理设计索引，例如对高频查询字段建立索引，避免全表扫描。同时可以利用联合索引减少回表次数，甚至通过覆盖索引直接在索引中完成查询。 2. 避免索引失效：在 SQL 编写时需要避免索引失效，例如不要对索引字段进行函数操作，不要发生隐式类型转换，避免 LIKE 以% 开头，以及遵循联合索引的最左前缀原则。 select from user where DATE(create_time)='2024' 优化为 select from user where create_time between '2024-01-01' and '2024-01-02' 3. 限制返回字段：select * 改为 select id,name，减少数据传输 4. 用explain 分析执行计划，重点关注是否走索引（type 是否为 index 或 range），定位全表扫描（type=ALL）为什么索引能优化性能？索引可以将全表扫描转化为基于 B+树的快速定位，从 O(n) 降低到 O(log n)。
---
## Chunk 265 — 按模式分 > 15. NoSQL 数据库与关系型数据库的区别

14. Redis的主从复制、哨兵模式、集群模式集群模式如何实现数据分片和高可用？主从复制实现读写分离。哨兵模式保障高可用，集群模式兼具分片和高可用；集群通过槽位分片和主从复制，支撑大规模数据和高并发场景。主从复制：一个主库写、多个从库读，提升读性能，但是主库挂了无人接替哨兵模式：基于主从，监控主从状态，自动切换主库，实现高可用集群模式：多个主库和从库，数据分片每个主库存一部分数据有自己的从库。高可用：集群主库挂了，从库自动晋升为主库。  
8. MySQL 的主从复制机制 MySQL 主从复制 = 主库把所有写操作记录到 binlog（操作日志），从库把这些操作重新执行一遍，解决单机数据库在性能（CPU/IO/连接数有限）、可用性和扩展性方面的瓶颈，通过读写分离提升读性能（主写，从读），通过多副本实现容灾（主库挂了从库可以顶上）和高可用。流程  
1. 主库修改数据+把这条操作写入binlog 2. 从库启动一个IO Thread连接主库，持续读取binlog写到本地 3. 从库SQL Thread读取relay log，执行里面的SQL，使从库数据=主库数据  
复制类型  
1. 异步复制（默认）：主库写完就返回不管从库，因此主库挂了 → 数据可能还没同步到从库，可能导致数据丢失  
2. 半同步复制 (Semi-sync)：主库至少等一个从库确认，减少数据丢失但写入变慢
---
## Chunk 266 — 常见问题

常见问题

1. 主从延迟：主库写得快，从库执行慢，本质是单线程执行+IO/CPU瓶颈。可以通过并行复制、提升从库配置和减少大事务解决  
2. 数据不一致：网络中断，binlog格式问题。可以使用ROW binlog和定期校验解决 3. 主从切换：主库挂了。可以通过MHAMGR等自动选主+切换解决  
9. 数据库的分库分表分库分表 = 把一个大数据库/大表拆成多个小的，来提升性能和扩展性水平分库分表：按行拆分（如按用户ID取模），数据量过大时用（如订单表）垂直分库分表：按列拆分（如拆分大字段到附表），字段过多或读写分离时用（如用户表拆分基本信息和详情追问
---
## Chunk 267 — 常见问题 > 五、Redis

常见问题 > 五、Redis

1. Redis，Redis为什么快 Redis 是一个基于内存的高性能key -value数据库。Redis在系统中主要作为缓存层，通过减少数据库访问来提升系统性能，同时需要配合合理的缓存策略来解决一致性和缓存失效问题。 Redis快主要有四个原因：
---
## Chunk 268 — 常见问题 > 1. 基于内存存储

常见问题 > 1. 基于内存存储

避免磁盘IO，访问延迟极低，MySQL 数据在磁盘 (Disk)，访问磁盘IO慢。
---
## Chunk 269 — 一个线程可以同时处理大量连接，提高并发能力

一个线程可以同时处理大量连接，提高并发能力

2. 缓存三大问题（穿透/击穿/雪崩） 1. 缓存穿透: 查不存在数据 → 打数据库解决：布隆过滤器，空值缓存
---
## Chunk 270 — 一个线程可以同时处理大量连接，提高并发能力 > 3. 缓存雪崩：大量key同时过期解决：TTL随机，多级缓存

一个线程可以同时处理大量连接，提高并发能力 > 3. 缓存雪崩：大量key同时过期解决：TTL随机，多级缓存

3. Redis 的数据结构 String：二进制安全，存字符串/数字，适用于缓存用户ID、计数器 Hash：键值对集合，存对象（如用户信息），支持字段级操作 List：有序链表，适用于消息队列、最新列表 Set：无序去重，适用于好友关系、标签去重 Sorted Set：分数排序，适用于排行榜、带权重的任务队列。  
4. Pawse怎么用Redis进行优化 Feed流缓存，用户信息缓存，点赞计数器，排行榜。（需要细化）
---
## Chunk 271 — 为什么不用Redis直接存？

为什么不用Redis直接存？

1. Redis在内存 → 不适合持久存储 2. MySQL保证ACID 3. Redis适合缓存  
6. Redis一致性问题先更新DB，再删缓存（常用），延迟双删。
---
## Chunk 272 — 为什么不用Redis直接存？ > 7. Redis 的持久化机制

为什么不用Redis直接存？ > 7. Redis 的持久化机制

Redis 的持久化机制主要包括 RDB 和 AOF。RDB 通过在某一时刻生成内存数据的快照来实现持久化，优点是文件小、恢复快，但可能丢失最近一段时间的数据。AOF 则通过记录每一次写操作来保证数据安全，支持不同的写入策略，默认每秒同步一次，在性能和安全之间取得平衡。  
随着写操作增加，AOF 文件会变大，因此 Redis 提供 AOF 重写机制，将多次操作合并为最终状态，从而减小文件体积并提升恢复效率。在实际生产中，通常会同时开启 RDB 和 AOF，以兼顾恢复速度和数据安全性  
8. Redis 的过期键删除策略 Redis 对过期键采用惰性删除和定期删除相结合的策略。惰性删除在访问键时检查是否过期，降低 CPU 开销；定期删除通过周期性随机扫描部分键，避免过期键长期占用内存。当内存不足时， Redis 会触发内存淘汰机制，根据配置的策略（如 allkeys-lru、volatile-lru 等）删除部分键以释放空间。LRU 在 Redis 中采用近似实现，通过随机采样方式选择最久未使用的键，从而在性能和准确性之间取得平衡。 LRU，LFU。
---
## Chunk 273 — 六、分布式系统与高可用

六、分布式系统与高可用
---
## Chunk 274 — 六、分布式系统与高可用

1. 分布式系统的CAP理论分布式系统的CAP理论是什么？BASE 理论与CAP理论的关系是什么？ CAP 理论指出分布式系统无法同时满足强一致性、高可用性和分区容错性，P 是必选故需权衡 CP 或AP；BASE 理论是CAP的妥协，追求最终一致性，适配高可用场景。 CAP 定义：Consistency（强一致性，数据实时同步）、Availability（高可用，服务持续响应）、 Partition Tolerance（分区容错，网络分区时系统可用）。关系：BASE（Basically Available、Soft state、Eventually consistent）基于AP 扩展，允许短期不一致，通过异步同步实现最终一致，是分布式系统的实际选择（如电商订单系统）。  
设计分布式系统时，我会按业务需求权衡：支付等强一致场景选CP（如ZooKeeper），电商等高可用场景选AP+BASE（如Redis 集群），平衡一致性和可用性。  
追问1：电商系统的订单支付场景，为什么通常选择AP+BASE 而非CP？请举例说明。  
电商订单支付需优先保障高可用（用户能正常下单支付），而非强一致性。例如用户下单后，库存异步扣减，短时间内可能存在“下单成功但库存未更新”的软状态，但通过定时对账最终实现一致，既保障了系统可用性，又避免了因强一致导致的服务不可用。  
2. 分布式一致性算法（如axos、Raft 等）请简述Raft 算法的核心流程（领导者选举、日志复制）  
分布式一致性算法有Paxos、Raft 等，Raft因流程清晰成为主流；其核心是领导者选举和日志复制，通过任期机制和多数确认保障一致性，易工程实现。核心流程：1. 领导者选举：节点初始为追随者，任期超时转为候选人，向其他节点请求投票，得多数票者当选领导者，任期号递增防止脑裂；2. 日志复制：领导者接收客户端请求，追加日志条目，同步给所有追随者，收到多数追随者确认后，提交日志并返回结果给客户端。安全性：领导者仅提交自己任期内的日志，确保所有节点日志一致。
---
## Chunk 275 — 六、分布式系统与高可用

设计分布式系统（如配置中心、分布式锁）时，我会优先选择基于Raft 的组件（如Etcd、Nacos），利用其成熟的一致性保障，避免重复实现复杂算法，提升系统可靠性。
---
## Chunk 276 — 追问1：Raft 算法中，“任期”的作用是什么？

追问1：Raft 算法中，“任期”的作用是什么？

如果出现多个领导者（脑裂），会如何处理？任期的作用是标识领导者的合法性，任期号递增，  
新任期的领导者优先级高于旧任期。若出现脑裂，新任期的领导者会通过日志复制机制覆盖旧任期领导者的未提交日志，同时其他节点发现更高任期的领导者后，会转为追随者，最终恢复单一领导者，保障日志一致性。  
3. 分布式锁实现分布式锁的常见方式有哪些？（如基于Redis、ZooKeeper 等）它们的优缺点是什么？  
分布式锁用于跨服务器同步共享资源访问，常见实现有Redis 和ZooKeeper；Redis 锁性能优， ZooKeeper 锁可靠性高，需按业务场景权衡选择。  
实现及优缺点： 1. Redis 锁：用set key value nx ex命令（原子操作），优点是性能高、实现简单，缺点是可能因过期时间设置不合理导致死锁，需配合看门狗机制； 2. ZooKeeper 锁：创建临时有序节点，监听前序节点，优点是自动释放锁（会话超时）、无死锁风险，缺点是性能略低、依赖ZooKeeper 集群。适用场景：高性能场景用Redis 锁，高一致性场景用 ZooKeeper锁。开发中我会按场景选型，如秒杀系统用Redis 锁提升并发，分布式事务场景用ZooKeeper 锁保障一致性；Redis 锁会设置合理过期时间并加看门狗，避免死锁。
---
## Chunk 277 — 追问1：Redis 分布式锁中，“看门狗机制”的作用是什么？

追问1：Redis 分布式锁中，“看门狗机制”的作用是什么？
---
## Chunk 278 — 追问1：Redis 分布式锁中，“看门狗机制”的作用是什么？

如何实现？  
看门狗机制用于解决Redis 锁过期时间过短导致的锁提前释放问题。实现：加锁成功后，启动后台线程，每隔一段时间（如过期时间的1/3）检查锁是否仍持有，若持有则延长过期时间，确保业务执行完前锁不释放，避免并发安全问题。  
4. 负载均衡负载均衡的原理是什么？常见的负载均衡算法有哪些？（如轮询、加权轮询、最少连接数等）负载均衡通过合理分发请求避免单点过载，提升系统可用性和吞吐量；常见算法按“公平性、资源利用率”设计，需结合业务场景选择。原理：接收客户端请求，按预设算法分发到后端服务器集群，避免单台服务器负载过高。常见算法：1. 轮询：请求依次分发，适用于服务器配置一致的场景；2. 加权轮询：按服务器权重分配（如性能高的权重高），适配服务器配置差异；3. 最少连接数：分发到当前连接数最少的服务器，适用于动态请求（如接口调用）；4. IP 哈希：按客户端IP 哈希固定分发，实现会话保持。设计系统时，我会按场景选型，静态资源服务用轮询，异构服务器集群用加权轮询，需会话保持的场景用IP 哈希；同时监控服务器负载，动态调整算法参数。  
追问1：“IP 哈希算法”实现会话保持有什么局限性？如何解决？局限性：1. 客户端IP 变化（如切换网络）会导致会话丢失；2. 部分客户端共用IP（如局域网）会导致负载不均。解决方法：1.用Cookie 或Token 存储会话信息，替代IP 绑定；2. 结合一致性哈希算法，即使IP 变化也能映射到相近服务器，减少会话丢失概率。  
5. 熔断、降级、限流熔断、降级、限流是分布式系统的“防护三剑客”，分别应对服务故障、资源紧张和流量峰值，核心是保障核心业务可用，避免级联故障。
---
## Chunk 279 — 追问1：Redis 分布式锁中，“看门狗机制”的作用是什么？

5. 熔断、降级、限流熔断、降级、限流是分布式系统的“防护三剑客”，分别应对服务故障、资源紧张和流量峰值，核心是保障核心业务可用，避免级联故障。  
定义、作用及实现：1. 熔断：服务调用失败率达阈值时触发（如Sentinel 的Circuit Breaker），暂时断连避免雪崩，故障恢复后闭合，实现方式有熔断器模式；2. 降级：资源紧张时关闭非核心功能（如电商大促关闭评价功能），实现方式有开关控制、动态配置；3. 限流：限制单位时间请求数（如令牌桶算法），保护后端服务，实现组件有Sentinel、GuavaRateLimiter。  
开发中我会用Sentinel 统一实现三者，核心接口配置限流（令牌桶算法），依赖服务配置熔断（失败率阈值50%），大促时通过动态开关降级非核心功能，保障核心业务稳定。  
追问1：限流的“令牌桶算法”和“漏桶算法”有何区别？分别适用于什么场景？令牌桶算法：按固定速率生成令牌，请求需获取令牌才能执行，支持突发流量（令牌积累），适用于允许短期高并发的场景（如秒杀）；漏桶算法：请求按固定速率处理，超出容量则丢弃，强制平滑流量，适用于需严格控制QPS 的场景（如数据库访问）。
---
## Chunk 280 — 追问1：Redis 分布式锁中，“看门狗机制”的作用是什么？ > 八、工程实践与开发效率

追问1：Redis 分布式锁中，“看门狗机制”的作用是什么？ > 八、工程实践与开发效率

1. 敏捷开发敏捷开发是迭代式开发理念，核心是快速响应变化、持续交付价值；Scrum 是敏捷的主流框架，通过明确角色、事件和交付物保障团队高效协作。  
产品负责人（PO）：梳理需求、维护产品待办列表 ● Scrum 大师（SM）：保障Scrum 流程落地，移除团队障碍. ● 开发团队：自组织完成冲刺任务 ● 冲刺 (Sprint) 是Scrum 的核心迭代周期，在固定时间内（通常2-4 周）团队交付一个可运行的产品增量。  
2. 代码评审代码评审的核心是保障代码质量、统一团队规范、促进知识共享，而非单纯找bug；评审需聚焦逻辑、性能等关键维度，通过建设性反馈提升团队代码水平。核心目的  
避免流于形式： ● 明确评审标准（如“高风险模块必须评审”） ● 限制评审代码量（单次不超过400 行） ● 要求评审人给出具体反馈而非“通过”  
提高效率用自动化工具（如SonarQube）检查格式、简单bug 评审前作者说明核心逻辑聚焦高风险模块（如支付、权限相关代码）
---
## Chunk 281 — 追问1：Redis 分布式锁中，“看门狗机制”的作用是什么？ > 3. CI/CD

追问1：Redis 分布式锁中，“看门狗机制”的作用是什么？ > 3. CI/CD

CI 是持续集成 (Integration) 代码频繁合并并自动化构建测试，CD (Deployment) 是持续交付或持续部署；完整流程需工具链支撑，核心是自动化与快速反馈。流程  
1. 开发者通过Git 提交代码到仓库 2. GitLab CI/Jenkins 触发自动化构建（如编译、打包） 3. 执行自动化测试（单元测试、集成测试） 4. 测试通过后，持续交付需手动批准部署，持续部署自动部署到生产/测试环境
---
## Chunk 282 — 工具作用

工具作用

Git（代码管理） ● Jenkins/GitLab CI（构建与流程编排） ● JUnit（单元测试） ● Docker（打包）。  
4. 如何保证代码质量保证代码质量通常需要从多个环节入手。首先是编码规范，保证代码风格统一、可读性强；其次是静态代码分析，在代码运行前发现潜在 bug、规范问题和安全风险；然后是代码评审，通过人工 review 检查业务逻辑、设计合理性和性能问题；最后是自动化测试，包括单元测试和集成测试，验证功能正确性。  
5. 单元测试、集成测试、系统测试三类测试按粒度从细到粗：单元测试测单个组件，集成测试测模块交互，系统测试测整体功能  
单元测试：测试单个函数/类（如接口逻辑），隔离外部依赖（用Mock 替代DB、网络），目的验证逻辑正确性  
Mock外部依赖 ○ 聚焦核心逻辑（如异常处理、边界条件） ○ 保持独立性（测试用例互不依赖） ○ 高覆盖率（重点覆盖核心路径）  
集成测试：测试模块间交互（如服务A 调用服务B），验证接口兼容性 ● 系统测试：测试整个系统，模拟真实用户场景，验证功能完整性  
AI相关  
Spec coding与vibe coding  
我理解 vibe coding 更偏快速试错，是基于比较模糊的需求让 AI 直接生成代码；而 spec coding 是基于明确的接口、数据结构和规范，让 AI 在这些约束下生成代码，更偏工程化。  
vibe coding 的优点是速度快，适合原型和探索，但代码质量和一致性比较难保证；spec coding 虽然前期需要定义 spec，但结果更稳定，更适合真实项目。  
在我的项目里，其实更偏 spec coding，比如我会通过 MCP 把设计稿和代码规范接入到 AI 的上下文中，让它基于结构化信息生成代码，而不是完全依赖 prompt。  
所以我一般会在探索阶段用 vibe coding，在正式开发中更倾向 spec coding。
---
## Chunk 283 — Menu里怎么用到了MCP

Menu里怎么用到了MCP

在 Menu 项目里，我把 MCP 接进了 Cursor 的 AI 辅助开发流程，这样能够“让 AI 能拿到更真实的项目上下文”。  
比如以前如果要让 AI 按设计稿写页面，或者按现有接口风格生成代码，往往需要手动复制很多设计稿信息、规范或者已有代码，而且这些内容很容易过时。接入 MCP 之后，像 Figma 这类外部资源可以通过标准方式暴露给模型，模型能按需读取设计稿节点或相关上下文，而不是完全依赖我手动复制粘贴。  
我负责的部分主要是开发环境里的集成和鉴权，比如配置 Figma/GitHub 相关 server、处理 API key 和环境变量，让这些资源能在 Cursor 里被模型稳定调用。最终效果是减少了 AI 生成代码和设计稿、接口命名不一致带来的返工。  
怎么看待AI coding  
我觉得 AI coding 的关键不只是“用不用”，而是“怎么把它接入工程体系”。  
比如在 Menu 项目里，我做了一些 MCP 集成，把设计稿、代码规范和部分外部信息变成模型可以按需访问的资源，而不是每次手动复制粘贴上下文。  
这样 AI 生成代码时不只是基于 prompt，而是基于更稳定的项目上下文，从而减少返工。  
但即便这样，我还是会把 AI 当作辅助工具，核心逻辑和架构决策仍然由工程师来控制。
---
## Chunk 284 — Menu里怎么用到了MCP > 1. System prompt

Menu里怎么用到了MCP > 1. System prompt

System prompt 就是给大模型设定的“最高级别说明书”。
---
## Chunk 285 — 它规定模型的角色规定模型的任务范围规定模型的回答风格规定模型的行为边界

它规定模型的角色规定模型的任务范围规定模型的回答风格规定模型的行为边界

它不是给用户看的，而是你作为开发者写给模型的“后台规则”。
---
## Chunk 286 — 理论上是什么

理论上是什么

Tool calling 的本质是：  
模型先判断“我该做什么动作”，然后调用外部函数/工具拿数据，再基于工具结果回答。
---
## Chunk 287 — 它解决的问题是：

它解决的问题是：

大模型本身不会真的查数据库，也不会真的知道你网站里的产品表、订单表、兼容性表。它只是会“生成文字”。
---
## Chunk 288 — 所以你需要给它“手和脚”：

所以你需要给它“手和脚”：

查 part 信息的工具查 compatibility 的工具查 order 的工具查 install guide 的工具  
模型负责“决定该用哪个工具”，工具负责“拿到真实数据”。
---
## Chunk 289 — 比如用户问：

比如用户问：

Is this part compatible with my WDT780SAEM1 model?  
如果没有 tool calling，模型可能会凭感觉胡说。但有了 tool calling，流程就是：
---
## Chunk 290 — 模型识别：这是 compatibility_check

模型识别：这是 compatibility_check

模型提取： part number model number 模型调用 checkCompatibility(partNumber, modelNumber) 工具返回 true/false/unknown 模型根据结果生成自然语言回复
---
## Chunk 291 — 你就记一句最核心的话：

你就记一句最核心的话：

先检索资料，再让模型基于资料回答。
---
## Chunk 292 — 它为什么重要？

它为什么重要？

因为模型自己记忆里的知识：  
可能不完整可能不准确可能不是你这个业务的数据可能会 hallucinate  
所以你需要让它先从你的知识库里找相关内容，再回答。
---
## Chunk 293 — 理论上是什么 Hallucination

理论上是什么 Hallucination

hallucination 就是模型“看起来说得很像真的，但其实是编的”。
---
## Chunk 294 — 比如：

比如：

编造一个不存在的 part 说某型号兼容，其实不兼容说某个安装步骤是这样，但实际资料里没有 Grounding  
grounding 就是让模型的回答“有依据”，基于：
---
## Chunk 295 — 简单说：

简单说：

hallucination = 胡编 grounding = 有根有据在你这个项目里，它拿来干嘛
---
## Chunk 296 — 这个项目非常怕 hallucination，因为这是电商+维修场景：

这个项目非常怕 hallucination，因为这是电商+维修场景：

如果兼容性说错，用户会买错零件如果安装指导说错，用户会操作错误如果故障排查说得太武断，会影响信任
---
## Chunk 297 — 所以你必须在设计上减少 hallucination：

所以你必须在设计上减少 hallucination：

范围缩小只做 refrigerator/dishwasher tool-first 先查数据，再说话 RAG 从知识库中取资料不确定时说不确定
---
## Chunk 298 — Structured output 就是：

Structured output 就是：

不要让模型随便吐一大段文本，而是让它按固定结构输出。  
例如输出成 JSON：  
{ "intent": "compatibility_check", "partNumber": "PS11752778", "modelNumber": "WDT780SAEM1" }
---
## Chunk 299 — 或者：

或者：

{ "reply": "Yes, this part is compatible.", "cards": [ { "type": "compatibility", "compatible": true } ], "suggestions": ["Show installation steps", "View product details"] }
---
## Chunk 300 — 更稳定更容易被程序处理更方便前端渲染更适合 agent workflow

更稳定更容易被程序处理更方便前端渲染更适合 agent workflow

八股：1. 「倒排思想（子串）」到底是什么？倒排（inverted index）本来是指：不是「从文档里找词」，而是「从词反查哪些文档里有它」。
---
## Chunk 301 — 经典例子：搜索引擎预先把网页处理成一张表：

经典例子：搜索引擎预先把网页处理成一张表：
---
## Chunk 302 — 经典例子：搜索引擎预先把网页处理成一张表：

词「冰箱」→ 出现在网页 A、网页 C 词「制冰机」→ 出现在网页 B、网页 C 用户搜「冰箱」，系统直接去表里拿「冰箱」对应的那几篇，比把全网扫一遍快得多。  
你们没有用这种建好的倒排表，但 lower.includes(关键词) 在效果上像一种极简版：  
「目录里预先有一些要找的串」（型号、关键词、matchIncludesAll 里的片段等） 「用户整句话是一个大文档」 逻辑是：看这些预定义串是否作为子串出现在用户话里  
所以我说「倒排思想（子串）」：指的是「用『词/短语 → 是否出现』这种查法」，而不是说你们真的实现了一个 Elasticsearch 那种倒排索引。更准确的一句是：你们是「在线子串匹配」，思想上接近 『从查询词去碰文档』这一侧，只是没有用索引加速。  
2. 结构化检索 vs 向量检索向量检索：把句子和每条数据都变成高维空间里的一个点（embedding），按「离得近不近」算相似度。优点：同义、换一种说法有时也能对上。缺点：为什么对上、有时错得离谱，不好解释；还要模型、算力、调参。结构化检索（你们这种）：命中条件是人写出来的明确规则，例如：  
消息里必须出现 PS11752778 且和表里的 partNumber 完全一致或型号串在规范化后要包含 WDT780SAEM1 或 matchFlexible：这一组里至少命中一个词，且另一组也至少命中一个词优点：可解释（「因为型号对上了」「因为关键词里出现了 lower rack」）。缺点：用户说法若和规则差太远，可能召不回。  
面试里可以一句话：向量偏「语义模糊匹配」，规则偏「符号/条件精确控制」；数据小、要合规和可解释时规则很划算；大了可以规则先收窄再向量精排，叫互补。  
3. 过滤条件/grounding（有 part 时兼容必须同 partNumber） Grounding 这里通俗讲：回答必须拴在「检索到的具体行」上，不能乱编。  
你们加了一层过滤：用户话里已经通过 PS 锁定了一个零件 A，再去扫兼容表时，只接受「也是零件 A」的那条兼容记录。
---
## Chunk 303 — 经典例子：搜索引擎预先把网页处理成一张表：

你们加了一层过滤：用户话里已经通过 PS 锁定了一个零件 A，再去扫兼容表时，只接受「也是零件 A」的那条兼容记录。  
否则会出现：用户问的是「PS111 配不配这个型号」，模型却拿「PS222 和这个型号」的表行来答 ——张冠李戴。  
所以这叫约束检索：在已有「零件实体」的前提下，缩小兼容行的候选集合，降低错误关联。  
4. 数据 join（兼容命中后回填 part） Join 就是两张表按同一个键对齐。  
兼容表一行：型号 WDT780SAEM1+零件号 PS11752778+是否兼容零件表一行：PS11752778+标题、安装说明等用户只说了型号，你只知道「兼容表这一行」，但卡片上要展示零件详情，就要用 PS11752778 去零件表里再查一行。  
SQL 里就是：compat JOIN parts ON compat.part_number = parts.part_number。你们用 find 写了一遍，本质一样。  
5. Citation/provenance（出处、可追溯） Provenance = 「这个结论依据的是哪条原始数据」。  
你们每条命中往 citations 里塞：id、source（零件目录/兼容表/维修指南）、label。
---
## Chunk 304 — 用途可以是：

用途可以是：

前端展示「来源」 日志里审计「当时命中了哪一行」 和 RAG 类比：别人用 chunk id 标「第几块文档」；你们用 catalog 行的 id 标「第几条记录」——同一类设计问题：回答要对齐到可指明的证据上。 6. 置信度分层（label 里写 exact vs keyword match）不是模型算出来的概率，而是你们用命中路径区分「多确定」：  
直接对上 PS 正则+表里 partNumber 完全一致 → 通常认为最硬只是 keywords 子串蹭上 → 可能用户随口一说也会蹭到 → 你们在 label 里写 (keyword match)，提醒：这是另一条路径，可信度语义上弱一档以后若要升级，可以给每条路径一个 score（分数）；现在用不同 label 已经是「分层」的雏形。  
7. 布尔检索/「CNF/析取范式」味道（用大白话重说）忘掉术语也可以，只记两种模式：
---
## Chunk 305 — （1）matchIncludesAll —— 全是 AND

（1）matchIncludesAll —— 全是 AND

配置里写：["whirlpool", "ice maker"] 意思是：用户话里既要有 whirlpool 又要有 ice maker 才算这篇指南命中。这就是 AND：条件全满足。
---
## Chunk 306 — 例如概念上是：

例如概念上是：

第一组：用户话里出现 「制冰机」或「ice maker」或「icemaker」 里任意一个就行（组内 OR）第二组：出现 「不工作」或「坏了」或「no ice」 里任意一个就行（组内 OR）但两组都要至少命中一个词（组间 AND）用逻辑式写就是： (词1 ∨ 词2 ∨ …) ∧ (词A ∨ 词B ∨ …)  
我说「CNF/析取范式味道」：在数理逻辑里，一堆括号里是 OR、括号之间是 AND 这种形状，就叫合取范式的一种常见样子。你不用背名词，面试可以说：「我们是多组关键词，组内同义扩展用或，组与组之间用与，控制误匹配。」  
8. 精确率 vs 召回率（先严后宽在干什么）召回率：用户该找的东西里，有多少被你们找回来（找全了吗）。精确率：你们找回来的东西里，有多少真的是对的（乱的多不多）。先严后宽：先走 PS 精确、严格短语 → 宁可少报，也不要乱报 → 精确率优先。再走 keywords、matchFlexible → 多给一次机会，可能多捞一些边界说法 → 换一点精确率换召回。一句话：前面步骤像安检严检，后面步骤像「模糊补漏」  
js手撕
---
## Chunk 307 — 一些易错点

一些易错点

JavaScript//echo函数就是泛型 function echo<T>(arg: T): T {  
return arg  
}  
echo<string>('Hello')//明确传入类型参数 echo('Hello')
---
## Chunk 308 — Promise.all

Promise.all

return new Promise((resolve, reject) => {})//必须是两层括号，老是写成只有一层
---
## Chunk 309 — if (promise.length == 0){

if (promise.length == 0){

resolve([]) return//这里不要漏写return，因为resolve只是promise状态完成了，不是
---
## Chunk 310 — 函数执行完成，如果不写return函数还会接着往下执行for循环 }

函数执行完成，如果不写return函数还会接着往下执行for循环 }

带并发限制的promise Promise.resolve(promises[index]).then(
---
## Chunk 311 — resolve(results)

resolve(results)

}  
runNext()///这个写在then里，是为了完成一个任务，就再补一个  
},  
发布订阅模式EventEmitter class EventEmitter{
---
## Chunk 312 — constructor(){

constructor(){

this.events = {}//必须写constructor，不能直接const events
---
## Chunk 313 — = {}，因为需要每个实例都有自己的events

= {}，因为需要每个实例都有自己的events

}  
this.events[eventName].push(xxx) this.events xxx//全程都必须this.events才能指向当前events实例，如果
---
## Chunk 314 — 不写this，js会找不到events实例

不写this，js会找不到events实例

//必须写成箭头函数，不要写成普通function，否则会丢this const tempEvent = (...args) => {//必须要传入的时候有args下面才能
---
## Chunk 315 — this.off(eventName, tempEvent)

this.off(eventName, tempEvent)
---
## Chunk 316 — this.off(eventName, tempEvent)

}  
}  
深/浅拷贝：//都是4步，base case，本轮res[key]，for循环里下一轮，return  
深拷贝的： if (map.has(obj)){ return map.get(obj)//必须写map.has,专门处理循环引用的，比如obj.self = obj  
}  
for (const key of Object.keys(obj)){ res[key] = deepClone(obj[key], map)//for循环里不需要if判断了，因为base case写过了 }  
return res//必须最后return res！必须返回新对象  
flatten扁平化 return arr.reduce((cul, curr) => {//reduce是array的方法，必须是一个 array来call他，不能单独reduce }  
if (!Array.isArray(curr)){ return cul.concat(curr)//reduce里两个分支都必须return，是因为 return 的值会作为下一轮的 acc  
}  
递归版flatten if (Array.isArray(item)){ res = res.concat(flatten(item))//必须写res = res赋值，不能只写右边, 因为concat底层是创建新数组，然后浅拷贝原数组，不会修改原数组，要修改之后用新res承接 }  
防抖 return function debounced(fn,...args){//这里不再需要传fn，因为这里已经可以用闭包里的fn  
clearTimeout(timer)//清除timer使用clearTimeout，不是设置成null  
fn.apply(this, args)//apply的第二个参数必须是数组，...args是展开的格式，不加...才是数组格式
---
## Chunk 317 — this.off(eventName, tempEvent)

fn.apply(this, args)//apply的第二个参数必须是数组，...args是展开的格式，不加...才是数组格式  
节流 if (!canRun){ return//这是个base case，不能跑就停止，所以才是节流 } canRun = false//这次跑了下次就先别跑了  
流式输出 function sleep(interval) {  
return new Promise(resolve => setTimeout(resolve, ms))//我写成了resolve => (setTimeout, ms)，虽然可以简化，但是setTimeout里面必须保持是一个fn和一个ms的结构啊！我把参数都写丢了 }  
let result = ""//字符串不可变的，所以result+= xxx会返回新的字符串，不能用const  
60秒倒计时 4步，建const，useEffect里用interval和setTime改变时间，清理timer，return 组件
---
## Chunk 318 — const [time, setTime] = useState(60)

const [time, setTime] = useState(60)

useEffect(() => { const timer = setInterval(() => {//必须用setInterval setTime(prev => { if (prev <= 0){//这里要用prev，不能用time！！因为time是闭包，不是最新的数据 clearInterval(timer) return 0//必须返回一个值，不能返回undefined }
---
## Chunk 319 — else{

else{

return prev - 1  
}  
})  
}, 1000)  
return () => clearInterval(timer)//clean up必须是函数，箭头函数普通函数都行，但是直接return clearInterval(timer)等价于返回结果，也就是 return undefined，不行！ }, [])  
return <div>{time}</div>  
}  
parseUrl const [path, queryStr] = url.split("?")//const合起来写 query = {}//必须用对象  
query[key] = [].concat(query[key], decodeURIComponent(value))//一般都写[].concat(a，b)，能把a和b拼起来，concat左边一般都是[]  
PromiseWithTimeout//promise都是const！！！要么拿const接着，要么直接return const timeOutPromise = new Promise((_, reject) => {//第一个 resolve省略成下划线，不能不写  
Promise.race([promise1, promise2])//race里面必须是数组  
curry return function(...nextArgs){//这是匿名函数 return curried(...args,...nextArgs)  
}
---
## Chunk 320 — //容易忘记后半部分是个匿名函数

//容易忘记后半部分是个匿名函数

this绑定规则 this = 当前函数“运行时”的调用对象，this属于函数，不属于对象。
---
## Chunk 321 — 判断this的唯一规则：看调用方式，不看函数来源

判断this的唯一规则：看调用方式，不看函数来源

点调用obj.print() VS f() 点调用（obj.fn()）会把点前面的对象作为 this，而普通调用（fn()）没有调用者，因此 this 使用默认绑定（window/undefined）。
---
## Chunk 322 — 判断this的唯一规则：看调用方式，不看函数来源 > JavaScript

判断this的唯一规则：看调用方式，不看函数来源 > JavaScript

obj.print() → this = obj (obj.print)(); → this = obj//括号只是改变优先级，不改变调用方式  
const f = obj.print; f() → this 丢（变成window/undefined）//f 是 obj.print 取出来的值 → 所以这个值丢了 obj → 所以没有 this
---
## Chunk 323 — ✅ 有点（绑定 this） obj.print()

✅ 有点（绑定 this） obj.print()

//this = obj
---
## Chunk 324 — (obj.print)()

(obj.print)()

//this = obj  
obj["print"]()//this = obj  
❌ 没点（丢失 this） const f = obj.print; f();//说的是这里没有点//this = window/undefined (obj.print = f)//this也丢失，因为这个obj.print = f是赋值表达式,返回的是f 函数本身，this丢失
---
## Chunk 325 — 四种this

四种this

1. 普通函数调用（this默认指向全局对象，浏览器为window，严格模式下卫 undefined） a. 即直接fn()，setTimeout 2. 对象方法调用（this = 调用对象）
---
## Chunk 326 — const obj = {

const obj = {

x: 10,  
a: {  
x: 20,  
fn() {  
console.log(this.x);  
}  
}  
};  
obj.a.fn();//this=obj.a，this由最后的调用者决定，而不是函数定义位置
---
## Chunk 327 — JavaScript

JavaScript

function Person(name) {  
this.name = name;  
}  
const p = new Person("Tom");//new 会创建新对象，并把 this 绑定到这个对象上  
console.log(p.name);//this=p  
4. call/apply/bind (手动绑定this） a. call：改 this+立即执行 b. apply：改 this+立即执行（参数数组） c. bind：返回新函数+永久绑定 this  
fn.call(obj)和fn.apply(obj, [1, 2]) 的意思是：当 fn 执行时，把 this 指向 obj（call 让 fn “假装”是 obj 调用的） bind：返回新函数+锁 this（bind 只在第一次绑定时生效，之后再 bind 不会改变 this），bind了之后，即使再用call，也改变不了已绑定的this
---
## Chunk 328 — function fn() {

function fn() {

console.log(this.x);  
}  
const f1 = fn.bind({ x: 1 });//bind 会返回一个新函数，并在第一次绑定时确定 this（x：1），之后再次 bind 不会生效，因此 f2 仍然使用 f1 的 this  
const f2 = f1.bind({ x: 2 });  
f2();//1
---
## Chunk 329 — Debounce防抖函数

Debounce防抖函数

防抖的核心是：在高频触发场景下，每次触发都先清掉上一次的定时器，再重新开启一个新的定时器，只有最后一次触发停止一段时间后，函数才会真正执行。实现上通常会用闭包保存 timer，让多次调用共享同一个定时器变量。
---
## Chunk 330 — JavaScript

JavaScript

function debounce(fn, delay) {  
let timer = null;
---
## Chunk 331 — if (timer) {

if (timer) {

clearTimeout(timer);
---
## Chunk 332 — //这后面不应该直接接return

//这后面不应该直接接return

}
---
## Chunk 333 — timer = setTimeout(() => {

timer = setTimeout(() => {

fn.apply(this, args);  
}, delay);  
};  
}  
const betterSearch = debounce(search, 300);  
追问 1：为什么 debounce 要用闭包？因为 timer 要在多次调用之间共享，但又不能是全局变量，所以要放在闭包里。
---
## Chunk 334 — 追问 2：为什么要 return function？

追问 2：为什么要 return function？

因为要返回一个“包装后的新函数”，用户以后调用的是这个新函数，不是原函数。
---
## Chunk 335 — 追问 3：防抖和节流区别？

追问 3：防抖和节流区别？

防抖：停下来再执行最后一次节流：固定时间内最多执行一次  
throttle节流函数节流的核心是控制高频事件的执行频率，在固定时间内最多执行一次。实现方式可以用时间戳或者定时器。时间戳版本会记录上一次执行时间，只有当前时间和上一次执行时间的差值大于设定间隔时，才允许再次执行。  
JavaScript//第一种，计时器写法，第一次调用会delay，延迟执行 function throttle(fn, delay){  
let canRun = true;//外面只设置一个闭包变量 return function(...args){  
if (!canRun) return;  
canRun = false;
---
## Chunk 336 — setTimeOut(() => {

setTimeOut(() => {

fn.apply(this, args);  
canRun = true;  
}, delay);  
}  
}  
//2. 时间戳版本，第一次立即执行 function throttle(fn, delay){  
let lasttime = 0;
---
## Chunk 337 — return function(...args){

return function(...args){

let now = Date.now();
---
## Chunk 338 — if (now - lasttime > delay){

if (now - lasttime > delay){

fn.apply(this, args);  
lasttime = now;  
}  
}  
}
---
## Chunk 339 — Promise.all([p1, p2, p3]) 的行为是：

Promise.all([p1, p2, p3]) 的行为是：

1. 接收一个数组 2. 等数组里所有 Promise 都成功 3. 按原顺序返回结果数组 4. 只要有一个失败，就立刻 reject  
Promise.all 的实现核心是返回一个新的 Promise，内部遍历输入数组，对每一项用 Promise.resolve 包装后统一处理。每个 Promise 成功时，把结果按原下标存入结果数组，并统计完成数量；当全部完成时，调用 resolve(results)。如果任意一个失败，就立即 reject。
---
## Chunk 340 — JavaScript

JavaScript

function myPromiseAll(promises){  
return new Promise(resolve, reject) => {  
let results = [];  
let count = 0;
---
## Chunk 341 — if (promises.length === 0){

if (promises.length === 0){

resolve([]);  
return;  
}  
for (let i = 0; i < promises.length; i++){
---
## Chunk 342 — (value) => {

(value) => {

results[i] = value;  
count++;
---
## Chunk 343 — if (count == promises.length){

if (count == promises.length){

resolve(results);  
}  
},
---
## Chunk 344 — (error) => {

(error) => {

reject(error);  
}  
)  
}  
}  
}
---
## Chunk 345 — JavaScript

JavaScript

function promiseAll(promises){  
return new Promise(resolve, reject) => {  
let results = [];  
let count = 0;
---
## Chunk 346 — if (promises.length == 0){

if (promises.length == 0){

resolve([]);  
return;  
}  
for (int i = 0; i < promises.length; i++){  
Promise.resolve(promises[i]).then(//容易忘
---
## Chunk 347 — (value) => {

(value) => {

results[i] = value;  
count++;
---
## Chunk 348 — if (count == promises.length){

if (count == promises.length){

resolve(results);  
}  
}
---
## Chunk 349 — (error) => {

(error) => {

reject(error);  
}  
)  
}  
}  
}  
流式输出给一个字符串 "hello"，每隔 500ms 输出一个字符
---
## Chunk 350 — function sleep(interval){

function sleep(interval){

return new Promise((resolve)=>setTimeout(resolve, interval));  
}  
async function streamOutput(text, onChunk, interval){  
let result = "";
---
## Chunk 351 — for (const char of text){

for (const char of text){

result+= char;  
onChunk(result);  
await sleep(interval);  
}  
}  
streamOutput("hello, world!", (output)=>{console.log(output}, 300)'  
//(output)=>{console.log(output}就是onChunk
---
## Chunk 352 — JavaScript

JavaScript

const chunks = ["Hel", "lo, ", "world", "!"];
---
## Chunk 353 — function sleep(interval){

function sleep(interval){

return new Promise((resolve)=>setTimeout(resolve, interval));  
}  
async function streamOutput(chunks, onChunk, interval){  
let result = "";
---
## Chunk 354 — for (const piece of chunks){

for (const piece of chunks){

result+= piece;  
onChunk(result);
---
## Chunk 355 — await sleep(interval)

await sleep(interval)

}
---
## Chunk 356 — return result

return result

}  
streamOutput(chunks, (output)=>{console.log(output)},300)  
timeout 的 Promise 实现实现一个 promiseTimeout，传入一个 Promise 和超时时间，如果在规定时间内没有 resolve/reject，就返回 timeout error。  
JavaScript//Promise Race, 一个是真正的异步任务，一个是timeoutPromise，谁先结束就用谁的结果。 function promiseWithTimeout(promise,timeout){  
const timeoutPromise = new Promise((_,reject)=>{
---
## Chunk 357 — setTimeout(() => {

setTimeout(() => {

reject(new Error("Request timeout");  
},timeout);  
});  
return Promise.race([promise, timeoutPromise]);  
}  
const task = new Promise((resolve)=>{  
setTimeout(()=>resolve("success"),1000);  
});
---
## Chunk 358 — .then((res)=>console.log(res))

.then((res)=>console.log(res))

.catch((err)=>console.error(error.message));
---
## Chunk 359 — JavaScript

JavaScript

function promiseWithTimeout(fn, interval){  
return new Promise((resolve,reject) => {
---
## Chunk 360 — const timer = setTimeout(() => {

const timer = setTimeout(() => {

reject(new Error("request rejected");  
},interval);
---
## Chunk 361 — .then((res) => {

.then((res) => {

clearTimeout(timer);  
resolve(res);  
})
---
## Chunk 362 — .catch((err) => {

.catch((err) => {

clearTimeout(timer);  
reject(err);  
});  
});  
}
---
## Chunk 363 — new Promise((resolve)=>{

new Promise((resolve)=>{

setTimeout(()=>resolve("done"),);  
})1000  
,2000)
---
## Chunk 364 — .then(console.log)

.then(console.log)

.catch(console.err);
---
## Chunk 365 — JavaScript

JavaScript

function fetchWithTimeout(url, options = {}, timeout = 5000){  
const controller = new AbortController();  
const signal = controller.signal;  
return new Promise((resolve,reject) => {
---
## Chunk 366 — const timer = setTimeOut(() => {

const timer = setTimeOut(() => {

controller.abort();  
reject(new Error("request rejected"));
---
## Chunk 367 — },timeout)

},timeout)

fetch(url, {...options,signal})
---
## Chunk 368 — .then((res) => {

.then((res) => {

clearTimeout(timer);  
resolve(res);  
})
---
## Chunk 369 — .catch((err) => {

.catch((err) => {

clearTimeout(timer);  
reject(error);  
});  
})  
}
---
## Chunk 370 — res = []

res = []

for (let item of arr){
---
## Chunk 371 — res.push(item)

res.push(item)

}  
}  
return res  
}
---
## Chunk 372 — function flatten(arr){

function flatten(arr){

return arr.reduce((acc,cur) => {
---
## Chunk 373 — if Array.isArray(cur){

if Array.isArray(cur){

return acc.concat(flatten(cur))//concat的特点是不会
---
## Chunk 374 — } else {

} else {

return acc.concat(cur)  
}  
},[])  
}  
GroupBy
---
## Chunk 375 — function groupBy(arr, fn){

function groupBy(arr, fn){

return arr.reduce((acc,cur) => {  
const key = fn(cur) if!acc[key]{//acc.has(key)是Map方法，acc[key]是普通对象
---
## Chunk 376 — acc[key] = []

acc[key] = []

}
---
## Chunk 377 — acc[key].push(cur)

acc[key].push(cur)

return acc  
},{})  
}
---
## Chunk 378 — JavaScript

JavaScript

arr.reduce((acc, cur) => {}, initialValue)//求和 [1, 2, 3].reduce((acc, cur) => acc+cur, 0)  
//map function map(arr, fn) {//例如把[1,2,3]map成[4,5,6] return arr.reduce((acc, cur, i) => {  
acc.push(fn(cur, i)) return acc//返回是因为reduce的下一轮要用这个acc }, [])  
}
---
## Chunk 379 — function filter(arr,fn){

function filter(arr,fn){

return arr.reduce((acc,cur) => {
---
## Chunk 380 — acc.push(cur)

acc.push(cur)

}  
return acc  
},[])  
}
---
## Chunk 381 — this.events = {}

this.events = {}

}
---
## Chunk 382 — this.events[eventName] = []

this.events[eventName] = []

}  
this.events[eventName].push(listener)  
}
---
## Chunk 383 — if (!this.events[eventName]) {

if (!this.events[eventName]) {

return  
}  
this.events[eventName].forEach(listener => {
---
## Chunk 384 — listener(...args)

listener(...args)

})  
}
---
## Chunk 385 — if (!this.events[eventName]) {

if (!this.events[eventName]) {

return  
}  
this.events[eventName] = this.events[eventName].filter(  
fn => fn!== listener  
)  
}
---
## Chunk 386 — this.off(eventName, wrapper)

this.off(eventName, wrapper)

}
---
## Chunk 387 — this.on(eventName, wrapper)

this.on(eventName, wrapper)

}  
}
---
## Chunk 388 — TypeScript

TypeScript

import React, { useEffect, useState } from "react";  
export default function Countdown() {  
const [seconds, setSeconds] = useState(60);
---
## Chunk 389 — useEffect(() => {

useEffect(() => {

if (seconds <= 0) return;
---
## Chunk 390 — const timer =setInterval(() => {

const timer =setInterval(() => {

setSeconds(prev => prev - 1)  
}, 1000);  
return () => clearInterval(timer);  
}, [seconds]);  
return <div>{seconds}s</div>;  
}
---
## Chunk 391 — 实现Append函数

实现Append函数

把任意多个值追加到目标数组里，过滤掉 undefined、null 等空值，返回新数组；同时兼容 arr 不是数组、或者 arr 为 undefined/null 的情况  
写法 append(base, item) append(base,...item)..items用法  
结果 push 一个数组 push 数组里的元素
---
## Chunk 392 — 实现Append函数 > JavaScript

实现Append函数 > JavaScript

function append(arr,...items){  
let base = Array.isArray(arr)? [...arr]: [];
---
## Chunk 393 — for (const item of items){

for (const item of items){

if (item === undefined || item === null) continue;
---
## Chunk 394 — base.push(item)

base.push(item)

}  
}
---
## Chunk 395 — return base

return base

}  
深拷贝嵌套对象会一层一层递归拷贝，同一个对象被多个属性引用时，不会重复拷贝
---
## Chunk 396 — JavaScript

JavaScript

function deepClone(obj, map = new Map()) {//1. 基本类型 if (obj === null || typeof obj!== 'object') return obj;  
//2. 处理循环引用 if (map.has(obj)) return map.get(obj);
---
## Chunk 397 — //3. 创建容器 const res = Array.isArray(obj)?

//3. 创建容器 const res = Array.isArray(obj)?

[]: {};  
map.set(obj, res);  
//4. 遍历（推荐 Object.keys） for (const key of Object.keys(obj)) {  
res[key] = deepClone(obj[key], map);  
}  
return res;  
}
---
## Chunk 398 — 柯里化 = 把一个需要多个参数的函数，拆成多次传参数

柯里化 = 把一个需要多个参数的函数，拆成多次传参数

柯里化用在：需要“固定一部分参数+复用逻辑” 的场景，比如固定request(“POST”)里的POST
---
## Chunk 399 — JavaScript

JavaScript

function curry(fn) {
---
## Chunk 400 — if (args.length >= fn.length) {

if (args.length >= fn.length) {

return fn(...args);  
}
---
## Chunk 401 — return function (...nextArgs) {

return function (...nextArgs) {

return curried(...args,...nextArgs);  
};  
};  
}
---
## Chunk 402 — JavaScript

JavaScript

function parseUrl(url) {  
const [path, queryStr] = url.split('?')
---
## Chunk 403 — const query = {}

const query = {}

queryStr?.split('&').forEach(kv => { let [k, v = ''] = kv.split('=')//split之后变成array
---
## Chunk 404 — if (query[k]) {

if (query[k]) {

query[k] = [].concat(query[k], decodeURIComponent(v))
---
## Chunk 405 — query[k] = decodeURIComponent(v)

query[k] = decodeURIComponent(v)

}  
})  
return { path, query }  
}  
反问&其他
---
## Chunk 406 — 反问：

反问：

如果我加入的话，前3个月最希望我能补齐或者做到的能力是什么？像豆包这种 AI 产品，前端在模型能力和用户体验之间是怎么做权衡的？团队现在前端主要在解决哪些比较有挑战的问题？
---
## Chunk 407 — 为什么选择前端

为什么选择前端

我选择前端主要有几个原因。首先是我比较喜欢做用户能直接感知的东西，比如在 Pawse 项目里做 Feed 和图片加载优化的时候，滚动流畅度和加载速度的提升是能明显感受到的，用户的反馈让我很有成就感。  
其次是我本身对设计和交互也比较感兴趣，平时会画画，也会关注一些 UI 和交互细节，所以在做前端的时候，会更自然地去思考比如信息怎么呈现、交互是否顺畅这些问题。  
但同时我也觉得前端不只是设计，它其实有不少工程挑战，比如状态管理、异步更新、性能优化这些问题，我在项目里也比较喜欢去优化这些部分。  
另外像豆包这种 AI 产品，我觉得前端在交互体验上会更关键，比如流式输出、对话体验这些，所以我也挺希望能参与这种更复杂的交互设计。
---
## Chunk 408 — 怎么看待ai写代码

怎么看待ai写代码

我现在在日常开发和刷题中会比较频繁地使用 AI 辅助编码，比如用它来快速生成基础代码结构、或者在遇到 bug 时帮助定位问题。但我不会直接依赖它的代码，而是会把它当成一个“加速器”，比如让我更快验证思路或者对比不同实现方式。  
我觉得 AI coding 最大的价值是在提升开发效率，尤其是在一些重复性工作或者不熟悉的领域上，但它的问题是有时候会生成看起来正确但实际上有问题的代码，所以我一般会结合自己的理解去检查和调整，而不是直接使用。  
我一般会在几个场景下用 AI coding：  
第一是快速搭结构，比如一个新功能或者一个算法，我会先让 AI 给一个初版，然后我再根据自己的思路做修改；第二是 debug，比如报错或者逻辑不符合预期时，我会把关键信息给 AI，让它帮我分析可能的原因；第三是对比不同实现方式，比如某个功能用不同数据结构实现，我会让 AI 给多个方案，然后自己判断 trade-off。  
但我会比较注意的一点是，不会把它当成完全可信的答案，而是当成一个辅助工具。  
Ai agent  
我最近也在学习 AI agent 相关的东西，目前主要是用 Dify 搭了一些比较简单的 agent 做探索，比如尝试做一个用于 brainstorm startup idea 的 agent。  
现在还在比较 early 的阶段，我主要是在理解 agent 的基本结构，比如 prompt 设计、工具调用以及多轮对话的组织方式。我现在更多是在探索不同 prompt 设计对结果的影响，以及怎么让输出更稳定和有结构。  
目前还没有做到一个特别完整的产品级项目，但这个过程中让我对 AI 在产品中的应用方式有了一些更直观的理解。
---
## Chunk 409 — 你这个 agent 怎么工作的？

你这个 agent 怎么工作的？

现在结构还比较简单，本质上是通过设计 prompt 来引导模型生成比较结构化的创业想法，比如会引导它从 problem、solution、target user 这些维度去输出。同时我也在尝试加入一些工具调用，比如固定模板或者约束输出格式，让结果更稳定
---
## Chunk 410 — Mova 5.5

Mova 5.5

准备：以高阶智能，让产品带着思考去清洁，把人类从日常琐事中解放，回归创造本质。非常非常重要，在ai盛行的今天，我觉得这是我们真的该做的事情。  
美学->设计+工程落地全球市场：有留学经验，会多国语言听了校招宣讲会，感觉对于新人有非常多的机会，有ownership。比如听说产品经理可以去不同的国家参加展会，可以落地blabla，很感兴趣  
问了很多ai agent项目的深挖，我估计要凉了多模态有没有做，只是纯文本吗具体哪个地方做了ai，都扮演什么角色怎么定的域都用的什么模型，claude，gpt，codex，分别都干嘛的你这玩意做了多久做的一个agent还是多个agent，为啥选择一个agent 前端跟其他地方是怎么协作的，后端，ui。尤其问了是更注重ui还原度还是流畅性，我回答的分情况讨论ab test，但他说一定是流畅性优先的。作为全栈，需要思考的更多，跟后端联调如果让你做一个ai漫剧，你该怎么做，用什么模型，看看ai漫剧怎么做的什么时候到岗  
“现在虽然不知道，但是给时间很迅速的就能学会”，在贵公司的指导下我可以学习  
总结就是一直在打断我，也不开摄像头，虽然来了两个人但给我感觉不太尊重。
---
## Chunk 411 — ai 项目过了

ai 项目过了

禾塞 4.28 问了ts八股，问我python做过什么，一道ts综合应用题，不会写。  
Ai agent方面提了两个建议，一个是对ai的能力的要更广泛的认知，使用知识库本身是对的。但是几万个产品的话怎么去做，要更加对ai能力的范围了解 2. 调用prompt的时候有什么库，了解一下，对于ai的基础知识
---
## Chunk 412 — 下一步：

下一步：

Ts，js八股加强！ ai完善，研究prompt怎么调用的，研究几万个产品的话是怎么做的，接了数据库  
小红书 4.27 React和unity模拟动物森友会，前端后端选啥，怎么做前端做一个动画，从js到出现在浏览器上经过了什么，穿插了打包一堆ai agent要我介绍实现流程的问题追问：如果用户给的信息品牌没办法match上，match可能出错怎么办，回答了两层：匹配+确认&索引  
React native比ract快的原因是啥？我回答我体感慢，扯到bridge，fiber，react和native，提到swift 和flutter
---
## Chunk 413 — 反问再问回来最后还问了在美国的面试情况，startup

反问再问回来最后还问了在美国的面试情况，startup

前面的开放题还行js手写题是场景题，写的太烂，根本不会读代码。。。。
---
## Chunk 414 — 下一步：

下一步：

加强js手写题，js读代码能力，不只是死记硬背把ai agent项目接了实际的数据库  
字节 4.7 讲了menu项目，讲我做的需求埋点。问埋点的数据怎么来的，根数据分析部分为啥用redux 问单向数据流问mcp具体做了啥问写日英互译的时候是调prompt还是啥
---
## Chunk 415 — (没回答出来）

(没回答出来）

Diff的过程（我提到了virtual DOM和浅比较）  
○  
react中useEffect的数组里顺序变换，会不会重新渲染（回答的有问题，这个数组顺序变换的化内存地址没变，所以不会重新渲染，但是当时没get到他在考我这个，所以我回答的是会重新渲染）  
Spec coding和vibe coding区别（让我查了spec coding） ● 说对于未来是spec还是vibe的我自己的看法 ● 更多关于我日常怎么用ai coding的
---
## Chunk 416 — 大概40min，然后根本就没做题反问

大概40min，然后根本就没做题反问

1. 如果进入公司，前三个月最大挑战（工作强度根实习生的区别） 2. 各种拥抱ai，用ai自己写需求做需求，因为某种意义上也要train火山引擎
---
## Chunk 417 — 三天后挂，原因：

三天后挂，原因：

1. React基础，复习八股的时候不知道哪些是最重要（但是简单的），比如key我完全不知道是啥，但其实非常简单，那问我我不会就非常扣分。还有useEffect浅比较比的是依赖数组里的东西的地址，我只是再振振有词的背浅比较，但是给我一个真实例子我就瞎猜。那面试官肯定是觉得我基础不稳，因为大厂更看重基础  
2. AI部分，你说了 MCP/prompt，但没打深度。尤其是flow又是一个ai部门，那我这边说的深度就是还不够，他问的日英互译怎么弄的我显然没答上来  
3. 好的部分：项目很深，业务很ok，所以被横向了。
---
## Chunk 418 — 下一步：

下一步：

1. 八股文要更加面试导向，而不是知识导向。现在的重点错了。我需要按照面试命中率排行，而不是把一个不重要的小点挖的非常深。  
后端纯笔记
---
## Chunk 419 — 一、网络编程

一、网络编程

1. 网络分层应用层协议（HTTP/DNS）传输层协议（TCP/UDP）网络层协议（IP）  
HTTP（应用层）GET/index.html ↓ TCP（传输层）负责建立连接，确保送到和顺序 ↓ IP（网络层）找到目标地址  
2. TCP与UDP 的核心区别有哪些？ TCP 是面向连接的（会先建立连接）、可靠的传输协议（必须确认收到），提供顺序保证（即使2先到 Receiver也会先等1再按顺序排好）、重传机制（丢了会补发）和拥塞控制； UDP 是无连接的、不可靠的协议，不保证顺序和重传，但开销更小、延迟更低。  
3. TCP 和UDP 的应用层协议（实际用的功能规则） TCP: HTTP（网页传输）\ HTTPS（加密网页）\ FTP（文件传输） UDP: DNS（域名解析）\ DHCP（地址分配） \ 视频/语音（如 RTP）  
HTTP 是用于客户端与服务器之间进行资源请求和响应的应用层协议（浏览网页、请求数据、调用 API） HTTP不能基于UDP是因为网页加载数据量大，且顺序必须对 FTP 是用于在客户端和服务器之间传输文件的协议，支持上传和下载（传大文件） SMTP 用于发送邮件，从客户端到服务器，或服务器之间传输邮件。基于 TCP（可靠）  
DNS 用于将域名解析为 IP 地址，是互联网访问的第一步（上网时计算器只认IP） DNS 基于UDP 是因查询请求数据量小，UDP 低延迟能提升解析速度。若数据量过大，DNS 会自动切换为TCP协议传输，确保数据完整传输。DNS丢包会重新发请求，不依赖TCP的重传机制。它会设置timeout，如果没收到响应再重新发送请求。这就是把可靠性从传输层上移到应用层，保证可靠的同时更轻量（没有三次握手延迟更低） DHCP 用于动态分配 IP 地址，使设备无需手动配置即可接入网络（连接WIFI自动获得IP地址） RTP Real-time Transport Protocol用于实时音视频传输，强调低延迟而非完全可靠（视频通话、直播、游戏语音，强调快而非可靠）
---
## Chunk 420 — 一、网络编程 > 4. TCP 的三次握手和四次挥手三次握手

一、网络编程 > 4. TCP 的三次握手和四次挥手三次握手

1. 客户端发送 SYN (Synchronize) 2. 服务端返回 SYN+ACK 3. 客户端发送 ACK (Acknowledgement)，连接建立  
核心是同步双方序列号不是两次 - 防止旧的连接请求影响新连接（避免历史 SYN 包）第三次 ACK 丢失或根本没有设计第三次确认，会导致服务端误以为连接已经建立。
---
## Chunk 421 — 四次挥手

四次挥手
---
## Chunk 422 — 四次挥手

1. Client → FIN (Finish) 2. Server → ACK（只是server知道client向自己发完了，但server自己可能还没发完） 3. Server → FIN 4. Client → ACK  
四次挥手的本质是：TCP 的两个方向必须独立关闭，而不是一次性关闭整个连接。  
TCP 是全双工通信，连接的两个方向是独立的。当主动关闭方发送 FIN 时，只表示自己不再发送数据，但仍然可以接收数据。被动方在收到 FIN 后，可能还有未发送完成的数据，因此需要先发送 ACK 确认，再在数据发送完毕后发送 FIN，从而导致四次挥手。  
如果四次挥手时，主动方发送的最后一个ACK 丢失，被动方会因未收到ACK 超时重传FIN 报文，主动方在TIME_WAIT 状态下会重新发送ACK。若超过重传次数，被动方会关闭连接；主动方TIME_WAIT 超时后也会关闭连接，确保连接最终释放。  
5. TCP 的滑动窗口和拥塞控制机制 TCP 通过滑动窗口允许发送方连续发送多个数据，提高传输效率。同时通过接收窗口（rwnd）实现流量控制，防止接收方过载；通过拥塞窗口（cwnd）实现拥塞控制，防止网络过载。最终发送窗口取 min(rwnd, cwnd)。拥塞控制通过慢启动、拥塞避免、快速重传和快速恢复机制动态调整 cwnd，以平衡传输效率和网络稳定性。 rwnd（接收窗口）当前接收方能承受的接受量 cwnd（拥塞窗口）当前网络能承受的发送量  
滑动窗口控制接收方，防止接收方爆掉。接收方通过TCP 头接受窗口大小告知缓冲区状态，发送方仅发送窗口内数据，接收方确认后窗口右移。流量控制中，窗口大小动态调整，避免接收方缓冲区溢出。  
拥塞控制控制发送方，防止发送过多导致网络堵塞和丢包滑动窗口大小由拥塞窗口决定，根据网络拥塞状态（如丢包）调整拥塞窗口，避免网络拥堵。本质：平衡传输效率和网络稳定性，避免因拥塞导致的丢包。先试探网络能承受多少 → 再慢慢增加 → 一旦出问题就降速
---
## Chunk 423 — 四次挥手

慢启动：cwnd指数增长，快速试探网络容量拥塞避免：cwnd线性增长，因此已经接近网络极限，避免网络拥塞快速重传：收到三个ACK后（若2丢失，则接收方一直收到ACK1，因为TCP是按顺序确认的，2不确认不会确认3），立即重传丢包数据，无需等待超时（提前判断丢包立即重传）快速恢复：重传后不会到慢启动，而是降速但继续发送超时丢包：网络严重堵塞，需要回到慢启动，cwnd从1开始
---
## Chunk 424 — 四次挥手 > 6. UDP 如何实现可靠传输 UDP 可通过应用层补充机制实现可靠传输

四次挥手 > 6. UDP 如何实现可靠传输 UDP 可通过应用层补充机制实现可靠传输
---
## Chunk 425 — 四次挥手 > 6. UDP 如何实现可靠传输 UDP 可通过应用层补充机制实现可靠传输

序号机制 (Sequence Number) - 给每个数据包编号，用以检测丢包、保证顺序 ● ACK确认机制 - 接收方接受到数据后发送ACK，确认数据到达或触发重传 ● 重传机制 (Retransmission) - 超时or检测丢包触发重新传送 ● 窗口控制 - 模仿TCP进行RTT估计和限速  
应用场景： 1. 实时音视频（如RTP+RTCP 协议，容忍少量丢包，关键帧重传） 2. 游戏通信（如LOL 游戏指令，基于UDP+自定义可靠机制，低延迟优先） 3. 物联网通信（如MQTT-SN，资源受限设备，需可靠且低开销）。  
7. QUIC协议 QUIC 是一个基于 UDP 实现的、在应用层提供可靠传输和拥塞控制的协议，被 HTTP/3 使用。它解决了TCP+HTTP的痛点即建立连接慢（多次握手）、队头阻塞（如果2丢了那么3、4必须等）、连接迁移困难（TCP绑定IP+端口，一旦切换则会断链，例如WIFI切4G）。QUIC 把“原本 TCP 在传输层做的事情”，搬到了应用层自己实现，自己实现序号、ACK、重传和拥塞控制。QUIC支持多路复用，即如果streamA发现丢包不会影响streamB，因此无对头堵塞。QUIC用Connection ID因此连接不断。追问1：QUIC协议是如何基于UDP 实现可靠传输的？它相比TCP 有哪些优势？参考回答：QUIC 通过序列号、确认重传、流量控制等机制实现可靠传输，同时具备优势：1. 握手延迟低（1RTT 或0-RTT）；2. 解决TCP 队头阻塞（基于流的独立传输）；3. 内置加密（TLS 1.3）；4. 连接迁移（基于连接ID，支持IP/端口变更）。  
8. 粘包和拆包粘包：多个数据包合并接收（发送Hello和World，接受端收到HelloWorld）拆包：单个数据包拆分接收（发送Hello，接受端收到He和llo）原因  
TCP 是流式传输，没有消息边界 ● 发送端缓冲区未满时把多个小包合并发送（提高效率），接受端缓冲区有限，拆分接收 ● Nagle算法让小数据被合并发送，更容易粘包
---
## Chunk 426 — 四次挥手 > 6. UDP 如何实现可靠传输 UDP 可通过应用层补充机制实现可靠传输

TCP 是流式传输，没有消息边界 ● 发送端缓冲区未满时把多个小包合并发送（提高效率），接受端缓冲区有限，拆分接收 ● Nagle算法让小数据被合并发送，更容易粘包  
解决方案 1. 固定消息长度（如每个消息1024 字节，不足补零）  
2. 分隔符标记（如用“\r\n”结尾），适用于文本数据，需要通过转译处理避免冲突 3. 消息头+消息体（头中包含消息长度），通用且可靠，适用于二进制数据  
9. HTTP/1.1、HTTP/2、HTTP/3 的主要区别 HTTP/2 的多路复用机制是如何实现的？ HTTP/1.1 是文本协议（长连接+管线化），存在队头阻塞 HTTP/2 是二进制协议，支持多路复用（并发请求 - 将请求/响应拆分为二进制帧，每个帧标记流ID，同一连接中多个流并行传输，互不干扰）+头部压缩 (HPACK)，但还是基于TCP，由于TCP是一个流因此无法完全解决队头阻塞问题 - 若TCP层出现丢包，整个连接会堵塞，所有流都受影响。 HTTP/3 基于QUIC（UDP）从根本上解决TCP 队头阻塞 - 为每个流分配独立的UDP 数据包，丢包仅影响对应流，其他流正常传输，握手延迟低（1RTT），支持0-RTT 重连。HTTP/2  
10. HTTPS的加密流程 SSL/TLS协议的作用 HTTP+SSL/TLS，用于在客户端和服务器之间建立加密、安全的通信通道。 SSL/TLS 提供加密通信(Confidentiality)、身份认证 (Authentication)和数据完整性 (Integrity)保护。  
SSL (Secure Sockets Layer) 用于加密网络通信的安全协议，现在已废用 ● TLS (Transport Layer Security) SSL的升级版本，握手过程被优化，可以减少RTT
---
## Chunk 427 — 四次挥手 > 6. UDP 如何实现可靠传输 UDP 可通过应用层补充机制实现可靠传输

SSL (Secure Sockets Layer) 用于加密网络通信的安全协议，现在已废用 ● TLS (Transport Layer Security) SSL的升级版本，握手过程被优化，可以减少RTT  
加密流程 1. SSL/TLS 握手：客户端发起请求 2. 服务端回CA 证书（防止中间人攻击）、共钥（锁）、域名 3. 客户端验证证书有效后，生成一个随机key，并用服务器共钥加密（把key放进箱子用锁锁住）。通过服务端公钥加密传输，即使被拦截，无服务端私钥也无法解密，能进一步提升密钥安全性，避免会话密钥直接暴露。 4. 服务器用私钥（钥匙）解密得到key，双方生成对称密钥 5. HTTP 数据传输：用会话密钥（对称加密）加密数据，MAC 校验完整性。
---
## Chunk 428 — 四次挥手 > 11. RESTful API

四次挥手 > 11. RESTful API

RESTful API 是一种基于 HTTP 的接口设计风格，用“资源+HTTP 方法”来描述系统操作。  
传统写法：/getUser，把行为写进URL ● RESTful API：/users，操作靠HTTP方法
---
## Chunk 429 — 核心原则

核心原则

1. 资源导向：URL 表示资源（如/users/123，而非/getUser?id=123） 2. HTTP 方法语义化：GET 查询、POST 创建、PUT 全量更新、PATCH局部更新、DELETE 删除。（如DELETE/users/1，而非/deleteUser） 3. 无状态：请求包含所有必要信息，不依赖会话；  
4. 统一接口：用标准HTTP 状态码（200 成功、404 未找到）和响应格式； 5. 可缓存：支持GET 请求缓存，提升性能； 6. 资源分层：客户端无需了解服务
---
## Chunk 430 — 优点：URL简洁、方法语义准确、响应格式统一

优点：URL简洁、方法语义准确、响应格式统一
---
## Chunk 431 — 优点：URL简洁、方法语义准确、响应格式统一

12. TCP 的TIME_WAIT 状态 TIME_WAIT 是 TCP 连接关闭时（第四次挥手），主动关闭方在发送最后一个 ACK 后进入的一个等待状态，用于  
1. 确保最后的ACK能被收到（避免被动方重传FIN） 2. 等待网络中延迟的旧数据过期（避免干扰新连接）  
TIME_WAIT 过多通常由于短连接和高并发请求导致。常见优化方案包括：  
第一，通过调整内核参数（如减少 MSL 或开启 tcp_tw_reuse）来缩短 TIME_WAIT 持续时间，但需要注意可能引入旧报文干扰新连接的风险；  
第二，通过端口复用（SO_REUSEADDR）提高端口利用率，但需要保证新旧连接的四元组不同，避免连接混淆；  
第三，使用长连接（Keep-Alive）或连接池，从根本上减少连接的频繁创建与关闭，是最推荐的方案。  
13. 网络IO 模型程序如何等待和处理网络数据的方式，一次网络IO实际执行等待数据到达和把数据拷贝到用户空间，IO模型的区别在于怎么等+谁来通知+是否阻塞  
同步阻塞 (BIO Blocking IO)：BIO 中，线程在 read/write 时会一直阻塞，直到 IO 完成，因此实现简单，但在高并发下需要大量线程，扩展性较差。（如小型TCP 服务器）  
同步非阻塞 (NIO Non-Blocking IO)：同步非阻塞 IO 中，线程不会在单次 read 上阻塞，  
但需要不断轮询数据是否就绪，因此会增加 CPU 开销，适用于低并发、对延迟敏感场景。 IO多路复用 (select/poll/epoll)：一个线程监听多个IO 事件，数据准备好后通知应用层，阻塞于select/poll/epoll，适用于高并发（如百万级连接） ○ select - 有数量限制（1024），每次都要遍历 ○ poll - 无数量限制，仍然遍历 ○ epoll - 事件驱动，不需要便利，高性能，是高并发服务器的基础  
异步IO (AIO)：内核完成数据准备和拷贝后通知应用层，应用层无需阻塞，适用于高并发、低延迟场景（如磁盘IO、网络IO）
---
## Chunk 432 — 优点：URL简洁、方法语义准确、响应格式统一

异步IO (AIO)：内核完成数据准备和拷贝后通知应用层，应用层无需阻塞，适用于高并发、低延迟场景（如磁盘IO、网络IO）  
高并发网络编程优先用IO 多路复用（epoll），磁盘IO 密集场景用异步IO；通过合理选型平衡性  
能和开发复杂度，提升系统并发能力。
---
## Chunk 433 — 优点：URL简洁、方法语义准确、响应格式统一 > 14. select、poll、epoll

优点：URL简洁、方法语义准确、响应格式统一 > 14. select、poll、epoll

select 把所有 fd 放进集合(上线：1024) ↓ 调用 select ↓ 内核遍历所有 fd （O(n)） ↓ 返回“哪些 ready
---
## Chunk 434 — poll 相比select只改进了：没有1024限制

poll 相比select只改进了：没有1024限制

epoll epoll_ctl 注册把 fd 加入内核 ↓ epoll_wait 监听等待事件 ↓ 只返回 ready的fd (O(1))  
LT水平触发：只要有数据就一直通知，开发简单，不容易丢数据，适用于大多数场景 ET边缘触发：仅在就绪状态变化时触发一次，需一次性读完数据，效率高，适用于高并发场景。  
14. DNS 解析 DNS 解析是将域名（如www.qq.com）转换为IP 地址的过程浏览器缓存（客户端先查询本地缓存，命中则返回IP） ↓ 操作系统缓存 ↓ 本地 DNS 服务器（本地DNS 负责全程递归查询） ↓  
根域名服务器（问谁管.com，返回.com的服务器地址） ↓ 顶级域名服务器（问谁管google.com，返回权威DNS地址） ↓ 权威 DNS 服务器 ↓ 返回 IP  
15. TCP 的keep-alive 参数 TCP Keep-Alive 是一种检测连接是否仍然存活的机制，通过定期发送探测包来判断对端是否还在线，从而释放无效链接，防止资源占用。当TCP 连接长时间无数据传输时(idle)，发送探测报文(probe)，若未收到响应则判定连接失效，主动关闭连接，避免资源浪费。关键参数  
1. tcp_keepalive_time 连接多久不活动 → 开始探测 2. tcp_keepalive_intval 两次探测之间的间隔 3. tcp_keepalive_probes 最多探测多少次  
TCP keep-alive 和HTTP keep-alive的区别 TCP keep-alive 释放无效连接，防止僵尸连接。HTTP keep-alive 表示多个 HTTP 请求可以复用同一个 TCP 连接，提升传输效率。同时启用场景：基于HTTP 长连接的服务（如WebSocket、API 网关），需keep-alive检测连接存活，避免长连接失效导致的通信异常。
---
## Chunk 435 — 二、OS 操作系统与进程通讯

二、OS 操作系统与进程通讯

1. 进程与线程进程和线程的本质区别是什么？线程共享进程的哪些资源？又有哪些独立的资源？进程是资源分配单位，线程是调度执行单位，这是核心区别；线程共享进程的核心资源，仅保留执行相关的独立资源，实现轻量级并发。本质区别：进程拥有独立地址空间，线程共享进程地址空间，线程切换开销远低于进程。共享资源：代码段、数据段、堆、文件描述符、信号处理方式等。独立资源：线程栈（存储局部变量）、程序计数器（记录执行位置）、寄存器组（保存执行状态）、线程私有数据（如线程局部存储TLS）。正因为共享资源多，线程通信更高效，但也需同步保护临界资源。  
开发中我会根据并发需求选型，高并发场景用线程减少开销，需资源隔离时用进程；同时做好线程同步，避免共享资源竞争导致的问题。
---
## Chunk 436 — 追问1：为什么线程切换开销比进程小？

追问1：为什么线程切换开销比进程小？
---
## Chunk 437 — 追问1：为什么线程切换开销比进程小？

具体体现在哪些方面？  
进程切换需切换地址空间（更新页表、刷新TLB），而线程共享地址空间，无需此操作；其次线程仅需保存/恢复自身独立资源（栈、寄存器等），数据量远少于进程的完整上下文，因此切换速度更快。  
2. 操作系统的进程调度算法有哪些？  
进程调度算法围绕公平性和效率设计，FCFS、短作业优先、时间片轮转等各有侧重，分别适配批处理、实时、交互式等不同场景。 1. FCFS(先来先服务)：按提交顺序调度，非抢占式，简单但长作业会阻塞短作业，适合批处理 2. 短作业优先（SJF）：优先调度运行时间最短的作业，抢占式可优化平均周转时间，但可能导致长作业饥饿 3. 时间片轮转：为进程分配固定时间片，轮转执行，抢占式，响应快，适合交互式系统 4. 优先级调度：按优先级分配CPU，抢占式，需搭配“老化机制”缓解饥饿，适合实时系统。  
设计并发系统时，我会借鉴调度思想，比如用“优先级+时间片”机制管理任务，通过老化策略避免低优先级任务饥饿，保障系统公平与高效。  
追问：“老化机制”是如何解决优先级调度的饥饿问题的？老化机制会随时间递增低优先级进程的优先级，比如每等待一个时间片，优先级加1。即使是最低优先级进程，等待足够长时间后，优先级也会提升至可被调度，从而避免因长期无法获得CPU 而饥饿。  
3. 死锁什么是死锁？死锁产生的四个必要条件是什么？如何预防和解决死锁问题？死锁定义：多个进程持有部分资源，同时等待对方持有的资源，形成循环等待而无法推进的状态。四个必要条件：互斥、持有并等待、不可剥夺、环路等待。预防措施：按顺序分配资源（破坏环路等待）、一次性申请所有资源（破坏持有并等待）。解决方法：  
1. 检测：用资源分配图判断死锁 ● 2. 恢复：终止优先级低的进程、剥夺部分进程资源，释放后打破循环。  
开发中我会采用“按顺序申请资源”等预防策略，同时在系统中设计死锁检测机制，定期检查资源分配状态，避免死锁导致系统不可用。
---
## Chunk 438 — 追问1：为什么线程切换开销比进程小？

1. 检测：用资源分配图判断死锁 ● 2. 恢复：终止优先级低的进程、剥夺部分进程资源，释放后打破循环。  
开发中我会采用“按顺序申请资源”等预防策略，同时在系统中设计死锁检测机制，定期检查资源分配状态，避免死锁导致系统不可用。  
追问：“按顺序分配资源”为什么能破坏环路等待条件？实际开发中如何落地？按顺序分配要求所有进程按统一资源序号申请，比如资源A 序号1、资源B 序号2，进程必须先申请A 再申请B，无法出现“进程1持B 等A，进程2 持A 等B”的环路。落地时需给系统资源编号，在代码中强制按序号申请，避免乱序请求。  
4. 进程间通信的方式、优缺点及应用场景进程间通信的方式有管道、消息队列、共享内存、信号量、Socket等。进程间通信分数据传输和同步两类，管道、消息队列等侧重数据传输，信号量侧重同步；需根据性能、场景需求选择，共享内存是本地最快方式。优缺点及场景： 1. 匿名管道：优点简单，缺点仅父子进程用，适合本地简单数据传输 2. 消息队列：优点有消息边界，缺点开销比管道大，适合本地非实时数据交换 3. 共享内存：优点速度最快，缺点需同步保护，适合本地高吞吐场景 4. 信号量：无数据传输，用于同步互斥 5. Socket：支持跨网络，缺点开销大，适合跨主机通信。  
开发中本地高并发用共享内存+信号量，简单本地通信用管道，跨网络用Socket；通过合理选型平衡性能与开发成本，确保进程间协作高效可靠。  
追问1：共享内存为什么是最快的IPC 方式？使用时必须搭配什么机制？为什么？共享内存让进程直接访问同一块物理内存，无需内核中转（如管道需拷贝数据到内核缓冲区），省去两次数据拷贝，故速度最快。必须搭配同步机制（如信号量、互斥锁），否则多个进程同时读写会导致数据竞争，破坏数据一致性。
---
## Chunk 439 — 追问1：为什么线程切换开销比进程小？

5. 内存分页，分段机制，虚拟内存请解释内存分页和分段机制的原理，它们的区别是什么？虚拟内存的实现依赖于哪些技术？分页按固定大小拆分物理内存，分段按逻辑模块拆分地址空间，二者定位不同；虚拟内存依赖地址转换、分页等技术，实现内存扩容与隔离。原理与区别：分页：将物理内存和虚拟内存均划分为固定大小页（如4KB），通过页表映射地址，优点内存利用率高，缺点无逻辑关联。分段：按代码、数据等逻辑模块拆分为段，段大小不固定，优点逻辑清晰，缺点易产生内存碎片。虚拟内存依赖技术：虚拟地址与物理地址转换、分页机制、缺页中断（触发页面加载）、交换（页面与磁盘交互）。  
开发中我会关注内存使用效率，比如避免内存碎片（参考分页思想），通过合理分配内存减少缺页次数，提升程序在虚拟内存环境下的性能。  
追问1：分页机制中的“页表”作用是什么？为了解决页表过大的问题，操作系统采用了什么优化方案？页表用于存储虚拟页号到物理页号的映射关系，实现地址转换。优化页表过大的方案是多级页表（如二级、三级），只将常用的页表项加载到内存，不常用的存放在磁盘，减少内存占用；还可结合TLB（快表）加速地址查找。  
6. inode作用，文件的硬链接与软链接 inode 是文件元数据的载体，记录文件大小、权限等信息，文件名通过目录项关联inode。硬链接是 inode 引用，软链接是独立文件，区别显著。  
node 作用：存储文件元数据（权限、大小、创建时间、物理块位置等），每个文件对应唯一inode。硬软链接区别：1. 本质：硬链接是同一inode 的多个目录项，软链接是独立inode（存原文件路径）； 2. 跨文件系统：硬链接不可，软链接可；3. 原文件删除：硬链接仍可用，软链接失效；4.大小：硬链接与原文件相同，软链接存路径故体积小。  
日常开发中，我会用硬链接备份关键配置文件（避免误删），用软链接简化文件访问路径；排查文件问题时，通过ls -i 查看inode，定位重复文件。
---
## Chunk 440 — 追问1：为什么线程切换开销比进程小？

日常开发中，我会用硬链接备份关键配置文件（避免误删），用软链接简化文件访问路径；排查文件问题时，通过ls -i 查看inode，定位重复文件。  
追问1：为什么删除原文件后，硬链接仍能正常访问文件内容？文件的删除本质是减少inode 的引用计数。创建硬链接时，inode 引用计数加1；删除原文件时，引用计数减1 但未到0，inode 及对应数据块仍存在，硬链接作为有效引用，自然能通过inode 访问文件内容，直到所有硬链接都被删除，引用计数为0 才释放资源。
---
## Chunk 441 — 追问1：为什么线程切换开销比进程小？ > 7. 临界区 "什么是临界区？

追问1：为什么线程切换开销比进程小？ > 7. 临界区 "什么是临界区？

如何保证多个线程对临界区资源的安全访问？（请举例说明实现方式）  
临界区是访问共享资源的代码段，多线程并发访问易导致数据不一致；需通过互斥、原子操作等机制保证安全，常用锁和信号量实现。  
1. 互斥锁（如Java 的synchronized）：线程进入临界区前获取锁，执行完释放，未获取到则阻塞，适合复杂临界区 2. 自旋锁：线程获取不到锁时循环等待，不放弃CPU，适合临界区执行时间短的场景；3. 原子操作（如C++的std::atomic）：通过CPU 指令保证操作原子性，无需锁，适合简单变量修改（如计数器递增）。开发中我会根据临界区特性选型，简单操作用原子类，复杂逻辑用互斥锁；同时避免锁粒度过大，通过细粒度锁减少线程阻塞，提升并发效率。  
追问：自旋锁和互斥锁的核心区别是什么？为什么“临界区执行时间短”适合用自旋锁？核心区别是获取不到锁时的行为：自旋锁循环等待（忙等），互斥锁阻塞线程（放弃CPU）。临界区执行时间短时，自旋等待的时间远小于线程阻塞-唤醒的开销，用自旋锁能减少上下文切换，提升效率；若执行时间长，自旋会浪费CPU 资源，此时互斥锁更合适。  
8. 信号量和互斥锁 38. "信号量和互斥锁的区别是什么？它们在进程同步和互斥中分别起到什么作用？" 互斥锁是信号量的特殊情况（计数=1），核心用于互斥；信号量通过计数实现同步与互斥，功能更灵活，二者定位和作用有明确区分。区别与作用：1. 核心区别：互斥锁有所有权（获锁线程才能释放），信号量无；互斥锁计数固定为1，信号量可设任意非负整数。2.作用：互斥锁：保证临界区资源独占访问，解决互斥问题（如多线程操  
作同一文件）；信号量：计数为1 时可实现互斥，计数>1 时实现同步（如控制并发访问资源的线程数，或协调生产消费顺序）。  
开发中我会精准选型，资源独占用互斥锁（避免误释放），控制并发数或协调顺序用信号量；通过明确使用场景，确保同步互斥逻辑清晰可靠。
---
## Chunk 442 — 追问1：用信号量实现生产者-消费者模型时，需要几个信号量？

追问1：用信号量实现生产者-消费者模型时，需要几个信号量？

分别起到什么作用？需要3 个信号量：1. 空缓冲区信号量（初值为缓冲区大小）：控制生产者不会向满缓冲区生产；2. 满缓冲区信号量（初值为0）：控制消费者不会从空缓冲区消费；3. 互斥信号量（初值为1）：保证生产者和消费者对缓冲区的操作互斥，避免数据竞争。  
9. 缓冲区操作系统的IO 子系统中，缓冲区的作用是什么？请解释缓冲区溢出的危害及预防措施。  
缓冲区用于匹配IO 设备与CPU 的速度差异，减少IO 次数；缓冲区溢出会导致程序崩溃或被恶意攻击，需从输入校验等多方面预防。缓冲区作用：1. 速度匹配：缓和CPU 高速与IO 设备低速的矛盾；2. 减少IO：积累数据批量读写，降低IO 操作开销；3. 数据整理：实现数据的拼接与拆分。溢出危害：覆盖程序计数器、栈帧等关键内存，导致程序崩溃，甚至被注入恶意代码（如缓冲区溢出攻击）。预防措施：1. 严格校验输入长度；2. 用编译器保护（如GS 编译选项）；3. 用安全语言（如Java）或安全函数（如strncpy 替代strcpy）。  
开发中我会优先用安全编程接口，对所有输入做长度和合法性校验；编译时开启安全选项，从编码和编译层面双重预防缓冲区溢出风险。
---
## Chunk 443 — 追问1：为什么用strncpy 比strcpy 更安全？

追问1：为什么用strncpy 比strcpy 更安全？
---
## Chunk 444 — 追问1：为什么用strncpy 比strcpy 更安全？

但使用strncpy 仍可能存在缓冲区溢出风险吗？ strcpy 会一直复制直到遇到'\0'，若源字符串长度超过目标缓冲区，必然溢出；strncpy 可指定最大复制长度，避免无限复制，故更安全。但仍有风险：若指定的长度大于目标缓冲区大小，或复制后未手动添加'\0'导致字符串截断异常，仍可能引发问题，需结合缓冲区大小精准设置复制长度。  
10. Linux系统中程序从编译到运行的完整过程 "请描述Linux 系统中，一个程序从编译到运行的完整过程，涉及到哪些操作系统机制？" 程序从编译到运行分五个阶段，预处理到链接由编译器完成，加载运行依赖操作系统的进程管理、虚拟内存等机制，协同实现程序执行。完整过程：1. 预处理：gcc -E 展开宏、包含头文件，生成.i 文件 2. 编译：将.i 文件编译为汇编代码（.s），做语法语义分析 3.汇编：将.s 文件转为机器码（.o） 4. 链接：ld 链接器将.o 与库文件合并，生成可执行文件。运行阶段：OS 通过fork 创建进程， execve 加载可执行文件到虚拟内存，分配资源；进程调度器分配CPU，程序开始执行，涉及IO 重定向（如标准输出）等机制。  
开发中我会利用编译链接知识优化程序（如静态链接减少依赖），结合OS 机制调优运行性能（如合理设置进程优先级），提升程序的可移植性与效率。  
“静态链接”和“动态链接”的区别是什么？操作系统在动态链接中起到什么作用？静态链接将库代码嵌入可执行文件，体积大但不依赖外部库；动态链接仅记录库引用，运行时才加载库文件，体积小但需依赖系统库。OS 在动态链接中负责：加载程序时定位并加载所需动态库，解析库函数地址，建立映射，确保程序能正确调用库接口。  
11. Top、ps、netstat、df等命令 Linux 系统中，top、ps、netstat、df 等命令的常用参数和作用是什么？如何用这些命令排查系统问题？
---
## Chunk 445 — 追问1：为什么用strncpy 比strcpy 更安全？

11. Top、ps、netstat、df等命令 Linux 系统中，top、ps、netstat、df 等命令的常用参数和作用是什么？如何用这些命令排查系统问题？  
这些命令是Linux 系统排查的核心工具，top 查进程资源，ps 列进程，netstat 看网络，df 查磁盘；需结合问题场景选择，形成完整排查链路。常用参数及排查：1. top：-p 查指定进程，%CPU 列定位高负载进程，排查CPU 飙升问题 2. ps：aux 列所有进程，grep 过滤目标进程，排查进程是否存活 3. netstat：-tuln 看监听端口，-an 看连接状态，排查端口占用或连接异常 4. df：-h 人性化显示磁盘占用，排查磁盘满导致的服务异常 5. 组合排查：top 发现CPU 高→ps 定位进程→netstat 看该进程网络连接。  
工作中我会用这些命令快速定位问题，比如服务起不来时，先用netstat 查端口是否被占，再用ps 看进程状态，高效排查故障，缩短服务恢复时间。  
用top 命令发现某个进程CPU 使用率持续100%，接下来如何排查具体是哪个函数导致的？ 1. 记录进程PID（如1234） 2. 用ps -mp1234 -o THREAD,tid,time 查看进程下高CPU 的线程TID 3. 将TID 转为十六进制（printf "%x\n" TID） 4. 用pstack 1234 | grep 十六进制TID，查看该线程的调用栈，定位到具体函数 5. 结合代码分析函数逻辑，找出CPU 高的原因（如死循环）。  
12. 进程的上下文切换什么是进程的上下文切换？上下文切换的开销主要体现在哪些方面？如何减少上下文切换？  
上下文切换是CPU 保存当前进程状态、加载新进程状态的过程，开销体现在多方面；减少切换需从进程管理、调度等层面综合优化。开销体现：1. 时间开销：保存/恢复寄存器、程序计数器等状态； 2. 资源开销：内核占用CPU 处理切换；3. 缓存失效：新进程替换缓存，导致缓存命中率下降。
---
## Chunk 446 — 追问1：为什么用strncpy 比strcpy 更安全？

减少方法：1. 用线程替代进程（线程切换开销低）；2. 合理设置线程池大小（避免过多线程竞争）；3. 优化锁机制（如用自旋锁减少阻塞）；4. 调整进程优先级，避免频繁抢占。开发中我会合理设计并发模型，用线程池控制并发数，通过细粒度锁减少线程阻塞；同时关注系统调度状态，避免不必要的上下文切换，提升性能。
---
## Chunk 447 — 追问1：为什么线程上下文切换的开销比进程小？

追问1：为什么线程上下文切换的开销比进程小？

具体小在哪些环节？  
因为线程共享进程的地址空间，而进程有独立地址空间。线程切换无需切换地址空间（省去更新页表、刷新TLB 的开销），仅需保存/恢复线程自身的独立资源（栈、寄存器、程序计数器），这些数据量远少于进程的完整上下文（包含地址空间信息），因此切换开销显著降低。
---
## Chunk 448 — 三、数据结构与算法

三、数据结构与算法

1. 数组与链表数组和链表的区别是什么？在实际开发中如何根据场景选择使用数组或链表？  
数组和链表的核心区别在存储结构，数组连续存储支持随机访问，链表离散存储适合灵活增删  
具体区别：数组内存连续，可通过下标O(1)随机访问，增删中间元素需移动数据（O(n)），栈/堆均可分配，内存碎片少。链表节点离散，靠指针关联，只能顺序访问（O(n)），增删节点仅改指针（O(1)），仅存堆上，易产生碎片。查多改少用数组（如配置列表），增删频繁且在首尾用链表（如消息队列）。
---
## Chunk 449 — Java 中的ArrayList 和LinkedList 分别对应数组和链表，为什么遍历LinkedList 时用迭代器比 for 循环快？

Java 中的ArrayList 和LinkedList 分别对应数组和链表，为什么遍历LinkedList 时用迭代器比 for 循环快？

LinkedList 用for 循环遍历会通过get(i)每次从头节点开始查找（O(n)），n 次遍历总复杂度O(n²)；迭代器通过指针记录当前节点，每次next()仅移动一步（O(1)），总复杂度O(n)，因此迭代器更高效。  
2. 单链表的反转，环检测，中间节点查找这三个操作均可通过指针控制实现，环检测和中间节点查找用快慢指针能优化空间，反转需关注前驱节点的保存，均要处理空链表等边界。  
反转：初始化前驱null、当前节点为头节点，循环中用临时变量存后继节点，再将当前节点指针指向前驱，依次移动三者，最终前驱为新头。环检测：快慢指针同时从头出发，快指针每次走两步，慢指针一步，若相遇则有环。中间节点：快慢指针同起点，快指针到尾时，慢指针恰好到中间（偶数节点取左中），均需先判断头节点是否为null。
---
## Chunk 450 — 环检测中，快慢指针相遇后，如何找到环的入口节点？

环检测中，快慢指针相遇后，如何找到环的入口节点？

相遇后将慢指针重置为头节点，快慢指针改为每次都走一步，再次相遇的节点就是环入口。原理是相遇时快指针走的距离是慢指针的2 倍，通过距离公式可推导出头节点到入口的距离等于相遇点到入口的距离。  
3. 栈和队列 45. "栈和队列的定义及特点是什么？请用数组或链表实现一个栈和一个队列。" 栈是先进后出的线性结构，队列是先进先出的线性结构；数组实现栈高效，链表实现队列灵活，均需处理边界和操作逻辑。  
栈仅允许栈顶操作（push/pop），队列仅允许队尾入、队头出（enqueue/dequeue）。数组实现栈：用下标top 记录栈顶，push 时top++存值，pop 时返回top--对应值，满时扩容（如2 倍）。链表实现队列：设头尾指针，enqueue 时尾指针指向新节点，dequeue 时头指针后移，空时返回异常，无需考虑扩容。  
开发中我会按需选择，高频操作的用数组栈（如表达式计算），动态增删的用链表队列（如任务排队）；同时添加空判断，避免操作异常。
---
## Chunk 451 — 追问1：用两个栈如何实现一个队列？

追问1：用两个栈如何实现一个队列？

核心逻辑是什么？用“入栈”和“出栈”两个栈实现。enqueue 时直接压入入栈；dequeue 时若出栈为空，将入栈所有元素弹出并压入出栈（反转顺序），再从出栈弹出顶部元素，这样就模拟了队列的先进先出特性。  
4. 哈希表哈希表的实现原理是什么？如何解决哈希冲突？常见的哈希函数有哪些？  
哈希表通过“键-哈希值-地址”的映射快速存取数据。哈希表实现原理：用哈希函数将键转换为哈希值，通过取模等方式映射到数组下标（存储地址），实现O(1)的存取。  
冲突解决： 1. 链地址法：数组下标对应链表，冲突键存链表中 2. 开放定址法：冲突时按规则找下一个空地址（如线性探测）。常见哈希函数：直接定址法（键直接作地址）、除留余数法（键%素数）、折叠法（键分段相加）。  
设计哈希表时，我会选素数作为数组大小，用链地址法解决冲突（易实现），搭配除留余数法哈希函数，控制负载因子在0.7 以下减少冲突。
---
## Chunk 452 — 追问1：链地址法和开放定址法相比，各自的优缺点是什么？

追问1：链地址法和开放定址法相比，各自的优缺点是什么？

什么场景下选开放定址法？链地址法优点是冲突处理简单、负载因子高时仍高效，缺点是需额外存储指针；开放定址法优点是内存连续、无指针开销，缺点是易产生聚集（如线性探测）、删除需标记。内存紧张且数据量不大时，选开放定址法更合适。  
5. 二叉树二叉树的前序、中序、后序遍历的递归和非递归实现方法是什么？三种遍历的核心是根节点访问时机不同，递归实现依赖递归栈，非递归需手动用栈管理节点，需明确入栈出栈逻辑和边界处理。递归实现：前序（根→左→右）、中序（左→根→右）、后序（左→右→根），均先判断节点是否为null，再按顺序递归左右子树。非递归：前序先压右子树再压左子树（栈先进后出），弹出即访问；中序先压左子树，左空后弹出访问根，再压右子树；后序用栈存节点和访问标记，未访问则标已访问并压右左子树，已访问则弹出。实现时我会先写递归（简洁易读），非递归用注释标注“压栈顺序原因”（如前序压右左是为了左先弹出）；同时处理空树，确保代码健壮。
---
## Chunk 453 — 追问1：已知二叉树的前序和中序遍历结果，如何重建该二叉树？

追问1：已知二叉树的前序和中序遍历结果，如何重建该二叉树？

核心逻辑是什么？核心逻辑是前序首元素为根节点，中序中根节点左侧是左子树、右侧是右子树。通过前序确定根，中序划分左右子树范围，再递归重建左子树（前序左段+中序左段）和右子树（前序右段+中序右段），需处理空树和单节点情况。  
6. 二叉搜索树什么是二叉搜索树？它的查找、插入、删除操作的时间复杂度是多少？  
二叉搜索树是左子树节点值≤根≤右子树节点值的二叉树，中序遍历为升序；操作复杂度依赖树高，平衡时高效，失衡时性能下降。定义：左子树所有节点值不大于根，右子树所有节点值不小于根，且左右子树均为BST。操作：查找时按值与根比较，小则查左、大则查右。插入时类似查找，找到空位置插入。删除时，叶子节点直接删，单孩子节点用孩子替代，双孩子节点用中序后继（右子树最小）替代。平衡时时间复杂度O(logn)，失衡（如链状）时O(n)。  
开发中若用BST，我会关注树的平衡，避免插入有序数据导致失衡；若需稳定性能，会选择红黑树等平衡BST，确保操作复杂度稳定在O(logn)。
---
## Chunk 454 — 二叉搜索树中，“中序后继”指什么？

二叉搜索树中，“中序后继”指什么？

如何快速找到一个节点的中序后继？中序后继是中序遍历中该节点的下一个节点。查找方法：1. 若节点有右子树，后继是右子树的最左节点（右子树中最小节点）；2. 若无右子树，向上追溯祖先，找到第一个“该节点是其左子树”的祖先，该祖先即为后继，若无则无后继。  
7. 红黑树，AVL树红黑树的核心特性是什么？它与AVL 树的区别是什么？红黑树的插入和删除过程是怎样的？  
红黑树是通过颜色规则保证近似平衡的BST，核心特性约束树高，与AVL 树平衡标准不同；插入删除靠变色和旋转调整，旋转频率更低。核心特性：1. 节点非红即黑；2. 根和叶子（NIL）为黑；3. 红节点子节点为黑；4. 任意节点到叶子的黑节点数相同。与AVL 树区别：AVL 树按高度差（≤1）严格平衡，旋转多；红黑树按颜色规则近似平衡，旋转少。插入删除：先按BST 操作，再通过变色（优先）和旋转（左/右/双旋）修复颜色违规，维持特性。  
开发中我会根据场景选树，需要稳定查找性能的用AVL树，增删频繁的用红黑树（旋转少效率高）；理解其调整逻辑，避免使用时因特性破坏导致问题。
---
## Chunk 455 — 追问1：红黑树的“黑高”是什么？

追问1：红黑树的“黑高”是什么？

为什么说红黑树的高度不会超过2log₂(n+1)？黑高是节点到叶子节点的路径上黑色节点的数量（含自身）。根据特性，任意路径的黑高相同，且红色节点不相邻，最长路径（红黑交替）的长度不会超过最短路径（全黑）的2 倍，而最短路径长度为黑高h，故树高≤2h，结合节点数与黑高的关系可推导出高度上限。  
8. B树和B+树 B 树和B+树的结构及特点是什么？为什么数据库索引通常使用B+树？ B 树和B+树都是多叉平衡树，核心区别在数据存储位置和叶子节点特性；B+树因适配磁盘IO 和范围查询，成为数据库索引的首选。结构特点：m 阶B 树每个节点最多m 个子节点、存m-1个数据，非叶子和叶子都存数据；m 阶B+树非叶子仅存索引（指引子节点），叶子节点存全部数据且按顺序双向连接（叶子结点之间是双向链表）。数据库选型原因：1. 树高矮（多叉），减少磁盘IO（一次读一个节点）；2. 叶子有序连接，范围查询（如between）无需回溯；3. 索引与数据分离，查询更高效。  
设计数据存储系统时，我会借鉴B+树思想，比如日志索引用B+树结构，通过有序叶子节点优化范围查询；同时控制节点大小匹配磁盘页，减少IO 开销。  
B 树和B+树在单值查询时性能差异不大，为什么范围查询B+树更有优势？ B 树范围查询时，找到起始数据后，需回溯父节点找下一个数据的位置（因非叶子节点存数据，叶子节点无序）；而B+树叶子节点按顺序双向连接，找到起始数据后，直接沿叶子节点链表依次遍历即可获取所有范围内数据，无需回溯，效率显著更高。  
9. 各种排序算法（冒泡，选择，插入，快排，归并，堆排） 1. 交换类：冒泡（时间O(n²)/O(n)，空间O(1)，稳定），相邻比较，大的往后“冒”（swap）快排（O(nlogn)/O(n²)，O(logn)，不稳定）
---
## Chunk 456 — 追问1：红黑树的“黑高”是什么？ > 2. 插入类：

追问1：红黑树的“黑高”是什么？ > 2. 插入类：

插入（O(n²)/O(n)，O(1)，稳定）。维护一个“已排序区间”（左边），每次取一个新元素，向前
---
## Chunk 457 — 追问1：红黑树的“黑高”是什么？ > 3. 选择类：

追问1：红黑树的“黑高”是什么？ > 3. 选择类：

选择（O(n²)，O(1)，不稳定）。每一轮：在未排序区间找最小值，然后和当前起点交换堆排（O(nlogn)，O(1)，不稳定）。先建一个大顶堆(O(n))，然后把堆顶（最大值）和最后一  
个元素交换，再对根节点重新 heapify（下沉），下沉n次每次logn，所以一共是O(nlogn) 4. 归并（O(nlogn)，O(n)，稳定）  
开发中我会按数据场景选型，小数据用插入排序（简单高效），大数据用快排（平均性能好），需稳定排序的用归并排序；避免在大数据场景用冒泡等低效算法。
---
## Chunk 458 — 追问1：为什么快排的平均时间复杂度是O(nlogn)，但最坏会退化到O(n²)？

追问1：为什么快排的平均时间复杂度是O(nlogn)，但最坏会退化到O(n²)？

如何避免这种退化？快排通过基准值划分区间，平均每次将数组分为两等份，递归深度O(logn)，每层操作O(n)，故平均O(nlogn)；若基准值选极值（如有序数组选首元素），划分后区间为1 和n-1，递归深度O(n)，退化到O(n²)。避免方法：随机基准值，减少极值选择概率。  
10. 实现快排，解释优化思路快排核心是“基准划分+递归排序”，通过优化基准值和处理重复元素提升性能，实现时需明确划分逻辑和递归边界。 1. 递归边界：若low≥high 直接返回；2.选基准值（如三数取中法：取low、mid、high 对应值的中值，交换到low 位置）；3. 双路划分：左指针找比基准大的，右指针找比基准小的，交换后继续，直到指针相遇，将基准值放到分界处；4. 递归排序左右区间。优化：重复元素用三路快排（分小于、等于、大于三区），避免重复元素聚集；递归深度大时改用堆排。
---
## Chunk 459 — 追问1：三路快排的核心思想是什么？

追问1：三路快排的核心思想是什么？
---
## Chunk 460 — 追问1：三路快排的核心思想是什么？

相比双路快排，它在处理重复元素时有什么优势？三路快排将数组分为“小于基准”“等于基准”“大于基准”三个区间，核心是用两个指针lt 和gt 分别标记小于区的尾和大于区的头，遍历数组时将元素归到对应区间。优势：重复元素集中在“等于区”，无需参与后续递归排序，减少递归处理的数据量，避免双路快排中重复元素分散导致的多次划分，提升性能。  
11. 动态规划动态规划是通过存储子问题最优解解决复杂问题的方法，核心是利用重叠子问题和最优子结构； LIS 问题可用DP 高效求解，分基础和优化解法。  
DP 定义：将问题拆为重叠子问题，存储子问题最优解（避免重复计算），通过最优子结构推导全局最优。LIS 解法：1. 基础O(n²)：状态dp[i]为以i 结尾的LIS 长度，转移方程dp[i] = max(dp[j]+1)（j<i 且nums[j]<nums[i]），初始化dp[i]=1，结果取max(dp)；2. 优化O(nlogn)：用数组tails 存LIS，遍历nums 时二分找插入位置，tails 长度即LIS 长度。解决DP 问题时，我会先明确状态定义（如LIS 的dp[i]含义），再推导转移方程；复杂问题先写基础解法，再结合场景优化时间空间，提升效率。  
追问1：0-1 背包问题和完全背包问题的核心区别是什么？它们的动态规划转移方程有何不同？核心区别是物品是否可重复选取：0-1 背包物品仅选一次，完全背包物品可选多次。0-1 背包转移方程：dp[j] = max(dp[j], dp[j-weight[i]]+value[i])，遍历背包容量需从大到小（避免重复选）；完全背包转移方程相同，但容量从左到右遍历（允许重复选）。
---
## Chunk 461 — 追问1：三路快排的核心思想是什么？

12. 贪心算法、它与动态规划的区别贪心算法是每次选局部最优解以推导全局最优的方法，需满足贪心选择性质；它与动态规划的核心区别在子问题处理和适用前提。定义：贪心需满足“贪心选择性质”（局部最优可导出全局最优）和最优子结构。与DP 区别：1. 子问题：DP 处理所有重叠子问题，贪心仅选当前子问题最优，不回溯；2. 前提：DP 无特殊前提，贪心需满足贪心选择性质；3. 效率：贪心更高（O(n)或O(nlogn)），DP 相对低。应用场景：活动选择（选最多不重叠活动）、哈夫曼编码（最优前缀码）、零钱兑换（面额满足贪心条件时）。  
开发中我会先判断问题是否满足贪心条件，如活动排期用贪心（选结束早的）；不满足时用DP（如普通零钱兑换），避免因误用贪心导致结果错误。
---
## Chunk 462 — 为什么“活动选择问题”能用贪心算法解决，而“旅行商问题”不能？

为什么“活动选择问题”能用贪心算法解决，而“旅行商问题”不能？
---
## Chunk 463 — 为什么“活动选择问题”能用贪心算法解决，而“旅行商问题”不能？

核心原因是什么？参考回答：面试官您好，活动选择问题满足贪心选择性质：选当前结束最早的活动，剩余时间最多，可容纳更多活动，局部最优能导出全局最优。旅行商问题（找经过所有城市的最短回路）不满足该性质：当前选最近的下一个城市，可能导致后续路线极长，局部最优无法导出全局最优，故需用动态规划或其他算法，不能用贪心。  
13. BFS与DFS DFS 和BFS 是图遍历的基础算法，DFS 用栈或递归实现深度优先，BFS 用队列实现广度优先，均需通过访问标记避免重复访问。DFS 优先访问当前节点的邻接节点，直到无未访问邻接节点再回溯。BFS 按“层”遍历，先访问当前节点的所有邻接节点，再依次访问邻接节点的邻接节点，用队列实现。实现关键：用数组visited 标记访问状态（true 为已访问），基于邻接表遍历（如节点u 的邻接表是所有相连节点v）。开发中我会按需选择，找路径是否存在用DFS（递归简洁），找最短路径（无权图）用BFS；实现时先初始化访问标记，避免因未标记导致死循环。  
追问1：在无向图中，如何用DFS 判断图中是否存在环？核心逻辑是什么？核心逻辑是追踪“父节点”，避免将回边误认为环。DFS 遍历中，对当前节点u 的邻接节点v：1. 若v 未访问，标记v 的父节点为u，递归遍历v；2. 若v 已访问且v 不是u 的父节点，说明存在环（u-v 是回边，形成环）。遍历结束未发现则无环。  
14. Dijkstra算法，Flyod算法什么是迪杰斯特拉算法和弗洛伊德算法？它们分别用于解决什么问题？时间复杂度是多少？  
迪杰斯特拉解决单源最短路径（从一个起点到所有节点），弗洛伊德解决多源最短路径（所有节点对之间），两者时间复杂度和适用场景不同。迪杰斯特拉：核心是“选未确定最短路径的节点中距离最小的，松弛其邻接边”，用邻接矩阵时间 O(n²)，邻接表+优先队列O(mlogn)，不能处理负权边（会导致松弛错误）。弗洛伊德：核心是“动态规划，通过中间节点k 更新i 到j 的最短路径”，时间O(n³)，可处理负权边（不能有负权环），实现简洁。
---
## Chunk 464 — 为什么“活动选择问题”能用贪心算法解决，而“旅行商问题”不能？

开发中我会按场景选型，单源且无负权用迪杰斯特拉（邻接表+优先队列高效），多源或有负权用弗洛伊德；避免在负权边场景用迪杰斯特拉导致结果错误。
---
## Chunk 465 — 为什么迪杰斯特拉算法不能处理含负权边的图？

为什么迪杰斯特拉算法不能处理含负权边的图？

如何修改算法使其能处理负权边？迪杰斯特拉算法假设“已确定最短路径的节点不会再被松弛”，但负权边会打破该假设（如已确定的节点u，其邻接边有负权，后续节点v 的更短路径可能通过u）。修改方法用贝尔曼-福特算法，通过n-1 次松弛所有边，可处理负权边；或用SPFA 算法（贝尔曼-福特的队列优化）提升效率。  
15. Top K问题在海量数据处理场景中，如何利用哈希分治、堆排序等思想解决“Top K”问题？  
海量数据Top K 问题无法一次性加载内存，需用哈希分治拆分数据，结合堆排序筛选局部和全局 Top K，核心是“分而治之+高效筛选”。解决步骤：1. 哈希分治：用哈希函数（如取模）将海量数据均匀分片到多个小文件（如1000 个），确保相同数据在同一文件，单个文件可加载内存；2. 局部Top K：对每个小文件，用小根堆（容量K）筛选TopK（遍历数据，比堆顶大则替换堆顶并调整）；3. 全局Top K：收集所有小文件的Top K，用小根堆再次筛选，最终堆内元素即为全局Top K。  
处理时我会优化哈希函数（选素数模）避免数据倾斜，若某文件仍过大则二次分片；用小根堆而非大根堆（减少调整次数），提升筛选效率。
---
## Chunk 466 — 如果海量数据中存在大量重复元素，如何优化上述方案进一步提升效率？

如果海量数据中存在大量重复元素，如何优化上述方案进一步提升效率？

可在哈希分治后增加“计数”步骤：对每个小文件，先用哈希表统计元素出现次数（键为元素，值为次数），再基于次数筛选Top K（此时比较的是次数而非元素本身）。这样避免重复遍历相同元素，减少堆调整次数；同时计数后数据量更小，进一步提升内存利用率和处理速度。
---
## Chunk 467 — 四、数据库

四、数据库

1. MySQL 的存储引擎 MySQL 是一个数据库管理系统。InnoDB 和 MyISAM 是 MySQL 里两种不同的表存储方式。存储引擎决定的是：这张表的数据怎么存到磁盘，查询的时候怎么找，更新的时候怎么改，多个人同时操作时怎么协调，出故障时能不能恢复
---
## Chunk 468 — 事务（一组操作要么全部成功要么全部失败，防止数据出错）

事务（一组操作要么全部成功要么全部失败，防止数据出错）

支持（数据库把两步看作一个整体，要么全部执行成功，要么一步失败就全部撤回） commit提交：正式生效 rollback回滚：撤销改动
---
## Chunk 469 — ✅（InnoDB 会记“操作痕迹”，所以出错后更容易恢复）

✅（InnoDB 会记“操作痕迹”，所以出错后更容易恢复）

❌
---
## Chunk 470 — ✅，因为InnoDB有日志（redo log，undo log）

✅，因为InnoDB有日志（redo log，undo log）

❌  
了，能不能尽量把数据恢复到正确状态）
---
## Chunk 471 — 数据储存

数据储存

聚簇索引（数据和索引存储在同一B+树，叶子节点存完整数据行，查找效率更高）
---
## Chunk 472 — 非聚簇索引（叶子节点存数据行指针，需二次查找数据）

非聚簇索引（叶子节点存数据行指针，需二次查找数据）

2. MySQL的索引类型索引 = 快速定位数据的有序结构，默认基于B+树实现主键索引：唯一、非空、聚簇索引二级索引：非主键字段的索引，用非主键字段找到主键，再用主键索引找整行数据（回表）联合索引：多字段组合建索引，遵循最左前缀。最左前缀原则指联合索引（a,b,c）仅对“a”，“a,b”， “a,b,c”的查询条件生效，不满足则索引失效（如“b”“b,c”查询）。若查询条件含最左前缀但中间字段缺失（如“a,c”），仅a 字段索引生效，c字段需全表扫描。
---
## Chunk 473 — 非聚簇索引（叶子节点存数据行指针，需二次查找数据） > 3. 索引失效索引失效 = MySQL 没用索引，而是走了全表扫描

非聚簇索引（叶子节点存数据行指针，需二次查找数据） > 3. 索引失效索引失效 = MySQL 没用索引，而是走了全表扫描

SQL SELECT * FROM user WHERE name = 'Alice'; --索引 SELECT * FROM user WHERE name LIKE '%Alice'; --全表扫描  
1. 函数操作索引字段（如where DATE(create_time)='2024'） 2. 隐式类型转换（字符串索引配数字值） 3. like%前缀（如like '%name'） 4. or 连接未索引字段 5. 联合索引不满足最左前缀避免方法：避免索引字段函数操作、显式类型转换、用like xxx%或覆盖索引、避免OR，用UNION 建立索引、按最左前缀设计查询。  
4. MySQL 的事务隔离级别事务隔离 = 多个事务同时操作数据库时，如何避免互相干扰三个经典并发问题  
1. 脏读 (Dirty Read)：读到了别人还没提交的数据 2. 不可重复读 (Non-Repeatable Read)：同一个事务里，两次读同一条数据，结果不同 3. 幻读 (Phantom Read)：同一个事务里，两次查询“行数”不同
---
## Chunk 474 — 四种隔离级别（从低到高）

四种隔离级别（从低到高）

1. 读未提交 (Read Uncommitted, RU) 可以读未提交数据，存在脏读/不可重复读/幻读  
2. 读已提交 (Read Committed, RC) 只能读已提交数据，解决脏读 3. 可重复读（RR）：同一事务内读取结果一致，解决前两者，允许并发，性能高  
a. MVCC 多版本并发控制，每个事物看到的是一个历史快照，就算别人改了数据看
---
## Chunk 475 — 到的还是旧版本

到的还是旧版本

b. Next-Key Lock 间隙锁+行锁，防止别人插入新数据 4. 串行化 (Serializable)：事务一个个执行，解决所有问题，性能低。  
事务隔离级别用于控制多个事务并发执行时彼此可见的数据范围，从而避免并发问题。常见并发问题包括：脏读，即读到其他事务未提交的数据；不可重复读，即同一事务中两次读取同一行结果不同；幻读，即同一事务中两次范围查询得到的记录数不同。  
MySQL 常见的四种隔离级别从低到高依次是：Read Uncommitted、Read Committed、 Repeatable Read 和 Serializable。RU 允许读取未提交数据，三种问题都可能发生；RC 只能读已提交数据，解决脏读；RR 在 MySQL InnoDB 中是默认级别，利用 MVCC 保证快照读一致，并结合 Next-Key Lock 在当前读场景下避免幻读；Serializable 则通过事务一个个执行解决所有并发问题，但性能最差。  
其中 MVCC 的核心思想是为数据保留多个版本，让事务读取自己开始时可见的快照版本； Next-Key Lock 是行锁和间隙锁的组合，用来防止其他事务在查询范围内插入新记录。
---
## Chunk 476 — 到的还是旧版本 > 5. MySQL 的锁机制按粒度分

到的还是旧版本 > 5. MySQL 的锁机制按粒度分

表锁：锁整张表，实现简单，并发差 ● 行锁：锁某一行，并发高，更精细。InnoDB 的行锁是基于索引实现的。如果没有索引， MySQL不知道哪一行是target，因此需要一行行扫描+一行行加锁，结果等于把表锁
---
## Chunk 477 — 按模式分

按模式分
---
## Chunk 478 — 按模式分

共享锁 (S锁 Shared lock)：读锁，多个事务可以同时加，只能读，不能写 ● 排他锁 (X锁 exclusive lock)：写锁，只能一个事务持有，其他全部阻塞。SELECT... FOR UPDATE 会将查询从快照读转为当前读，并对命中的记录加排他锁（X锁）  
6. MVCC（多版本并发控制）机制 MVCC 是InnoDB 实现非阻塞读的核心机制。通过数据的多个版本，让读操作不加锁也能保证一致性。实现原理  
1. 每行数据含事务ID（DB_TRX_ID）和回滚指针（DB_ROLL_PTR） 2. 数据修改时，旧版本写入undo 日志，形成版本链 3. 事务开启时生成Read View，通过事务ID 判断版本链中数据是否可见（仅读已提交或未开始的事务数据）  
作用：实现快照读，读写不冲突，提升并发性能。
---
## Chunk 479 — 按模式分

作用：实现快照读，读写不冲突，提升并发性能。  
7. SQL 语句的优化方法 SQL 优化 = 减少扫描数据量+减少 IO 次数 1. 索引优化：select from order where user_id=100 优化为给user_id 建索引。合理设计索引，例如对高频查询字段建立索引，避免全表扫描。同时可以利用联合索引减少回表次数，甚至通过覆盖索引直接在索引中完成查询。 2. 避免索引失效：在 SQL 编写时需要避免索引失效，例如不要对索引字段进行函数操作，不要发生隐式类型转换，避免 LIKE 以% 开头，以及遵循联合索引的最左前缀原则。 select from user where DATE(create_time)='2024' 优化为 select from user where create_time between '2024-01-01' and '2024-01-02' 3. 限制返回字段：select * 改为 select id,name，减少数据传输 4. 用explain 分析执行计划，重点关注是否走索引（type 是否为 index 或 range），定位全表扫描（type=ALL）为什么索引能优化性能？索引可以将全表扫描转化为基于 B+树的快速定位，从 O(n) 降低到 O(log n)。  
8. MySQL 的主从复制机制 MySQL 主从复制 = 主库把所有写操作记录到 binlog（操作日志），从库把这些操作重新执行一遍，解决单机数据库在性能（CPU/IO/连接数有限）、可用性和扩展性方面的瓶颈，通过读写分离提升读性能（主写，从读），通过多副本实现容灾（主库挂了从库可以顶上）和高可用。流程  
1. 主库修改数据+把这条操作写入binlog 2. 从库启动一个IO Thread连接主库，持续读取binlog写到本地 3. 从库SQL Thread读取relay log，执行里面的SQL，使从库数据=主库数据  
复制类型
---
## Chunk 480 — 按模式分

1. 主库修改数据+把这条操作写入binlog 2. 从库启动一个IO Thread连接主库，持续读取binlog写到本地 3. 从库SQL Thread读取relay log，执行里面的SQL，使从库数据=主库数据  
复制类型  
1. 异步复制（默认）：主库写完就返回不管从库，因此主库挂了 → 数据可能还没同步到从库，可能导致数据丢失  
2. 半同步复制 (Semi-sync)：主库至少等一个从库确认，减少数据丢失但写入变慢
---
## Chunk 481 — 常见问题

常见问题
---
## Chunk 482 — 常见问题

1. 主从延迟：主库写得快，从库执行慢，本质是单线程执行+IO/CPU瓶颈。可以通过并行复制、提升从库配置和减少大事务解决  
2. 数据不一致：网络中断，binlog格式问题。可以使用ROW binlog和定期校验解决 3. 主从切换：主库挂了。可以通过MHAMGR等自动选主+切换解决  
9. 数据库的分库分表分库分表 = 把一个大数据库/大表拆成多个小的，来提升性能和扩展性水平分库分表：按行拆分（如按用户ID取模），数据量过大时用（如订单表）垂直分库分表：按列拆分（如拆分大字段到附表），字段过多或读写分离时用（如用户表拆分基本信息和详情追问  
10. 分布式事务解决方案分布式事务是在多个数据库或服务之间保证数据一致性的机制。常见方案包括2PC、TCC和 SAGA，它们本质是在一致性和性能之间做不同程度的权衡。 2PC (Two-Phase Commit)：Prepare - Coordinator协调参与者准备，各节点锁资源写log返回 YES/NO；Commit/Rollback - 全部yes→ commit 否则→ rollback。强一致但阻塞、性能差。 TCC (Try-Confirm-Cancel)：把事务交给业务自己控制。Try 预留资源（如冻结订单库存），确保后续操作可行；Confirm 阶段：确认执行事务（如扣减库存），不可逆；Cancel 阶段：取消事务并释放资源（如解冻库存），恢复初始状态。非阻塞，性能好但开发复杂。 SAGA：不保证强一致，只保证最终一致本地消息表：基于消息队列异步通知，实现最终一致，开发简单。 11.Redis  
Redis 是一个基于内存的高性能key -value数据库，常用于缓存、加速访问和处理高并发场景。数据类型key-value MySQL 数据在磁盘 (Disk)，访问磁盘IO慢 Redis数据在内存 (Memory)，内存访问快 Redis和MySQL可以配合使用，用户请求→Redis缓存→MySQL
---
## Chunk 483 — 常见问题

12. Redis 的数据结构 String：二进制安全，存字符串/数字，适用于缓存用户ID、计数器 Hash：键值对集合，存对象（如用户信息），支持字段级操作 List：有序链表，适用于消息队列、最新列表 Set：无序去重，适用于好友关系、标签去重 Sorted Set：分数排序，适用于排行榜、带权重的任务队列。
---
## Chunk 484 — 常见问题 > 12. Redis 的持久化机制

常见问题 > 12. Redis 的持久化机制

Redis 的持久化机制主要包括 RDB 和 AOF。RDB 通过在某一时刻生成内存数据的快照来实现持久化，优点是文件小、恢复快，但可能丢失最近一段时间的数据。AOF 则通过记录每一次写操作来保证数据安全，支持不同的写入策略，默认每秒同步一次，在性能和安全之间取得平衡。  
随着写操作增加，AOF 文件会变大，因此 Redis 提供 AOF 重写机制，将多次操作合并为最终状态，从而减小文件体积并提升恢复效率。  
在实际生产中，通常会同时开启 RDB 和 AOF，以兼顾恢复速度和数据安全性  
13. Redis 的过期键删除策略 Redis 对过期键采用惰性删除和定期删除相结合的策略。惰性删除在访问键时检查是否过期，降低 CPU 开销；定期删除通过周期性随机扫描部分键，避免过期键长期占用内存。当内存不足时， Redis 会触发内存淘汰机制，根据配置的策略（如 allkeys-lru、volatile-lru 等）删除部分键以释放空间。LRU 在 Redis 中采用近似实现，通过随机采样方式选择最久未使用的键，从而在性能和准确性之间取得平衡。  
14. Redis的主从复制、哨兵模式、集群模式集群模式如何实现数据分片和高可用？主从复制实现读写分离。哨兵模式保障高可用，集群模式兼具分片和高可用；集群通过槽位分片和主从复制，支撑大规模数据和高并发场景。主从复制：一个主库写、多个从库读，提升读性能，但是主库挂了无人接替哨兵模式：基于主从，监控主从状态，自动切换主库，实现高可用集群模式：多个主库和从库，数据分片每个主库存一部分数据有自己的从库。高可用：集群主库挂了，从库自动晋升为主库。
---
## Chunk 485 — 常见问题 > 15. NoSQL 数据库与关系型数据库的区别

常见问题 > 15. NoSQL 数据库与关系型数据库的区别

NoSQL 和关系型数据库的主要区别在数据模型、事务支持和扩展方式。关系型数据库采用表结构，具有严格的 schema，并支持 ACID 事务（原子性，一致性，隔离性，持久性），适合强一致性和复杂查询场景；而 NoSQL 数据库通常是无固定 schema 的，支持非结构化或半结构化数据，强调高并发和可扩展性。  
在扩展方面，关系型数据库主要依赖垂直扩展，而 NoSQL 更适合水平扩展。根据数据模型的不同，NoSQL 可以分为键值型（如 Redis）、文档型（如 MongoDB）、列族型（如 HBase）和图数据库（如 Neo4j），分别适用于缓存、内容存储、大数据和关系分析等场景。
---
## Chunk 486 — 五、脚本语言

五、脚本语言

1. Python 的装饰器 Python 装饰器是基于闭包的函数包装工具，可在不修改原函数代码的前提下增强功能，计时、日志等场景常用，支持带参数函数适配。实现原理：装饰器接收原函数作为参数，定义wrapper函数包裹原函数，在执行前后添加增强逻辑，最后返回wrapper。
---
## Chunk 487 — Python

Python

def timer(func): @wraps(func)#保留原函数信息（面试加分点）
---
## Chunk 488 — def wrapper(*args, **kwargs):

def wrapper(*args, **kwargs):
---
## Chunk 489 — def wrapper(*args, **kwargs):

start = time.time()  
result = func(*args, **kwargs)  
end = time.time() print(f"{func.__name__} 执行时间: {end - start:.4f} 秒") return result  
return wrapper  
2. Shell 脚本 Shell 脚本是一种用来自动执行一系列 Linux 命令的脚本语言，本质是把一堆命令写到一个文件里 → 一次执行  
Shell#变量定义 name="Alice"#不能有空格 echo $name#使用变量  
#条件判断 if [ -d "$dir" ]; then#[]两边必须有空格 echo "目录存在" else echo "不存在" fi  
#循环 for file in "$dir"/*; do  
echo $file  
done  
i=0  
while [ $i -lt 5 ]; do  
echo $i  
i=$((i+1))  
done  
3. Python 的迭代器和生成器生成器是自动实现的迭代器，并且支持惰性计算。  
生成器是迭代器的特殊形式，核心区别在实现方式和内存占用；生成器通过惰性求值处理大量数据，大幅降低内存开销，是Python 高效处理大数据的关键。  
迭代器需手动实现__iter__和__next__方法，生成器用yield 关键字或生成器表达式实现，自动支持迭代协议；  
迭代器需一次性加载数据，生成器按需生成数据，不占用大量内存； ● 生成器语法更简洁  
4. Shell 脚本中，$0、$1、$#、$?等特殊变量的含义 $0（脚本名） $1-$n（第1 到n 个参数 $#（参数个数） $?（上一条命令是否成功，0 为成功）
---
## Chunk 490 — def wrapper(*args, **kwargs):

4. Shell 脚本中，$0、$1、$#、$?等特殊变量的含义 $0（脚本名） $1-$n（第1 到n 个参数 $#（参数个数） $?（上一条命令是否成功，0 为成功）  
5. Python 的多线程和多进程 GIL（Global Interpreter Lock，全局解释器锁）是 Python 解释器中的一个锁，保证同一时间只有一个线程在执行 Python 代码 Python 多线程受GIL 限制无法真正并行，多进程可利用多核CPU；CPU 密集型任务需并行计算，多进程无GIL 限制，故更有优势，两者适用场景明确区分。 1. 并行性：多线程受GIL 限制，同一时刻仅一个线程执行Python 字节码，无法利用多核；多进程每个进程有独立GIL，支持真正并行； 2. 资源：多线程占用少、通信简单（共享内存），多进程占用多、通信复杂（如队列、管道）；3. 适用场景：多线程适合IO 密集型（如网络请求），多进程适合CPU 密集型（如数据计算）。六、分布式系统与高可用  
1. 分布式系统的CAP理论分布式系统的CAP理论是什么？BASE 理论与CAP理论的关系是什么？ CAP 理论指出分布式系统无法同时满足强一致性、高可用性和分区容错性，P 是必选故需权衡 CP 或AP；BASE 理论是CAP的妥协，追求最终一致性，适配高可用场景。 CAP 定义：Consistency（强一致性，数据实时同步）、Availability（高可用，服务持续响应）、 Partition Tolerance（分区容错，网络分区时系统可用）。关系：BASE（Basically Available、Soft state、Eventually consistent）基于AP 扩展，允许短期不一致，通过异步同步实现最终一致，是分布式系统的实际选择（如电商订单系统）。  
设计分布式系统时，我会按业务需求权衡：支付等强一致场景选CP（如ZooKeeper），电商等高可用场景选AP+BASE（如Redis 集群），平衡一致性和可用性。
---
## Chunk 491 — def wrapper(*args, **kwargs):

设计分布式系统时，我会按业务需求权衡：支付等强一致场景选CP（如ZooKeeper），电商等高可用场景选AP+BASE（如Redis 集群），平衡一致性和可用性。  
追问1：电商系统的订单支付场景，为什么通常选择AP+BASE 而非CP？请举例说明。  
电商订单支付需优先保障高可用（用户能正常下单支付），而非强一致性。例如用户下单后，库存异步扣减，短时间内可能存在“下单成功但库存未更新”的软状态，但通过定时对账最终实现一致，既保障了系统可用性，又避免了因强一致导致的服务不可用。
---
## Chunk 492 — def wrapper(*args, **kwargs):

79. "分布式一致性算法有哪些？（如Paxos、Raft 等）请简述Raft 算法的核心流程（领导者选举、日志复制）。" 分布式一致性算法有Paxos、Raft 等，Raft 因流程清晰成为主流；其核心是领导者选举和日志复制，通过任期机制和多数确认保障一致性，易工程实现。提出观察（50 秒）：核心流程：1. 领导者选举：节点初始为追随者，任期超时转为候选人，向其他节点请求投票，得多数票者当选领导者，任期号递增防止脑裂；2. 日志复制：领导者接收客户端请求，追加日志条目，同步给所有追随者，收到多数追随者确认后，提交日志并返回结果给客户端。安全性：领导者仅提交自己任期内的日志，确保所有节点日志一致。未来贡献（20 秒）：设计分布式系统（如配置中心、分布式锁）时，我会优先选择基于Raft 的组件（如Etcd、Nacos），利用其成熟的一致性保障，避免重复实现复杂算法，提升系统可靠性。 ④面试官可能追问的问题及回答追问1：Raft 算法中，“任期”的作用是什么？如果出现多个领导者（脑裂），会如何处理？参考回答：面试官您好，任期的作用是标识领导者的合法性，任期号递增，新任期的领导者优先级高于旧任期。若出现脑裂，新任期的领导者会通过日志复制机制覆盖旧任期领导者的未提交日志，同时其他节点发现更高任期的领导者后，会转为追随者，最终恢复单一领导者，保障日志一致性。 80. "什么是分布式锁？实现分布式锁的常见方式有哪些？ （如基于Redis、ZooKeeper 等）它们的优缺点是什么？" 分布式锁用于跨服务器同步共享资源访问，常见实现有Redis 和ZooKeeper；Redis 锁性能优，ZooKeeper 锁可靠性高，需按业务场景权衡选择
---
## Chunk 493 — def wrapper(*args, **kwargs):

。提出观察（50 秒）：实现及优缺点：1. Redis 锁：用set key value nx ex 命令（原子操作），优点是性能高、实现简单，缺点是可能因过期时间设置不合理导致死锁，需配合看门狗机制；2. ZooKeeper 锁：创建临时有序节点，监听前序节点，优点是自动释放锁（会话超时）、无死锁风险，缺点是性能略低、依赖 ZooKeeper 集群。适用场景：高性能场景用Redis 锁，高一致性场景用ZooKeeper 锁。未来贡献（20 秒）：开发中我会按场景选型，如秒杀系统用Redis 锁提升并发，分布式事务场景用ZooKeeper 锁保障一致性；Redis 锁会设置合理过期时间并加看门狗，避免死锁。 ④面试官可能追问的问题及回答追问1：Redis 分布式锁中，“看门狗机制”的作用是什么？如何实现？参考回答：面试官您好，看门狗机制用于解决Redis 锁过期时间过短导致的锁提前释放问题。实现：加锁成功后，启动后台线程，每隔一段时间（如过期时间的1/3）检查锁是否仍持有，若持有则延长过期时间，确保业务执行完前锁不释放，避免并发安全问题。 81. "负载均衡的原理是什么？常见的负载均衡算法有哪些？ （如轮询、加权轮询、最少连接数等）" 负载均衡通过合理分发请求避免单点过
---
## Chunk 494 — def wrapper(*args, **kwargs):

载，提升系统可用性和吞吐量；常见算法按“公平性、资源利用率”设计，需结合业务场景选择。提出观察（50 秒）：原理：接收客户端请求，按预设算法分发到后端服务器集群，避免单台服务器负载过高。常见算法：1. 轮询：请求依次分发，适用于服务器配置一致的场景；2. 加权轮询：按服务器权重分配（如性能高的权重高），适配服务器配置差异；3. 最少连接数：分发到当前连接数最少的服务器，适用于动态请求（如接口调用）；4. IP 哈希：按客户端IP 哈希固定分发，实现会话保持。未来贡献（20 秒）：设计系统时，我会按场景选型，静态资源服务用轮询，异构服务器集群用加权轮询，需会话保持的场景用IP 哈希；同时监控服务器负载，动态调整算法参数。 ④面试官可能追问的问题及回答追问1：“IP 哈希算法”实现会话保持有什么局限性？如何解决？参考回答：面试官您好，局限性：1. 客户端IP 变化（如切换网络）会导致会话丢失；2. 部分客户端共用IP（如局域网）会导致负载不均。解决方法：1. 用Cookie 或Token 存储会话信息，替代IP 绑定；2. 结合一致性哈希算法，即使IP 变化也能映射到相近服务器，减少会话丢失概率。 82. "常见的负载均衡设备或组件有哪些？（如LVS、Nginx、 HAProxy 等）它们的适用场景有何不同？" LVS、Nginx、HAProxy 是主流负载均衡组件，LVS 是四层高性能转发，Nginx 和HAProxy 支持七层，功能更丰富，适用场景因层级和性能差异而不同。提出观察（50 秒）：特性及适用场景：1. LVS：四层负载均衡（TCP/UDP），基于内核转发，性能最高（百万并发），无复杂功能，适用于高并发TCP 服务（如数据库、Redis）；2. Nginx：七层为主（HTTP/HTTPS），支持反向代理、静态资源缓存，功能丰富，适用于Web 服务负载均衡（如网站、接口）；3. HAProxy：支持四层和七层，健康检查能力强，适用于复杂负载场景（如需要会话保持、动态权重调整）
---
## Chunk 495 — def wrapper(*args, **kwargs):

。未来贡献（20 秒）：架构设计时，我会按协议和并发需求选型，高并发TCP 服务用LVS，Web 服务用Nginx（兼顾缓存），复杂场景用HAProxy；通过多层负载均衡（LVS+Nginx）提升系统可用性。 ④面试官可能追问的问题及回答追问1：为什么大型互联网公司常采用“LVS+Nginx”的多层负载均衡架构？核心优势是什么？参考回答：面试官您好，核心优势是“性能+功能”互补：LVS 作为第一层负载均衡，利用四层内核转发的高性能承接海量并发请求，实现流量分流；Nginx 作为第二层，提供七层协议解析、静态资源缓存、反向代理等丰富功能，同时可进一步分流到后端应用服务器，既保障了高并发处理能力，又满足了Web 服务的功能需求。 "系统容灾设计的核心原则是什么？请简述“两地三中心” 的容灾架构。" 系统容灾设计的核心是保障业务连续性，核心指标是RTO（恢复时间）和RPO（数据丢失量）；两地三中心架构是高等级容灾方案，能抵御单点和区域灾难。提出观察（50 秒）：核心原则：1. 数据多副本备份；2. 故障隔离（避免单点故障扩散）；3. 快速恢复（RTO 最小化）；4. 数据低丢失（RPO 最小化）； 5. 定期演练。两地三中心：1. 生产中心（主城市，承载核心业务）；2. 同城灾
---
## Chunk 496 — def wrapper(*args, **kwargs):

备中心（同城市，实时同步数据，快速切换）；3. 异地灾备中心（异城市，异步同步数据，抵御区域灾难）。未来贡献（20 秒）：设计核心业务系统时，我会按两地三中心架构规划容灾方案，明确RTO 和RPO 指标（如RTO<4 小时，RPO<5 分钟）；定期做灾备切换演练，确保灾难发生时能快速恢复业务。 ④面试官可能追问的问题及回答追问1：“同城灾备”和“异地灾备”的数据同步策略有何不同？为什么？参考回答：面试官您好，同城灾备采用实时同步（如MySQL 主从复制、存储双活），因距离近、网络延迟低，能保证RPO 接近0，支持快速切换；异地灾备采用异步同步，因跨城市网络延迟高，实时同步会影响生产中心性能，异步同步第 101 页共 119 页虽RPO 略高，但平衡了性能和容灾能力，抵御区域灾难（如地震、洪水）。 84. "分布式系统中的服务注册与发现机制是什么？请举例说明相关的组件（如Eureka、Nacos 等）的实现原理。" 服务注册与发现是分布式微服务的核心，解决服务地址动态变化问题；Eureka 基于最终一致性，Nacos 支持AP/CP 双模，适配不同一致性需求。提出观察（50 秒）：核心机制：服务启动时注册到注册中心，定期发送心跳维持在线状态，客户端从注册中心获取服务列表，注册中心通过健康检查剔除下线服务。组件原理：1. Eureka：Peer to Peer 集群复制，服务列表最终一致，支持自动故障转移，适合AP 场景；2. Nacos：支持AP（服务发现）和CP（配置管理）双模，基于Raft 算法实现一致性，提供服务健康检查、动态配置等丰富功能。未来贡献（20 秒）：微服务架构设计时，我会优先选择Nacos（功能丰富），按场景选择一致性模式；配置合理的心跳间隔和健康检查阈值，确保服务列表实时准确，提升系统可用性
---
## Chunk 497 — def wrapper(*args, **kwargs):

。未来贡献（20 秒）：微服务架构设计时，我会优先选择Nacos（功能丰富），按场景选择一致性模式；配置合理的心跳间隔和健康检查阈值，确保服务列表实时准确，提升系统可用性。 ④面试官可能追问的问题及回答追问1：Eureka 的“自我保护机制”是什么？为什么需要这个机制？参考回答：面试官您好，Eureka 的自我保护机制是当一定时间内（默认90 第 102 页共 119 页秒）收到的服务心跳数低于阈值，会认为网络分区而非服务下线，不会剔除服务列表中的实例。原因是避免网络抖动导致误判服务下线，进而引发大量服务调用失败，保障分布式系统的稳定性。 85. "什么是熔断、降级、限流？它们在分布式系统中的作用是什么？请举例说明实现方式。"，熔断、降级、限流是分布式系统的“防护三剑客”，分别应对服务故障、资源紧张和流量峰值，核心是保障核心业务可用，避免级联故障。提出观察（50 秒）：定义、作用及实现：1. 熔断：服务调用失败率达阈值时触发（如Sentinel 的Circuit Breaker），暂时断连避免雪崩，故障恢复后闭合，实现方式有熔断器模式；2. 降级：资源紧张时关闭非核心功能（如电商大促关闭评价功能），实现方式有开关控制、动态配置；3. 限流：限制单位时间请求数（如令牌桶算法），保护后端服务，实现组件有Sentinel、Guava RateLimiter。未来贡献（20 秒）：开发中我会用Sentinel 统一实现三者，核心接口配置限流（令牌桶算法），依赖服务配置熔断（失败率阈值50%），大促时通过动态开关降级非核心功能，保障核心业务稳定。
---
## Chunk 498 — def wrapper(*args, **kwargs):

④面试官可能追问的问题及回答追问1：限流的“令牌桶算法”和“漏桶算法”有何区别？分别适用于什么第 103 页共 119 页场景？参考回答：面试官您好，令牌桶算法：按固定速率生成令牌，请求需获取令牌才能执行，支持突发流量（令牌积累），适用于允许短期高并发的场景（如秒杀）；漏桶算法：请求按固定速率处理，超出容量则丢弃，强制平滑流量，适用于需严格控制QPS 的场景（如数据库访问）。 86. " 分布式追踪系统的作用是什么？请简述 OpenTelemetry 或SkyWalking 的核心原理。" 分布式追踪系统用于追踪跨服务调用链路，定位分布式问题（如超时、异常），核心是通过TraceID/SpanID 串联调用； OpenTelemetry 和SkyWalking 是主流实现，原理类似。提出观察（50 秒）：核心作用：1. 调用链可视化（展示服务间调用关系）； 2. 问题定位（快速定位跨服务超时/异常节点）；3. 性能分析（统计各环节耗时）；4. 依赖分析（梳理服务依赖关系）。核心原理：1. 生成TraceID（全局调用ID）和SpanID（单个服务调用ID）；2. 无侵入采集调用数据（如SkyWalking 的字节码增强）；3. 数据传输到后端存储；4. 可视化展示调用链和性能指标。未来贡献（20 秒）：运维分布式系统时，我会部署SkyWalking 实现全链路第 104 页共 119 页追踪，配置合理采样率（如10%）避免性能损耗；通过调用链分析优化慢接口，定位跨服务依赖问题，提升系统稳定性。 ④面试官可能追问的问题及回答追问1：分布式追踪系统中的“采样率”是什么？如何设置合理的采样率？参考回答：面试官您好，采样率是指采集调用链数据的比例（如10%表示仅采集10%的请求），用于平衡追踪效果和系统性能。设置原则：1. 低流量服务设高采样率（如50%），确保足够数据；2. 高流量服务设低采样率（如1%），避免采集压力；3. 异常请求强制采样（如超时、报错请求100%采集），确保问题可追踪
---
## Chunk 499 — def wrapper(*args, **kwargs):

。设置原则：1. 低流量服务设高采样率（如50%），确保足够数据；2. 高流量服务设低采样率（如1%），避免采集压力；3. 异常请求强制采样（如超时、报错请求100%采集），确保问题可追踪。 87. "高可用系统的设计要点有哪些？如何保证服务的 99.99%可用性？"，高可用系统设计需围绕“避免单点故障、快速故障恢复”，核心要点含集群、容灾等；99.99%可用性需通过多层防护和自动化手段，将年故障时间控制在52 分钟内。提出观察（50 秒）：设计要点：1. 集群部署（避免单点）；2. 异地容灾（如两地三中心）；3. 熔断降级限流（防护核心服务）；4. 数据多副本（避免数据丢失）；5. 监控告警（实时感知故障）；6. 自动化故障切换（减少恢复时间）；7. 定期故障演练（验证容灾能力）。99.99%保障：按要点落地，核心服
---
## Chunk 500 — def wrapper(*args, **kwargs):

务多活部署，数据实时同步，故障自动切换，恢复时间控制在分钟级。未来贡献（20 秒）：设计系统时，我会按高可用要点分层架构，核心服务部署3 个以上副本，配置自动化切换和监控告警；每季度做故障演练，持续优化容灾能力，确保达到99.99%可用性。 ④面试官可能追问的问题及回答追问1：如何通过“故障注入”演练验证系统的高可用性？请举例说明常见的故障注入场景。参考回答：面试官您好，故障注入是模拟各类故障（如服务器宕机、网络延  
迟、数据库不可用），验证系统是否能正常容错。常见场景：1. 关闭核心服务的一个副本，验证负载均衡是否正常；2. 模拟网络延迟（如增加1s 延迟），验证熔断降级是否触发；3. 断开数据库从库，验证主从切换是否正常，确保系统在故障下仍能提供服务。
---
## Chunk 501 — 七、云原生技术

七、云原生技术

1. 云原生是什么？核心组件有什么什么是云原生？云原生技术体系包含哪些核心组件？（如容器、编排、服务网格等）云原生是基于云架构的设计理念，核心是实现应用弹性、敏捷迭代；技术体系围绕容器化、编排等核心组件，构建高效可扩展的分布式系统。定义：以微服务为架构、容器化为基础、DevOps 为流程，支持快速迭代、弹性伸缩、故障自愈的应用开发部署模式。核心组件：1.容器（Docker）：应用打包与隔离；2. 编排（K8s）：容器调度与管理；3. 服务网格（Istio）：服务通信与治理；4. 持续交付（Jenkins）：自动化部署；5.可观测性（Prometheus+Grafana）：监控告警。  
开发云原生应用时，我会遵循微服务架构设计，用Docker打包、K8s 编排，结合Istio 治理服务通信；通过持续交付提升迭代效率，确保应用适配云环境的弹性需求。
---
## Chunk 502 — 追问1：云原生的“12 因素应用”原则是什么？

追问1：云原生的“12 因素应用”原则是什么？

它对云原生应用开发有何指导意义？ 12 因素应用是云原生应用的设计准则，包括基准代码、依赖管理、配置分离等。指导意义：确保应用可移植（适配不同云环境）、可伸缩（支持弹性扩缩容）、易维护（简化部署与迭代），是云原生应用具备高可用、高弹性的核心保障。  
2. Docker 的核心概念 Docker 容器与虚拟机的区别是什么？ Docker 核心概念是镜像、容器、仓库，镜像为打包模板，容器为运行实例，仓库用于存储；容器与虚拟机的核心区别在内核共享，导致性能和资源占用差异显著。核心概念：镜像（只读模板，含应用及依赖）、容器（镜像运行实例，可读写）、仓库（存储镜像的远程/本地仓库）。区别：1. 内核：容器共享宿主机内核，虚拟机有独立内核；2. 启动速度：容器秒级，虚拟机分钟级；3. 资源：容器占用少，虚拟机占用多；4. 隔离性：虚拟机强于容器。容器基于 namespace 隔离、cgroups 限制资源。开发中我会用Docker 打包应用（确保环境一致性），优先用容器部署微服务（提升资源利用率）；需强隔离场景选用虚拟机，平衡性能与隔离需求。  
追问1：Docker 镜像的分层结构是什么？这种结构有什么优势？ Docker 镜像采用分层文件系统（如UnionFS），每层对应镜像构建的一个步骤（如安装依赖、复制代码）。优势：1. 分层复用（不同镜像可共享底层层，减少存储占用）；2. 增量构建（修改仅重建上层层，提升构建效率）；3. 可追溯（每层对应构建步骤，便于排查问题）。
---
## Chunk 503 — 追问1：云原生的“12 因素应用”原则是什么？ > 3. Kubernetes

追问1：云原生的“12 因素应用”原则是什么？ > 3. Kubernetes
---
## Chunk 504 — 追问1：云原生的“12 因素应用”原则是什么？ > 3. Kubernetes

Kubernetes 的核心组件有哪些？（如API Server、Etcd、Scheduler、Controller Manager、Kubelet 等）它们的作用是什么？" K8s 核心组件分控制平面和节点组件，控制平面负责集群管理，节点组件负责容器运行；各组件通过API Server 协作，Etcd 存储集群核心数据。核心组件及作用：1. API Server：集群统一入口，处理所有请求；2. Etcd：分布式键值存储，存集群状态和配置；3. Scheduler：调度Pod 到合适节点（基于资源需求）；4. Controller Manager：运行控制器（如Deployment 控制器），保障集群状态符合期望；5. Kubelet：节点上运行，管理容器生命周期；6. Kube-proxy：维护节点网络规则，实现Service 通信。  
运维K8s 集群时，我会重点监控核心组件状态（如APIServer 可用性、Etcd 健康），理解组件协作逻辑；通过组件日志定位问题，确保集群稳定运行。  
追问1：Kubernetes 中，Pod 调度的完整流程是什么？Scheduler 在其中起到了什么关键作用？调度流程：1. 用户通过API Server 提交Pod 创建请求；2. Scheduler 监听未调度的Pod，筛选出满足资源需求的节点（预选）；3. 对候选节点打分（优选，如资源利用率、亲和性）；4. 选择最高分节点，通过API Server 通知Kubelet 创建Pod。Scheduler 的关键作用是“最优节点匹配”，确保Pod 高效利用集群资源。
---
## Chunk 505 — 追问1：云原生的“12 因素应用”原则是什么？ > 3. Kubernetes

4. Kubernetes 中的Pod、Deployment、Service、ConfigMap、Secret K8s 核心资源各司其职，Pod 是容器运行载体，Deployment 管理Pod 生命周期，Service 提供网络访问，ConfigMap 和Secret 存储配置，共同支撑应用稳定运行。资源作用：1. Pod：最小运行单位，可包含多个容器，共享网络和存储；2. Deployment：声明式编排 Pod，支持扩缩容、滚动更新、回滚；3. Service：为Pod 提供固定访问IP 和端口，实现负载均衡（如轮询）；4. ConfigMap：存储非敏感配置（如数据库地址），明文存储；5. Secret：存储敏感配置（如密码），Base64 加密，保障安全。部署应用时，我会用Deployment 管理Pod（配置扩缩容策略），Service 暴露应用访问入口，敏感配置用Secret 存储，非敏感用ConfigMap，确保资源配置规范安全。  
追问1：Kubernetes 中，Deployment 的“滚动更新”和“重建更新”有何区别？分别适用于什么场景？滚动更新：逐步替换旧Pod 为新Pod，过程中服务不中断，适用于需高可用的生产环境（如API 服务）；重建更新：先删除所有旧Pod，再创建新Pod，更新过程中服务中断，适用于无状态且可短暂停机的场景（如测试环境应用）。  
5. 服务网格（Service Mesh）什么是服务网格？Istio 作为服务网格的代表，其核心功能是什么？  
服务网格是微服务的通信治理基础设施，通过透明化代理分离业务与治理；Istio 作为主流实现，核心功能涵盖流量控制、安全通信等，提升微服务可靠性。
---
## Chunk 506 — 追问1：云原生的“12 因素应用”原则是什么？ > 3. Kubernetes

服务网格是微服务的通信治理基础设施，通过透明化代理分离业务与治理；Istio 作为主流实现，核心功能涵盖流量控制、安全通信等，提升微服务可靠性。  
定义：在微服务间插入代理层（如Envoy），统一处理通信、安全、监控等非业务逻辑，业务代码无需关注治理细节。Istio 核心功能：1. 流量控制（灰度发布、熔断、重试）；2. 安全通信（mTLS 加密、身份认证）；3. 可观测性（调用链追踪、监控 metrics）；4. 服务治理（负载均衡、故障注入）。架构分控制平面（Pilot）和数据平面（Envoy）。  
微服务架构中，我会用Istio 实现灰度发布（降低迭代风险）、mTLS 加密（保障通信安全）；通过可观测性监控服务通信状态，快速定位跨服务问题。
---
## Chunk 507 — Istio 的“数据平面”和“控制平面”分别起到什么作用？

Istio 的“数据平面”和“控制平面”分别起到什么作用？

它们之间如何协作？数据平面由Envoy 代理组成，部署在每个Pod 中，负责转发服务流量、执行治理策略（如流量控制、加密）；控制平面由Pilot、Citadel 等组成，负责制定治理策略、管理服务发现、发放证书。协作：控制平面将策略推送给数据平面，Envoy 按策略处理实际流量，实现“策略与执行分离”。
---
## Chunk 508 — 八、工程实践与开发效率

八、工程实践与开发效率

1. 敏捷开发敏捷开发是迭代式开发理念，核心是快速响应变化、持续交付价值；Scrum 是敏捷的主流框架，通过明确角色、事件和交付物保障团队高效协作。  
产品负责人（PO）：梳理需求、维护产品待办列表 ● Scrum 大师（SM）：保障Scrum 流程落地，移除团队障碍. ● 开发团队：自组织完成冲刺任务 ● 冲刺 (Sprint) 是Scrum 的核心迭代周期，在固定时间内（通常2-4 周）团队交付一个可运行的产品增量。  
2. 代码评审代码评审的核心是保障代码质量、统一团队规范、促进知识共享，而非单纯找bug；评审需聚焦逻辑、性能等关键维度，通过建设性反馈提升团队代码水平。核心目的  
避免流于形式： ● 明确评审标准（如“高风险模块必须评审”） ● 限制评审代码量（单次不超过400 行） ● 要求评审人给出具体反馈而非“通过”  
提高效率用自动化工具（如SonarQube）检查格式、简单bug 评审前作者说明核心逻辑聚焦高风险模块（如支付、权限相关代码）
---
## Chunk 509 — 八、工程实践与开发效率 > 3. CI/CD

八、工程实践与开发效率 > 3. CI/CD

CI 是持续集成 (Integration) 代码频繁合并并自动化构建测试，CD (Deployment) 是持续交付或持续部署；完整流程需工具链支撑，核心是自动化与快速反馈。流程  
1. 开发者通过Git 提交代码到仓库 2. GitLab CI/Jenkins 触发自动化构建（如编译、打包） 3. 执行自动化测试（单元测试、集成测试） 4. 测试通过后，持续交付需手动批准部署，持续部署自动部署到生产/测试环境
---
## Chunk 510 — 工具作用

工具作用

Git（代码管理） ● Jenkins/GitLab CI（构建与流程编排） ● JUnit（单元测试） ● Docker（打包）。  
4. 如何保证代码质量保证代码质量通常需要从多个环节入手。首先是编码规范，保证代码风格统一、可读性强；其次是静态代码分析，在代码运行前发现潜在 bug、规范问题和安全风险；然后是代码评审，通过人工 review 检查业务逻辑、设计合理性和性能问题；最后是自动化测试，包括单元测试和集成测试，验证功能正确性。像 SonarQube 这样的工具，主要作用是从 bug、漏洞、代码异味、测试覆盖率和重复代码等多个维度对代码进行自动化分析，并通过质量门禁帮助团队持续提升代码质量。静态分析工具如 Checkstyle、SpotBugs 等，则更偏向于在开发阶段提前发现格式问题、潜在 bug 和不安全写法，帮助开发者尽早修复问题。  
5. 单元测试、集成测试、系统测试三类测试按粒度从细到粗：单元测试测单个组件，集成测试测模块交互，系统测试测整体功能  
单元测试：测试单个函数/类（如接口逻辑），隔离外部依赖（用Mock 替代DB、网络），目的验证逻辑正确性  
Mock外部依赖 ○ 聚焦核心逻辑（如异常处理、边界条件） ○ 保持独立性（测试用例互不依赖） ○ 高覆盖率（重点覆盖核心路径）  
集成测试：测试模块间交互（如服务A 调用服务B），验证接口兼容性 ● 系统测试：测试整个系统，模拟真实用户场景，验证功能完整性
---
## Chunk 511 — 工具作用 > 1. 线上服务CPU利用率过高与排查解决

工具作用 > 1. 线上服务CPU利用率过高与排查解决

线上服务出现CPU 利用率过高的问题，你会如何定位和解决？请详细描述排查步骤。  
线上CPU 过高需按“定位进程→线程→代码→优化”的步骤排查，核心是用工具找到消耗CPU 的核心线程和代码，再针对性优化，避免盲目重启。  
排查步骤：1. 定位进程：用top 命令找到CPU 使用率高的进程（如PID 1234）；2. 定位线程：用ps -mp 1234 -o THREAD,tid,time 找到高CPU 线程，将TID 转为十六进制；3. 分析堆栈：用jstack 1234 | grep 十六进制TID，查看线程执行的代码（如死循环、频繁调用的方法）；4. 辅助分析：用 jprofiler/perf 工具进一步定位热点代码；5. 排查根因：分析代码逻辑（如死循环、低效算法、频繁GC）。解决方法：优化代码（如修复死循环、替换高效算法）、调整JVM 参数（如优化GC 策略）。  
遇到CPU 过高问题时，我会先通过工具定位根因，避免盲目重启；针对死循环等代码问题快速修复上线，针对高并发场景优化算法和缓存策略，确保服务稳定。  
追问1：如果排查发现是JVM 频繁GC 导致的CPU 过高，如何进一步定位GC问题的根因？有哪些优化方案？  
进一步定位：1. 用jstat -gcutil 1234 1000 查看GC统计（如YGCT、FGCT、GCT）；2. 用jmap -dump:format=b,file=heap.hprof 1234导出堆快照，用MAT 分析内存泄漏或大对象。优化方案：1. 调整JVM 参数（如增大新生代内存、更换GC 收集器）；2. 修复内存泄漏（如静态集合未释放）；3. 减少大对象创建（如复用对象池）。
---
## Chunk 512 — 工具作用 > 2. 内存泄漏与排查

工具作用 > 2. 内存泄漏与排查

99. "线上服务出现内存泄漏问题，你会采用哪些工具和方法进行排查？请举例说明。" 1. 确认泄漏：用jstat -gcutil PID1000 监控内存和GC，若内存持续增长、GC 频繁则疑似泄漏；2. 导出堆快照：用jmap -dump:format=b,file=heap.hprof PID 导出，用MAT 工具分析 3. 定位泄漏对象：在MAT 中查看支配树、引用链，找到未被回收的大对象（如静态 List） 4. 结合日志：分析GC 日志和应用日志，排查资源未关闭（如数据库连接）、线程池未销毁等场景。排查时我会先通过jstat 监控确认泄漏，再用MAT 分析堆快照定位引用链；重点排查静态集合、未关闭资源等常见场景，修复后通过压测验证，避免泄漏复发。  
追问1：如何区分“内存泄漏”和“内存溢出”？两者的处理思路有何不同？内存泄漏是原因（无用对象未回收），内存溢出是结果（内存不足导致OOM）。处理思路：内存泄漏需定位泄漏对象并修复代码（如释放静态集合）；内存溢出若因泄漏导致则先修复泄漏，若因内存不足则调整JVM 参数（增大堆内存）或优化内存使用（如减少大对象）。
---
## Chunk 513 — 工具作用 > 3. 与产品和前端对齐

工具作用 > 3. 与产品和前端对齐
---
## Chunk 514 — 工具作用 > 3. 与产品和前端对齐

在与产品和前端工程师合作推进产品迭代时，如何高效地沟通需求和解决协作中的问题？请结合实际场景说明。与产品和前端协作的核心是“清晰对齐目标、书面化确认、换位思考”，通过规范沟通流程和主动解决分歧，确保产品迭代高效推进，减少返工。  
高效沟通方法：1. 需求阶段：参与需求评审会，结合原型图和PRD 文档，明确功能边界、验收标准，提出技术可行性风险（如“高频查询需缓存优化”）；2. 开发阶段：用接口文档（如Swagger）明确前  
后端交互，每日站会同步进度，遇到需求变更及时书面确认；3. 问题解决：如前端反馈接口响应慢，主动协助排查（用监控看耗时），共同优化（如增加缓存），而非相互推诿。  
协作中我会主动对齐需求细节，用书面文档避免理解偏差；遇到问题换位思考（如前端兼容问题），主动提供技术支持；平衡产品需求与技术实现，确保迭代高效高质量。  
如果产品提出的需求技术实现难度大、工期紧张，你会如何沟通？我会按“理解需求→分析成本→提供方案”沟通： 1. 先确认需求核心目标（如“提升用户支付转化率”）；2. 客观说明技术难度和工期（如“核心功能需3 周，当前工期仅1 周”）；3. 提供替代方案（如“先实现核心功能，非核心功能后续迭代”）；4. 与产品协商优先级，平衡用户价值和技术成本，达成共识。  
instlily  
During internship at Menu, medium sized start-up, I worked on high-traffic user flows like search and homepage, but what I focused on was not just UI, but how user actions translate into business decisions.
---
## Chunk 515 — 工具作用 > 3. 与产品和前端对齐

For example, I designed a event-tracking system across 20+entry points, and by collaborating with the AI and Data analytics team, it allowed us to understand the full user conversion path from landing to checkout, and after that month’s release, I really see how my event tracking system is actually placed in production, and how actual user data can be converted into next step business decisions. One of the benefits of working in start-up.  
I also worked on integrating AI-assisted coding guidelines into our development workflow. Instead of using AI as a standalone tool, I structured context rules to make AI outputs more consistent and aligned with engineering standards.
---
## Chunk 516 — 工具作用 > 3. 与产品和前端对齐

This made me think more about how AI can be embedded into workflows, rather than just used interactively. So, after my internship, I plan to build user-facing systems that connect AI, data, and real-world workflows, and from what i learned from the website, instlily is exactly the area I plan to touch on the next step. They build a system where AI agents can directly operate inside enterprise systems with structured access, shared memory, and controlled execution.
---
## Chunk 517 — Pawse

Pawse
---
## Chunk 518 — Pawse

In Pawse, I led the development of a pet-centered social app where I focused on designing a dynamic feed system driven by ranking and user interaction signals.  
Instead of static rendering, the system continuously adapts based on user behavior, which is conceptually similar to how intelligent systems prioritize and make decisions.  
I also integrated AI features like pet recognition and explored AI-assisted development workflows, which gave me hands-on experience in embedding AI into real product pipelines.  
Instalily公司研究公司介绍： InstaLILY AI is a vertical AI platform for the physical economy that enables companies to deploy autonomous AI teammates, called InstaWorkers™, to execute revenue-generating
---
## Chunk 519 — Pawse

sales, service, and operations workflows inside existing enterprise systems. Powered by InstaBrain™, a shared company brain built from domain-specific small language models, InstaLILY turns institutional knowledge into autonomous execution, without replacing systems of record. One company brain. Many AI teammates.  
2 model Read the google deepmind article, notice you combine Gemini and Gemma. Gemini3用于深度推理 Gemma-based Small Language Models (SLMs) for vertical efficiency （根据企业的内存 instabrain来生成这个垂直型agent SLM）  
Why join instlily, why startup  
1. See the impact very quickly，ownership 2. Really build product end to end 3. Like the team atmosphere, women in AI 4. 一面的时候我讲解pawse，我认为面试官非常感兴趣，我觉得气场很合适  
scaling vertical AI agents across different industries，SLM就算是这个vertical，节省成本，减少延迟，保护数据隐私，很感兴趣认为这个概念很新颖，但是很有前途
---
## Chunk 520 — Pawse

scaling vertical AI agents across different industries，SLM就算是这个vertical，节省成本，减少延迟，保护数据隐私，很感兴趣认为这个概念很新颖，但是很有前途  
反问： What are the biggest challenges in scaling vertical AI agents across different industries? （instead of one-size-fits-all AI Women in AI Has a lot of potential to grow，really want to step into real AI start-up as the begin of my career
---
## Chunk 521 — Pawse > 整体问题：很容易说的很绕。尽量总分结构去说

Pawse > 整体问题：很容易说的很绕。尽量总分结构去说

1 ⃣ 先结论（有问题） 2 ⃣ 再机制（为什么有问题） 3 ⃣ 再解决（你会怎么做）🔥 4 如何优化，tradeoff：批量更新，减少请求（节流），减少渲染
---
## Chunk 522 — Agent 的核心不是生成，而是“规划+调用工具”

Agent 的核心不是生成，而是“规划+调用工具”

我目前是用规则来触发 tool，这样系统更稳定、可控。因为我这个项目要求很高的精确性，结构性比较强。  
但我也理解真正的 agent 应该让模型来做决策，这样更灵活。如果系统复杂度提高，我会考虑把部分决策交给模型，同时保留一些规则来做约束。
---
## Chunk 523 — Agent 的核心不是生成，而是“规划+调用工具” > 1. 先说本质（高频 setState）

Agent 的核心不是生成，而是“规划+调用工具” > 1. 先说本质（高频 setState）

在 AI streaming 场景下，比如 ChatGPT 一边生成一边输出，本质是一个高频的状态更新过程。  
每生成一小段文本，前端都会触发一次 setState，从而引发组件的重新渲染。  
如果直接操作真实 DOM，这种高频更新会带来很大的性能开销，而 Virtual DOM 的作用是通过在内存中对比新旧树，只更新发生变化的部分，从而降低真实 DOM 操作的成本  
Virtual DOM 解决的是“怎么更新” 但 streaming 场景更重要的是“更新多少次”
---
## Chunk 524 — Agent 的核心不是生成，而是“规划+调用工具” > 2. useState为啥会执行两次

Agent 的核心不是生成，而是“规划+调用工具” > 2. useState为啥会执行两次

在开发环境中，useEffect 执行两次主要是因为 React 开启了 StrictMode。  
在 StrictMode 下，React 会故意执行一次 mount → unmount → 再 mount 的流程，也就是模拟组件被卸载再重新挂载。
---
## Chunk 525 — 这样做的目的是帮助开发者发现副作用中的问题，比如：

这样做的目的是帮助开发者发现副作用中的问题，比如：

有没有正确清理定时器 ● 有没有内存泄漏  
Ai stream是高频 state 更新（render），不是频繁发请求。在 streaming 场景下：一个请求 = 一个数据流。如果执行两次：= 两个数据流 ❌  
就会：数据重复/UI错乱/状态混乱。所以ai strem场合下更需要useState来检测副作用是否安全，是否有重复请求，内存泄漏等
---
## Chunk 526 — 这样做的目的是帮助开发者发现副作用中的问题，比如： > 3. redux为啥能减少rerender

这样做的目的是帮助开发者发现副作用中的问题，比如： > 3. redux为啥能减少rerender

Redux 能减少不必要 rerender，核心是它的“订阅机制+selector+浅比较”。  
首先，组件不会直接订阅整个 store，而是通过 useSelector 订阅自己关心的那一小部分 state。  
当 store 更新时，Redux 会重新执行 selector，然后用浅比较（=== 或 shallowEqual）去对比前后的结果，如果没有变化，就不会触发组件重新渲染。  
另外 Redux 强调不可变更新，这样每次 state 变化都会产生新的引用，React 可以通过引用比较快速判断哪些数据变了，从而减少不必要的更新。  
Ai agent VS prompt engineering 普通 prompt 调用更像一次性的问答，输入一个问题得到一个结果，本质是 stateless 的。而 AI Agent 通常是有目标的，它会结合上下文去做规划，并且可以多步执行任务。所以 Agent 更像一个“会思考和行动的系统”，而不是简单的文本生成工具。  
React和unity模拟动物森友会，前端后端选啥，怎么做前端做一个动画，从js到出现在浏览器上经过了什么，穿插了打包一堆ai agent要我介绍实现流程的问题追问：如果用户给的信息品牌没办法match上，match可能出错怎么办，回答了两层：匹配+确认&索引  
React native比ract快的原因是啥？我回答我体感慢，扯到bridge，fiber，react和native，提到swift 和flutter
---
## Chunk 527 — //sdk.js

//sdk.js

//============================//1.设计的分片数据结构,  
//============================
---
## Chunk 528 — //请在这里设计你的分片数据结构类型

//请在这里设计你的分片数据结构类型

type Chunk = {//TODO: 后端给我返回什么数据 const String chunks }  
//============================//2. 流式对话渲染组件主体//============================  
class StreamingMarkdownRenderer {/** * @param {Function} renderFn - 用于将完整 Markdown 文本渲染到页面的函数 */constructor(renderFn) {//TODO: 保存渲染函数，初始化内部状态 let results = "" }  
/** * 当收到一个新的分片时调用，分片进行和渲染、处理异常 case * 不考虑换行、分片、一段会话结束后不需要保留历史记录 * @param {any} chunk - 使用你自己设计的分片结构 * */onChunk(chunks) {//TODO:进行增量渲染 for (const chunk of chunks){ setTimeout(() => { results+= chunk renderFn(chunks) }, 1000) }  
return results } }
---
## Chunk 529 — //out.js

//out.js

import React, { useState, useEffect } from 'react'  
function ChatView() { const [md, setMd] = useState('')  
//传给 StreamingMarkdownRenderer 的渲染函数 const renderMarkdownToDOM = (mdText) => { setMd(mdText) }  
useEffect(() => { const renderer = new StreamingMarkdownRenderer(renderMarkdownToDOM) evtSource.onmessage = (data) => { renderer.onChunk(data) } }, [])  
//这里为了简单，直接用 <pre> 输出 Markdown 文本本身（不做真正的 Markdown 解析） return <pre>{md}</pre> }  
ai学习笔记（langchain+python）
---
## Chunk 530 — LangChain

LangChain

LCEL链条表达式保存历史记录：只有一个基于内存的inMemoryChatHistory组件，但是因为这个是基于内存的，所以实际上生产中不太够用。
---
## Chunk 531 — 重要的部分是大模型的回答往往是不稳定的，怎么让模型回复更加稳定

重要的部分是大模型的回答往往是不稳定的，怎么让模型回复更加稳定

Tools：允许ai调用本地的业务接口，对工具的声明要非常谨慎。
---
## Chunk 532 — 如何让大模型知道要调用哪个工具？

如何让大模型知道要调用哪个工具？

1. 写@tools注解：1. 这个方法是干嘛的，2. 这个方法的参数是啥。这样大模型才能够理解他要去调用哪个tool
---
## Chunk 533 — 如何让大模型知道要调用哪个工具？ > 2. 用StructuredTool_from_function

如何让大模型知道要调用哪个工具？ > 2. 用StructuredTool_from_function

Langchain这种框架，应用层变得非常简单，但是缺的是用这个框架把工作做活的人。  
文本向量化：用redis/数据库把文本向量化的数据持久化 retriver，可以加入LCEL链式表达式  
微调：成本很高 RAG分为两个阶段：indexing索引阶段和retriveal检索增强阶段 Index：把文档处理成知识库，把text转成segment，然后用embedding model把它转成向量，保存到向量数据库里具体操作流程：  
1. 加载文档，textLoader，baseLoader 2. 切分文档，textSplitter 3. 文本向量化：构建向量化模型，然后构建向量数据库，把数据存到向量数据库当中 Retriveal检索增强：用retriver从向量数据库里找top k个近似向量，然后写一个prompt template （调用的时候fill这个template），调用LLM（实际上用LCEL语法链把它们整合起来） ai大模型的思想比实现重要
---
## Chunk 534 — 如何验证RAG应用的质量？

如何验证RAG应用的质量？

自动化测试：构造样本集，有Q和A，然后让RAG回答出来一个A‘，最后看A和A’的相似度召回率：A有4个点，那么A’回答出来几个精确率：对于A’回答出来的几个点，有哪些是正确的，哪些不正确  
如何提升RAG应用的质量？数据获取阶段：数据质量，比如爬虫要去掉header和footer，比如把图片用ocr识别，把表格做成markdown 检索阶段：  
1. 对用户的问题做拆分，如果用户一次问n个问题，对小的问题做rag然后再整合 2. 对用户的问题进行转写，如果用户的问题很复杂，那可以把它拆成不同的步骤 3. 对检索出来的问题做重排序，把重要的信息放在前面（比如阿里的深度文本重排序就是把 rag检索出来的信息做重新排序）
---
## Chunk 535 — Python并发编程：多线程，多进程，多协程

Python并发编程：多线程，多进程，多协程

多线程：适合处理IO密集型任务，比如读写数据库多进程：处理CPU密集型任务，比如递归计算/加密解密，正则匹配
---
## Chunk 536 — 线程池好处（进程池也差不多）

线程池好处（进程池也差不多）

1. 提升性能：因为减少了大量新建，终止线程的开销，可以复用线程资源 2. 规定了一定数量的线程上限，不会无限增加线程，程序不会崩溃  
使用场景：适合突发需要处理大量请求或者大量线程来完成任务，但是每个任务的实际完成时间比较短  
使用方法：线程池：from cuncurrent.futures import ThreadPoolExecutor as pool 两个用法：
---
## Chunk 537 — 线程池好处（进程池也差不多） > 1. Map函数 2. Future模式

线程池好处（进程池也差不多） > 1. Map函数 2. Future模式

a. For future in futures 按顺序 b. For future in as_completed 哪个任务先结束就先返回  
FastAPI: 异步框架，本来就是为了前后端分离制作的可以自动生成交互式文档
---
