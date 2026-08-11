# Chapter 04 Lab: Character CRUD, File Uploads, and Voice

🌐 **Language:** [中文](../chapter-04-character-crud.md) | **English**

## Goal

Build your first complete business module:

```text
Create
Read
Update
Delete
```

The resource is an AI `Character`.

This chapter also introduces:

- image uploads;
- Django `ImageField`;
- `multipart/form-data`;
- the `Voice` foreign key;
- object-level authorization: users may only modify their own Characters.

---

## Historical checkpoints

```text
2081304f049a58a404b39bfe09f9c373b80d24df  Character CRUD backend
84f1c92eba32c62ef2e5724a77eeb7c64979de6b  create Character frontend
95cf0456ef46696bca36c602928fbbb6dbe658d5  update Character frontend
88343a97f0d74570e10bfe3952c0192669876a61  selectable voices
```

Treat them as project history. Current `main` includes later engineering improvements and may differ from these snapshots.

---

## TODO 1: Design the model before writing it

Sketch:

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

Decide the Django field type for each.

### Acceptance

Explain:

- why `author` is a relation instead of a plain username string;
- why `voice` is a foreign key rather than copying a display name into every Character;
- why images are modeled with `ImageField`/media storage instead of a giant JSON array.

---

## TODO 2: Create Character API

Endpoint:

```text
POST /api/create/character/create/
```

Use `FormData` with fields such as:

```text
name
profile
voice_id
photo
background_image
```

Frontend example:

```js
const formData = new FormData()
formData.append('name', name)
formData.append('photo', file)
```

Backend: understand the difference between:

```python
request.data
request.FILES
```

### Acceptance

Network shows a multipart request and Django receives actual file objects for the image fields.

---

## TODO 3: Never trust `author_id` from the browser

When creating a Character, derive ownership from:

```python
request.user
```

then resolve the current user's `UserProfile`.

Do **not** trust input like:

```json
{
  "author_id": 123
}
```

### Security experiment

Add a fake `author_id` for another user to the request.

The server should ignore it and create the Character for the authenticated user only.

Principle:

> Identity comes from authentication, not from a client assertion.

---

## TODO 4: Read a single Character for editing

Endpoint:

```text
GET /api/create/character/get_single/?character_id=...
```

For an owner-only edit endpoint, constrain the query by both object ID and current user, conceptually:

```python
Character.objects.get(
    id=character_id,
    author__user=request.user,
)
```

### Acceptance

User A cannot change `character_id` in DevTools and retrieve/edit User B's private edit resource.

### Security discussion

Decide whether an unauthorized object should return:

```text
403 Forbidden
```

or be hidden behind:

```text
404 Not Found
```

Both can be defensible depending on information-disclosure goals. Be consistent.

---

## TODO 5: Update Character

Handle:

- required text fields;
- optional image replacement;
- preserving old files when no new file is uploaded;
- the lifecycle of old files when a new file replaces them;
- changing `voice`;
- updating timestamps;
- validating ownership again on the server.

### Why `.filter(id=id).update(...)` is not enough

This operation also involves:

```text
ownership
validation
file lifecycle
foreign-key resolution
error semantics
```

The shortest code is not always the safest or clearest API.

---

## TODO 6: Delete Character

A delete query must include the current owner constraint, for example:

```python
Character.objects.filter(
    id=character_id,
    author__user=request.user,
)
```

### Deliberate attack experiment

1. Login as account A and create a Character.
2. Login as account B.
3. Manually send A's `character_id` from DevTools/Postman.
4. Verify B cannot delete it.

Do not confuse “the UI hides the delete button” with authorization.

---

## TODO 7: Voice relation

Create at least two Voice rows in Admin:

```text
Voice(name='Voice A', voice_id='...')
Voice(name='Voice B', voice_id='...')
```

Expose/select them through:

```text
GET /api/create/character/voice/get_list/
```

### Acceptance

Two Characters can persist different `Voice` foreign keys.

Understand the two ID layers:

```text
Voice.id       → AiFriends database primary key
Voice.voice_id → provider-specific TTS voice identifier
```

---

## TODO 8: Understand the current text-only fallback

In current AiFriends, TTS is optional. A Character without a usable voice should not make real text chat impossible when TTS is disabled/unavailable.

Reason about the desired product behavior:

```text
text chat capability
  ≠
TTS capability
```

This is a useful example of feature decoupling.

---

## Reference data flow

```text
Vue Form
  ↓ FormData
HTTP multipart
  ↓
Django APIView
  ├─ request.data
  └─ request.FILES
  ↓
UserProfile + Voice resolution
  ↓
Character Model
  ├─ SQLite stores relational/file-path metadata
  └─ media/ stores image files
```

---

## Common errors

### Uploaded image returns 404

Check:

```text
MEDIA_ROOT
MEDIA_URL
Vite /media proxy in development
Django DEBUG media serving
actual file path
```

### `NOT NULL constraint failed`

A required field is missing, or your database migration/schema does not match the code you think you are running.

### `request.FILES` is empty

Make sure the browser appended a real `File`/`Blob`, the field name matches exactly, and the request is multipart.

### Delete looks successful in the UI but data remains

Updating a local array and deleting from the backend are separate operations. Confirm the Network response and database state.

### File upload is accepted, but should it be?

The learning project still treats stronger MIME/size/content validation as security work. Chapter 18 asks you to harden this boundary.

---

## Challenge

Design:

```text
POST /api/create/character/clone/
```

Rules:

- a public Character's persona text may be copied;
- the new `author` must be the authenticated user;
- do not blindly reuse another owner's private media path;
- decide whether Voice can be copied by relation;
- write down authorization and file-ownership rules before coding.

The challenge is the design argument, not just making the endpoint return 200.
