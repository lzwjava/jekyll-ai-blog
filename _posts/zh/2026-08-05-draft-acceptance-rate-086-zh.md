---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 稿件接受率0.86%
translated: true
type: note
---

我仔细查看了评估代码和草稿检查点。以下是完整的情况。

## 如何阅读表格

```
dataset | target_model | draft_model | #propose | accept_len | verify_rate | accept_rate@0 ... @6
gsm8k   | Qwen3-4B-FP8 | step_latest | 7.00+1   | 1.01       | 0.1261      | 0.0086 0.0000 ... 0.0000
```

列（来自 `deepspec/eval/base_evaluator.py` 中的 `build_results_table` + `build_metrics_row`）：

| 列 | 值 | 含义 |
| --- | --- | --- |
| `#propose` | `7.00+1` | 每轮投机采样提出 **7 个草稿 token**（始终是完整块——见下文）+ 1 个锚点 token（`+1` 在格式字符串中是硬编码的） |
| `accept_len` | `1.01` | 每轮平均提交的 token 数 = `avg(accepted_draft_tokens + 1)`。**平均只接受 0.01 个草稿 token**——你总是提交 1 个有保证的目标 token，从未提交草稿的 |
| `verify_rate` | `0.1261` | `accept_len / (propose + 1)` = `1.01/8 ≈ 0.126`——**你计算的 token 位置中只有 12.6% 实际出现在输出中** |
| `accept_rate@k` | `0.0086, 0, 0, …` | 第 k 个草稿 token 被接受的概率。**第一个草稿 token 在 0.86% 的情况下被接受，位置 1–6 从未被接受**。这是确凿的证据 |

所以表格告诉你：**草稿提出 7 个 token，约 99% 的时间被拒绝。**

## 为什么这么慢

1. **~0% 草稿接受率 = 纯开销，无加速。** 每轮仍然运行：
   - 草稿前向（7 个 token 通过 2 层 DSpark 块），然后
   - 目标 **8 个位置的验证前向**通过完整的 Qwen3-4B 目标。

   由于每轮只提交 1.01 个 token，与普通自回归解码相比，每个输出 token 要做 **~8 倍的目标 FLOPs**。在计入任何开销之前，大约比基线慢 8 倍。

2. **草稿是个玩具。** `dspark_block7_qwen3_4b_fp8_toy/step_latest` 是一个 2 层模型（`num_hidden_layers=2`，约 2 GB），根据检查点的 `train_config.py`，在 114 个样本的玩具集（`perfectblend_train.jsonl`）上训练。其分布与 gsm8k/math500/humaneval/mbpp/alpaca 无关，所以它提出的 token 目标几乎永远不会同意。

3. **置信度阈值在这里是无效的。** 玩具配置中 `enable_confidence_head = False` 且 `confidence_head_alpha = 0.0` → `model.confidence_head is None` → `_confident_prefix_length` 始终返回完整块。所以 `--confidence-threshold 0.0` 意味着"始终提出全部 7 个"，保证在糟糕的草稿上浪费验证工作。

4. **工作负载是 5 个数据集 × 100 个样本 × 最多 128 个 token = 500 个样本**，batch-size-1，顺序执行，在单个 RTX 4070（12 GB）上，每轮有 Python/torch 开销：markov-head 采样（对 151,936 词表的 7 个顺序步骤）、每次验证对整个词表的 softmax、gather/cumprod/residual-sampling、KV-cache 裁剪。FP8 目标还带有一些 CPU 端的反量化/内核开销（`kernels-community/finegrained-fp8` v2 vs v4 也打印了一个通知）。

你的运行仍在进行中（PID 49938，约 19 分钟，已完成 2/5 个数据集——与约 9–10 分钟/数据集一致，所以 humaneval+mbpp+alpaca 还需要约 30 分钟）。

## 该怎么做

- 对于真正的冒烟测试，使用脚本文档字符串中预期的大小——终止当前运行并执行：

  ```bash
  CUDA_VISIBLE_DEVICES=0 PYTHONPATH=/mnt/data/DeepSpec /usr/bin/python3.12 toy_run/eval_smoke.py --dataset gsm8k --num-samples 3 --max-new-tokens 128
  ```

- 要真正观察到加速，你需要一个在评估分布上训练的草稿（真正的 DSpark 检查点，而不是玩具），并且最好有一个**基线比较**：对相同样本在相同目标上计时普通自回归采样的 tokens/sec 并进行比较——在 0.86% 的首 token 接受率下，差距会很大（投机采样约慢 8 倍）。
- 如果必须保留这个玩具草稿用于机制测试，缩小提议长度（更小的 `block_size`，例如 2），这样每轮被拒绝的验证工作更少，或者临时修补 `_confident_prefix_length`/提议以提前停止。
- 次要问题：指标行命名（`7.00+1`、`verify_rate`）令人困惑——`verify_rate` 实际上是"保留/计算比率"，而不是速率。

要我终止正在运行的作业并重新运行小型冒烟测试，还是给 `eval_smoke.py` 添加基线（普通解码）比较，让你能定量看到减速因子？
