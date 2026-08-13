---
audio: false
generated: true
image: false
lang: en
layout: post
title: "WeFlow: WeChat History Export Tool"
translated: false
type: note
---

Question: What is WeFlow, the WeChat history export tool?

Answer: WeFlow is a fully local, open-source tool (Electron + React + TypeScript) for viewing, analyzing, and exporting WeChat chat history in real time. It supports WeChat version 4.0 and above, and it's a fully local tool for viewing, analyzing, and exporting WeChat chat history in real time, generating unique analysis reports based on your chat history.

How it works:

- Reads the WeChat client's local SQLite/MSG database files directly off disk (Windows/macOS/Linux) — no root needed, no cloud upload.
- It works by directly reading the local database files (the MSG files) on your Windows WeChat client to retrieve all chat records — text, images, stickers, files — and lets you export as structured HTML archives filterable by contact, group, or time range.
- It can decrypt images, videos, and Live Photos from chats (only those shot with Google's protocol for Live Photos), supports modifying/deleting local messages, and refreshes new messages in real time without generating an intermediate decrypted database.
- Claims "zero network permission" — everything from DB decryption to rendering happens locally, no outbound connections.

Repo status — worth knowing before you `git clone`:
The original repo (`hicccc77/WeFlow`) got hit with a DMCA 1201 takedown from Tencent's lawyers (MSK firm), framed as circumventing WeChat's DB encryption ("sophisticated techniques"). The README now sarcastically memorializes this, noting the project doesn't contain any cracking/decryption/reverse-engineering code, and that any "data visualization phenomena" from opening an unencrypted SQLite file with the tool aren't the developer's fault. There are forks like `jacklilyhello/WeFlow` and `chency7/WeFlow` circulating post-takedown — check which fork is actually maintained before relying on it, since the original author's contact info was scrubbed for privacy.

If you're doing this programmatically instead (which fits your CLI-first workflow better): WeChat on Windows/macOS stores messages in an encrypted SQLite DB; the key derivation and table schema are what tools like this reverse-engineer. For Android there's also `wechat-dump` (rooted phone + adb), which parses WeChat messages from a rooted Android phone and renders them into self-contained HTML files including voice messages, images, emojis, and video — more scriptable than WeFlow's GUI if you want to pipe chat history into an LLM pipeline.

References:

- [chency7/WeFlow](https://github.com/chency7/WeFlow)
- [hicccc77/WeFlow (original, DMCA'd)](https://github.com/hicccc77/WeFlow)
- [jacklilyhello/WeFlow (fork)](https://github.com/jacklilyhello/WeFlow)
- [ppwwyyxx/wechat-dump (Android, scriptable)](https://github.com/ppwwyyxx/wechat-dump)
