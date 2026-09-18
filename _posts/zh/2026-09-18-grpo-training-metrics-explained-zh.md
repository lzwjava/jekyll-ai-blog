---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GRPO训练指标详解
translated: true
type: note
---

## 问题：这些GRPO/RLHF训练指标是什么意思？

## 答案：

这看起来像是一个**GRPO（组相对策略优化）**训练日志——一种强化学习微调方法（用于DeepSeek-R1风格的训练）。以下是各指标的含义：

---

## 📉 损失与优化

| 指标 | 数值 | 含义 |
|---|---|---|
| `loss` | 0.0001647 | 策略损失极低——模型稳定 |
| `grad_norm` | 0.6875 | 梯度幅度；健康范围（未爆炸/未消失） |
| `learning_rate` | 4.571e-06 | 调度器衰减后的当前学习率 |
| `num_tokens` | ~101,600 | 此步骤处理的标记数 |

---

## 📝 补全统计

| 指标 | 数值 | 含义 |
|---|---|---|
| `mean_length` | 60.25 个标记 | 生成的平均响应长度 |
| `min/max_length` | 9 / 148 | 响应长度范围 |
| `clipped_ratio` | 0 | 没有生成被 `max_new_tokens` 截断——良好 |
| `terminated_*` | 同上 | 自然结束（EOS 标记）的响应长度 |

---

## 🏆 奖励信号

| 指标 | 数值 | 含义 |
|---|---|---|
| `rewards/reward_format/mean` | **0.0** | ⚠️ 格式奖励为零——模型未遵循预期的输出格式 |
| `rewards/reward_correctness/mean` | **0.8125** | ✅ 81.25% 的答案正确 |
| `rewards/reward_correctness/std` | 0.5303 | 方差高——部分正确，部分错误（二元化奖励） |
| `reward` | 0.8125 | 总奖励（格式 + 正确性合并） |
| `reward_std` | 0.5303 | 组内奖励方差 |
| `frac_reward_zero_std` | **0.5** | 50% 的组奖励方差为零 → 一半组全部正确或全部错误 |

---

## 📊 策略行为（KL 散度与熵）

| 指标 | 数值 | 含义 |
|---|---|---|
| `kl` | 0.008645 | 与参考模型的 KL 散度非常小——策略偏离不大 |
| `entropy` | 0.7208 | 熵低 → 模型输出相当自信/确定性高 |
| `clip_ratio/*` | 全部为 0 | 未触发 PPO 式裁剪——更新小而安全 |

---

## ⏱️ 训练进度

| 指标 | 数值 | 含义 |
|---|---|---|
| `step_time` | 5.263 秒 | 每个训练步骤耗时 |
| `epoch` | 0.2658 | 第 1 个 epoch 完成约 26.6%——训练早期 |

---

## 🔍 关键要点

1. **正确率高（81%）**——基础模型大多数情况下回答正确
2. **格式奖励为 0**——模型忽略了格式约束（例如 ` 思考` 标签、JSON 等）——这需要关注
3. **`frac_reward_zero_std = 0.5`** 意味着 GRPO 对一半组没有学习信号（奖励全部相同），这会减慢训练速度
4. **KL 很小**——模型几乎没有偏离基础，可能是因为格式奖励没有推动它

---

参考资料：
- [GRPO 论文 (DeepSeekMath)](https://arxiv.org/abs/2402.03300)
- [TRL GRPO 训练器文档](https://huggingface.co/docs/trl/grpo_trainer)