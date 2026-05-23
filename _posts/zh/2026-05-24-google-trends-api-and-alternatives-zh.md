---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 谷歌趋势API与替代方案
translated: true
type: note
---

**问题：** Google Trends 有 API 吗？

**回答：**

有的——而且这还是最近才推出的。以下是完整情况：

---

## 官方 Google Trends API（Alpha 阶段，2025 年 7 月）

谷歌于 2025 年 7 月 24 日宣布了官方 Google Trends API——这是多年来用户反复要求后，他们首次推出 Trends 的 API。

关键信息：
- 数据回溯 5 年——一个滚动 1800 天的时间窗口，数据更新至约 2 天前。
- 提供结构化数据：随时间变化的兴趣度、热门趋势及相关查询。
- 目前处于 Alpha 阶段，访问受限——需要申请。谷歌正在控制发布以收集反馈，随后再扩大开放。

申请/了解更多：[developers.google.com/search/blog/2025/07/trends-api](https://developers.google.com/search/blog/2025/07/trends-api)

---

## 实用替代方案（由于 Alpha 访问受限）

### 1. `pytrends`（非官方 Python 封装）
经典的常用工具，但越来越不可靠：

```python
pip install pytrends

from pytrends.request import TrendReq
import pandas as pd

pt = TrendReq(hl='en-US', tz=360)
pt.build_payload(kw_list=['Claude AI', 'ChatGPT'], timeframe='today 12-m')

df = pt.interest_over_time()
print(df)

# 相关查询
related = pt.related_queries()
print(related)
```

PyTrends 已不再积极维护，且经常因谷歌更新内部端点而中断——不适合生产环境使用。

### 2. SerpApi（付费，可靠）
付费抓取服务，提供正式的 Google Trends 端点。如果你需要稳定性，效果很好：

```python
import serpapi

client = serpapi.Client(api_key="YOUR_KEY")
results = client.search({
    "engine": "google_trends",
    "q": "Claude AI",
    "date": "today 12-m"
})
print(results["interest_over_time"])
```

### 3. Apify Actor（提供免费套餐）
一个托管替代方案，自动处理 Cookie 轮换、代理管理和 429 重试——无需自己处理验证码或 IP 轮换。支持类似 pytrends 的时间范围字符串，如 `today 12-m`、`today 5-y`。

### 4. Glimpse API（企业级）
在 Google Trends 的 0-100 相对评分基础上增加了绝对搜索量。对于生产环境仪表盘更准确。

---

## TL;DR

| 选项 | 费用 | 稳定性 | 备注 |
|---|---|---|---|
| 官方 API | 免费（Alpha） | 高 | 需要申请 |
| pytrends | 免费 | 低 | 经常出问题 |
| SerpApi | 付费 | 高 | 按查询计费 |
| Apify Actor | 免费套餐 | 中等 | 适合脚本 |
| Glimpse | 付费（企业级） | 高 | 提供绝对量 |

对于你的用例（构建 Agent、CLI 工具），建议先用 `pytrends` 快速原型验证，并申请官方 Alpha 访问权限。如果你需要将趋势信号输入到任何规模的 LLM 管道中，那么 SerpApi 或 Glimpse 比调试 `pytrends` 的 429 错误更划算。

**参考资料：**

- [Google Trends API Alpha 公告](https://developers.google.com/search/blog/2025/07/trends-api)
- [2026 年最佳 Google Trends 抓取 API — ScrapingBee](https://www.scrapingbee.com/blog/best-google-trends-api/)
- [pytrends 替代方案 — Glimpse](https://meetglimpse.com/software-guides/pytrends-alternatives/)
- [Apify 免费 Google Trends Actor](https://apify.com/s-r/free-google-trends-actor)