# Chapter 02 Lab: Django, Models, Migrations, and SQLite

🌐 **Language:** [中文](../chapter-02-django-orm.md) | **English**

## Goal

Build your first backend mental model:

```text
URL → View → Model → SQLite
```

You will create a minimal `UserProfile`, inspect it in Django Admin, and return it through a small DRF API.

---

## Historical checkpoints

```text
3ab2bd28ca6551e188084e7502de82a06df96b0a  database implemented
248a7d8ea7c24e32d6f6a5d3631e277e7a09bb87  backend implemented
```

Useful archaeology:

```bash
git show --stat 3ab2bd28ca6551e188084e7502de82a06df96b0a
git show 3ab2bd28ca6551e188084e7502de82a06df96b0a -- backend/web/models/user.py
```

Historical commits are learning evidence, not guaranteed canonical solutions. Compare them with current tests and models.

---

## TODO 1: Django Project vs Django App

Locate:

```text
backend/manage.py
backend/backend/settings.py
backend/backend/urls.py
backend/web/apps.py
backend/web/urls.py
```

Write one sentence describing the role of each.

### Acceptance

You can explain:

> `backend/backend` contains Django project configuration, while `backend/web` is the application that contains most AiFriends business code.

---

## TODO 2: Create a minimal model

Do not copy the final model immediately. Start with:

```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.TextField(default='')
```

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Observe the migration system

Before and after:

```bash
python manage.py showmigrations
```

Open the generated migration file and identify how Django represents a schema change as Python operations.

### Acceptance

You understand:

```text
Model change
  ↓
makemigrations
  ↓
Migration file
  ↓
migrate
  ↓
Database schema change
```

---

## TODO 3: Use the Django shell

```bash
python manage.py shell
```

Experiment:

```python
from django.contrib.auth.models import User
from web.models.user import UserProfile

u = User.objects.create_user(username='lab_user', password='123456')
p = UserProfile.objects.create(user=u, profile='hello django')

UserProfile.objects.all()
UserProfile.objects.get(user__username='lab_user')
```

### Acceptance

- [ ] You can explain what `objects` is.
- [ ] You can explain the double underscore in `user__username`.
- [ ] You know when `get()` differs from `filter()`.
- [ ] You know that a failed `get()` raises an exception instead of returning an empty queryset.

---

## TODO 4: Register the model in Django Admin

Create an admin user:

```bash
python manage.py createsuperuser
```

Register `UserProfile` in `admin.py`, then visit:

```text
http://127.0.0.1:8000/admin/
```

### Acceptance

You can create and inspect data without building a Vue page.

### Think

Why are configuration-like models such as `SystemPrompt` and `Voice` useful to manage through Admin during development and teaching?

---

## TODO 5: Write your first DRF endpoint

Add:

```text
GET /api/lab/profile/
```

Return something like:

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

Requirements:

1. register a route in `web/urls.py`;
2. write an `APIView`;
3. query through Django ORM;
4. return a DRF `Response`.

---

## TODO 6: Deliberately create three backend failures

Create, one at a time:

1. a wrong URL → 404;
2. access to a nonexistent model field → 500;
3. `.get()` for an object that does not exist → exception.

For each one, record:

```text
Browser status code:
Django terminal error:
Actual file:
Actual line:
Root cause:
```

This is more valuable than memorizing exception names.

---

## Reference request flow

```text
Browser request
    ↓
backend/backend/urls.py
    ↓ include('web.urls')
backend/web/urls.py
    ↓ URL pattern
APIView.get()/post()
    ↓ ORM
Model.objects...
    ↓
SQLite
    ↓
Response(JSON)
```

A Django Model is **not** the database. It is a Python abstraction over schema and query behavior.

---

## Common errors

### `no such table`

Usually migrations were not applied:

```bash
python manage.py migrate
```

### `You are trying to add a non-nullable field`

You changed a table that already contains rows. Decide how existing rows receive a value before enforcing the new constraint.

### `DisallowedHost`

Inspect `ALLOWED_HOSTS`. Do not treat `*` as a permanent production solution.

### Model changed but the database did not

Model edits are not database hot reloads. Run:

```text
makemigrations → migrate
```

---

## Challenge

Extend the lab API:

```text
GET /api/lab/profile/?username=lab
```

Use:

```python
username__icontains
```

Then explain what work the ORM ultimately asks the database to perform and why filtering in SQL/database space is preferable to loading every row into Python first.
