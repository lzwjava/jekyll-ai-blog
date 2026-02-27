---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Shadowrocket Hysteria 2 设置指南
translated: true
type: note
---

**Shadowrocket** 是一款受欢迎的付费 iOS 应用（可在 App Store 下载），自 **2.2.35**（及更高版本）起支持 **Hysteria 2** 协议。截至 2026 年，它可可靠连接 Hysteria 2 服务器。

### 前提条件

- 已安装并更新 Shadowrocket（检查版本 ≥ 2.2.35）。
- 您的 Hysteria 2 服务器正在运行且可访问（来自之前的设置：UDP 端口开放、域名或 IP、密码认证等）。
- 您已准备好服务器详情：
  - 服务器地址（域名或 IP）
  - 端口（通常为 443）
  - 密码（来自服务器的 `auth.password`）
  - 可选：SNI（使用 TLS/ACME 时通常与域名相同）
  - 可选：如果服务器配置中启用混淆（salamander），则需混淆密码

### 逐步指南：在 Shadowrocket 中添加 Hysteria 2（手动设置）

1. 在 iPhone/iPad 上打开 **Shadowrocket**。

2. 转到 **Home** 选项卡（或 **Nodes** / 代理列表界面）。

3. 点击右上角的 **+**（加号）图标添加新节点/服务器。

4. 在“Type” / 协议下拉菜单中，选择 **Hysteria 2**（显示为“Hysteria2”或“HY2”）。

5. 填写字段：
   - **Server** / Address：your-domain.com（或服务器 IP）
   - **Port**：443（或您配置的 UDP 端口）
   - **Password**：your-strong-password-here（单一密码认证）
   - **SNI**（Server Name Indication）：your-domain.com（使用 TLS 时重要；通常与服务器域名匹配）
   - **Obfs** / Obfuscation：如果服务器启用 salamander 混淆，选择“salamander”并输入 obfs 密码；否则保持禁用/无。
   - **ALPN**：通常保持默认或设置为 `h3`（用于 HTTP/3 伪装兼容性）
   - **Up Mbps** / **Down Mbps**：可选带宽限制（例如，100–200 以提高稳定性；设为 0 表示无限制）
   - **Remarks** / Name：为其命名，如“HY2 Home Server”
   - 其他高级选项（拥塞控制等）：默认值通常即可（推荐 Brutal）

6. 点击 **Save** 或 **Done**。

7. 返回主列表，选择您的新 Hysteria 2 节点。

8. 打开主屏幕顶部的 **Connect** 开关。

9. 如果提示，授予 VPN 权限（Shadowrocket 使用 Apple's VPN 框架，以 TUN 模式实现全设备代理）。

10. 测试：打开 Safari 或任意应用 → 访问 whatismyipaddress.com 等网站，确认 IP 已更改。

### 替代方法：通过 URI 导入（如果您有 hy2:// 链接，这是最简单的方式）

许多 Hysteria 2 设置（例如 H-UI 等面板、自定义脚本）会生成如下格式的分享链接：

```
hy2://password@your-domain.com:443/?sni=your-domain.com&insecure=0
```

（或带 obfs：&obfs=salamander&obfs-password=xxx）

- 复制完整的 `hy2://...` 链接。
- Shadowrocket 会自动从剪贴板检测 → 提示时点击导入。
- 或：在 Shadowrocket → + → Import from Clipboard（或如果有二维码，则 Scan QR）。

### 常见提示与故障排除
- **连接失败？** 
  - 仔细检查 UDP 443 未被阻塞（使用 sing-box desktop 等其他客户端测试服务器可达性）。
  - 确保 SNI 完全匹配（区分大小写）。
  - 如果使用自签名证书：在 URI 中启用“Allow Insecure” / insecure=1，或在应用中切换 insecure。
  - 服务器防火墙允许 UDP 入站。
- **速度慢？** 尝试降低带宽上限或测试不同的拥塞设置。
- **全设备代理**：Shadowrocket 默认使用 TUN 模式（路由所有流量）；如果需要按应用/仅代理，使用“Config” → “Global Routing”设置规则。
- **更新应用**：如果缺少 Hysteria 2 选项 → 更新 Shadowrocket。

此设置可在 iOS 上提供出色性能和强大的抗审查能力。

参考资料：  

- [Hysteria 2 Official - 3rd-party Apps](https://v2.hysteria.network/docs/getting-started/3rd-party-apps)
- [GitHub Discussion - Hysteria2 with Shadowrocket](https://github.com/apernet/hysteria/discussions/1325)
- [Hysteria 2 One-Click Script Repo (client notes)](https://github.com/missuo/Hysteria2/blob/main/README.md)