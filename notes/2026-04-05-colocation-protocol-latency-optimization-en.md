---
audio: false
generated: true
image: false
lang: en
layout: post
title: Colocation and Protocol Latency Optimization
translated: false
type: note
---

Question: In quantitative trading, when using a nearby/colocated server to trade on Binance, is the most critical thing to use the REST API to directly place orders and measure order fill time? And does this same principle apply to US stocks, London stocks, and other exchanges?

Answer:

## The Core Concept: What You're Actually Optimizing

Yes — you are correct in spirit, but let's be precise. The **primary metric** being optimized in quantitative/HFT trading is:

> **Round-trip latency**: The time from when your system sends an order to when you receive a confirmed fill (execution confirmation) back.

This is often called **"tick-to-trade"** latency in professional HFT literature.

---

## Why "Nearby Server" (Colocation) Matters

The fundamental idea is placing your own server as close to the exchange's servers as possible to reduce time lost communicating over wires. Most exchanges do not publicly publish their API server's location — so one approach is to ping the exchange from multiple regions and pick the fastest one, since that's probably where the exchange is hosted.

Physical distance creates fundamental latency limits. Light travels at 200,000 km/s in fiber optic cable. For example, the distance from New York to Tokyo creates a minimum one-way latency of around 54ms. For Binance specifically, AWS ap-northeast-1 (Tokyo) is the best-performing region, achieving 5–12ms round-trip latency — a 75% improvement over distant regions.

---

## REST API: Is It the Right Tool for Order Execution?

This is where it gets more nuanced. REST API works, but it is **not the fastest option** for order placement:

### Protocol Speed Comparison (Fastest → Slowest)

| Protocol | Latency Level | Best Use |
| --- | --- | --- |
| **FIX API** | Microseconds | Institutional HFT order execution |
| **WebSocket API** | Low milliseconds | Real-time market data streaming |
| **REST API** | Higher milliseconds | Infrequent orders, account management |

Professional HFT firms optimize for protocol choice, favoring FIX (Financial Information eXchange) rather than REST or WebSockets, while minimizing protocol-induced latency.

Protocols matter enormously: FIX and WebSocket beat REST every time. Binary or custom feeds are faster still.

### Why REST Is Slower

REST API follows a request-response model. Every time your trading bot needs data, it creates a new connection, sends a request, receives a response, and closes the connection. Each request carries connection establishment overhead, and most brokers rate-limit REST APIs to prevent system overload.

### The Better Hybrid Approach

Smart algorithmic traders don't choose between WebSocket and REST — they use both simultaneously. WebSocket handles all market data streaming, live price feeds, order book depth updates, and trade execution confirmations. REST API manages account operations like balance inquiries, historical data queries, and periodic health checks.

### Binance Specifically — WebSocket Order Placement

Binance's documentation includes an option to place orders via WebSocket (not just REST), which can avoid HTTP/REST network overhead for sending orders.

Binance has also introduced SBE (Simple Binary Encoding) Market Data Streams, which offer smaller payloads and better latency than the equivalent JSON streams for latency-sensitive data.

---

## What You Actually Measure: Order Fill Time

The correct measurement approach uses two timestamps per order: a **pre-transmission timestamp** (recorded just before the API request is sent) and a **post-transmission timestamp** (recorded when a successful confirmation is received from the exchange). The round-trip of these two is what you optimize.

This round-trip covers:

1. **Network transit** (your server → exchange gateway)
2. **Exchange matching engine processing**
3. **Confirmation delivery** (exchange → your server, often via WebSocket)

---

## Does This Apply to US Stocks, London Stocks, etc.?

**Yes — universally.** The same principles apply across all electronic markets:

For institutional quantitative trading, a FIX API connection sends orders directly to an exchange's matching engine, bypassing intermediaries and minimizing execution latency. Quantitative funds run high-frequency strategies over FIX — the protocol's microsecond-level speed is a requirement for their business model to function profitably.

In traditional finance, co-location is standard: firms place their servers in the same data center as the exchange, often in the same rack, reducing latency to microseconds. For crypto, true co-location is generally not available — the best you can do is deploy in the same AWS/GCP region as the exchange, which is still orders of magnitude slower than traditional HFT co-location of 10–100 microseconds.

Traditional exchange examples:

- **NYSE/NASDAQ (US stocks)**: Colocation at Mahwah, NJ (NYSE) or Carteret, NJ (NASDAQ) data centers
- **LSE (London stocks)**: Colocation at LD4 Equinix in Slough, UK
- **Binance (Crypto)**: Best via AWS Tokyo (ap-northeast-1)

---

## Summary: The Full Optimization Stack

For serious quantitative trading, the priority order is:

1. **Geographic colocation** — Get your server physically close to the matching engine. Highest ROI improvement.
2. **Protocol choice** — Use FIX API or WebSocket for order execution, not plain REST.
3. **Market data feed** — Use WebSocket (or binary/SBE streams on Binance) for real-time price data.
4. **Measure round-trip latency** — Pre-send to post-confirmation, not just ping times.
5. **Hardware/OS tuning** — Kernel bypass networking (DPDK), CPU pinning, etc. for microsecond-level work.

REST API for order placement is fine for **non-latency-sensitive strategies** (e.g., daily rebalancing, TWAP execution over hours), but for anything competitive in quant trading, WebSocket order placement or FIX API is the correct choice.

References:

- [Latency Analysis of Binance Exchange Across AWS Regions](https://viktoriatsybko.substack.com/p/an-analysis-of-binance-exchange-across)
- [Geographic Latency in Crypto: Colocation Guide](https://elitwilliams.medium.com/geographic-latency-in-crypto-how-to-optimally-co-locate-your-aws-trading-server-to-any-exchange-58965ea173a8)
- [High-Frequency Trading in Crypto: Latency, Infrastructure, and Reality](https://medium.com/@laostjen/high-frequency-trading-in-crypto-latency-infrastructure-and-reality-594e994132fd)
- [AWS: Optimize tick-to-trade latency for digital assets](https://aws.amazon.com/blogs/web3/optimize-tick-to-trade-latency-for-digital-assets-exchanges-and-trading-platforms-on-aws/)
- [FIX vs WebSocket: What to Choose for Your Trading Platform](https://b2prime.com/news/fix-vs-websocket-what-to-choose-for-your-trading-platform)
- [CoinAPI: FIX API vs REST API for Crypto Markets](https://www.coinapi.io/blog/fix-api-vs-rest-api)
- [Binance Developer Changelog](https://developers.binance.com/docs/binance-spot-api-docs)
- [Algo Trading Infrastructure Guide: WebSocket, REST, VPS](https://tradingfxvps.com/api-trading-vps-optimization-2025-websocket-rest-for-algo-strategies/)
