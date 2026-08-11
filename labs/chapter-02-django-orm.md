# Chapter 02 Lab：Django、Model、Migration 与 SQLite

## 本章目标

第一次真正建立后端心智模型：

```text
URL → View → Model → SQLite
```

你要创建一个最小 `UserProfile`，在 Admin 中看到它，并通过一个 GET API 返回数据。

---

## 历史检查点

```text
3ab2bd28ca6551e188084e7502de82a06df96b0a  实现完数据库
248a7d8ea7c24e32d6f6a5d3631e277e7a09bb87  实现后端
```

观察：

```bash
git show --stat 3ab2bd28ca6551e188084e7502de82a06df96b0a
git show 3ab2bd28ca6551e188084e7502de82a06df96b0a -- backend/web/models/user.py
```

---

## TODO 1：理解 Django Project 与 App

找出：

```text
backend/manage.py
backend/backend/settings.py
backend/backend/urls.py
backend/web/apps.py
backend/web/urls.py
```

给每个文件写一句自己的解释。

### 验收

你应该能回答：

> `backend/backend` 是 Django project 配置；`backend/web` 是实际承载业务代码的 app。

---

## TODO 2：创建一个最小 Model

先不要复制最终模型，自己写：

```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.TextField(default='')
```

然后：

```bash
python manage.py makemigrations
python manage.py migrate
```

### 必须观察

执行前后：

```bash
python manage.py showmigrations
```

打开生成的 migration 文件，看看它如何描述数据库变更。

---

## TODO 3：进入 Django Shell

```bash
python manage.py shell
```

手动创建/查询数据。

练习：

```python
from django.contrib.auth.models import User
from web.models.user import UserProfile

u = User.objects.create_user(username='lab_user', password='123456')
p = UserProfile.objects.create(user=u, profile='hello django')

UserProfile.objects.all()
UserProfile.objects.get(user__username='lab_user')
```

### 验收

- [ ] 能解释 `objects` 是 Django ORM Manager
- [ ] 能解释 `user__username` 为什么有双下划线
- [ ] 知道 `get()` 和 `filter()` 的区别

---

## TODO 4：注册 Admin

创建管理员：

```bash
python manage.py createsuperuser
```

把 `UserProfile` 注册到 `admin.py`。

访问：

```text
http://127.0.0.1:8000/admin/
```

### 验收

你可以不写前端页面，就在 Admin 中创建、修改和观察数据。

思考：为什么项目里的 `SystemPrompt` 和 `Voice` 很适合由 Admin 管理？

---

## TODO 5：写第一个 DRF API

自己添加：

```text
GET /api/lab/profile/
```

返回：

```json
{
  "result": "success",
  "profiles": [
    {
      "username": "lab_user",
      "profile": "hello django"
    }
  ]
}
```

要求：

1. 在 `web/urls.py` 注册 URL
2. 写一个 `APIView`
3. 使用 ORM 查询
4. 使用 `Response` 返回 JSON

---

## TODO 6：主动制造三个错误

依次制造：

1. URL 路径拼错 → 404
2. View 中访问不存在字段 → 500
3. 查询一个不存在对象并用 `.get()` → 异常

每次都记录：

```text
浏览器状态码：
Django 终端错误：
真正出错文件：
真正出错行：
```

这是整个后端课程最重要的调试习惯之一。

---

## 参考答案思路

请求进 Django 的路线：

```text
浏览器请求
    ↓
backend/urls.py
    ↓ include('web.urls')
web/urls.py
    ↓ URL pattern
APIView.get()/post()
    ↓ ORM
Model.objects...
    ↓
SQLite
    ↓
Response(JSON)
```

Model 不是数据库本身。Model 是 Python 对数据库表结构和查询行为的抽象。

---

## 常见错误

### `no such table`

通常是 migration 没执行。

### `You are trying to add a non-nullable field`

你改了已有表的字段约束，需要考虑旧数据如何获得默认值。

### `DisallowedHost`

查看 `ALLOWED_HOSTS`，不要为了省事在生产环境长期设置成 `*`。

### 修改 Model 后页面没变化

Model 改动不是热更新数据库结构。需要 `makemigrations` + `migrate`。

---

## Challenge

给实验 API 增加：

```text
GET /api/lab/profile/?username=lab
```

要求使用：

```python
username__icontains
```

并解释 ORM 查询最终在数据库层面解决了什么问题。
