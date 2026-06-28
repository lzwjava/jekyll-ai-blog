---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 均值回归现在使用日线柱
translated: true
type: note
---

已完成。更改如下：

```python
{'symbol': 'AAPL', ... 'strategy': 'mean_reversion', 'period': BarPeriod.DAY, ...}
{'symbol': 'INTC', ... 'strategy': 'mean_reversion', 'period': BarPeriod.DAY, ...}
```

**此更改对行为的影响：**

- 两个名称现在均以**日线**而非15分钟线评估均值回归策略。z-score窗口（`ZSCORE_WINDOW=20`）现在使用20*天*的历史数据，而非20个15分钟K线；`BARS_LIMIT=120`提供120天——足够充裕。
- 开仓和平仓现在自然落在**不同的日历日**，因此不再计入日内交易。PDT防护（`engine.py:84-88`）不再针对这些名称触发，机器人能够真正执行退出信号，而非推迟执行。
- 每15分钟的cron定时任务保持不变且无害——日线每个交易时段只更新一次，但机器人仍会在每次运行时重新检查持仓/止损。

**无需改动其他代码**——`engine.py`、`risk.py`和`strategies.py`均从交易品种配置中读取周期，因此会自动采用新设置。`NVDA`（1小时动量）、`GLD`/`USO`（4小时趋势）保持不变。

这仅是对一个很小的策略表进行配置修改——风险较低。我尚未提交。是否需要我提交（并可选择推送，以便下次定时运行时使用）？