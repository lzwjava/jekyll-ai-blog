---
audio: false
generated: true
image: false
lang: en
layout: post
title: Browser Tools in Hermes Agent
translated: false
type: note
---

The browser tools I'm using are built into Hermes Agent (the CLI AI agent you're talking to). Here's how it works:

**Stack:**

- **Browserbase** — the underlying headless browser infrastructure (cloud-hosted Chromium instances). It's stealth-capable (though running without residential proxies in this case).
- The tools are exposed as functions I can call in sequence:

| Tool | What it does |
|------|-------------|
| `browser_navigate(url)` | Opens a page, initializes the session |
| `browser_snapshot()` | Reads the DOM/accessibility tree — returns element refs like `@e1`, `@e2` |
| `browser_click(ref)` | Clicks an element by ref |
| `browser_type(ref, text)` | Types into an input field by ref |
| `browser_press(key)` | Keyboard keys (Enter, Tab, Escape) |
| `browser_scroll(direction)` | Scroll up/down |
| `browser_console(expression)` | Execute JS in the page context, read results |
| `browser_vision(question)` | Screenshot + visual analysis (native vision or fallback model) |
| `browser_back()` | Navigate back |

**Workflow for this login attempt:**

1. `browser_navigate` → loaded `http://192.168.22.1`, got the form structure with ref IDs
2. `browser_type(@e1, "admin")` → filled username
3. `browser_type(@e2, "admin")` → filled password
4. `browser_click(@e3)` → clicked "登录" button
5. Checked result with `browser_snapshot()` and `browser_console()` to read JS state
6. After 3 failed combos, `browser_vision()` → took a screenshot to read the Chinese error message

**Key detail:** The `dosubmit()` JS function Base64-encodes the password before POSTing, so I could also call it directly via `browser_console` to manipulate the form programmatically rather than clicking.

It's essentially a remote-controlled Chromium — think Playwright/Puppeteer but cloud-hosted and accessible as tool calls from the CLI agent.
