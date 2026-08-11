# 🤖 AiFriends

> **从 0 学会做一个有角色、记忆、RAG 与语音能力的 AI 伙伴。**
>
> 一个基于 **Vue 3 + Django + LangChain + LangGraph + LanceDB** 的 AI 全栈学习项目，也是一套可以逐步拆解、逐步复刻的真实 AI 应用。

---

## 🌱 这个仓库适合谁？

如果你是下面任何一种情况，这个项目就是为你准备的：

- 只会一点 Python，不知道前后端怎么配合；
- 学过 Vue / Django，但没独立做过完整项目；
- 会调用大模型 API，但不知道 LangChain / LangGraph 到底解决什么；
- 听过 RAG、向量数据库、Tool Calling、Agent、长期记忆，却没有完整串起来；
- 想做 AI 陪伴、AI 角色、数字人、智能助手类项目；
- 想通过一个真实项目同时学习前端、后端和 AI 应用工程。

**零基础建议不要直接从源码最深处开始看。**

先进入：

👉 **[AiFriends 零基础学习地图](./docs/README.md)**

👉 **[从 0 开始完整复刻教程](./docs/BEGINNER_TUTORIAL.md)**

👉 **[系统架构与完整请求链路](./docs/ARCHITECTURE.md)**

👉 **[常见报错与排查手册](./docs/TROUBLESHOOTING.md)**

---

# ✨ 项目能做什么？

## 🎭 AI 角色

- 创建自己的 AI 角色；
- 设置角色名称；
- 上传头像；
- 上传聊天背景；
- 编写人格 / 世界观 / 角色设定；
- 给不同角色选择不同音色。

## 💬 智能聊天

- 自然语言对话；
- LLM 流式输出；
- 保存聊天历史；
- 最近聊天自动进入上下文；
- 保存输入 / 输出 token 用量。

## 🧠 长期记忆

- 原始聊天记录保存在数据库；
- 最近消息直接作为短期上下文；
- 每隔若干轮对话调用独立 Memory Graph；
- 把历史信息压缩后保存到 `Friend.memory`；
- 后续聊天自动把长期记忆放回系统上下文。

## 🧰 Tool Calling / Agent

当前 LangGraph Agent 可：

- 查询当前精确时间；
- 根据问题调用知识库检索工具；
- 获取 Tool 结果后回到 LLM 再生成自然语言答案。

## 📚 RAG 知识库

- TextLoader 加载原始文本；
- RecursiveCharacterTextSplitter 文本切块；
- 自定义 Embedding；
- LanceDB 保存向量；
- similarity search 检索相关片段；
- RAG 被封装成 LangChain Tool，由 Agent 自主决定是否调用。

## 🎙️ 语音

- 浏览器麦克风输入；
- PCM 音频上传；
- WebSocket ASR；
- LLM 文本流与 TTS 并行；
- TTS 二进制音频转 Base64 后通过 SSE 推到浏览器；
- 浏览器使用 MediaSource / SourceBuffer 连续播放 MP3 流。

---

# 🧠 你真正会学到什么？

AiFriends 不只是“调用一个模型 API”。

你会完整经历一条现代 AI Web 应用链路：

```text
Vue 页面
  ↓
Vue Router
  ↓
Pinia
  ↓
Axios / SSE
  ↓
JWT
  ↓
Django REST Framework
  ↓
Django ORM / SQLite
  ↓
LangChain Messages
  ↓
LangGraph Agent
  ↓
Tool Calling
  ↓
RAG / LanceDB
  ↓
Long-term Memory
  ↓
ASR / TTS WebSocket
```

如果你能从头解释清楚“一条用户消息”如何穿过这些层，你就已经掌握了 AI 全栈开发最重要的系统思维。

---

# 🏗️ 架构总览

```text
┌──────────────────────────────────────────────────────────┐
│                         Browser                          │
│ Vue 3 / Router / Pinia / Axios / SSE / MediaSource      │
└──────────────────────────┬───────────────────────────────┘
                           │ HTTP JSON / SSE
                           ▼
┌──────────────────────────────────────────────────────────┐
│                    Django + DRF                         │
│ Auth / Character / Friend / Message / Chat / Voice     │
└──────────┬───────────────────┬───────────────────────────┘
           │                   │
           ▼                   ▼
      ┌─────────┐      ┌──────────────────┐
      │ SQLite  │      │ LangChain/Graph  │
      └─────────┘      │ Agent + Memory   │
                       └────────┬─────────┘
                                │
                     ┌──────────┼──────────┐
                     ▼          ▼          ▼
                    LLM      LanceDB    Speech WS
                              RAG       ASR / TTS
```

更详细的数据流：

👉 [系统架构与完整请求链路](./docs/ARCHITECTURE.md)

---

# 🔥 一句话是怎么完成聊天的？

```text
InputField.vue
  ↓
streamApi('/api/friend/message/chat/')
  ↓
Django web/urls.py
  ↓
MessageChatView
  ↓
鉴权 + Friend 校验
  ↓
角色 System Prompt
  ↓
Friend.memory
  ↓
最近 Message 历史
  ↓
CharGraph
  ↓
LLM
  ↓
需要工具？
  ├─ 否 → 继续回答
  └─ 是 → ToolNode
            ├─ get_time
            └─ LanceDB RAG
                ↓
              再回 LLM
  ↓
astream
  ├─ 文本 chunk ─────────────► SSE ─► Vue
  └─ 文本 chunk ─► TTS WS ─► MP3 ─► SSE ─► MediaSource
  ↓
Message 落库
  ↓
每 5 条 Message 更新长期记忆
```

这是整个项目最值得反复阅读的一条链路。

---

# 🛠️ 技术栈

## Backend

| 技术 | 用途 |
|---|---|
| Python | 后端与 AI 主语言 |
| Django 6 | Web 框架 |
| Django REST Framework | API |
| Simple JWT | 用户认证 |
| SQLite | 当前开发数据库 |
| django-cors-headers | 前后端跨域 |
| WebSocket | ASR / TTS 双工通信 |
| SSE | LLM 文本与音频流式返回 |

## AI

| 技术 | 用途 |
|---|---|
| LangChain | Message、Tool、模型与向量库抽象 |
| LangGraph | Agent / Memory 工作流 |
| ChatOpenAI | OpenAI-compatible Chat API |
| OpenAI Python SDK | Embedding API |
| LanceDB | 向量数据库 |
| RecursiveCharacterTextSplitter | 文档切块 |

## Frontend

| 技术 | 用途 |
|---|---|
| Vue 3 | UI |
| Vite | 开发与构建 |
| Vue Router | SPA 路由 |
| Pinia | 全局用户状态 |
| Axios | 普通 HTTP API |
| fetch-event-source | SSE 流式聊天 |
| Tailwind CSS | 样式 |
| daisyUI | UI 组件样式 |
| MediaSource API | 流式 MP3 播放 |
| vad-web | 语音活动检测相关能力 |

---

# 📂 先记住这些核心文件

```text
AiFriends/
│
├── README.md
├── requirements.txt
├── .env.example
├── docs/
│   ├── README.md
│   ├── BEGINNER_TUTORIAL.md
│   ├── ARCHITECTURE.md
│   └── TROUBLESHOOTING.md
│
├── backend/
│   ├── manage.py
│   ├── backend/
│   │   ├── settings.py
│   │   └── urls.py
│   └── web/
│       ├── urls.py
│       ├── admin.py
│       ├── models/
│       │   ├── character.py
│       │   ├── friend.py
│       │   └── user.py
│       ├── documents/
│       │   └── utils/
│       │       ├── custom_embeddings.py
│       │       └── insert_documents.py
│       └── views/
│           └── friend/message/
│               ├── chat/
│               │   ├── chat.py
│               │   └── graph.py
│               ├── memory/
│               │   ├── graph.py
│               │   └── update.py
│               └── asr/
│                   └── asr.py
│
└── frontend/
    ├── package.json
    └── src/
        ├── main.js
        ├── router/index.js
        ├── stores/user.js
        ├── js/
        │   ├── config/config.js
        │   └── http/
        │       ├── api.js
        │       └── streamApi.js
        └── components/
            └── character/chat_field/input_field/
                └── InputField.vue
```

---

# 🚀 5 分钟了解启动流程

> 完全零基础请不要只看这一节，请直接阅读 [完整复刻教程](./docs/BEGINNER_TUTORIAL.md)。

## 1. 克隆

```bash
git clone https://github.com/tfyf103/AiFriends.git
cd AiFriends
```

## 2. Python 虚拟环境

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux：

```bash
source .venv/bin/activate
```

## 3. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

当前 Django 6.0 建议使用 Python 3.12+。

## 4. 环境变量

```bash
cp .env.example .env
```

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

填写：

```env
API_KEY=...
API_BASE=...
WSS_URL=...
```

## 5. Django

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

后端：

```text
http://127.0.0.1:8000
```

## 6. Vue

新终端：

```bash
cd frontend
npm install
npm run dev
```

前端：

```text
http://localhost:5173
```

---

# ⚙️ 环境要求

## Python

项目固定：

```text
Django==6.0.5
```

推荐：

```text
Python 3.12 / 3.13
```

## Node

`frontend/package.json` 当前要求：

```text
^20.19.0 || >=22.12.0
```

---

# 🔐 环境变量说明

| 变量 | 用途 |
|---|---|
| `API_KEY` | LLM / Embedding / ASR / TTS 服务鉴权 |
| `API_BASE` | OpenAI-compatible HTTP API 地址 |
| `WSS_URL` | ASR / TTS WebSocket 服务地址 |

仓库提供 `.env.example`，真实 `.env` 不应提交。

---

# 📚 第一次使用 RAG

因为知识库原始数据和向量存储都不会提交到 Git：

```text
backend/web/documents/data.txt
backend/web/documents/lancedb_storage
```

所以第一次需要自己创建：

```text
backend/web/documents/data.txt
```

然后：

```bash
cd backend
python manage.py shell
```

```python
from web.documents.utils.insert_documents import insert_documents
insert_documents()
```

完整原理：

👉 [零基础完整复刻教程：RAG 部分](./docs/BEGINNER_TUTORIAL.md)

---

# 🛡️ Django Admin

创建管理员：

```bash
cd backend
python manage.py createsuperuser
```

访问：

```text
http://127.0.0.1:8000/admin/
```

可以管理：

- UserProfile；
- Character；
- Voice；
- Friend；
- Message；
- SystemPrompt。

新手可以在 Admin 中快速配置 Voice 和 SystemPrompt，不需要先写额外后台页面。

---

# 📖 推荐学习路线

```text
第 1 关：跑起来
  ↓
第 2 关：Vue 页面 / Component / Router
  ↓
第 3 关：Pinia / Axios / JWT
  ↓
第 4 关：Django URL / View / Model
  ↓
第 5 关：普通聊天
  ↓
第 6 关：SSE 流式聊天
  ↓
第 7 关：LangChain Message
  ↓
第 8 关：LangGraph Agent
  ↓
第 9 关：Tool Calling
  ↓
第 10 关：长期记忆
  ↓
第 11 关：Embedding / LanceDB / RAG
  ↓
第 12 关：ASR
  ↓
第 13 关：流式 TTS
```

详细路线：

👉 [AiFriends 零基础学习地图](./docs/README.md)

---

# 🧪 新手如何正确调试？

同时打开：

```text
VS Code
浏览器 Console
浏览器 Network
Django runserver 终端
Vite 终端
```

问题按层判断：

```text
UI
 ↓
Vue State
 ↓
Network
 ↓
Django URL
 ↓
APIView
 ↓
ORM
 ↓
LLM
 ↓
Tool / RAG
 ↓
Speech Service
```

遇到错误：

👉 [常见报错与排查手册](./docs/TROUBLESHOOTING.md)

---

# 🗺️ Roadmap

## 教学体验

- [x] 零基础学习地图
- [x] 从 0 完整复刻教程
- [x] 架构与请求链路文档
- [x] 新手排错手册
- [x] `.env.example`
- [ ] API 请求/响应参考文档
- [ ] 每章对应 Git Tag / 教学分支
- [ ] 配套截图与架构图图片
- [ ] 配套视频章节索引

## 工程化

- [ ] 把模型名 / Embedding / ASR / TTS 全部配置化
- [ ] 支持 text-only 模式
- [ ] 完善错误处理与超时
- [ ] 自动化测试
- [ ] OpenAPI / Swagger
- [ ] Docker / Compose
- [ ] PostgreSQL
- [ ] CI/CD
- [ ] 生产环境配置模板

## AI

- [ ] 多模型供应商
- [ ] 角色级知识库
- [ ] 用户级知识库
- [ ] RAG 来源引用
- [ ] 结构化长期记忆
- [ ] Memory 冲突更新策略
- [ ] Tool 权限与隔离
- [ ] Agent observability

---

# 🤝 参与贡献

欢迎通过 Issue / Pull Request 一起完善。

尤其欢迎：

- 新手复刻时真实遇到的错误；
- 更容易理解的解释；
- Windows / macOS / Linux 差异补充；
- 架构图；
- 测试；
- Docker；
- 模型适配；
- RAG / Memory 改进。

提交前请确认：

- 不包含真实 API Key；
- 不包含私人数据；
- 前端可构建；
- 后端迁移完整；
- 新功能尽量补充文档。

---

# 📄 License

当前项目暂未声明开源许可证。

这意味着“代码公开可见”并不自动等于“任何人都拥有复制、修改、再分发的授权”。如果计划把项目作为正式开源项目推广，建议后续明确选择并添加 LICENSE（例如 MIT、Apache-2.0 等，具体取决于作者希望授予的权利）。

---

## ⭐ 最后

如果你是新手，不要要求自己第一次就理解：

```text
Vue + Django + JWT + SSE + LangChain + LangGraph + RAG + ASR + TTS
```

真正有效的方式是：

> **先跑通，再跟踪一条请求，再拆掉复杂功能重新做一遍。**

从这里开始：

👉 **[从 0 开始完整复刻 AiFriends](./docs/BEGINNER_TUTORIAL.md)**
