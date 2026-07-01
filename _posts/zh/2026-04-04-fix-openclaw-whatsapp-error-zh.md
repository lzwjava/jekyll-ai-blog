---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复OpenClaw WhatsApp代理错误
translated: true
type: note
---

问：如何修复 OpenClaw 网关错误 “channels.whatsapp: Unrecognized key: proxy”（位于 `~/.openclaw/openclaw.json` 中）？

答：

## 根因

`channels.whatsapp` 下的 `proxy` 键**目前还不是 OpenClaw 支持的配置选项**。截至 2026 年 2 月，已有人提交功能请求（Issue #23500）要求为 WhatsApp 连接添加代理支持——类似于 `channels.telegram.proxy` 已有的功能——但尚未实现。

这意味着，如果您手动在 `channels.whatsapp` 配置中添加了 `"proxy": "..."`（可能是受 Telegram 代理配置的启发，或是遵循了过时的指南），OpenClaw 的配置验证器会将其视为无法识别的键并拒绝启动。

---

## 如何修复

### 选项 1 —— 运行自动修复命令（推荐的第一步）

```bash
openclaw doctor --fix
```

`doctor --fix` 命令会自动迁移已知的已弃用或无效的键。运行后，请重新尝试启动网关。

---

### 选项 2 —— 手动从配置中移除 `proxy` 键

1. 打开配置文件：

```bash
nano ~/.openclaw/openclaw.json
```

2. 找到 `channels.whatsapp` 部分。它可能类似这样：

```json
"channels": {
  "whatsapp": {
    "proxy": "http://127.0.0.1:7890",
    ...
  }
}
```

3. **完全删除 `"proxy": "..."` 这一行**，保存并退出。

4. 重启网关：

```bash
openclaw gateway restart
```

---

### 选项 3 —— 先验证配置结构

运行以下命令以在编辑前查看所有无效键：

```bash
openclaw config validate
```

然后修复每个报告的问题键。

---

## 代理需求变通方案（如果您身处受限地区）

由于 OpenClaw 尚未实现 WhatsApp 代理支持，在 WhatsApp 被屏蔽的地区（例如中国大陆）的用户应在启动 OpenClaw 前设置系统级的代理环境变量：

```bash
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
openclaw gateway restart
```

这会将所有出站连接（包括 WhatsApp WebSocket）在操作系统级别通过您的代理进行路由，而无需触及 OpenClaw 配置文件。

---

## 总结表格

| 步骤 | 命令 |
| ------ | --------- |
| 自动修复配置 | `openclaw doctor --fix` |
| 手动编辑 | 从 `~/.openclaw/openclaw.json` 中的 `channels.whatsapp` 里移除 `"proxy"` |
| 重启网关 | `openclaw gateway restart` |
| 系统代理变通方案 | 启动 OpenClaw 前执行 `export http_proxy=...` |

参考：

- [功能请求：WhatsApp 代理支持（Issue #23500）](https://github.com/openclaw/openclaw/issues/23500)
- [OpenClaw 网关故障排除流程图](https://clawtank.dev/blog/openclaw-gateway-troubleshooting-flowchart)
- [OpenClaw 故障排除指南](https://docs.openclaw.ai/gateway/troubleshooting)
- [Bug：WhatsApp 通道配置损坏（Issue #24263）](https://github.com/openclaw/openclaw/issues/24263)
