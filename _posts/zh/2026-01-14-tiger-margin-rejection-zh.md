---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 老虎证券交易保证金不足被拒详解
translated: true
type: note
---

Question: 解释 Tiger Trade 的拒绝消息："201:Order rejected - Reason: YOUR ORDER IS NOT ACCEPTED. IN ORDER TO OBTAIN THE DESIRED POSITION YOUR EQUITY WITH LOAN VALUE [636.45 USD] MUST EXCEED THE INITIAL MARGIN [736.92 USD]"

Answer:

这条来自 **Tiger Trade** (Tiger Brokers 平台) 的错误消息意味着您的订单被拒绝，因为您的账户没有足够的 Equity 来满足您尝试开启的交易的 **Initial Margin** 要求。

### 关键术语解释

- **Equity with Loan Value (ELV)**：这是您 Margin Account 中可用于支持杠杆持仓的有效资产净值。它通常等于您资产的总价值（现金 + 证券价值）减去某些调整项（例如某些情况下的 Options 价值），它是计算您可以借入多少资金或使用多少杠杆的基础。
- **Initial Margin (IM)**：这是使用 Margin（杠杆）**开启**新仓位所需的最低 Equity 金额。它通常是总持仓价值的一个百分比，具体取决于资产类型（如 Stock、Futures、Options）。对于许多股票，这一比例可能在 50% 左右，但对于高波动性资产、Options、Futures 或特定工具，比例可能会更高。

该消息明确指出，您的 **Equity with Loan Value ($636.45)** **低于**交易执行后开启该仓位所需的 **Initial Margin ($736.92)**。

### 为什么会发生这种情况

- 您正在使用 **Margin** 交易（向券商借款以扩大持仓规模）。
- 拟议的交易所需的抵押品（Initial Margin）超过了您当前可用的有效资产净值。
- 您的账户缺乏足够的“自有资金”来安全地开启更大的杠杆头寸。
- 这是一项 **Risk Control** 措施——券商（及监管机构）防止过度杠杆化，以避免可能导致的快速亏损或负余额。

### 常见原因

- 账户余额相对于交易规模较低。
- 尝试开启过大的仓位（股数或合约数过多）。
- 交易高 Margin 要求的品种（如高波动性股票、Options、Futures）。
- 近期的亏损降低了您的 Equity。
- 日内盈利可能并不总是完全计入开启新仓位的额度（类似于某些券商在特定情况下使用前一交易日 Equity 的规则）。
- 在非本位币交易时涉及的货币或跨市场问题。

### 如何解决或避免

- **存入更多资金**，使您的 Equity with Loan Value 超过所需的 Initial Margin。
- **减小订单规模**（买入/卖出更少的股数或合约），使所需的 Initial Margin 降至您当前的 ELV 以下。
- **关闭现有仓位**以释放 Margin/Equity。
- **切换到 Cash Account**（如果可行）或者在不想满足杠杆要求时避免 Margin 交易。
- 在 Tiger Trade App 中检查您的账户详情：查看“Account” → Margin/Equity 部分，了解当前的 ELV、Initial Margin 要求、Excess Liquidity 和 Buying Power。
- 查看特定资产的 Margin 要求（Tiger 提供了可融资证券的列表）。

简而言之：您账户的可用 Equity ($636.45) 太低，不足以支持新仓位的 Initial Margin 需求 ($736.92)。请增加资金或减小交易规模以解决此问题。

References:

- [Tiger Trade Help - Margin & Leverage](https://www.tigertrade.app/help/detail/07532949)
- [Tiger Trade Help - Risk State](https://www.tigertrade.app/help/detail/68026009)
