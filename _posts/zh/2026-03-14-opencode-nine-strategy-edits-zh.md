---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源代码 9 策略文件编辑
translated: true
type: note
---

**问题：** opencode (anomalyco/opencode) 如何实现其文件编辑工具？

**答案：**

## opencode 的 `EditTool` — 深入剖析

opencode 是一个基于 TypeScript/Bun 的开源编码代理。其编辑工具位于 `packages/opencode/src/tool/edit.ts`，比 Claude Code 的简单 `str_replace` 复杂得多，具有 **9 种策略的回退替换器级联**。

---

### 1. 工具参数

`EditTool` 使用 `Tool.define` 定义，并使用权限键 `edit`（与 `WriteTool` 共享）。外部目录路径会触发额外的 `external_directory` 权限请求。

工具的参数 schema（TypeScript）：

```typescript
{
  filePath: string,      // absolute path to the file
  oldString: string,     // exact text to find and replace
  newString: string,     // replacement text
  replaceAll?: boolean,  // default false — replace all vs. unique match
}
```

### 2. `oldString === ""` 特殊情况：文件创建

当 `oldString` 为 `""`（空字符串）时，`EditTool` 会创建新文件 — 它走与 `WriteTool` 相同的代码路径。这意味着 `EditTool` 同时作为文件创建工具，具有单一统一的接口。

### 3. 编辑前的读取新鲜度检查

在成功的 `ReadTool` 调用后，`FileTime.read(ctx.sessionID, filePath)` 会记录时间戳。随后 `EditTool` 调用会验证此新鲜度 — 如果文件未在当前会话中读取，则拒绝编辑。

这是与 Claude Code 的“读取前编辑”强制执行相同概念，但实现为显式的时间戳比较，而不是会话文件列表检查。

### 4. 9 种策略的替换器级联 — 关键差异

这就是 opencode 编辑工具的亮点所在。`edit.ts` 中的 `replace()` 函数会按顺序运行 9 种不同的“替换器”策略，以修复代理的错误：

```typescript
for (const replacer of [
  SimpleReplacer,               // 1. Exact string match (fastest)
  LineTrimmedReplacer,          // 2. Match after trimming each line
  BlockAnchorReplacer,          // 3. Fuzzy match using block boundaries
  WhitespaceNormalizedReplacer, // 4. Collapse all \s+ → " "
  IndentationFlexibleReplacer,  // 5. Strip common leading indentation
  EscapeNormalizedReplacer,     // 6. Normalize escape sequences
  TrimmedBoundaryReplacer,      // 7. Trim leading/trailing whitespace of match
  ContextAwareReplacer,         // 8. Use surrounding context lines as anchors
  MultiOccurrenceReplacer,      // 9. Handle ambiguous multi-match situations
]) {
  const result = replacer(content, oldString, newString, replaceAll)
  if (result !== null) return result
}
throw new Error("No replacement strategy succeeded")
```

每个策略按顺序尝试；第一个找到匹配的策略获胜。

#### 策略详解

  
| 策略 | 功能描述 |
|---|---|
| `SimpleReplacer` | 原始 `content.indexOf(search)` — 精确匹配 |
| `LineTrimmedReplacer` | 分割成行，修剪每行，比较修剪版本 |
| `BlockAnchorReplacer` | 使用 `oldString` 的首/尾行作为锚点进行模糊块查找 |
| `WhitespaceNormalizedReplacer` | 将所有 `\s+` 替换为单个空格后再匹配 |
| `IndentationFlexibleReplacer` | 剥离所有行的共同前导缩进 |
| `EscapeNormalizedReplacer` | 归一化 `\t`、`\r\n`、转义序列后再匹配 |
| `TrimmedBoundaryReplacer` | 修剪匹配区域的前导/尾随空白 |
| `ContextAwareReplacer` | 纳入周围行用于消歧 |
| `MultiOccurrenceReplacer` | 当 `replaceAll=false` 且存在多个匹配时，选择最可能的那个 |

这些回退策略的存在正是因为代理在处理空白和缩进时容易出错。该工具设计这些回退作为“权宜之计”，承认根本问题：`ReadTool` 输出格式使用制表符作为行号分隔符（不可见、可变宽度），导致代理意外地将行号前缀字符包含在 `oldString` 中。

### 5. `replaceAll=false` 的歧义 Bug

`edit.ts` 中存在一个已知的多重出现处理 Bug。当 `replaceAll: false` 时，代码使用 `lastIndexOf` 检查唯一性 — 它跳过 `indexOf !== lastIndexOf` 的匹配。然而，块锚点策略可能匹配非唯一子串（例如分别匹配 `}` 和 `return mainLayout`），导致几乎整个文件被替换的损坏。

### 6. 编辑后的 LSP 集成

与 Claude Code 的一个重要区别：opencode 集成了 LSP（Language Server Protocol）支持 — 文件写入/编辑成功后，LSP 客户端会收到变更通知，并立即向代理报告诊断（语法错误、类型错误）。

### 7. `patch.ts` 工具（独立于 `edit.ts`）

opencode 还有一个独立的 `tool/patch.ts` — 与 `edit.ts` 不同的工具 — 它使用传统的 unified-diff/patch 方法，类似于 Codex 的 `apply_patch`。`edit.ts` 和 `patch.ts` 共享 `external_directory` 权限键。

---

## 架构图

```
EditTool.execute(filePath, oldString, newString, replaceAll)
  │
  ├── oldString === "" ?
  │     └── → WriteTool code path (create new file)
  │
  ├── FileTime.check(sessionID, filePath)  ← freshness guard
  │     └── not read yet? → permission.ask("edit")
  │
  ├── fs.readFile(filePath)
  │
  ├── replace(content, oldString, newString, replaceAll)
  │     ├── 1. SimpleReplacer          (exact match)
  │     ├── 2. LineTrimmedReplacer     (trim each line)
  │     ├── 3. BlockAnchorReplacer     (fuzzy block boundary) ← bug risk
  │     ├── 4. WhitespaceNormalizedReplacer
  │     ├── 5. IndentationFlexibleReplacer
  │     ├── 6. EscapeNormalizedReplacer
  │     ├── 7. TrimmedBoundaryReplacer
  │     ├── 8. ContextAwareReplacer
  │     └── 9. MultiOccurrenceReplacer
  │           └── all fail? → throw Error("not found")
  │
  ├── fs.writeFile(filePath, result)
  │
  └── LSP.didChange(filePath) → diagnostics feedback
```

---

## 比较：opencode 与 Claude Code 编辑工具

  
| 特性 | opencode `EditTool` | Claude Code `str_replace_based_edit_tool` |
|---|---|---|
| **语言** | TypeScript (Bun) | 无 schema（内置于模型） |
| **回退策略** | ✅ 9 种策略级联 | ❌ 仅精确匹配（模型自动重试） |
| **文件创建** | ✅ `oldString=""` 路径 | ✅ 独立的 `create` 命令 |
| **新鲜度检查** | ✅ 基于时间戳 | ✅ 基于会话文件列表 |
| **Patch 工具** | ✅ 独立的 `patch.ts` | ❌ 无独立的 patch 工具 |
| **LSP 反馈** | ✅ 每次写入后 | ❌ 未内置 |
| **`replaceAll`** | ✅ 支持 | ✅ 支持 |
| **已知 Bug** | `BlockAnchorReplacer` 可能损坏 | 空白漂移静默失败 |

最重要的架构洞见：opencode 竭尽全力即使模型生成不精确的 `oldString` 值也能成功，使用 9 种渐进式更模糊的策略。Claude Code 则依赖模型精确，并在精确匹配失败时仅自动重试整个工具调用。

参考资料：

- [opencode Tool System - DeepWiki](https://deepwiki.com/anomalyco/opencode/2.5-tool-system-and-permissions)
- [opencode Edit Tool Bug: BlockAnchorReplacer Issue #2433](https://github.com/anomalyco/opencode/issues/2433)
- [opencode PR #12030: Improve Read tool for Edit tool accuracy](https://github.com/anomalyco/opencode/pull/12030)
- [opencode Bug: LineTrimmedReplacer newline issue #1676](https://github.com/sst/opencode/issues/1676)
- [opencode Issue #5395: Split external_directory permissions](https://github.com/anomalyco/opencode/issues/5395)