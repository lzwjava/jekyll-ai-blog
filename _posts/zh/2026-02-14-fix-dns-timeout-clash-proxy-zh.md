---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 通过 Clash 代理修复 DNS 超时问题
translated: true
type: note
---

**Question: 在不导出 proxy 环境变量的情况下，Python 脚本查询 Cloudflare DoH (https://1.1.1.1/dns-query) 超时。如何在中国寻找合适的 DNS server，或者能否通过 Clash proxy 转发 DNS 请求？**

**Answer:**

你的测试展示了中国大陆的一个经典问题：直接访问像 `https://1.1.1.1/dns-query` 这样的国外 DoH server 通常会因为 **GFW 级别的封锁**（TLS handshake 或 SNI filtering）而失败或超时，即使普通的 UDP DNS 到 1.1.1.1 可能部分可用。

当你将 `HTTP_PROXY`/`HTTPS_PROXY` 设置为 Clash (127.0.0.1:7890) 时，`requests` 库会自动将 DoH HTTPS 请求通过你的 proxy 建立 tunnel -> 请求成功，因为 proxy 节点绕过了封锁。

当你取消 proxy 设置 (`stop_proxy`) 时，Clash 不再处理传出的 HTTPS 连接 -> 机器发起的直接连接超时。

### Solution 1: 通过 proxy 转发 Clash 自身的 DNS 查询 (DoH/DoT) (推荐)

Clash（特别是 Meta/Mihomo core）支持将其 upstream DNS 查询 (nameserver / fallback) **通过特定的 proxy** 或 group 发送。这非常适合你的情况。

像这样更新你的 Clash config：

```yaml
dns:
  enable: true
  ipv6: false
  enhanced-mode: fake-ip          # 或 redir-host
  fake-ip-range: 198.18.0.1/16
  listen: 0.0.0.0:53              # 可选，用于 TUN/系统级

  # 快速的国内 DNS，用于解析 proxy 节点域名 + bootstrap
  default-nameserver:
    - 119.29.29.29                # DNSPod
    - 223.5.5.5                   # AliDNS

  # 主 DoH – 强制通过你的 proxy group
  nameserver:
    - https://1.1.1.1/dns-query#PROXY     # ← #PROXY 表示使用名为 "PROXY" 的 group
    - https://1.0.0.1/dns-query#PROXY

  # 针对污染结果的 Fallback
  fallback:
    - https://cloudflare-dns.com/dns-query#PROXY
    - tls://1.1.1.1#PROXY                 # DoT 备选

  # 可选：仅对非 CN 站点使用 fallback
  fallback-filter:
    geoip: true
    ipcidr:
      - 240.0.0.0/4

  # 防止“鸡生蛋”问题：直接解析 proxy 节点的域名
  proxy-server-nameserver:
    - 119.29.29.29
    - 223.5.5.5
```

- 假设你有一个名为 `"PROXY"` 的 proxy-group（或者改为你的实际组名，例如 `🐟 漏网之鱼`）。
- `#PROXY` 语法告诉 Clash 通过指定的 proxy/group 路由 **该特定的 DoH 连接**，而不是直接连接。
- 重载/重启 Clash 后 -> 你的 Python 脚本**即使不设置** `HTTP_PROXY` 环境变量也应该可以工作，因为 Clash 的内置 DNS（如果你在使用它）或你的脚本（如果通过 tunnel）间接受益。

如果你的 core 是旧版 Clash（不是 Meta），可能不支持 `#proxyname` 语法 -> 请升级到 Clash Meta / Mihomo / Clash Verge Rev。

### Solution 2: 使用国内 / 针对中国优化的 DoH / DoT server (DNS 不需要 proxy)

许多 server 在中国可以不通过 proxy 稳定工作：

- `https://doh.pub/dns-query` (非常流行且快速，DoH)
- `https://dns.alidns.com/dns-query` (AliDNS DoH)
- `https://doh.360.cn/dns-query` (360 DoH)
- `tls://223.5.5.5:853` (AliDNS DoT)
- `tls://223.6.6.6:853` (AliDNS 次要 DoT)

最小化配置示例：

```yaml
dns:
  enable: true
  nameserver:
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query
  fallback:
    - tls://223.5.5.5:853
```

这些通常不会被封锁，对于国内 + 国际解析都很快速（尽管在敏感域名上可能会有一些污染 -> 配合 fallback-filter 使用）。

### Solution 3: 在脚本中继续使用环境变量 (简单，无需更改配置)

始终在跑 DNS 测试脚本时启用 proxy：

```bash
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
python ./scripts/clash/try_dns.py
```

或者将其包装在你的 `start_proxy` alias/脚本中。

### 快速测试命令 (Terminal)

- 通过 Clash proxy 测试 DoH：`curl -x http://127.0.0.1:7890 -H "accept: application/dns-json" "https://1.1.1.1/dns-query?name=www.google.com&type=A"`
- 直接测试（应该会超时/失败）：`curl -H "accept: application/dns-json" "https://1.1.1.1/dns-query?name=www.google.com&type=A"`

这证实了封锁发生在直接连接到 Cloudflare DoH 的出站 HTTPS 上。

使用 `#PROXY` 方法是长期解决该问题的最优雅方式。

**References:**

- [MetaCubeX mihomo DNS Configuration (nameserver #proxy support)](https://wiki.metacubex.one/en/config/dns)
- [Clash DNS upstream through proxy discussion](https://github.com/MetaCubeX/mihomo/discussions/1434)
- [Common Clash DNS setups for China](https://github.com/Loyalsoldier/clash-rules)