---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 快捷支付系统集成指南
translated: true
type: note
---

香港的快速支付系统（FPS）由香港银行同业结算有限公司（HKICL）运营，并受香港金融管理局（HKMA）监管。该系统并未向银行提供公开的软件开发工具包（SDK）进行集成。银行需通过直接连接FPS基础设施完成对接，相关技术规范会在参与银行（即结算参与者）加入时私下共享。这些规范指导银行升级其系统以接入FPS，但官方文档中并未提及现成的SDK或开发工具包。

关于API，FPS目前并未提供专门供外部或第三方集成的API。不过，该系统与金管局推行的「香港银行业开放API框架」（于2018年推出并分阶段更新至2025年）相衔接，鼓励银行通过API向第三方服务提供商开放部分功能（如账户信息或支付发起）。FPS交易可间接利用此框架实现支付发起等功能，但尚未提供FPS专用API——出于安全及监管考虑，访问权限仍按需受限。金管局将持续关注相关进展，未来或会扩展API支持。

### 银行接入核心要点

- **连接方式**：银行可通过IBM MQ消息传递实现实时处理，或通过文件传输（如经HKICL安全网络ICLNET）进行批量处理。系统全天候运行。
- **报文标准**：所有通信均采用ISO 20022格式，支持丰富数据字段、中文字符及系统互操作性。
- **接入流程**：银行需向金管局（港元业务）或中国银行（香港）（人民币业务）注册，签署《FPS规则协议》，根据提供的技术规范改造系统，通过HKICL测试后正式上线。所有持牌银行必须作为直接结算机构参与。
- **其他特性**：支持代理标识（如手机号/邮箱）、二维码（EMV标准）及多币种（港元/人民币）转账。认证遵循金管局双重认证指引，交易限额由各银行自行设定。

关于详细技术规范，银行须在注册后直接联系HKICL获取，因相关文件不对外公开下载。

[快速支付系统（FPS） - 香港金融管理局](https://www.hkma.gov.hk/eng/key-functions/international-financial-centre/financial-market-infrastructure/faster-payment-system-fps/)
[计划文件 - HKICL FPS](https://fps.hkicl.com.hk/eng/fps/about_fps/scheme_documentation.php)
[世界银行FPS案例研究：香港](https://fastpayments.worldbank.org/sites/default/files/2021-09/World_Bank_FPS_Hong_Kong_SAR_China_FPS_Case_Study.pdf)
[银行业开放API框架 - 香港金融管理局](https://www.hkma.gov.hk/eng/key-functions/international-financial-centre/fintech/open-application-programming-interface-api-for-the-banking-sector/)
