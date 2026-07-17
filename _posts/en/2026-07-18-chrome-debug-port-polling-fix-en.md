---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chrome debug port polling fix
translated: false
type: note
---

Fixed and pushed (`d601f9f`).

The problem: `launch_chrome()` used a fixed `time.sleep(3)` — Chrome hadn't finished starting its debug server yet when Playwright tried to connect to port 9222, so you got `ECONNREFUSED`.

Now it polls port 9222 every 0.5s (up to 15s) and only returns once the port is actually accepting connections. Try `ww x unfollow` again.

One thing to note: you need to close all other Chrome windows first, otherwise Chrome may attach to the existing process and skip the `--remote-debugging-port` flag entirely.
