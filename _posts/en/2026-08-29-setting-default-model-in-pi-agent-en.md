---
audio: false
generated: true
image: false
lang: en
layout: post
title: Setting Default Model in Pi Agent
translated: false
type: note
---

**Question:** How do you set the default model in Pi agent (pi.dev coding agent)?

**Answer:**

Pi agent (the open-source coding agent at pi.dev / earendil-works/pi) stores its default model in `settings.json`. There are three ways to set it:

---

**Method 1 — Interactive (recommended for beginners)**

Use `/model` in Pi's interactive mode and press **Ctrl+S** on the desired model to save it as the startup default. Similarly, use `/thinking` and press **Ctrl+S** to save the default thinking level.

---

**Method 2 — Edit `settings.json` directly**

The global settings file is located at `~/.pi/agent/settings.json` and applies to all agent sessions. The project-scoped settings file is at `.pi/settings.json` within your current working directory.

The relevant fields are `defaultProvider` (e.g. `"anthropic"`, `"openai"`) and `defaultModel` (the model ID string). You can also set `defaultThinkingLevel` to values like `"off"`, `"low"`, `"medium"`, `"high"`, `"max"`.

Example:

```json
{
  "defaultProvider": "anthropic",
  "defaultModel": "claude-opus-4-8",
  "defaultThinkingLevel": "medium"
}
```

---

**Method 3 — Set subagent model defaults (for agent teams)**

You can control the model for subagents separately using `subagents.defaultModel`, and pin individual agents by name using `subagents.agentOverrides`. The precedence order (strongest first) is: per-run override → agent frontmatter model → `agentOverrides.<name>.model` → `subagents.defaultModel` → the parent session model.

Example:

```json
{
  "defaultModel": "claude-opus-4-8",
  "subagents": {
    "defaultModel": "claude-sonnet-4-6",
    "agentOverrides": {
      "reviewer": {
        "model": "claude-opus-4-8",
        "thinking": "high"
      }
    }
  }
}
```

---

**References:**
- [Pi Settings Docs (official)](https://pi.dev/docs/latest/settings)
- [earendil-works/pi — settings.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/settings.md)
- [pi-subagents — models.md](https://github.com/nicobailon/pi-subagents/blob/main/docs/models.md)
