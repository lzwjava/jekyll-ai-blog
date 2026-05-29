---
audio: false
generated: true
image: false
lang: en
layout: post
title: Codex CLI Installation and Update Notes
translated: false
type: note
---

Here's what I found:

=== Current Codex Installation ===

Location:       /opt/homebrew/bin/codex (symlink to npm global)
Installed:      @openai/codex@0.128.0
Latest npm:     @openai/codex@0.135.0
You are 7 versions behind.

=== How to Update ===

Simplest way to update the CLI on this Mac:

    npm install -g @openai/codex@latest

That will pull 0.135.0 and replace the binary at /opt/homebrew/bin/codex.

=== Architecture Overview ===

The codex repo at /Users/lzwjava/projects/codex is a monorepo with:

1. npm package (@openai/codex) — the TypeScript CLI that bundles the Rust binary
2. Rust workspace (codex-rs/) — the actual binary source
   - codex-rs/cli/ — the `codex` binary (Rust)
   - codex-rs/tui/ — the `codex-tui` binary (ratatui-based TUI)
   - 100+ internal crates (core, config, mcp-server, tools, etc.)

The npm package ships a pre-built Rust binary for each platform (darwin-arm64, linux-x64, etc.), so `npm install -g` gets you both the JS wrapper and the native Rust codex binary.

=== Building from Source (optional, for dev) ===

If you want to build the Rust binary locally from this repo:

    cd /Users/lzwjava/projects/codex
    cargo build -p codex-cli        # builds codex binary
    cargo build -p codex-tui        # builds codex-tui

Or via just:
    just codex                      # cargo run --bin codex
    just test -p codex-tui          # run TUI tests

Want me to run `npm install -g @openai/codex@latest` to update it now?