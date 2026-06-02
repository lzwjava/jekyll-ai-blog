---
audio: false
generated: true
image: false
lang: en
layout: post
title: Setting Up CDP in AI Agents
translated: false
type: note
---

Question: How do I set up Chrome DevTools Protocol (CDP) in Claude Code or OpenClaw (AI agent)?

Answer:

## Overview

Both **Claude Code** and **OpenClaw** support Chrome DevTools Protocol (CDP) integration, letting your AI agent directly control a browser — navigating pages, clicking elements, capturing screenshots, monitoring network requests, and more. Here's a complete guide for both.

---

## Part 1: CDP Setup in Claude Code

### Method A — Official Chrome DevTools MCP Server (Recommended)

The `chrome-devtools-mcp` package lets your AI coding agent (Claude, Cursor, Copilot, etc.) control and inspect a live Chrome browser. It acts as a Model Context Protocol (MCP) server, giving your AI assistant access to Chrome DevTools for automation, debugging, and performance analysis.

**Step 1: Add the MCP server to Claude Code**

Run this command in your terminal:

```bash
claude mcp add -- chrome npx -y chrome-devtools-mcp@latest
```

Or, if you want to add it via the marketplace plugin system:

```
/plugin marketplace add ChromeDevTools/chrome-devtools-mcp
```

Then restart Claude Code.

**Step 2: Configure via `claude_desktop_config.json`**

Add the MCP server to your Claude Code configuration file at `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

**Step 3: Launch Chrome with Remote Debugging**

Chrome needs to be running with remote debugging enabled:

**macOS:**

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222
```

**Windows:**

```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

**Linux:**

```bash
google-chrome --remote-debugging-port=9222
```

### Method B — Using a Persistent Authenticated Profile

The standard Chrome DevTools MCP installation launches Chrome in a fresh, isolated profile. This works well for basic automation, but you can't use it with sites that require authentication. The key is Chrome's `--user-data-dir` flag — it creates a separate profile directory where Chrome saves all your login sessions, cookies, and browsing data.

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chrome-debug-profile"
```

Then configure the MCP to connect via `--browserUrl`:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--browserUrl", "http://localhost:9222"]
    }
  }
}
```

> ⚠️ **Security Note:** Opening the remote debugging port exposes your browser to any application on your machine. Use this setup only for development and testing. Don't browse sensitive sites in a Chrome instance with remote debugging enabled.

### Method C — cdp-cli (Lightweight Alternative)

Install a standalone CDP CLI tool as an alternative to MCP servers — you can see exactly what it's doing, and it saves tokens by not piping full DOM trees:

```bash
npm install -g @myerscarpenter/cdp-cli

# List open tabs
cdp-cli tabs

# Read console logs for a tab
cdp-cli console "GitHub" --tail 5

# Take a screenshot
cdp-cli screenshot "GitHub" --output screenshot.jpg
```

---

## Part 2: CDP Setup in OpenClaw

OpenClaw integrates Google's official Chrome DevTools MCP server, letting AI agents operate your Chrome browser directly — reading pages, clicking elements, filling forms, recording performance traces, and analyzing network requests, all through CDP.

OpenClaw offers **three browser control modes**:

### Mode 1 — OpenClaw Managed (Isolated, Default)

OpenClaw Managed (ports 18800–18899) provides isolated Chromium instances ideal for safe automation. This is the recommended starting point.

```bash
# Start the managed browser
openclaw browser start

# Check status
openclaw browser status

# Take a snapshot of the current page
openclaw browser snapshot --interactive --compact --depth 6

# Click an element by ref
openclaw browser click e12

# Type into a field
openclaw browser type e15 "your text"

# Screenshot
openclaw browser screenshot --full-page
```

### Mode 2 — Existing Session (Your Logged-in Chrome)

OpenClaw uses the official Chrome DevTools MCP `--autoConnect` flow for this. It attaches to your existing Chrome session (with your login state and cookies).

```bash
# Start using your existing Chrome profile
openclaw browser --browser-profile user start
```

> Note: This path is higher-risk than the isolated OpenClaw profile because it can act inside your signed-in browser session. OpenClaw does not launch the browser for this driver; it attaches to an existing session only.

### Mode 3 — Remote CDP (Cloud/External Browser)

For a remote headless Chromium, paste the following configuration into your `openclaw.json`:

```json
"browser": {
  "enabled": true,
  "attachOnly": true,
  "defaultProfile": "remote",
  "profiles": {
    "remote": {
      "cdpUrl": "http://your-browser-host:9222",
      "color": "#FF4500"
    }
  }
}
```

### Installing Playwright (Required for Advanced Features)

Some features (navigate, act, AI snapshot, role snapshot, element screenshots, PDF) require Playwright. If you see "Playwright is not available", install it:

```bash
npm install playwright
# Then restart the Gateway
```

---

## Quick Comparison Table

| Feature | Claude Code (MCP) | OpenClaw |
|---|---|---|
| Protocol | CDP via MCP | CDP via Playwright/Extension |
| Isolated browser | ✅ | ✅ (Managed mode) |
| Use existing login session | ✅ (with `--user-data-dir`) | ✅ (Existing-session mode) |
| Remote CDP | ✅ | ✅ |
| Screenshots | ✅ | ✅ |
| Element clicking | ✅ | ✅ |
| Auth support | Requires profile setup | Built-in via `user` profile |

References:

- [Chrome DevTools MCP — GitHub (Official)](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [OpenClaw Browser Docs](https://docs.openclaw.ai/tools/browser)
- [Setup Guide: Authenticated Chrome Debugging with Claude Code](https://raf.dev/blog/chrome-debugging-profile-mcp/)
- [cdp-cli for Claude Code](https://icepick.info/2025/10/28/chrome-devtools-cli-for-claude-code/)
- [OpenClaw + Chrome DevTools MCP Guide (Medium)](https://medium.com/@tentenco/openclaw-chrome-devtools-mcp-how-to-give-your-local-agent-full-browser-control-a4e7c723a649)
- [OpenClaw Browser Control Deep Dive](https://blog.laozhang.ai/en/posts/openclaw-browser-control)
