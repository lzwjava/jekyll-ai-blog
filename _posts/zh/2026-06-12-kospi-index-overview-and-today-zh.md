---
audio: false
generated: true
image: false
lang: zh
layout: post
title: KOSPI指数概述与今日
translated: true
type: note
---

**问题：** 什么是KOSPI指数，目前处于什么水平？

**答案：**

KOSPI（韩国综合股价指数）是韩国的主要股市基准，追踪在韩国交易所（KRX）上市的主要公司。该指数于1980年推出，基值为100，采用自由流通市值加权法计算，由三星电子和SK海力士等科技/出口巨头主导——因此它实际上是全球半导体和AI硬件周期的替代指标。

当前状况（截至最近收盘）：KOSPI指数收于8,123.62点，较前一收盘价7,763.95点上涨4.63%（+359.67点）。近期该指数波动剧烈——周三因美伊紧张局势升级以及美国芯片股抛售潮重创三星电子和SK海力士，指数暴跌4.52%至7,731点，随后迅速反弹。纵观全局，该指数正处于历史性的AI驱动牛市：2026年6月2日曾触及8,933.62点的历史新高，同比上涨约179%，52周波动范围约为2,877点至8,934点——一年内近乎翻三倍，这也解释了估值为何受到质疑。近期外国投资者持续抛售韩国股票，巴克莱银行认为日本日经指数目前比KOSPI更安全。

快速参考：股票代码为`^KS11`（雅虎）/`KS11`（Investing.com），以韩元计价，交易时间为韩国标准时间9:00–15:30。如需通过编程方式获取数据：

```python
import yfinance as yf
kospi = yf.Ticker("^KS11")
print(kospi.history(period="5d")[["Close"]])
```

**参考资料：**

- [KOSPI综合指数 — 雅虎财经](https://finance.yahoo.com/quote/%5EKS11/)
- [韩国股票市场 — Trading Economics](https://tradingeconomics.com/south-korea/stock-market)
- [KOSPI — CNBC](https://www.cnbc.com/quotes/.KS11)
