---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tailscale安全评估与建议
translated: true
type: note
---

**问题：** 我的 Tailscale 设置安全吗？

**回答：**

是的，基本没问题。你的设置正确遵循了安全模型：

**安全的地方：**
- **WireGuard 加密** — Tailscale 的隧道在密码学上是稳固的、点对点的，且具有前向安全性。你的 Mac 和工作站之间的流量默认端到端加密。
- **公钥 SSH 认证** — 你在使用最强的 SSH 认证机制，没有密码暴露面。
- **无入站暴露** — 位于 NAT 后面的机器如果不属于你的 tailnet，就无法从公共互联网访问。Tailscale 内部处理 NAT 穿越。
- **自动更新** — Tailscale 保持密钥交换更新；1.96.4 和 1.98.x 之间的版本差异在操作上没问题（WireGuard 协议是稳定的）。

**需要考虑的现实风险：**

1. **Tailscale 账户泄露** — 如果 `lzwjava@` 的凭据泄露或 Tailscale 后端被攻破，攻击者可能会劫持你的 tailnet。缓解措施：使用强密码短语，如果 Tailscale 支持则启用 2FA，定期轮换认证密钥。

2. **工作站被攻破** — 如果你的 Ubuntu 机器（运行 `tailscaled` 的那台）被攻破，攻击者就能获取你的私有 WireGuard 密钥并冒充你的工作站。缓解措施：保持 Ubuntu 打补丁，对非 Tailscale 端口进行防火墙限制，运行最小服务。

3. **SSH 密钥泄露** — 如果你的 SSH 私钥（用于 `ssh lzw@<工作站-ip>`）从你的 Mac 被盗，攻击者就能 SSH 登录进来。缓解措施：使用 SSH agent，考虑带密码短语保护的 Ed25519 密钥，监控工作站上的 `.ssh/authorized_keys` 是否有未授权添加。

4. **Tailscale 的基础设施** — 你在信任 Tailscale Inc. 进行协调。理论上他们能看到元数据（哪些设备连接、大致时间）。他们无法看到加密流量内容。这对于家庭/个人使用是可接受的；如果你运行敏感的业务工作负载，自托管 WireGuard 是替代方案。

**快速改进：**
- 将两台机器都更新到最新的 Tailscale（Mac 上 `brew upgrade tailscale`，Ubuntu 上 `sudo apt upgrade tailscale`）。
- 在 Tailscale 管理控制台中启用 MagicDNS — 比记住 IP 地址更清晰，减少可能误连到错误机器的拼写错误。
- 锁定工作站的 SSH：在 `/etc/ssh/sshd_config` 中禁用密码认证（你已经在做了，但请确认），限制为仅公钥方式。
- 检查工作站上的 `~/.ssh/authorized_keys` — 确保只有你的密钥在里面。

**总结：** 你的设置比直接将 SSH 暴露到互联网或使用基于密码的 VPN 更安全。对于 AI/ML 工作来说操作上是合理的。最薄弱的环节是人为失误（丢失密码短语、SSH 密钥保管不当）——而不是协议本身。