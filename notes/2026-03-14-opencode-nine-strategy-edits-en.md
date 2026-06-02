---
audio: false
generated: true
image: false
lang: en
layout: post
title: opencode nine strategy file edits
translated: false
type: note
---

**Question:** How does opencode (anomalyco/opencode) implement its file edit tool?

**Answer:**

## opencode's `EditTool` — Deep Dive

opencode is a TypeScript/Bun-based open-source coding agent. Its edit tool lives at `packages/opencode/src/tool/edit.ts` and is significantly more sophisticated than Claude Code's simple `str_replace`, featuring a **9-strategy fallback replacer cascade**.

---

### 1. Tool Parameters

The `EditTool` is defined using `Tool.define` and uses the permission key `edit` (shared with `WriteTool`). An external directory path triggers an additional `external_directory` permission request.

The tool's parameter schema (TypeScript):

```typescript
{
  filePath: string,      // absolute path to the file
  oldString: string,     // exact text to find and replace
  newString: string,     // replacement text
  replaceAll?: boolean,  // default false — replace all vs. unique match
}
```

### 2. The `oldString === ""` Special Case: File Creation

When `oldString` is `""` (empty string), the `EditTool` creates a new file — it takes the same code path as `WriteTool`. This means `EditTool` doubles as a file-creation tool with a single unified interface.

### 3. The Read-Before-Edit Freshness Check

After a successful `ReadTool` call, `FileTime.read(ctx.sessionID, filePath)` records a timestamp. A subsequent `EditTool` call then validates this freshness — if the file hasn't been read in the current session, the edit is rejected.

This is the same concept as Claude Code's read-before-edit enforcement, but implemented as an explicit timestamp comparison rather than a session file-list check.

### 4. The 9-Strategy Replacer Cascade — The Key Differentiator

This is what makes opencode's edit tool stand out. The `replace()` function in `edit.ts` runs through 9 different "replacer" strategies in sequence to fix agent mistakes:

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

Each strategy is tried in order; the first one that finds a match wins.

#### Strategy Breakdown

| Strategy | What it does |
|---|---|
| `SimpleReplacer` | Raw `content.indexOf(search)` — exact match |
| `LineTrimmedReplacer` | Splits into lines, trims each, compares trimmed versions |
| `BlockAnchorReplacer` | Uses the first/last line of `oldString` as anchors to fuzzy-find the block |
| `WhitespaceNormalizedReplacer` | Replaces all `\s+` with a single space before matching |
| `IndentationFlexibleReplacer` | Strips common leading whitespace prefix from all lines |
| `EscapeNormalizedReplacer` | Normalizes `\t`, `\r\n`, escape sequences before matching |
| `TrimmedBoundaryReplacer` | Trims the leading/trailing boundary of the matched region |
| `ContextAwareReplacer` | Incorporates surrounding lines for disambiguation |
| `MultiOccurrenceReplacer` | When `replaceAll=false` and multiple matches exist, picks the most likely one |

These fallback strategies exist precisely because agents struggle with whitespace and indentation. The tool was designed with these fallbacks as a "band-aid", acknowledging the fundamental problem: the `ReadTool` output format uses a tab character as the line number separator (invisible, variable width), causing agents to accidentally include line-number-prefix characters in their `oldString`.

### 5. The `replaceAll=false` Ambiguity Bug

There is a known bug in `edit.ts` with the multi-occurrence handling. When `replaceAll: false`, the code uses `lastIndexOf` to check uniqueness — it skips matches where `indexOf !== lastIndexOf`. However, the block-anchor strategy can match across non-unique substrings (e.g. matching just `}` and `return mainLayout` separately), leading to corruption where nearly the entire file gets replaced.

### 6. LSP Integration After Edit

One important distinction from Claude Code: opencode integrates LSP (Language Server Protocol) support — after a successful file write/edit, the LSP client receives the change notification and can immediately report diagnostics (syntax errors, type errors) back to the agent.

### 7. The `patch.ts` Tool (Separate from `edit.ts`)

opencode also has a separate `tool/patch.ts` — a distinct tool from `edit.ts` — which uses a traditional unified-diff/patch approach similar to Codex's `apply_patch`. Both `edit.ts` and `patch.ts` share the `external_directory` permission key.

---

## Architecture Diagram

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

## Comparison: opencode vs Claude Code Edit Tools

| Feature | opencode `EditTool` | Claude Code `str_replace_based_edit_tool` |
|---|---|---|
| **Language** | TypeScript (Bun) | Schema-less (baked into model) |
| **Fallback strategies** | ✅ 9-strategy cascade | ❌ Exact match only (auto-retry by model) |
| **File creation** | ✅ `oldString=""` path | ✅ Separate `create` command |
| **Freshness check** | ✅ Timestamp-based | ✅ Session file-list based |
| **Patch tool** | ✅ Separate `patch.ts` | ❌ No separate patch tool |
| **LSP feedback** | ✅ After every write | ❌ Not built-in |
| **`replaceAll`** | ✅ Supported | ✅ Supported |
| **Known bug** | `BlockAnchorReplacer` can corrupt | Whitespace drift fails silently |

The most important architectural insight: opencode tries *very hard* to succeed even when the model generates imprecise `oldString` values, using 9 progressively fuzzier strategies. Claude Code instead relies on the model being precise, and just auto-retries the whole tool call if exact matching fails.

References:

- [opencode Tool System - DeepWiki](https://deepwiki.com/anomalyco/opencode/2.5-tool-system-and-permissions)
- [opencode Edit Tool Bug: BlockAnchorReplacer Issue #2433](https://github.com/anomalyco/opencode/issues/2433)
- [opencode PR #12030: Improve Read tool for Edit tool accuracy](https://github.com/anomalyco/opencode/pull/12030)
- [opencode Bug: LineTrimmedReplacer newline issue #1676](https://github.com/sst/opencode/issues/1676)
- [opencode Issue #5395: Split external_directory permissions](https://github.com/anomalyco/opencode/issues/5395)
