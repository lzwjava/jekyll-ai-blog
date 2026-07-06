---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TCSP持牌人登记册条目
translated: true
type: note
---

**问题：** 我看到的是什么表格——一行显示"TC010660, Hong Kong Blue Bridge International Business Limited"，商业地址在葵涌？

**回答：**

您粘贴的内容来自香港**TCSP持牌人公开登记册**——这是由公司注册处维护的可搜索数据库，网址为 tcsp.cr.gov.hk。TCSP 代表 **Trust or Company Service Provider**（信托或公司服务提供者）。

背景如下：2018年3月之前，任何人在香港都可以开店为客户注册公司，几乎不受审查。这一情况在《打击洗钱及恐怖分子资金筹集条例》(AMLO，第615章)生效后发生了改变——从那时起，公司服务业务需要持牌经营、通过适当人选测试并接受合规审计，由公司注册处通过专门的TCSP牌照办公室进行监管。无牌经营信托或公司服务业务即属违法，最高可处以10万港元罚款及6个月监禁。

TCSP持牌人是指依法获准从事以下业务的公司：成立公司、担任（或安排）董事或公司秘书、提供注册办事处或商业/通讯地址、担任明示信托的受托人或代名人股东。每个牌照有效期为3年，并记录持牌人的名称及商业地址——这正是您那一行所显示的内容：

- **牌照编号** — `TC010660`，唯一的牌照识别码
- **名称 (英文/中文)** — 持牌实体，此处为葵涌的一家公司
- **商业地址** — 注册的营业地点
- **备注** — 通常标注条件、暂停或状态说明

登记册本身是开放数据：TCSP持牌人的完整名单由公司注册处在 DATA.GOV.HK 上发布，每月更新，可通过 XLSX、CSV 或 API 下载。因此，如果您想以编程方式抓取或分析这些数据（例如，为您的香港实体寻找公司秘书公司），无需抓取搜索界面——直接拉取 CSV 文件即可。

**这对您的具体意义：** 当您注册香港实体时（操作手册第8项），您聘请的负责公司注册、公司秘书及注册地址服务的公司*必须*出现在此登记册中。在这里核对牌照号码是您的尽职调查步骤——无牌服务商是一个危险信号。另请注意，"Blue Bridge International Business"是典型的注册代理公司名称；此类公司数以千计（截至2024年中约有7,000家持牌人），因此请比较价格和声誉，而不仅仅是牌照状态。

**参考资料：**

- [TCSP持牌人登记册 — 公开搜索](https://www.tcsp.cr.gov.hk/tcspls/search/public-search)
- [TCSP持牌人名单 — DATA.GOV.HK 开放数据集](https://data.gov.hk/en-data/dataset/hk-cr-crtcspdata-list-tcsp-licensees)
- [香港TCSP牌照申请完整指南](https://kyc.management/en-hk/resources/a-complete-guide-to-obtaining-a-tcsp-licence-in-hong-kong)