# AiFriends 自动验收与学习反馈

> 目标：不要用“页面看起来差不多”判断自己是否学会。

AiFriends 第四轮开始提供四层反馈。

---

## Level 1：环境反馈 `doctor`

```bash
cd backend
python manage.py doctor
```

它检查“你能不能开始这一模式的学习”：Python、数据库、AI 配置、Prompt、Voice、RAG、VAD 等。

`doctor` 的 Warning 不一定阻止学习。例如 mock/text-only 模式没有 Voice 是允许的。

---

## Level 2：课程结构 grader

项目根目录：

```bash
python scripts/grade.py --chapter 3
python scripts/grade.py --chapter 7
python scripts/grade.py --chapter 13
```

它只回答：

> 预期的文件/概念是否已经接进正确层级？

它不能证明行为绝对正确。

---

## Level 3：Behavior Tests

后端：

```bash
cd backend
python manage.py test web
```

前端：

```bash
cd frontend
npm test
```

这里验证可重复行为，例如密码 hash、refresh cookie、mock SSE、single-flight token refresh。

---

## Level 4：Build / CI

前端本地：

```bash
npm run check
```

GitHub PR 会运行：

```text
.github/workflows/ci.yml
```

覆盖：

```text
Python compile
Django system check
Django tests
npm ci
VAD setup
frontend quality check
Node tests
Vite build
```

---

# 失败时怎么看？

推荐顺序：

```text
doctor 失败
→ 环境/配置问题

grade 失败
→ 课程结构/文件问题

unit test 失败
→ 某个具体行为回归

build 失败
→ import / bundle / frontend production build 问题

CI 失败但本地成功
→ 环境差异、未提交文件、大小写、lockfile 等问题
```

---

# 为什么真实历史 Commit 不是“标准答案”？

`COURSE_REBUILD.md` 使用真实历史帮助你观察项目如何演进。

真实历史可能包含：

```text
当时尚未发现的 bug
临时写法
后续才修复的接口
不完整的错误处理
```

因此请这样理解：

```text
历史 commit = 工程考古 / 思考材料
当前测试通过的实现 = 当前参考实现
实验验收条件 = 你需要证明的学习目标
```

未来还可以增加：

```text
course/chXX-start
course/chXX-solution
```

作为稳定的 canonical checkpoint。

---

# 最推荐的每章闭环

```text
读需求
 ↓
写预测
 ↓
实现最小版本
 ↓
python scripts/grade.py --chapter N
 ↓
相关 unit test
 ↓
主动制造一个 bug
 ↓
从日志/Network 定位
 ↓
修复
 ↓
全套 check
 ↓
git commit
```

当你开始依赖“证据”而不是“感觉”判断代码时，你已经跨过了非常重要的一道工程门槛。
