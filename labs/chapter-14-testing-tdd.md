# Chapter 14 Lab：Testing / TDD / 自动判错

## 本章目标

把“页面看起来能用”升级成：

> **我能用自动化证据证明关键功能没有被改坏。**

本轮已经加入：

```text
backend/web/tests.py
frontend/tests/singleFlight.test.js
scripts/grade.py
.github/workflows/ci.yml
```

---

## TODO 1：跑后端测试

```bash
cd backend
python manage.py test web
```

要求你能区分：

```text
测试数据库
真实开发数据库
```

并解释为什么测试不应该污染 `db.sqlite3`。

### 当前重点测试

- AI_MODE 配置；
- 注册密码 hash；
- 重复用户名；
- 错误密码；
- refresh cookie；
- mock SSE；
- ASR feature flag。

---

## TODO 2：跑前端测试

```bash
cd frontend
npm test
```

当前测试故意只依赖 Node 自带的 `node:test`，目的是让第一套前端测试尽量轻。

重点阅读：

```text
frontend/src/js/utils/singleFlight.js
frontend/tests/singleFlight.test.js
```

解释：

> 为什么 10 个请求同时 401 时，不应该发 10 次 refresh？

---

## TODO 3：体验红 → 绿

故意把 `singleFlight.js` 改坏：

```js
return task(...args)
```

再运行：

```bash
npm test
```

你应该看到并发测试失败。

恢复代码，让测试重新变绿。

这就是最小的 TDD 反馈循环。

---

## TODO 4：结构 grader

项目根目录：

```bash
python scripts/grade.py --chapter 7
```

它检查的是“课程结构是否出现了预期概念”，不是行为正确性。

必须理解：

```text
structural grader ≠ unit test ≠ integration test ≠ e2e test
```

---

## TODO 5：写你的第一个回归测试

任选一个真实 bug：

- SSE refresh 没更新 Pinia；
- 注册缺字段抛异常；
- ASR 关闭时仍访问 WSS；
- Mock Chat 意外调用真实模型。

要求：

1. 先写一个会失败的测试；
2. 再修代码；
3. 测试转绿；
4. commit 中写明 root cause。

---

## 验收

- [ ] 能运行后端测试；
- [ ] 能运行前端测试；
- [ ] 能解释 mock 为什么适合 CI；
- [ ] 能故意制造一次 failing test；
- [ ] 能给一个真实 bug 写回归测试；
- [ ] 能解释“测试通过”为什么仍不代表产品绝对没 bug。

---

## Challenge

为 `get_vite_entry()` 增加测试：

```text
manifest 不存在
manifest 有 index.html
manifest 只有 isEntry
CSS 有 0/1/多个文件
```

并把测试加入 CI。
