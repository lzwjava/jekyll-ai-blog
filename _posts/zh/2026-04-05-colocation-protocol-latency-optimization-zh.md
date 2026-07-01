---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 主机托管和协议延迟优化
translated: true
type: note
---

## 核心概念：实际优化目标

是的——你的理解方向正确，但需要更精确些。在量化/高频交易中优化的**首要指标**是：

> **往返延迟**：从你的系统发送订单到收到确认成交（执行确认）的时间。

这在专业高频交易文献中常被称为 **“报价到交易”** 延迟。

---

## 为何“附近服务器”（托管共置）重要

核心理念是将你自己的服务器放置在尽可能靠近交易所服务器的地方，以减少线路上通信损失的时间。大多数交易所不公开其API服务器的位置——因此一种方法是从多个区域ping交易所并选择最快的那个，因为那很可能就是交易所的托管地。

物理距离会带来根本性的延迟限制。光在光纤中传播速度为200,000 km/s。例如，从纽约到东京的距离会产生至少约54毫秒的单向延迟。具体对于币安而言，AWS ap-northeast-1（东京）是性能最佳的区域，可实现5-12毫秒的往返延迟——比遥远区域提升了75%。

---

## REST API：它是下单执行的正确工具吗？

这里需要更细致的分析。REST API可行，但**并非最快的**下单方式：

### 协议速度比较（最快 → 最慢）

| 协议 | 延迟级别 | 最佳用途 |
| --- | --- | --- |
| **FIX API** | 微秒级 | 机构高频交易的下单执行 |
| **WebSocket API** | 低毫秒级 | 实时市场数据流 |
| **REST API** | 高毫秒级 | 低频下单、账户管理 |

专业高频交易公司会优化协议选择，偏好FIX（金融信息交换协议）而非REST或WebSocket，并最小化协议引入的延迟。

协议极其重要：FIX和WebSocket总是优于REST。二进制或自定义数据流则更快。

### 为何REST更慢

REST API遵循请求-响应模型。每次你的交易机器人需要数据时，它都需要建立新连接、发送请求、接收响应并关闭连接。每个请求都带有连接建立的开销，且大多数经纪商会对REST API进行速率限制以防止系统过载。

### 更优的混合方法

聪明的算法交易者不会在WebSocket和REST之间二选一——他们会同时使用两者。WebSocket处理所有市场数据流、实时价格推送、订单簿深度更新以及交易执行确认。REST API则管理账户操作，如余额查询、历史数据查询和定期健康检查。

### 币安特例——通过WebSocket下单

币安的文档中包含通过WebSocket（不仅仅是REST）下单的选项，这可以避免HTTP/REST网络开销。

币安还引入了SBE（简单二进制编码）市场数据流，与等效的JSON流相比，它具有更小的有效载荷和更低的延迟，适合对延迟敏感的数据。

---

## 实际测量对象：订单成交时间

正确的测量方法是为每个订单使用两个时间戳：**发送前时间戳**（记录在API请求发送前一刻）和**发送后时间戳**（记录在从交易所收到成功确认时）。这两者之间的往返时间就是你优化的目标。

这个往返时间包括：

1. **网络传输**（你的服务器 → 交易所网关）
2. **交易所撮合引擎处理**
3. **确认返回**（交易所 → 你的服务器，通常通过WebSocket）

---

## 这适用于美股、伦股等市场吗？

**是的——普遍适用。** 相同原则在所有电子市场都适用：

对于机构量化交易，FIX API连接直接将订单发送至交易所的撮合引擎，绕过中间环节，最小化执行延迟。量化基金通过FIX运行高频策略——该协议的微秒级速度是其商业模式能够盈利运行的必要条件。

在传统金融领域，托管共置是标准做法：公司将服务器放置在交易所所在的同一数据中心，通常在同一机架内，将延迟降至微秒级。对于加密货币，真正的托管共置通常不可用——你能做的最好部署是在与交易所相同的AWS/GCP区域，这仍然比传统高频交易10-100微秒的托管共置慢得多。

传统交易所例子：

- **纽交所/纳斯达克（美股）**：托管共置于Mahwah, NJ（NYSE）或Carteret, NJ（NASDAQ）的数据中心
- **伦交所（伦敦股票）**：托管共置于英国斯劳的LD4 Equinix
- **币安（加密货币）**：最佳选择是通过AWS东京（ap-northeast-1）

---

## 总结：完整的优化栈

对于严肃的量化交易，优先级顺序是：

1. **地理位置托管共置** —— 将您的服务器物理上靠近撮合引擎。投资回报率最高的改进。
2. **协议选择** —— 使用FIX API或WebSocket进行下单执行，而非普通REST。
3. **市场数据源** —— 使用WebSocket（或币安上的二进制/SBE数据流）获取实时价格数据。
4. **测量往返延迟** —— 测量“发送前到确认后”的全程时间，不仅仅是ping时间。
5. **硬件/操作系统调优** —— 内核旁路网络（DPDK）、CPU绑定等，用于微秒级工作。

对于**非延迟敏感的策略**（例如，每日再平衡、数小时的TWAP执行），使用REST API下单是可接受的；但对于量化交易中的任何竞争性策略，WebSocket下单或FIX API才是正确的选择。

参考文献：

- [币安交易所跨AWS区域延迟分析](https://viktoriatsybko.substack.com/p/an-analysis-of-binance-exchange-across)
- [加密货币中的地理延迟：托管共置指南](https://elitwilliams.medium.com/geographic-latency-in-crypto-how-to-optimally-co-locate-your-aws-trading-server-to-any-exchange-58965ea173a8)
- [加密货币中的高频交易：延迟、基础设施与现实](https://medium.com/@laostjen/high-frequency-trading-in-crypto-latency-infrastructure-and-reality-594e994132fd)
- [AWS：为数字资产优化报价到交易延迟](https://aws.amazon.com/blogs/web3/optimize-tick-to-trade-latency-for-digital-assets-exchanges-and-trading-platforms-on-aws/)
- [FIX对比WebSocket：为您的交易平台选择什么](https://b2prime.com/news/fix-vs-websocket-what-to-choose-for-your-trading-platform)
- [CoinAPI：针对加密货币市场的FIX API对比REST API](https://www.coinapi.io/blog/fix-api-vs-rest-api)
- [币安开发者更新日志](https://developers.binance.com/docs/binance-spot-api-docs)
- [算法交易基础设施指南：WebSocket、REST、VPS](https://tradingfxvps.com/api-trading-vps-optimization-2025-websocket-rest-for-algo-strategies/)
