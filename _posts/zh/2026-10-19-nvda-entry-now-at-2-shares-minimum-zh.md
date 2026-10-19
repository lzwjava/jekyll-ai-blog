---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVDA 入场门槛现降至最低2股
translated: true
type: note
---

完成。NVDA 条目现在的大小改为**至少2股**，而不是1股：

- **`bot/config.py`** — 在 NVDA 工具条目中添加了 `'min_quantity': 2`。
- **`bot/engine.py`** — 在 `open_long()` 中，在“大小过小”检查之后，数量会被提升到工具的 `min_quantity`（默认为1，因此其他工具不受影响）。由于新语句将两个分支分开，`elif dry_run:` 变成了 `if dry_run:`。

已验证：当旧的配仓逻辑在 NVDA 当前价格下产生1股时，现在会得到2股；已经是 ≥ 2 股的大小保持不变，并且“大小过小”跳过逻辑仍然有效。机器人将在下一次符合条件的入场信号时下达第一笔2股的 NVDA 买入订单。