# AiFriends 零基础学习中心

> 目标：让只会安装软件、复制命令的新手，也能从 **0** 跑起 AiFriends，并在复刻过程中真正理解 Vue、Django、REST API、JWT、SSE、LangChain、LangGraph、RAG、长期记忆、ASR 与 TTS。

---

## 从哪里开始？

如果你是第一次接触全栈 + AI 应用开发，请严格按下面顺序：

```text
① 项目 README：先知道 AiFriends 是什么
        ↓
② BEGINNER_TUTORIAL：先把最终项目跑起来
        ↓
③ COURSE_REBUILD：按真实 Git 历史从零重新造一遍
        ↓
④ 阅读带教学注释的核心源码
        ↓
⑤ ARCHITECTURE：从系统角度串起全部数据流
        ↓
⑥ TROUBLESHOOTING：遇到问题按层排查
```

### 核心文档

- **[零基础完整运行与复刻教程](./BEGINNER_TUTORIAL.md)**：第一次启动项目、安装环境、配置 Django/Vue/LLM。
- **[按真实 Git 历史逐章复刻](./COURSE_REBUILD.md)**：从 Vue 页面一路重建到 LangGraph、RAG、ASR、TTS，每章都有真实 commit 检查点、动手任务和验收标准。
- **[系统架构与请求链路](./ARCHITECTURE.md)**：从“浏览器输入一句话”追踪到 Django、LangGraph、LLM、Tool、TTS、数据库和长期记忆。
- **[常见报错与排查手册](./TROUBLESHOOTING.md)**：Python、Node、JWT、CORS、SSE、LLM、RAG、ASR/TTS 等问题的分层排查方法。
- **[返回项目首页](../README.md)**。

---

# 你最终应该学会什么？

完成整套学习后，你应该能独立回答：

- Vue 的 `ref`、props、emits、Router、Pinia 各自解决什么问题？
- Axios 为什么需要请求/响应拦截器？
- JWT 的 access token 和 refresh token 为什么要分开？
- Django 的 URL、View、Model、ORM、Migration 是怎么连接起来的？
- 一个 Character 怎样从 Vue 表单进入 SQLite 和 media 目录？
- 一条聊天消息经过了哪些前后端文件？
- 为什么普通 JSON 响应无法实现 ChatGPT 式逐段输出？
- SSE 与 WebSocket 的职责有什么不同？
- LangChain 在 AiFriends 中到底负责什么？
- LangGraph 的 State、Node、Edge、Conditional Edge 是什么？
- `@tool`、`bind_tools()` 和 `ToolNode` 为什么不是一回事？
- 最近聊天和长期记忆为什么需要同时存在？
- RAG 为什么需要 Loader、Chunk、Embedding、VectorStore、Retriever？
- LanceDB 中到底保存的是什么？
- ASR 为什么是“声音 -> 文字”，TTS 为什么是“文字 -> 声音”？
- 为什么前端收到 Base64 MP3 后还需要 MediaSource / SourceBuffer？

---

# 第一阶段：先把项目跑起来

阅读：**[BEGINNER_TUTORIAL.md](./BEGINNER_TUTORIAL.md)**

先完成：

1. 安装 Git
2. 安装 Python
3. 安装 Node.js
4. 克隆项目
5. 创建 Python 虚拟环境
6. `pip install -r requirements.txt`
7. 从 `.env.example` 创建 `.env`
8. Django migration
9. 创建 Django superuser
10. 启动 Django
11. `npm install`
12. 启动 Vite
13. 注册用户
14. 在 Admin 中准备 `Voice` / `SystemPrompt`
15. 创建 AI Character
16. 成功进行一次聊天

如果这一步没跑通，先看：**[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)**。

不要在环境还没成功时急着研究 LangGraph。

---

# 第二阶段：按真实版本重新做一遍

阅读：**[COURSE_REBUILD.md](./COURSE_REBUILD.md)**

这一步不是“阅读最终代码”，而是顺着项目真实开发历史学习：

```text
Chapter 00  环境
Chapter 01  Vue / Router
Chapter 02  Django / SQLite
Chapter 03  JWT / Pinia / Axios
Chapter 04  Character CRUD
Chapter 05  Homepage / Friend
Chapter 06  普通 LLM Chat
Chapter 07  SSE Streaming
Chapter 08  LangGraph / Tool Calling
Chapter 09  Long-term Memory
Chapter 10  RAG / LanceDB
Chapter 11  ASR
Chapter 12  TTS
Chapter 13  Full Pipeline
```

每章都建议你在自己的学习仓库中 commit：

```bash
git add .
git commit -m "learn: chapter 07 sse streaming"
```

这样半年以后你仍然可以看到自己是怎样一步一步把项目做出来的。

---

# 第三阶段：直接读“教材化源码”

第二轮文档改造后，下面这些真实运行文件已经加入了面向零基础的逐段中文解释。

## 1. Vue 聊天入口

```text
frontend/src/components/character/chat_field/input_field/InputField.vue
```

重点学习：

```text
props
emits
ref / useTemplateRef
v-model
@submit.prevent
SSE callback
乐观 UI 更新
processId 取消旧流
Base64 -> Uint8Array
MediaSource
SourceBuffer
```

---

## 2. SSE 客户端

```text
frontend/src/js/http/streamApi.js
```

重点学习：

```text
fetchEventSource
Authorization: Bearer
onopen
onmessage
[DONE]
401 refresh token
重新建立 SSE 连接
```

---

## 3. Django 聊天总调度器

```text
backend/web/views/friend/message/chat/chat.py
```

重点学习：

```text
APIView
IsAuthenticated
SystemMessage
最近聊天上下文
StreamingHttpResponse
generator / yield
threading
asyncio
Queue
WebSocket TTS
SSE
Message 落库
长期记忆触发
```

第一次阅读时只追踪：

```text
post()
 ↓
event_stream()
```

第二次再学习 TTS 的异步部分。

---

## 4. LangGraph Agent

```text
backend/web/views/friend/message/chat/graph.py
```

重点学习：

```text
@tool
bind_tools
AgentState
add_messages
StateGraph
ToolNode
Conditional Edge
START / END
```

当前结构：

```text
START
  ↓
agent
  ↓
有 tool_calls？
  ├─ 否 → END
  └─ 是 → tools
            ↓
          agent
```

---

## 5. 长期记忆

```text
backend/web/views/friend/message/memory/graph.py
backend/web/views/friend/message/memory/update.py
```

重点理解：

```text
最近聊天原文 = 短期上下文
Friend.memory = 长期压缩摘要
```

更新链：

```text
旧 memory
   +
最近对话
   ↓
MemoryGraph
   ↓
新的 memory
```

---

## 6. Embedding / RAG 建库

```text
backend/web/documents/utils/custom_embeddings.py
backend/web/documents/utils/insert_documents.py
```

建库链路：

```text
data.txt
  ↓ TextLoader
Document
  ↓ TextSplitter
Chunks
  ↓ Embedding
Vectors
  ↓ LanceDB
```

查询链路则回到：

```text
backend/web/views/friend/message/chat/graph.py
```

中的：

```text
search_knowledge_base()
```

---

# 第四阶段：追踪“一句话”的完整生命周期

这是整个项目最重要的练习。

```text
InputField.vue
  ↓
streamApi('/api/friend/message/chat/')
  ↓
Authorization: Bearer <JWT>
  ↓
web/urls.py
  ↓
MessageChatView.post()
  ↓
校验 Friend 属于当前用户
  ↓
SystemPrompt + Character.profile + Friend.memory
  ↓
最近 10 条 Message
  ↓
CharGraph.create_app()
  ↓
LangGraph agent
  ├─ 普通回答
  ├─ get_time()
  └─ search_knowledge_base()
          ↓
       Embedding
          ↓
       LanceDB
  ↓
LLM BaseMessageChunk
  ├─ content → Queue → SSE
  └─ content → TTS WebSocket
                    ↓
                 MP3 bytes
                    ↓ Base64
                    └──────→ Queue → SSE
  ↓
浏览器 onmessage
  ├─ content → AI 气泡
  └─ audio → Base64 解码 → MediaSource
  ↓
Message.objects.create(...)
  ↓
每 5 条消息 update_memory(friend)
```

如果你能不看文档自己解释这条链，你已经理解了项目的大部分核心。

---

# 第五阶段：建立“技术是为需求服务”的习惯

不要这样学习：

```text
今天背 Vue API
明天背 Django API
后天背 LangChain API
```

应该这样：

```text
需求：页面要切换
 ↓
Router

需求：多个组件共享用户状态
 ↓
Pinia

需求：API 要知道当前是谁
 ↓
JWT

需求：模型回复要逐步显示
 ↓
SSE

需求：模型要主动查资料
 ↓
Tool Calling + LangGraph

需求：聊天不能无限增长
 ↓
Memory Compression

需求：模型要回答私有资料
 ↓
RAG

需求：用户想说话
 ↓
ASR

需求：AI 想边生成边说话
 ↓
Streaming TTS
```

这才是真正的工程学习方式。

---

# 调试时永远按层排查

看到“聊天失败”，不要直接怀疑模型。

按顺序判断：

```text
UI 输入正确吗？
  ↓
Vue 状态正确吗？
  ↓
Network 请求发出去了吗？
  ↓
JWT 带了吗？
  ↓
URL 命中了吗？
  ↓
Django View 收到了吗？
  ↓
ORM 查到数据了吗？
  ↓
LLM 请求成功吗？
  ↓
LangGraph 路由正确吗？
  ↓
Tool 成功吗？
  ↓
LanceDB 有表吗？
  ↓
SSE 有 chunk 吗？
  ↓
TTS WebSocket 有音频吗？
  ↓
MediaSource 能播放吗？
```

建议开发时同时打开：

- VS Code
- Vite 终端
- Django 终端
- 浏览器 DevTools → Console
- 浏览器 DevTools → Network
- Django Admin

---

# 推荐阅读顺序

### 完全零基础

```text
../README.md
 ↓
BEGINNER_TUTORIAL.md
 ↓
COURSE_REBUILD.md
 ↓
带教学注释的源码
 ↓
ARCHITECTURE.md
```

### 已会 Vue / Django，只想学 AI 应用

```text
COURSE_REBUILD.md Chapter 06
 ↓
Chapter 07 SSE
 ↓
Chapter 08 LangGraph
 ↓
Chapter 09 Memory
 ↓
Chapter 10 RAG
 ↓
Chapter 11/12 Voice
```

### 已会 LangChain，只想理解本项目

```text
ARCHITECTURE.md
 ↓
chat/chat.py
 ↓
chat/graph.py
 ↓
memory/*
 ↓
documents/utils/*
 ↓
InputField.vue
```

---

## 文档导航

- [零基础完整运行与复刻教程](./BEGINNER_TUTORIAL.md)
- [按真实 Git 历史逐章复刻](./COURSE_REBUILD.md)
- [系统架构与请求链路](./ARCHITECTURE.md)
- [常见报错与排查手册](./TROUBLESHOOTING.md)
- [返回项目 README](../README.md)
