---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 极简主义在科技设计中胜出
translated: true
type: note
---

问题：科技产品中“less is better”的真实案例有哪些？为什么从软件/硬件中移除功能比添加它们更难？

答案：

## “Less is Better” — 科技中简化的哲学与实践

这是一个引人入胜的话题，涉及设计哲学、工程学、商业策略和人类心理学。让我们全面分解一下。

---

## 1. 核心理念：为什么“Less”更有价值

数字极简主义是有意将数字产品和流程聚焦于真正重要的事物，同时剥离不必要的部分。它拒绝“feature bloat”——添加更多按钮、菜单或配置的诱惑——而是优先考虑深度而非广度、目的而非新奇。

“Worse is Better”（也称为 New Jersey 风格）这一概念由 Richard P. Gabriel 提出。它认为软件质量并不一定随着功能增加而提升——存在一个点，在实用性和可用性方面，更少的功能（“worse”）是更优选择（“better”）。功能有限但简单易用的软件可能比相反的情况更吸引用户和市场。

极简主义隐含在 Unix 哲学的“everything is a text stream”和“do one thing and do it well”中，尽管现代 Unix/Linux 发行版并未严格遵守这一哲学。

---

## 2. Apple — 最著名的简化者

Apple 是公司中不断无情移除功能的典型例子，有时备受争议，但常常影响整个行业。

### The iMac G3 (1998) — 杀死 Floppy Disk
Steve Jobs 回归 Apple 后发布的原始 iMac G3 时尚酷炫——直到你发现 Apple 决定不包含 serial ports 和 floppy disk drives，而是用 USB ports 和 CD-ROMs 替换它们。相比新兴的 USB 标准，serial ports 变得越来越不便，后者支持即插即用外围设备。

### MacBook Air (2008) — 杀死 Optical Drive
在大力推广 CD 十年后，Apple 在 2008 年的原始 MacBook Air 中移除了 optical drive。这是一个明显的选择，因为 Apple 将 MacBook Air 定位为市场上最薄的笔记本电脑——CD-ROM drive 会让便携 PC 变厚。

### MacBook Pro (2016) — 大端口清洗
2016 年，Apple 移除了 MagSafe 2 充电端口、剥离了 HDMI port、SD card slot、关闭了 Thunderbolt 2 ports，最引人注目的是杀死了标准 USB port——用四个 Thunderbolt 3/USB-C ports 替换所有这些。

这极具争议。2016 年，Apple 达到了“谁需要端口 lol”的设计巅峰，向用户出售 dongle 来连接 MacBook 的一个（单一的、uno）USB port，并去除了 MacBook Pro 的 HDMI、USB Type-A 和 SD card ports。

### iPhone 7 (2016) — 杀死 Headphone Jack
在具有里程碑意义的决定中，Apple 从 2016 年的 iPhone 7 开始淘汰了 3.5mm headphone jack。Apple 给出的理由包括：该端口仅服务单一功能；它腾出了空间用于其他增强；数字音频比模拟音频提供更优质量。

没有 headphone jack，更易设计防水或防水的设备。此外，这一转变与行业向无线技术的转变一致，像 Google 和 Apple 这样的公司推出了自己的无线耳机（Pixel Buds Pro 和 AirPods）。

### Apple 最终逆转了方向
2021 年，Apple 放弃了不受欢迎的 OLED Touch Bar，并在 MacBook Pro 上恢复了更多端口。正如 The Verge 当时所写，很难忽略更广泛的背景——这些改进有效地将 2021 MacBook Pro 带回 2012 至 2016 年初已提供的功能水平。

Apple 长期坚持的“Less But Better”承诺仍是其持续成功设计消费电子产品的核心支柱。利用极简主义将 Apple 推向成为全球最有价值的公司。

---

## 3. 软件和 OS 示例

### Google Search
在众多杂乱的搜索引擎中，Google 的极简方法——干净界面只有一个 search bar——彻底改变了我们在网上查找信息的方式。

### Basecamp (Project Management)
2004 年最初推出时，Basecamp 的创始人决心创建避免企业平台如 Microsoft Project 中无尽 feature bloat 和复杂界面的项目管理软件。正如 Basecamp 创始人 Jason Fried 解释：“我们故意限制功能数量。”没有复杂的 Gantt charts、自定义 dashboards 或高级 reporting。

### WhatsApp
WhatsApp 以简单前提起步——通过互联网发送消息。通过聚焦这一核心功能并确保可靠性，他们建立了数十亿用户基础。

### Windows 8 / iOS 7 — 视觉简化
Windows 8 实现了“simple, squared-off”的 Metro 外观，比 Windows 7 和 Vista 中的 Aero 界面图形密集度更低。这一变化部分是因为小型电池供电设备的兴起以及节省电力的需要。iOS 7 为用户体验原因进行了类似变化。

### Microsoft 和 Apple 悄然移除功能（且备受争议）
当 Apple 重写 iWork 应用以完全支持 64-bit 和统一文件格式时，发布说明中没有通知功能被移除。客户并不高兴。Apple 表示计划在后续版本中重新引入一些功能。Tesla 也通过软件更新单方面从价值 10 万美元的汽车中移除一项功能，而未通知车主。Amazon 远程删除了用户已在 Kindle 上下载并支付的书籍，而未通知用户。

---

## 4. 为什么“添加容易，移除困难”

这是深刻而重要的问题。有几个维度：

### 技术：Legacy Code 和 Spaghetti Dependencies
旧代码与新代码密不可分。当你尝试移除或更改它时，会产生蝴蝶效应，可能对运营连续性造成毁灭性影响。

处理 legacy systems 中的代码复杂性，以及梳理系统支持的业务流程，会带来巨大挑战。从业务流程和规则中解开数千甚至数百万行代码的复杂性令人生畏。

### 人类：用户抵抗和习惯
除了 IT 团队，最大的障碍往往是终端用户采用。不管新系统多么先进——如果员工拒绝使用，整个项目就胎死腹中。人们抵制变革，尤其是当它打乱他们的工作流程时。

### 商业：害怕丢失客户
如果你移除即使 2% 用户依赖的功能，这些用户可能离开。产品团队倾向于对移除持风险厌恶态度，因为下行风险（丢失真实用户）感觉比上行益处（更干净的产品）更直接。添加功能有明确的成功故事；移除功能没有剪彩时刻。

### 组织：功能所有权和内部政治
在公司内部，每个功能都是由一个团队构建的。该团队拥有所有权、自豪感和商业理由。移除他们的功能在政治上很困难——这暗示他们的工作是浪费的。极简代码库更容易让新团队成员上手、更少出错、更适应变化需求——但实现它们需要实践“You Aren't Gonna Need It”（YAGNI），抵制“以防万一”实现功能的冲动。

### 认知：Feature Bloat 感觉像价值
人类常常将“更多功能”等同于“更好产品”。在一个“更多功能”常被视为“更好产品”的世界中，说服利益相关者拥抱极简主义需要分享成功极简产品的案例研究，并用数据证明专注功能如何带来更高的用户参与度。

---

## 5. 移除的商业理由

更少代码和更少功能意味着更少 bug、减少支持负载、更容易升级。小型专注发布可以快速交付、用真实用户验证并迭代。更简单的软件也更容易审计安全、隐私和监管要求。

减少提供的功能数量可以优化用户的决策。太多选项可能让用户不知所措，最终放弃他们试图完成的任务。

---

## 6. 编码“Less is Better”的工程原则



| Principle | Meaning |
|---|---|
| **KISS** | Keep It Simple, Stupid — 优先简单解决方案 |
| **YAGNI** | You Aren't Gonna Need It — 不要投机构建功能 |
| **DRY** | Don't Repeat Yourself — 减少代码重复 |
| **Unix Philosophy** | Do one thing and do it well |
| **MVP** | Minimum Viable Product — 发布最小有用产品 |

---

## 总结

“less is better”的洞见违反直觉，但在科技历史上被反复证明。添加容易因为它是加法性的——无破坏、无政治斗争，感觉像进步。移除困难因为它破坏依赖、激怒用户、摧毁内部所有权，并需要勇气承认过去工作不必要。Apple 反复的端口和功能移除——有些 brilliant（floppy disk、optical drive），有些过度修正（2016 MacBook Pro ports）——是这种张力的最清晰真实世界实验室。

参考文献：

- [Beyond the Backlog — Less is More in Product Design](https://beyondthebacklog.com/2024/01/20/less-is-more/)
- [Minimalism (computing) — Wikipedia](https://en.wikipedia.org/wiki/Minimalism_(computing))
- [Gitready — Digital Minimalism in Software Engineering](https://gitready.com/the-rise-of-digital-minimalism-in-software-engineering/)
- [The National — When Apple Removed Key Hardware Components](https://www.thenationalnews.com/business/technology/2023/09/12/when-apple-removed-key-hardware-components-on-its-devices-and-turned-out-to-be-right/)
- [PC Gamer — Apple Ports and the Courage Narrative](https://www.pcgamer.com/hardware/7-years-after-declaring-it-took-courage-to-remove-the-iphones-headphone-jack-apple-has-finally-decided-buttons-and-ports-are-cool-again/)
- [TechCrunch — MacBook Pro Kills Off Ports](https://techcrunch.com/2016/10/27/apples-new-macbook-pro-just-killed-off-most-of-the-ports-you-probably-need/)
- [Steve Blank — When Product Features Disappear](https://steveblank.com/2013/11/21/when-product-features-disappear-amazon-apple-and-tesla-and-troubled-future-of-21st-century-consumers/)
- [TechTarget — 6 Reasons Legacy Systems Are Still In Use](https://www.techtarget.com/searchcio/feature/6-reasons-legacy-systems-are-still-in-use)
- [Generaite Labs — Art of Minimalism in Software Engineering](https://generaitelabs.com/the-art-of-minimalism-in-software-engineering-focusing-on-core-features-for-maximum-impact/)
