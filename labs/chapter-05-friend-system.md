# Chapter 05 Lab：首页、搜索、无限加载与 Friend 关系

## 本章目标

把 Character 从“我自己管理的数据”变成“用户可以发现并建立关系的内容”。

最终完成：

```text
首页角色流
  + 搜索
  + 无限加载
  + 添加 AI 好友
  + 好友列表
  + 删除好友
```

---

## 历史检查点

```text
f96da725bbfd77aa9766f70786a6061f35f8dcb9  首页前后端
c9ea5e0f3b1a276c3fe6d0b10fa648db3f5510ca  搜索
102b31a0f60be51bbc6f22f690ec74d3ee0a5be3  好友页面后端
1c9d9e000c77c4e1779e0681ae5fca7e8123dc67  好友列表前端
```

---

## TODO 1：先画数据关系

```text
UserProfile ──< Friend >── Character
```

`Friend` 的含义不是“另一个真实用户”。

它表达：

> 当前用户与某个 AI Character 建立了一条持续聊天关系。

至少包含：

```text
me
character
memory
create_time
update_time
```

### 验收

你能解释为什么长期记忆应该放 Friend，而不是直接放 Character。

答案：同一个 Character 面对不同用户，应该拥有不同记忆。

---

## TODO 2：首页分页

实现：

```text
GET /api/homepage/index/?items_count=0
```

第一次返回 20 个，下一次：

```text
items_count=20
```

### 思考

项目这里使用的是 offset 风格：

```python
queryset[items_count: items_count + 20]
```

它简单易懂，但数据量很大时可能有性能和数据漂移问题。先掌握，再考虑 cursor pagination。

---

## TODO 3：IntersectionObserver 无限加载

前端放一个 sentinel：

```html
<div ref="sentinel-ref"></div>
```

当 sentinel 进入可视区域时加载下一页。

### 验收

- [ ] 首屏内容不足一屏时会继续加载
- [ ] 滚到底部加载下一批
- [ ] 没有数据后停止请求
- [ ] `isLoading` 能防止重复并发请求

### 主动错误实验

去掉 `isLoading` 判断，快速滚动。

观察 Network 是否产生重复请求，再恢复保护。

---

## TODO 4：搜索

使用：

```text
/?q=Alice
```

前端把 query 转成后端：

```text
search_query=Alice
```

后端使用：

```python
Q(name__icontains=search_query) |
Q(profile__icontains=search_query)
```

### 验收

修改 URL query 后：

1. 清空旧列表
2. 重置分页状态
3. 从第 0 条重新搜索

不能把新搜索结果追加到旧搜索结果后面。

---

## TODO 5：Get or Create Friend

实现：

```text
POST /api/friend/get_or_create/
```

请求：

```json
{
  "character_id": 123
}
```

逻辑：

```text
当前用户 + character_id 已经有 Friend？
├── 是 → 返回已有 Friend
└── 否 → 创建后返回
```

### 验收

连续点击同一个角色 5 次，数据库不应该创建 5 条完全重复的 Friend。

---

## TODO 6：好友列表

实现：

```text
GET /api/friend/get_list/?items_count=0
```

按：

```text
-update_time
```

排序。

思考：为什么聊天以后把 `update_time` 更新，可以让最近聊天的人排前面？

---

## TODO 7：删除好友

实现：

```text
POST /api/friend/remove/
```

后端必须带当前用户约束：

```python
Friend.objects.filter(
    id=friend_id,
    me__user=request.user,
)
```

### 验收

用户不能通过伪造 friend_id 删除别人的好友关系。

---

## 参考答案思路

这一章把三个不同概念串起来：

```text
发现内容：首页 Character
        ↓
过滤内容：Search Query
        ↓
建立私有关系：Friend
        ↓
以后聊天/记忆都围绕 Friend
```

Character 是“角色模板/身份”；Friend 是“某个用户与这个角色的会话关系”。

---

## 常见错误

### 搜索后列表重复

route query 变化时没有 reset 分页状态。

### 无限加载一直请求

没有 `hasMore/hasCharacters`，或 sentinel 一直可见但接口已经返回空数组。

### 好友重复

只做了 create，没有在 `(user, character)` 维度先查询。

### 删了前端卡片但数据库还在

UI 删除与后端删除是两件事。先确认 Network API 成功，再更新本地数组。

---

## Challenge

设计一个数据库级唯一约束，使 `(me, character)` 无法出现重复 Friend。

提示：研究 Django `UniqueConstraint`。

先回答：即使应用代码已经 `get_or_create`，为什么数据库约束仍然有价值？
