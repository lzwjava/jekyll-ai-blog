---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 禁用markdownlint的MD029规则
translated: true
type: note
---

**问题：** markdownlint 配置中 `"MD029": false` 是什么意思？

**回答：**

`"MD029": false` **完全禁用 MD029 规则**。

**MD029 的作用（默认行为）：**

MD029 即“有序列表项前缀”规则。默认情况下，它强制有序列表使用连续编号：

```markdown
✅ 正确（MD029 强制要求）：
1. 第一项
2. 第二项
3. 第三项

❌ 错误（MD029 会标记）：
2. 第一项
1. 第二项
3. 第三项
```

**当你设置 `"MD029": false` 时：**

markdownlint 不再检查该规则。你的列表可以是任意顺序：

```markdown
2. 主要组件
1. 主要组件
3. 主要组件
```

✅ 全部通过——规则已被禁用。

**区别：`false` 与 `{ "style": "any" }`**

| 配置 | 行为 |
|------|------|
| `"MD029": false` | 规则禁用——完全不检查 |
| `"MD029": { "style": "any" }` | 规则启用——允许任何编号样式（1, 2, 3 或 2, 1, 3 或 1, 1, 1——均有效） |

针对你的使用场景（保留自定义顺序），两种方式都可行。如果你完全不在乎列表验证，使用 `false`。如果你希望 markdownlint 仍然验证列表语法但允许非连续编号，使用 `{ "style": "any" }`。
