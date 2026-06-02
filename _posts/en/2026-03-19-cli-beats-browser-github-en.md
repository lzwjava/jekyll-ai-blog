---
audio: false
generated: true
image: false
lang: en
layout: post
title: CLI Beats Browser for GitHub Actions
translated: false
type: note
---

Question: Is using Claude Code CLI easier than clicking in a browser to trigger GitHub Actions workflows?

Answer:

Yes, absolutely. Using Claude Code (or any CLI approach) to trigger GitHub Actions workflows is significantly easier and more efficient than using the browser UI. Here's why:

## CLI vs Browser for GitHub Actions

### CLI Advantages

**Speed & Efficiency**
- One command to trigger: `gh workflow run gh-pages.yml`
- No page loading, navigation, or clicking through menus
- Instant feedback in your terminal

**Scriptable & Automatable**
- Can be chained with other commands
- Easy to loop, retry, or schedule
- Can be triggered from scripts or other tools like Claude Code

**Better Visibility**
- `gh run list` gives a clean, structured status view
- Can poll/watch runs programmatically
- Easier to pipe output into other tools

**Context Switching**
- Stay in your terminal — no need to open a browser
- Keeps your flow uninterrupted

---

### What Claude Code Adds on Top of Plain CLI

Claude Code can:
- **Intelligently decide *when* to trigger** a workflow (e.g., after a build succeeds)
- **Parse the run output** and react — like detecting `in_progress` vs `pending` vs `success`
- **Chain actions** — trigger → wait → check result → act on failure
- **Handle concurrency logic** — as seen in your example, it detected the `cancel-in-progress` behavior automatically

---

### From Your Example

Claude Code correctly:
1. Triggered `gh workflow run gh-pages.yml`
2. Verified the new run appeared as `pending` (`23255811075`)
3. Detected a concurrent scheduled run was `in_progress`
4. Reasoned about the `cancel-in-progress` concurrency setting
5. Re-ran when needed and confirmed `success`

That level of **observe → reason → act** is exactly what makes Claude Code more powerful than just clicking a button in the GitHub UI.

---

### Quick Reference

| Action | Browser | CLI (`gh`) | Claude Code |
|---|---|---|---|
| Trigger workflow | 4–5 clicks | 1 command | Automatic |
| Check status | Refresh page | `gh run list` | Automatic |
| React to result | Manual | Scripted | Intelligent |
| Handle concurrency | Manual check | Manual check | Reasoned |

**Bottom line:** CLI beats browser for repeatability; Claude Code beats plain CLI for intelligence.
