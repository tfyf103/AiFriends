# AiFriends Screenshots & GIF Guide / 截图与 GIF 指南

[简体中文 + English]

This page is the bilingual visual index for AiFriends and the contribution standard for future screenshots/GIFs. / 本页既是 AiFriends 的双语视觉索引，也是后续截图/GIF 贡献规范。

> **Authenticity rule / 真实性规则：** real-runtime screenshots must come from a real local runtime or the deployed application. Generated design mockups may be useful for proposals, but they must be explicitly labeled as mockups and must never be presented as proof that a feature works. / 真实运行截图必须来自真实本地运行环境或线上部署；生成式设计稿必须明确标注，不得冒充功能已运行的证据。

---

## 1. Real production walkthrough / 真实线上体验动图

![AiFriends real production walkthrough](./assets/live-demo/walkthrough.gif)

The animation is generated **only from the four real production screenshots below** using `scripts/build_demo_gif.py`. It is a visual gallery, not a claim that one recorded browser session performed all four actions. / 该 GIF 仅由下面 4 张真实线上截图通过 `scripts/build_demo_gif.py` 合成；它是视觉浏览动图，不表示同一段录屏完成了全部交互。

Rebuild / 重新生成：

```bash
python scripts/build_demo_gif.py
```

Verify it is up to date / 检查 GIF 是否与截图同步：

```bash
python scripts/build_demo_gif.py --check
```

---

## 2. Real production screenshots / 真实线上截图

Captured on **2026-08-11** from the public deployment documented in [LIVE_DEMO.md](./LIVE_DEMO.md). / 这些截图于 **2026-08-11** 从真实公开部署采集，验证方式见 [LIVE_DEMO.md](./LIVE_DEMO.md)。

### Homepage / 首页

![Live homepage](./assets/live-demo/homepage.png)

**EN:** Public Character discovery from the deployed homepage.  
**中文：** 线上首页的公开 AI Character 发现页面。

### Login / 登录

![Live login](./assets/live-demo/login.png)

**EN:** Real deployed login form.  
**中文：** 真实线上登录表单。

### Register / 注册

![Live register](./assets/live-demo/register.png)

**EN:** Real deployed registration form.  
**中文：** 真实线上注册表单。

### Public user space / 公开用户空间

![Live public user space](./assets/live-demo/public-profile.png)

**EN:** Public user space and associated Character content.  
**中文：** 公开用户空间与其关联的 Character 内容。

---

## 3. Screenshot naming convention / 截图命名规范

Use lowercase kebab-case and describe the user-visible state. / 使用小写 kebab-case，并描述用户真正看到的状态。

Good / 推荐：

```text
homepage.png
login.png
register.png
friend-list-empty.png
chat-streaming-text.png
rag-citation-result.png
voice-input-ready.png
```

Avoid / 避免：

```text
Screenshot 2026-08-11 at 20.00.00.png
final-final-2.png
image.png
```

For bilingual docs, prefer reusing one language-neutral product screenshot with separate Chinese/English captions instead of duplicating identical image bytes. / 对中英文文档，优先复用同一张语言中立的产品截图，并分别提供中英文说明，而不是复制两份相同图片。

---

## 4. Required screenshot metadata / 截图必须说明的信息

When a screenshot is used as evidence, document: / 当截图作为功能证据时，应说明：

- **source**: local runtime or production deployment / 来源：本地运行或线上部署；
- **capture date** for production snapshots / 线上快照的采集日期；
- **mode** when relevant: `mock`, `text`, or `full` / 必要时标明运行模式；
- **data boundary**: whether test data was created / 是否创建测试数据；
- **feature scope**: what the image proves and what it does not prove / 截图证明什么、不证明什么。

Example / 示例：

> Captured from local `AI_MODE=mock` after Browser E2E registration. This proves the frontend→backend authentication flow works; it does not prove external LLM/RAG/TTS providers are available.

---

## 5. GIF rules / GIF 规则

Prefer short GIFs for flows where motion matters: / 只有在“过程”本身重要时才优先使用 GIF：

- SSE text appearing incrementally / SSE 文本逐段出现；
- chat cancellation / 中止生成；
- audio/voice state transitions / 语音状态切换；
- RAG citation UI once available / 后续 RAG Citation UI；
- browser E2E happy path / 浏览器 E2E 主流程。

Keep GIFs: / GIF 应：

- short and focused / 短而聚焦；
- free of secrets/JWT/private conversations / 不包含密钥、JWT、私聊；
- readable without audio / 不依赖声音才能理解；
- accompanied by alt text and a text explanation / 同时提供 alt 文本和文字说明；
- generated from real runtime frames when presented as runtime evidence / 若作为运行证据，必须来自真实运行画面。

---

## 6. Screenshot review checklist / 截图审查清单

Before merge / 合并前：

- [ ] The image comes from the claimed source.
- [ ] No secrets, tokens, email addresses, or private conversations are visible.
- [ ] Production screenshots do not require destructive/mutating test actions unless explicitly documented.
- [ ] The file name is stable and descriptive.
- [ ] Chinese and English captions use terms from [BILINGUAL_GLOSSARY.md](./BILINGUAL_GLOSSARY.md).
- [ ] Relative image paths render from both repository landing pages where referenced.
- [ ] `python scripts/check_i18n.py` passes.
- [ ] `python scripts/build_demo_gif.py --check` passes when live-demo screenshots changed.

Related:

- [Live Demo Verification](./LIVE_DEMO.md)
- [Bilingual Engineering Glossary](./BILINGUAL_GLOSSARY.md)
- [English Browser E2E example](../e2e/README.md)
