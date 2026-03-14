---
audio: false
generated: true
image: false
lang: en
layout: post
title: Auto Expand OpenClaw Tool Outputs
translated: false
type: note
---

**Question:** How to make OpenClaw automatically expand tool outputs instead of requiring clicking one by one?

**Answer:** 

OpenClaw (the open-source personal AI assistant framework) does not currently have a built-in global setting to automatically expand all tool output sections in the UI by default. Tool results (especially longer ones from commands like `exec`, `browser`, file reads, etc.) are typically shown collapsed to keep the chat clean, and you need to click each one individually to view the full content.

Here are the practical workarounds and options based on the current version (as of March 2026):

1. **Use the TUI (Terminal User Interface) instead of Web UI**  
   The terminal interface (`openclaw tui` or `openclaw tui chat`) usually shows tool outputs fully expanded or in a more scrollable/readable format without collapse behavior.  
   Many users prefer it for heavy tool usage because it avoids the click-to-expand annoyance completely.  
   Run it like this:
   ```
   openclaw tui chat
   ```
   or start chatting directly in terminal mode.

2. **Ask the agent to summarize or inline important parts**  
   Add instructions in your prompt or in `AGENTS.md` / `SOUL.md` to force the agent to include key parts of tool results directly in the message instead of relying on collapsible blocks.  
   Example prompt additions:
   - "Always inline the most important 10–20 lines of tool output directly in your reply. Do not rely only on the collapsed tool card."
   - "For every tool call result, show a concise summary + the full relevant output without requiring expansion."

   This does not expand the UI card but makes the information visible without clicking.

3. **Check for UI improvements in latest release**  
   Recent releases (e.g., 2026.3.13) added auto-expand behavior for the chat compose textarea, showing the team is working on better UX.  
   There is no specific "auto-expand tool outputs" feature yet, but watch GitHub releases or run `openclaw update` frequently — this kind of improvement could arrive in a near-future patch.

4. **Custom theme / browser extension / userscript (advanced)**  
   If you're using the web UI:
   - Write a small browser userscript/tampermonkey script that automatically clicks expand buttons on tool cards when the page loads or mutates.
   - Or use dev tools to override CSS (e.g. remove `display: none` or `max-height` on collapsed sections).

   This is unofficial and fragile across updates.

5. **Request the feature**  
   The project is very active on GitHub (https://github.com/openclaw/openclaw).  
   Open an issue or +1 an existing one requesting "auto-expand tool output cards" or "persistent expanded state for tool results in web UI". The maintainers have been responsive to UX feedback.

**Short answer:** There is no direct config/flag for this right now — switch to the TUI for the best experience, or prompt the agent to inline more content.

**References:**  

- [https://github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- [https://docs.openclaw.ai/tools](https://docs.openclaw.ai/tools)
- [https://github.com/openclaw/openclaw/releases](https://github.com/openclaw/openclaw/releases)