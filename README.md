# 🤖 AiFriends

[![AiFriends CI](https://github.com/tfyf103/AiFriends/actions/workflows/ci.yml/badge.svg)](https://github.com/tfyf103/AiFriends/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

🌐 **语言 / Language：** **简体中文** | [English](./README_EN.md)

> **从 0 做出一个有角色、长期记忆、RAG、Agent 与语音能力的 AI 伙伴，并一路学到测试、安全、CI 与部署。**
>
> **An open-source, project-based full-stack AI curriculum and reference application for learning how modern AI products are actually engineered and maintained.**

AiFriends 使用 **Vue 3 + Django + DRF + JWT + LangChain + LangGraph + LanceDB + SSE + WebSocket**，把一个真实 AI 应用拆成可运行、可复刻、可测试、可继续工程化的学习路径。

它不是“只调用一次大模型 API”的示例。项目覆盖从浏览器 UI、认证、数据库、流式协议，到 Agent、RAG、Memory、ASR/TTS，再到自动测试、数据约束、安全边界、CI 和构建发布。

---

## 30 秒项目快照

| 项目维度 | 当前状态 |
| --- | --- |
| 开源许可 | **MIT** |
| 维护状态 | **Active development**，由 `@tfyf103` 主要维护 |
| 学习语言 | **中文 + English 双语入口**；英文已覆盖 Quick Start、Architecture 与核心 Labs 00/06/07/08/10/13 |
| 入门门槛 | `AI_MODE=mock` 可 **零 API Key** 跑通核心 Web/SSE 链路 |
| 课程 | Chapter **00–20**，从零基础到工程化 |
| 自动反馈 | Django tests + Node tests + structural grader + GitHub Actions |
| AI 能力 | LangGraph Agent / Tool Calling / Memory / RAG / ASR / TTS |
| 工程能力 | Serializer / cancellation / migration checks / Health / Request-ID / Docker learning image |
| 安全入口 | [SECURITY.md](./SECURITY.md) |
| 贡献入口 | [CONTRIBUTING.md](./CONTRIBUTING.md) |

> **项目目标：让学习者不仅“把 AI Demo 跑起来”，还能够理解它为什么这样设计、如何验证它、如何维护它，以及怎样逐步把 Demo 变成可靠的软件工程。**

---

# 为什么做 AiFriends？

很多 AI 教程停在：

```text
输入 Prompt
   ↓
调用模型 API
   ↓
打印答案
```

真实 AI 产品却往往是：

```text
Frontend
  ↓
Authentication
  ↓
HTTP / SSE / WebSocket
  ↓
Backend / ORM
  ↓
LLM / Agent / Tools
  ↓
RAG / Memory
  ↓
Speech
  ↓
Persistence / Tests / CI / Security
```

AiFriends 希望补上这中间的工程断层。项目从中文 AI 学习社区起步，提供一条 **code-first、可复现、带实验和自动反馈** 的学习路线，并通过中英文双语文档逐步向全球开发者开放。

项目把“教程”和“真实维护”放在同一个仓库里：学生看到的不是另一套玩具代码，而是实际运行路径、真实 Git 历史、真实测试、真实数据迁移和真实 CI。

---

# 🌱 零基础学习路线

```text
README：先知道项目是什么
   ↓
AI_MODE=mock：零 API Key 跑通项目
   ↓
BEGINNER_TUTORIAL：理解基础概念
   ↓
COURSE_REBUILD：沿真实 Git 历史重新实现
   ↓
Labs Chapter 00–13：独立完成 AI 应用
   ↓
Labs Chapter 14–20：Testing / Security / CI / Deploy
   ↓
源码 + ARCHITECTURE：形成完整系统视角
```

## 中文核心入口

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

## English Core Track

- 🌍 [English Learning Hub](./docs/README_EN.md)
- 🚀 [English Quick Start](./docs/QUICK_START_EN.md)
- 🧠 [English Architecture Guide](./docs/ARCHITECTURE_EN.md)
- 🧪 [English Core Labs](./labs/en/README.md) — Chapter 00 / 06 / 07 / 08 / 10 / 13

---

# ✨ 你最终会做出什么？

## 🎭 AI Character

- 创建自己的 AI 角色；
- 自定义名称、头像、聊天背景；
- 编写人格 / 世界观 / 角色设定；
- 为不同 Character 选择 Voice；
- 每个用户与 Character 建立独立 Friend 关系。

## 💬 Streaming Chat

- JWT 登录与刷新；
- SSE 流式文本；
- Message 历史保存；
- 最近聊天作为短期上下文；
- Token 使用量记录；
- `AbortController` 真实终止浏览器 SSE；
- 后端 cancellation event 尽快停止生成 worker。

## 🧠 Long-term Memory

```text
历史 Message
   +
旧 Friend.memory
   ↓
MemoryGraph
   ↓
新的长期摘要
```

长期记忆与 Character 固定人格分离，让学习者可以理解：

```text
Character.profile = 角色是谁
Friend.memory     = 这个角色记住了某个用户什么
```

## 🧰 LangGraph Agent / Tool Calling

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

当前示例 Tool 包括：

- 当前时间；
- LanceDB 知识库检索。

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

Retrieval 已从 Agent 中拆出，可以独立评测，不必把“检索错误”和“生成错误”混在一起。

## 🎙️ Voice

- 浏览器 VAD；
- PCM 音频上传；
- WebSocket ASR；
- LLM 文本与 TTS 并行；
- MP3 bytes → Base64 → SSE；
- MediaSource / SourceBuffer 连续播放。

---

# ⭐ 三种 AI 运行模式

为了让新手先学系统，再处理第三方模型服务，AiFriends 支持：

| Mode | 外部模型要求 | 适合学习 |
| --- | --- | --- |
| `mock` | 无 | Vue / Django / JWT / Friend / SSE / DB / CI |
| `text` | Chat Model | LLM / LangGraph / Tool / Memory |
| `full` | Chat + Embedding + Speech | RAG / ASR / TTS 完整链路 |

## 1. `mock`：第一次学习推荐

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

不需要：

```text
API_KEY
API_BASE
WSS_URL
```

但仍然走真实：

```text
Vue
 ↓
JWT
 ↓
Django
 ↓
Friend
 ↓
SSE
 ↓
Message 数据库
```

## 2. `text`

```env
AI_MODE=text
API_KEY=...
API_BASE=...
CHAT_MODEL=...
```

用于先学习真实 LLM / LangGraph，而不把 TTS/ASR 作为聊天成功的前置条件。

## 3. `full`

完整开启 Chat / RAG / ASR / TTS。

为了兼容旧部署，没有配置 `AI_MODE` 时运行时代码默认仍按 `full` 处理；新学习者复制 `.env.example` 时从 `mock` 开始。

---

# 🚀 第一次启动

## 1. Clone

```bash
git clone https://github.com/tfyf103/AiFriends.git
cd AiFriends
```

## 2. Python

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

```bash
pip install -r requirements.txt
```

## 3. Environment

Windows：

```powershell
Copy-Item .env.example .env
```

macOS / Linux：

```bash
cp .env.example .env
```

第一次保持：

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

幂等创建基础学习数据：

```text
Demo Voice
回复 SystemPrompt
记忆 SystemPrompt
```

### `doctor`

根据当前 AI 模式检查真正需要的环境：

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

开发模式通过 Vite Proxy 转发 `/api` 和 `/media`，降低第一次学习时的 CORS / Cookie host 干扰。

## 6. 第一条消息

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

完成这里后，再逐步切换到 `text` / `full`。

---

# 🎙️ 学语音前

```bash
cd frontend
npm run setup:vad
```

它会从 npm 依赖中自动准备浏览器所需 VAD / ONNX Runtime 静态资源。

之后再逐项开启：

```env
ENABLE_ASR=true
ENABLE_TTS=true
```

环境有疑问时重新执行：

```bash
cd backend
python manage.py doctor
```

---

# ✅ 自动反馈：不要靠“感觉”判断做对了

AiFriends 当前提供四层反馈。

## Level 1 — Environment

```bash
cd backend
python manage.py doctor
```

## Level 2 — Course Structural Grader

```bash
python scripts/grade.py --chapter 7
python scripts/grade.py --chapter 13
python scripts/grade.py --chapter 20
```

## Level 3 — Behavior Tests

Backend：

```bash
cd backend
python manage.py test web
```

Frontend：

```bash
cd frontend
npm test
```

## Level 4 — Build / CI

```bash
cd frontend
npm run check
```

Pull Request 的 GitHub Actions 会在干净环境运行：

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

详见 [GRADING.md](./docs/GRADING.md)。

---

# 🔥 一条聊天消息如何穿过整个系统？

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
  ├─ mock → deterministic local stream
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

完整说明：[ARCHITECTURE.md](./docs/ARCHITECTURE.md)。  
English: [ARCHITECTURE_EN.md](./docs/ARCHITECTURE_EN.md)。

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

目标：**独立做出一个完整 AI Web 应用。**

英文核心路径已覆盖：

```text
00 Environment
06 Basic LLM Chat
07 SSE Streaming
08 LangGraph / Tool Calling
10 RAG + LanceDB
13 Full-System Capstone
```

入口：[Labs](./labs/README.md) / [English Labs](./labs/en/README.md)。

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

目标：**把能跑的 AI Demo 升级成可验证、可维护的工程项目。**

入口：[Labs](./labs/README.md)。

---

# 🛡️ Security & maintenance

AiFriends 的维护面横跨：

```text
JWT / refresh cookies
Object-level authorization
File uploads
SSE / WebSocket
LLM Tool Calling
RAG / user data
Third-party AI endpoints
Dependency supply chain
```

因此安全不是课程最后的一页，而是项目维护的一部分。

- 安全问题请遵循 **[SECURITY.md](./SECURITY.md)**，不要公开披露未修复漏洞。
- 普通 Bug、文档、测试和工程改进欢迎按 **[CONTRIBUTING.md](./CONTRIBUTING.md)** 提交。
- CI 默认使用 `mock` 模式，不要求贡献者提交真实 API Key，也不消耗外部模型额度。
- `/api/health/`、`X-Request-ID`、migration drift check、behavior tests 和 Docker learning build 用于提升可诊断性和回归保护。

> `Dockerfile.learning`、SQLite、Django `runserver` 和开发环境设置是**教学参考**，不是生产环境安全承诺。生产部署需要继续完成 WSGI/ASGI、HTTPS、PostgreSQL、持久化存储、Secrets、Rate Limit、metrics/tracing 等工作。

---

# 🧪 RAG Retrieval Eval

真实 RAG 配好后：

```bash
python scripts/eval_rag.py \
  --cases evals/rag_cases.example.json \
  --k 3
```

它先独立测试 Retrieval：

```text
问题
 ↓
Embedding
 ↓
Top-k Retrieval
 ↓
预期关键词 / source
```

这样可以区分：

```text
Retrieval 没找对
vs
LLM 找到了证据但没用好
```

这是 Chapter 19 的核心工程思维之一，也是英文 [Chapter 10 RAG Lab](./labs/en/chapter-10-rag.md) 的重点。

---

# 🐳 Learning Docker

教学用“干净环境复现器”：

```bash
docker build -f Dockerfile.learning -t aifriends:learning .
docker run --rm -p 8000:8000 aifriends:learning
```

或：

```bash
docker compose -f compose.learning.yml up --build
```

它故意仍使用 Django `runserver`。Chapter 20 再继续学习真正的生产部署边界。

---

# 🤝 Contributing

AiFriends 欢迎这些贡献：

- 可以复现的 Bug fix；
- Authentication / Authorization / Upload / Streaming / RAG 安全改进；
- Regression tests；
- 新手第一次运行问题和诊断工具；
- 文档与源码不一致的修复；
- Labs / Debugging exercises；
- Accessibility / Performance / CI / Observability / Deploy 改进；
- RAG / Memory evaluation cases；
- **英文文档改进与翻译贡献。**

开始前请阅读：[CONTRIBUTING.md](./CONTRIBUTING.md)。

最低检查：

```bash
python scripts/grade.py --chapter 20

cd backend
python manage.py makemigrations --check --dry-run
python manage.py check
python manage.py test web

cd ../frontend
npm run check
npm test
npm run build
```

不要提交：

```text
真实 API Key / JWT / Django Secret
.env
私人聊天数据
db.sqlite3
运行时 LanceDB 数据
```

---

# 🗺️ Roadmap

下一阶段更值得做的是提高教学质量、软件供应链安全、国际可访问性和生产思维，而不是继续堆基础教程。

## Internationalization / Learning Experience

- [x] 中文 + English 仓库首页
- [x] English Learning Hub
- [x] 独立 English Quick Start
- [x] 当前实现版 English Architecture Guide
- [x] 高价值 English Labs：00 / 06 / 07 / 08 / 10 / 13
- [x] 明确欢迎 English documentation improvements and translations
- [ ] Chapter 01–05 / 09 / 11–12 英文 Labs
- [ ] Chapter 14–20 Engineering Labs 英文化
- [ ] API / Database / Troubleshooting 完整英文版本
- [ ] `course/chXX-start` / `course/chXX-solution` 稳定教学标签
- [ ] Bug Museum：把真实历史 Bug 变成 Debug Lab
- [ ] 每章截图 / GIF / Expected Result
- [ ] 更细粒度 behavioral grader
- [ ] 配套视频索引

## Backend / Security

- [ ] 更多旧 API 迁移到 Serializer / 统一错误结构
- [ ] 文件上传 MIME / Size / Image validation
- [ ] Object-level Permission 系统化
- [ ] Refresh-token blacklist / revoke 策略
- [ ] Rate Limit
- [ ] Dependency audit / supply-chain hardening
- [ ] PostgreSQL / 并发 Transaction 实验

## AI Engineering

- [ ] Provider Adapter
- [ ] RAG source 结构化事件与前端 Citation UI
- [ ] Generation / Faithfulness Eval
- [ ] Structured Memory
- [ ] Memory conflict resolution
- [ ] Prompt Injection / Tool permission tests
- [ ] Token / Latency dashboard

## Production

- [ ] Production WSGI/ASGI Server
- [ ] Nginx / HTTPS
- [ ] Persistent media / object storage
- [ ] PostgreSQL production config
- [ ] Structured logging / metrics / tracing
- [ ] Route-level lazy loading / code splitting

---

# 📄 License

AiFriends is open source under the **MIT License**. See [LICENSE](./LICENSE).

---

## 最重要的学习原则

不要第一天同时调：

```text
Vue + Django + JWT + SSE + LangGraph + RAG + Memory + ASR + TTS + Docker
```

正确顺序是：

> **先用 Mock 跑通 → 看懂一条请求 → 自己重写 → 用测试证明 → 再逐个打开复杂能力。**
