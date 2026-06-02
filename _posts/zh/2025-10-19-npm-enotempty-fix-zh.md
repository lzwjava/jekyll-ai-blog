---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 解决npm ENOTEMPTY安装错误
translated: true
type: note
---

### 理解错误原因

您执行的 `sudo npm i -g @anthropic-ai/claude-code --verbose` 命令在安装过程中因 `ENOTEMPTY` 错误而失败。这是 npm 常见问题，通常发生在 npm 尝试重命名（或移动）现有目录作为更新或重新安装包的一部分时，但该目录非空。具体到本例，是重命名 `/usr/lib/node_modules/@anthropic-ai/claude-code` 到临时备份位置（`/usr/lib/node_modules/@anthropic-ai/.claude-code-ZjqcDZyQ`）时失败。

这通常由以下原因引起：
- 之前的部分安装或中断安装遗留了文件或子目录
- 其他进程的文件锁（例如包被部分加载或其他 npm 命令正在运行）
- 少数情况下，使用 `sudo` 进行全局安装时的权限异常

该包本身（`@anthropic-ai/claude-code`）是合法的——这是 Anthropic 官方的 "Claude Code" CLI 工具，一个能与您的终端和代码库集成的智能编码助手。

### 快速解决方案

按顺序尝试以下步骤。由于是全局安装，请在需要时使用 root 权限或 `sudo`。

1. **手动移除现有目录**
   这会清除有问题的部分安装：
   ```
   sudo rm -rf /usr/lib/node_modules/@anthropic-ai/claude-code
   ```
   - 如果父级作用域目录（`@anthropic-ai`）现在为空，也可以移除：
     ```
     sudo rm -rf /usr/lib/node_modules/@anthropic-ai
     ```
   然后重试原命令：
   ```
   sudo npm i -g @anthropic-ai/claude-code --verbose
   ```

2. **清除 npm 缓存**
   如果上述方法无效，可能是缓存条目损坏：
   ```
   sudo npm cache clean --force
   sudo npm cache verify
   ```
   清理后重试安装。

3. **检查运行中的进程**
   确保没有其他 npm/Node 进程正在使用该目录：
   ```
   ps aux | grep npm
   ```
   如有需要终止残留进程（例如 `sudo kill <PID>`），然后重试。

4. **替代方案：使用 npx 测试**
   如果只想测试工具而不进行完整全局安装，可尝试：
   ```
   npx @anthropic-ai/claude-code --help
   ```
   这会临时下载并运行，而不修改全局模块。

### 额外建议
- **权限最佳实践**：使用 `sudo` 进行全局安装可能导致后续所有权问题。考虑使用 node 版本管理器如 `nvm` 完全避免 `sudo`，或设置自定义全局前缀：
  ```
  mkdir ~/.npm-global
  npm config set prefix '~/.npm-global'
  export PATH=~/.npm-global/bin:$PATH
  ```
  然后无需 `sudo` 即可安装。
- **安装后验证**：安装完成后，使用 `claude-code --version` 检查（假设这是二进制文件名——请查阅文档确认）。
- 如果问题仍然存在，请分享 `npm ls -g @anthropic-ai/claude-code` 的输出以进行更多诊断。

这应该能让您快速运行起来。如果遇到其他问题，请粘贴新的日志！

[Claude Code on npm](https://www.npmjs.com/package/@anthropic-ai/claude-code)
[Anthropic Docs: Set up Claude Code](https://docs.claude.com/en/docs/claude-code/setup)
