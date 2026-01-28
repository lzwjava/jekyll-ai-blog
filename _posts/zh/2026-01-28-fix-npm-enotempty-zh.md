---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 快速修复 npm ENOTEMPTY 错误
translated: true
type: note
---

**问题：** 如何修复在尝试全局安装 @anthropic-ai/claude-code 时出现的 npm 错误 "ENOTEMPTY: directory not empty"？

**答案：**

这是一个非常常见的 npm bug / race condition，在全局安装或更新包时发生，当时 npm 试图重命名旧文件夹，但目标临时文件夹已经存在（或有权限问题，或有残留文件）。

以下是最可靠的修复方法，按从最安全/最快到更激进的顺序排列：

### 快速且推荐的修复方法（按此顺序尝试）

1. **强制删除 npm 创建的临时文件夹**

   ```bash
   sudo rm -rf /usr/lib/node_modules/@anthropic-ai/.claude-code-*
   ```

   然后重试：

   ```bash
   sudo npm install -g @anthropic-ai/claude-code
   ```

2. **先完全删除现有的包文件夹**

   ```bash
   sudo rm -rf /usr/lib/node_modules/@anthropic-ai
   sudo npm install -g @anthropic-ai/claude-code
   ```

3. **使用 --force 标志（文件夹部分损坏时通常有效）**

   ```bash
   sudo npm install -g @anthropic-ai/claude-code --force
   ```

4. **清理 npm 缓存 + 强制安装（怀疑有缓存问题时适用）**

   ```bash
   sudo npm cache clean --force
   sudo npm install -g @anthropic-ai/claude-code --force
   ```

### 如果以上仍失败（罕见情况）

5. **手动重命名文件夹（绕过 npm 的重命名逻辑）**

   ```bash
   sudo mv /usr/lib/node_modules/@anthropic-ai/claude-code \
           /usr/lib/node_modules/@anthropic-ai/claude-code-old-$(date +%s)
   sudo npm install -g @anthropic-ai/claude-code
   ```

   之后如果一切正常，可以删除 -old- 文件夹。

6. **使用 npm@latest（有时旧版 npm 的重命名处理更差）**

   ```bash
   sudo npm install -g npm@latest
   sudo npm install -g @anthropic-ai/claude-code
   ```

### 最可靠的一行命令组合（我通常这样操作）

```bash
sudo rm -rf /usr/lib/node_modules/@anthropic-ai \
           /usr/lib/node_modules/@anthropic-ai/.claude-code-* \
&& sudo npm cache clean --force \
&& sudo npm install -g @anthropic-ai/claude-code --force
```

任何一种成功后，使用以下命令验证：

```bash
claude-code --version
# 或直接
claude-code
```

**注意：** 包名 `@anthropic-ai/claude-code` 似乎不是 Anthropic 的官方包（截至 2025 年底 / 2026 年初）。请确保安装的是您实际想要使用的工具。

**参考：**

- 无（常见 npm 错误，在 Stack Overflow、GitHub issues 和 npm bug tracker 上有详细文档）