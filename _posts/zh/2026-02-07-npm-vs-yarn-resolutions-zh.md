---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: npm Overrides 与 Yarn Resolutions 的比较
translated: true
type: note
---

是的，你说得对！

**npm 8.3.0+**：在 package.json 中引入了 `overrides` 字段
**npm 8.3.0 之前**：没有原生的 npm 解决方案 - 你必须使用 **Yarn** 的 `resolutions` 字段（这是 Yarn 特有的，不是 npm 的）

以下是详细说明：

## 对于 npm 8.3.0 及更高版本：

| 字段 | 描述 |
| :--- | :--- |
| `overrides` | 用于强制替换依赖树中的特定版本 |

```json
{
  "overrides": {
    "package-name": "version",
    "parent-package": {
      "dependency-name": "version"
    }
  }
}
```

## 对于 npm 8.3.0 之前：

如果你使用的是 **Yarn**，你可以使用：
```json
{
  "resolutions": {
    "package-name": "version"
  }
}
```

如果你使用的是 **npm < 8.3.0**，你的选择非常有限：
- 使用 `npm-force-resolutions` 包作为 workaround
- 手动使用 `npm shrinkwrap`
- 切换到 Yarn 以使用 `resolutions`
- 等待 npm 8.3.0+ 以获得原生支持

所以 `resolutions` 从来不是 npm 的特性 - 它一直是 Yarn 的特性。npm 终于在 8.3.0 版本通过 `overrides` 添加了对应的功能。