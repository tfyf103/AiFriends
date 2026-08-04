# 🤖 AiFriends

> 一个探索 **AI 角色陪伴、智能交互与长期记忆** 的全栈应用。

AiFriends 旨在打造一个具有个性化角色、自然语言交流、语音交互能力的 AI 伙伴平台。

用户可以创建属于自己的 AI 角色，为角色设定外观、背景、性格与声音，并通过文字或语音与 AI 进行持续交流。

---

## ✨ 项目亮点

### 🎭 AI 角色系统

- 创建属于自己的 AI 角色
- 自定义角色名称、头像、背景图片
- 编写角色设定与人格描述
- 为不同角色配置独立音色

### 💬 智能对话

- 支持自然语言聊天
- 流式输出对话内容
- 支持角色上下文扩展
- 支持好友关系与聊天记录管理

### 🎙️ 语音交互

- 浏览器端语音输入
- 后端语音识别处理
- AI 回复语音合成
- 支持角色独立声音配置

### 🧠 知识库与长期记忆探索

- 集成向量数据库能力
- 支持知识库扩展
- 为 AI 角色提供更丰富的上下文信息

---

## 🏗️ 系统架构

```text
                 用户
                  │
                  ▼
        ┌─────────────────┐
        │   Vue 3 前端     │
        │  Chat / Voice   │
        └────────┬────────┘
                 │ HTTP / SSE / WebSocket
                 ▼
        ┌─────────────────┐
        │ Django 后端服务  │
        │ API / Auth / AI │
        └────────┬────────┘
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
  LLM服务    向量数据库    语音服务
```

---

## 🛠️ 技术栈

### Backend

- Python
- Django 6
- Django REST Framework
- Simple JWT
- LangChain
- LangGraph
- LanceDB
- WebSocket / Server-Sent Events

### Frontend

- Vue 3
- Vite
- Pinia
- Vue Router
- Axios
- Tailwind CSS
- daisyUI

### AI 能力

- 大语言模型调用
- Agent 工作流编排
- 向量检索增强生成（RAG）
- 语音识别（ASR）
- 语音合成（TTS）

---

## 📂 项目结构

```text
AiFriends/
│
├── backend/          # Django 后端服务
│   ├── API接口
│   ├── 数据模型
│   ├── 用户系统
│   └── AI能力模块
│
├── frontend/         # Vue 前端应用
│   ├── 页面组件
│   ├── 状态管理
│   └── 聊天交互
│
├── requirements.txt  # Python依赖
└── README.md
```

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/tfyf103/AiFriends.git
cd AiFriends
```

### 2. 后端启动

创建 Python 环境：

```bash
python -m venv .venv
```

安装依赖：

```bash
pip install -r requirements.txt
```

配置环境变量：

```env
API_KEY=your_api_key
WSS_URL=your_websocket_service_url
```

启动服务：

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

### 3. 前端启动

```bash
cd frontend
npm install
npm run dev
```

---

## 📖 使用流程

1. 注册账号并登录
2. 创建 AI 角色
3. 设置角色资料和声音
4. 进入聊天页面
5. 使用文字或语音与 AI 伙伴交流

---

## 🗺️ Roadmap

### 基础能力

- [x] AI角色创建
- [x] 文本聊天
- [x] 语音输入
- [x] 语音合成
- [x] 自定义角色音色

### 持续优化

- [ ] 完善长期记忆系统
- [ ] 增加多模型支持
- [ ] 优化角色人格系统
- [ ] 增加 Docker 部署方案
- [ ] 完善 API 文档
- [ ] 增加自动化测试

---

## 🤝 参与贡献

欢迎提交 Issue 或 Pull Request，一起探索 AI 伙伴应用的新方向。

贡献代码前建议确认：

- 不包含敏感信息和 API 密钥
- 功能可以正常运行
- 前端可以正常构建
- 数据库迁移保持同步

---

## 📄 License

当前项目暂未声明开源许可证。

如果你希望使用、修改或分发本项目，请先联系项目作者确认授权。
