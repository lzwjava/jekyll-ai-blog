---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Stripe Link 概述与优势
translated: true
type: note
---

**问题：** 什么是 Stripe Link，它是如何工作的？

**答案：**

## 什么是 Stripe Link？

Link 是 Stripe 的数字钱包。它让客户能够安全地保存并重复使用支付方式，实现快速结账。在可用地区，客户可以使用银行卡、银行账户、先买后付选项以及其他方式进行支付。

---

## 核心功能

### 一键/快速结账
Link 可在任何设备、浏览器及支持的 AI 代理中，通过几个简单步骤自动填充客户已保存的信息。客户数据经过加密以确保安全，作为经认证的 PCI 一级服务提供商，Link 达到了支付行业可获得的最高级别认证标准。

### 身份验证方式
当客户在新网站或新设备上使用 Link 时，会通过短信收到一次性验证码，以验证其身份并保障支付信息安全。当客户输入电子邮件地址时，Link 会立即填充其保存的支付详情，使其能在任何支持 Link 的网站上快速结账。

### 支持的支付方式
用户可关联银行卡、银行账户、加密钱包及先买后付服务等支付方式，同时还能保存在线结账所需的重要信息，如账单和收货地址。

### 交易确认与结算
所有 Link 交易均即时确认，成功付款的结算时间与银行卡支付相同，无论为支付提供资金的支付方式是什么，都将结算到您的 Stripe 余额中。

---

## 对商家的益处

拥有大量回头客的商家，其回头客转化率平均提升了 14%。客户结账速度比非 Link 用户快 3 倍。Link 还能帮助商家触达全球超过 2 亿消费者，并已内置在数十万个由 Stripe 提供支持的网站中。

当客户使用比银行卡成本更低的替代支付方式（如仅通过 Link 提供的即时银行支付）时，商家还能降低处理成本。

---

## 适用范围

Link 适用于 Checkout、Payment Links、Web Elements、Mobile Elements 以及 Invoicing。它可用于 Express Checkout Element 和 Card Element 集成。Link 也适用于原生的 iOS、Android 和 React Native 应用。

对于 40 多个国家和地区的商家和平台，Link 可通过 Payment Element 无缝集成到结账流程中。Link 已内置到现有的 Stripe 支付集成中，无需额外费用。

---

## AI 代理支持（2026 年新功能）

Stripe 已升级 Link 以支持自主 AI 代理，使其能够执行购物、支付预订、购票等任务。用户可关联其 AI 代理并授予支付权限，而无需暴露其支付凭证。

要使用此功能，用户首先需通过 OAuth 身份验证流程授权 AI 代理访问其 Link 钱包。然后，AI 代理可以创建支付请求、提供上下文信息，并等待用户批准。在移动端和网页端，用户会收到通知，在支付凭证与 AI 代理共享之前批准该支付请求。

---

## 退款与争议

Link 支持全额和部分退款，可通过 Stripe 管理平台或 API 发起。退款流程通常在 5-10 个工作日内完成，具体取决于银行。针对 Link 付款的争议处理流程与银行卡争议类似，可通过 Stripe 管理平台或 API 进行回应。

---

**参考文献：**

- [Stripe Link 概述](https://stripe.com/payments/link)
- [Stripe Link 文档](https://docs.stripe.com/payments/link)
- [Stripe Link 钱包文档](https://docs.stripe.com/payments/wallets/link)
- [TechCrunch：面向 AI 代理的 Stripe Link](https://techcrunch.com/2026/04/30/stripe-link-digital-wallet-ai-agents-shopping/)