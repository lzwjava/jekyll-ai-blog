---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Git 文件自动补全
translated: true
type: note
---

Question: 我们可以使用 `git ls-files` 来获取自动排除 `.gitignore` 条目的文件列表，用作 `@` 提及自动补全的来源吗？

Answer:

是的 — `git ls-files` 正是这里正确的工具。它原生尊重 `.gitignore`，仅返回已跟踪/可跟踪的文件。这也是 Claude Code 内部所做的。

## 为什么 `git ls-files` 比 `glob` 更好

| Approach | Respects `.gitignore` | Fast | Handles nested ignores |
| --- | --- | --- | --- |
| `glob("**/*")` | ❌ | Slow on large repos | ❌ |
| Manual `.gitignore` parsing | Partial | Medium | Hard |
| `git ls-files` | ✅ | Fast | ✅ |

---

## 使用 `git ls-files` 的更新版 `AtFileCompleter`

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

## 每个 `git ls-files` 标志的作用

```bash
git ls-files --cached --others --exclude-standard
```

| Flag | What it includes |
| --- | --- |
| `--cached` | Files already tracked by git (committed or staged) |
| `--others` | New files not yet tracked (untracked) |
| `--exclude-standard` | Applies `.gitignore`, `.git/info/exclude`, and global gitignore |

没有 `--others`，您刚创建的全新文件在 `git add` 之前不会出现。通常您需要两者。

---

## 可选：文件变更时的缓存失效

如果您希望文件列表在文件变更时刷新（例如用户在会话中创建新文件），可以在每次 `@` 触发时强制刷新：

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

对于大多数仓库（< 10,000 个文件），`git ls-files` 在 50ms 以内完成，因此这没问题。

---

## 总结

用 `git ls-files --cached --others --exclude-standard` 替换您的 `glob` 方法 — 它通过一次 subprocess 调用为您提供干净的、感知 `.gitignore` 的文件列表。在内存中缓存结果，并在每次 `@` 触发时可选刷新。这正好匹配 Claude Code 如何相对于仓库根目录解析其文件提及列表。

**参考资料：**

- [git ls-files documentation](https://git-scm.com/docs/git-ls-files)
- [prompt_toolkit Completer API](https://python-prompt-toolkit.readthedocs.io/en/master/pages/reference.html#prompt_toolkit.completion.Completer)
