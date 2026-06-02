---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: NPM Caret 与 Tilde 版本规则
translated: true
type: note
---

在 `package.json` 中，`~` 和 `^` 符号控制 npm 如何更新你的 dependencies：

**`^` (caret) - minor 和 patch 更新**

- 允许不改变左侧第一个非零数字的更新
- `^1.2.3` → 允许 `1.2.4`, `1.3.0`, `1.9.9` 但**不允许** `2.0.0`
- `^0.2.3` → 允许 `0.2.4`, `0.2.9` 但**不允许** `0.3.0` (因为在 0.x 版本中，第二个数字被视为 major)
- 这是运行 `npm install package` 时的**默认**选项

**`~` (tilde) - 仅 patch 更新**

- 仅允许 patch 级别的更改
- `~1.2.3` → 允许 `1.2.4`, `1.2.9` 但**不允许** `1.3.0`
- 比 `^` 更保守

**实际示例：**

```json
{
  "dependencies": {
    "react": "^18.2.0",     // 可以更新到 18.x.x
    "lodash": "~4.17.21",   // 只能更新到 4.17.x
    "express": "4.18.2"     // 精确版本，不进行更新
  }
}
```

大多数项目使用 `^`，因为它在获取 bug fixes 和新特性与避免 breaking changes 之间取得了平衡。如果你需要最大程度的稳定性（例如在 production 应用中），你可能会使用 `~` 或精确版本，并提交你的 `package-lock.json` 以确保每个人都获得完全相同的 dependencies。
