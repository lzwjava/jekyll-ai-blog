---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中国严格禁止未经授权代理服务
translated: true
type: note
---

**问题：** 在中国销售代理服务是否非法，以及为什么像腾讯云和阿里云这样的中国云提供商不提供此类服务？

**回答：**

## 在中国销售代理服务是否非法？

### 简短回答：是的，在大多数有实际意义的形式下——特别是销售未经授权的代理/VPN 服务明确非法且可被起诉

---

### 法律框架

中国通过一系列法律、法规以及被称为 **Great Firewall**（官方称为“金盾工程”）的技术系统控制互联网访问。主要法律工具包括：

**1. 1996 年《国际联网暂行规定》**
该法规定，未经许可建立国际通信通道是非法的。建立或出租国际通信通道（包括 VPN）用于商业活动也是非法的。

**2. 2017 年 MIIT VPN 规定**
2017 年，中国工业和信息化部（MIIT）实施规定，要求在中国运营的所有 VPN 服务必须获得政府批准。

**3. 刑法第 225(d) 条——非法经营罪**
以严重扰乱电信市场的方式提供 VPN 服务构成非法经营罪。如果 VPN 被用于实施非法活动并提供以协助和教唆犯罪，则 VPN 提供可能落入协助犯罪范畴。

---

### 究竟什么是非法的？

法律区分了 **销售/提供** 代理服务与 **个人使用** 它们：

- **销售或运营未经授权的代理/VPN 服务** → 明确且严重非法，有实际刑事起诉案例。
- **个人使用** → 技术上非法，但很少对个人（尤其是游客）执行。

未注册的代理服务是被禁止的——只有政府批准的 VPN 和代理服务才被允许。绕过 Great Firewall 是一种可惩罚的违法行为——虽然个人用户很少被起诉，但企业和组织因提供未经授权访问而可能面临罚款或被关闭。

---

### 销售者的实际刑事处罚

政府对提供或销售未经授权 VPN 服务的个人采取更严格的打击措施。吴祥阳因非法运营 VPN 服务被判处五年半有期徒刑并罚款 50 万元（约合 7.6 万美元）。他被认定为提供软件和硬件帮助用户绕过互联网限制，而未获得必要许可。

另一个著名案例：一名程序员马某被责令支付超过 105.8 万元的非法收入没收款外加 200 元罚款，因使用未经批准的国际连接向公司提供互联网咨询服务。

---

### 为什么腾讯云、阿里云等不提供代理服务？

主要中国云提供商避开这一领域有几个强有力的原因：

**1. 法律禁止和许可要求**
中国政府已授权几家遵守中国审查和后门访问法律的官方许可 VPN 提供商。那些开发或销售自家 VPN 的人可能面临数年监禁。腾讯和阿里云没有动力为未经授权的代理服务而冒险整个业务。

**2. 必须遵守《网络安全法》**
腾讯云将其中国基础设施与其国际平台分离，以遵守中国的网络安全法规。阿里云和腾讯云均完全在法律界限内运营，这意味着它们无法提供绕过 Great Firewall 的服务。

**3. 日志记录和监督要求**
使用合法 VPN 服务的公司必须遵守《网络安全法》、《数据安全法》和《个人信息保护法》等法规。中国政府可随时检查数据和运营，网络流量须至少保留六个月记录。即使是合法的、经国家批准的服务也带有沉重的监控义务——这是有意为之。

**4. 巨大的财务和运营风险**
违反中国《网络安全法》的组织可能面临最高 100 万元人民币（约合 15 万美元）的罚款，个人也可能被罚款。公司还可能面临非法所得被没收。此外，违规者的网站可能被关闭，或整个业务运营被暂停。

**5. 只有经国家批准的电信公司才能合法提供 VPN**
在中国，只有从国有电信公司获得的政府批准 VPN 才是合法的，这些通常仅供企业使用。私有云提供商如腾讯和阿里云在此语境下并非许可电信运营商，因此它们无法合法提供此类服务。

---

### 总结表格

| 行为主体 | 合法性 | 风险 |
|---|---|---|
| 销售未经授权的代理/VPN 服务 | **非法** | 监禁 + 罚款 |
| 提供经国家批准的企业 VPN | 合法（需许可） | 严格监督 |
| 个人使用个人 VPN | 灰色地带 | 很少被起诉 |
| 中国云提供商提供代理服务 | **禁止** | 许可吊销 + 罚款 |

---

简而言之，在中国销售代理服务是一个严重的法律风险——而非监管灰色地带。腾讯云、阿里云和类似提供商遵守中国法律，正是因为它们的整个业务存在依赖于维持运营许可和政府关系。

**参考资料：**

- [Internet Censorship in China – Wikipedia](https://en.wikipedia.org/wiki/Internet_censorship_in_China)
- [Great Firewall – Wikipedia](https://en.wikipedia.org/wiki/Great_Firewall)
- [Are Proxies Illegal? – RapidSeedbox](https://www.rapidseedbox.com/blog/proxies-illegal)
- [VPNs in China: Legal but Limited – GoClick China](https://www.goclickchina.com/blog/vpns-in-china-legal-but-limited-with-loopholes-and-restrictions/)
- [China VPN Law for Business – CBL Translations](https://cbltranslations.com/en-us/china-law/privacy/vpn-business-explained/)
- [Complete Guide to Tencent Cloud in China – AppInChina](https://appinchina.co/a-guide-to-tencent-cloud-in-china/)
- [Accelerate the Network to China – Alibaba Cloud Blog](https://www.alibabacloud.com/blog/accelerate-the-network-to-china-for-global-enterprises_596343)
