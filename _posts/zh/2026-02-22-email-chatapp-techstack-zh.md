---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 邮件到聊天应用技术栈
translated: true
type: note
---

太好了！让我们深入了解 **MailTime: Email Messenger** 移动应用的细节。

核心理念是将电子邮件客户端转变为像消息应用（例如 WhatsApp 或 iMessage）一样的收件箱体验。为了实现这一点，它结合了特定技术和标准电子邮件协议。

以下是其技术栈和所用协议的分解。

### ⚙️ The Tech Stack: How the App is Built

构建一款能在不同设备上无缝运行的应用，需要多种多样的编程语言和框架。根据公司招聘描述，以下是涉及的技术：

| 组件 | 使用的技术 |
| :--- | :--- |
| **Mobile (iOS)** | **Objective C, Swift** |
| **Mobile (Android)** | **Java, C/C++** |
| **Backend Server** | **PHP, Python, Golang, MongoDB**, RESTful APIs |
| **Web Technologies** | **JavaScript, HTML, CSS** |
| **Core Logic** | 专用的 **content-parsing engine**，用于将电子邮件重新格式化为聊天气泡 |

**content-parsing engine** 是 MailTime 的“秘诀所在”。它的任务是通过标准协议接收电子邮件，剥离杂乱内容（如签名、以往回复和元数据），并智能地将对话重构为干净、气泡风格的格式，便于在手机上阅读。

### 📧 The Protocols: How the App Communicates

由于 MailTime 连接到您现有的电子邮件账户（如 Gmail、Outlook 或 iCloud），它必须使用这些服务相同的协议。它使用标准、开放的电子邮件协议来实现这一点。

* **接收和同步邮件：IMAP (Internet Message Access Protocol)**
  * 这是用于同步电子邮件的主要协议。IMAP 非常适合移动应用，因为它将所有电子邮件保留在服务器上。当您在 MailTime 中阅读、删除或移动电子邮件时，这些更改会与您的电子邮件提供商同步，并在笔记本电脑上的 Gmail 中显示。这保持了一致性。
  * 该应用还支持 **Exchange (ActiveSync)**，这是 Microsoft 用于同步商业账户邮件、日历和联系人的协议。

* **发送邮件：SMTP (Simple Mail Transfer Protocol)**
  * 这是 *发送* 电子邮件消息的标准协议。当您点击聊天气泡发送时，MailTime 将消息交给您的电子邮件提供商的 SMTP 服务器进行投递。

* **连接方式：OAuth 和基于密码的登录**
  * MailTime 支持连接大量提供商，包括 **Gmail, Yahoo Mail, Outlook.com, Hotmail, iCloud, AOL 和 Office 365**，以及标准的 **IMAP** 账户。对于 Gmail 等现代服务，它主要使用 **OAuth**，这是一个安全的基于令牌的授权系统，让您可以授予 MailTime 访问权限，而无需提供实际的电子邮件密码。

简而言之，MailTime 不会取代您的电子邮件提供商。相反，它作为一个智能、设计精美的前端，使用与其他电子邮件应用相同的 **SMTP 和 IMAP** 协议，但以全新的方式呈现信息。

希望这能让您清楚了解 MailTime 应用的动力来源。这个技术分解有助于您理解其工作原理吗？
