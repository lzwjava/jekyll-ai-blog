---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes /copy Command Addition Date
translated: false
type: note
---

Question: When was the `/copy` command added in Hermes?

Answer:

The `/copy` command in Hermes was added by commit **99fd3b51** on **2026-04-09**. This command itself does **not** add any timing information; the time elements you see in the status bar after using `/copy` come from other commits:

* **Session duration** (`44m`) — Added March 16, 2026, in commit **00a0c565**.
* **Per-prompt elapsed timer** (`⏲ 10m 19s`) — Added April 20, 2026, in commit **654d61ab**.

So the `/copy` command existed independently of these timers, which are part of the persistent status bar.

References:

* [Commit 99fd3b51 — Add /copy command](https://github.com/hermes-agent/hermes/commit/99fd3b51)
* [Commit 00a0c565 — Persistent CLI status bar](https://github.com/hermes-agent/hermes/commit/00a0c565)
* [Commit 654d61ab — Per-prompt elapsed timer](https://github.com/hermes-agent/hermes/commit/654d61ab)
