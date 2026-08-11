# AiFriends 实验课（Labs）

🌐 **语言 / Language：** **简体中文** | [English Labs](./en/README.md)

> 目标：把“我看懂了”升级成“我能自己写出来，而且能证明自己写对了”。

Labs 分成两段：

```text
Chapter 00–13：从零做出完整 AI 全栈应用
Chapter 14–20：把 AI Demo 升级成可靠工程项目
```

> English learners: **Chapter 00–20 now has a complete English lab track**, plus English Quick Start / Architecture / Engineering Course / API / Database / Troubleshooting references.

---

## 推荐用法

不要在主项目分支里直接做实验。建议：

```bash
git switch main
git pull
git switch -c learn/aifriends
```

查看真实历史版本：

```bash
git show <commit-sha>
git diff <old-sha> <new-sha>
```

真实历史 commit 是“工程考古材料”，不一定等于标准答案。历史中可能包含当时尚未修复的 bug；课程最终参考应以当前测试、实验验收与 canonical/current solution 为准。

每完成一章：

```bash
git add .
git commit -m "learn: finish chapter 03 jwt auth"
```

---

# English Track：Chapter 00–20 已完整覆盖

英文实验目录：[`labs/en/README.md`](./en/README.md)。

英文完整路线：

```text
English Quick Start
  ↓
Chapter 00 → 01 → 02 → 03 → 04 → 05
  ↓
06 → 07 → 08 → 09 → 10 → 11 → 12
  ↓
13 Capstone
  ↓
14 → 15 → 16 → 17 → 18 → 19 → 20
  ↓
English Architecture / API / ER / Troubleshooting
```

---

# 第一阶段：Chapter 00–13

| Chapter | 中文实验 | English Lab | 你要做出来的东西 |
|---|---|---|---|
| 00 | [环境与骨架](./chapter-00-environment.md) | [Environment](./en/chapter-00-environment.md) | Python/Node/Git、前后端可启动 |
| 01 | [Vue 页面与 Router](./chapter-01-vue-router.md) | [Vue / Router](./en/chapter-01-vue-router.md) | 页面、路由、组件通信 |
| 02 | [Django + ORM + SQLite](./chapter-02-django-orm.md) | [Django / ORM](./en/chapter-02-django-orm.md) | Model、migration、Admin、基础 API |
| 03 | [注册登录 + JWT](./chapter-03-jwt-auth.md) | [JWT / Pinia / Axios](./en/chapter-03-jwt-auth.md) | 注册、登录、Token refresh |
| 04 | [Character CRUD](./chapter-04-character-crud.md) | [Character CRUD](./en/chapter-04-character-crud.md) | 角色 CRUD、文件、Voice、权限 |
| 05 | [首页、搜索与 Friend](./chapter-05-friend-system.md) | [Friend System](./en/chapter-05-friend-system.md) | 分页、搜索、Friend 关系/唯一约束 |
| 06 | [最小 LLM Chat](./chapter-06-basic-chat.md) | [Basic LLM Chat](./en/chapter-06-basic-chat.md) | Django 调 LLM、Vue 发消息 |
| 07 | [SSE 流式聊天](./chapter-07-sse.md) | [SSE Streaming](./en/chapter-07-sse.md) | 流式输出、刷新、取消、Message 落库 |
| 08 | [LangGraph Tool Calling](./chapter-08-langgraph-tools.md) | [LangGraph Tools](./en/chapter-08-langgraph-tools.md) | SystemPrompt、多轮上下文、ToolNode |
| 09 | [长期记忆](./chapter-09-memory.md) | [Long-Term Memory](./en/chapter-09-memory.md) | 历史压缩为 Friend.memory |
| 10 | [RAG + LanceDB](./chapter-10-rag.md) | [RAG + LanceDB](./en/chapter-10-rag.md) | Chunk、Embedding、Retrieval、Eval |
| 11 | [ASR](./chapter-11-asr.md) | [ASR](./en/chapter-11-asr.md) | 浏览器录音 → PCM → 后端 → 文字 |
| 12 | [流式 TTS](./chapter-12-tts.md) | [Streaming TTS](./en/chapter-12-tts.md) | LLM 文本同步转语音并连续播放 |
| 13 | [全链路毕业实验](./chapter-13-capstone.md) | [Full-System Capstone](./en/chapter-13-capstone.md) | 完整请求追踪与跨层功能改造 |

---

# 第二阶段：Chapter 14–20

| Chapter | 中文实验 | English Lab | 工程能力 |
|---|---|---|---|
| 14 | [Testing / TDD](./chapter-14-testing-tdd.md) | [Testing / TDD](./en/chapter-14-testing-tdd.md) | 自动测试、回归测试、CI feedback |
| 15 | [DRF 工程化](./chapter-15-drf-engineering.md) | [DRF Engineering](./en/chapter-15-drf-engineering.md) | Serializer、Validation、Status Code |
| 16 | [配置与多模型](./chapter-16-config-providers.md) | [Config / Providers](./en/chapter-16-config-providers.md) | mock/text/full、Feature Flag、Provider |
| 17 | [异步与取消](./chapter-17-stream-cancellation.md) | [Cancellation](./en/chapter-17-stream-cancellation.md) | AbortController、SSE、Queue、cancel_event |
| 18 | [数据与安全](./chapter-18-data-security.md) | [Data / Security](./en/chapter-18-data-security.md) | Constraint、Migration、权限、隐私、安全 |
| 19 | [RAG / Memory Eval](./chapter-19-rag-memory-eval.md) | [RAG / Memory Eval](./en/chapter-19-rag-memory-eval.md) | Citation、Eval Set、Structured Memory |
| 20 | [CI / Deploy / Observability](./chapter-20-ci-deploy-observability.md) | [CI / Deploy / Observability](./en/chapter-20-ci-deploy-observability.md) | CI、Build、Health、Logging、Docker、Metrics |

工程进阶总览：

- 中文：[`docs/ENGINEERING_COURSE.md`](../docs/ENGINEERING_COURSE.md)
- English：[`docs/ENGINEERING_COURSE_EN.md`](../docs/ENGINEERING_COURSE_EN.md)

---

## “机器反馈”

### 环境自检

```bash
cd backend
python manage.py doctor
```

### 初始化教学数据

```bash
python manage.py seed_demo
```

### Chapter 结构 grader

项目根目录：

```bash
python scripts/grade.py --chapter 7
python scripts/grade.py --chapter 20
```

### Backend behavior tests

```bash
cd backend
python manage.py test web
```

### Frontend tests / quality / build

```bash
cd frontend
npm run check
```

PR 还会在 GitHub Actions 的干净环境重新运行 backend、frontend 与 learning Docker image 检查。

---

## 每个实验都遵守这 8 步

1. **先写预测**：数据会经过哪些文件？
2. **只做最小闭环**。
3. **先写/找到验收条件**。
4. **打开 DevTools / Django 日志**。
5. **一次只改一个层级**。
6. **主动制造一个错误**并定位它。
7. **运行 grader / test / build**，不要只凭肉眼。
8. **Git commit**，写清楚为什么需要这项技术。

---

## 什么叫“完成实验”？

不是页面看起来差不多。

至少要能回答：

- 请求从哪个 Vue 文件发出？
- URL / Method / Header / Body 是什么？
- Django 哪个 View 接住？
- 读写哪些 Model / 数据存储？
- 哪些数据进入 LLM / Tool / RAG？
- 流式数据如何回来？
- 如何取消？
- ownership 在哪里验证？
- 出错先看哪里？
- 哪一个自动测试证明关键行为没坏？
- 这个设计做了什么 trade-off？

---

## 配套资料

### 中文

- [零基础学习中心](../docs/README.md)
- [工程进阶课程](../docs/ENGINEERING_COURSE.md)
- [从 0 复刻课程](../docs/COURSE_REBUILD.md)
- [零基础完整教程](../docs/BEGINNER_TUTORIAL.md)
- [API Reference](../docs/API_REFERENCE.md)
- [数据库 ER 图](../docs/DATABASE_ER.md)
- [架构与请求链路](../docs/ARCHITECTURE.md)
- [排错手册](../docs/TROUBLESHOOTING.md)

### English

- [English Learning Hub](../docs/README_EN.md)
- [English Quick Start](../docs/QUICK_START_EN.md)
- [English Architecture Guide](../docs/ARCHITECTURE_EN.md)
- [English Engineering Course](../docs/ENGINEERING_COURSE_EN.md)
- [English API Reference](../docs/API_REFERENCE_EN.md)
- [English Database / ER Guide](../docs/DATABASE_ER_EN.md)
- [English Troubleshooting](../docs/TROUBLESHOOTING_EN.md)
- [English Labs](./en/README.md)
