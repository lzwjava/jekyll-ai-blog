---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: RSA SecurID 双重因素身份验证指南
translated: true
type: note
---

Question: Provide a comprehensive introduction to RSA SecurID token.

Answer:

RSA **SecurID**（通常称为 RSA SecurID 或简称 SecurID）是全球最知名的 **two-factor authentication** (2FA) 系统之一。它最初由 RSA Security 开发（后被 EMC 收购，随后归入 Dell，目前作为 RSA 品牌下身份识别产品组合的一部分运营）。

它通过结合 **something you know**（由你所知的 PIN 或密码）与 **something you have**（由你拥有的实体 Token 或软件认证器）来提供强认证（strong authentication）。

### 核心概念
该系统生成**基于时间的一次性代码** (tokencodes)，这些代码会定期更改 —— 最常见的是每 **60 seconds** 更改一次，尽管某些实现使用 30 秒。

这是一个典型的 **Time-based One-Time Password** (TOTP) 类机制的例子，但 RSA 使用其专有的算法（历史上基于对称密钥运算，在较新版本中通常基于 AES）。

### 主要组件
1. **The Token / Authenticator（令牌/认证器）**
   - **Hardware tokens** —— 小型钥匙扣样式的设备（例如 SID700, SID800 系列），具有：
     - 显示 6 位（有时是 8 位）代码的 LCD 屏幕
     - 显示距离下一个代码生成剩余时间的倒计时点或条格
     - 某些型号包含用于存储证书的 USB 接口或智能卡接口
     - 无需按钮 —— 代码始终可见
     - 电池寿命通常为 3–5 年

   - **Software tokens** (soft tokens)
     - 移动端 App (iOS / Android)
     - 桌面端应用程序 (Windows / macOS)
     - 在某些实现中，要求用户在 App 内输入 PIN，从而生成 8 位 passcode

   - **On-demand / delivery tokens**
     - 通过 SMS、电子邮件或语音通话发送 tokencode（无需部署实体或软件 Token）

2. **RSA Authentication Manager** (前身为 ACE/Server)
   - 服务端软件（本地部署）或云服务
   - 存储每个 Token 唯一的 **serial number**（序列号）和秘密 **seed**（种子，128-bit 对称密钥）数据库
   - 拥有与 Token 相同的时间源和算法
   - 随时为每个 Token 生成预期的代码
   - 处理时间偏移补偿 (time drift compensation)，因为廉价的内部时钟可能导致 Token 出现轻微的时间偏差

3. **Authentication Flow**（身份验证流程示例）
   - 用户尝试登录 VPN、服务器或云端应用等
   - 系统提示输入 **username + passcode**
   - Passcode = **PIN**（4–8 位，用户自定义）+ **tokencode**（Token 上显示的 6 位数字）
     - 示例：PIN = 1234，Token 显示 567890 → 用户输入 1234567890
   - 某些实现（特别是软件 Token）的组合方式不同，或者在 App 中输入 PIN 后仅需输入 tokencode
   - 认证代理 (Authentication Agent，位于目标系统上) 将凭据转发给 Authentication Manager
   - 服务器计算预期的 tokencode → 进行比对 → 允许或拒绝访问

### 安全特性
- Seed 对每个 Token 都是**唯一的**，且永远不会离开工厂或服务器
- 代码每 60 秒更改一次 → 被截获的代码会迅速失效
- 即使 PIN 被盗，攻击者仍需持有实体或软件 Token
- 服务器允许微小的**时间窗口** (±1 个间隔)，以补偿时钟偏差和用户输入延迟

### 优势
- 用户体验非常简单（只需读取并输入数字）
- 支持离线工作（Token 端不需要互联网连接）
- 经过数十年在高度安全环境（银行、政府、国防、技术公司）中的验证
- 广泛的集成支持（通过 RADIUS, SAML 等支持 VPN, RDP, SSH, 云服务等）

### 局限性与演进
- 实体 Token 可能会丢失或被盗（尽管 Seed 的泄露非常困难）
- 容易受到实时 **phishing**（网络钓鱼）的攻击（攻击者立即转发代码）
- 较旧的部署曾受到时间同步不佳或 Seed 泄露事件的影响（特别是 2011 年 RSA 因网络钓鱼导致的 Seed 泄露担忧）
- 现代替代方案（Push notifications、生物识别、FIDO/WebAuthn、以及 Microsoft Authenticator / Google Authenticator 等应用）因更便捷而更受欢迎
- RSA 已将 SecurID 扩展为更广泛的 **SecurID Access** / **SecurID Suite**，涵盖了推送、生物识别、基于风险的认证 (risk-based auth) 以及云端选项

截至 2026 年，RSA SecurID 在企业中（特别是传统或本地部署环境）仍被广泛使用，尽管许多组织已经使用现代 MFA 方法补充或取代了纯 Token 的使用。

References:

- [RSA SecurID - Wikipedia](https://en.wikipedia.org/wiki/RSA_SecurID)
- [RSA official SecurID page](https://www.rsa.com/products/securid)
- [Baeldung on Computer Science - RSA SecurID Tokens](https://www.baeldung.com/cs/rsa-securid-tokens)
- [NinjaOne - What is RSA SecurID?](https://www.ninjaone.com/it-hub/endpoint-security/what-is-rsa-securid)
