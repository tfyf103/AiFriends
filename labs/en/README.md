# AiFriends English Labs

🌐 **Language:** [中文 Labs](../README.md) | **English**

> Goal: move from “I understand the explanation” to “I can implement it, break it on purpose, debug it, and prove it works.”

The complete AiFriends curriculum currently contains Chapters 00–20. This English track starts with six high-value chapters that cover the core full-stack AI path:

```text
00 Environment & reproducibility
06 Minimal LLM Chat
07 SSE Streaming
08 LangGraph Tool Calling
10 RAG + LanceDB
13 Full-System Capstone
```

These are translations and updates of the corresponding Chinese labs, while the same source code, tests, grader, CI, and acceptance philosophy are shared across languages.

---

## Recommended English path

```text
English Quick Start
      ↓
Chapter 00
      ↓
Chapter 06
      ↓
Chapter 07
      ↓
Chapter 08
      ↓
Chapter 10
      ↓
Chapter 13
      ↓
English Architecture Guide
```

| Chapter | Lab | What you prove |
|---|---|---|
| 00 | [Environment & Reproducible Setup](./chapter-00-environment.md) | Python/Node/Git setup; Django and Vite both run |
| 06 | [Minimal LLM Chat](./chapter-06-basic-chat.md) | Browser input reaches a real LLM through Django |
| 07 | [SSE Streaming Chat](./chapter-07-sse.md) | Tokens stream incrementally and messages persist |
| 08 | [LangGraph Tool Calling](./chapter-08-langgraph-tools.md) | Agent state, tools, ToolNode, conditional routing |
| 10 | [RAG + LanceDB](./chapter-10-rag.md) | Chunking, embeddings, retrieval, RAG Tool |
| 13 | [Full-System Capstone](./chapter-13-capstone.md) | Trace and modify one message across the entire stack |

---

# How to use these labs

Do not do every experiment directly on `main`.

A simple learning branch:

```bash
git switch main
git pull
git switch -c learn/aifriends
```

The repository also preserves real Git history. Historical commits are useful as engineering archaeology, but they may contain bugs or incomplete behavior that was fixed later.

Use this mental model:

```text
historical commit = how the project evolved
current tests      = current reference behavior
lab acceptance     = learning objective
```

After each lab, make your own learning commit:

```bash
git add .
git commit -m "learn: finish chapter 07 sse streaming"
```

---

# The eight-step lab loop

Every lab should follow this pattern:

1. **Predict first** — which files and layers should data pass through?
2. Build the **smallest working loop**.
3. Identify the acceptance criteria before adding complexity.
4. Keep browser DevTools and Django logs visible.
5. Change one layer at a time.
6. Create a deliberate failure and diagnose it.
7. Run grader/tests/build instead of trusting visual inspection.
8. Commit the result and explain the trade-off in your own words.

---

# Machine feedback

## Environment

```bash
cd backend
python manage.py doctor
```

## Structural grader

From the repository root:

```bash
python scripts/grade.py --chapter 7
python scripts/grade.py --chapter 13
python scripts/grade.py --chapter 20
```

## Backend tests

```bash
cd backend
python manage.py test web
```

## Frontend checks

```bash
cd frontend
npm run check
```

Pull requests also run GitHub Actions in a clean environment.

---

# What “finished” means

A finished lab is not just a page that looks approximately correct.

You should be able to answer questions such as:

- Which Vue file sends the request?
- What are the URL, HTTP method, headers, and body?
- Which Django View receives it?
- Which Models are read or written?
- Which messages enter the LLM?
- How does streaming data return?
- How can the request be cancelled?
- Where would you inspect the first failure signal?
- Which automated check protects the key behavior?

---

# English documentation

- [English Quick Start](../../docs/QUICK_START_EN.md)
- [English Architecture Guide](../../docs/ARCHITECTURE_EN.md)
- [English Learning Hub](../../docs/README_EN.md)
- [English Project README](../../README_EN.md)

For chapters that are not translated yet, use the [complete Chinese Labs index](../README.md).

English lab translations are welcome through [CONTRIBUTING.md](../../CONTRIBUTING.md).
