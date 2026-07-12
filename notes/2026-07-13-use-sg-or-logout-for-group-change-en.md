---
audio: false
generated: true
image: false
lang: en
layout: post
title: Use sg or Logout for Group Change
translated: false
type: note
---

The group change only applies to **new login sessions**. Your current terminal still has the old group. Run this right now to work around it:

```bash
sg dialout -c "cargo run -- uno status"
```

That temporarily runs the command with the `dialout` group. Press `q` or `Esc` to quit.

If you want it to work without `sg`, **log out and back in** (or reboot), then you can run `cargo run -- uno status` directly.
