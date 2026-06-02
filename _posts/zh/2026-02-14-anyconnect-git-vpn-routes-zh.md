---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: AnyConnect 通过 VPN 路由 Git 流量
translated: true
type: note
---

Question: macOS 上的 Cisco AnyConnect 等软件是否会强制通过 SSH 进行的 git pull 走 VPN/proxy？如果我使用 Cisco AnyConnect，是否不需要在环境变量或系统设置中设置 HTTP/HTTPS proxy？

Answer:

**是的——在大多数企业级设置中，Cisco AnyConnect 会强制你通过 SSH 进行的 `git pull` 经过 VPN tunnel。**
这是因为 AnyConnect 通常会修改 macOS 的 routing table，将**所有**（或大部分）出站流量通过企业 VPN 发送——包括指向 github.com 或其他 git 托管商在 TCP port 22 上的 SSH 流量。

### 关于 Cisco AnyConnect 在 macOS 上行为的关键点

- **Full tunnel (企业中最常见)**:
  VPN server 会推送一个策略（通常是 "tunnel-all" 或 "full tunnel"）来更改你的 default route。
  → **所有 internet 流量**——包括到 github.com 的 SSH (port 22)、基于 HTTPS 的 git (port 443)、浏览器等——都会经过 VPN tunnel。
  → 你的 `git pull` (SSH) 会自动使用 VPN 路径，无需任何额外配置。

- **Split tunnel (较少见，但可能存在)**:
  只有特定的企业 IP 范围/子网会经过 VPN；其他所有内容（如 github.com）都会直接通过你的普通 internet 连接。
  → 在这种情况下，连接到公共 git 托管商的 SSH 会**绕过** VPN（与 VPN 关闭时相同）。

出于安全/合规原因（强制所有流量经过企业 firewall、proxy、检测、DLP 等），大多数公司使用 **full tunnel**。因此在实践中：**是的，当 AnyConnect 连接时，你基于 SSH 的 git pull 将通过 VPN**。

### 你还需要设置 HTTP_PROXY / HTTPS_PROXY 环境变量或 macOS 系统设置中的 proxy 吗？

**不——在使用 AnyConnect 时（尤其是在 full-tunnel 模式下），你通常不需要设置它们。**

- AnyConnect 自身运行**不需要**也不使用标准的 `http_proxy`/`https_proxy` 环境变量（它是一个 SSL VPN tunnel，而不是一个 HTTP proxy）。
- 对于 **git over HTTPS** (`https://github.com/...`):
  → 流量已经通过 VPN tunnel → 企业网络中的上游 proxy（如果有）会由企业 firewall/router 透明地处理。
  → 你**不需要**亲自设置 `HTTP_PROXY`；公司会在 tunnel 内部处理 proxy。

- 对于 **git over SSH** (`git@github.com:...`):
  → SSH **不是**基于 HTTP 的 → 它无论如何都会完全忽略 `HTTP_PROXY`/`HTTPS_PROXY`。
  → 但由于 VPN 路由了所有流量，SSH 数据包仍然会通过企业 VPN → 任何企业的 SSH 检测/proxy/jump-host（罕见）都会透明地应用。

- macOS 系统设置 → 网络 → 代理:
  → AnyConnect 在连接时经常会**覆盖**或**忽略**这些设置（尤其是在 full-tunnel 模式下）。
  → 许多用户反映系统偏好设置中的 proxy 设置会被 AnyConnect 绕过或更改。

**总结**
当 Cisco AnyConnect 连接时（尤其是企业 full-tunnel VPN）：
- 你**不需要**手动设置 `export HTTP_PROXY` / `HTTPS_PROXY` 或在系统设置中配置 proxy 以使 git (SSH 或 HTTPS) 工作。
- 所有内容都会自动路由到 VPN → 企业网络处理任何所需的 proxy/firewall 规则。

如果你的 git pull 仍然失败或变慢：
- 检查是 full-tunnel 还是 split-tunnel（询问 IT 或在连接前后运行 `netstat -nr` / `route get github.com`）。
- 企业 proxy 有时会屏蔽 SSH → 如果允许，请切换到 HTTPS remote (`git remote set-url origin https://github.com/...`)。
- VPN MTU/分片问题可能会降低 git 速度 → 尝试 `git config --global http.postBuffer 524288000`（针对 HTTPS）或降低 MTU。

References:

- [Cisco AnyConnect Administrator Guide - Proxy & Tunnel Policies](https://www.cisco.com/c/en/us/td/docs/security/vpn_client/anyconnect/Cisco-Secure-Client-5/admin/guide/b-cisco-secure-client-admin-guide-5-1/m_configure_vpn_access-noth.html)
- [Apple Discussions - Cisco AnyConnect routes all traffic](https://discussions.apple.com/thread/253565623)
- [Super User - Cisco AnyConnect forces all traffic](https://superuser.com/questions/284709/how-to-allow-local-lan-access-while-connected-to-cisco-vpn)
- [Cisco Community - AnyConnect Split vs Full Tunnel](https://community.cisco.com/t5/security-knowledge-base/anyconnect-split-tunneling-local-lan-access-split-tunneling/ta-p/4050866)
