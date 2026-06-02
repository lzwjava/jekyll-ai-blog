---
audio: false
generated: true
image: false
lang: en
layout: post
title: At Mention Autocomplete in Python
translated: false
type: note
---


**Question:** How do Claude Code and OpenAI Codex implement the `@` symbol file mention with an autocomplete dropdown, and how can I replicate this in Python since my current `readline`-based approach seems limited?

**Answer:**

## Why Your `readline` Approach Feels Hard

Your current code uses Python's `readline` module with `tab: complete`, which only handles **Tab-key triggered completion at word boundaries**. It has no concept of:

- Watching for a specific trigger character like `@`
- Showing a **popup dropdown menu** inline
- Doing fuzzy/partial file path matching mid-sentence

This is the core limitation — `readline` was designed for shell-style completion, not rich in-line mention triggers.

---

## How Claude Code Does It

Claude Code is a Node.js/TypeScript TUI application. Its `@` autocomplete is implemented using a Rust-based fuzzy finder in the core engine, not a simple readline hook. Key behaviors observed from its issue tracker:

- The autocomplete scans files relative to the git repository root, not just the current working directory.
- The `@` character triggers a dropdown that suggests files as you type — this is a full TUI popup rendered by the terminal UI layer.
- In VS Code, pressing `Option+K` / `Alt+K` inserts an `@`-mention with file path and line numbers, e.g. `@app.ts#5-10`.

The key architectural point: Claude Code renders its own terminal UI (like a mini-editor), so it has full control over every keystroke and can render popup menus without relying on the shell's readline.

---

## The Right Python Tool: `prompt_toolkit`

`prompt_toolkit` is a library for building powerful interactive command line and terminal applications in Python — it can be a very advanced pure Python replacement for GNU readline, and can also be used for building full screen applications.

Autocompletion can be added by passing a `completer` parameter — an instance of the `Completer` abstract base class — and `complete_while_typing=True` makes the dropdown appear automatically as you type, without needing Tab.

Here is a working implementation of `@`-triggered file autocomplete using `prompt_toolkit`:

```python
import os
import glob
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion

class AtFileCompleter(Completer):
    """Triggers file suggestions after @ character."""

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor

        # Find the last @ in the current input
        at_pos = text.rfind("@")
        if at_pos == -1:
            return  # No @ found, no completions

        # Everything after the @ is the file prefix to match
        prefix = text[at_pos + 1:]

        # Don't trigger if there's a space after @
        if " " in prefix:
            return

        # Glob for matching files
        pattern = f"{prefix}*"
        matches = glob.glob(pattern) + glob.glob(os.path.join("**", pattern), recursive=True)

        seen = set()
        for path in sorted(matches)[:20]:  # limit to 20 results
            if path in seen:
                continue
            seen.add(path)
            # Completion replaces only the text after @
            yield Completion(
                path,
                start_position=-len(prefix),
                display=path,
                display_meta="file" if os.path.isfile(path) else "dir"
            )

def main():
    session = PromptSession(
        completer=AtFileCompleter(),
        complete_while_typing=True,   # popup appears as you type, no Tab needed
    )

    messages = []
    print("Type your message. Use @filename to reference files.\n")

    while True:
        try:
            user_input = session.prompt("> ")
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.strip() == ".exit":
            break

        # TODO: parse @mentions out of user_input before sending to LLM
        messages.append({"role": "user", "content": user_input})
        print(f"[Sending: {user_input}]\n")

if __name__ == "__main__":
    main()
```

---

## Key Concepts Explained

| Concept | `readline` | `prompt_toolkit` |
|---|---|---|
| Trigger character | Tab only | Any character (`@`, `/`, etc.) |
| Popup dropdown | No | Yes, rendered inline |
| Fuzzy matching | No | Yes (via `FuzzyCompleter` wrapper) |
| Complete while typing | No | Yes (`complete_while_typing=True`) |
| Cross-platform | macOS/Linux only | Windows + macOS + Linux |
| Multiline input | Hard | Built-in |

---

## Parsing `@mentions` After Input

Once the user submits their message, you need to extract the file references and inject content:

```python
import re

def resolve_at_mentions(text):
    """Find all @file references and return (cleaned_text, file_contents_dict)."""
    mentions = re.findall(r"@(\S+)", text)
    file_contents = {}
    for path in mentions:
        if os.path.isfile(path):
            with open(path) as f:
                file_contents[path] = f.read()
    return text, file_contents
```

You would then prepend the file contents to your LLM message context, exactly like Claude Code does when it resolves `@` mentions before sending to the API.

---

## Summary

The reason Claude Code's `@` mention UX feels polished is because it builds its own **TUI layer** (using Rust/Ink in Node.js) rather than relying on the shell's readline. In Python, `prompt_toolkit` gives you the same capability — trigger-character-aware completions, dropdown menus, fuzzy matching, and cross-platform support — and is the standard library used by tools like IPython, pgcli, and mycli for exactly this kind of rich terminal autocomplete.

**References:**

- [prompt_toolkit documentation – Asking for input](https://python-prompt-toolkit.readthedocs.io/en/master/pages/asking_for_input.html)
- [prompt_toolkit on PyPI](https://pypi.org/project/prompt-toolkit/)
- [Claude Code @ autocomplete – GitHub Issues](https://github.com/anthropics/claude-code/issues/1818)
- [Claude Code VS Code Extension Docs](https://code.claude.com/docs/en/vs-code)
