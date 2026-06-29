---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 每日均值回归配置更新
translated: true
type: note
---

已提交并推送。

- **提交：** `ec948f7`（位于 `main` 分支）
- **推送至** `origin/main`（`e521e46..ec948f7`）

下一次计划运行（美股交易时段每15分钟一次的交易循环，UTC时间 `2,17,32,47 13-20 * * 1-5`）将使用新的配置：AAPL/INTC 的日线数据，以及三个新名称（AVGO、GOOGL、PDD）。由于这些现在都是日线均值回归策略，它们将以波段持仓的方式交易，不会触发 PDT 规则。

您可以在市场开盘后使用 `gh run list` 查看首次使用该配置的运行情况，或通过工作流的 `workflow_dispatch`（`run` 作业）手动触发一次。
