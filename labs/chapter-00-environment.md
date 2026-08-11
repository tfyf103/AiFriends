# Chapter 00 Lab：从空电脑到前后端都能启动

## 本章目标

你不写业务功能，只完成一件事：**建立一个任何新手都能重复的开发环境**。

完成后应该同时看到：

```text
Vite:   http://localhost:5173
Django: http://127.0.0.1:8000
```

---

## 起点

建议先阅读：

- [`docs/BEGINNER_TUTORIAL.md`](../docs/BEGINNER_TUTORIAL.md)
- 根目录 [`.env.example`](../.env.example)

你需要安装：

- Git
- Python 3.12 / 3.13
- Node.js（满足 `frontend/package.json` 的 engines）
- VS Code（推荐，不强制）

---

## TODO 1：证明工具真的可用

在终端执行并记录输出：

```bash
git --version
python --version
node --version
npm --version
```

### 验收

- [ ] 4 条命令都能正常运行
- [ ] 知道 `python` 如果不可用时 Windows 上可能需要尝试 `py`
- [ ] 知道 Node 和 npm 是前端工具，不是 Python 依赖

---

## TODO 2：克隆并认识目录

```bash
git clone https://github.com/tfyf103/AiFriends.git
cd AiFriends
```

不要马上运行程序。先自己写出下面目录的用途：

```text
backend/
frontend/
docs/
labs/
requirements.txt
.env.example
```

### 验收

你应该能解释：

> `requirements.txt` 管 Python；`frontend/package.json` 管 JavaScript。它们是两个独立运行环境。

---

## TODO 3：Python 虚拟环境

创建：

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

安装：

```bash
pip install -r requirements.txt
```

### 必须观察

激活前后执行：

```bash
python -c "import sys; print(sys.executable)"
```

看看 Python 路径发生了什么变化。

---

## TODO 4：环境变量

复制：

```bash
cp .env.example .env
```

Windows 可以手动复制文件。

打开 `.env`，理解：

```text
API_KEY   = 访问模型/语音服务的凭证
API_BASE  = OpenAI-compatible HTTP API 地址
WSS_URL   = ASR/TTS WebSocket 服务地址
```

### 安全实验

执行：

```bash
git status
```

确认真实 `.env` 不会进入 Git 提交。

- [ ] `.env` 没有被准备提交
- [ ] `.env.example` 可以提交
- [ ] 能解释为什么不能把 API Key 写进 README

---

## TODO 5：启动 Django

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

另开终端访问：

```text
http://127.0.0.1:8000
```

### 故障实验

故意停止 Django，再刷新浏览器。

观察浏览器报错与终端状态，理解：

> 前端页面问题 ≠ 后端服务器没启动。

---

## TODO 6：启动 Vue

新开终端：

```bash
cd frontend
npm install
npm run dev
```

访问：

```text
http://localhost:5173
```

---

## 参考答案思路

这一章没有“代码答案”。正确答案是你能清楚区分：

```text
系统级工具
├── Git
├── Python
└── Node

Python 项目环境
├── .venv
└── requirements.txt

前端环境
├── node_modules
└── package.json

运行进程
├── Django :8000
└── Vite   :5173
```

---

## 常见错误

### `ModuleNotFoundError`

先确认虚拟环境是否激活，再确认 `pip install -r requirements.txt` 是否成功。

### `npm` 不是命令

Node 没安装好或终端还没刷新 PATH。

### 端口占用

不要直接乱杀进程。先确认哪个程序占用了 5173/8000，再决定是否关闭或换端口。

### `.env` 有了但 Django 读不到

确认运行目录、文件名以及 `python-dotenv` 是否安装。

---

## Challenge

写一个 `MY_SETUP_NOTES.md`（不要提交秘密），记录：

- 操作系统
- Python 版本
- Node 版本
- 你遇到的第一个错误
- 你如何定位它

如果未来换电脑，只看这份笔记能重新把项目跑起来，才算真正完成 Chapter 00。
