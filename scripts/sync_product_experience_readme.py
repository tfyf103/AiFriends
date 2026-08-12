from pathlib import Path

ZH_PATH = Path("README.md")
EN_PATH = Path("README_EN.md")

ZH_MARKER = "# 🧭 实际产品体验：用户真正怎么使用 AiFriends？"
EN_MARKER = "# 🧭 Product experience: what does a user actually do?"

ZH_SECTION = r'''# 🧭 实际产品体验：用户真正怎么使用 AiFriends？

> **这部分按产品行为写，而不是按技术名词写。** 完整的用户旅程、证据等级和“线上已观察 / Browser E2E 已验证 / 源码实现 / 依赖配置”边界见 [Product Experience / 实际产品体验](./docs/PRODUCT_EXPERIENCE.md)。

从用户视角看，AiFriends 更接近一个轻量的 **AI Character 社区 + 持续关系型 AI 伙伴系统**：

```text
浏览 / 搜索公开 Character
          ↓
查看创作者空间
          ↓
注册 / 登录
          ↓
点击一个 Character
          ↓
自动创建或复用 Friend 关系
          ↓
打开角色专属聊天窗口
          ↓
文本 / 可选语音输入
          ↓
SSE 流式文本 + 可选流式语音
          ↓
Message 持久化
          ↓
以后回来继续同一段关系 / Memory / Tool / RAG
```

## 用户能直接感受到的功能

| 用户动作 | 实际产品行为 | 证据 |
| --- | --- | --- |
| **发现角色** | 首页加载公开 Character，支持搜索与无限加载，并展示头像、背景、名称、人格简介和作者 | **Production observed** |
| **查看创作者** | 公开用户空间展示用户资料与其创建的 Character | **Production observed** |
| **注册 / 登录** | JWT + Refresh Cookie；受保护路由需要登录，刷新后可恢复认证 | **Production + Browser E2E** |
| **开始聊天** | 点击 Character 后自动 `get_or_create` Friend，不是每次创建一段孤立会话 | **Source implemented** |
| **管理 AI 伙伴** | `/friend` 是已有 Friend/聊天伙伴列表，可再次打开聊天或移除关系 | **Browser E2E + Source** |
| **角色专属聊天** | Chat Modal 使用 Character 自己的聊天背景，加载历史 Message，SSE 增量显示回复 | **Source implemented** |
| **停止生成** | 前端 `AbortController` 真正终止活跃 SSE，请求取消会继续传递到后端 worker | **Source implemented** |
| **创建自己的 Character** | 上传头像、名称、角色设定、Voice、聊天背景；之后可更新或删除 | **Source implemented** |
| **维护个人身份** | 可编辑头像、用户名、简介，并在公开用户空间作为 Character 作者展示 | **Source implemented** |
| **长期记忆 / Agent / RAG / Voice** | 发生在同一个聊天体验背后，不额外制造“AI 功能演示页” | **Source implemented + Config-dependent** |

### 一个关键产品设计：`Character` 和 `Friend` 不是同一件事

```text
Character.profile = 这个 AI 角色是谁
Friend             = 某个 User 与这个 Character 的长期关系
Friend.memory      = 这个 Character 记住了这个 User 什么
```

所以 AiFriends 的核心并不是“一次 Prompt 得到一次回答”，而是让同一个用户能够**发现角色、建立关系、持续聊天、让关系产生历史和记忆，同时也能创造自己的角色**。

### AI 能力如何映射到用户体验

- **Streaming**：回答边生成边出现，而不是等待整段答案；
- **Memory**：再次回来和同一个 Friend 聊天时，长期关系状态可以继续发挥作用；
- **Tool Calling**：模型在聊天背后决定是否调用时间、知识库等工具；
- **RAG**：知识库检索发生在回答背后，目标是让回复使用外部 evidence，而不是给用户看一个向量数据库页面；
- **ASR / TTS**：开启语音 Provider 后，可从麦克风输入并连续播放语音回复；
- **`mock` / `text` / `full`**：同一套产品 UI，通过运行模式逐步开启真实模型、RAG 与 Speech，而不是维护三套 Demo。

> **证据边界：** 真实公网截图证明公开部署；Browser E2E 证明维护版登录态跨层链路；源码证明维护中的产品能力；RAG/ASR/TTS 等能力是否在某次公网访问中开启，仍以实际部署 Feature Flag / Provider 配置为准。

---

'''

EN_SECTION = r'''# 🧭 Product experience: what does a user actually do?

> **This section is organized by product behavior, not framework names.** See [Product Experience](./docs/PRODUCT_EXPERIENCE.md) for the complete user journey, evidence matrix, and the distinction between production-observed, Browser-E2E-verified, source-implemented, and configuration-dependent capabilities.

From a user's perspective, AiFriends is closer to a lightweight **AI Character community + persistent companion system** than to a blank chatbot box:

```text
Browse / search public Characters
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
Return later to the same relationship / Memory / Tools / RAG
```

## User-visible behavior

| User action | Product behavior | Evidence |
| --- | --- | --- |
| **Discover Characters** | Public Character cards, search, incremental loading, persona and creator information | **Production observed** |
| **Open creator space** | Public profile plus the Characters created by that user | **Production observed** |
| **Register / sign in** | JWT + refresh cookie; protected routes and auth restoration after reload | **Production + Browser E2E** |
| **Start a conversation** | Clicking a Character creates or reuses a Friend relationship rather than a disposable chat | **Source implemented** |
| **Manage companions** | `/friend` is the persistent Friend/companion list and can reopen or remove relationships | **Browser E2E + Source** |
| **Character-specific chat** | Chat modal uses the Character background, loads Message history, and streams reply deltas | **Source implemented** |
| **Stop generation** | `AbortController` terminates the active SSE request and cancellation propagates toward backend work | **Source implemented** |
| **Create Characters** | Avatar, name, persona, Voice and chat background, with later update/remove controls | **Source implemented** |
| **Maintain creator identity** | Edit avatar, username and profile used by public creator spaces | **Source implemented** |
| **Memory / Agents / RAG / Voice** | Runtime intelligence behind the same chat UX rather than separate showcase pages | **Source implemented + Config-dependent** |

### A key product distinction: `Character` is not `Friend`

```text
Character.profile = who this AI persona is
Friend             = the persistent User–Character relationship
Friend.memory      = what this Character remembers about this User
```

The core product is therefore not “one prompt, one answer.” It is a loop where a user can **discover a persona, establish continuity, return to the same relationship, accumulate history/memory, and also publish their own Characters**.

### How AI capabilities surface in the product

- **Streaming**: the answer appears incrementally instead of after full generation;
- **Memory**: returning to the same Friend can preserve relationship state;
- **Tool Calling**: the agent can invoke time or knowledge tools behind the conversation;
- **RAG**: retrieval enriches answers with external evidence instead of exposing a vector-database UI;
- **ASR / TTS**: configured speech providers enable microphone input and continuous spoken replies;
- **`mock` / `text` / `full`**: one maintained product UI progressively enables real models, retrieval and speech instead of maintaining three unrelated demos.

> **Evidence boundary:** production screenshots prove the public deployment; Browser E2E proves maintained authenticated cross-layer behavior; source proves maintained capabilities; whether RAG/ASR/TTS are enabled on a particular production visit still depends on deployment feature flags and providers.

---

'''


def insert_once(text: str, marker: str, anchor: str, section: str) -> str:
    if marker in text:
        return text
    if anchor not in text:
        raise RuntimeError(f"README anchor not found: {anchor}")
    return text.replace(anchor, section + anchor, 1)


def main() -> None:
    zh = ZH_PATH.read_text(encoding="utf-8")
    en = EN_PATH.read_text(encoding="utf-8")

    zh = insert_once(zh, ZH_MARKER, "# 为什么做 AiFriends？", ZH_SECTION)
    en = insert_once(en, EN_MARKER, "# Why AiFriends?", EN_SECTION)

    zh = zh.replace(
        "`COURSE_REBUILD` 等真实历史工程考古资料仍可能以中文为主，但已经不影响英文用户完成完整核心课程。",
        "`COURSE_REBUILD.md` 与 `COURSE_REBUILD_EN.md` 已形成中英文双轨，英文用户可以沿同一组真实 Git 历史 checkpoint 完成工程考古学习。",
    )

    ZH_PATH.write_text(zh, encoding="utf-8")
    EN_PATH.write_text(en, encoding="utf-8")


if __name__ == "__main__":
    main()
