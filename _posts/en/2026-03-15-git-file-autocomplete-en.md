---
audio: false
generated: true
image: false
lang: en
layout: post
title: Git for File Autocomplete
translated: false
type: note
---

Question: Can we use `git ls-files` to get a file list that automatically excludes `.gitignore` entries, to use as the source for `@` mention autocomplete?

Answer:

Yes — `git ls-files` is exactly the right tool here. It natively respects `.gitignore` and only returns tracked/trackable files. This is also what Claude Code does internally.

## Why `git ls-files` is Better Than `glob`

| Approach | Respects `.gitignore` | Fast | Handles nested ignores |
| --- | --- | --- | --- |
| `glob("**/*")` | ❌ | Slow on large repos | ❌ |
| Manual `.gitignore` parsing | Partial | Medium | Hard |
| `git ls-files` | ✅ | Fast | ✅ |

---

## Updated `AtFileCompleter` Using `git ls-files`

```python
import subprocess
import os
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion

def get_git_files():
    """Return all files tracked or untracked-but-not-ignored by git."""
    try:
        # --cached      = tracked files (staged/committed)
        # --others      = untracked files
        # --exclude-standard = respect .gitignore, .git/info/exclude, etc.
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.splitlines()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return []


# Cache file list — refresh only when needed
_file_cache = None

def get_cached_files(force_refresh=False):
    global _file_cache
    if _file_cache is None or force_refresh:
        _file_cache = get_git_files()
    return _file_cache


class AtFileCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        at_pos = text.rfind("@")
        if at_pos == -1:
            return

        prefix = text[at_pos + 1:]
        if " " in prefix:
            return

        all_files = get_cached_files()

        for path in all_files:
            if prefix.lower() in path.lower():  # fuzzy substring match
                meta = "dir" if os.path.isdir(path) else "file"
                yield Completion(
                    path,
                    start_position=-len(prefix),
                    display=path,
                    display_meta=meta,
                )


def main():
    session = PromptSession(
        completer=AtFileCompleter(),
        complete_while_typing=True,
    )
    print("Type your message. Use @filename to reference files.\n")
    while True:
        try:
            user_input = session.prompt("> ")
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.strip() == ".exit":
            break
        print(f"[You said]: {user_input}\n")


if __name__ == "__main__":
    main()
```

---

## What Each `git ls-files` Flag Does

```bash
git ls-files --cached --others --exclude-standard
```

| Flag | What it includes |
| --- | --- |
| `--cached` | Files already tracked by git (committed or staged) |
| `--others` | New files not yet tracked (untracked) |
| `--exclude-standard` | Applies `.gitignore`, `.git/info/exclude`, and global gitignore |

Without `--others`, brand-new files you just created won't appear until you `git add` them. Usually you want both.

---

## Optional: Cache Invalidation on File Change

If you want the list to refresh when files change (e.g. user creates a new file mid-session), you can force refresh on each `@` trigger:

```python
class AtFileCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        at_pos = text.rfind("@")
        if at_pos == -1:
            return

        prefix = text[at_pos + 1:]
        if " " in prefix:
            return

        # Force refresh each time @ is triggered (slightly slower but always fresh)
        all_files = get_cached_files(force_refresh=True)

        for path in all_files:
            if prefix.lower() in path.lower():
                yield Completion(path, start_position=-len(prefix))
```

For most repos (< 10,000 files) `git ls-files` completes in under 50ms so this is fine.

---

## Summary

Replace your `glob` approach with `git ls-files --cached --others --exclude-standard` — it gives you a clean, `.gitignore`-aware file list in one subprocess call. Cache the result in memory and optionally refresh on each `@` trigger. This matches exactly how Claude Code resolves its file mention list relative to the repo root.

**References:**

- [git ls-files documentation](https://git-scm.com/docs/git-ls-files)
- [prompt_toolkit Completer API](https://python-prompt-toolkit.readthedocs.io/en/master/pages/reference.html#prompt_toolkit.completion.Completer)
