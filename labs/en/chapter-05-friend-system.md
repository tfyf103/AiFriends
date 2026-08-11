# Chapter 05 Lab: Homepage, Search, Infinite Loading, and Friend Relationships

🌐 **Language:** [中文](../chapter-05-friend-system.md) | **English**

## Goal

Turn `Character` from “data I manage” into content that users can discover and form persistent relationships with.

You will build:

```text
homepage Character feed
  + search
  + infinite loading
  + add AI Friend
  + Friend list
  + remove Friend
```

---

## Historical checkpoints

```text
f96da725bbfd77aa9766f70786a6061f35f8dcb9  homepage frontend/backend
c9ea5e0f3b1a276c3fe6d0b10fa648db3f5510ca  search
102b31a0f60be51bbc6f22f690ec74d3ee0a5be3  Friend backend
1c9d9e000c77c4e1779e0681ae5fca7e8123dc67  Friend list frontend
```

Use them to understand how the product evolved. Current `main` additionally has a database-level Friend uniqueness constraint.

---

## TODO 1: Draw the relationship first

```text
UserProfile ──< Friend >── Character
```

A `Friend` does not mean another human account. It represents:

> a persistent relationship between one user and one AI Character.

Core fields:

```text
me
character
memory
create_time
update_time
```

### Acceptance

Explain why long-term memory belongs to `Friend`, not directly to `Character`:

```text
User A ↔ Character X → memory A
User B ↔ Character X → memory B
```

The Character identity may be shared; the relationship memory is user-specific.

---

## TODO 2: Homepage pagination

Endpoint:

```text
GET /api/homepage/index/?items_count=0
```

The learning implementation uses an offset-like slice:

```python
queryset[items_count: items_count + 20]
```

### Acceptance

- [ ] first request returns the initial batch;
- [ ] later requests advance `items_count`;
- [ ] empty result stops further loading;
- [ ] you can explain why very large datasets may eventually prefer cursor pagination.

---

## TODO 3: Infinite loading with `IntersectionObserver`

Render a sentinel near the end of the list:

```html
<div ref="sentinelRef"></div>
```

When it enters the viewport, request the next page.

### Acceptance

- [ ] a short first page can trigger another load;
- [ ] scrolling to the end loads more;
- [ ] no more requests after the server returns no items;
- [ ] `isLoading` prevents duplicate concurrent fetches.

### Deliberate failure

Remove the `isLoading` guard and scroll aggressively.

Inspect Network for duplicate requests, then restore the guard.

---

## TODO 4: Search

Browser route:

```text
/?q=Alice
```

Frontend maps the query to backend search input:

```text
search_query=Alice
```

Backend concept:

```python
Q(name__icontains=search_query) |
Q(profile__icontains=search_query)
```

### Acceptance

When the search term changes:

1. clear the old list;
2. reset pagination;
3. request from offset 0;
4. never append the new search results to the previous query's list.

---

## TODO 5: Get or create a Friend

Endpoint:

```text
POST /api/friend/get_or_create/
```

Request:

```json
{
  "character_id": 123
}
```

Desired behavior:

```text
Does current user already have a Friend for Character 123?
├─ yes → return existing Friend
└─ no  → create and return one
```

The maintained implementation uses Django `get_or_create()` **and** the database model now enforces:

```text
(me, character) is unique
```

with `UniqueConstraint`.

### Acceptance

Click the same Character five times. The database still contains exactly one Friend row for that `(me, character)` pair.

---

## TODO 6: Understand why app checks and DB constraints both matter

Compare:

```text
filter + create
get_or_create
UniqueConstraint
transaction handling
```

A database uniqueness constraint is the final invariant under concurrency.

Without it, two concurrent requests can both observe “no row yet” before either creates one.

---

## TODO 7: Friend list

Endpoint:

```text
GET /api/friend/get_list/?items_count=0
```

Sort recent relationships by:

```text
-update_time
```

### Think

Why does updating a Friend's `update_time` after activity allow recent conversations to move toward the top?

Also distinguish this product choice from the exact semantics of “last message time” if those ever diverge.

---

## TODO 8: Remove Friend

Endpoint:

```text
POST /api/friend/remove/
```

The server must constrain the operation by the authenticated user, conceptually:

```python
Friend.objects.filter(
    id=friend_id,
    me__user=request.user,
)
```

### Security acceptance

A user cannot delete someone else's relationship by changing `friend_id` in DevTools.

---

## Reference mental model

```text
Discover content: Character feed
          ↓
Filter content: search
          ↓
Create private relation: Friend
          ↓
Chat history + long-term memory are scoped to Friend
```

```text
Character = reusable AI identity/template
Friend    = one user's ongoing relationship with that Character
```

---

## Common errors

### Search results duplicate or mix with old results

You changed the query but did not reset the list and pagination state.

### Infinite loading never stops

Check `hasMore`/empty-result handling and whether the sentinel remains visible after the backend returns no items.

### Duplicate Friends appear

If you are rebuilding the lab, make sure both application logic and the database uniqueness invariant exist.

### UI card disappears but database row remains

Frontend state mutation is not backend persistence. Confirm the remove request succeeded before treating the operation as complete.

### `IntegrityError` on duplicate Friend

That can be the database doing its job. Decide how the API should convert a race/constraint conflict into a clean response instead of a raw 500.

---

## Challenge

Write a concurrency-oriented test for the invariant:

```text
one UserProfile + one Character → at most one Friend
```

Then explain:

> Why is a database constraint still valuable even when `get_or_create()` is already used in the view?

Your answer should mention race conditions and the database as the final source of truth for relational integrity.
