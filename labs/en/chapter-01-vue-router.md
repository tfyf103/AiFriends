# Chapter 01 Lab: Vue Pages, Components, and Router

🌐 **Language:** [中文](../chapter-01-vue-router.md) | **English**

## Goal

Before connecting Django, understand **why the web page changes without reloading the entire document**.

You will build three routes:

```text
/
/login
/register
```

and prove that navigation happens inside one Vue application.

---

## Historical checkpoints

Inspect these real project commits:

```text
b1703e8eff39f95dcd8cf3ed7b5d1def0e616758  routing implemented
b938159da24699eaec1249251b99ec06884f6b0a  login/register pages implemented
```

Compare them:

```bash
git diff b1703e8eff39f95dcd8cf3ed7b5d1def0e616758 b938159da24699eaec1249251b99ec06884f6b0a
```

Before reading the diff, predict what the Router had to gain when new pages were added.

---

## TODO 1: Create three views

Start with one title per page:

```text
Homepage
Login
Register
```

Use Vue Single-File Components:

```vue
<script setup>
</script>

<template>
</template>

<style scoped>
</style>
```

### Acceptance

- [ ] Each URL renders the expected page.
- [ ] Changing routes does not trigger a full white-page browser reload.
- [ ] You can point to the line in `main.js` where Router is installed into the Vue app.

---

## TODO 2: Navigate with `RouterLink`

Do not start with a normal document navigation:

```html
<a href="/login">Login</a>
```

Use Vue Router instead:

```vue
<RouterLink :to="{ name: 'user-account-login-index' }">
  Login
</RouterLink>
```

### Explain why

Your explanation should include:

- client-side routing;
- keeping the existing Vue app alive;
- avoiding a complete document download for every navigation;
- Router-managed params, query strings, route metadata, and navigation guards.

---

## TODO 3: Use your first reactive `ref()`

In the login page:

```js
const username = ref('')
const password = ref('')
```

Bind them with `v-model`.

Temporarily show:

```text
Current username: ...
```

Do **not** render the password.

### Acceptance

Typing changes the displayed username immediately.

You should be able to explain:

> `ref()` does not mean “read the current DOM input value.” It creates reactive application state that Vue tracks and renders.

---

## TODO 4: Extract a child component

Move the submit button into something like:

```text
components/LoginButton.vue
```

Pass a prop:

```text
loading
```

and emit an event:

```text
submit
```

Use both:

```js
defineProps()
defineEmits()
```

### Deliberate failure

Try mutating the incoming prop directly inside the child.

Then fix the design so the child emits intent and the parent owns the state change.

---

## TODO 5: Route params vs query parameters

Create two experiments:

```text
/user/space/123
/?q=Alice
```

Read them with:

```js
const route = useRoute()
```

Display:

```text
route.params.user_id
route.query.q
```

### Reason about the difference

A useful rule of thumb:

```text
/user/123  → resource identity; part of the path
?q=Alice   → optional/filtering state; can change independently
```

---

## Reference mental model

```text
main.js
  ↓ createApp
App.vue
  ↓ RouterView
router/index.js
  ↓ select the view for the current URL
views/*.vue
  ↓ compose
components/*.vue
  ↓ props / emits
reactive state with ref()
```

Do not think of Vue Router as “switching HTML files.” It decides which component tree should be rendered inside the same Vue application.

---

## Common errors

### URL changes but the page content does not

Check:

- whether `RouterView` exists;
- whether the route is registered;
- whether the route name/path is the one you think it is.

### `ref is not defined`

Import it:

```js
import { ref } from 'vue'
```

### A child component cannot safely change a prop

Props belong to the parent. Emit an event and let the parent update its own state.

### A normal `<a>` reloads the app

That is normal browser navigation. Use `RouterLink` when you want Vue Router navigation.

---

## Challenge

Build a fake navigation state without Pinia yet:

```text
Logged out: Login / Register
Logged in:  Home / Friends / Create / Logout
```

Use a parent-level:

```js
ref(false)
```

for the fake login state.

In Chapter 03, compare this local approach with a real shared user store and explain why authentication state belongs in a centralized store.
