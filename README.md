# 🤖 AiFriends

> **从 0 做出一个有角色、记忆、RAG、语音能力的 AI 伙伴，并一路学到测试、CI、数据安全与部署。**
>
> 技术栈：**Vue 3 + Django + DRF + JWT + LangChain + LangGraph + LanceDB + SSE + WebSocket**。

AiFriends 既是一个真实可运行的 AI 全栈项目，也是一套项目制课程。

你可以先把最终项目跑起来，再沿真实 Git 历史重新实现它，最后继续学习“如何把 AI Demo 做成可靠工程”。

---

## 🌱 完全零基础？只走这一条路线

```text
README：知道项目是什么
   ↓
AI_MODE=mock：零 API Key 跑通项目
   ↓
BEGINNER_TUTORIAL：理解基础概念
   ↓
COURSE_REBUILD：沿真实 Git 历史重新造
   ↓
Labs Chapter 00–13：自己实现完整 AI 应用
   ↓
Labs Chapter 14–20：Testing / Security / Deploy
   ↓
源码 + ARCHITECTURE：形成系统视角
```

### 核心入口

- 📘 [零基础学习中心](./docs/README.md)
- 🚀 [完整运行与复刻教程](./docs/BEGINNER_TUTORIAL.md)
- 🧭 [沿真实 Git 历史重建](./docs/COURSE_REBUILD.md)
- 🧪 [Labs：Chapter 00–20](./labs/README.md)
- 🏗️ [工程进阶课程 Chapter 14–20](./docs/ENGINEERING_COURSE.md)
- ✅ [自动验收 / Grading](./docs/GRADING.md)
- 🔌 [API Reference](./docs/API_REFERENCE.md)
- 🗄️ [数据库 ER 图](./docs/DATABASE_ER.md)
- 🧠 [系统架构与请求链路](./docs/ARCHITECTURE.md)
- 🧯 [常见报错与排查](./docs/TROUBLESHOOTING.md)

---

# ✨ 你最终会做出什么？

## 🎭 AI Character

- 创建角色；
- 自定义头像、背景图、人格设定；
- 为不同角色选择 Voice；
- 用户与 Character 建立独立 Friend 关系。

## 💬 Streaming Chat

- JWT 登录；
- SSE 流式文本；
- Message 历史保存；
- 最近对话作为短期上下文；
- Token 使用量记录；
- AbortController 真正关闭浏览器 SSE；
- 后端 cancellation event 尽快停止生成 worker。

## 🧠 Long-term Memory

```text
原始 Message
   +
旧 Friend.memory
   ↓
MemoryGraph
   ↓
新的长期摘要
```

## 🧰 LangGraph Agent

```text
START
  ↓
agent
  ↓
需要 Tool？
  ├─ 否 → END
  └─ 是 → ToolNode
             ↓
           agent
```

当前可扩展 Tool 包括：

- 当前时间；
- LanceDB 私有知识库检索。

## 📚 RAG

```text
原始文档
  ↓
Chunk
  ↓
Embedding
  ↓
LanceDB
  ↓
Retrieval
  ↓
带 source 的 evidence
  ↓
Agent
```

第四轮已经把 Retrieval 从 Agent 中拆出，因此可以单独做 Retrieval Eval。

## 🎙️ Voice

- 浏览器 VAD；
- PCM 上传；
- WebSocket ASR；
- LLM 文本与 TTS 并行；
- MP3 bytes → Base64 → SSE；
- MediaSource / SourceBuffer 连续播放。

---

# ⭐ 三种 AI 运行模式

新手第一次 clone 项目时，最常见的问题不是不会写 LangGraph，而是：

```text
没有正确模型
没有 Embedding
没有 Speech 账号
没有 LanceDB
没有 Voice
```

所以项目现在支持：

## 1. `mock`

**第一次学习推荐。**

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

不需要真实：

```text
API_KEY
API_BASE
WSS_URL
```

但仍然经过真实：

```text
Vue
JWT
Django
Friend
SSE
Message 数据库
```

所以 Chapter 00–07 和 CI 都能在零模型费用下运行。

## 2. `text`

```env
AI_MODE=text
API_KEY=...
API_BASE=...
CHAT_MODEL=...
```

先学习真实 LLM / LangGraph，不要求语音服务。

## 3. `full`

完整开启 Chat / RAG / ASR / TTS。

为兼容已有部署，如果没有配置 `AI_MODE`，代码默认仍使用 `full`；新用户复制 `.env.example` 时默认是 `mock`。

---

# 🚀 第一次启动：推荐流程

## 1. Clone

```bash
git clone https://github.com/tfyf103/AiFriends.git
cd AiFriends
```

## 2. Python 环境

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

安装：

```bash
pip install -r requirements.txt
```

## 3. `.env`

Windows：

```powershell
Copy-Item .env.example .env
```

macOS / Linux：

```bash
cp .env.example .env
```

第一次不要改：

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

## 4. Django

```bash
cd backend
python manage.py migrate
python manage.py seed_demo
python manage.py doctor
python manage.py runserver
```

### `seed_demo`

幂等创建学习所需基础数据：

```text
Demo Voice
回复 SystemPrompt
记忆 SystemPrompt
```

### `doctor`

自动检查当前模式真正需要的：

```text
Python
Database
API 配置
SystemPrompt
Voice
LanceDB
VAD assets
```

## 5. Vue

新终端：

```bash
cd frontend
npm ci
npm run dev
```

开发模式通过 Vite Proxy 转发：

```text
/api
/media
```

因此第一次学习不需要同时处理一堆跨域与 Cookie host 问题。

## 6. 看到第一条 Mock Chat

```text
注册
 ↓
登录
 ↓
创建 Character
 ↓
添加 Friend
 ↓
发送消息
 ↓
看到【Mock 模式】流式回复
```

做到这里，再把 `AI_MODE` 切到 `text`。

---

# 🎙️ 学语音前执行一次

```bash
cd frontend
npm run setup:vad
```

它会自动准备浏览器所需的 VAD / ONNX Runtime 静态资源。

然后再逐项开启：

```env
ENABLE_ASR=true
ENABLE_TTS=true
```

每改一次环境配置都可以重新：

```bash
cd backend
python manage.py doctor
```

---

# ✅ 不要用“感觉”判断代码是否正确

AiFriends 现在提供四层反馈。

## Level 1：环境

```bash
cd backend
python manage.py doctor
```

## Level 2：课程结构

```bash
python scripts/grade.py --chapter 7
python scripts/grade.py --chapter 13
python scripts/grade.py --chapter 20
```

## Level 3：Behavior Tests

后端：

```bash
cd backend
python manage.py test web
```

前端：

```bash
cd frontend
npm test
```

## Level 4：Build / CI

```bash
cd frontend
npm run check
```

Pull Request 会自动运行 GitHub Actions，包括：

```text
Python compile
Chapter 00–20 grader
Migration drift check
Django system check
Backend tests
npm ci
VAD setup
Frontend quality check
Frontend unit tests
Vite production build
Docker learning image build
```

详细说明：[GRADING.md](./docs/GRADING.md)。

---

# 🔥 一条消息经过哪些层？

```text
InputField.vue
  ↓
streamApi
  ↓
Authorization: Bearer <JWT>
  ↓
Vite Proxy / Django URL
  ↓
MessageChatView
  ↓
Friend ownership
  ↓
SystemPrompt
+ Character.profile
+ Friend.memory
+ recent Message
  ↓
AI_MODE
  ├─ mock → local deterministic stream
  └─ text/full → CharGraph
                   ↓
                  LLM
                   ↓
                ToolNode
                ├─ time
                └─ RAG retrieval
                     ↓
                source evidence
  ↓
content chunk
  ├──────────────→ SSE text
  └→ optional TTS WebSocket
                   ↓
                MP3 bytes
                   ↓ Base64
                 SSE audio
  ↓
Vue onmessage
  ├─ message bubble
  └─ MediaSource
  ↓
Message persistence
  ↓
periodic Memory update
```

完整版本：[ARCHITECTURE.md](./docs/ARCHITECTURE.md)。

---

# 📚 两阶段课程

## Chapter 00–13：先学“做出来”

```text
00 Environment
01 Vue / Router
02 Django / ORM
03 JWT / Pinia / Axios
04 Character CRUD
05 Friend
06 Basic LLM Chat
07 SSE
08 LangGraph / Tool
09 Memory
10 RAG
11 ASR
12 TTS
13 Full Pipeline
```

目标：

> **独立做出一个完整 AI Web 应用。**

## Chapter 14–20：再学“做可靠”

```text
14 Testing / TDD
15 DRF / Serializer / HTTP Status
16 Config / Feature Flag / Provider
17 Async / Cancellation
18 Constraint / Transaction / Security
19 RAG / Memory Evaluation
20 CI / Build / Deploy / Observability
```

目标：

> **把一个 AI Demo 升级成可以验证、维护和部署的工程项目。**

入口：[Labs](./labs/README.md)。

---

# 🧪 第四轮已经真正落地了什么？

## First-run success

- [x] `mock / text / full` 三模式
- [x] 模型名配置化
- [x] RAG / ASR / TTS Feature Flag
- [x] Text-only Chat 不依赖 TTS
- [x] Vite local proxy
- [x] 开发/生产 Cookie 策略集中管理
- [x] `manage.py doctor`
- [x] `manage.py seed_demo`
- [x] `npm run setup:vad`

## Authentication / REST

- [x] Axios 与 SSE 共用 single-flight refresh
- [x] 修复 SSE refresh 后可能继续使用旧 access token
- [x] 登录/注册开始使用 DRF Serializer
- [x] 400 / 401 / 409 等状态码
- [x] 基础机器可读错误码

## Streaming / Async

- [x] AbortController 关闭真实 SSE
- [x] backend `cancel_event`
- [x] text-only worker
- [x] optional TTS worker

## Data

- [x] Friend `(user, character)` 数据库 UniqueConstraint
- [x] `0008` 安全数据迁移：合并潜在重复 Friend / Message
- [x] migration drift CI check

## RAG

- [x] Retrieval 从 Agent 解耦
- [x] Tool evidence 带 source
- [x] source 不泄露服务器绝对路径
- [x] `evals/rag_cases.example.json`
- [x] `scripts/eval_rag.py`

## Testing / CI

- [x] Backend behavior tests
- [x] Frontend single-flight tests
- [x] Chapter 00–20 structural grader
- [x] Frontend quality check
- [x] Vite build smoke test
- [x] GitHub Actions

## Build / Observability

- [x] `/api/health/`
- [x] `X-Request-ID`
- [x] Django runtime settings 环境变量化
- [x] Vite manifest，不再手工写 hash bundle
- [x] `Dockerfile.learning`
- [x] `compose.learning.yml`
- [x] CI Docker build

---

# 🧪 RAG Retrieval Eval

真实 RAG 配好后：

```bash
python scripts/eval_rag.py \
  --cases evals/rag_cases.example.json \
  --k 3
```

它先只测试：

```text
问题
 ↓
Embedding
 ↓
Top-k Retrieval
 ↓
是否拿到预期关键词 / source
```

而不是直接让 LLM 生成答案。

这样可以区分：

```text
Retrieval 没找对
vs
LLM 找到了但没用好
```

这也是 Chapter 19 的核心工程思维。

---

# 🐳 Learning Docker

这不是生产部署模板，而是教学用“干净环境复现器”。

```bash
docker build -f Dockerfile.learning -t aifriends:learning .
docker run --rm -p 8000:8000 aifriends:learning
```

或：

```bash
docker compose -f compose.learning.yml up --build
```

它故意仍然使用 Django `runserver`。

Chapter 20 再继续学习：

```text
production WSGI/ASGI
Nginx
HTTPS
PostgreSQL
persistent media
secret management
metrics / tracing
```

---

# 📂 第四轮最值得阅读的新增文件

```text
backend/web/ai/config.py
backend/web/serializers/account.py
backend/web/management/commands/doctor.py
backend/web/management/commands/seed_demo.py
backend/web/middleware.py
backend/web/views/health.py
backend/web/documents/retrieval.py
backend/web/migrations/0008_friend_unique_constraint.py
backend/web/tests.py

frontend/src/js/http/authRefresh.js
frontend/src/js/utils/singleFlight.js
frontend/scripts/setup-vad.mjs
frontend/scripts/quality-check.mjs
frontend/tests/singleFlight.test.js

scripts/grade.py
scripts/eval_rag.py
evals/rag_cases.example.json
.github/workflows/ci.yml
Dockerfile.learning
compose.learning.yml
```

---

# 🗺️ 下一阶段 Roadmap

现在更值得做的是继续提高“教学质量与生产思维”，而不是继续堆基础教程。

## 教学体验

- [ ] `course/chXX-start` / `course/chXX-solution` 稳定教学标签
- [ ] Bug Museum：把真实历史 Bug 变成 Debug Lab
- [ ] 每章截图 / GIF / Expected Result
- [ ] 更细粒度 behavioral grader
- [ ] 配套视频索引

## Backend / Security

- [ ] 把更多旧 API 迁移到 Serializer / 统一错误结构
- [ ] 文件上传 MIME / Size / Image validation
- [ ] Object-level Permission 系统化
- [ ] Refresh-token blacklist / revoke 策略课程
- [ ] Rate Limit
- [ ] PostgreSQL / 并发 Transaction 实验

## AI Engineering

- [ ] Provider Adapter
- [ ] 把 RAG source 以结构化事件直接展示到 UI
- [ ] Generation / Faithfulness Eval
- [ ] Structured Memory
- [ ] Memory conflict resolution
- [ ] Prompt Injection / Tool permission tests
- [ ] Token / Latency dashboard

## Production

- [ ] Production WSGI/ASGI Server
- [ ] Nginx / HTTPS
- [ ] Persistent media/object storage
- [ ] PostgreSQL production config
- [ ] Structured logging / metrics / tracing

---

# 🤝 贡献前最低检查

Backend：

```bash
cd backend
python manage.py test web
```

Frontend：

```bash
cd frontend
npm run check
```

课程结构：

```bash
python scripts/grade.py --chapter 20
```

并确认没有提交：

```text
真实 API Key
真实 Django Secret
.env
私人聊天数据
db.sqlite3
运行时 LanceDB 数据
```

---

# 📄 License

当前仓库尚未声明正式开源许可证。

如果准备把 AiFriends 作为正式开源教学项目推广，建议后续明确选择 MIT / Apache-2.0 等许可证。

---

## 最重要的学习原则

不要第一天同时调：

```text
Vue + Django + JWT + SSE + LangGraph + RAG + Memory + ASR + TTS + Docker
```

正确顺序是：

> **先用 Mock 跑通 → 看懂一条请求 → 自己重写 → 用测试证明 → 再逐个打开复杂能力。**

从这里开始：**[AiFriends 零基础学习中心](./docs/README.md)**。
