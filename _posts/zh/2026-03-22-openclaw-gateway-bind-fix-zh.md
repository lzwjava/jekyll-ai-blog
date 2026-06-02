---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 OpenClaw 网关绑定验证错误
translated: true
type: note
---

**问题：** 错误 “Config validation failed: gateway.bind: gateway.bind host aliases (for example 0.0.0.0/localhost) are legacy; use bind modes (lan/loopback/custom/tailnet/auto) instead (auto-migrated on load)” 是什么意思，以及如何修复它？

**答案：**

## 这个错误的意思

这个错误来自 **OpenClaw**（或兼容的 gateway 工具如 ClawdBot），意思是你的配置文件中的 `gateway.bind` 设置使用了**过时/旧值**。

旧版本接受原始 IP 地址或主机名字符串，例如：

- `"0.0.0.0"`
- `"localhost"`
- `"127.0.0.1"`
- 特定的 Tailscale IP 地址（例如 `100.x.x.x`）

在 gateway 升级后（大约 2026.2.19 版本），配置验证器现在拒绝 `gateway.bind` 中设置的特定 IP 地址——这项破坏性变更与 bind 验证方式的更新一同引入。

系统现在要求使用**命名 bind 模式**，而不是原始 IP 或主机别名。

---

## 5 种有效的 Bind 模式

| Mode | 作用 |
|---|---|
| `loopback` | 绑定到 `127.0.0.1` — 仅本地机器（最安全，默认） |
| `lan` | 监听 `0.0.0.0`（所有接口）— 允许本地 LAN 访问 |
| `tailnet` | 绑定到 Tailscale IP（`100.64.0.0/10` 范围）— 用于 Tailscale 网络访问 |
| `custom` | 绑定到你定义的特定自定义地址 |
| `auto` | 自动选择最佳可用 bind 地址；当 loopback 不可用时回退 |

---

## “auto-migrated on load” 的意思

消息表示配置在加载时被**自动迁移**——意思是 gateway 尝试在运行时自动将你的旧旧值转换为最接近的匹配 bind 模式。但是，它仍然**警告/验证失败**，以提醒你配置文件已过时，需要手动更新。

---

## 如何修复

打开你的配置文件（通常是 `~/.openclaw/openclaw.json` 或 `OPENCLAW_CONFIG_PATH` 指向的位置），并更改 `gateway.bind` 字段：

**之前（旧版 — 会导致错误）：**

```json
{
  "gateway": {
    "bind": "0.0.0.0"
  }
}
```

**之后（正确）：**

```json
{
  "gateway": {
    "bind": "lan"
  }
}
```

### 选择正确的模式

- **仅本地访问**（同一台机器）：使用 `loopback`
- **从同一网络上的其他设备访问**：使用 `lan`
- **通过 Tailscale VPN 访问**：使用 `tailnet`（需要 Tailscale 运行）
- **不确定**：使用 `auto`

---

## 重要：非 Loopback 模式需要认证

非 loopback bind 模式（`lan`、`tailnet`、`custom` 或 `auto` 当 loopback 不可用时）需要配置认证——具体是 `gateway.auth.token` 或环境变量 `OPENCLAW_GATEWAY_TOKEN`。

如果你切换到 `lan` 或 `tailnet` 且未设置认证，下一步会得到“refusing to bind without auth”错误。

---

## 通过 CLI 快速修复

你也可以运行内置的迁移/修复工具：

```bash
openclaw doctor --fix
```

或干净地重新安装 gateway 服务：

```bash
openclaw gateway install --force
```

**参考资料：**

- [OpenClaw Troubleshooting Docs](https://docs.claw.so/engine/gateway/troubleshooting/)
- [GitHub Issue #21504 — gateway.bind IP validation after upgrade](https://github.com/openclaw/openclaw/issues/21504)
- [OpenClaw Security Docs](https://docs.openclaw.ai/gateway/security)
- [Configuring OpenClaw Gateway Bind on Azure](https://lucaberton.com/blog/configuring-openclaw-gateway-bind-and-control-ui/)
