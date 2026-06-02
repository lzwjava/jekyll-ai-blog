---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: NPM Overrides Support by Version Guide
translated: false
type: note
---

You're correct on most points! Let me clarify the npm versions and their `overrides` support:

**npm and `overrides` support:**

- **npm 6**: No `overrides` support ❌
- **npm 7**: No `overrides` support ❌
- **npm 8.3.0+**: First version with `overrides` support ✅
- **npm 8.1**: No `overrides` support (as you noted)

**Node.js versions and their bundled npm:**

- **Node 14**: Ships with npm 6.x (no `overrides`)
- **Node 16**: Ships with npm 7.x - 8.x depending on the exact version
  - Most Node 16 versions ship with npm 7.x or early npm 8.x (before 8.3)
  - Only later Node 16 patch versions include npm 8.3+
- **Node 18**: Ships with npm 8.19.x or later (has `overrides` support) ✅

**Bottom line:**
You need **npm 8.3.0 or higher** for `overrides` to work. The safest approach is:

- Use Node 18+ (which guarantees npm 8.3+)
- Or manually upgrade npm to 8.3+ on Node 16: `npm install -g npm@8.3.0`

So yes, your understanding is correct—Node 18 is the reliable choice for `overrides` support out of the box!
