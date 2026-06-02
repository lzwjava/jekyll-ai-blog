---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 仅发送者和接收者可读的安全消息
translated: true
type: note
---

**问题：** 什么是 end-to-end encryption？请用英语解释提供的描述。

**答案：**

端到端加密 (E2EE) 是一种安全方法，确保数据从发送者的设备离开的那一刻起直到到达接收者的设备时始终保持加密状态。您提供的描述是正确的——以下是清晰的英文版本和解释：

**核心定义：**
端到端加密意味着消息从源头到目的地在整个传输过程中始终保持加密（ciphertext）形式。解密仅发生在接收者的设备上。

**关键特性：**
- 消息在发送者的设备上使用仅接收者拥有的密钥（或仅发送者和接收者知道的密钥派生）进行加密。
- 所有中间服务器、云服务、网络运营商和中间潜在攻击者只能看到加密数据——他们无法读取内容。
- 解密从未在任何服务器或中继节点上发生；它仅发生在真正的端点（接收者的设备）。
- 即使服务器被入侵、黑客攻击或法律强制交出数据，实际消息内容仍然不可读。

**中文社区常见名称：**
- 端到端加密 (most common)
- 端对端加密
- 脱线加密 (less common, emphasizes that decryption is "offline" from the service provider)
- 包加密 (sometimes used, highlights per-message/packet encryption)

**重要的现实世界含义：**
- 正确实现 E2EE 的良好示例：Signal、WhatsApp (after 2016)、iMessage (between Apple devices)、Threema、Element (when configured properly)、Telegram Secret Chats
- 非真正 E2EE：标准 Telegram cloud chats、WeChat、Line (ordinary chats)、大多数电子邮件服务包括 Gmail、Outlook web mail、企业 Slack/Teams (unless specially configured)

**为什么描述强调“即使节点被入侵，消息也不会泄露”：**
因为只有两个通信端点持有解密密钥。任何中间节点（服务器、路由器、CDN、ISP 设备等）仅转发密文，并且无法访问明文或解密所需的私钥。

总之：
端到端加密保护消息内容免受除预期接收者外的所有人的侵害——包括服务提供商本身。

**参考文献：**

- 无（解释基于标准密码学定义和常见行业用法）
