# Chapter 15 Lab: DRF Engineering, Serializers, and HTTP Status Codes

🌐 **Language:** [中文](../chapter-15-drf-engineering.md) | **English**

## Goal

Move from “manually pull fields out of `request.data` inside every `APIView`” toward APIs with explicit validation contracts and meaningful HTTP semantics.

Current AiFriends already demonstrates part of this migration in authentication:

```text
201 Created      registration success
400 Bad Request  invalid input
401 Unauthorized invalid credentials
409 Conflict     duplicate username
```

The rest of the codebase still contains older patterns that make good refactoring exercises.

---

## TODO 1: Audit legacy validation patterns

Search for patterns such as:

```text
request.data.get(...).strip()
except:
Response({'result': ...})
```

Record at least five endpoints and answer:

```text
What happens if the field is missing?
What happens if the type is wrong?
Can a bare except hide the real traceback?
Does every error incorrectly return HTTP 200?
Can the frontend distinguish validation from auth from server failure?
```

---

## TODO 2: Write a Serializer for Profile Update

Design something like:

```python
class UpdateProfileSerializer(serializers.Serializer):
    username = serializers.CharField(...)
    profile = serializers.CharField(...)
    photo = serializers.ImageField(required=False)
```

Move field-level concerns into the serializer:

```text
presence
blank handling
length
file type/basic validation
```

Leave the View focused on business behavior:

```text
validate input
resolve authenticated user
check business conflicts/ownership
persist
return an intentional response
```

---

## TODO 3: Compare with the current account serializers

Read:

```text
backend/web/serializers/account.py
```

Current authentication serializers are a reference implementation for:

- explicit fields;
- registration-specific password policy;
- machine-readable validation errors;
- keeping password verification/business logic in the appropriate layer.

Do not assume every endpoint must copy the exact same serializer shape. Learn the separation of responsibilities.

---

## TODO 4: Design a stable error envelope

A learning-friendly target might be:

```json
{
  "result": "error",
  "code": "USERNAME_EXISTS",
  "message": "Username already exists.",
  "fields": {
    "username": ["Username already exists."]
  }
}
```

The exact schema can evolve, but avoid using a human-language sentence as the only machine protocol.

### Explain the roles

```text
HTTP status → broad protocol/result category
code        → stable application-level machine meaning
message     → human-readable explanation
fields      → field-specific validation details
```

---

## TODO 5: Use status codes intentionally

Be able to explain at least:

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

### Security question

A Character exists but is owned by someone else. Should an edit endpoint return:

```text
403
```

or:

```text
404
```

There is no universal answer. Discuss information disclosure, API consistency, and client behavior.

---

## TODO 6: Refactor one older endpoint

Choose Profile or Character CRUD.

Compare:

```text
APIView
GenericAPIView
ModelViewSet
```

Do not choose a ViewSet only because it produces fewer lines of code.

Discuss:

- is the resource standard CRUD?
- are multipart uploads involved?
- are there custom actions?
- is object-level authorization complex?
- does the endpoint return a streaming response?

A streaming chat endpoint, for example, has very different needs from simple CRUD.

---

## TODO 7: Test validation and authorization

Add automated cases such as:

```text
missing username
username containing only whitespace
profile too long
invalid image
unauthenticated request
attempt to modify another user's Character
duplicate username
provider-dependent feature disabled
```

### Acceptance

Tests should assert both:

```text
HTTP status
machine-readable response meaning
```

where that contract is already defined.

---

## TODO 8: Avoid broad exception handling

Find an endpoint with a broad/bare exception.

Refactor so expected problems are handled specifically while unexpected bugs still produce useful tracebacks/logs.

Distinguish:

```text
validation error
object not found
permission failure
provider unavailable
unexpected programmer error
```

Collapsing all five into one generic “failed” response makes debugging and security review harder.

---

## TODO 9: Think about OpenAPI

Once serializers and status contracts become explicit, machine-readable API documentation becomes easier.

Compare:

```text
OpenAPI / Swagger schema
vs
human teaching document such as docs/API_REFERENCE_EN.md
```

They complement each other:

- schema is precise and tool-friendly;
- teaching docs explain architecture and why the contract exists.

---

## Acceptance

- [ ] You wrote or refactored at least one Serializer.
- [ ] You removed at least one broad/bare `except:` from an exercise endpoint.
- [ ] At least one endpoint returns a meaningful non-200 error status.
- [ ] The frontend can distinguish validation/conflict/auth errors.
- [ ] Automated tests protect the refactor.
- [ ] You can explain status code vs business error code.

---

## Challenge: Create an error-code catalog

Design codes such as:

```text
AUTH_INVALID_CREDENTIALS
AUTH_REFRESH_EXPIRED
VALIDATION_ERROR
USERNAME_EXISTS
CHARACTER_NOT_FOUND
FRIEND_NOT_FOUND
AI_PROVIDER_UNAVAILABLE
RAG_NOT_READY
ASR_DISABLED
TTS_DISABLED
```

Then update the API reference with:

```text
code
HTTP status
endpoint(s)
meaning
client action
```

Avoid inventing codes in documentation that the runtime does not yet return. Mark proposed codes separately from implemented ones.
