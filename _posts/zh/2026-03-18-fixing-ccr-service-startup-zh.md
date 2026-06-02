---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 CCR 代码服务启动问题
translated: true
type: note
---

Question: 为什么最近 `ccr code` 不工作，显示 "Service not running, starting service..." 然后停止？

Answer:

这是 Claude Code Router (CCR) 的 **已知且常见问题**。根据 GitHub issues，有几个根本原因：

---

## 根本原因

### 1. `claude` 命令在 PATH 中未找到（最常见）

当 `ccr code` 尝试自动启动服务并启动 Claude Code 时，它会在 `/bin/sh` 子进程中运行 `claude` —— 该进程可能无法继承您的 shell 别名或 PATH。错误 `/bin/sh: claude: command not found` 出现是因为 `claude` 命令被设置为 shell 别名（例如，`claude: aliased to /Users/.../.claude/local/claude`），但 `/bin/sh` 不会加载 shell 别名。

**修复：** 先在终端中单独运行 `ccr start`，然后使用 `ccr code`。或者将完整的 Claude 二进制路径添加到 `/etc/paths` 或您的 shell 的 `PATH` 中，以使 `/bin/sh` 能够找到它。

### 2. 服务启动超时

`ccr code` 在等待后台服务启动时超时，并显示 "Service startup timeout, please manually run `ccr start`."。

**修复：** 先手动运行 `ccr start`，等待它确认正在运行，然后运行 `ccr code`。

### 3. 未设置 `ANTHROPIC_BASE_URL`（路由失败）

`ccr code` 命令启动了 router 服务，但在启动 Claude Code 子进程之前未能设置 `ANTHROPIC_BASE_URL` 环境变量，导致 Claude Code 直接连接到 Anthropic API，而不是配置的 CCR proxy。

**修复：** 手动启动并导出：
```bash
ccr start
export ANTHROPIC_BASE_URL="http://127.0.0.1:3456"
export ANTHROPIC_API_KEY="routing-key"
claude
```

或者使用 `ccr activate`：
```bash
eval "$(ccr activate)"
claude
```

### 4. `claude` 二进制文件权限被拒绝

在某些系统（例如 Windows 上的 WSL2）上，错误为 `/bin/sh: claude: Permission denied`，表示 claude 二进制文件存在但不可执行。

**修复：**
```bash
chmod +x ~/.claude/local/claude
```

---

## 通用调试步骤

1. **检查服务状态：**
   ```bash
   ccr status
   ```

2. **手动启动服务：**
   ```bash
   ccr start
   ```

3. **检查日志** 以获取详细错误消息：
   ```bash
   tail -f ~/.claude-code-router.log
   ```

4. **验证 `claude` 是否可从非交互式 shell 访问：**
   ```bash
   /bin/sh -c "which claude"
   ```
   如果此命令无输出，则 PATH 是问题所在。

5. **使用 `ccr activate` 作为变通方法：**
   ```bash
   eval "$(ccr activate)"
   claude
   ```
   `activate` 命令设置 `ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_BASE_URL` 和 `NO_PROXY` 环境变量，从而使 `claude` 命令自动通过 router 路由请求。

6. **更新 CCR** —— 这是一个反复出现的问题，随着时间推移发布了修复：
   ```bash
   npm update -g @musistudio/claude-code-router
   ```

---

## 总结

根本问题是后台服务未能干净启动，或者 `claude` 二进制文件在 `ccr code` 使用的子进程 shell 中未找到/不可访问。最可靠的变通方法是 **显式运行 `ccr start`，然后激活环境变量后直接使用 `claude`**。

References:

- [CCR Issue #544: CCR start and then stop immediately](https://github.com/musistudio/claude-code-router/issues/544)
- [CCR Issue #211: running `ccr code` asks to run service manually](https://github.com/musistudio/claude-code-router/issues/211)
- [CCR Issue #327: Error starting `ccr code` — Permission denied](https://github.com/musistudio/claude-code-router/issues/327)
- [CCR Issue #1137: `ccr code` not passing routing config to Claude Code subprocess](https://github.com/musistudio/claude-code-router/issues/1137)
- [Claude Code Router GitHub README](https://github.com/musistudio/claude-code-router)
