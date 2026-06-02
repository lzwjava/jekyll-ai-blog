---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 精通 npm config list
translated: true
type: note
---

我将详细解释 `npm config list` 命令及其用法。

## Basic Usage

```bash
npm config list
```

此命令显示你当前的 npm configuration 设置。它会展示：

- 用户特定设置（来自 `~/.npmrc`）
- Global 设置
- 内置的 npm defaults

## Common Variations

**仅列出用户和 global 设置（不包含 defaults）：**

```bash
npm config list --json
```

**以 JSON 格式列出以便于解析：**

```bash
npm config list -l
```

**显示所有 config 选项，包括 defaults：**

```bash
npm config list -l
```

## What You'll See

输出通常包含如下设置：

- Registry URL (`registry`)
- Package 安装 prefix (`prefix`)
- Cache 路径 (`cache`)
- 用户信息 (`init-author-name`, `init-author-email`)
- Authentication tokens（部分隐藏）
- Proxy 设置

## Related Useful Commands

**获取特定的 config 值：**

```bash
npm config get registry
```

**设置一个 config 值：**

```bash
npm config set registry https://registry.npmjs.org/
```

**删除一个 config 值：**

```bash
npm config delete proxy
```

**在默认编辑器中编辑 config：**

```bash
npm config edit
```

该命令对于调试 npm 问题、检查 registry 设置或验证 authentication configuration 非常有用。
