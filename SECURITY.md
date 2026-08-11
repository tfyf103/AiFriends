# Security Policy

AiFriends is an educational full-stack AI project, but it contains real security-sensitive surfaces: authentication and refresh cookies, file uploads, object-level authorization, SSE/WebSocket streaming, third-party AI endpoints, RAG/vector retrieval, and user-generated data.

Security reports are welcome and should be handled privately until a fix is available.

## Supported versions

AiFriends is under active development. Security fixes are made against the latest `main` branch. Older commits, tutorial checkpoints, historical Git states, and learning-only Docker examples are provided for education and are not maintained as production release lines.

| Version | Supported |
| --- | --- |
| Latest `main` | ✅ |
| Historical tutorial/checkpoint commits | ❌ |
| Forks or modified deployments | Best effort only |

## Reporting a vulnerability

**Please do not open a public GitHub Issue for a suspected vulnerability.**

Preferred reporting path:

1. Use GitHub's private vulnerability reporting / Security Advisory interface for this repository when it is available.
2. If private GitHub reporting is unavailable, email **tangfangyifan@gmail.com** with the subject `AiFriends Security Report`.

Please include as much of the following as possible:

- affected file, endpoint, component, or commit;
- vulnerability class and expected impact;
- minimal reproduction steps or proof of concept;
- required configuration or attacker prerequisites;
- whether secrets or personal data may have been exposed;
- suggested mitigation, if you have one.

Do not include real user secrets, access tokens, private conversations, or third-party credentials in a report unless strictly necessary. Redact them whenever possible.

## Response process

The maintainer aims to:

- acknowledge a valid private report within **5 business days**;
- provide an initial severity/reproducibility assessment within **14 days** when practical;
- keep the reporter informed when a fix requires a longer investigation;
- validate the fix with tests where the vulnerability can be reproduced safely;
- publish remediation details after users have had a reasonable opportunity to update.

These are best-effort targets for a small open-source project, not a guaranteed SLA.

## Security areas of particular interest

Reports are especially useful around:

- JWT issuance, refresh, logout, cookie attributes, and token replay;
- authorization bypass or cross-user access to Character/Friend/Message data;
- unsafe file upload, MIME/type confusion, path traversal, or oversized uploads;
- SSE/WebSocket authentication, cancellation, resource exhaustion, or data leakage;
- prompt injection that crosses a trust boundary or causes unsafe Tool behavior;
- RAG source/data leakage or retrieval of data outside the intended corpus;
- exposure of API keys, Django secrets, database contents, or private filesystem paths;
- vulnerable dependencies and supply-chain issues with a realistic impact on AiFriends;
- Docker/build configuration that unexpectedly exposes secrets or private data.

## Learning project vs. production deployment

`Dockerfile.learning`, `compose.learning.yml`, SQLite defaults, Django `runserver`, and permissive development settings are intentionally designed for learning. They are **not** a production-hardening guide.

A report that demonstrates an unexpected security impact in the documented learning configuration is still valuable. Production-hardening suggestions that do not demonstrate a vulnerability are better filed as normal Issues or Pull Requests.

## Coordinated disclosure

Please allow reasonable time for validation and remediation before public disclosure. Once a fix is ready, the maintainer is happy to credit reporters who want public attribution.

## Good-faith research

Good-faith security research that avoids privacy violations, data destruction, service disruption, and unnecessary access to third-party systems is welcome. Testing must stay within systems and data you are authorized to access.
