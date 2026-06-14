---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 诊断Tailscale SSH直接连接
translated: true
type: note
---

## 诊断流程 — Tailscale SSH 延迟问题

**1. SSH 配置检查**

```bash
cat ~/.ssh/config
```

发现 `lzw-to` 配置了 `ProxyCommand none`，且通配规则 `Host !192.168.*.*` 通过 SOCKS5 代理路由。

**2. Tailscale 状态及中继信息**

```bash
ssh lzw@<TAILSCALE_IP> "tailscale status"
```

显示 Mac 通过 `relay "sin"`（新加坡）连接。

**3. 对端 Tailscale ping 及网络检测**

```bash
ssh lzw@<TAILSCALE_IP> "tailscale ping -c 3 --until-direct <TAILSCALE_IP_MAC>"
ssh lzw@<TAILSCALE_IP> "tailscale netcheck"
```

关键发现：`direct connection not established`，DERP(sin) 延迟 324–914ms，最近 DERP 节点在 LAX 延迟 163ms，无 IPv6，`PortMapping:` 为空。

**4. Mac 端 Tailscale 网络检测**

```bash
tailscale netcheck
```

结果：`Nearest DERP: Singapore (54ms)`，`PortMapping: UPnP`，公网 IP `<IP_ADDRESS>`。

**5. 可达性测试**

```bash
ping <IP_ADDRESS>                    # 对端公网 IP — 100% 丢包（NAT 阻止 ICMP）
ssh dmit "ping -c 3 <IP_ADDRESS>"   # 从 DMIT 测试 — 同样 100% 丢包
```

**6. NAT 类型及端点发现**

```bash
ssh lzw@<TAILSCALE_IP> "tailscale status --json" | python3 -c "..."
```

解析 JSON 获取 `RelayName`、`CurAddr`、`Endpoints`、`NATType`。

**7. 守护进程日志及 STUN 测试**

```bash
ssh lzw@<TAILSCALE_IP> "journalctl -u tailscaled -n 10"
ssh lzw@<TAILSCALE_IP> "nc -u -z -v stun.l.google.com 19302"
ssh lzw@<TAILSCALE_IP> "tailscale debug prefs"
```

STUN 正常工作，已发现端点（`<IP_ADDRESS>:<PORT>`），确认为锥形 NAT。

**8. 强制直连**

```bash
tailscale ping --until-direct -c 5 <TAILSCALE_IP>
```

成功建立直连：`via <IP_ADDRESS>:<PORT> in 76ms`。

**9. 验证 SSH 性能提升**

```bash
time ssh lzw-to "echo connected; hostname; uptime"
```

从 5–6 秒 → 1.9 秒。

---

所有命令均通过普通 `terminal()` 工具执行 — 包括远程服务器的 SSH 连接、本地 `tailscale` 命令行、`ping`、`nc`、`journalctl`，以及通过 Python 解析 `tailscale status --json` 的 JSON 数据。
