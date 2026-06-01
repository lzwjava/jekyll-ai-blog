---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DigitalOcean积分与GPU推广指南
translated: true
type: note
---

**问题：** DigitalOcean 积分系统是如何运作的 —— 具体来说，是账单仪表板中显示的 AMD Dev Cloud GPU Promotion 积分。

**回答：**

这属于直接的账单机制：

**你看到的内容：**

| 字段 | 数值 | 含义 |
|---|---|---|
| 总计可用 | $99.97 | 可用于抵扣下一张账单的积分 |
| 促销名称 | AMD Dev Cloud GPU Promotion | 可能是 AMD 或 DigitalOcean 的合作/促销积分 |
| 过期时间 | 2026 年 6 月 26 日 | 积分约在 25 天后过期 |
| 初始额度 | $100.00 | 你获得了 $100 积分 |
| 剩余金额 | $72.36 | 目前已消耗约 $27.64 |

**实际运作机制：**

1. 每月账单生成时，DigitalOcean 会自动先使用可用积分，再扣款你的支付方式
2. 积分按 FIFO（先到期先使用）顺序消耗
3. 显示的“总计可用”$99.97 = $72.36 剩余促销积分 + 其他小额积分（可能来自推荐奖励或其他来源，这解释了 $99.97 与 $72.36 的差异）

**对你而言的关键数据：**

- 你已消耗约 $27.64 促销积分 → 按 MI300X 约 $2/小时计算，相当于使用了约 **13.8 小时** GPU 时长
- 剩余 $72.36 → 促销积分还剩约 **36 小时** 可用
- 促销积分于 6 月 26 日过期 —— 你还有 **25 天**，但在扣款到你信用卡前，实际上只有约 36 个计费小时

**操作建议：**

```bash
# 查看当前 droplet/GPU 消费速率
# DigitalOcean API — 列出当前资源
curl -X GET "https://api.digitalocean.com/v2/droplets" \
  -H "Authorization: Bearer $DO_TOKEN" | jq '.droplets[] | {name, size, status}'
```

- 如果有排队的训练任务，**优先在 6 月 26 日前执行**
- 不要让闲置的 GPU droplet 浪费积分 —— 不使用时确保没有运行中的资源
- $72.36 按 $2/小时计 = 可用于集中冲刺的预算（微调任务、GPT-2 实验等）