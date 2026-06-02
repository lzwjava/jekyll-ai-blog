---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building and Running Warp Terminal
translated: false
type: note
---

== Warp Build Summary ==

Prerequisites
-------------

- Rust 1.92.0 (installed via Homebrew)
- protoc (installed via `brew install protobuf`)
- Xcode command line tools (already present)

Build Commands
--------------

cd /Users/lzwjava/projects/warp

# Check (type-check only, ~2 min)

cargo check --bin warp-oss --features gui

# Build (compile binary, ~4.5 min)

cargo build --bin warp-oss --features gui

# Run

./target/debug/warp-oss

What Happened
-------------

1. cargo resolved ~500+ dependencies from Cargo.lock
2. Compiled 65+ local crates from crates/ directory
3. Linked against macOS frameworks (Cocoa, Metal, CoreFoundation)
4. Produced single binary: target/debug/warp-oss (721 MB debug, ~strip→smaller release)

Architecture
------------

- Language: Rust
- UI framework: custom warpui/warpui_core (GPU-accelerated, Metal backend)
- Terminal backend: Alacritty's VT parser + custom PTY layer
- Async runtime: Tokio
- Build system: Cargo workspace with 65+ crates
- Binary: warp-oss (OSS channel) or warp (internal channel)

Key Crates
----------

warp_terminal  - PTY, shell integration, terminal state
warpui         - GPU rendering, window management, input
ai             - LLM integration, agent features
mcp            - Model Context Protocol support
editor         - Code editor components
vim            - Vim mode support

Build Profiles
--------------

cargo build                          # debug (721 MB, unoptimized)
cargo build --release                # release (optimized, smaller)
cargo bundle --bin warp-oss --features gui  # .app bundle for macOS

Official Scripts
----------------

./script/bootstrap --skip-common-skills -y  # install all deps
./script/run                                 # build + launch as .app
./script/presubmit                           # fmt + clippy + tests
