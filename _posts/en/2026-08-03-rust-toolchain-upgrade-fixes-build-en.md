---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rust toolchain upgrade fixes build
translated: false
type: note
---

Done. Here's what happened:

## Summary

**1. Git pull** — Already at the latest commit. `origin/main` was up to date at `d48ab2d` ("Fix BCG circular import during server startup").

**2. Build failed initially** — The freshly pulled code includes a new Rust crate, `sglang-server` (added in PR #33103, "feat: rust sglang server openai apis"), which pulls in `rustpython-ruff_python_ast@0.15.8` and friends that require **rustc ≥ 1.92**. Your installed toolchain was rustc 1.91.0, so `cargo` refused to compile.

**3. Fixed the toolchain** — Upgraded the rustup stable toolchain:
```
stable updated - rustc 1.97.1 (from rustc 1.91.0)
```

**4. Rebuilt** — `pip install -e . --no-deps` recompiled all Rust/PyO3 extensions:
- `sglang/srt/grpc/_core` → 6.5 MB
- `sglang/srt/multimodal/_core` → 1.1 MB
- `sglang/srt/server/_core` → 13.4 MB (new crate)

**5. Verified** — Fresh install `sglang-0.0.0.dev63+gd48ab2d38` imports cleanly with all Rust extensions loading.

One note: the old toolchain 1.91.0 is still installed via rustup (can switch back with `rustup override` if needed), and the upgrade is user-level — nothing system-wide was modified.