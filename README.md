# 🤖 AiFriends

> **从 0 学会做一个有角色、记忆、RAG、语音与完整工程闭环的 AI 伙伴。**
>
> 一个基于 **Vue 3 + Django + LangChain + LangGraph + LanceDB** 的真实 AI 全栈项目，也是一套从“第一次 clone”一路学到“测试、CI、部署、观测”的项目制课程。

---

## 🌱 第一次来？从这里开始

完全零基础，不要先啃最终版 `chat.py`。

推荐严格按这个顺序：

```text
① 15 分钟跑起来
        ↓
② BEGINNER_TUTORIAL：理解基础概念
        ↓
③ COURSE_REBUILD：沿真实 Git 历史重新造
        ↓
④ LABS Chapter 00–13：自己写、自己调、自己验收
        ↓
⑤ ENGINEERING Chapter 14–20：测试、重构、安全、部署
        ↓
⑥ 阅读教材化源码 + ARCHITECTURE
```

### 一级入口

- 📘 **[零基础学习中心](./docs/README.md)**
- 🚀 **[从 0 完整运行与复刻](./docs/BEGINNER_TUTORIAL.md)**
- 🧭 **[按真实 Git 历史逐章重建](./docs/COURSE_REBUILD.md)**
- 🧪 **[Labs：Chapter 00–20](./labs/README.md)**
- 🏗️ **[工程进阶课程 Chapter 14–20](./docs/ENGINEERING_COURSE.md)**
- ✅ **[自动验收 / Grading](./docs/GRADING.md)**
- 🔌 **[API Reference](./docs/API_REFERENCE.md)**
- 🗄️ **[数据库 ER 图](./docs/DATABASE_ER.md)**
- 🧠 **[系统架构与请求链路](./docs/ARCHITECTURE.md)**
- 🧯 **[常见报错与排查手册](./docs/TROUBLESHOOTING.md)**

---

# ✨ 项目能做什么？

## 🎭 AI Character

- 创建自己的 AI 角色；
- 设置名称、头像、背景图；
- 编写人格 / 世界观 /角色设定；
- 为角色选择独立 Voice。

## 💬 Streaming Chat

- JWT 登录后聊天；
- SSE 流式文本；
- 聊天历史保存；
- 最近对话作为短期上下文；
- Token 使用量记录；
- `AbortController` 真正停止浏览器 SSE；
- 后端通过 `cancel_event` 尽快结束生成 worker。

## 🧠 Long-term Memory

- 原始历史保存在 `Message`；
- 最近消息直接进入上下文；
- 历史压缩后保存到 `Friend.memory`；
- Memory 使用独立 LangGraph；
- 每若干轮自动更新。

## 🧰 Agent / Tool Calling

当前 LangGraph Agent 可：

- 查询当前时间；
- 在启用 RAG 时检索 LanceDB；
- Tool 结果回到 LLM 后再生成最终答案。

## 📚 RAG

```text
TextLoader
  ↓
Text Splitter
  ↓
Embedding
  ↓
LanceDB
  ↓
Similarity Search
  ↓
Tool Result
  ↓
LLM
```

## 🎙️ Voice

- 浏览器 VAD；
- PCM 上传；
- WebSocket ASR；
- LLM 流与 TTS 并行；
- Base64 音频通过 SSE 返回；
- MediaSource / SourceBuffer 连续播放 MP3。

---

# ⭐ 第四轮：为了新手第一次成功，项目增加了 3 种运行模式

以前最终项目默认要求模型、RAG、ASR、TTS 一起存在，这对第一次学习过于困难。

现在统一通过：

```text
backend/web/ai/config.py
```

管理。

## `AI_MODE=mock`

**推荐第一次使用。**

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

特点：

```text
不需要 API_KEY
不需要 API_BASE
不需要 WSS_URL
不消耗模型费用
但仍然走真实 JWT / Django / SSE / Message 数据库链路
```

你可以先把 Web 全栈学会，再接真实模型。

## `AI_MODE=text`

只接真实 Chat Model：

```env
AI_MODE=text
API_KEY=...
API_BASE=...
CHAT_MODEL=...
```

默认不要求：

```text
LanceDB
ASR
TTS
```

## `AI_MODE=full`

完整能力模式。

为了兼容已有部署，如果旧 `.env` 没有 `AI_MODE`，代码默认仍使用 `full`。

---

# 🚀 新手最推荐的第一次启动

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

## 3. 安装后端依赖

```bash
pip install -r requirements.txt
```

## 4. 复制环境变量

Windows：

```powershell
Copy-Item .env.example .env
```

macOS / Linux：

```bash
cp .env.example .env
```

第一次先保持：

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

## 5. Django

```bash
cd backend
python manage.py migrate
python manage.py seed_demo
python manage.py doctor
python manage.py runserver
```

`seed_demo` 会幂等创建：

```text
Demo Voice
回复 SystemPrompt
记忆 SystemPrompt
```

`doctor` 会告诉你当前模式缺什么、哪些只是 warning。

## 6. Vue

新终端：

```bash
cd frontend
npm ci
npm run dev
```

Vite 开发环境现在通过 proxy 把：

```text
/api
/media
```

转发给 Django，因此第一次学习不用同时处理一堆跨域与 Cookie host 问题。

## 7. 第一次验证

```text
注册
 ↓
登录
 ↓
创建 Character
 ↓
添加 Friend
 ↓
发送一句话
 ↓
看到【Mock 模式】流式回复
```

成功后再进入 `text` 模式。

---

# 🎙️ 第一次学习语音前

安装完前端依赖后：

```bash
cd frontend
npm run setup:vad
```

它会把 `@ricky0123/vad-web` 与 ONNX Runtime 所需浏览器资源复制到：

```text
frontend/public/vad/
```

然后开启：

```env
ENABLE_ASR=true
ENABLE_TTS=true
```

再运行：

```bash
cd backend
python manage.py doctor
```

不要在文本聊天没跑通之前同时调 ASR/TTS。

---

# 🧠 一句话是怎么走完整个系统的？

```text
InputField.vue
  ↓
streamApi('/api/friend/message/chat/')
  ↓
JWT access token
  ↓
Vite proxy / Django URL
  ↓
MessageChatView
  ↓
Friend ownership
  ↓
SystemPrompt + Character.profile + Friend.memory
  ↓
最近 Message
  ↓
AI_MODE ?
  ├─ mock → 本地确定性 SSE
  └─ text/full → CharGraph
                    ↓
                  LLM
                    ↓
               Tool Calls?
              ├─ get_time
              └─ RAG / LanceDB
                    ↓
              streaming content
                    ├────────────► SSE text
                    └─ optional TTS WS
                              ↓
                           MP3 bytes
                              ↓ Base64
                              └────► SSE audio
  ↓
Vue onmessage
  ├─ content → 消息气泡
  └─ audio → MediaSource
  ↓
Message 落库
  ↓
周期性 Memory update
```

完整解释：**[ARCHITECTURE.md](./docs/ARCHITECTURE.md)**。

---

# 🛠️ 技术栈

## Frontend

| 技术 | 用途 |
|---|---|
| Vue 3 | UI / Component |
| Vue Router | SPA Routing |
| Pinia | User / Access Token State |
| Axios | 普通 HTTP API |
| fetch-event-source | SSE |
| Vite | Dev / Build / Proxy / Manifest |
| Tailwind CSS + daisyUI | UI |
| MediaSource | 流式 MP3 |
| vad-web | Browser VAD |

## Backend

| 技术 | 用途 |
|---|---|
| Python | 后端与 AI 主语言 |
| Django 6 | Web Framework |
| DRF | API |
| SimpleJWT | Auth |
| SQLite | 当前教学数据库 |
| SSE | AI 流式返回 |
| WebSocket | ASR / TTS |

## AI

| 技术 | 用途 |
|---|---|
| LangChain | Message / Tool / Model / Embedding 抽象 |
| LangGraph | Agent / Memory Workflow |
| ChatOpenAI | OpenAI-compatible Chat |
| OpenAI Python SDK | Embedding |
| LanceDB | Vector Store |

---

# 📂 学习时优先认识这些文件

```text
AiFriends/
├── README.md
├── .env.example
├── requirements.txt
├── scripts/
│   └── grade.py
├── labs/
│   ├── chapter-00-...
│   ├── ...
│   └── chapter-20-ci-deploy-observability.md
├── docs/
│   ├── README.md
│   ├── BEGINNER_TUTORIAL.md
│   ├── COURSE_REBUILD.md
│   ├── ENGINEERING_COURSE.md
│   ├── GRADING.md
│   ├── API_REFERENCE.md
│   ├── DATABASE_ER.md
│   ├── ARCHITECTURE.md
│   └── TROUBLESHOOTING.md
├── backend/
│   ├── manage.py
│   └── web/
│       ├── ai/config.py
│       ├── tests.py
│       ├── management/commands/
│       │   ├── doctor.py
│       │   └── seed_demo.py
│       └── views/friend/message/
│           ├── chat/
│           ├── memory/
│           └── asr/
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── scripts/
    │   ├── setup-vad.mjs
    │   └── quality-check.mjs
    ├── tests/
    │   └── singleFlight.test.js
    └── src/
        ├── js/http/
        │   ├── api.js
        │   ├── authRefresh.js
        │   └── streamApi.js
        └── components/character/chat_field/input_field/
            ├── InputField.vue
            └── Microphone.vue
```

---

# ✅ 自动反馈：不要只用肉眼判断“做对了”

## 环境

```bash
cd backend
python manage.py doctor
```

## Chapter 结构 grader

```bash
python scripts/grade.py --chapter 7
```

## Backend tests

```bash
cd backend
python manage.py test web
```

## Frontend tests

```bash
cd frontend
npm test
```

## Frontend 综合检查

```bash
npm run check
```

## CI

PR 会运行：

```text
.github/workflows/ci.yml
```

详细说明：**[GRADING.md](./docs/GRADING.md)**。

---

# 📚 课程结构

## 第一阶段：Chapter 00–13

```text
Environment
Vue / Router
Django / ORM
JWT / Pinia / Axios
Character CRUD
Friend
Basic LLM Chat
SSE
LangGraph / Tool
Memory
RAG
ASR
TTS
Full Pipeline
```

目标：

> **从 0 做出一个完整 AI 全栈应用。**

## 第二阶段：Chapter 14–20

```text
Testing / TDD
DRF Engineering
Config / Providers
Async / Cancellation
Data / Security
RAG + Memory Evaluation
CI / Build / Deploy / Observability
```

目标：

> **把能跑的 AI Demo 升级成可靠的软件工程项目。**

---

# 🧪 当前第四轮已经落地的工程改造

- [x] mock / text / full 三模式
- [x] Chat / Memory / Embedding / ASR / TTS 模型名配置化
- [x] TTS 可关闭，文本聊天不依赖 WSS
- [x] SSE refresh 与 Axios 共用 single-flight refresh
- [x] Local Vite proxy
- [x] 开发环境 refresh cookie 策略集中管理
- [x] AbortController + backend cancel event
- [x] `manage.py doctor`
- [x] `manage.py seed_demo`
- [x] `npm run setup:vad`
- [x] Backend tests
- [x] Frontend unit tests
- [x] Chapter structural grader
- [x] GitHub Actions
- [x] Frontend build smoke test
- [x] Vite manifest，不再硬编码构建 hash
- [x] Chapter 14–20 工程课程

---

# 🗺️ 后续 Roadmap

## 教学

- [ ] `course/chXX-start` / `course/chXX-solution` 稳定教学标签
- [ ] Bug Museum：把真实历史 bug 变成 Debug 实验
- [ ] 每章截图 / GIF / 预期页面
- [ ] 更细粒度 behavioral grader
- [ ] 配套视频索引

## Backend Engineering

- [ ] Serializer 全面重构
- [ ] 统一错误码与 API schema
- [ ] Friend 数据库 UniqueConstraint
- [ ] Transaction / concurrency tests
- [ ] Health endpoint
- [ ] Structured logging / request id
- [ ] PostgreSQL

## AI Engineering

- [ ] Provider Adapter
- [ ] RAG citation
- [ ] RAG eval set
- [ ] Structured Memory
- [ ] Memory conflict resolution
- [ ] Prompt Injection / Tool permission tests
- [ ] Latency / Token dashboard

## Deploy

- [ ] Docker / Compose 教学实现
- [ ] Production ASGI/WSGI server
- [ ] Nginx / HTTPS
- [ ] static/media strategy
- [ ] observability stack

---

# 🤝 贡献

特别欢迎提交：

- 新手第一次 clone 遇到的真实问题；
- 可以自动复现的 bug；
- 回归测试；
- 更好的错误信息；
- Windows / macOS / Linux 差异；
- RAG / Memory eval case；
- Debug Lab；
- Accessibility 改进。

提交前至少运行：

```bash
cd backend
python manage.py test web

cd ../frontend
npm run check
```

并确认没有提交：

```text
真实 API Key
私人聊天数据
.env
db.sqlite3
运行时 LanceDB 数据
```

---

# 📄 License

当前仓库尚未声明正式开源许可证。

代码“公开可见”不自动等于任何人都获得复制、修改和再分发授权。如果计划正式推广为开源教学项目，建议明确选择 MIT / Apache-2.0 等许可证。

---

## 最重要的一条学习原则

不要试图第一天同时理解：

```text
Vue + Django + JWT + SSE + LangChain + LangGraph + RAG + Memory + ASR + TTS + CI
```

真正有效的顺序是：

> **先用 Mock 跑通 → 看懂一条请求 → 自己重写 → 用测试证明 → 再逐个打开复杂能力。**

从这里开始：**[AiFriends 零基础学习中心](./docs/README.md)**。
