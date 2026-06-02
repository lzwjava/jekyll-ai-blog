---
audio: false
generated: true
image: false
lang: en
layout: post
title: Node.js 25 Breaks Amp Fixes
translated: false
type: note
---

**Question:** Why does `@sourcegraph/amp` crash with `TypeError: Cannot read properties of undefined (reading 'prototype')` on Node.js v25.3.0, and how do I fix it?

**Answer:**

## Root Cause

This is a **known Node.js v25 compatibility issue**, not a bug in your code. The error occurs because the dependency chain of tools like `@sourcegraph/amp` includes packages that rely on the deprecated `SlowBuffer` API, which was removed (marked as "End-of-Life") in Node.js v25.0.0 per **DEP0030**.

Specifically, `SlowBuffer.prototype` no longer exists in Node.js v25+, so when the bundled code tries to access `.prototype` on it, it gets `undefined` and throws the error.

This same issue has affected many CLI tools across the ecosystem — the CLI throws `TypeError: Cannot read properties of undefined (reading 'prototype')` because Node.js 25 removed support for `SlowBuffer`.

---

## Solutions

### ✅ Option 1: Downgrade Node.js (Recommended — Fastest Fix)

Switch to a Node.js LTS version that still supports `SlowBuffer`:

```bash
# Using nvm
nvm install 22
nvm use 22

# Or install Node.js v22 LTS from nodejs.org
```

Node.js **v20** or **v22** (LTS) are the most stable choices and are fully compatible with `@sourcegraph/amp`.

---

### ✅ Option 2: Use a Node Version Manager to Pin the Version

If you use `nvm`, add a `.nvmrc` file to your project:

```bash
echo "22" > .nvmrc
nvm use
```

---

### ✅ Option 3: Wait for an `@sourcegraph/amp` Update

The upstream package needs to update its transitive dependencies — specifically packages in the JWT/authentication chain that use `buffer-equal-constant-time` or similar libraries that rely on `SlowBuffer`. The proper fix is to update those transitive dependencies to use `crypto.timingSafeEqual()` instead of `SlowBuffer.prototype.equal`. Check the Sourcegraph/Amp GitHub repository for an updated release.

---

## Summary Table

| Node.js Version | Works with `@sourcegraph/amp`? |
|---|---|
| v18 (LTS) | ✅ Yes |
| v20 (LTS) | ✅ Yes |
| v22 (LTS) | ✅ Yes |
| v25+ | ❌ No (SlowBuffer removed) |

**TL;DR:** Downgrade to Node.js v20 or v22 LTS. Your Node v25.3.0 is the direct cause of the crash.

**References:**

- [Node.js v25 breaking change - SlowBuffer removal (Claude Code issue)](https://github.com/anthropics/claude-code/issues/9628)
- [Same issue on Salesforce CLI](https://github.com/forcedotcom/cli/issues/3460)
