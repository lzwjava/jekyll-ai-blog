---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 赫尔墨斯代理复制命令详解
translated: true
type: note
---

**问题：** Hermes Agent 中的复制命令是什么？

**答案：**

Hermes Agent（由 Nous Research 开发）没有传统意义上的“复制”命令用于复制文件。不过，它支持多种剪贴板及文件相关操作：

## 剪贴板操作

### 从剪贴板粘贴图片
Hermes 支持通过 Ctrl+V 或 /paste 命令直接从剪贴板粘贴图片到 CLI 进行视觉分析。具体方法包括：

1. **`/paste` 命令** - 输入 /paste 并按 Enter 键，即可检查剪贴板中的图片并附加。这是最可靠的方法，适用于所有环境。

2. **Ctrl+V** - 当剪贴板同时包含文本和图片时，Ctrl+V 也会自动检索图片（要求终端具备括号粘贴支持）。

3. **Alt+V** - 按 Alt+V 可检查剪贴板中的图片，但此功能在 VSCode 集成终端中不可用。

### 图片存储
从剪贴板粘贴的图片会自动以带时间戳的 PNG 文件格式保存到 ~/.hermes/images/ 目录下。

## 文件系统复制操作

尽管 Hermes Agent 的 CLI 中没有明确记录为专用的“复制”命令，但代理可访问终端工具，并能通过其终端工具执行如 `cp` 等标准的 Unix 命令来复制文件。

## 配置导出
对于复制配置数据（如 Browser Use API 密钥），Hermes 会使用 `hermes config set BROWSER_USE_API_KEY $(browser-use config get api_key)` 之类的命令在系统间复制密钥。

**参考资料：**

- [https://hermes-agent.nousresearch.com/docs/guides/tips/](https://hermes-agent.nousresearch.com/docs/guides/tips/)
- [https://hermes-agent.nousresearch.com/docs/user-guide/features/vision/](https://hermes-agent.nousresearch.com/docs/user-guide/features/vision/)
- [https://docs.browser-use.com/cloud/tutorials/integrations/hermes-agent](https://docs.browser-use.com/cloud/tutorials/integrations/hermes-agent)