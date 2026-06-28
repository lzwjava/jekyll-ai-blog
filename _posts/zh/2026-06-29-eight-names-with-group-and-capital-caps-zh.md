---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 八个带分组和大写首字母的名称
translated: true
type: note
---

现在工具有 8 个名称：

| 符号   | 名称         | 策略                | 周期       | 分组       |
| ------ | ------------ | ------------------- | ---------- | --------- |
| AAPL   | Apple        | mean_reversion      | DAY        | risk_on   |
| INTC   | Intel        | mean_reversion      | DAY        | risk_on   |
| AVGO   | Broadcom     | mean_reversion      | DAY        | risk_on   |
| GOOGL  | Alphabet     | mean_reversion      | DAY        | risk_on   |
| PDD    | PDD Holdings | mean_reversion      | DAY        | china     |
| NVDA   | Nvidia       | momentum_breakout   | ONE_HOUR   | risk_on   |
| GLD    | Gold         | trend_following     | FOUR_HOURS | commodity |
| USO    | Crude Oil    | trend_following     | FOUR_HOURS | commodity |

两件值得注意的事：

1. **分组上限交互。** `risk_on` 目前持有 5 个名称（AAPL、INTC、AVGO、GOOGL、NVDA），但 `MAX_GROUP_POSITIONS = 2`，因此机器人**同时最多持有 2 个 risk_on 头寸**——相关性过滤器会跳过其余名称。这是故意设计的（避免堆积在相关的大型科技股上），但由于 5 个候选者竞争 2 个位置，单个名称的交易频率会降低。PDD 在其独立的 `china` 分组中拥有专用位置。如果你希望给大型科技股更多空间，可将 `MAX_GROUP_POSITIONS` 提高到 3。

2. **资金。** 在约 $2k 的账户上，`entry_quantity` 也受到可用现金（`AVAILABLE_FUNDS_BUFFER`）的限制，因此现实中同时只能为其中几个提供资金——分组上限很少成为真正的约束条件。

这两项修改（每日时间周期 + 3 个新符号）仍然**未提交**。需要我将它们一起提交并推送，以便下一次定时运行时生效吗？
