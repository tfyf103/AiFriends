# AiFriends 零基础学习中心

> 这里不是“文档目录”，而是你的学习路线控制台。

AiFriends 现在分成两个阶段：

```text
Chapter 00–13
从零做出完整 AI 全栈应用

Chapter 14–20
把 AI Demo 升级成可靠工程项目
```

---

# 1. 你是哪一种学习者？

## A. 完全零基础

严格按：

```text
README
 ↓
BEGINNER_TUTORIAL
 ↓
先用 AI_MODE=mock 跑通
 ↓
COURSE_REBUILD
 ↓
Labs Chapter 00–13
 ↓
ENGINEERING_COURSE Chapter 14–20
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
Chapter 11/12 Voice
 ↓
Chapter 14 Testing
 ↓
Chapter 16 Config
 ↓
Chapter 19 RAG / Memory Eval
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
documents/utils/*
 ↓
InputField.vue / streamApi.js
```

---

# 2. 核心资料

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

---

# 3. 第一次启动：不要先配真实模型

第四轮加入三种模式。

## Mock

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

## Text

真实 Chat Model，默认关闭语音/RAG。

## Full

完整 Agent + RAG + ASR/TTS。

推荐升级顺序：

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

Windows 复制 `.env`：

```powershell
Copy-Item .env.example .env
```

## Frontend

```bash
cd frontend
npm ci
npm run dev
```

如果准备学习语音：

```bash
npm run setup:vad
```

---

# 5. 第四轮新手工具

## `doctor`

```bash
cd backend
python manage.py doctor
```

它回答：

> “我现在选的 AI 模式，环境到底准备好了吗？”

会检查：

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

幂等准备：

```text
Demo Voice
回复 Prompt
记忆 Prompt
```

## Chapter grader

```bash
python scripts/grade.py --chapter 7
```

## Tests

```bash
cd backend
python manage.py test web

cd ../frontend
npm test
```

## Frontend 综合检查

```bash
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
| 04 | 一个角色如何从表单进入 SQLite/media？ |
| 05 | User / Character / Friend 是什么关系？ |
| 06 | 一条消息如何进入 LLM？ |
| 07 | 为什么 AI 能逐段显示？ |
| 08 | Agent 为什么能调用 Tool？ |
| 09 | 为什么不能无限塞聊天历史？ |
| 10 | 私有资料怎么进入回答？ |
| 11 | 声音怎么变文字？ |
| 12 | AI 为什么能边生成边说话？ |
| 13 | 能否完整追踪一句话？ |

入口：**[Labs](../labs/README.md)**。

---

# 7. Chapter 14–20：再学“怎么做可靠”

| Chapter | 核心问题 |
|---|---|
| 14 Testing | 谁证明修改没把功能弄坏？ |
| 15 DRF Engineering | 为什么 API 不能全靠 try/except + dict？ |
| 16 Config | 为什么换模型不该改五个业务文件？ |
| 17 Cancellation | Stop 如何真的停止 SSE/LLM/TTS？ |
| 18 Data/Security | 为什么 View 判断不能替代 DB constraint？ |
| 19 Eval | RAG / Memory 怎么证明“更好”？ |
| 20 CI/Deploy | 为什么“我电脑能跑”远远不够？ |

入口：**[ENGINEERING_COURSE](./ENGINEERING_COURSE.md)**。

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

重点理解：

```text
Pinia
JWT header
single-flight refresh
SSE
AbortController
Base64
MediaSource
VAD
```

## Backend

```text
web/urls.py
 ↓
models/*
 ↓
views/user/account/*
 ↓
views/friend/message/chat/chat.py
 ↓
chat/graph.py
 ↓
memory/*
 ↓
documents/utils/*
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

看到“聊天失败”不要直接改 LangChain。

```text
UI
 ↓
Vue state
 ↓
Network
 ↓
JWT
 ↓
Django URL
 ↓
View
 ↓
ORM
 ↓
AI mode/config
 ↓
LLM
 ↓
Tool / RAG
 ↓
SSE
 ↓
ASR/TTS
```

同时打开：

```text
VS Code
Vite terminal
Django terminal
DevTools Console
DevTools Network
Django Admin
```

遇到问题：**[TROUBLESHOOTING](./TROUBLESHOOTING.md)**。

---

# 11. 真实历史 Commit 怎么正确使用？

`COURSE_REBUILD.md` 的历史 commit 价值在于：

> 看一个真实项目如何逐步增加需求与复杂度。

但历史版本可能包含当时的 bug。

因此：

```text
历史 commit = 工程考古
当前测试 = 当前参考行为
Labs 验收 = 学习目标
```

不要把每一个历史版本都当“标准答案”。

---

# 12. 最终学习闭环

每一章尽量做到：

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
写一句 trade-off
```

如果你开始习惯用：

```text
Network
Traceback
Test
CI
Metric
```

证明自己的判断，而不是不停“试一试代码”，你已经开始从教程学习者向工程开发者过渡。

---

返回：**[项目首页](../README.md)**。
