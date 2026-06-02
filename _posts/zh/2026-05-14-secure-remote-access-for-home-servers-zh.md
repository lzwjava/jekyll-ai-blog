---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 家庭服务器的安全远程访问
translated: true
type: note
---

问题：如何使用Tailscale或其他Linux解决方案，让我的朋友连接到我在中国广州的家庭服务器？

答案：

你可以使用Tailscale或其他VPN/远程访问解决方案，安全地允许远程访问像广州这样大城市中的家庭服务器。以下是详细指南：

---

### **1. 在Linux上使用Tailscale**

Tailscale是一个基于WireGuard的零配置VPN。它能在你的设备之间创建一个安全的网络。

**步骤：**

1. **在Linux上安装Tailscale**

   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   sudo tailscale up
   ```

   * 这会打开一个URL，用于通过你的Tailscale账户（谷歌、GitHub、微软或邮箱登录）进行认证。

2. **检查Tailscale状态**

   ```bash
   tailscale status
   ```

   * 你应该会看到你的设备已列出，并带有Tailscale IP（通常是`100.x.x.x`）。

3. **与朋友共享访问权限**

   * 在浏览器中前往 [Tailscale管理控制台](https://login.tailscale.com/admin/machines)。
   * 通过将朋友的邮箱添加到你的Tailscale网络来共享访问权限。他们需要在自己的设备上安装Tailscale并进行认证。
   * 他们会获得一个私有Tailscale IP来访问你的服务器。

4. **连接到服务器**

   * 在你朋友的机器上：

     ```bash
     ssh user@100.x.x.x   # 使用你服务器的Tailscale IP
     ```

   * 或者通过Tailscale IP访问你暴露的任何服务（网页服务器、媒体服务器）。

**注意事项：**

* 即使在NAT和限制性ISP（在中国很常见）环境下也能正常工作。
* 端到端加密，无需端口转发。
* 免费版足以满足小型网络需求；如需更多设备，可考虑付费版。

---

### **2. 替代方案**

#### **A. 直接使用WireGuard**

* Tailscale底层使用WireGuard，但你可以手动配置WireGuard。
* 需要：

  * 为服务器和客户端生成密钥。
  * 在两台设备上配置`wg0.conf`。
  * 如需要，在路由器上进行端口转发。
* 更灵活，但技术性更强，不如Tailscale方便。

#### **B. Ngrok / Cloudflare Tunnel**

* 如果你的朋友只需要访问特定服务（Web、SSH等），这个方案很有用。
* SSH示例：

  ```bash
  ssh -R 2222:localhost:22 user@remote-ngrok-server
  ```

* 优点：

  * 无需设置VPN。
  * 即使在CGNAT或严格ISP环境下也易于使用。
* 缺点：

  * 持久隧道可能需要付费计划。
  * 并非完整的网络访问。

#### **C. ZeroTier**

* 另一个类似于Tailscale的VPN解决方案。
* 可在NAT环境下工作，支持点对点连接。
* 最多50台设备免费。
* 需要在 [ZeroTier](https://www.zerotier.com) 创建网络并安装其客户端。

---

### **3. 针对中国的实用建议**

* Tailscale和ZeroTier通常在中国可用，但某些ISP可能会屏蔽或限速基于WireGuard的流量。
* 使用Cloudflare Tunnel或基于VPS的中继可以帮助绕过严格的NAT或防火墙限制。
* 如果速度至关重要（如游戏或大文件传输），在有线宽带家庭服务器上使用Tailscale效果最佳。

---

如果你愿意，我可以为你编写一个 **在广州的完整设置分步示例**，包括Linux服务器、Tailscale和朋友访问权限——涵盖SSH和Web服务——这样你的朋友就可以立即连接。

需要我这样做吗？
