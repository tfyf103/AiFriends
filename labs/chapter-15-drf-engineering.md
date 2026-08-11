# Chapter 15 Lab：DRF 工程化、Serializer 与 HTTP Status

## 本章目标

从“APIView 里手工取字段”进入更稳定的 API 设计。

当前项目已经开始修正一部分问题：注册使用 201，重复用户名使用 409，错误密码使用 401，空输入使用 400。

---

## TODO 1：先审计旧式写法

搜索：

```text
request.data.get(...).strip()
except:
Response({'result': ...})
```

记录至少 5 个 API。

思考：

```text
字段不存在会怎样？
类型不对会怎样？
为什么裸 except 会让 traceback 消失？
为什么所有情况都 HTTP 200 会让前端难判断？
```

---

## TODO 2：给 Profile Update 写 Serializer

目标：

```python
class UpdateProfileSerializer(serializers.Serializer):
    username = serializers.CharField(...)
    profile = serializers.CharField(...)
    photo = serializers.ImageField(required=False)
```

把：

```text
字段读取
空值检查
长度检查
```

移到 Serializer。

View 只保留业务逻辑：

```text
validate
check ownership
save
return response
```

---

## TODO 3：设计统一错误格式

建议学习版先统一成：

```json
{
  "result": "error",
  "code": "USERNAME_EXISTS",
  "message": "用户名已存在",
  "fields": {
    "username": ["用户名已存在"]
  }
}
```

不要把给用户看的中文字符串当唯一机器协议。

---

## TODO 4：正确使用 Status Code

至少覆盖：

```text
200 OK
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
500 Internal Server Error
503 Service Unavailable
```

要求你能解释：

> “角色不存在”和“角色存在但不属于当前用户”为什么可以有不同安全取舍？

---

## TODO 5：把一个 API 改成 GenericAPIView / ViewSet

任选 Character CRUD。

比较：

```text
APIView
GenericAPIView
ModelViewSet
```

不要因为“代码少”就机械选择 ViewSet，要说明：

- CRUD 是否标准；
- 是否有文件上传；
- 是否有额外业务动作；
- 权限是否复杂。

---

## TODO 6：测试 Validation

新增测试：

```text
缺 username
username 只有空格
profile 超长
非法图片
未登录
修改别人的 Character
```

---

## 验收

- [ ] 至少写一个 Serializer；
- [ ] 至少删掉一个裸 `except:`；
- [ ] 至少一个 API 使用合理非 200 状态码；
- [ ] 前端能正确显示 400/409 的业务信息；
- [ ] 有自动测试保护重构。

---

## Challenge

给所有 API 设计一个错误码表：

```text
AUTH_INVALID_CREDENTIALS
AUTH_REFRESH_EXPIRED
CHARACTER_NOT_FOUND
FRIEND_NOT_FOUND
AI_PROVIDER_UNAVAILABLE
RAG_NOT_READY
ASR_DISABLED
```

然后在 `docs/API_REFERENCE.md` 中补充。
