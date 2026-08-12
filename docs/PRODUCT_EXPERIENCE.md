# AiFriends Product Experience / 实际产品体验

[简体中文](#中文版) | [English](#english-version)

> This document explains **what AiFriends feels like as a real product**, not only which frameworks exist in the repository. It also separates what has been observed on the public deployment, what is verified by Browser E2E, what is implemented in source code, and what depends on runtime configuration.
>
> 本文回答的不是“仓库用了哪些技术”，而是：**作为一个真实用户，AiFriends 到底能做什么、每一步会经过什么产品路径，以及这些能力被什么证据验证。**

---

# 中文版

## 1. 先看结论：AiFriends 不是一个聊天输入框 Demo

从用户视角看，AiFriends 更接近一个轻量的 **AI Character 社区 + 个性化 AI 伙伴系统**：

```text
发现公开 Character
        ↓
查看创作者空间
        ↓
注册 / 登录
        ↓
点击一个 Character
        ↓
自动建立或复用 Friend 关系
        ↓
进入角色专属聊天窗口
        ↓
文本 / 语音输入
        ↓
SSE 流式回复 + 可选连续语音播放
        ↓
Message 持久化
        ↓
后续对话继续使用上下文 / Memory / Tool / RAG
```

与此同时，登录用户也可以从“使用者”变成“创作者”：</n
```text
创建 Character
   ↓
上传头像
   ↓
填写名称与角色设定
   ↓
选择 Voice
   ↓
设置聊天背景
   ↓
发布到自己的用户空间
   ↓
继续更新或删除自己创建的 Character
```

这意味着 AiFriends 的产品核心不是单次 Prompt，而是三个长期存在的实体：

```text
User        = 谁在使用系统
Character   = AI 角色是谁
Friend      = 某个 User 与某个 Character 的长期关系
```

`Friend` 是整个产品体验非常关键的一层：聊天历史、长期记忆和“这个角色认识这个用户到什么程度”都围绕这条关系展开。

---

## 2. 证据等级：哪些是线上看到的，哪些是代码能力？

为了避免把“源码存在”写成“生产环境已经亲测”，AiFriends 的功能介绍使用以下四级证据：

| 标记 | 含义 | 可以说明什么 |
|---|---|---|
| **Production observed** | 已在真实公网部署中观察 | 页面/公开内容确实在线运行 |
| **Browser E2E verified** | 真实 Chromium 跨前后端执行通过 | 登录态、路由、API、数据库等真实链路可工作 |
| **Source implemented** | 当前 `main` 有明确前后端实现 | 功能属于维护中的产品代码，而不是路线图概念 |
| **Config-dependent** | 需要模型、Embedding、ASR/TTS 等配置 | 代码支持，但具体部署是否启用取决于 Feature Flag / Provider |

这四种证据是互补关系，而不是高低好坏关系。例如 RAG 和 TTS 很可能属于 **Source implemented + Config-dependent**，不能仅凭源码就声称某次线上访问一定启用了它们。

---

## 3. 访客体验：先发现角色，再决定和谁聊天

**Evidence: Production observed + Source implemented**

AiFriends 首页不是静态介绍页，而是公开 AI Character 的发现页。

当前实现会：

- 从 `/api/homepage/index/` 获取公开 Character；
- 支持关键词搜索；
- 使用 `IntersectionObserver` 无限加载更多角色；
- 每张卡片展示角色背景图、头像、名称和人格简介；
- 展示 Character 作者，并可进入作者的公开用户空间。

对应实现：

- `frontend/src/views/homepage/HomepageIndex.vue`
- `frontend/src/components/character/Character.vue`

真实生产截图：

![AiFriends live homepage](./assets/live-demo/homepage.png)

因此一个新用户第一次进入 AiFriends 时，产品动作不是“先配置 API”，而是像浏览一个角色社区一样先看有哪些 AI 人设可以互动。

---

## 4. 公开用户空间：Character 也有创作者归属

**Evidence: Production observed + Source implemented**

点击 Character 卡片下方的作者，可以进入：

```text
/user/space/:user_id
```

这个页面同时展示：

- 用户头像与资料；
- 该用户创建的 Character；
- Character 列表继续按分页/无限加载方式获取。

对应实现：

- `frontend/src/views/user/space/SpaceIndex.vue`

真实生产截图：

![AiFriends live public user space](./assets/live-demo/public-profile.png)

这让 AiFriends 不只是“系统预置几个机器人”，而是具备用户创作 Character 并公开展示的产品结构。

---

## 5. 注册、登录与登录状态恢复

**Evidence: Production observed + Browser E2E verified + Source implemented**

真实线上部署已经验证登录与注册页面可访问；仓库 Browser E2E 进一步真实执行：

```text
打开注册页面
   ↓
填写浏览器表单
   ↓
Vite Proxy
   ↓
Django / DRF 注册 API
   ↓
SQLite 创建用户
   ↓
进入登录态
   ↓
访问受保护 /friend
   ↓
刷新浏览器
   ↓
Refresh Token 恢复认证
   ↓
继续停留在 /friend
```

对应路由：

- `/user/account/register`
- `/user/account/login`
- `/user/profile`
- `/friend`
- `/create`

对应验证：

- `e2e/browser-smoke.mjs`
- `frontend/src/router/index.js`

登录态并不是“前端写了一个布尔变量”：它真实跨越 Vue、JWT、Refresh Cookie、DRF 和数据库。

---

## 6. 点击 Character：不是跳页面，而是建立一段关系

**Evidence: Source implemented**

Character 卡片最重要的交互是点击本身。

如果用户未登录：

```text
点击 Character
   ↓
跳转登录
```

如果已经登录：

```text
点击 Character
   ↓
POST /api/friend/get_or_create/
   ↓
根据 User + Character 获取或创建唯一 Friend
   ↓
打开 ChatField 对话弹窗
```

对应实现：

- `frontend/src/components/character/Character.vue`
- `backend/web/friend/` 相关 View / Model

这一步很重要，因为用户不是每次点击都创建一段新聊天，而是在回到“我和这个 Character 已经存在的关系”。

---

## 7. Friend 页面：你的 AI 伙伴列表

**Evidence: Browser E2E verified + Source implemented**

登录后的 `/friend` 是持续关系入口，而不是公开角色广场。

当前页面会：

- 拉取当前用户已有 Friend；
- 继续显示对应 Character 卡片；
- 支持无限加载；
- 可以移除 Friend；
- 点击任意 Friend 对应 Character 再次打开聊天。

对应实现：

- `frontend/src/views/friend/FriendIndex.vue`

从产品语义上看：

```text
Homepage = 我可以认识谁？
Friend   = 我已经在和谁建立长期关系？
```

这也是 AiFriends 与“每次打开就是一个空白聊天框”的典型 Chat UI 最大区别之一。

---

## 8. ChatField：角色自己的视觉聊天空间

**Evidence: Source implemented**

聊天不会切换到一个完全通用的聊天页面，而是在 Character 卡片上打开 Modal。

聊天窗口会：

- 使用 Character 的 `background_image` 作为对话背景；
- 展示该 Character 的视觉信息；
- 加载历史 Message；
- 自动滚动到最新消息；
- 提供文本输入和麦克风入口。

对应实现：

- `frontend/src/components/character/chat_field/ChatField.vue`
- `frontend/src/components/character/chat_field/chat_history/`
- `frontend/src/components/character/chat_field/input_field/`

因此“聊天背景”不是创建 Character 时一个无意义的上传字段，它直接成为用户与这个 Character 对话时的视觉空间。

---

## 9. 文本聊天：边生成边显示，而不是等完整答案

**Evidence: Source implemented**

发送消息后，前端先立即插入：

```text
User Message
AI Empty Message
```

随后通过 SSE 持续接收增量内容：

```text
POST /api/friend/message/chat/
        ↓
      SSE
        ↓
content delta
        ↓
追加到最后一条 AI Message
```

用户体验上表现为 AI 文本逐步出现，而不是等待整个回答结束后一次性刷新。

同时当前实现已经使用真实 `AbortController`：关闭聊天或停止生成时，浏览器会真正终止活跃 SSE 请求，而不只是“在 UI 上忽略后续字符”。

对应实现：

- `frontend/src/components/character/chat_field/input_field/InputField.vue`
- `frontend/src/js/http/streamApi.js`
- `backend/web/friend/message/` 聊天流实现

---

## 10. 语音体验：输入和回复是两条不同链路

**Evidence: Source implemented + Config-dependent**

### 语音输入

用户可以从文本输入框切换到麦克风模式：

```text
Browser microphone
   ↓
VAD
   ↓
PCM audio
   ↓
WebSocket ASR
   ↓
transcript
   ↓
作为聊天消息发送
```

### 语音回复

当部署开启 TTS 时：

```text
LLM text
   ↓
TTS audio chunks
   ↓
Base64 over SSE
   ↓
MediaSource / SourceBuffer
   ↓
浏览器连续播放
```

也就是说，AiFriends 的 Voice 不是“回答完以后再下载一个 mp3 文件”，而是设计成与流式文本并行到达浏览器。

相关能力受以下配置控制：

- `ENABLE_ASR`
- `ENABLE_TTS`
- Provider / model / WebSocket endpoint

因此某个公开部署是否开启完整语音能力，应以该部署配置为准。

---

## 11. 创建 Character：用户可以真正设计自己的 AI 人设

**Evidence: Source implemented**

登录后访问 `/create`，当前创建表单要求：

- **头像**；
- **名称**；
- **Voice**；
- **角色介绍 / 人格设定**；
- **聊天背景**。

创建成功后会回到自己的用户空间。

对应实现：

- `frontend/src/views/create/CreateIndex.vue`
- `frontend/src/views/create/character/CreateCharacter.vue`

这五类数据不是纯展示信息：

```text
头像 / 名称     → Character identity
角色介绍         → Character profile / persona
Voice            → TTS personality
聊天背景         → ChatField visual context
作者             → Public creator ownership
```

---

## 12. Character 不是一次性内容：可以继续更新和删除

**Evidence: Source implemented**

当 Character 属于当前登录用户时，卡片会显示编辑/删除入口。

更新页面：

```text
/create/character/update/:character_id/
```

可以重新修改：

- 头像；
- 名称；
- Voice；
- 角色介绍；
- 聊天背景。

对应实现：

- `frontend/src/views/create/character/UpdateCharacter.vue`
- `frontend/src/components/character/Character.vue`

这使 AiFriends 的 Character 更接近一个可持续维护的内容实体，而不是一次提交后不可修改的 Prompt 模板。

---

## 13. 用户资料：创作者身份也可以维护

**Evidence: Source implemented**

登录用户可以在 `/user/profile` 修改：

- 用户头像；
- 用户名；
- 个人简介。

这些资料会继续出现在公开用户空间和 Character 作者信息中。

对应实现：

- `frontend/src/views/user/profile/ProfileIndex.vue`

---

## 14. Memory：用户看不到一个“记忆数据库页面”，但会影响以后聊天

**Evidence: Source implemented + Config-dependent**

AiFriends 把“角色是谁”和“角色记住了这个用户什么”分开：

```text
Character.profile = 这个 AI 角色的稳定人格
Friend.memory     = 这个 Character 对当前 User 的长期记忆
```

长期记忆通过历史 Message 与旧 Memory 更新，而不是把所有历史消息无限塞进每次 Prompt。

用户侧真正感受到的不是一个 Memory 管理后台，而是：

> 再次回来和同一个 Character 聊天时，它拥有一条属于“你和它”的持续关系状态。

---

## 15. Agent / Tool Calling：部分能力发生在聊天背后

**Evidence: Source implemented + Config-dependent**

LangGraph 会让模型根据对话决定是否调用工具：

```text
START
  ↓
agent
  ↓
需要 Tool？
  ├─ 否 → END
  └─ 是 → ToolNode → agent
```

当前示例工具包括：

- 当前时间；
- LanceDB 知识库检索。

因此 Tool Calling 不是单独的“工具页面”，而是聊天回答背后的推理/编排能力。

---

## 16. RAG：它的产品价值是“让回答有外部知识”，不是展示向量数据库

**Evidence: Source implemented + Config-dependent**

当开启 RAG 时，知识链路为：

```text
Document
  ↓
Chunk
  ↓
Embedding
  ↓
LanceDB
  ↓
Retrieval
  ↓
source-aware evidence
  ↓
Agent response
```

项目已经把 Retrieval 从 Agent 编排里拆开，使检索可以独立评测。

对普通用户而言，RAG 的产品效果应该体现在“回答使用了知识库内容”；对学习者而言，则可以继续研究 Chunk、Embedding、Vector DB、Retrieval、Citation 和 Evaluation。

---

## 17. `mock` / `text` / `full`：同一套产品 UI，可以逐步学习不同 AI 深度

AiFriends 刻意没有让第一次运行就依赖所有第三方 AI 服务。

| Mode | 用户仍然能体验 | 主要缺少什么 |
|---|---|---|
| `mock` | 注册、登录、Character/Friend、真实 SSE、Message DB | 外部真实 LLM / RAG / Speech |
| `text` | 上述全部 + 真实 LLM / LangGraph / Tool / Memory | 完整 Speech，可按配置关闭 RAG |
| `full` | 完整 Chat + 可选 RAG + ASR + TTS | 取决于 Provider 与 Feature Flag |

因此教学版和产品版并不是两套代码：**同一套 Web 产品路径，通过运行模式控制外部 AI 依赖。**

---

## 18. 产品体验与工程实现的对应关系

| 用户看到/感受到的功能 | 前端入口 | 后端/AI 含义 | Evidence |
|---|---|---|---|
| 浏览公开角色 | `/` | Character discovery | Production observed |
| 搜索 Character | 顶部搜索 / `?q=` | Query filtering | Source implemented |
| 查看创作者 | `/user/space/:id` | UserProfile + Character ownership | Production observed |
| 注册 / 登录 | account routes | DRF + JWT + Refresh Cookie | Production + Browser E2E |
| 登录状态恢复 | 页面刷新 | single-flight refresh + JWT | Browser E2E verified |
| 创建角色 | `/create` | Character + Voice + media | Source implemented |
| 更新/删除角色 | user space / update route | ownership-protected CRUD | Source implemented |
| 建立 AI 好友 | 点击 Character | `Friend(me, character)` | Source implemented |
| 我的聊天伙伴 | `/friend` | Friend collection | Browser E2E + Source |
| 历史聊天 | Chat modal | Message persistence | Source implemented |
| 流式回复 | Chat modal | SSE streaming | Source implemented |
| 停止生成 | Chat input | AbortController + backend cancel | Source implemented |
| 语音输入 | Mic | VAD + WebSocket ASR | Config-dependent |
| 连续语音回复 | Chat modal | TTS + SSE audio + MSE | Config-dependent |
| 长期关系记忆 | 再次聊天时体现 | `Friend.memory` / MemoryGraph | Config-dependent |
| 工具调用 | 回答中体现 | LangGraph ToolNode | Config-dependent |
| 知识库问答 | 回答中体现 | LanceDB Retrieval / RAG | Config-dependent |

---

## 19. 不夸大线上部署：README 应该怎样理解“支持”

AiFriends 的 README 使用下面的口径：

- **真实生产截图**证明公开部署页面确实运行；
- **Browser E2E**证明维护版代码的登录态跨层链路真实通过；
- **Source implemented**证明功能属于当前维护代码；
- **Config-dependent**意味着生产环境是否启用仍取决于部署配置。

因此不会因为仓库里有 ASR/TTS/RAG 代码，就声称任意时刻访问公网部署都一定开启了所有 Provider。

这也是本项目把“真实产品”和“教学工程”放在同一仓库时坚持的证据边界。

---

# English Version

## 1. The product in one sentence

AiFriends is closer to a lightweight **AI Character community + persistent companion system** than to a one-box chatbot demo.

A typical user journey is:

```text
Discover public Characters
        ↓
Open a creator space
        ↓
Register / sign in
        ↓
Click a Character
        ↓
Create or reuse a Friend relationship
        ↓
Open that Character's visual chat space
        ↓
Text / optional voice input
        ↓
SSE streaming text + optional streaming audio
        ↓
Persist Messages
        ↓
Continue later with context / Memory / Tools / RAG
```

A signed-in user can also become a creator:

```text
Create Character
   ↓
Avatar + name + persona
   ↓
Choose Voice
   ↓
Choose chat background
   ↓
Publish in user space
   ↓
Update or remove later
```

The important product entities are:

```text
User        = who uses the system
Character   = who the AI persona is
Friend      = the persistent relationship between one User and one Character
```

---

## 2. Evidence levels

AiFriends deliberately separates implementation claims from deployment claims:

| Label | Meaning |
|---|---|
| **Production observed** | Seen on the real public deployment |
| **Browser E2E verified** | Executed through real Chromium, frontend, API and database |
| **Source implemented** | Present in maintained `main` source code |
| **Config-dependent** | Requires runtime feature flags/providers such as LLM, RAG, ASR or TTS |

A feature can have multiple labels. RAG, for example, can be both **Source implemented** and **Config-dependent**.

---

## 3. What a visitor can do

The public homepage is a Character discovery surface, not a static landing page. It loads public Character cards, supports search, incrementally loads more content, shows persona summaries, and links Characters back to their creators.

Public creator spaces expose a user profile together with the Characters that user created.

Production evidence:

- `./assets/live-demo/homepage.png`
- `./assets/live-demo/public-profile.png`

Source evidence:

- `frontend/src/views/homepage/HomepageIndex.vue`
- `frontend/src/components/character/Character.vue`
- `frontend/src/views/user/space/SpaceIndex.vue`

---

## 4. What changes after sign-in

Protected routes include profile editing, Friend management, Character creation, and Character updates.

The maintained Browser E2E executes a real cross-layer path:

```text
Browser registration form
   ↓
Vite proxy
   ↓
Django / DRF
   ↓
SQLite
   ↓
authenticated session
   ↓
protected /friend
   ↓
page reload
   ↓
refresh-token recovery
   ↓
still authenticated
```

See:

- `e2e/browser-smoke.mjs`
- `frontend/src/router/index.js`

---

## 5. Clicking a Character creates continuity

For an anonymous visitor, clicking a Character leads to sign-in.

For an authenticated user, the card calls `POST /api/friend/get_or_create/`, creates or reuses the unique User–Character Friend relationship, and opens `ChatField`.

This means a Character is not a disposable prompt. The user returns to an existing relationship.

---

## 6. The Friend page is the companion list

`/friend` loads the current user's Friend relationships, supports incremental loading, allows removing a Friend, and reopens chat from the associated Character card.

Conceptually:

```text
Homepage = who could I meet?
Friend   = who am I already talking to?
```

See `frontend/src/views/friend/FriendIndex.vue`.

---

## 7. Chat is Character-specific

`ChatField` uses the Character's `background_image`, loads message history, keeps the latest conversation in view, and provides both text and microphone entry points.

Text is streamed incrementally through SSE. The current frontend also uses a real `AbortController`, so stopping or closing an active chat aborts the browser request instead of merely hiding late output.

When TTS is enabled, audio chunks travel alongside the stream and are played continuously with `MediaSource` / `SourceBuffer`.

See:

- `frontend/src/components/character/chat_field/ChatField.vue`
- `frontend/src/components/character/chat_field/input_field/InputField.vue`

---

## 8. Character creation is a product workflow

The `/create` workflow requires:

- avatar;
- name;
- Voice;
- persona/profile;
- chat background.

The creator can later update or remove owned Characters. Their profile and Characters remain visible through the public user space.

See:

- `frontend/src/views/create/character/CreateCharacter.vue`
- `frontend/src/views/create/character/UpdateCharacter.vue`
- `frontend/src/views/user/profile/ProfileIndex.vue`

---

## 9. Memory, Tools and RAG live behind the chat UI

Not every AI capability needs a separate page.

```text
Character.profile = stable persona identity
Friend.memory     = what this Character remembers about this User
```

LangGraph Tool Calling, long-term Memory and LanceDB-backed RAG are orchestration/runtime capabilities that affect future responses inside the same chat experience.

They are **Source implemented** and can be **Config-dependent** depending on the selected AI mode and feature flags.

---

## 10. One UI, three learning/runtime depths

| Mode | What still works | External AI dependency |
|---|---|---|
| `mock` | auth, Character/Friend, real SSE, Message persistence | none |
| `text` | above + real LLM/LangGraph/Tools/Memory | chat model |
| `full` | above + optional RAG/ASR/TTS | configured providers |

The teaching experience and the product are not separate implementations. They are the same maintained Web path with progressively enabled AI dependencies.

---

## 11. Product-to-engineering map

| User-facing behavior | Engineering meaning | Evidence |
|---|---|---|
| Discover Characters | homepage API + infinite loading | Production observed |
| Search Characters | query-driven discovery | Source implemented |
| Open creator space | UserProfile + Character ownership | Production observed |
| Register / sign in | DRF + JWT + refresh cookie | Production + Browser E2E |
| Survive page reload | token refresh / auth restoration | Browser E2E verified |
| Create/update Character | media + persona + Voice CRUD | Source implemented |
| Start a relationship | unique Friend(User, Character) | Source implemented |
| Open companion list | Friend collection | Browser E2E + Source |
| Stream a reply | SSE + cancellation | Source implemented |
| Voice input | VAD + WebSocket ASR | Config-dependent |
| Voice reply | TTS + SSE audio + MSE | Config-dependent |
| Remember the user | Friend.memory / MemoryGraph | Config-dependent |
| Use tools | LangGraph ToolNode | Config-dependent |
| Retrieve knowledge | LanceDB RAG | Config-dependent |

---

## 12. What the project does **not** overclaim

A source-code capability is not automatically claimed as enabled on every production visit.

- real production screenshots prove the public deployment;
- Browser E2E proves maintained authenticated cross-layer behavior;
- source evidence proves an implemented product path;
- runtime/provider-dependent AI features are labeled as such.

That evidence boundary is part of the project's engineering quality, not a limitation of the product description.

---

## Related

- [Live Demo Verification](./LIVE_DEMO.md)
- [Screenshots & GIF Guide](./SCREENSHOTS.md)
- [Architecture](./ARCHITECTURE.md)
- [English Architecture](./ARCHITECTURE_EN.md)
- [Browser E2E](../e2e/README.md)
- [Bilingual Engineering Glossary](./BILINGUAL_GLOSSARY.md)
