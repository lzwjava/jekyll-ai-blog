---
audio: true
generated: false
image: false
lang: zh
layout: post
title: 设置你的代理服务器
translated: true
type: post
---

要设置服务器，请使用Outline Manager：[https://getoutline.org](https://getoutline.org)。

推荐的托管提供商包括DigitalOcean、Google Cloud、Amazon Lightsail、Azure、Vultr和Linode。为了获得最佳性能，选择新加坡或东京的服务器位置。虽然香港也是一个可行的选择，但请注意，某些AI工具如ChatGPT和Claude在该地区被限制。

你仍然可以在香港服务器上使用Deepseek、Mistral、Grok和Gemini API（通过Cursor）。由于其他人可能会避开香港服务器，它们往往不那么拥堵。

考虑服务器位置和距离。对于广州的人来说，香港是托管代理服务器的好选择。使用Speedtest测量网络速度。

为了获得最佳速度，我建议使用阿里云香港服务器和BGP（高级）弹性IP。弹性IP功能允许快速更换当前IP被封禁。阿里云的优化BGP（高级）连接确保快速性能。该服务每1GB流量收取3元人民币。

协议如Shadowsocks、VMess和Trojan容易被封禁。

Linode的IP转移功能允许你迅速将服务器迁移到新位置，从而获得新的IP地址。

你可能需要一个脚本每天自动续订你的服务器。

如果代理服务器被GFW封禁或遇到其他问题，可以使用中国电信澳门SIM卡与笔记本共享蜂窝数据。这允许你设置一个新的服务器。

对于像Google Cloud Platform这样的云服务，配置新服务器需要现有的代理服务器。然而，像DigitalOcean或Vultr这样的提供商可以直接设置而不需要代理服务器。

使用[Auto SS Config](https://github.com/lzwjava/lzwjava.github.io/blob/main/scripts/auto-ss-config/upload_configs.py)生成和上传Shadowsocks或Clash订阅URL。

使用Digital Ocean的快照功能。如果服务器的IP被封禁，从服务器的快照创建一个新的droplet并再次运行`install.sh`。

使用Digital Ocean的保留IP功能。如果服务器的IP被封禁，分配一个新的保留IP。

我们使用Outline Manager来设置我们自己的服务器，因为它快速且允许我们自己享受服务器。VPN提供商的节点往往不可靠。我们的服务器也可能出现问题，但我们对情况有更详细的了解。我们还可以选择不同的云提供商。此外，我们知道我们是使用中国电信还是中国移动，以及我们是使用家庭Wi-Fi还是蜂窝数据。
