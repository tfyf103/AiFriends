# Contributing to AiFriends

Thank you for helping improve AiFriends. The project is both a real full-stack AI application and a step-by-step bilingual learning repository, so contributions should preserve three qualities at the same time:

1. **the code should become more correct, secure, and maintainable;**
2. **a beginner should still be able to understand why the code exists;**
3. **Chinese and English learning paths should not silently drift away from the maintained source.**

## Good contributions

Useful contributions include:

- bug fixes with a reproducible case;
- authentication, authorization, upload, streaming, RAG, or dependency security improvements;
- tests that catch a real regression;
- clearer error messages and beginner diagnostics;
- documentation fixes where source code and tutorial content drift apart;
- Chinese/English terminology, translation, link, or screenshot synchronization fixes;
- new labs or debugging exercises tied to real project behavior;
- accessibility, performance, build, CI, observability, or deployment improvements;
- RAG/Memory evaluation cases with clear expected behavior.

For large architecture changes, opening an Issue first is recommended so the scope can be discussed before a large PR is written.

## Security reports

Do **not** disclose suspected vulnerabilities in a public Issue or Pull Request. Follow [SECURITY.md](./SECURITY.md) instead.

## Development setup

### 1. Fork and branch

Create a fork, then work from the latest `main` branch.

```bash
git clone https://github.com/<your-user>/AiFriends.git
cd AiFriends
git switch -c feature/short-description
```

Keep one PR focused on one logical change whenever possible.

### 2. Python environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Use Mock mode first

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

For most contribution work, begin with:

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

Mock mode lets contributors test JWT, Django, Friend, SSE, Vue, Message persistence, and Browser E2E without spending external AI credits.

### 4. Prepare Django

```bash
cd backend
python manage.py migrate
python manage.py seed_demo
python manage.py doctor
```

Run the backend:

```bash
python manage.py runserver
```

### 5. Prepare the frontend

In another terminal:

```bash
cd frontend
npm ci
npm run dev
```

If you work on microphone/VAD features, also run:

```bash
npm run setup:vad
```

## Required checks before a PR

Run the checks that match your change. For most PRs, run all of these.

### Course structure

```bash
python scripts/grade.py --chapter 20
```

### Internationalization / documentation drift

```bash
python scripts/check_i18n.py
```

This deterministic check covers paired core documents, Chapter 00–20 bilingual Lab coverage, important source sentinels, required live-demo assets, canonical glossary terms, and important relative links. It is a structural guard, not a semantic translation judge.

When live-demo screenshots change:

```bash
python scripts/build_demo_gif.py
python scripts/build_demo_gif.py --check
```

### Backend

```bash
cd backend
python manage.py makemigrations --check --dry-run
python manage.py check
python manage.py test web
```

### Frontend

```bash
cd frontend
npm run check
npm test
npm run build
```

### Browser E2E

For user-visible authentication/routing/browser-flow changes, run the English-first Browser E2E example where practical:

```bash
npm install --prefix e2e
npm exec --prefix e2e -- playwright install chromium
node e2e/browser-smoke.mjs
```

The default E2E uses a temporary SQLite database and `AI_MODE=mock`; it must not depend on production data or real model credentials.

GitHub Actions repeats the main checks in a clean environment, runs the Browser E2E gate, and builds the learning Docker image.

## Testing expectations

A bug fix should usually include a regression test when the behavior can be tested safely.

When adding or changing an AI feature, separate deterministic behavior from paid/non-deterministic model behavior whenever possible. Prefer testing:

- request validation;
- permissions and ownership;
- state transitions;
- SSE event shapes;
- cancellation behavior;
- retrieval behavior independently from answer generation;
- feature flags and fallback paths.

Do not require real API keys in the default CI workflow.

Use Browser E2E for a small number of high-value cross-layer contracts. Do not duplicate every unit/behavior test in Chromium.

## Documentation expectations

AiFriends is a teaching repository. If a change alters a learner-visible concept, update the relevant documentation in the same PR.

Common places to check:

- `README.md` / `README_EN.md` — project entry point and current capabilities;
- `docs/README.md` / `docs/README_EN.md` — learning-hub navigation and status;
- `docs/COURSE_REBUILD.md` / `docs/COURSE_REBUILD_EN.md` — historical engineering archaeology;
- `docs/API_REFERENCE*.md` — route/status/payload changes;
- `docs/ARCHITECTURE*.md` — request-flow or component changes;
- `docs/DATABASE_ER*.md` — model/relationship changes;
- `docs/TROUBLESHOOTING*.md` — current failure modes;
- `docs/BILINGUAL_GLOSSARY.md` — canonical Chinese/English terminology;
- `docs/SCREENSHOTS.md` — visual evidence and screenshot/GIF rules;
- `docs/i18n-manifest.json` — paired documents, source sentinels, and required assets;
- `docs/GRADING.md` — validation workflow changes;
- `labs/` and `labs/en/` — chapter exercises affected by the change;
- `e2e/` — high-value browser contracts.

Do not present an intentionally simplified learning implementation as production-ready architecture.

### Bilingual documentation rules

- Keep source identifiers literal when they refer to code: `Character`, `Friend`, `Message`, `AI_MODE`, `ToolNode`, `X-Request-ID`.
- Follow [docs/BILINGUAL_GLOSSARY.md](./docs/BILINGUAL_GLOSSARY.md) for canonical terminology.
- Mark historical behavior as historical when current `main` has evolved.
- Prefer one real language-neutral screenshot with separate Chinese/English captions over duplicated image bytes.
- Never present a generated mockup as proof that a runtime feature works.
- If you add or rename a paired core document/source sentinel, update `docs/i18n-manifest.json`.

## Pull Request checklist

Before requesting review, confirm:

- [ ] The PR has a focused purpose and explains **why** the change is needed.
- [ ] No real `.env`, API key, token, private conversation, database, or runtime vector-store data is committed.
- [ ] New behavior is covered by an appropriate test where practical.
- [ ] `python manage.py makemigrations --check --dry-run` passes when models changed.
- [ ] Backend tests pass when backend behavior changed.
- [ ] Frontend checks/build pass when frontend behavior changed.
- [ ] `python scripts/check_i18n.py` passes for documentation/source changes.
- [ ] Browser E2E passes when a covered user-visible flow changed.
- [ ] Learner-facing Chinese/English docs are updated when behavior or architecture changed.
- [ ] New screenshots/GIFs follow `docs/SCREENSHOTS.md` and contain no secrets/private content.
- [ ] Security-sensitive changes explain trust boundaries and expected failure behavior.

## Code style and reviewability

Prefer:

- small functions with clear responsibilities;
- explicit validation and meaningful HTTP status codes;
- object-level authorization close to data access;
- configuration through environment/settings rather than scattered hard-coded provider values;
- comments that explain *why*, not comments that merely restate syntax;
- minimal diffs over unrelated formatting churn.

Avoid broad `except:` blocks for new code unless there is a documented reason and the original error remains observable through safe logging.

## AI/RAG contribution notes

When changing RAG or Memory behavior, include a concrete evaluation story rather than only a subjective demo.

For retrieval work, consider adding cases under `evals/` and running:

```bash
python scripts/eval_rag.py --cases evals/rag_cases.example.json --k 3
```

If a change introduces a Tool or external side effect, document:

- who is allowed to invoke it;
- what data it can read/write;
- what untrusted model/user text can reach it;
- how failure and timeout behavior are handled.

## License

By contributing to AiFriends, you agree that your contribution may be distributed under the repository's [MIT License](./LICENSE).
