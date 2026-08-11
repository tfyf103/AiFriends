# AiFriends 零基础学习中心

🌐 **语言 / Language：** **简体中文** | [English Learning Hub](./README_EN.md)

> 这里不是“文档目录”，而是你的学习路线控制台。

AiFriends 分成两个阶段：

```text
Chapter 00–13
从零做出完整 AI 全栈应用

Chapter 14–20
把 AI Demo 升级成可靠工程项目
```

> **英文核心课程现已完整覆盖 Chapter 00–20。** English learners can use dedicated Quick Start / Architecture / Engineering Course / API / Database / Troubleshooting documents and complete the full Labs path independently.

---

# 1. 你是哪一种学习者？

## A. 完全零基础

中文路线：

```text
README
 ↓
BEGINNER_TUTORIAL
 ↓
AI_MODE=mock
 ↓
COURSE_REBUILD
 ↓
Labs Chapter 00–13
 ↓
ENGINEERING_COURSE Chapter 14–20
```

英文路线：

```text
README_EN
 ↓
English Learning Hub
 ↓
QUICK_START_EN
 ↓
AI_MODE=mock
 ↓
English Labs Chapter 00–13
 ↓
English Engineering Labs Chapter 14–20
```

## B. 会 Vue / Django，只想学 AI 应用

```text
Chapter 06 Basic Chat
 ↓
Chapter 07 SSE
 ↓
Chapter 08 LangGraph / Tool
 ↓
Chapter 09 Memory
 ↓
Chapter 10 RAG
 ↓
Chapter 11 ASR
 ↓
Chapter 12 TTS
 ↓
Chapter 13 Capstone
```

## C. 已会 LangChain，只想看项目架构

```text
ARCHITECTURE
 ↓
chat/chat.py
 ↓
chat/graph.py
 ↓
memory/*
 ↓
documents/*
 ↓
InputField.vue / streamApi.js
```

## D. 想学工程化 / 开源维护

```text
Chapter 14 Testing
 ↓
15 DRF Engineering
 ↓
16 Config / Providers
 ↓
17 Cancellation
 ↓
18 Data / Security
 ↓
19 RAG / Memory Eval
 ↓
20 CI / Deploy / Observability
```

---

# 2. 核心资料

## 中文

| 资料 | 用途 |
|---|---|
| [BEGINNER_TUTORIAL](./BEGINNER_TUTORIAL.md) | 第一次安装、运行、理解基础概念 |
| [COURSE_REBUILD](./COURSE_REBUILD.md) | 沿真实 Git 历史看项目如何成长 |
| [Labs 00–20](../labs/README.md) | 真正动手、制造错误、验收 |
| [ENGINEERING_COURSE](./ENGINEERING_COURSE.md) | Testing → Deploy 的第二阶段课程 |
| [GRADING](./GRADING.md) | doctor / grader / test / CI |
| [API_REFERENCE](./API_REFERENCE.md) | 前后端联调手册 |
| [DATABASE_ER](./DATABASE_ER.md) | Model / Relation / ER 图 |
| [ARCHITECTURE](./ARCHITECTURE.md) | 完整请求与 AI 数据流 |
| [TROUBLESHOOTING](./TROUBLESHOOTING.md) | 分层排错 |

## English

| Resource | Purpose |
|---|---|
| [English Learning Hub](./README_EN.md) | Full English navigation |
| [English Quick Start](./QUICK_START_EN.md) | Zero-API-key first run |
| [English Labs 00–20](../labs/en/README.md) | Complete hands-on curriculum |
| [English Architecture Guide](./ARCHITECTURE_EN.md) | Current end-to-end architecture |
| [English Engineering Course](./ENGINEERING_COURSE_EN.md) | Chapters 14–20 overview |
| [English API Reference](./API_REFERENCE_EN.md) | HTTP / JWT / SSE / current API behavior |
| [English Database / ER Guide](./DATABASE_ER_EN.md) | Relations, constraints, storage boundaries |
| [English Troubleshooting](./TROUBLESHOOTING_EN.md) | Current layered debugging guide |
| [README_EN](../README_EN.md) | International project landing page |

---

# 3. 第一次启动：不要先配真实模型

推荐：

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

但仍然能学习：

```text
注册 / 登录
JWT
Character / Friend
Django API
SSE
Message 保存
Vue 实时更新
```

升级顺序：

```text
mock
 ↓
text
 ↓
text + RAG
 ↓
text + ASR
 ↓
full
```

---

# 4. 第一次运行命令

## Backend

```bash
python -m venv .venv
# 激活 .venv
pip install -r requirements.txt
cp .env.example .env
cd backend
python manage.py migrate
python manage.py seed_demo
python manage.py doctor
python manage.py runserver
```

Windows：

```powershell
Copy-Item .env.example .env
```

## Frontend

```bash
cd frontend
npm ci
npm run dev
```

学语音前：

```bash
npm run setup:vad
```

---

# 5. 新手诊断与机器反馈

## `doctor`

```bash
cd backend
python manage.py doctor
```

按当前 Mode / Feature 检查真正需要的：

```text
Python
Database
API_KEY / API_BASE
WSS_URL
SystemPrompt
Voice
LanceDB
VAD assets
```

## `seed_demo`

```bash
python manage.py seed_demo
```

幂等准备教学基础数据。

## Structural grader

```bash
python scripts/grade.py --chapter 7
python scripts/grade.py --chapter 20
```

## Backend tests

```bash
cd backend
python manage.py test web
```

## Frontend checks

```bash
cd frontend
npm run check
```

---

# 6. Chapter 00–13：先学“怎么做出来”

| Chapter | 核心问题 |
|---|---|
| 00 | 前端和后端为什么分别运行？ |
| 01 | URL 为什么能切页面？ |
| 02 | Python Model 为什么变成数据库表？ |
| 03 | 登录状态如何贯穿前后端？ |
| 04 | 一个 Character 如何从表单进入 SQLite/media？ |
| 05 | User / Character / Friend 是什么关系？ |
| 06 | 一条消息如何进入 LLM？ |
| 07 | 为什么 AI 能逐段显示？ |
| 08 | Agent 为什么能调用 Tool？ |
| 09 | 为什么不能无限塞聊天历史？ |
| 10 | 私有资料怎么进入回答？ |
| 11 | 声音怎么变文字？ |
| 12 | AI 为什么能边生成边说话？ |
| 13 | 能否完整追踪一句话？ |

入口：

- [中文 Labs](../labs/README.md)
- [English Labs](../labs/en/README.md)

---

# 7. Chapter 14–20：再学“怎么做可靠”

| Chapter | 核心问题 |
|---|---|
| 14 Testing | 谁证明修改没把功能弄坏？ |
| 15 DRF Engineering | 为什么 API 不能全靠 try/except + dict？ |
| 16 Config | 为什么换模型不该改多个业务文件？ |
| 17 Cancellation | Stop 如何真的停止 SSE/LLM/TTS？ |
| 18 Data/Security | 为什么 View 判断不能替代 DB constraint？ |
| 19 Eval | RAG / Memory 怎么证明“更好”？ |
| 20 CI/Deploy | 为什么“我电脑能跑”远远不够？ |

入口：

- [中文 Engineering Course](./ENGINEERING_COURSE.md)
- [English Engineering Course](./ENGINEERING_COURSE_EN.md)

---

# 8. 教材化源码阅读顺序

## Frontend

```text
frontend/src/main.js
 ↓
router/index.js
 ↓
stores/user.js
 ↓
js/http/api.js
 ↓
js/http/authRefresh.js
 ↓
js/http/streamApi.js
 ↓
InputField.vue
 ↓
Microphone.vue
```

## Backend

```text
web/urls.py
 ↓
models/*
 ↓
serializers/*
 ↓
views/user/account/*
 ↓
views/friend/message/chat/chat.py
 ↓
chat/graph.py
 ↓
memory/*
 ↓
documents/retrieval.py
 ↓
asr/asr.py
```

## Engineering helpers

```text
web/ai/config.py
management/commands/doctor.py
management/commands/seed_demo.py
web/tests.py
.github/workflows/ci.yml
scripts/grade.py
scripts/eval_rag.py
```

---

# 9. 一句话完整生命周期

```text
InputField.vue
 ↓
streamApi
 ↓
JWT
 ↓
Django URL
 ↓
MessageChatView
 ↓
Friend ownership
 ↓
SystemPrompt + Character + Memory + History
 ↓
AI_MODE
 ├─ mock
 └─ LangGraph
      ├─ LLM
      ├─ Tool
      └─ optional RAG
 ↓
Queue / async worker
 ↓
optional TTS
 ↓
SSE content/audio
 ↓
Vue
 ↓
Message DB
 ↓
Memory update
```

能自己讲清楚这条链，是 Chapter 13 的核心毕业标准。

---

# 10. 调试顺序

```text
UI
 ↓
Vue state
 ↓
Network
 ↓
JWT / refresh
 ↓
Django URL / View / Serializer
 ↓
ORM / ownership / constraint
 ↓
AI mode/config
 ↓
LLM
 ↓
Tool / RAG
 ↓
SSE / cancellation
 ↓
ASR/TTS
```

- 中文：[TROUBLESHOOTING](./TROUBLESHOOTING.md)
- English：[TROUBLESHOOTING_EN](./TROUBLESHOOTING_EN.md)

---

# 11. 真实历史 Commit 怎么使用？

`COURSE_REBUILD.md` 的价值是：

> 看一个真实项目如何逐步增加需求与复杂度。

但历史版本可能包含当时的 bug。

因此：

```text
历史 commit = 工程考古
当前测试 = 当前参考行为
Labs 验收 = 学习目标
```

不要把每一个历史版本都当标准答案。

---

# 12. 国际化状态

核心路径已经完成：

- [x] 中英文项目首页
- [x] English Learning Hub
- [x] English Quick Start
- [x] English Architecture Guide
- [x] **English Labs Chapter 00–20**
- [x] English Engineering Course
- [x] English API Reference
- [x] English Database / ER Guide
- [x] English Troubleshooting
- [x] 中英文贡献入口

后续国际化已经从“补缺失课程”转成“持续质量维护”：

- [ ] 按价值翻译 `COURSE_REBUILD` / 历史工程考古等辅助资料
- [ ] 自动检查双语文档与代码漂移
- [ ] 中英文截图 / GIF / Expected Result
- [ ] 术语一致性和可访问性优化

原则：**双语文档首先要与当前代码一致，其次才是追求文字覆盖率。**

---

# 13. 最终学习闭环

```text
预测
 ↓
实现
 ↓
DevTools / 日志观察
 ↓
主动制造 bug
 ↓
定位
 ↓
修复
 ↓
grader / test / build
 ↓
commit
 ↓
写 trade-off
```

如果你开始习惯用：

```text
Network
Traceback
Test
CI
Metric
```

证明自己的判断，而不是不停“试代码”，你已经开始从教程学习者向工程开发者过渡。

---

返回：**[项目首页](../README.md)**。  
English: **[English Learning Hub](./README_EN.md)**。
