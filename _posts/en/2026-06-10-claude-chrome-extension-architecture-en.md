---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Chrome Extension Architecture
translated: false
type: note
---

**Question:** How does Claude in Chrome work internally — is it built on existing "browser use" tech (Playwright, browser-use, CDP)?

**Answer:**

Yes and no. It's the same *category* of tech as browser-use/Playwright MCP — an LLM tool-use loop driving a browser — but it's not built on Playwright or the `browser-use` library. It's a native Chrome extension that talks **Chrome DevTools Protocol (CDP) directly via the `chrome.debugger` API**, plus injected content scripts. No external driver process, no separate browser instance — it attaches to *your* running Chrome profile.

## The core loop

It's the vanilla Anthropic agentic loop. The extension builds a system prompt (server config + platform + tab context + domain skills), resolves available tools for the current page type, streams a claude-sonnet-4-5 response, executes any tool_use blocks, feeds results back, and loops until Claude returns a response with no tool calls — then detaches the CDP debugger from all tabs. During execution it continuously hits the official `/v1/messages` endpoint — same API you use. In ~30 lines, the shape is:

```python
import anthropic

client = anthropic.Anthropic()
messages = [{"role": "user", "content": task}]

while True:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=10000,
        system=build_system_prompt(tab_context, domain_skills),
        tools=[read_page, find, computer, form_input, javascript_tool, ...],
        messages=messages,
    )
    tool_uses = [b for b in resp.content if b.type == "tool_use"]
    if not tool_uses:
        break  # done — detach debugger
    messages.append({"role": "assistant", "content": resp.content})
    messages.append({"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": t.id,
         "content": execute_in_browser(t.name, t.input)}  # ← CDP / content script
        for t in tool_uses
    ]})
```

The only novel part is `execute_in_browser` — *how* tools are grounded in the page.

## Perception: accessibility tree first, pixels second

The extension uses two modes to understand pages: the page's accessibility tree, and screenshots when the a11y tree can't achieve the goal. The accessibility tree is the structure browsers build for screen readers — semantic info about interactive elements: roles (button, link, input), names, descriptions, states.

Concretely, the `read_page` tool injects a `window.__generateAccessibilityTree(filter, depth, maxChars, refId)` function via `chrome.scripting.executeScript`, which walks the DOM recursively (default depth 15) and maps elements to ARIA roles. It supports a filter ('interactive' for buttons/links/inputs only, or 'all'), a `ref_id` to scope reads to a subtree, and caps output at 50,000 characters. Each element gets a `ref_N` handle the model uses in subsequent click/type calls — the same ref-based grounding pattern as Playwright MCP's `browser_snapshot`, but homegrown rather than using Playwright's ariaSnapshot.

Why a11y tree over screenshots? Tokens. Text-structured roles+names compress a page ~10–50x vs vision, and refs are exact (no coordinate regression). The downside is documented in the reverse-engineering writeups: the full a11y tree on long pages explodes context, and screenshot fallbacks (100–500 KB each) persist across turns, making long tasks slow and expensive.

## Action: CDP via chrome.debugger

This is the interesting privilege layer. Unlike standard extensions that rely on high-level DOM APIs, the extension leverages the `chrome.debugger` API, giving it direct access to the Chrome DevTools Protocol. Through CDP it can synthesize "trusted" user events (clicks, keystrokes) indistinguishable from human hardware input, read network requests, console logs, and the raw accessibility tree, and inject arbitrary JavaScript into any open page.

The "trusted events" point matters: a plain `element.dispatchEvent(new MouseEvent('click'))` from a content script produces `isTrusted: false` events that many sites (React synthetic event guards, bot detection, payment iframes) ignore. CDP's `Input.dispatchMouseEvent` / `Input.dispatchKeyEvent` go through the browser's input pipeline, so they're `isTrusted: true` — same trick Playwright and Puppeteer use, just accessed from inside an extension instead of an external WebSocket connection to a `--remote-debugging-port`.

One practical consequence: all operations depend on the debugger permission, and when the debugger is attached, the browser shows the debugging banner and the tab grabs focus — so "background operation" is leaky in practice. You've seen the yellow "Claude is debugging this browser" bar — that's `chrome.debugger.attach()`.

## Stack comparison

| | Claude in Chrome | browser-use / Playwright MCP | OpenAI Operator-style |
| --- | --- | --- | --- |
| Browser | **your** Chrome profile (extension) | separate Playwright-launched browser | cloud VM browser |
| Transport | `chrome.debugger` → CDP in-process | WebSocket → CDP via Playwright | vision + VNC-ish |
| Perception | custom a11y tree walker (`ref_N`) + screenshot fallback | ariaSnapshot / DOM extraction | screenshots primarily |
| Auth | free — inherits your logged-in sessions | must replay cookies/login | re-login in VM |
| Claude Code bridge | native messaging host (stdio JSON) → extension | n/a | n/a |

So the honest answer to "is it using some browser use tech": it independently implements the same three primitives every browser agent converges on — **(1)** an a11y-tree/DOM serialization for cheap perception, **(2)** CDP for trusted input + console/network introspection, **(3)** a tool-use loop against `/v1/messages` — but packaged as an extension so it rides your real session instead of a sandboxed browser. That session-inheritance is both the killer feature (no auth plumbing) and the reason for the heavy permission prompts and prompt-injection guardrails.

If you want to study a working reimplementation of the loop at nano-scale, the `browser-use` repo (Python, ~CDP via Playwright) is the nanoGPT of this space — read its DOM serializer and compare it to the `read_page` schema in the gist below; the convergent design will be obvious.

**References:**

- [Claude for Chrome Extension Internals (v1.0.56) — sshh12 gist](https://gist.github.com/sshh12/e352c053627ccbe1636781f73d6d715b)
- [The Cyborg Session: Reversing & Detecting Claude AI Agent Chrome Extension — CHEQ](https://cheq.ai/blog/the-cyborg-session-reversing-detecting-claude-ai-agent-chrome-extension/)
- [How Claude in Chrome Works — reverse-engineering writeup](https://medium.com/@buttercanbentley/how-claude-in-chrome-works-45b86b06f689)
- [Use Claude Code with Chrome (beta) — Claude Code Docs](https://code.claude.com/docs/en/chrome)
