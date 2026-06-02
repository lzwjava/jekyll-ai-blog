---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bodhi AI Desktop Agent Workbench
translated: false
type: note
---

Here's the breakdown:

== Bodhi AI ==

Bodhi AI is a Tauri 2 desktop application that serves as a desktop AI agent workbench. It's the "desktop shell" layer in a 3-part architecture:

  bodhi  = Tauri desktop shell (this repo)
  lotus  = React + Vite frontend UI (sibling repo @bigduu/lotus)
  bamboo = Rust backend runtime (sibling repo, published as bamboo-agent crate on crates.io)

== What it does ==

An AI agent desktop app that:
- Plans tasks, runs tools, connects MCP servers
- Keeps long-running context alive (memory, session notes, Dream notebook)
- Turns successful runs into workflows and schedules
- Shows its work (agent loop, tool calls, status changes are visible)

Think: a Hermes/Claude Code-style agent, but packaged as a native desktop app with a GUI.

== Tech stack ==

  Language:   Rust (Tauri 2) + TypeScript (React/Vite)
  Backend:    bamboo-agent crate (actix-web HTTP server, runs embedded in-process on port 9562)
  Frontend:   lotus (React, built separately, served as static dist)
  Tauri plugins: dialog, fs, global-shortcut, shell, process, notification, log

== Key source files ==

  src-tauri/src/main.rs          -- entry point, calls lib::run()
  src-tauri/src/lib.rs           -- Tauri builder, plugins, setup, commands
                                    - registers global shortcut Cmd/Ctrl+Shift+Space to toggle window
                                    - starts embedded bamboo HTTP server on 127.0.0.1:9562
                                    - commands: copy_to_clipboard, proxy config, theme, notifications
  src-tauri/src/embedded/mod.rs  -- manages embedded bamboo-agent WebService lifecycle
                                    - resolves static frontend dist from multiple candidates
                                    - health check loop (10 attempts, 200ms intervals)
  src-tauri/src/app_settings.rs  -- re-exports bamboo path helpers (data dir, config.json)
  src-tauri/src/command/copy.rs  -- clipboard copy command

== Architecture highlights ==

1. The bamboo backend runs IN-PROCESS (not a sidecar) -- the EmbeddedWebService wraps
   bamboo_agent::server::WebService directly in the Tauri app.

2. It also supports standalone mode: run bamboo separately on port 9562 and lotus
   independently for dev/debugging.

3. Internal/public build modes control whether a startup confirmation dialog appears.

4. The lotus frontend dist is resolved from multiple candidate paths (env var, config,
   .lotus-dist dir, macOS app bundle layout).

5. Version: 2026.4.24, actively tagged (latest tag: app-v2026.5.5), CI via GitHub Actions.

== Related repos (sibling directories expected) ==

  ../bamboo  -- the core Rust agent runtime (patched via Cargo.toml for local dev)
  ../lotus   -- the React frontend
