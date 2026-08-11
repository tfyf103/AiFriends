# AiFriends 实验课（Labs）

> 目标：把“我看懂了”升级成“我能自己写出来”。
>
> 这一目录与 [`docs/COURSE_REBUILD.md`](../docs/COURSE_REBUILD.md) 的 Chapter 00–13 一一对应。每个实验都要求你从一个明确的起点开始，完成 TODO，最后按验收清单自己证明功能真的可用。

---

## 推荐用法

不要在主项目分支里直接做实验。建议新建自己的学习分支：

```bash
git switch main
git pull
git switch -c learn/aifriends
```

如果某一章提供了历史 commit 检查点，可以先观察真实项目当时的状态：

```bash
git show <commit-sha>
git diff <old-sha> <new-sha>
```

然后**回到自己的学习分支**自己实现，而不是长期停留在 detached HEAD：

```bash
git switch learn/aifriends
```

每完成一个实验都提交一次：

```bash
git add .
git commit -m "learn: finish chapter 03 jwt auth"
```

---

## 实验目录

| Chapter | 实验 | 你要做出来的东西 |
|---|---|---|
| 00 | [环境与骨架](./chapter-00-environment.md) | Python/Node/Git 环境、前后端可启动 |
| 01 | [Vue 页面与 Router](./chapter-01-vue-router.md) | 三个页面、路由跳转、组件通信 |
| 02 | [Django + ORM + SQLite](./chapter-02-django-orm.md) | Model、migration、Admin、基础 API |
| 03 | [注册登录 + JWT](./chapter-03-jwt-auth.md) | 注册、登录、Pinia、Axios 自动带 Token |
| 04 | [Character CRUD](./chapter-04-character-crud.md) | 角色增删改查、图片上传、音色选择 |
| 05 | [首页、搜索与好友](./chapter-05-friend-system.md) | 无限加载、搜索、Friend 关系 |
| 06 | [最小 LLM Chat](./chapter-06-basic-chat.md) | Django 调 LLM、Vue 发消息 |
| 07 | [SSE 流式聊天](./chapter-07-sse.md) | token 级流式输出与历史落库 |
| 08 | [LangGraph Tool Calling](./chapter-08-langgraph-tools.md) | SystemPrompt、多轮上下文、ToolNode 循环 |
| 09 | [长期记忆](./chapter-09-memory.md) | 历史压缩为 Friend.memory |
| 10 | [RAG + LanceDB](./chapter-10-rag.md) | 文档切块、Embedding、向量检索 Tool |
| 11 | [ASR](./chapter-11-asr.md) | 浏览器录音 → PCM → 后端 → 文字 |
| 12 | [流式 TTS](./chapter-12-tts.md) | LLM 文本流同步转语音并连续播放 |
| 13 | [全链路毕业实验](./chapter-13-capstone.md) | 从输入到 Memory/RAG/语音完整追踪与改造 |

---

## 每个实验都遵守这 7 步

1. **先写预测**：你认为数据会经过哪些文件？
2. **只做最小闭环**：先让最简单版本工作。
3. **打开 DevTools / Django 终端**：不要盲猜。
4. **一次只改一个层级**：前端、后端、AI 服务不要同时乱改。
5. **按验收清单逐项验证**。
6. **主动制造一个错误**，再用日志定位它。
7. **提交 Git commit**，写一句“这一章为什么需要这项技术”。

---

## 什么叫“完成实验”？

不是页面看起来差不多就算完成。

至少要能回答：

- 请求从哪个 Vue 文件发出？
- 请求 URL、Method、Body 是什么？
- Django 哪个 URL pattern 接住它？
- 哪个 View 执行业务逻辑？
- 读写了哪些 Model？
- 哪些数据进入 LLM？
- 流式数据如何回到浏览器？
- 出错时应该先看哪里？

如果答不上来，说明你只是把代码“跑起来”了，还没有真正掌握它。

---

## 配套资料

- [从 0 复刻课程](../docs/COURSE_REBUILD.md)
- [零基础完整教程](../docs/BEGINNER_TUTORIAL.md)
- [API Reference](../docs/API_REFERENCE.md)
- [数据库 ER 图](../docs/DATABASE_ER.md)
- [架构与请求链路](../docs/ARCHITECTURE.md)
- [排错手册](../docs/TROUBLESHOOTING.md)
