---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Note Plugin Without Source Changes
translated: false
type: note
---

Clean — no source changes. Here's the summary:

---

**You're right — the plugin approach is the correct way.** I reverted the source changes. Here's what was built instead:

**Files created (no source modifications needed):**

```
~/.hermes/plugins/note/
├── plugin.yaml          # manifest
└── __init__.py          # registers /note via ctx.register_command()
```

**Config change:**

```
~/.hermes/config.yaml — added "note" to plugins.enabled
```

**How it works:**

The plugin uses the official `ctx.register_command()` API (line 412 in `hermes_cli/plugins.py`). It:

1. Gets conversation history from `ctx._manager._cli_ref` (the CLI instance)
2. Extracts the last assistant response (handles string or OpenAI multi-part content)
3. Strips reasoning tags (``)
4. Calls `ww`'s `create_note_from_content()` to create the markdown note with front matter

**Usage:**

```
/note                              # save last response, LLM generates title
/note --title "My Title"           # skip LLM title generation
/note --dir ~/my-notes             # custom output directory
/note 3                            # save 3rd assistant response
/note 2 --title "Foo" --dir ~/notes
```

**Why this is better than editing source:**

- `hermes update` won't break it — plugins survive upgrades
- Official API — `ctx.register_command()` is designed for exactly this
- Portable — copy `~/.hermes/plugins/note/` to any machine
- No recompilation — just restart Hermes

**To activate:** restart Hermes. The plugin auto-loads because `note` is in `plugins.enabled`.
