---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Claude Code: Root Directory Tradeoffs"
translated: false
type: note
---

Question: When using Claude Code launched from the root directory (`/`), can you use `@` to reference files across all projects without copying paths? And will running it from `/` be slow?

Answer:

Yes, your intuition is correct — and there are real tradeoffs to understand.

## How `@` Works in Claude Code

When you use `@` to reference a file in a prompt, Claude Code includes the file's content directly into the conversation context. File paths can be relative or absolute, and you can use **tab-completion** after typing `@` to quickly navigate and select files without typing full paths.

The `@` reference syntax allows you to quickly add a file's content to the context without Claude having to find and read the file itself, which usually takes longer than explicit referencing.

So yes — if you launch from `/`, you *can* `@` any file on the system with tab-completion. You won't need to copy paths from outside.

## Will Running from `/` Be Slow?

**Short answer: Yes, noticeably so.** Here's why:

### 1. `@` Autocomplete Uses ripgrep to Scan the Directory

If `@` file mentions aren't finding files, the bundled ripgrep binary may be the culprit. Claude Code uses ripgrep to power file search and `@` autocomplete. Starting from `/` means ripgrep has to index the **entire filesystem** every time you type `@something`, which will be very slow.

### 2. The File Picker Slowdown Is a Known Issue

If your project is a large monorepo where the default file picker is slow, you can replace it with a custom command via the `fileSuggestion` setting in `settings.json`:

```json
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

The command receives JSON via stdin with a `query` field and outputs newline-separated file paths.

### 3. `@` Autocomplete Slowdown Is a Confirmed Bug Too

There is a known reported issue where entering files with `@` used to be snappy but now takes nearly a second for matching files to appear — and that's just in a *normal project directory*, not from `/`. From `/`, it would be far worse.

### 4. Context Window Fills Fast

The context window is the most important resource to manage. A single debugging session or codebase exploration might generate and consume tens of thousands of tokens. LLM performance degrades as context fills — Claude may start "forgetting" earlier instructions or making more mistakes.

## Better Alternative: Use `--add-dir`

Instead of running from `/`, run Claude Code **inside your primary project** and add other project directories as needed:

Claude Code's multi-directory support lets you work across multiple directories in one session using the `--add-dir` flag:

```bash
claude --add-dir /path/to/backend --add-dir /path/to/frontend
```

This lets you work across frontend, backend, and shared modules without switching sessions, while maintaining good performance.

## Summary

| Approach | Cross-project `@` | Performance |
| --- | --- | --- |
| Launch from `/` | ✅ Can reference everything | ❌ Very slow autocomplete, huge ripgrep scope |
| Launch from project + `--add-dir` | ✅ Explicit multi-dir access | ✅ Fast, scoped search |
| Launch from project dir only | ❌ Limited to one project | ✅ Fastest |

**Recommendation:** Use `--add-dir` for cross-project work. It gives you the same convenience of referencing files from multiple projects without the performance penalty of scanning from `/`.

References:

- [Claude Code File Referencing Guide - Steve Kinney](https://stevekinney.com/courses/ai-development/referencing-files-in-claude-code)
- [Claude Code Best Practices - Anthropic Docs](https://code.claude.com/docs/en/best-practices)
- [Claude Code Troubleshooting - Anthropic Docs](https://code.claude.com/docs/en/troubleshooting)
- [Claude Code Settings Reference](https://claudefa.st/blog/guide/settings-reference)
- [Multi-directory Support - Apidog](https://apidog.com/blog/claude-code-multi-directory-support/)
- [@ File Autocomplete Slow - GitHub Issue](https://github.com/anthropics/claude-code/issues/2078)
