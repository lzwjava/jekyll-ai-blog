---
audio: false
generated: true
image: false
lang: en
layout: post
title: Code Edit Tools Compared
translated: false
type: note
---

**Question:** How do Claude Code and OpenAI Codex implement their file edit tools, and how do they compare to each other?

**Answer:**

## Claude Code vs OpenAI Codex: Edit Tool Implementations

These two agents take fundamentally different approaches to file editing.

---

## 1. Claude Code — `str_replace_based_edit_tool`

### The Tool Name & Versions

The tool is named `str_replace_based_edit_tool` and is declared with type `text_editor_20250728` in the API. It is a schema-less tool — the schema is built into the model itself and cannot be modified by the developer.

### Commands Supported

The tool dispatches on a `command` parameter with the following branches: `view` (read file contents), `str_replace` (replace text in file), `create` (create a new file), `insert` (insert text at a location), and `undo_edit` (revert last edit — only available in Claude Sonnet 3.7, removed in Claude 4).

### How `str_replace` Works Internally

The Edit tool uses **exact string matching**. The `old_string` must have exactly **one** match in the file by default (unless `replace_all=true`). The tool enforces a **read-before-edit** policy: it validates that the file was read at least once in the current session. It also preserves exact indentation (tabs/spaces) from source and handles line number prefixes in `cat -n` style format.

```python
# Conceptual implementation (developer-side handler)
def handle_editor_tool(tool_call):
    command  = tool_call.input["command"]
    path     = tool_call.input["path"]

    if command == "view":
        return open(path).read()

    elif command == "str_replace":
        old_str = tool_call.input["old_str"]
        new_str = tool_call.input["new_str"]
        content = open(path).read()
        # MUST match exactly once
        if content.count(old_str) != 1:
            return {"error": "old_str not found or not unique"}
        open(path, "w").write(content.replace(old_str, new_str, 1))

    elif command == "create":
        open(path, "w").write(tool_call.input["file_text"])

    elif command == "insert":
        lines = open(path).readlines()
        insert_line = tool_call.input["insert_line"]
        lines.insert(insert_line, tool_call.input["new_str"] + "\n")
        open(path, "w").writelines(lines)
```

### The str_replace Tool Schema

```typescript
interface EditTool {
  file_path: string;       // absolute path, required
  old_string: string;      // exact text to find
  new_string: string;      // replacement (must differ from old_string)
  replace_all?: boolean;   // default false
}
```

### Known Failure Modes

The two most common errors are `"String to replace not found in file"` (exact match fails due to whitespace, encoding differences, or stale context) and `"File has been unexpectedly modified"` (state tracking bug, more common on Windows/WSL2). Claude Code automatically retries failed edits and usually succeeds within a few attempts.

### Code Execution Sandbox Variant

When used inside Anthropic's code execution sandbox, the tool is named `text_editor_code_execution` and returns structured diff metadata on `str_replace`, including `oldStart`, `oldLines`, `newStart`, `newLines`, and a diff-style `lines` array (e.g. `["- \"debug\": true", "+ \"debug\": false"]`).

---

## 2. OpenAI Codex CLI — `apply_patch`

Codex takes a completely different approach: instead of `str_replace`, it uses a **diff/patch format** modeled after unified diffs.

### The `apply_patch` Tool Type

OpenAI strongly recommends using their exact `apply_patch` implementation, as the model has been trained specifically for this diff format. There are two variants: a **Freeform** variant (first-class implementation via the Responses API) and a **Function** variant (standard function calling, used for non-OpenAI hosted models like gpt-4.1 on Azure).

### The Patch Format

By default, `apply_patch` shows 3 lines of context above and below each change. If a change is within 3 lines of a previous change, context lines are not duplicated. If 3 lines of context is insufficient to uniquely identify the snippet, the `@@` operator can indicate the class or function scope (e.g. `@@ class BaseClass`), and multiple `@@` statements can be stacked for deeply nested code.

A patch looks like this:

```
*** /path/to/file.py
--- /path/to/file.py
***************
*** 10,15 ****
  def foo():
-     return "old"
--- 10,15 ----
  def foo():
+     return "new"
```

### Tool Dispatch Hierarchy

The Codex system prompt instructs the model to default to solver tools in this priority: `git`, `rg` (ripgrep), `read_file`, `list_dir`, `glob_file_search`, `apply_patch`, `todo_write/update_plan` — only falling back to raw shell (`cmd`/`run_terminal_cmd`) when no dedicated tool can perform the action.

### Write vs Edit Separation

Claude Code separates Write (full file overwrite) and Edit (surgical `str_replace`) as two distinct tools. Write enforces a read-before-write safety check for existing files. Edit is preferred for modifications to existing files; Write is only for genuinely new files.

In contrast, Codex uses `apply_patch` for both create and modify, with `+++ /dev/null` meaning delete and `--- /dev/null` meaning create.

---

## Summary Comparison Table

| Feature | Claude Code (`str_replace_based_edit_tool`) | OpenAI Codex (`apply_patch`) |
|---|---|---|
| **Edit paradigm** | Exact string match & replace | Unified diff / patch format |
| **Context lines** | None (pure string match) | 3 lines before/after (configurable) |
| **Create file** | `create` command | `--- /dev/null` patch header |
| **Read-before-edit** | ✅ Enforced by system | ❌ Not enforced |
| **Undo support** | ✅ (`undo_edit`, Claude 3.7 only) | ✅ (via `git apply` rollback) |
| **Multi-file edits** | One file per tool call | Single patch can span multiple files |
| **Failure mode** | String not found / exact mismatch | Patch conflict / hunk rejection |
| **Schema** | Schema-less (baked into model) | Function or Freeform (configurable) |
| **Line number anchor** | ❌ (string-based) | ✅ (line numbers in `@@` headers) |
| **Notebook support** | ✅ `NotebookEditTool` for `.ipynb` | ❌ |

The core tradeoff: Claude Code's `str_replace` is simpler to implement on the developer side but brittle to whitespace/encoding drift, while Codex's `apply_patch` is more robust for large changes but requires the model to generate structurally valid unified diffs.

References:

- [Claude Code Text Editor Tool Docs](https://docs.claude.com/en/docs/agents-and-tools/tool-use/text-editor-tool)
- [Claude Code Internal Tools Reference (GitHub Gist)](https://gist.github.com/bgauryy/0cdb9aa337d01ae5bd0c803943aa36bd)
- [OpenAI Codex Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide/)
- [OpenAI Codex apply_patch instructions (GitHub)](https://github.com/openai/codex/blob/main/codex-rs/apply-patch/apply_patch_tool_instructions.md)
- [OpenAI Codex CLI prompt.md (GitHub)](https://github.com/openai/codex/blob/main/codex-rs/core/prompt.md)
- [Claude Code Edit Errors Explained](https://claudelog.com/faqs/claude-code-error-editing-file/)
