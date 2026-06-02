---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: npm 包的 Tgz 与 Zip 对比
translated: true
type: note
---

npm package 中 `.tgz` 和 `.zip` 之间的主要区别：

## Format & Compression

- **`.tgz`**：使用 gzip 压缩的 tarball (tar.gz)。这是 npm 的原生格式。
- **`.zip`**：一种 zip 存档，在 Windows 环境中更常见。

## npm Usage

- **`.tgz`**：由 `npm pack` 创建的标准格式。当你运行此命令时，npm 会为你的 package 创建一个 `.tgz` 文件。
- **`.zip`**：并非由 npm 命令原生支持，尽管你可以手动创建一个。

## Installation

两者都可以被安装，但语法不同：

```bash
npm install package.tgz
npm install package.zip
```

## Key Practical Differences

**File permissions**：`.tgz` 保留了 Unix file permissions 和 symbolic links，而 `.zip` 并不总是能很好地处理这些。这对于包含可执行 scripts 的 packages 至关重要。

**Consistency**：`.tgz` 是 npm registry 内部使用的格式。当你发布到 npm 时，它会以 tarball 的形式存储。

**Cross-platform**：`.zip` 对于 Windows 用户来说更熟悉，但在现代 npm 环境下，`.tgz` 在所有平台上都能正常工作。

## When to Use Each

- 在标准 npm workflows 中使用 `.tgz`（packing、sharing、installing packages）
- 仅在有特定原因时才使用 `.zip`，例如分发给可能没有 tar 解压工具的非开发人员

对于 npm package 的开发和分发，请坚持使用 `.tgz` —— 它是标准做法，且能避免潜在的 compatibility 问题。
