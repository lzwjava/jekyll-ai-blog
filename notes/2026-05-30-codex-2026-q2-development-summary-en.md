---
audio: false
generated: true
image: false
lang: en
layout: post
title: Codex 2026 Q2 Development Summary
translated: false
type: note
---

Here's a comprehensive breakdown of Codex updates over the past ~3 months (March–May 2026), based on 146 commits:

---

## 1. Extension System (`codex-rs/ext/`)

The biggest architectural shift — Codex now has a formal extension framework with 6 extensions:

```
ext/
├── extension-api/    # Contributor/registry system
├── goal/             # Goal steering, accounting, usage limits
├── guardian/         # Safety review with prompt caching
├── image-generation/ # Standalone image gen via native pipeline
├── memories/         # Dedicated SQLite memory store
└── web-search/       # Standalone web.run search tool
```

Key commits:
- **Standalone web search extension** (a22706d) — new `web.run` tool that calls `codex-api` search client directly, hides hosted `web_search` when standalone is enabled
- **Standalone image generation** (ecb41fc, 10b0399) — feature-gated extension routing through native image completion pipeline
- **Goal extension** — steering via `inject_if_running`, usage limits (bc00502), telemetry parity, thread eligibility gating
- **Guardian** — 9 commits stabilizing prompt cache key handling, review metrics, and cache reuse across sessions

---

## 2. Thread/Lifecycle Model

Major rework of how threads and sessions work:

- **Thread idle lifecycle hook** (d2ebb8d) — new `thread-idle` contributor
- **Wire task completion into thread-idle** (462deb0)
- **Durable session interface** (c9dc0f6) — code-mode introduces persistence
- **Thread resume with turns page** (2a1158b) — app-server includes turn history on resume
- **Forked thread lineage** (1911021) — `forked_from_thread_id` metadata
- **Subagent lineage metadata** (fc9cf62) — tracks agent ancestry in Responses API
- **Permission profiles stored per thread** (a1ecf0c)
- **Seed prompt history from resumed messages** (56958f2)

---

## 3. Python SDK (Beta)

The Python SDK hit beta (`python-v0.1.0b1`, `python-v0.1.0b2`):

- Independent beta release pipeline (4d0c4cd)
- Sandbox presets (b1cbf62) — friendly defaults
- Renamed `AppServerConfig` → `CodexConfig` (0db49a7)
- Documentation and metadata cleanup
- `codex app-server --stdio` alias (b90ec46) for SDK consumers

---

## 4. TUI Improvements

- **Markdown table rendering** — app-style tables (6b4b15a) + cramped tables as key-value records (26c9502)
- **OSC 8 web links** (7a26497) — clickable hyperlinks in terminal
- **Vim text objects** (8d398d3) — `iw`, `aw`, etc.
- **Configurable turn interruption keybind** (2d1ad37)
- **Unified mentions** (6c1215d) — polished @mention rendering
- **Named permission profile picker** (f6fd753)
- **Multiline hook output** (251b241)
- **`/archive` slash command** (36cd366)

---

## 5. Windows Sandbox

Active development on Windows sandbox support:

- Provisioning setup command (cb9178e)
- Workspace roots passed to runner (986c604)
- Network denial cancellation fix (3cf737e)
- Capture cancellation test roots (bcf2b55)
- Removed old SandboxPolicy plumbing (0a6bc4e)

---

## 6. Cleanup / Retirements

- **debug-client fully removed** — 8 commits deleting the entire CLI, JSONL helper, event reader, manifest, README, and plumbing
- Removed Bedrock OSS models from catalog (0a8c835)
- Removed redundant SQLite dynamic tool storage (24819)
- Moved memory to dedicated SQLite DB (aad59a0)
- Rust toolchain uprevved to 1.95.0 (cca1e0b)
- SQLx bumped for newer bundled SQLite (379511d)

---

## 7. Security & Sandboxing

- Deny-read sandboxing preserved for safe commands (6e10142)
- Unix socket permissions set to deny (bf72be5)
- WebSocket Origin header rejection (a027135)
- `/diff` prevented from repository-configured code execution (2e0c4f4)
- `exec-server` CoreFoundation env preservation (a717e4e)

---

## 8. App-Server Protocol

- Remote control migrated to server tokens (912d7d4)
- Model tool mode selector (5577a9e)
- Tool UI visibility meta (577ec03)
- Startup benchmark crate (bd2a732, then reverted)
- Extension TurnItemEmitter for tool calls (2066874)

---

**TL;DR**: The biggest story is the **extension system** (goal, guardian, image-gen, web-search, memories) — Codex is moving from monolithic core to a plugin architecture. The **Python SDK beta** is shipping. The **thread lifecycle model** got a major rework with idle hooks, resume semantics, and fork lineage. TUI got significant UX polish. Windows sandbox is actively being built out. The old debug-client was fully retired.