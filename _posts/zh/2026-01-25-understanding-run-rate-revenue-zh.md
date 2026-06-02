---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 简单理解运行率收入
translated: true
type: note
---

Question: What does run-rate revenue mean?

Answer:

**Run-rate revenue**（也称为 **annualized run rate** 或 **ARR run rate**）是一种根据当前的业绩表现，假设在没有任何变化的情况下持续发展，来推算公司全年总收入的方法。

它通常被以下对象使用：

- Startups 和 SaaS 公司
- 快速增长的企业
- 拥有 Recurring revenue（经常性收入）的公司
- 准备融资或进行投资者演示的公司

### Main ways to calculate run-rate revenue

1. **最常见的公式 (Monthly run rate)**
   Annual Run Rate (ARR) = 当前的 Monthly recurring revenue (MRR) × 12

   Example:
   如果一家 SaaS 公司在 2026 年 1 月的 MRR 为 $85,000
   → Run-rate revenue = $85,000 × 12 = **$1,020,000 ARR**

2. **Quarterly run rate**
   Annual Run Rate = 当前季度收入 × 4

   Example:
   第一季度收入 = $320,000
   → Run-rate revenue = $320,000 × 4 = **$1,280,000**

3. **Last month / last week annualized**（通常用于极早期阶段或超高增长阶段）
   上个月收入 × 12
   或
   上周收入 × 52

### Important caveats

- Run-rate 是**前瞻性的且乐观的** —— 它假设当前月度/季度的表现将在接下来的 12 个月内完全保持一致（没有增长，没有 Churn，没有季节性波动，也没有大的新订单）。
- 它**并不等于**你实际将获得的收入 —— 大多数公司最终的实际收入要么超过、要么低于其 Run-rate 预测。
- 投资者通常会同时查看 **Run-rate** 和实际的 **Trailing Twelve Months (TTM)** 收入。
- 在 SaaS 领域，人们通常更倾向于使用 **ARR** (Annual Recurring Revenue) 而非简单的 Run-rate，因为 ARR 通常只包含已签约的 Recurring revenue，而不包含一次性费用（One-time fees）。

### Quick comparison

| Metric | What it shows | Time period | Usually more conservative? |
| :--- | :--- | :--- | :--- |
| TTM Revenue | 过去 12 个月的实际收入 | Past | Yes |
| Run-rate revenue | 如果当前节奏持续 12 个月的结果 | Future (projected) | No – 往往更高 |
| ARR (SaaS) | 年度化的已签约经常性收入 | Current + future | 比原始 Run-rate 更保守 |

简而言之：
Run-rate revenue = 一种简单的表达方式，意思是 **“如果我们保持现在的表现，一整年的业绩大概就是这样。”**

References:

- None (standard business/finance term, no specific source needed)
