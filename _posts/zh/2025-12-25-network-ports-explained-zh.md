---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 网络端口解析教程概论
translated: true
type: note
---

Question: Transcribe the YouTube video at <https://www.youtube.com/watch?v=g2fT-g9PX9o> and organize it a bit.

Answer:

# Network Ports Explained

**Video Details**

- **Title:** Network Ports Explained
- **Channel:** PowerCert Animated Videos
- **Upload Date:** July 18, 2022

## Organized Transcript (by Sections)

### 什么是 Port？ (00:00)

Port（端口）不是物理连接；它是一种逻辑连接，供程序和服务用于交换信息。它决定了计算机或服务器上将使用哪个特定的程序或服务——例如加载网页、使用 FTP、访问电子邮件等。Port 通过唯一的数字进行标识，范围从 0 到 65,535。

常见示例：

- Port 80 和 443：Web 页面
- Port 21：FTP
- Port 25：Email

Port number 始终与 IP address 相关联，后者用于标识网络上的设备。它们共同实现了数据交换。

### IP Addresses vs. Ports (00:47)

IP address 定位设备（例如：大洲、国家、城市）。Port number 指定该设备上的服务。

### 常见端口示例：访问网站 (01:36)

访问 google.com 时：

- Domain name 被转换为 Google 的 IP address。
- 由于是 HTTP（网页浏览），因此会添加 Port 80。
- IP address 定位服务器。
- 服务器看到 Port 80 并将请求转发到其 Web service。

（注意：Port 443 用于 HTTPS 安全网站，这已变得越来越普遍。）

### 使用 Netstat 查看端口 (02:55)

Netstat (network statistics) 是一个命令行工具，用于查看活动连接和端口。
Windows 上的示例：`netstat -n`

- 显示 Local IP 和 Client-side port。
- 显示 Remote (foreign) IP 和 Server port（例如：Web 的 :80）。

FTP (Port 21) 示例：过程类似，但转发到 FTP service。

### Port Numbers 和类别 (05:00)

Port numbers (0–65,535) 由 Internet Assigned Numbers Authority (IANA) 管理，分为三个类别：

- **Well-Known Ports (0–1023):** 用于常见服务的系统端口（例如：80/HTTP, 443/HTTPS, 21/FTP, 25/SMTP）。在服务器端使用。
- **Registered Ports (1024–49,151):** 用于特定应用程序/公司。在服务器端使用。
- **Dynamic/Private Ports (49,152–65,535):** 在会话期间分配的临时 Client-side 端口（例如，当你的计算机连接到网站时）。

客户端计算机使用 Dynamic ports 进行出站连接。服务器在 Well-known/registered ports 上进行监听。

你的计算机也可以作为服务器运行（例如：运行本地 Web 或 FTP server），因此你可能会看到本地正在监听的 Well-known ports。

### 最终示例 (07:48)

连接到多个网站（例如：使用 Port 80 访问 yahoo.com, example.com）和一个 FTP server (Port 21)：
Netstat 显示：

- 带有 Dynamic client ports 的 Local IP。
- 带有 Server ports (80 或 21) 的 Remote IPs。

### 补充说明

- 许多现代网站使用 Port 443 (HTTPS) 而不是 80。
- 为了专注于核心内容，省略了有声读物和 Netstat 视频的推广片段。

References:

- [Original YouTube Video](https://www.youtube.com/watch?v=g2fT-g9PX9o)
