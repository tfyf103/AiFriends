# AiFriends Bilingual Engineering Glossary / 双语工程术语表

**English** | **简体中文**

This glossary is the terminology baseline for AiFriends documentation, Labs, screenshots, issue/PR discussions, and future translations. / 本术语表是 AiFriends 中英文文档、Labs、截图、Issue/PR 讨论和后续翻译的统一术语基线。

> The goal is consistency, not forced literal translation. Code identifiers such as `Character`, `Friend`, `Message`, `AI_MODE`, `ToolNode`, and `Request-ID` should normally stay unchanged when they refer to concrete source concepts. / 目标是保持一致，而不是逐字硬译。当术语对应源码中的具体概念时，通常保留代码标识符本身。

---

## Product domain / 产品领域

| Canonical term | 中文推荐 | Meaning in AiFriends / 在 AiFriends 中的含义 |
|---|---|---|
| **Character** | AI 角色 / 角色 | A reusable AI persona with profile, visual assets, and optional voice. Do not translate it as “user”. / 可复用的 AI 人设实体，不等同于用户。 |
| **Friend** | 好友关系 / Friend 关系 | The relationship between one user and one Character. It is **not another human account**. / 用户与某个 Character 之间的关系实体，不是另一个真人账号。 |
| **Message** | 消息 / 对话记录 | Persisted chat exchange and token/accounting metadata. / 持久化的聊天记录及相关 token 元数据。 |
| **UserProfile** | 用户资料 | Application-level profile attached to the authenticated user. / 与登录用户关联的应用层资料。 |
| **SystemPrompt** | 系统提示词 | Maintained prompt instructions used by chat or memory flows. / Chat 或 Memory 流程使用的系统级提示。 |
| **Voice** | 音色 / Voice | Provider-facing voice configuration used by TTS. / TTS 使用的供应商音色配置。 |

---

## AI runtime / AI 运行时

| Canonical term | 中文推荐 | Usage note / 使用说明 |
|---|---|---|
| **Mock mode** | Mock 模式 / 模拟模式 | `AI_MODE=mock`; deterministic local learning path with no external AI credentials. / 无需外部 AI 凭证的确定性学习模式。 |
| **Text mode** | Text 模式 / 文本模式 | `AI_MODE=text`; real chat model path without making speech mandatory. / 使用真实聊天模型，但语音不是成功前置条件。 |
| **Full mode** | Full 模式 / 完整模式 | `AI_MODE=full`; chat + optional RAG/ASR/TTS according to feature flags/provider config. |
| **Feature flag** | 功能开关 | Environment-controlled capability switch such as `ENABLE_RAG`. / 例如 `ENABLE_RAG` 的环境变量能力开关。 |
| **Provider** | 服务供应商 / Provider | External model, embedding, ASR, or TTS service implementation. |
| **Chat model** | 聊天模型 | The model that produces conversational/agent responses. |
| **Embedding** | 向量表示 / Embedding | Numeric representation used for semantic retrieval. / 用于语义检索的数值向量表示。 |

---

## Agent, RAG, and memory / Agent、RAG 与记忆

| Canonical term | 中文推荐 | Usage note / 使用说明 |
|---|---|---|
| **Agent** | 智能体 / Agent | LLM-driven decision loop that may call tools before answering. / 可在回答前主动选择工具的模型决策循环。 |
| **Tool Calling** | 工具调用 | Model emits tool calls; application executes them and returns results. / 模型选择工具，应用负责真正执行。 |
| **Tool** | 工具 | Permissioned callable capability exposed to the Agent. |
| **ToolNode** | ToolNode | LangGraph node that executes tool calls. Keep the code name unchanged. |
| **Long-term Memory** | 长期记忆 | Compressed/stable information stored in `Friend.memory`; not raw chat history. / `Friend.memory` 中的压缩稳定信息，不等同于原始聊天记录。 |
| **Short-term context** | 短期上下文 | Recent messages included directly in the current prompt/context. |
| **RAG** | 检索增强生成 | Retrieval-Augmented Generation: retrieval evidence is supplied to generation. |
| **Retrieval** | 检索 | Fetch relevant evidence before generation. / 在生成前查找相关证据。 |
| **Chunk** | 文本块 / Chunk | A smaller document segment used for embedding and retrieval. |
| **Vector store** | 向量数据库 / 向量存储 | Storage/retrieval layer for embedding vectors; LanceDB is the current example. |
| **Source / citation metadata** | 来源 / 引用元数据 | Metadata identifying the evidence source; avoid leaking private filesystem paths. |

---

## Web and streaming / Web 与流式工程

| Canonical term | 中文推荐 | Usage note / 使用说明 |
|---|---|---|
| **SSE** | 服务器发送事件 / SSE | Server-Sent Events; one HTTP response streams incremental events to the browser. |
| **Streaming response** | 流式响应 | Response delivered incrementally instead of waiting for one complete body. |
| **Cancellation** | 取消 / 取消传播 | User/browser abort signal propagated toward backend workers. |
| **AbortController** | AbortController | Browser API used to stop the active request; keep API name unchanged. |
| **single-flight refresh** | 单飞刷新 / 单次并发刷新 | Multiple failed requests share one refresh operation instead of refreshing in parallel. |
| **JWT** | JWT / JSON Web Token | Authentication token used for API authorization. |
| **access token** | access token / 访问令牌 | Short-lived token used on API requests. |
| **refresh token** | refresh token / 刷新令牌 | Longer-lived credential used to obtain a new access token. |
| **Request ID** | 请求 ID | Per-request trace identifier exposed through `X-Request-ID`. |
| **Health endpoint** | 健康检查接口 | Operational endpoint such as `/api/health/`. |

---

## Speech / 语音

| Canonical term | 中文推荐 | Usage note / 使用说明 |
|---|---|---|
| **ASR** | 自动语音识别 | Automatic Speech Recognition: speech → text. |
| **TTS** | 语音合成 | Text To Speech: text → audio. |
| **PCM** | PCM 音频 | Raw/uncompressed sample representation used in the speech input path. |
| **WebSocket** | WebSocket | Bidirectional connection used by provider-facing speech flows. |
| **MediaSource** | MediaSource | Browser API for incrementally appending media bytes. |
| **SourceBuffer** | SourceBuffer | MediaSource buffer receiving audio chunks. |

---

## Testing and maintenance / 测试与维护

| Canonical term | 中文推荐 | Usage note / 使用说明 |
|---|---|---|
| **unit test** | 单元测试 | Isolated behavior test for a function/module. |
| **behavior test** | 行为测试 | Test the externally visible contract rather than implementation details. |
| **Browser E2E** | 浏览器端到端测试 | Real browser crosses frontend + HTTP + backend + database boundaries. |
| **structural grader** | 结构化验收器 | Repository/course checker used for Chapter acceptance. |
| **migration drift** | Migration 漂移 | Model changes that are not represented by committed migration files. |
| **documentation drift** | 文档漂移 | Docs no longer match source paths, commands, paired translations, or current behavior. |
| **bilingual drift** | 双语文档漂移 | Chinese/English document structure diverges or one side disappears/moves. |
| **CI** | 持续集成 / CI | Automated checks executed on clean runners before merge. |
| **learning image** | 教学镜像 | Reproducible Docker image for learning; not a production-security guarantee. |

---

## Preferred style rules / 推荐写法

1. **Keep source identifiers literal.** Write `Friend.memory`, `AI_MODE`, `ToolNode`, `AbortController`, `X-Request-ID` exactly when referring to code.
2. **Define abbreviations once.** The first appearance can use `Server-Sent Events (SSE)` / `服务器发送事件（SSE）`; later use `SSE`.
3. **Do not equate Friend with a human friend account.** Prefer “Friend relationship” / “Friend 关系”.
4. **Do not equate RAG with a vector database.** RAG includes loading/chunking/embedding/retrieval/context/generation; LanceDB is only one layer.
5. **Do not call raw Message persistence long-term memory.** `Friend.memory` is a distinct compressed memory layer.
6. **Use “production deployment” only for the actual hosted application.** `Dockerfile.learning`, SQLite, and Django `runserver` remain learning references.
7. **Use “real screenshot” only for an image captured from a real runtime/deployment.** Generated mockups must be labeled as mockups.
8. **Use neutral provider language in maintained docs.** Historical model/provider names can remain in archaeology sections, but current instructions should prefer configurable environment variables.

---

## Translation contribution checklist / 翻译贡献检查表

Before merging a bilingual documentation change / 合并双语文档前：

- [ ] The paired Chinese/English page exists.
- [ ] Code paths and commands still exist on `main`.
- [ ] Canonical domain terms follow this glossary.
- [ ] Historical behavior is labeled as historical when it differs from current `main`.
- [ ] Screenshots are identified as live/local/generated correctly.
- [ ] Relative links and image paths resolve.
- [ ] `python scripts/check_i18n.py` passes.
- [ ] If a user-visible flow changed, update or extend Browser E2E where practical.

Related resources:

- [Chinese learning hub](./README.md)
- [English learning hub](./README_EN.md)
- [English Git-history rebuild course](./COURSE_REBUILD_EN.md)
- [Screenshot & GIF guide](./SCREENSHOTS.md)
