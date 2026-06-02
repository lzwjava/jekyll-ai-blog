---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open-Source Components of macOS
translated: false
type: note
---

**Question:** Does macOS have open-source components? Where can I find the source?

**Answer:**

Yes — macOS is partially open source. Apple calls this collection **Darwin**, and it covers the core OS layer. Here's the breakdown:

## What's Open Source

### 1. Darwin / XNU Kernel
The kernel itself — **XNU** (X is Not Unix) — is open source. It's a hybrid kernel combining:
- **Mach** microkernel (from CMU)
- **BSD** (FreeBSD-derived) layer
- **IOKit** for drivers

→ **Source:** https://github.com/apple-oss-distributions/xnu

### 2. Apple OSS Distributions
Apple publishes a large collection of open-source components that ship in macOS:

→ **Main hub:** https://opensource.apple.com/

→ **GitHub org:** https://github.com/apple-oss-distributions

This includes: `dyld`, `libdispatch` (GCD), `libc`, `launchd`, `zsh`, `bash`, `curl`, `WebKit`, `clang/LLVM`, `Swift stdlib`, `libpthread`, and hundreds more.

### 3. LLVM / Clang
Apple is a major contributor. The `clang` you get with Xcode is Apple's fork.

→ https://github.com/llvm/llvm-project

### 4. Swift
Fully open source.

→ https://github.com/apple/swift

### 5. WebKit
The browser engine behind Safari.

→ https://github.com/WebKit/WebKit

---

## What's Closed Source

Everything above the Darwin layer is proprietary:

- **AppKit / UIKit / SwiftUI** — UI frameworks
- **CoreGraphics, Metal** — GPU/rendering stack
- **Finder, Spotlight, Siri** — user-facing apps
- **Security Enclave** firmware
- **WindowServer** — the compositor
- **CoreML runtime internals**

---

## Quick Reference

| Component | Open? | URL |
|---|---|---|
| XNU kernel | ✅ | github.com/apple-oss-distributions/xnu |
| dyld (dynamic linker) | ✅ | github.com/apple-oss-distributions/dyld |
| libdispatch (GCD) | ✅ | github.com/apple/swift-corelibs-libdispatch |
| launchd | ✅ | github.com/apple-oss-distributions/launchd |
| Swift | ✅ | github.com/apple/swift |
| WebKit | ✅ | github.com/WebKit/WebKit |
| AppKit/UIKit | ❌ | closed |
| Metal | ❌ | closed |
| WindowServer | ❌ | closed |

---

## Practical tip

If you want to read XNU source alongside kernel behavior, pair it with:
```bash
# Check your macOS version → match to XNU release tag
sw_vers -productVersion
# Then find matching tag at:
# https://github.com/apple-oss-distributions/xnu/tags
```

Apple doesn't always release source at the same time as the OS ships — there's usually a lag of weeks to months after a major release.
