# AiFriends 实验课（Labs）

> 目标：把“我看懂了”升级成“我能自己写出来，而且能证明自己写对了”。

Labs 分成两段：

```text
Chapter 00–13：从零做出完整 AI 全栈应用
Chapter 14–20：把 AI Demo 升级成可靠工程项目
```

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

真实历史 commit 是“工程考古材料”，不一定等于标准答案。历史中可能包含当时尚未修复的 bug；课程最终参考应以当前测试、实验验收与后续 canonical solution 为准。

每完成一章：

```bash
git add .
git commit -m "learn: finish chapter 03 jwt auth"
```

---

# 第一阶段：Chapter 00–13

| Chapter | 实验 | 你要做出来的东西 |
|---|---|---|
| 00 | [环境与骨架](./chapter-00-environment.md) | Python/Node/Git 环境、前后端可启动 |
| 01 | [Vue 页面与 Router](./chapter-01-vue-router.md) | 页面、路由、组件通信 |
| 02 | [Django + ORM + SQLite](./chapter-02-django-orm.md) | Model、migration、Admin、基础 API |
| 03 | [注册登录 + JWT](./chapter-03-jwt-auth.md) | 注册、登录、Pinia、Axios Token 刷新 |
| 04 | [Character CRUD](./chapter-04-character-crud.md) | 角色增删改查、图片、Voice |
| 05 | [首页、搜索与 Friend](./chapter-05-friend-system.md) | 分页、搜索、Friend 关系 |
| 06 | [最小 LLM Chat](./chapter-06-basic-chat.md) | Django 调 LLM、Vue 发消息 |
| 07 | [SSE 流式聊天](./chapter-07-sse.md) | 流式输出与 Message 落库 |
| 08 | [LangGraph Tool Calling](./chapter-08-langgraph-tools.md) | SystemPrompt、多轮上下文、ToolNode |
| 09 | [长期记忆](./chapter-09-memory.md) | 历史压缩为 Friend.memory |
| 10 | [RAG + LanceDB](./chapter-10-rag.md) | Chunk、Embedding、向量检索 Tool |
| 11 | [ASR](./chapter-11-asr.md) | 浏览器录音 → PCM → 后端 → 文字 |
| 12 | [流式 TTS](./chapter-12-tts.md) | LLM 文本同步转语音并连续播放 |
| 13 | [全链路毕业实验](./chapter-13-capstone.md) | 完整请求追踪与跨层功能改造 |

---

# 第二阶段：Chapter 14–20

| Chapter | 实验 | 你要学会的工程能力 |
|---|---|---|
| 14 | [Testing / TDD](./chapter-14-testing-tdd.md) | 自动测试、回归测试、CI feedback |
| 15 | [DRF 工程化](./chapter-15-drf-engineering.md) | Serializer、Validation、Status Code |
| 16 | [配置与多模型](./chapter-16-config-providers.md) | mock/text/full、Feature Flag、Provider |
| 17 | [异步与取消](./chapter-17-stream-cancellation.md) | AbortController、SSE、Queue、cancel_event |
| 18 | [数据与安全](./chapter-18-data-security.md) | Constraint、Transaction、权限、隐私 |
| 19 | [RAG / Memory Eval](./chapter-19-rag-memory-eval.md) | Citation、Eval Set、Structured Memory |
| 20 | [CI / Deploy / Observability](./chapter-20-ci-deploy-observability.md) | CI、Build、Health、Logging、Docker 思维 |

工程进阶总览：[`docs/ENGINEERING_COURSE.md`](../docs/ENGINEERING_COURSE.md)。

---

## 第四轮新增的“机器反馈”

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
```

### Backend behavior tests

```bash
cd backend
python manage.py test web
```

### Frontend tests / quality / build

```bash
cd frontend
npm test
npm run lint
npm run build
```

或一次执行：

```bash
npm run check
```

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
- URL / Method / Body 是什么？
- Django 哪个 View 接住？
- 读写哪些 Model？
- 哪些数据进入 LLM？
- 流式数据如何回来？
- 如何取消？
- 出错先看哪里？
- 哪一个自动测试证明关键行为没坏？

---

## 配套资料

- [工程进阶课程](../docs/ENGINEERING_COURSE.md)
- [从 0 复刻课程](../docs/COURSE_REBUILD.md)
- [零基础完整教程](../docs/BEGINNER_TUTORIAL.md)
- [API Reference](../docs/API_REFERENCE.md)
- [数据库 ER 图](../docs/DATABASE_ER.md)
- [架构与请求链路](../docs/ARCHITECTURE.md)
- [排错手册](../docs/TROUBLESHOOTING.md)
