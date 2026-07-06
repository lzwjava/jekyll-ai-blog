---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 量化机器人暂停，DCA移至周三
translated: true
type: note
---

已完成。以下是变更内容：

**停止了量化机器人的策略循环**——`.github/workflows/bot.yml` 仍在仓库中（保留完整，未删除），但除非手动触发，否则不会运行。之前的计划是在美国市场交易时段每15分钟运行一次。工作流文件保留作为量化策略的记录。

**将 DCA 调整至周三**——`.github/workflows/main.yml` 的计划时间从：
- `35 14 * * 4`（每个**周四** 14:35 UTC / 北京时间 22:35）
- 改为 `35 14 * * 3`（每个**周三** 14:35 UTC / 北京时间 22:35）

**invest.py 未改动**——仍通过老虎证券以市价单买入1股 NVDA。代码无任何变化。

**所有量化代码均已保留**——`bot/` 目录（配置、引擎、策略、指标、风控、券商、新闻、报告）、`run_bot.py`、GitHub Actions 工作流——全部保留。如有需要，后续可通过更新 bot.yml 的 `on.schedule` 重新启用。

已推送至 `main` 分支。下一次 DCA 将于本周三北京时间 22:35 执行。