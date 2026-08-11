# Chapter 03 Lab：注册、登录、JWT、Pinia 与 Axios

## 本章目标

把“页面上的登录表单”升级成真正的身份系统。

最终链路：

```text
Vue 登录表单
  ↓ POST username/password
Django authenticate()
  ↓
access token → 返回给 JS
refresh token → HttpOnly Cookie
  ↓
Pinia 保存 access token
  ↓
Axios 每次自动 Authorization: Bearer ...
  ↓
access 过期 → refresh → 重发原请求
```

---

## 历史检查点

```text
248a7d8ea7c24e32d6f6a5d3631e277e7a09bb87  实现后端认证接口
b0aa1d5c169d836023fd3788152d5cb1eb4bf55b  刷新页面拉取用户信息
a27cbf8f90cf256ab075173f19d468319b302f67  前端对接注册登录退出
```

---

## TODO 1：只做注册 API

实现：

```text
POST /api/user/account/register/
```

请求：

```json
{
  "username": "alice",
  "password": "123456"
}
```

要求：

- 用户名不能为空
- 密码不能为空
- 用户名不能重复
- 使用 `User.objects.create_user()`，不要自己明文存密码
- 同时创建 `UserProfile`

### 验收

- [ ] 注册成功后数据库中存在 User
- [ ] 存储的 password 不是 `123456` 明文
- [ ] 重复用户名得到可理解的业务错误

---

## TODO 2：实现登录

使用：

```python
user = authenticate(username=username, password=password)
```

成功后：

```python
refresh = RefreshToken.for_user(user)
```

返回 access token，并把 refresh token 写入 HttpOnly Cookie。

### 必须理解

为什么不把两个 token 都塞进 localStorage？

这不是绝对唯一方案，但本项目的设计意图是：

- access：JS 需要读取，用来写 Authorization Header
- refresh：尽量不让普通 JS 直接读取，由 Cookie 带给刷新接口

---

## TODO 3：用浏览器 DevTools 观察 Token

登录后打开：

```text
DevTools → Network → login request
```

观察：

- Request Payload
- Response JSON
- Response Cookie

再打开下一条受保护请求，观察：

```http
Authorization: Bearer <access-token>
```

### 验收

你能指出 access token 在“请求头”哪个位置，refresh token 在浏览器哪个位置。

---

## TODO 4：用 Pinia 管登录状态

Store 至少保存：

```text
id
username
photo
profile
accessToken
```

实现：

```text
isLogin()
setAccessToken()
setUserInfo()
logout()
```

### 思考

为什么不能把用户状态分别复制进 NavBar、Friend 页面、Profile 页面？

答案应该涉及：

- 单一数据源
- 多组件共享
- 状态更新一致性

---

## TODO 5：Axios Request Interceptor

创建统一 `api` 实例。

要求每个普通 API 请求自动附带：

```http
Authorization: Bearer <token>
```

不要在每个页面里重复：

```js
headers: { Authorization: ... }
```

### 验收

新写一个组件时，只需要：

```js
api.get('/some/protected/api/')
```

就能自动携带 token。

---

## TODO 6：实现 refresh

模拟 access token 失效。

你需要实现：

```text
请求 A → 401
       ↓
POST refresh_token
       ↓
拿到新 access
       ↓
重新执行请求 A
```

然后思考一个更难的问题：

> 如果此时 A、B、C 三个请求同时 401，是不是应该同时发三个 refresh 请求？

观察项目 `frontend/src/js/http/api.js` 中：

```text
isRefreshing
refreshSubscribers
```

尝试自己解释为什么要“排队等待同一次刷新”。

---

## TODO 7：Router Guard

给需要登录的页面添加：

```js
meta: {
  needLogin: true,
}
```

未登录访问时跳到 login。

### 验收

- [ ] 未登录不能进入 `/friend`
- [ ] 登录后可以进入
- [ ] 刷新浏览器时不会因为用户信息还没拉取完成就错误跳转

---

## 参考答案思路

身份系统不要想成“登录页面”。真正结构是：

```text
Credentials
  ↓
Django Auth
  ↓
JWT issuance
  ↓
Token storage
  ↓
Request interceptor
  ↓
DRF authentication
  ↓
request.user
```

后端业务代码通常不需要重新解析用户名密码，而是依赖：

```python
request.user
```

---

## 常见错误

### 登录成功但受保护 API 401

先在 Network 看 Authorization Header 是否存在，不要先改 Django。

### Cookie 没出现

检查：

- `withCredentials`
- SameSite
- Secure
- HTTP/HTTPS 环境
- 域名是否一致

### 无限刷新 Token

检查 refresh 请求本身是否也被错误地当成普通 401 请求反复拦截。

### 刷新网页后 Pinia 丢状态

Pinia 内存会重置。项目采用“用 refresh cookie 重新获得 access，再拉用户信息”的思路恢复登录状态。

---

## Challenge

在 DevTools 中人为修改 access token 为错误字符串，再访问受保护页面。

要求你能画出实际发生的网络请求顺序：

```text
原请求 → 401 → refresh → 原请求重试
```

并说明每一步使用的是 access 还是 refresh。
