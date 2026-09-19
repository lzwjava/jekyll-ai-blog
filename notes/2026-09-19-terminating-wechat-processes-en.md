---
audio: false
generated: true
image: false
lang: en
layout: post
title: Terminating WeChat Processes
translated: false
type: note
---

Done. WeChat was running and is now terminated.

- Found the main process `/usr/bin/wechat` (PID 20044) plus ~15 helper processes (`WeChatAppEx`, `wxocr`, `wxplayer`, `wxutility`, crashpad handlers).
- Killed them all with `pkill -TERM -f`. A follow-up check shows **no remaining wechat/weixin processes**.

Note: the `pkill -f` pattern also matched the shell running the command itself (its command line contained "wechat"), so that shell was terminated before it could print the follow-up check — but WeChat was killed as intended. If you want a cleaner kill script in the future, use `pkill -f '/usr/bin/wechat|/opt/wechat/'` or kill by exact process name.
