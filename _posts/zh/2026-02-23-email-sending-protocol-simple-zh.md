---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 邮件发送协议简单解释
translated: true
type: note
---

问题：用户代理向邮件服务器发送电子邮件时使用什么协议？

答案：

用于从用户代理（如 Outlook、Thunderbird 或作为客户端的网页邮件界面）向邮件服务器发送电子邮件的正确协议是 **SMTP**（Simple Mail Transfer Protocol）。

以下是对所提供选项的分解：

* **A. SNMP (Simple Network Management Protocol)：** 该协议用于管理和监控网络设备，如 routers、switches 和 servers。它不涉及电子邮件传输。
* **B. SMTP (Simple Mail Transfer Protocol)：** 这是发送电子邮件的标准协议。它处理用户客户端（User Agent）向外发邮件服务器提交电子邮件，以及邮件服务器之间传输电子邮件。
* **C. HTTP (Hypertext Transfer Protocol)：** 这是万维网数据通信的基础。虽然基于网页的电子邮件服务（如 Gmail 或 Yahoo Mail）使用 HTTP/HTTPS 让用户在浏览器中与收件箱交互，但将电子邮件交给邮件服务器进行投递的实际过程通常在内部依赖 SMTP。在标准电子邮件架构问题的上下文中，HTTP 并非代理与服务器之间邮件提交的主要定义协议。
* **D. FTP (File Transfer Protocol)：** 该协议用于在计算机网络上客户端与服务器之间传输文件。它不用于发送电子邮件消息。

因此，**SMTP** 是专为问题中描述的任务设计的确切协议。

参考资料：

* [RFC 5321 - Simple Mail Transfer Protocol](https://datatracker.ietf.org/doc/html/rfc5321)
