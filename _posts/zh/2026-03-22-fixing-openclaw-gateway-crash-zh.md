---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 OpenClaw 网关崩溃和警告
translated: true
type: note
---

**问题：** 如何修复持续崩溃的 `openclaw-gateway.service`，错误为 `error: unknown option '--host'` 以及 Telegram 群组策略警告？

**答案：**

您的日志显示 **两个不同问题** — 一个是致命崩溃（`--host` 选项错误），另一个是 Telegram 警告。分别修复它们：

---

## 问题 1（致命）：`error: unknown option '--host'`

这是崩溃循环的根本原因（重启计数器已达 131+）。gateway 启动命令传递了一个 **无效选项** `--host` 标志，该标志对当前版本的 OpenClaw 来说 **不是有效选项**。错误消息本身提示：`(Did you mean --port?)`。

这种情况通常发生在：

- 您的配置中有 `gateway.host` 键，CLI 错误地将它转换为 `--host` 标志，或者
- systemd 服务单元的 `ExecStart` 行中手动编辑了 `--host`，这在 v2026.x 中不再有效

### 修复步骤

**步骤 1 — 删除无效的 `gateway.host` 配置键：**

```bash
openclaw config set gateway.bind "localhost"
```

或者如果您特别想设置端口：

```bash
openclaw config set gateway.port 3001
```

**不要** 使用 `gateway.host` — 某些旧设置的正确配置键是 `gateway.host`，但当前推荐的修复是 `openclaw config set gateway.bind "localhost"` 和 `openclaw config set gateway.port 3001`。

**步骤 2 — 运行自动修复 doctor：**

```bash
openclaw doctor --fix
```

`openclaw doctor --fix` 运行健康检查并自动修复常见问题，包括权限、配置和缺失目录。

**步骤 3 — 检查您的 systemd 服务单元** 是否有硬编码的 `--host` 标志：

```bash
systemctl --user cat openclaw-gateway.service
```

如果在 `ExecStart=` 行中看到 `--host`，则编辑删除它：

```bash
systemctl --user edit openclaw-gateway.service
```

删除 `--host` 参数并保存。

**步骤 4 — 重新安装并重启 gateway：**

```bash
openclaw gateway install --force
openclaw gateway restart
```

或者通过 systemd：

```bash
systemctl --user restart openclaw-gateway
```

---

## 问题 2（警告）：Telegram 群组消息被静默丢弃

日志警告：

> `channels.telegram.groupPolicy is "allowlist" but groupAllowFrom (and allowFrom) is empty — all group messages will be silently dropped.`

这不会导致服务崩溃，但意味着您的 bot 会忽略所有 Telegram 群组消息。用 **以下两个选项之一** 修复它：

**选项 A — 将允许的发送者 ID 添加到允许列表：**

```bash
openclaw config set channels.telegram.groupAllowFrom '[-1001234567890]'
```

用您的实际 Telegram 群组聊天 ID 替换该数字。

**选项 B — 对所有人开放群组消息（安全性较低）：**

```bash
openclaw config set channels.telegram.groupPolicy "open"
```

---

## 要运行的命令摘要

```bash
# 1. 修复 host 配置问题
openclaw config set gateway.bind "localhost"
openclaw config set gateway.port 3001

# 2. 自动修复其他配置问题
openclaw doctor --fix

# 3. 修复 Telegram 群组策略（选择一个）
openclaw config set channels.telegram.groupPolicy "open"
# 或者将特定群组 ID 添加到允许列表

# 4. 重新安装并重启
openclaw gateway install --force
openclaw gateway restart

# 5. 验证其稳定性
openclaw status
openclaw logs --follow
```

重启后，崩溃循环应该停止，重启计数器应该冻结。

**参考资料：**

- [OpenClaw Official Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting)
- [ClawTank: Fix Common Errors](https://clawtank.dev/blog/openclaw-troubleshooting-common-errors)
- [LumaDock: OpenClaw Deep Troubleshooting](https://lumadock.com/tutorials/openclaw-troubleshooting-common-errors)
- [Zeabur: OpenClaw Troubleshooting](https://zeabur.com/blogs/openclaw-troubleshooting-on-zeabur)
