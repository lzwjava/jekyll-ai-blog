---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Discord更新程序绕过代理
translated: true
type: note
---

## 诊断 — 根本原因已确认

我精确追踪到了 Discord 卡在“检查更新”的原因。**并非**代理规则的问题——而是 Discord **更新子进程根本没有使用代理**。

**发生了什么**（来自更新程序自身日志的证据）：

`~/Library/Application Support/discord/logs/Discord_updater_rCURRENT.log` 每约 75 秒重复出现：

```
ERROR [updater_client]: Failed 16 ... host: updates.discord.com
  source: hyper::Error(Connect, ConnectError("tcp connect error",
  Os { code: 60, kind: TimedOut, message: "Operation timed out" }))
```

**原因：**
1. Discord 的应用更新程序（`.../Resources/updater.node`，一个 Rust `reqwest` 客户端）会向 `https://updates.discord.com/...` 发起**原始 TCP 套接字**连接 → 解析为 `54.89.135.129:443`。
2. 该客户端**不遵循** HTTP(S) 系统代理（127.0.0.1:7890）也不遵循 `HTTPS_PROXY` 环境变量。
3. 从该网络直接无法访问该 IP/域名。

我通过实时测试确认了这种不对称性：

| 连接方式 | 结果 |
|---|---|
| **直接连接（无代理）**，`--noproxy '*'` | ❌ `Connection timed out after 15s` |
| **通过 mihomo** `127.0.0.1:7890` | ✅ HTTP 200 响应，耗时 0.34 秒 |

我的 shell 中 `curl` 能正常工作，是因为终端环境设置了 `https_proxy=http://127.0.0.1:7890` ——但从 Finder/Dock 启动的更新程序无法继承该环境变量。

**为什么你的规则未能捕获它：** `~/.config/mihomo/config.yaml` 中已存在 `DOMAIN-SUFFIX,discord.com → Proxy` 规则，因此 `updates.discord.com` 能被正确匹配。问题在于，该规则仅在流量**到达 mihomo 时**才生效。更新程序的原始套接字从未经过 mihomo，因为你运行 mihomo 时仅使用**代理模式（无 TUN）**。

## 正确的解决方案：启用 mihomo TUN 模式

你的二进制文件已经是 `with_gvisor` 构建版本（支持 TUN），因此持久化的解决方案是让 mihomo 拦截**所有**流量——包括绕过代理的原始套接字。启用 TUN 后，更新程序对 `54.89.135.129` 的直接连接将被捕获，由规则匹配（`discord.com → Proxy`），并通过你的 Hysteria2/SS 节点进行隧道传输。

为此，我需要在配置中添加：

```yaml
tun:
  enable: true
  stack: system        # 或 gvisor
  auto-route: true
  auto-redirect: true
  auto-detect-interface: true
  dns-hijack:
    - any:53
```

然后重启 mihomo。⚠️ 这需要**管理员权限**（TUN 需要 root/网络权限），并且 mihomo 重启期间会有**短暂的断连**——因此我不希望在会话中途修改，以免切断你当前的连接。

## 临时解决方案（在启用 TUN 之前）

如果更新程序在代理环境中运行，它就能正常工作——但你需要确保它处于该环境。两种快速方案：

- **最佳快速修复：** 在 macOS 上，让更新程序使用你的 `HTTPS_PROXY` 环境变量——由于更新程序遵循 `HTTPS_PROXY` 环境变量，通过终端启动 Discord 使其继承该变量即可生效，但这种方式仅在保持该变量设置时才持久有效。
- **更可靠的方法：** 启用 TUN（如上所述）。

需要我现在应用 TUN 配置更改并重启 mihomo 吗？我需要先确认两件事：（1）你是否能接受短暂的连接中断；（2）mihomo 能否获取管理员/网络权限（你是通过特权助手/代理运行它，还是我们应该将其配置为使用 utun 接口）。另外，如果你告诉我 mihomo 的启动方式（普通终端？登录项？），我可以给你提供精确的安全操作步骤。