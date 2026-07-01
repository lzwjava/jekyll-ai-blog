---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代码编辑工具对比
translated: true
type: note
---

**问题：** Claude Code 和 OpenAI Codex 如何实现它们的文件编辑工具，它们之间有何比较？

**回答：**

## Claude Code 与 OpenAI Codex：编辑工具实现比较

这两个代理在文件编辑方面采用了根本不同的方法。

---

## 1. Claude Code — `str_replace_based_edit_tool`

### 工具名称与版本

该工具名为 `str_replace_based_edit_tool`，在 API 中声明类型为 `text_editor_20250728`。它是一个无 schema 工具 — schema 内置于模型本身，无法由开发者修改。

### 支持的命令

该工具根据 `command` 参数分派，具有以下分支：`view`（读取文件内容）、`str_replace`（替换文件中的文本）、`create`（创建新文件）、`insert`（在指定位置插入文本）和 `undo_edit`（撤销最后一次编辑 — 仅在 Claude Sonnet 3.7 中可用，在 Claude 4 中已移除）。

### `str_replace` 的内部工作原理

编辑工具使用**精确字符串匹配**。默认情况下，`old_string` 在文件中必须**恰好匹配一次**（除非 `replace_all=true`）。该工具强制执行**读前编辑**策略：验证当前会话中至少读取过一次文件。它还会保留源文件的精确缩进（制表符/空格），并处理 `cat -n` 风格的行号前缀。

```python
# 概念性实现（开发者侧处理程序）
def handle_editor_tool(tool_call):
    command  = tool_call.input["command"]
    path     = tool_call.input["path"]

    if command == "view":
        return open(path).read()

    elif command == "str_replace":
        old_str = tool_call.input["old_str"]
        new_str = tool_call.input["new_str"]
        content = open(path).read()
        # 必须恰好匹配一次
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

### str_replace 工具 Schema

```typescript
interface EditTool {
  file_path: string;       // 绝对路径，必填
  old_string: string;      // 要查找的精确文本
  new_string: string;      // 替换文本（必须与 old_string 不同）
  replace_all?: boolean;   // 默认 false
}
```

### 已知故障模式

两种最常见的错误是 `"String to replace not found in file"`（由于空白字符、编码差异或过时上下文导致精确匹配失败）和 `"File has been unexpectedly modified"`（状态跟踪错误，在 Windows/WSL2 上更常见）。Claude Code 会自动重试失败的编辑，通常在几次尝试后成功。

### 代码执行沙箱变体

在 Anthropic 的代码执行沙箱中使用时，该工具名为 `text_editor_code_execution`，并在 `str_replace` 上返回结构化的 diff 元数据，包括 `oldStart`、`oldLines`、`newStart`、`newLines` 和 diff 风格的 `lines` 数组（例如 `["- \"debug\": true", "+ \"debug\": false"]`）。

---

## 2. OpenAI Codex CLI — `apply_patch`

Codex 采用了完全不同的方法：不是使用 `str_replace`，而是使用**diff/patch 格式**，模仿 unified diff。

### `apply_patch` 工具类型

OpenAI 强烈推荐使用他们确切的 `apply_patch` 实现，因为模型已针对此 diff 格式进行了特定训练。有两种变体：**Freeform** 变体（通过 Responses API 的首选实现）和 **Function** 变体（标准函数调用，用于非 OpenAI 托管模型，如 Azure 上的 gpt-4.1）。

### 补丁格式

默认情况下，`apply_patch` 在每个更改前后显示 3 行上下文。如果更改位于前一个更改的 3 行以内，则不会重复上下文行。如果 3 行上下文不足以唯一标识代码片段，则 `@@` 操作符可以指示类或函数范围（例如 `@@ class BaseClass`），并且可以堆叠多个 `@@` 语句用于深度嵌套代码。

补丁示例：

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

### 工具分派层次

Codex 系统提示指示模型按照此优先级默认使用求解器工具：`git`、`rg` (ripgrep)、`read_file`、`list_dir`、`glob_file_search`、`apply_patch`、`todo_write/update_plan` — 仅在没有专用工具可以执行操作时才回退到原始 shell (`cmd`/`run_terminal_cmd`)。

### 写入与编辑分离

Claude Code 将 Write（完整文件覆盖）和 Edit（精确 `str_replace`）分离为两个不同的工具。对于现有文件，Write 强制执行读前写入安全检查。Edit 优先用于修改现有文件；Write 仅用于真正的新文件。

相比之下，Codex 使用 `apply_patch` 同时处理创建和修改，其中 `+++ /dev/null` 表示删除，`--- /dev/null` 表示创建。

---

## 总结比较表

| 特性 | Claude Code (`str_replace_based_edit_tool`) | OpenAI Codex (`apply_patch`) |
| --- | --- | --- |
| **编辑范式** | Exact string match & replace | Unified diff / patch format |
| **上下文行** | 无（纯字符串匹配） | 更改前后 3 行（可配置） |
| **创建文件** | `create` 命令 | `--- /dev/null` 补丁头部 |
| **读前编辑** | ✅ 系统强制执行 | ❌ 未强制执行 |
| **撤销支持** | ✅ (`undo_edit`，仅 Claude 3.7) | ✅ (通过 `git apply` 回滚) |
| **多文件编辑** | 每个工具调用一个文件 | 单个补丁可跨越多个文件 |
| **故障模式** | 字符串未找到 / 精确不匹配 | 补丁冲突 / hunk 拒绝 |
| **Schema** | 无 schema（内置于模型） | Function 或 Freeform（可配置） |
| **行号锚定** | ❌ (基于字符串) | ✅ (`@@` 头部中的行号) |
| **Notebook 支持** | ✅ `NotebookEditTool` 用于 `.ipynb` | ❌ |

核心权衡：Claude Code 的 `str_replace` 在开发者侧更容易实现，但对空白字符/编码漂移敏感，而 Codex 的 `apply_patch` 对于大更改更健壮，但要求模型生成结构有效的 unified diff。

参考资料：

- [Claude Code Text Editor Tool Docs](https://docs.claude.com/en/docs/agents-and-tools/tool-use/text-editor-tool)
- [Claude Code Internal Tools Reference (GitHub Gist)](https://gist.github.com/bgauryy/0cdb9aa337d01ae5bd0c803943aa36bd)
- [OpenAI Codex Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide/)
- [OpenAI Codex apply_patch instructions (GitHub)](https://github.com/openai/codex/blob/main/codex-rs/apply-patch/apply_patch_tool_instructions.md)
- [OpenAI Codex CLI prompt.md (GitHub)](https://github.com/openai/codex/blob/main/codex-rs/core/prompt.md)
- [Claude Code Edit Errors Explained](https://claudelog.com/faqs/claude-code-error-editing-file/)
