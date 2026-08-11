# Chapter 03 Lab: Registration, Login, JWT, Pinia, and Axios

🌐 **Language:** [中文](../chapter-03-jwt-auth.md) | **English**

## Goal

Turn a login form into a real authentication system.

The target request lifecycle is:

```text
Vue login form
  ↓ POST username/password
Django authenticate()
  ↓
access token → JSON to JavaScript
refresh token → HttpOnly Cookie
  ↓
Pinia stores access token
  ↓
Axios adds Authorization: Bearer ...
  ↓
access expires → one refresh → retry original request(s)
```

The current project also reuses the same refresh mechanism for SSE so normal API requests and streaming requests do not drift into two incompatible authentication systems.

---

## Historical checkpoints

```text
248a7d8ea7c24e32d6f6a5d3631e277e7a09bb87  backend authentication endpoints
b0aa1d5c169d836023fd3788152d5cb1eb4bf55b  restore user state after refresh
 a27cbf8f90cf256ab075173f19d468319b302f67 front-end registration/login/logout
```

Use these commits as engineering archaeology. Current `main` has since added serializers, centralized refresh-cookie handling, and a shared single-flight refresh path.

---

## TODO 1: Implement registration first

Endpoint:

```text
POST /api/user/account/register/
```

Request:

```json
{
  "username": "alice",
  "password": "123456"
}
```

Requirements:

- username cannot be blank;
- password cannot be blank;
- registration password follows the current serializer policy;
- username must be unique;
- use `User.objects.create_user()` so Django hashes the password;
- create the matching `UserProfile`.

### Current status semantics

The maintained project uses:

```text
201 Created      successful registration
400 Bad Request  invalid input
409 Conflict     username already exists
```

### Acceptance

- [ ] A Django `User` row exists after registration.
- [ ] The stored password is not the original plaintext.
- [ ] Duplicate usernames return a machine-detectable conflict.
- [ ] Validation errors do not become unhandled 500s.

---

## TODO 2: Implement login

Use Django authentication:

```python
user = authenticate(username=username, password=password)
```

Then issue JWTs:

```python
refresh = RefreshToken.for_user(user)
```

Return the access token in JSON and put the refresh token in an HttpOnly Cookie.

### Current status semantics

```text
200 OK            login succeeded
400 Bad Request   malformed/blank input
401 Unauthorized  invalid credentials
```

### Explain the storage split

The project intentionally uses:

```text
access token  → JavaScript/Pinia, needed for Authorization header
refresh token → HttpOnly Cookie, not read directly by normal app JavaScript
```

This is a design choice, not the only possible JWT architecture. Explain its trade-offs instead of memorizing it as a universal rule.

---

## TODO 3: Inspect tokens in DevTools

After login:

```text
DevTools → Network → login request
```

Inspect:

- Request Payload;
- Response JSON;
- Set-Cookie / browser cookie state.

Then inspect a protected request and find:

```http
Authorization: Bearer <access-token>
```

### Acceptance

You can identify where the access token travels and where the refresh token is stored/sent.

---

## TODO 4: Manage identity with Pinia

The store should contain enough shared user state for the app, for example:

```text
id
username
photo
profile
accessToken
```

and actions such as:

```text
isLogin()
setAccessToken()
setUserInfo()
logout()
```

### Why a store?

Explain:

- one source of truth;
- many components depend on identity;
- login/logout must update the whole app consistently;
- duplicating user state in NavBar, Friend, Profile, etc. creates drift.

---

## TODO 5: Axios request interceptor

Create/reuse one `api` instance so protected normal HTTP requests automatically attach:

```http
Authorization: Bearer <access-token>
```

A feature component should be able to write:

```js
api.get('/api/some/protected/path/')
```

without duplicating auth headers everywhere.

---

## TODO 6: Refresh an expired access token

The basic flow:

```text
Request A → 401
          ↓
POST /api/user/account/refresh_token/
          ↓
new access token → Pinia
          ↓
retry Request A
```

The more important concurrency question:

> What happens when A, B, and C all receive 401 at almost the same time?

Current AiFriends centralizes this with:

```text
frontend/src/js/http/authRefresh.js
frontend/src/js/utils/singleFlight.js
```

The desired behavior is:

```text
A 401 ─┐
B 401 ─┼→ one refresh Promise → new access → A/B/C retry
C 401 ─┘
```

### Deliberate failure experiment

Temporarily bypass single-flight protection and trigger multiple concurrent protected requests with an expired access token.

Observe how many refresh requests appear in Network, then restore the shared refresh path.

---

## TODO 7: Understand refresh cookies in local development

The project centralizes refresh-cookie behavior in:

```text
backend/web/views/user/account/cookies.py
```

Development and production do not use identical cookie security settings. In local `DEBUG=true`, Secure cookies would break plain-HTTP onboarding, while production should use HTTPS and secure cookie handling.

Vite also proxies `/api` and `/media` so the browser sees a same-origin development path and avoids unnecessary localhost-vs-127.0.0.1 cookie friction.

### Acceptance

You can explain:

```text
HttpOnly
Secure
SameSite
cookie Path
same-origin development proxy
```

at a conceptual level.

---

## TODO 8: Router guard

Mark protected routes with metadata such as:

```js
meta: {
  needLogin: true,
}
```

### Acceptance

- [ ] A logged-out user cannot enter `/friend`.
- [ ] A logged-in user can.
- [ ] Reloading the page does not redirect too early while the app is still attempting to restore the session through the refresh cookie.

---

## TODO 9: SSE uses the same refresh truth

Streaming chat does not use the same request mechanism as ordinary Axios calls.

Current files:

```text
frontend/src/js/http/api.js
frontend/src/js/http/streamApi.js
frontend/src/js/http/authRefresh.js
```

When an SSE connection opens with an expired access token:

```text
SSE 401
  ↓
refreshAccessToken()
  ↓
write new access to Pinia
  ↓
restart the stream with a newly built Authorization header
```

This fixes a real historical class of bug: “refresh endpoint succeeded, but SSE retried with the stale token.”

---

## Reference mental model

Authentication is not “the login page.”

```text
Credentials
  ↓
Django Auth
  ↓
JWT issuance
  ↓
Token storage
  ↓
Request / streaming clients
  ↓
DRF authentication
  ↓
request.user
  ↓
object-level authorization
```

Business views should normally rely on authenticated `request.user`, not repeatedly trust usernames/user IDs sent by the browser.

---

## Common errors

### Login succeeds but protected APIs return 401

Check Network first:

```http
Authorization: Bearer ...
```

### Refresh cookie is missing

Inspect:

```text
credentials / withCredentials behavior
SameSite
Secure
host/origin
cookie Path
DEBUG vs HTTPS environment
```

### Infinite refresh loop

Do not route the refresh endpoint itself through a response interceptor that treats its own 401 as another reason to refresh forever.

### Page refresh loses Pinia state

Pinia memory is not permanent storage. AiFriends restores access using the HttpOnly refresh cookie, then fetches current user information again.

### Many simultaneous refresh calls

Your refresh logic is not using single-flight coordination.

---

## Challenge

Replace the access token in DevTools/app state with an invalid string, then open a protected page.

Record the actual network sequence:

```text
original protected request
  ↓ 401
refresh request (cookie)
  ↓ 200 + new access
retry original request (new Bearer token)
```

Explain which step uses access, which step uses refresh, and why the browser can send the refresh cookie even though normal JavaScript cannot read its HttpOnly value.
