---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自定义Markdown列表顺序配置
translated: true
type: note
---

**问题：** 如何配置 markdownlint-cli2 以保留自定义列表顺序（例如，不强制有序列表使用连续编号）？

**答案：**

问题在于 markdownlint 的 `MD029` 规则，该规则强制有序列表使用连续编号（1, 2, 3...）。通过 `.markdownlint.json` 配置文件禁用它：

```json
{
  "MD029": false
}
```

或者使用更细粒度的配置——允许任意列表前缀：

```json
{
  "MD029": {
    "style": "any"
  }
}
```

对于你的 pre-commit 钩子设置，将 `.markdownlint.json` 放置在仓库根目录：

```yaml
- repo: https://github.com/DavidAnson/markdownlint-cli2
  rev: v0.18.1
  hooks:
    - id: markdownlint-cli2
      args: ["--fix"]
      exclude: (node_modules/|logs/)
```

markdownlint-cli2 会自动发现 `.markdownlint.json` 或 `.markdownlint.yaml`。

**其他需要考虑禁用的相关列表规则：**

| 规则 | 默认值 | 功能 | 解决方案 |
| ------ | -------- | ------ | ---------- |
| `MD029` | `one_or_ordered` | 强制列表连续编号 | `"MD029": { "style": "any" }` |
| `MD030` | 强制列表标记后加空格 | `- item` vs `-item` | `"MD030": false` |
| `MD007` | 无序列表缩进 | 强制一致缩进 | `"MD007": false` |

**完整的 `.markdownlint.json` 以保留列表格式：**

```json
{
  "MD029": { "style": "any" },
  "MD030": false,
  "MD007": false
}
```

使用此配置运行 `--fix`，你的列表顺序将保持不变。
