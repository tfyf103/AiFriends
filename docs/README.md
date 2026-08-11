# AiFriends 零基础学习地图

> 目标：让一个只会“安装软件、复制命令”的新手，也能从 **0** 跑起 AiFriends，并在复刻过程中真正理解 Vue、Django、REST API、JWT、SSE、LangChain、LangGraph、RAG、长期记忆、ASR 与 TTS。

---

## 你会学到什么？

完成整套教程后，你应该能够回答下面这些问题：

- 浏览器输入一句话后，到底经过了哪些文件？
- Vue 的 `ref`、组件、事件、路由、Pinia 分别负责什么？
- Axios 为什么要拦截请求？JWT 的 access token 和 refresh token 有什么区别？
- Django 的 URL、View、Model 是怎么连起来的？
- 什么是 REST API？什么是前后端分离？
- 为什么普通 HTTP 请求不能像 ChatGPT 一样一个字一个字输出？
- SSE 是什么？它与 WebSocket 有什么区别？
- LangChain 在本项目里到底做了什么？
- LangGraph 为什么比“直接调用一次 LLM”更适合 Agent？
- `@tool`、`bind_tools()`、`ToolNode`、`StateGraph` 是怎么配合的？
- 长期记忆为什么不能把所有聊天记录永久塞进 prompt？
- RAG 为什么要“切块 → Embedding → 向量数据库 → 相似度检索”？
- LanceDB 在本项目里保存的是什么？
- 语音识别（ASR）和语音合成（TTS）分别位于哪一层？
- 为什么前端要用 MediaSource 连续播放流式 MP3？

---

## 推荐学习顺序

### 第 0 阶段：完全不懂代码也先跑起来

阅读：[`BEGINNER_TUTORIAL.md`](./BEGINNER_TUTORIAL.md)

先完成：

1. 安装 Git
2. 安装 Python 3.12 / 3.13
3. 安装 Node.js 20.19+ 或 22.12+
4. 克隆项目
5. 创建 Python 虚拟环境
6. 安装 Python 依赖
7. 创建 `.env`
8. 数据库迁移
9. 启动 Django
10. 安装前端依赖
11. 启动 Vite
12. 注册用户并创建角色

如果第 0 阶段没跑通，**不要急着学 LangChain**。先去看 [`TROUBLESHOOTING.md`](./TROUBLESHOOTING.md)。

---

### 第 1 阶段：先理解网页为什么能动

重点文件：

```text
frontend/src/main.js
frontend/src/router/index.js
frontend/src/stores/user.js
frontend/src/js/http/api.js
frontend/src/js/http/streamApi.js
frontend/src/js/config/config.js
```

你需要建立下面这个心智模型：

```text
main.js
  ↓ 创建 Vue 应用
App.vue
  ↓ Router 决定显示哪个页面
views/*
  ↓ 页面组合 components/*
components/*
  ↓ 用户点击 / 输入
api.js / streamApi.js
  ↓ HTTP 请求
Django
```

这一阶段不要死背 Vue API，先理解：

- 数据改变为什么页面会自动更新？
- 父组件怎么把数据传给子组件？
- 子组件怎么告诉父组件“我发生了某件事”？
- 为什么登录状态适合放在 Pinia？
- 为什么路由守卫能阻止未登录用户进入某些页面？

---

### 第 2 阶段：理解 Django 后端

重点文件：

```text
backend/manage.py
backend/backend/settings.py
backend/backend/urls.py
backend/web/urls.py
backend/web/models/*
backend/web/views/*
```

先把 Django 理解成 4 层：

```text
URL
 ↓
View
 ↓
Model / Service
 ↓
Database / AI Service
```

例如聊天接口：

```text
POST /api/friend/message/chat/
    ↓
web/urls.py
    ↓
MessageChatView
    ↓
Friend / Message / SystemPrompt
    ↓
CharGraph
    ↓
LLM / Tools / RAG
```

---

### 第 3 阶段：理解认证

本项目使用 JWT。

核心概念：

```text
登录成功
  ↓
access token
  ↓
每个 API 请求：Authorization: Bearer xxx
  ↓
access token 过期
  ↓
refresh token 换一个新的 access token
  ↓
重新发送原请求
```

重点文件：

```text
frontend/src/stores/user.js
frontend/src/js/http/api.js
frontend/src/js/http/streamApi.js
backend/backend/settings.py
backend/web/views/user/account/*
```

---

### 第 4 阶段：追踪“一句话”的完整生命周期

这是整个项目最重要的一节。

```text
InputField.vue
  ↓
streamApi('/api/friend/message/chat/')
  ↓
MessageChatView.post()
  ↓
add_system_prompt()
  ↓
add_recent_messages()
  ↓
CharGraph.create_app()
  ↓
LangGraph Agent
  ├─ 普通回答 → LLM
  ├─ 需要时间 → get_time()
  └─ 需要知识库 → search_knowledge_base()
  ↓
astream(..., stream_mode='messages')
  ↓
SSE 文本片段 + TTS 音频片段
  ↓
InputField.vue
  ├─ 拼接 AI 文本
  └─ MediaSource 播放 MP3
  ↓
Message.objects.create(...)
  ↓
每 5 轮触发 update_memory(friend)
```

只要你真正看懂这张图，就已经理解了这个项目 60% 以上的核心。

---

### 第 5 阶段：LangChain / LangGraph

重点文件：

```text
backend/web/views/friend/message/chat/graph.py
backend/web/views/friend/message/chat/chat.py
```

本项目不是简单：

```python
llm.invoke('你好')
```

而是：

```text
StateGraph
  ↓
agent 节点
  ↓
LLM 判断是否调用工具
  ├─ 否 → END
  └─ 是 → tools 节点
             ↓
          ToolNode
             ↓
          agent 再思考
```

这就是一个最小可理解的 Agent 工作流。

---

### 第 6 阶段：长期记忆

重点文件：

```text
backend/web/models/friend.py
backend/web/views/friend/message/memory/graph.py
backend/web/views/friend/message/memory/update.py
backend/web/views/friend/message/chat/chat.py
```

本项目把记忆分成两种：

1. **近期对话**：最近若干条 Message。
2. **长期记忆**：压缩后写入 `Friend.memory`。

核心思想：

```text
越来越长的聊天记录
      ↓
选最近对话
      ↓
LLM 总结 / 更新记忆
      ↓
Friend.memory
      ↓
以后每次聊天放进系统上下文
```

---

### 第 7 阶段：RAG / 知识库

重点文件：

```text
backend/web/documents/utils/custom_embeddings.py
backend/web/documents/utils/insert_documents.py
backend/web/views/friend/message/chat/graph.py
```

链路：

```text
原始文档
  ↓ TextLoader
Document
  ↓ RecursiveCharacterTextSplitter
多个文本块
  ↓ CustomEmbeddings
向量
  ↓ LanceDB
向量数据库

用户问题
  ↓ Embedding
问题向量
  ↓ similarity_search(k=3)
最相关文本块
  ↓
作为 Tool 结果回到 LLM
```

---

### 第 8 阶段：语音

ASR：

```text
浏览器麦克风
  ↓
PCM
  ↓
/api/friend/message/asr/asr/
  ↓
WebSocket
  ↓
ASR 服务
  ↓
文字
```

TTS：

```text
LLM 流式 token
  ↓
后端 WebSocket TTS
  ↓
MP3 二进制片段
  ↓ Base64
SSE
  ↓
前端 Base64 → Uint8Array
  ↓
MediaSource / SourceBuffer
  ↓
连续播放
```

---

## 建议的“复刻式学习法”

不要只阅读最终代码。建议新建一个空目录，按下面顺序自己重写：

```text
01-vue-static-page
02-vue-router
03-pinia-user-state
04-django-project
05-django-models
06-register-login-jwt
07-character-crud
08-friend-list
09-basic-chat
10-sse-streaming
11-langchain-llm
12-langgraph-agent
13-tool-calling
14-long-term-memory
15-rag-lancedb
16-asr
17-tts-streaming
18-full-aifriends
```

每完成一步都 commit：

```bash
git add .
git commit -m "learn: step 01 vue static page"
```

你最终得到的不只是一个能运行的项目，而是一条完整的学习轨迹。

---

## 学习时必须养成的调试习惯

每当“不工作”，都先判断问题在哪一层：

```text
浏览器 UI？
  ↓
Vue 状态？
  ↓
网络请求？
  ↓
Django URL？
  ↓
View？
  ↓
数据库？
  ↓
LLM？
  ↓
Tool / RAG？
  ↓
第三方语音服务？
```

推荐同时打开：

- VS Code
- 浏览器 DevTools → Console
- 浏览器 DevTools → Network
- Django 终端
- Vite 终端

不要只看页面上的一句“失败”。

---

## 文档导航

- [零基础完整复刻教程](./BEGINNER_TUTORIAL.md)
- [系统架构与请求链路](./ARCHITECTURE.md)
- [常见报错与排查手册](./TROUBLESHOOTING.md)
- [返回项目 README](../README.md)
