---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Zscaler零信任安全概述
translated: true
type: note
---

问题：给我介绍一下 Zscaler——它是什么以及如何工作。

回答：

Zscaler 是一个基于**零信任**模型的云原生安全平台。它不会将流量路由到本地防火墙/VPN 集中器，而是以云代理的形式插入用户与其所连接的目标（互联网、SaaS、内部应用）之间。所有流量在到达目的地之前，都会在 Zscaler 的边缘云中进行内联检查。

核心架构——两个主要产品：

**ZIA（Zscaler Internet Access）**——安全 Web 网关/正向代理。你的设备到互联网/SaaS 的流量被隧道传输到最近的 Zscaler 数据中心，在那里进行解密（通过安装的根证书进行 TLS 检查）、检查（DLP、恶意软件沙箱、URL 过滤、CASB），然后转发。这是让工程师头疼的部分——它对你的 TLS 进行中间人攻击，因此像 `pip`、`npm`、`git`、`docker pull` 和 curl 等工具会因证书验证错误而失败，除非你信任 Zscaler 的 CA。

**ZPA（Zscaler Private Access）**——替代内部应用的 VPN。它不会让你“接入网络”，而是轻量级的**App Connectors** 放置在内部应用旁边，并建立*出站*连接到 Zscaler 云。当你请求一个应用时，Zscaler 通过将你的隧道与连接器的隧道拼接来协调连接。该应用永远无法通过网络直接访问——没有入站端口，没有暴露的子网。你只能访问你被授权的特定应用，而不是整个局域网。

数据平面是 **Zscaler Client Connector**（笔记本电脑上的代理）→ 最近的 ZEN/Service Edge（检查节点）→ 目的地。认证/策略决策基于身份（通过 IdP 使用 SAML/SCIM），因此策略跟随用户，而不是 IP。

一句话解释其存在理由：旧模型信任边界内的一切；零信任假设没有隐式信任，并对每个请求进行认证和检查，无论其位置如何。

对你的银行/开发设置的实际说明——TLS 检查是问题所在。通常的解决方法是导出 Zscaler 根 CA 并将其指向你的工具链：

```bash
# 提取 Zscaler 根证书（macOS 钥匙串）
security find-certificate -a -c "Zscaler" -p /Library/Keychains/System.keychain > zscaler.pem

# 将常用工具指向该证书
export REQUESTS_CA_BUNDLE=$PWD/zscaler.pem   # python requests
export NODE_EXTRA_CA_CERTS=$PWD/zscaler.pem  # node/npm
export CURL_CA_BUNDLE=$PWD/zscaler.pem        # curl
git config --global http.sslCAInfo $PWD/zscaler.pem
pip config set global.cert $PWD/zscaler.pem
```

要深入了解产品线和架构的最新详细信息，建议直接查阅他们的文档，因为具体细节会不断演变。