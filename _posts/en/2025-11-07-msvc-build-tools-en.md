---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: MSVC Build Tools Uses and Alternatives
translated: false
type: note
---

The MSVC Build Tools are indeed massive! Here's what they're actually used for:

## Primary Uses

**For Rust specifically:**
- Building Rust crates that have **C/C++ dependencies** (very common)
- Compiling native Windows system APIs
- Linking against Windows libraries
- Building projects that use `cc` crate or bindgen

**General purposes:**
- Compiling C/C++ code on Windows
- Building Python packages with native extensions (like numpy, pandas)
- Compiling Node.js native addons
- Building any software that needs a C/C++ compiler on Windows

## Why So Large?

The bloat comes from:
- Windows SDK (headers, libraries for every Windows version)
- Multiple compiler toolchains (x86, x64, ARM, ARM64)
- ATL/MFC libraries
- Debugging tools and symbols
- Build system components (MSBuild)

## Lighter Alternatives

If you only need Rust:
1. **Use the GNU toolchain instead** - install `rustup` with the `x86_64-pc-windows-gnu` target (needs MinGW, ~2-3GB)
2. **WSL2** - Use Linux toolchain entirely
3. **Minimal MSVC install** - During installation, deselect optional components you don't need

For pure Rust code without C/C++ dependencies, you don't need MSVC at all. But realistically, many popular crates (like `openssl-sys`, `ring`, windowing libraries) need a C compiler, so most Windows Rust developers end up installing it.

It's annoying, but Microsoft's toolchain has always been heavy. The GNU alternative works but occasionally has compatibility issues with some crates.
