---
audio: false
generated: true
image: false
lang: en
layout: post
title: Browser Tools Architecture in Hermes Agent
translated: false
type: note
---

Here's how the browser tools work in Hermes Agent. The code is at:

    ~/.hermes/hermes-agent/tools/browser_tool.py  (~3,863 lines)

Architecture summary:

1. AGENT-BROWSER CLI (the core engine)
   The Python code doesn't use Playwright/Puppeteer directly. Instead it shells out to
   an npm package called `agent-browser` — a Rust CLI that wraps Playwright/Chromium.
   Every browser action is a subprocess call:

     agent-browser [--cdp <ws_url> | --session <name>] [--json] <command> [args...]

   Commands: open, click, fill, scroll, snapshot, screenshot, eval, press, close, etc.

2. THREE BACKENDS (auto-detected)

   a) LOCAL headless Chromium (default, zero-cost)
      - Uses `--session <name>` flag
      - agent-browser launches/manages a local Chromium daemon
      - Requires: `npx agent-browser install` (downloads Chromium)

   b) CLOUD providers (Browserbase, Browser Use, Firecrawl)
      - Uses `--cdp <websocket_url>` flag to connect to a remote browser
      - Providers live under plugins/browser/<vendor>/provider.py
      - Auto-detect order: Browser Use → Browserbase
      - Config: browser.cloud_provider in config.yaml

   c) Camofox (anti-detection local browser)
      - When CAMOFOX_URL env is set, routes through a REST API instead
      - Imported from tools/browser_camofox.py

3. SESSION MANAGEMENT
   - _get_session_info(task_id) creates/reuses sessions
   - Each task_id gets its own socket directory under /tmp
   - Owner PID tracking for orphan cleanup
   - Inactivity timeout: daemon self-terminates after idle period
   - AGENT_BROWSER_SOCKET_DIR isolates concurrent sessions

4. ELEMENT REFERENCES (@e1, @e2, etc.)
   - `browser_snapshot` calls `agent-browser snapshot` which returns an
     accessibility tree (ariaSnapshot) — text-based DOM representation
   - Each interactive element gets a ref ID (@e1, @e2, ...)
   - `browser_click(@e5)` → `agent-browser click @e5`
   - `browser_type(@e3, "text")` → `agent-browser fill @e3 "text"`

5. EXECUTION FLOW (the key function)
   _run_browser_command(task_id, command, args) at line 1875:
   - Finds agent-browser binary via _find_agent_browser()
   - Gets/creates session via _get_session_info()
   - Builds: [agent-browser, --cdp/--session, ..., --json, command, args]
   - Runs as subprocess with temp-file stdout/stderr (avoids pipe hangs
     from the daemon inheriting fds)
   - Parses JSON output, handles timeouts (default 30s)
   - Falls back to Lightpanda→Chrome if engine mismatch

6. SECURITY LAYERS
   - SSRF protection: blocks private/internal URLs in cloud mode
   - Secret exfiltration: blocks URLs containing API keys/tokens
   - Website policy: configurable allow/block lists
   - Cloud metadata endpoints always blocked (169.254.169.254 etc.)
   - Post-redirect checks: if redirect lands on blocked URL, navigates away

7. HYBRID ROUTING
   - browser.auto_local_for_private_urls (default true)
   - Cloud provider handles public URLs, local Chromium handles LAN/localhost
   - Keyed by _navigation_session_key(task_id, url)

8. CDP SUPERVISOR
   - browser_supervisor.py monitors dialogs (alert/confirm/prompt)
   - Attaches to CDP endpoint, auto-accepts/dismisses based on policy
   - Config: browser.dialog_policy, browser.dialog_timeout_s

The whole thing is ~4K lines of Python orchestrating a Rust CLI binary that manages Chromium instances — local or remote — with session isolation, security guards, and multi-backend fallbacks.
