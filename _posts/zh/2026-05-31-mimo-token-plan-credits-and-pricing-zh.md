---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MiMo 代币计划积分与定价
translated: true
type: note
---

**问题：** 小米MiMo Token Plan订阅页面说了什么？（积分、定价和模型消耗比例的完整说明。）

**回答：**

实际文档比我先前的回答详细得多。以下是真实情况：

---

## 1 积分 ≠ 1 token

积分按token扣除，但每个模型每个token消耗的积分数量不同。具体表格如下：

| 模型 | 输入（缓存命中） | 输入（缓存未命中） | 输出 |
|---|---|---|---|
| mimo-v2.5-pro | 2.5 积分/token | 300 积分/token | 600 积分/token |
| mimo-v2.5 | 2 积分/token | 100 积分/token | 200 积分/token |
| mimo-v2-pro | 140 积分/token | 700 积分/token | 2100 积分/token |
| mimo-v2-omni | 56 积分/token | 280 积分/token | 1400 积分/token |
| TTS 系列 | 免费（限时） | 免费 | 免费 |

因此 **1 积分 ≠ 1 token**，恰恰相反：**对于未缓存的输入，1 token 需要花费数百积分**，而缓存命中时仅需几个积分。积分是一种细粒度的内部计价单位，而非 1:1 的 token 别名。

---

## 套餐定价与积分配额

**月度套餐：**

| 套餐 | 价格 | 月度积分 |
|---|---|---|
| Lite | $6/月，¥39/月 | 4.1B 积分 |
| Standard | $16/月，¥99/月 | 11B 积分 |
| Pro | $50/月，¥329/月 | 38B 积分 |
| Max | $100/月，¥659/月 | 82B 积分 |

---

## 实际示例

如果你订阅了 Lite（4.1B 积分），并在 mimo-v2.5-pro 上使用了 1000 万未缓存的输入 token，这将消耗 3000M 积分（10M × 300），剩余 1100M 积分——大致相当于在 mimo-v2.5 上使用 550 万未缓存的输入 token（按 200 积分/输出 token 计算）。

---

## 关键说明

- **夜间折扣：** 非高峰时段（北京时间 00:00–08:00）消耗系数为 0.8 倍。
- **配额耗尽：** 服务停止；不会回退到你的余额或奖励积分。
- **Token Plan API 密钥** 使用 `tp-xxxxx` 格式，与常规按量付费的 `sk-xxxxx` 密钥不同。
- **兼容 Anthropic 的端点** 可用：例如 `https://token-plan-sgp.xiaomimimo.com/anthropic`，因此你可以将 Claude Code 直接指向 MiMo。

**重要限制：** Token Plan 配额只能用于编程工具（OpenClaw、OpenCode、Claude Code 等）。将 API 密钥用于编程场景之外的自动化脚本或自定义应用后端视为违规，可能导致账号暂停。

---

**参考：**

- [MiMo Token Plan 订阅文档（zh-CN）](https://platform.xiaomimimo.com/docs/zh-CN/price/tokenplan/subscription)
