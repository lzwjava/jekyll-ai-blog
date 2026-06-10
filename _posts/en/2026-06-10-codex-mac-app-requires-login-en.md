---
audio: false
generated: true
image: false
lang: en
layout: post
title: Codex Mac App Requires Login
translated: false
type: note
---

No. The Codex Mac app does need authentication.

Per the current official Codex docs, when you first open the app you should “sign in with your ChatGPT account or an OpenAI API key,” and Codex supports those two login methods for the app: ChatGPT login or API key login. Sources: [Codex app getting started](https://developers.openai.com/codex/app), [Authentication and sessions](https://developers.openai.com/codex/auth).

What may be confusing is this: after you log in once, Codex caches your credentials locally and reuses them later, so it can look like “no login is needed” on future launches. The docs say the app/CLI/IDE cache login details and ChatGPT sessions are refreshed automatically while active. Source: [Authentication and sessions](https://developers.openai.com/codex/auth).

So the short version is:

- First use: yes, login is required.
- Later use: maybe not prompted again, because the app remembers your login.

If you want, I can also explain the difference between `ChatGPT login` and `API key login` in one minute.
