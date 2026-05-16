---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解析加密货币支付路径
translated: true
type: note
---

**问题：** 我成功向 OpenRouter 充值了 10 USDC，从币安转账——路径经过了 MetaMask → Coinbase → Stripe → OpenRouter。这条路径是不是太长了？能解释一下这笔链上交易发生了什么吗？

**回答：**

是的，这确实是一段相当长的旅程！而且查看实际的链上交易，情况比看起来更有趣。以下是完整的详细解析：

---

## 交易摘要

- **状态：** ✅ 成功
- **时间：** 2026 年 5 月 16 日 02:46:17 UTC
- **网络：** Base（以太坊 Layer 2）
- **发送金额：** 10.5 USDC（约 $10.50）
- **OpenRouter 收到金额：** 10.395 USDC（扣除 1% 手续费后）
- **Gas 费：** ~$0.0044（在 Base L2 上极其便宜）

---

## 完整的链上路径

以下是区块链日志记录的每一步具体操作：

### 1. 入口点（ERC-4337 账户抽象）
交易通过 **ERC-4337 账户抽象**（`Entry Point 0.6.0`）发起。这是 Coinbase 智能钱包使用的标准——意味着你的钱包是一个智能合约账户，而非普通的 EOA。你无需自己持有 ETH 支付 Gas 费，而是由 **Paymaster** 赞助 Gas。

### 2. 你的 Coinbase 智能钱包（发送方）
地址 `0x133243d4...be3C566Eb`——这是你在 Base 上持有 USDC 的 Coinbase 管理智能钱包。它授权了一笔 **10.5 USDC** 的转账。

### 3. Coinbase Business：支付协议
10.5 USDC 首先进入 Coinbase 的 **Payment Protocol** 合约（`0x0E3dF951...`）。这是 Coinbase 的 x402 支付基础设施——一个基于 Base 构建的 HTTP 支付协议，支持机器对机器的加密货币支付（被 OpenRouter 的 API 计费系统使用）。

### 4. 费用拆分（通过 x402 路由器 `0x47C5d3fc...`）
支付路由器对资金进行了拆分：
- **0.105 USDC（1%）** → Coinbase 费用接收地址（`0x6D8675A5...`）——这是 Coinbase 的处理费用
- **10.395 USDC（99%）** → OpenRouter 的接收地址（`0x4C3f2E39...`）

### 5. Gas 由 Paymaster 赞助
Gas 费（约 $0.004）由 **Paymaster**（`0x2FAEB076...`）支付，因此你的钱包中完全不需要持有 ETH。这就是账户抽象的魔力所在。

---

## 为什么有这么多跳转？

| 层级 | 角色 |
|---|---|
| 币安 | 你将 USDC 提现到 Base 网络 |
| MetaMask / Coinbase Wallet | 你的钱包界面 |
| Coinbase 智能钱包（ERC-4337） | 链上智能合约钱包 |
| Coinbase x402 支付协议 | 机器对机器支付路由 |
| 费用路由器合约 | 将 1% 费用分给 Coinbase，99% 分给 OpenRouter |
| OpenRouter | 收到 10.395 USDC 作为 API 额度 |

这条路径看起来很长，但实际上相当优雅：
- **Coinbase 的 x402 协议**专为 AI API 计费设计——它允许像 OpenRouter 这样的服务按请求收费，无需传统支付通道（你这边不需要 Stripe 账户）
- **账户抽象**意味着用户零 Gas 摩擦
- 所有操作在 **Base L2** 上数秒内完成，费用不到半美分

---

## 有趣的事实：什么是 x402？

你在交易中看到的 "x402" 标签指的是 **HTTP 402 "Payment Required"（需要付款）** 状态码——这是 Coinbase 对原生网络支付协议的愿景。它专门设计用于让 AI 代理和 API 能够在链上自主地相互支付，无需人工干预。OpenRouter 已集成此功能，因此开发者可以直接使用链上 USDC 为 API 使用量充值。

所以，是的——路径很长，但这是现代加密支付基础设施在高效运转！🎉

**参考链接：**

- [BaseScan 交易记录](https://basescan.org/tx/0x31f501491588da24e706aa199d1a6aa3ce15dea4159458efbeafea3a07ed0ec0)