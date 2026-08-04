# AiFriends

一个面向 AI 角色陪伴与自然交互场景的全栈项目。用户可以创建自己的 AI 角色，设置角色资料、头像、聊天背景与音色，并通过文字或语音与角色交流。

> 项目仍在持续开发中，接口、配置方式与功能细节可能会继续调整。

## 功能概览

- 用户注册、登录与身份认证
- 创建、编辑和管理 AI 角色
- 自定义角色名称、头像、介绍与聊天背景
- 为不同角色选择独立音色
- 文本对话与流式消息输出
- 浏览器端语音输入
- 后端语音识别与语音合成
- 前端自动播放合成语音
- 基于知识库和向量数据库扩展角色上下文
- 对话记录与好友关系管理

## 技术栈

### 后端

- Python
- Django 6
- Django REST Framework
- Simple JWT
- LangChain / LangGraph
- LanceDB
- WebSocket / Server-Sent Events

### 前端

- Vue 3
- Vite
- Pinia
- Vue Router
- Axios
- Tailwind CSS
- daisyUI
- 浏览器端语音活动检测

## 项目结构

```text
AiFriends/
├── backend/          # Django 后端、接口、模型与管理命令
├── frontend/         # Vue 3 前端工程
├── requirements.txt  # Python 依赖
└── README.md
```

## 本地开发

### 1. 克隆仓库

```bash
git clone https://github.com/tfyf103/AiFriends.git
cd AiFriends
```

### 2. 配置后端环境

建议使用 Python 虚拟环境：

```bash
python -m venv .venv
```

激活虚拟环境：

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

根据实际使用的模型与语音服务，在本地环境中配置所需密钥和服务地址。项目代码中使用到的配置包括：

```env
API_KEY=your_api_key
WSS_URL=your_websocket_service_url
```

请勿将真实密钥提交到 Git 仓库。

执行数据库迁移并启动后端：

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

默认情况下，Django 开发服务器运行在：

```text
http://127.0.0.1:8000
```

### 3. 启动前端

打开新的终端窗口：

```bash
cd frontend
npm install
npm run dev
```

生产构建：

```bash
npm run build
```

前端所需 Node.js 版本以 `frontend/package.json` 中的 `engines` 配置为准。

## 基本使用流程

1. 注册或登录账号。
2. 创建一个 AI 角色。
3. 上传角色头像和聊天背景。
4. 填写角色名称与角色设定。
5. 选择角色音色。
6. 进入聊天页面，通过文字或语音开始对话。

## 开发说明

- 后端接口基于 Django REST Framework。
- 登录状态通过 JWT 维护。
- 前端使用 Pinia 管理状态，Axios 发送接口请求。
- 部分对话和语音能力依赖外部模型服务，请先完成对应环境配置。
- 向量数据库与知识库相关功能依赖项目内的数据初始化流程。

## Roadmap

- [ ] 补充完整的环境变量示例文件
- [ ] 完善自动化测试
- [ ] 优化异常处理与错误提示
- [ ] 完善部署文档
- [ ] 支持更多模型与语音服务
- [ ] 优化知识库管理体验
- [ ] 增强多角色与长期记忆能力

## 贡献

欢迎通过 Issue 提交问题、建议或功能需求，也欢迎提交 Pull Request 参与改进。

提交代码前，建议先确认：

- 新功能能够正常运行
- 未提交任何密钥或隐私数据
- 前端能够成功构建
- 数据库迁移文件与模型改动保持一致

## License

当前仓库暂未声明开源许可证。在添加许可证前，仓库内容默认不代表可以被自由复制、修改或分发。
