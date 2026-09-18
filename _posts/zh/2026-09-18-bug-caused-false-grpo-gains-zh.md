---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Bug导致虚假GRPO增益
translated: true
type: note
---

已保存并验证。当前状态如下——之前的矛盾已化解为实际的主要发现。

## 已保存

| 文件 | 说明 |
| --- | --- |
| `/mnt/data/zz/eval_grpo_adapter.py` | 统一的 base 与 adapter 评估脚本。`--mode indist/ood`、`--greedy`、`--show-samples`、`--save-json`。取代了两个一次性脚本。 |
| `/mnt/data/zz/grpo-rl/headroom.py` | 按类别的 base 准确率，并给出 `saturated / little headroom / GOOD / too hard` 的类别结论。 |
| `/mnt/data/zz/grpo-rl/run2.sh` | Run-2 配置：`--difficulty harder`、`--format-warmup 512`、1 epoch。 |
| `/mnt/data/zz/grpo-rl/train_grpo.py` | 新增 `--difficulty`、`--format-warmup`、`--warmup-lr`、最佳 checkpoint 跟踪，以及提取修复。 |

所有脚本均已通过语法检查并在 GPU 上实际运行。`--format-warmup` 已验证：格式奖励在 8 步内从 **0.00 → 0.30**（最大值），峰值显存 2.12 GB。`run2.sh` 已配置好，但**尚未启动**。

## 矛盾化解后的真正发现

我之前 79% 的 “harder” 检查使用的是 `headroom.py` 的提取逻辑；83% 这个数字来自 `eval_grpo_adapter.py`，而它仍然带有 run 1 的**有 bug** 的规则。同样的 64 个 greedy prompts、同一个 base 模型、两条规则对比：

```
OLD rule (what run 1 trained on):  53/64 = 82.8%
NEW rule (fixed):                  64/64 = 100.0%
stray  response with no number after it: 11/64
answers rescued by the fix:            11
```

**Run 1 的全部测量提升都来自这个 bug。** 82.8% → 100% 正好对应那 11 个游离标签补全，而 base 模型在训练分布上已经达到 100%。GRPO 只是教会它不再输出一个游离的 `response`——这是奖励函数造成的 token 习惯——和算术毫无关系。我之前说 “它专门修复了 `(a+b)*c` 的错误” 是错的；那些就是同样的 11 个产物。

更糟的是，`rewards/reward_format/mean` 在整个 run 中都是 0.0，所以它甚至从未学会预期的格式。它只是不再关闭一个它从未打开过的标签。

## `headroom.py` 的结果——一切均已饱和

```
=== Qwen/Qwen2.5-1.5B - greedy, 10 problems/category ===
add2      10/10  100%    add3   10/10  100%    sub3  10/10  100%
mul1      10/10  100%    mul2    9/10   90%    twoterm 10/10 100%
threeterm 10/10  100%
Best training tiers: NONE - everything is saturated or too hard
```

所以，base 模型已经能处理两位数的乘法和三项表达式。**Greedy 饱和本身并不能证明没有梯度**——GRPO 以 T=1.0 采样，关键是一个 prompt 的 G=4 个样本是否获得*不同*的奖励。我的探针用错了工具。但这确实意味着 `run2.sh` 的 “harder” 档能带来的收益远比我注释中所声称的少，而且 `eval_grpo_adapter.py` 在 greedy 解码下已经无法再展示合成算术上的提升了。

## 在启动 run 2 之前我会做的事

两个低成本的测量就能决定是否启动：

1. `headroom.py --gsm8k 24` —— 文字应用题是 1.5B base 模型真正可能薄弱的唯一地方，而且它们能让 `thinking` 真正有意义。
2. T=1.0 group-variance 探针：对 `standard`、`harder` 和 GSM8K，每个 prompt 采样 G=4，报告平均奖励和 `frac_reward_zero_std`——也就是 run 1 结束时为 82% 的那个值。这才是判断是否有梯度可用的真正 go/no-go 标准。

要我把这两个跑一下吗？另外注意 T=1.0 探针大约需要 5–10 分钟的 GPU，所以如果你更希望我控制探针时间，请告诉我。
