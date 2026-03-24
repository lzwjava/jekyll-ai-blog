---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Claude Code 路由启动超时问题
translated: true
type: note
---

**Question:** 为什么 Claude Code Router (`ccr`) 启动失败，即使 `ccr restart` 显示成功后仍显示 "Service startup timeout"？

**Answer:**

这是一个关于 `claude-code-router` 非常常见且已有记录的问题。以下是最可能的原因及修复方法：

---

## Root Causes

### 1. `$PATH` 中找不到 `claude` 命令 (在 Mac/zsh 上最常见)

服务会静默崩溃并报错 `/bin/sh: claude: command not found`，因为 `ccr` 使用 `/bin/sh` 启动后台服务，而 `/bin/sh` **不会**加载你的 shell aliases 或 `~/.zshrc`。如果 `claude` 是以 alias 形式安装（例如 `alias claude=...`），或者其路径仅存在于 `.zshrc` 中，则 daemon 进程将无法找到它。

**Fix:** 确保 `claude` 在标准 `PATH` 路径下是一个真实可执行的 binary，而不仅仅是一个 shell alias。检查方法：

```bash
which claude        # 应该返回一个真实路径，而不是 "aliased to..."
ls -la $(which claude)
```

如果它只是一个 alias，请将真实路径添加到 `/etc/paths` 或创建一个 symlink：

```bash
sudo ln -sf ~/.claude/local/claude /usr/local/bin/claude
```

---

### 2. Config 文件缺失或格式错误

大多数启动失败归结为端口冲突或 `config.json` 文件格式错误。最常见的配置错误是 `Providers` 中的模型名称与 `Router` 中的模型名称不匹配 —— 两者必须完全一致。

检查你的配置：

```bash
cat ~/.claude-code-router/config.json
```

确保它是有效的 JSON（没有注释，没有末尾逗号），并且 provider 模型名称与 router 模型名称完全匹配。

---

### 3. Port 3456 已被占用

如果端口被占用或服务启动失败，你会看到 connection refused 错误。检查 `~/.claude-code-router/logs/` 中的 server logs 获取详细信息。

```bash
lsof -i :3456
```

如果该端口已被占用，请终止该进程或配置不同的端口。

---

### 4. Router 自身的已知 Race Condition Bug

`claude-code-router` 服务曾存在一个 race condition，即在服务器启动期间到达的 HTTP 请求可能会访问到未定义的 `providerService`。该问题源于 constructor 模式：JavaScript 中的 constructors 是同步的并会立即返回，但原始代码在回调中启动了 `ProviderService` 的异步初始化。这导致了间歇性的启动失败。

**Fix:** 更新到最新版本：

```bash
npm update -g @musistudio/claude-code-router
```

---

## Debugging Steps

1. **直接检查日志：**
```bash
tail -f ~/.claude-code-router/logs/$(ls -t ~/.claude-code-router/logs/ | head -1)
```

2. **在前台手动运行 `ccr start`** 以查看实际的错误输出：
```bash
ccr start
```

3. **验证 `claude` 是否可以从非交互式 shell 访问：**
```bash
/bin/sh -c "which claude"
```

4. **在 `ccr restart` 报告成功后，检查服务是否真的在运行：**
```bash
ccr status
curl http://127.0.0.1:3456
```

---

## Summary Table

| Cause | Fix |
|---|---|
| `claude` 不在 `/bin/sh` PATH 中 | 创建 Symlink 到 `/usr/local/bin/claude` |
| `config.json` 格式错误 | 验证 JSON，修复模型名称不匹配问题 |
| Port 3456 被占用 | `lsof -i :3456` 并杀掉进程 |
| CCR 版本 Bug (race condition) | `npm update -g @musistudio/claude-code-router` |

**References:**

- [Issue #544: CCR start and then stop immediately](https://github.com/musistudio/claude-code-router/issues/544)
- [Issue #211: running `ccr code` asks to run service manually](https://github.com/musistudio/claude-code-router/issues/211)
- [Issue #1258: Fixing the ProviderService Race Condition](https://github.com/musistudio/claude-code-router/issues/1258)
- [DataCamp: Claude Code Router tutorial](https://www.datacamp.com/tutorial/claude-code-router)