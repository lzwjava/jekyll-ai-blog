---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Discord更新挂起分析审查
translated: true
type: note
---

我已审阅您分享的 Discord 挂起分析。内容全面且技术准确。以下是我的评估：

## 对您 Discord“检查更新”挂起问题的分析回顾

### ✅ 准确之处

1. **更新服务器不可达** — 您对启动流程（检查清单 → 下载 → 验证 → 启动）的分析是正确的。Discord 使用 `updates.discord.com` 和 Squirrel（Windows）/ Electron 自动更新器，这些服务器**确实**经常从中国大陆被屏蔽或出现降级。您给出的 `curl` 诊断命令是正确的第一步。

2. **缓存损坏** — Electron 的本地更新状态（`%AppData%/Discord`、`%LocalAppData%/Discord`）是导致持续挂起循环的常见原因。`rmdir` 加重新安装的方法虽然彻底，但可靠。

3. **DNS 路由** — 中国 ISP（中国电信、联通、移动）经常返回通往 Cloudflare IP 的非最优路由。您建议使用 `1.1.1.1` / `8.8.8.8` 很好，但需注意 `8.8.8.8` 本身从中国访问可能会有较高延迟。由于 Cloudflare 与百度的中国合作，`1.1.1.1` 通常更可靠。

4. **代理/VPN 不匹配** — 关键点：Squirrel 更新器继承系统代理设置，但 Discord 的 Electron 应用使用自己的 Chromium 网络栈，可能不继承。这种“脑裂”场景极为常见。

### 🔍 细微之处 / 补充

| 要点 | 您的分析 | 我的补充 |
|-------|--------------|--------------|
| **TLS 指纹识别** | 未提及 | 中国的 DPI（深度包检测）即使通过 Cloudflare IP 也能检测并阻断 Discord 的 TLS 握手。简单的 curl 检查可能显示连接正常，但由于 SNI 层面的封锁，完整的更新下载仍可能失败。 |
| **Squirrel 更新协议** | 概述良好 | Discord 使用 Squirrel（Windows）/ Squirrel.Mac。它首先检查 `RELEASES` 文件，然后下载各个 `.nupkg` 包。如果 `RELEASES` 文件下载失败或返回过期响应，更新会静默挂起。 |
| **`Hosts` 文件干扰** | 未提及 | 用户常为 VPN 分流将 Discord IP 添加到 `/etc/hosts` 或 `C:\Windows\System32\drivers\etc\hosts`。指向旧 IP 的过期 hosts 条目会导致更新器挂起。 |
| **Windows Update / 后台智能传输服务 (BITS)** | 未提及 | Squirrel 可使用 BITS 进行后台下载。如果 BITS 被禁用或损坏，更新会挂起。`net start bits && sc query bits` 可验证此状态。 |
| **macOS 变体** | 以 Windows 为主 | 在 macOS 上，Discord 将更新存储在 `~/Library/Application Support/discord/` 中。基于 `.dmg` 的更新器略有不同，但原理相同。 |

### 💡 为您工具箱增加的额外诊断方法

```bash
# 检查 Discord 域名是否解析到被屏蔽或保留的 IP
for domain in discord.com updates.discord.com cdn.discordapp.com; do
  echo "=== $domain ==="
  nslookup $domain 2>&1 | tail -3
  curl -sI "https://$domain" -o /dev/null -w "HTTP %{http_code}, Time: %{time_total}s\n" --connect-timeout 5
done

# 检查分流代理路由
curl -s --proxy http://127.0.0.1:7890 https://discord.com -o /dev/null -w "Via proxy: %{http_code}\n"
curl -s --noproxy '*' https://discord.com -o /dev/null -w "Direct: %{http_code}\n"
```

### 🔗 与本项目的关联

您的分析与 `ww` 中现有工具高度契合：

| 现有 ww 工具 | 覆盖范围 |
|---|---|
| `ww network ip-scan / port-scan` | 网络诊断层 |
| `ww clash query-dns` | DNS 解析检查 |
| `ww macos settings-proxy / linux proxy-setup` | 代理配置 |
| `ww utils request-proxy` | 代理感知的 HTTP 请求 |
| `ww.try.solve` | 通用问题解决方法论 |

如果您愿意，可以将此 Discord 专有诊断流程添加为新命令（例如 `ww try discord-diagnose`），利用现有的 `ww/network/` 和代理工具。需要我起草该命令吗？