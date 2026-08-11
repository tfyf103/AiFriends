# Chapter 04 Lab：Character CRUD、文件上传与 Voice

## 本章目标

第一次完成一个真正完整的业务模块：

```text
Create
Read
Update
Delete
```

对象是 AI Character。

除了普通文本字段，这一章还包含：

- 图片文件上传
- Django `ImageField`
- `multipart/form-data`
- 外键 Voice
- 当前用户只能修改自己的角色

---

## 历史检查点

```text
2081304f049a58a404b39bfe09f9c373b80d24df  角色 CRUD 后端
84f1c92eba32c62ef2e5724a77eeb7c64979de6b  创建角色前端
95cf0456ef46696bca36c602928fbbb6dbe658d5  更新角色前端
88343a97f0d74570e10bfe3952c0192669876a61  自由选择音色
```

---

## TODO 1：设计 Character Model

先画字段，不要马上写代码：

```text
Character
├── author
├── name
├── photo
├── background_image
├── profile
├── voice
├── create_time
└── update_time
```

思考每个字段的数据类型。

### 验收

能解释：

- `author` 为什么是 ForeignKey
- `voice` 为什么不是简单把音色名称直接写进 Character
- 图片为什么使用 `ImageField`

---

## TODO 2：创建角色 API

实现：

```text
POST /api/create/character/create/
```

使用 `FormData`，至少传：

```text
name
profile
voice_id
photo
background_image
```

### 前端要求

```js
const formData = new FormData()
formData.append('name', name)
formData.append('photo', file)
```

不要手工把图片转成一个巨大 JSON 数组。

### 后端要求

分别理解：

```python
request.data
request.FILES
```

---

## TODO 3：权限约束

创建角色时 `author` 必须来自：

```python
request.user
```

而不是相信浏览器上传：

```json
{"author_id": 123}
```

### 安全实验

尝试在浏览器请求中伪造别人的 user id。

你的后端应该完全忽略这个值。

原则：

> 身份信息来自认证系统，不来自用户自己声明。

---

## TODO 4：查询单个角色

实现：

```text
GET /api/create/character/get_single/?character_id=...
```

如果这是“编辑自己的角色”的 API，需要限定：

```python
Character.objects.get(
    id=character_id,
    author__user=request.user,
)
```

### 验收

用户 A 不应该通过修改 `character_id` 编辑用户 B 的角色。

---

## TODO 5：Update

更新时：

- name/profile 必须更新
- photo/background_image 可选更新
- 没上传新图片时保留旧文件
- 有新图片时考虑删除旧文件
- `update_time` 变化
- voice 可以改变

### 思考

为什么更新 API 不能简单 `Character.objects.filter(id=id).update(...)` 后就结束？

因为这里还涉及：

- 权限
- 文件生命周期
- 数据校验
- ForeignKey

---

## TODO 6：Delete

实现删除角色。

必须至少保证：

```python
Character.objects.filter(
    id=character_id,
    author__user=request.user,
)
```

### 主动攻击实验

1. 登录账号 A，创建角色
2. 登录账号 B
3. 从 DevTools 手动 POST A 的 character_id
4. 验证删除失败/无权限

不要只依赖前端“隐藏删除按钮”。

---

## TODO 7：Voice

在 Admin 创建至少两个：

```text
Voice(name='音色 A', voice_id='...')
Voice(name='音色 B', voice_id='...')
```

实现：

```text
GET /api/create/character/voice/get_list/
```

然后让创建/编辑页面显示 select。

### 验收

不同 Character 保存不同 Voice ForeignKey。

---

## 参考答案思路

完整链路：

```text
Vue Form
  ↓ FormData
Axios
  ↓ multipart/form-data
Django APIView
  ├─ request.data
  └─ request.FILES
  ↓
Character Model
  ├─ SQLite 保存字段/文件路径
  └─ media/ 保存图片文件
```

数据库里通常不是保存整张图片二进制，而是保存 Django Field 对应的文件路径信息，文件放在媒体目录。

---

## 常见错误

### 图片请求 404

检查：

```text
MEDIA_ROOT
MEDIA_URL
DEBUG 开发路由
```

### `NOT NULL constraint failed`

必填字段没传，或 migration/Model 约束与你理解的不一致。

### FormData 后端读不到文件

确认前端真的 append 了 `File/Blob`，字段名与 `request.FILES.get()` 完全一致。

### 删除按钮隐藏了就以为安全

前端权限只是 UX；真正权限必须由后端查询条件保证。

---

## Challenge

增加一个“复制角色”功能：

```text
POST /api/create/character/clone/
```

规则：

- 可以复制公开角色的人格文本
- 新角色 author 必须是当前登录用户
- 不能直接复用对方私有文件路径而不思考文件所有权

先写设计方案，不必马上加入正式项目。
