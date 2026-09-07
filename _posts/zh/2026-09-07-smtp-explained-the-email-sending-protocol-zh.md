---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SMTP详解：电子邮件发送协议
translated: true
type: note
---

问题：什么是SMTP？

答案：

SMTP（简单邮件传输协议）是用于在互联网上发送和路由电子邮件消息的标准通信协议。以下是详细说明：

**工作原理：**
- SMTP 是一种推送协议——它负责处理从客户端到服务器，或服务器之间的邮件 *发送* 和 *中继*
- 当你点击“发送”时，你的电子邮件客户端连接到 SMTP 服务器（通常使用端口 25、587 或 465），进行身份验证，并将消息转交给服务器
- SMTP 服务器随后将邮件路由到收件人的邮件服务器

**主要作用：**
- **邮件提交**——从你的电子邮件客户端到你的服务提供商服务器
- **邮件中继**——在互联网上的服务器之间传输
- **不用于接收**——SMTP 仅负责 *发送*；接收邮件使用 IMAP 或 POP3

**常用端口：**
| 端口 | 用途 |
|------|------|
| 25 | 服务器间中继 |
| 587 | 客户端提交（使用 STARTTLS） |
| 465 | 客户端提交（隐式 TLS） |

**简要历史：**
由 Jon Postel 在 RFC 821（1982）中定义，后由 RFC 5321（2008）更新，该版本仍是当前标准。

参考文献：
- [RFC 5321 – 简单邮件传输协议](https://datatracker.ietf.org/doc/html/rfc5321)
- [SMTP – MDN Web 文档术语表](https://developer.mozilla.org/zh-CN/docs/Glossary/SMTP)
- [电子邮件工作原理 – Cloudflare 学习中心](https://www.cloudflare.com/zh-cn/learning/email-security/what-is-smtp/)