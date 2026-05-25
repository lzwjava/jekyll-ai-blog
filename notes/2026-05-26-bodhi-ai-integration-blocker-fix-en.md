---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bodhi AI Integration Blocker Fix
translated: false
type: note
---

Here's the full picture:
    
    == What Bodhi AI Is ==
    
    A Tauri 2 desktop AI agent workbench by bigduu. Three-layer architecture:
      bodhi  = Tauri shell (this repo, /Users/lzwjava/projects/Bodhi-AI)
      lotus  = React+Vite UI (submodule in zenith repo)
      bamboo = Rust agent runtime (crate: bamboo-agent, 747 deps, actix-web on port 9562)
    
    Features: agent loop with 28 tools, session management, memory/dream notebook, workflows, MCP integration, skills store, global shortcut (Cmd+Shift+Space).
    
    == What We Did ==
    
    1. Cloned zenith monorepo (git@github.com:bigduu/Zenith.git) -> ~/projects/zenith
    2. Initialized submodules (bamboo, lotus, bodhi, pavilion, bodhi-server)
    3. Symlinked ~/projects/lotus -> zenith/lotus, ~/projects/bamboo -> zenith/bamboo
    4. npm install in both Bodhi-AI and lotus
    5. First Rust build: 747 crates in 2m 05s
    6. App launched successfully - Tauri window opens, backend starts on 127.0.0.1:9562
    
    == Current Blocker: LLM Provider Config ==
    
    The app starts but agent chat fails. Two issues:
    
    1. Config overwrite: The app regenerates provider_instances on startup with a new UUID and resets to gemini type, ignoring our edits to config.json. Our OpenRouter config gets clobbered.
    
    2. Gemini API rejection: Even when Gemini was configured, Google's API rejects bamboo's tool definitions because they include additionalProperties in JSON Schema, which Gemini doesn't support.
    
    Config location: ~/.bamboo/config.json
    Data dir: ~/.bamboo/ (sessions, skills, logs, metrics.db)
    
    == What Needs Fixing ==
    
    Option A: Fix bamboo's Gemini provider to strip additionalProperties before sending to Google API (code change in provider_factory.rs or Gemini provider)
    
    Option B: Figure out why config.json gets overwritten on startup and prevent it, so OpenRouter config persists
    
    Option C: Configure the provider through the Bodhi AI UI settings (if the setup wizard writes config correctly)
    
    The app itself is fully built and runnable — it's just the LLM integration that needs a working provider config.