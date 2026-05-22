---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diagnosing a Stuck Plugin Issue
translated: false
type: note
---

Now I have the full picture. Here's the diagnosis:

---

## Root Cause: `/note` Gets Stuck

The `/note` plugin calls `create_note_from_content()` which makes a **synchronous HTTP request** to OpenRouter with **no timeout**. Here's the exact call chain:

```
/note
  → _handle_note()
    → create_note_from_content()
      → _generate_titles()
        → generate_title()
          → _call_llm_or_exit()
            → call_openrouter_api()
              → requests.post(url, headers, json, data)  ← NO TIMEOUT
```

### Problem 1: No HTTP timeout (the main "stuck" cause)

In `~/projects/ww/ww/llm/openrouter_client.py` line 53:

```python
response = requests.post(url, headers=headers, json=data)
#                          ^^^ no timeout parameter!
```

If OpenRouter is slow, rate-limited, or the network drops, this blocks **forever**. The CLI is single-threaded, so the entire UI freezes.

### Problem 2: No user feedback

The plugin handler runs synchronously in `process_command()` (cli.py:8210-8211):

```python
result = resolve_plugin_command_result(
    plugin_handler(user_args)   # blocks here, no spinner, no progress
)
```

No spinner, no "Generating title..." message, nothing. The user stares at a blank prompt.

### Problem 3: Error log evidence

From `agent.log` at 01:14:43:

```
⚙️  /note [error] LLM call failed. Model: (not set), max_tokens: 300
```

The `MODEL` env var wasn't loaded. The `dotenv` load on line 69 of the plugin might be running but `override=False` means if Hermes already set `MODEL` in the process env, the `.env` value is skipped. Or the `.env` load fails silently.

### Problem 4: `sys.exit(1)` kills the CLI

In `create_note_utils.py` lines 53-56 and 61:

```python
if not content or not content.strip():
    print("Content is empty or invalid. Aborting.")
    sys.exit(1)  # KILLS the entire Hermes process!
```

If content is short or empty, `sys.exit(1)` terminates the whole CLI, not just the command.

---

## Fix

The quickest fix — add a timeout and a loading message. Edit `~/projects/ww/ww/llm/openrouter_client.py`:

```python
# Line 53: add timeout
response = requests.post(url, headers=headers, json=data, timeout=30)
```

And edit `~/.hermes/plugins/note/__init__.py` to add feedback and handle errors gracefully:

```python
# In _handle_note, before calling create_note_from_content:
print("Generating title via LLM...")

# Wrap in try/except instead of letting sys.exit kill the CLI
try:
    file_path = create_note_from_content(text, custom_title=title, directory=note_dir)
    return f"Note saved: {file_path}
```

Want me to apply these fixes?