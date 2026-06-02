---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Shadowrocket配置文件解析
translated: true
type: note
---

这似乎是 Shadowrocket 的配置文件，这是一款基于规则的 iOS 代理应用（类似于 Surge 或 Quantumult 等工具）。它采用基于文本的配置文件结构，定义了应用如何路由流量、处理 DNS、应用规则以及执行重写或 MITM（中间人）拦截。文件标注日期为 "2025-10-02 20:25:43"，可能是时间戳或占位符。

我将逐节解析，说明每个部分的作用及其配置原因。此配置似乎针对网络受限地区（如中国）的用户进行了优化，将某些全球/被屏蔽的服务通过代理服务器路由，同时保持本地/国内流量直连以获得更佳速度并避免不必要的重定向。这并非完整设置——您仍需在应用中单独配置代理服务器（例如通过 Shadowsocks、V2Ray 等），且此配置引用了从 GitHub 自动更新的外部规则集。

### 关键假设与说明
- **代理设置**：此配置假设您已在 Shadowrocket 中配置了可用的代理服务器（例如 SOCKS5、HTTP 或加密协议）。若无此设置，"PROXY" 规则将无法工作。
- **目的**：似乎用于规避审查（例如中国的防火长城）。AI 服务（如 OpenAI/ChatGPT）通过代理访问，而中文域名/IP 则直连以避免限速。
- **TUN 模式**：引用 "tun"（隧道模式）将所有设备流量通过代理路由。
- **外部依赖**：部分规则从 GitHub URL 加载（例如规则列表）。请确保信任这些来源，因为它们会自动更新。
- 如有任何不清楚之处或需要应用帮助，请告知您的设置详情。

### 各节详解

#### **[常规]**
设置全局应用行为、DNS 解析和网络路由。类似于 Shadowrocket 的"偏好设置"或"系统设置"。

- `bypass-system = true`：忽略 iOS 系统代理设置。Shadowrocket 自行处理所有代理，不依赖系统级配置。

- `skip-proxy = 192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,localhost,*.local,captive.apple.com,*.ccb.com,*.abchina.com.cn,*.psbc.com,www.baidu.com`：逗号分隔的域名/IP 范围列表，**始终直连**（不经过代理）。包括：
  - 私有网络（例如家庭 Wi-Fi IP，如 192.168.x.x）。
  - 本地域名（*.local）和 localhost。
  - Apple 的 captive portal 检查。
  - 中国银行域名（*.ccb.com 为中国建设银行，*.abchina.com.cn 为中国农业银行，*.psbc.com 为邮政储蓄银行）。
  - 百度（www.baidu.com），主要中文搜索引擎。
  - *原因？* 国内中文网站（尤其是银行和搜索）无需代理即可访问，且若经代理路由可能被限速或标记。

- `tun-excluded-routes = 10.0.0.0/8, 100.64.0.0/10, 127.0.0.0/8, 169.254.0.0/16, 172.16.0.0/12, 192.0.0.0/24, 192.0.2.0/24, 192.88.99.0/24, 192.168.0.0/16, 198.51.100.0/24, 203.0.113.0/24, 224.0.0.0/4, 255.255.255.255/32, 239.255.255.250/32`：在隧道（TUN）模式下，这些 IP 范围**排除**在代理隧道外。防止干扰本地/路由流量，如环回 IP、组播和测试范围。

- `dns-server = https://doh.pub/dns-query,https://dns.alidns.com/dns-query,223.5.5.5,119.29.29.29`：代理流量的优先 DNS 解析器列表。这些是 DoH（DNS over HTTPS）服务器和普通 DNS（腾讯的 119.29.29.29 和阿里云的 223.5.5.5）。以加密/公共服务器（doh.pub 和 alidns.com）开头以保障隐私/安全。

- `fallback-dns-server = system`：若主 DNS 失败，回退至 iOS 系统 DNS。

- `ipv6 = true`：启用 IPv6 支持。`prefer-ipv6 = false`：连接时优先使用 IPv4 而非 IPv6（例如出于稳定性或兼容性考虑）。

- `dns-direct-system = false`：直连时不使用系统 DNS——改用配置的 DNS。

- `icmp-auto-reply = true`：自动回复 ICMP（ping）请求。有助于连通性检查。

- `always-reject-url-rewrite = false`：允许触发 URL 重写（后续配置中使用）。

- `private-ip-answer = true`：允许包含私有 IP 的 DNS 响应（例如您的路由器）。

- `dns-direct-fallback-proxy = true`：若直连 DNS 查询失败，通过代理重试。

- `tun-included-routes = `：（空）TUN 模式下无自定义包含路由——使用默认值。

- `always-real-ip = `：（空）无强制真实 IP 暴露——标准行为。

- `hijack-dns = 8.8.8.8:53,8.8.4.4:53`：拦截来自 Google 公共 DNS（8.8.8.8/8.8.4.4 端口 53）的 DNS 流量，并通过代理路由。强制使用配置的 DNS 而非可能被屏蔽或监控的公共 DNS。

- `udp-policy-not-supported-behaviour = REJECT`：若策略不支持 UDP 流量，则拒绝而非允许。

- `include = `：（空）未包含额外配置文件。

- `update-url = `：（空）无来自 URL 的自动配置更新。

#### **[规则]**
定义流量路由规则，按顺序处理。类似于 ACL（访问控制列表），告知 Shadowrocket 基于域名、关键词、GEOIP 等条件决定代理或直连。若无规则匹配，则回退至 `FINAL,DIRECT`。

- `DOMAIN-SUFFIX,anthropic.com,PROXY`：将所有 anthropic.com 子域名通过代理路由（例如 api.anthropic.com）。Anthropic 为 AI 公司——可能用于绕过屏蔽。

- `DOMAIN-SUFFIX,chatgpt.com,PROXY`：将 ChatGPT 域名通过代理路由。ChatGPT 在某些地区常受限制。

- `DOMAIN-SUFFIX,openai.com,PROXY`：将 OpenAI 域名通过代理路由（类似原因）。

- `DOMAIN-SUFFIX,googleapis.com,PROXY`：将 Google API 服务通过代理路由（可能用于间接访问 Google 服务）。

- `DOMAIN-SUFFIX,zhs.futbol,DIRECT`：将此特定域名（可能为西班牙语/中文体育站点）直连。

- `RULE-SET,https://github.com/lzwjava/lzwjava.github.io/raw/refs/heads/main/scripts/auto-ss-config/AI.list,PROXY`：从 GitHub 加载外部规则集（AI 相关域名列表）并代理它们。此规则自动更新并扩展 AI 代理规则。

- `RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/Lan/Lan.list,DIRECT`：加载本地网络（LAN）域名规则集并直连。避免代理家庭/内部流量。

- `DOMAIN-KEYWORD,cn,DIRECT`：任何包含关键词 "cn" 的域名（例如 anything.cn）直连。适用于中文网站。

- `GEOIP,CN,DIRECT`：任何地理定位为中国的 IP 直连。防止代理国内流量，此类流量快速且无限制。

- `FINAL,DIRECT`：默认操作——若无规则匹配，则直连。保持多数流量不经代理以提高效率。

*整体效果*：此为"代理被屏蔽全球服务"的设置。AI/ChatGPT/OpenAI 流量强制通过 VPN/代理以绕过地区限制，而中文/本地内容保持直连。

#### **[主机]**
手动主机映射（类似本地 hosts 文件）。

- `localhost = 127.0.0.1`：将 "localhost" 映射至环回 IP。标准设置——确保应用可连接本地服务。

#### **[URL 重写]**
在请求发出前重写传入 URL。使用正则表达式匹配。

- `^https?://(www.)?g.cn https://www.google.com 302`：重写任何 g.cn（或 www.g.cn）的 HTTP/HTTPS URL，以 302 状态（临时重定向）跳转至 google.com。g.cn 为 Google 中国域名——此操作绕过它。

- `^https?://(www.)?google.cn https://www.google.com 302`：同样将 google.cn 重写至 google.com。中国常屏蔽或重定向 google.com，此操作强制清洁重定向。

*原因？* 在审查地区，google.cn 可能提供篡改/被禁结果。此设置确保直接访问全球 Google 站点。

#### **[MITM]**
用于拦截和修改 HTTPS 流量的中间人设置（需在 Shadowrocket 中安装根 CA 证书）。

- `hostname = *.google.cn`：拦截任何 google.cn 子域名的流量。结合 URL 重写，可能用于解密/重定向 Google 中国域名流量。

*原因？* 可能用于强制执行重写或处理中国境内的证书固定问题，其中 google.cn 使用不同证书。

### 如何使用此配置
1. **导入**：在 Shadowrocket 中，将此文件作为配置导入。
2. **代理服务器**：在"服务器"部分添加实际代理（例如 Shadowsocks 服务器）——"PROXY" 等规则依赖于此。
3. **启用**：切换至此配置，并在需要时启用隧道模式（VPN）。
4. **CA 证书**：对于 MITM，若未完成，安装并信任 Shadowrocket 的 CA。
5. **测试**：访问如 whatismyipaddress.com 等站点检查 IP/路由是否按预期工作。监控中文站点是否缓慢。
6. **故障排除**：若规则集加载失败，可能因限速或变更。IPv6 偏好设置可能需要切换以解决连通性问题。

### 潜在问题/安全说明
- **隐私**：暴露的规则集（GitHub 链接）可能泄露您的路由内容。MITM 可拦截敏感流量——仅使用受信任的 CA。
- **更新**：规则集自动加载；若 GitHub 被屏蔽，需使用代理访问它们。
- **未来日期**：配置标注 2025 年 10 月——可能为笔误或未来验证，但无功能依赖于此。
- **合法性**：为规避审查使用代理在某些地区允许，但在其他地区受限——请自行承担风险。
- 若您分享错误日志或目标，我可提供更精准建议！
