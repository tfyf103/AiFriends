# Chapter 01 Lab：Vue 页面、组件与 Router

## 本章目标

不连接 Django，先把“网页为什么会动”弄明白。

你要独立做出：

```text
/
/login
/register
```

并且页面跳转时不整页刷新。

---

## 历史检查点

建议观察：

```text
b1703e8eff39f95dcd8cf3ed7b5d1def0e616758  实现路由
b938159da24699eaec1249251b99ec06884f6b0a  实现登录注册页面
```

比较：

```bash
git diff b1703e8eff39f95dcd8cf3ed7b5d1def0e616758 b938159da24699eaec1249251b99ec06884f6b0a
```

先猜：新增页面以后，Router 到底多了什么？

---

## TODO 1：创建三个页面

每个页面先只显示一个标题：

```text
Homepage
Login
Register
```

要求使用 Vue 单文件组件：

```vue
<script setup>
</script>

<template>
</template>

<style scoped>
</style>
```

### 验收

- [ ] 每个 URL 显示正确页面
- [ ] URL 改变时浏览器不整页白屏刷新
- [ ] 能指出 `main.js` 在哪里把 Router 安装进 Vue App

---

## TODO 2：用 RouterLink 做导航

不要写：

```html
<a href="/login">Login</a>
```

尝试：

```vue
<RouterLink :to="{ name: 'user-account-login-index' }">
  登录
</RouterLink>
```

### 思考

为什么 SPA 更倾向 RouterLink？

你的回答至少应该包含：

- 客户端路由
- 不必重新下载整个页面
- Router 可以管理 route meta / params / query

---

## TODO 3：第一次使用 `ref()`

在登录页写两个响应式变量：

```js
const username = ref('')
const password = ref('')
```

用 `v-model` 绑定两个 input。

在页面下方临时显示：

```text
当前用户名：xxx
```

不要显示密码内容。

### 验收

修改 input 时，页面上的用户名实时变化。

你必须能解释：

> `ref` 不是“读取 DOM input”，而是让数据成为 Vue 的响应式状态。

---

## TODO 4：拆一个子组件

把登录按钮拆成自己的组件，例如：

```text
components/LoginButton.vue
```

父组件传入：

```text
loading
```

子组件点击后向父组件发出：

```text
submit
```

要求至少使用一次：

```js
defineProps()
defineEmits()
```

---

## TODO 5：理解 route param 与 query

分别建立两个实验 URL：

```text
/user/space/123
/?q=Alice
```

读取：

```js
const route = useRoute()
```

显示：

- `route.params.user_id`
- `route.query.q`

### 思考

什么时候适合 param？什么时候适合 query？

一个合理答案：

- `user/123`：资源身份，是路径的一部分
- `?q=Alice`：筛选条件，可以为空或变化

---

## 参考答案思路

建立这个心智模型：

```text
main.js
  ↓ createApp
App.vue
  ↓ RouterView
router/index.js
  ↓ 根据 URL 选择 View
views/*.vue
  ↓ 组合
components/*.vue
  ↓ props / emits
响应式状态 ref()
```

不要把 Router 理解成“切换 HTML 文件”。它是在同一个 Vue 应用里决定当前渲染哪个组件树。

---

## 常见错误

### 页面 URL 对但内容没变

检查 `RouterView` 是否存在、route 是否真的注册。

### `ref is not defined`

你忘了：

```js
import { ref } from 'vue'
```

### props 改不动

Props 默认是父组件拥有的数据。子组件应该通过 emit 请求父组件改变，而不是把父数据当本地变量随便修改。

---

## Challenge

实现一个“未登录导航栏”和“已登录导航栏”的假状态切换：

```text
未登录：登录 / 注册
已登录：主页 / 好友 / 创建 / 退出
```

这一章不要用 Pinia。先用父组件 `ref(false)` 完成，下一章认证实验再体会为什么全局用户状态需要 Store。
