---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSpec 在单块GPU上运行
translated: true
type: note
---

完成——我已经让 DeepSpec 在你的机器上端到端跑通了。以下是全貌：

## DeepSpec 是什么

一个用于**投机解码**的框架：训练一个小型 *草稿* 模型来提议 token，由大型 *目标* 模型（例如 Qwen3-4B）并行验证——从而实现大幅加速。包含三条管道：数据处理 → 训练 → 评估。

## 硬件现实检查

| 需求 | 当前机器 |
| --- | --- |
| 默认配置假设 **8 个 GPU** | 1× RTX 4070 (12GB) |
| 真实配置的目标缓存 | ~38 TB (!) |
| 你的机器 | 1 个 GPU，12GB，桌面应用占用约 3GB |

因此，论文中的完整配置在此不可行。但有一个**玩具设置**（来自之前会话已存在）可以运行相同的代码路径：114 个样本的小型数据集，Qwen3-4B-FP8 目标缓存（477MB），2 个草稿层，7-token 块。我完整运行了它：

## 我运行了什么（全部成功 ✅）

**1. 训练**（约 20 秒）：

```bash
cd /mnt/data/DeepSpec
CUDA_VISIBLE_DEVICES=0 /usr/bin/python3.12 train.py \
  --config config/dspark/dspark_qwen3_4b_fp8_toy.py \
  --opts "data.target_cache_path=${HOME}/.cache/deepspec/qwen3_4b_fp8_toy_cache"
```

损失从 3.34 降到 2.66，检查点已保存到 `~/checkpoints/deepspec/dspark_block7_qwen3_4b_fp8_toy/`。

**2. 评估**（投机解码演示，`toy_run/eval_smoke.py` — 3 个 gsm8k 样本，128 个 token）：

```
|  gsm8k  | Qwen3-4B-FP8 | step_latest | 7.00+1 | accept_len 1.00 | verify_rate 0.1253 | accept_rate@0 0.0026 |
```

草稿模型提议 7-token 块，目标模型验证它们，并测量接受率。数字较低是因为这是一个 100 样本/2 epoch 的冒烟模型——真正的检查点每个块接受 2-4 个 token。机制工作正常：提议 → 验证 → 拒绝采样 → 提交。

## 我发现并修复的两个错误

1. **NaN 错误**（真实代码 bug）：`build_draft_config` 深度复制了目标配置，"包括" Qwen3-4B-FP8 的 `quantization_config`，导致 transformers 在评估时构建 FP8 线性层，期望得到 bf16 检查点不包含的 `weight_scale_inv` 权重 → NaN logits → 崩溃。修复方法：在 `deepspec/modeling/dspark/{qwen3,eagle3/qwen3}/config.py` 中剥离 `quantization_config`。
2. **缺少依赖**：`prettytable` 未路径 → 通过 `pip install --break-system-packages prettytable` 安装。

## 真实场景的说明

- 要获得实际结果，请在 8-GPU 节点上运行 `bash scripts/train/train.sh` 和 `bash scripts/eval/eval.sh`，使用 `config/*.py` 配置（真实配置指向 `Qwen/Qwen3-4B` 和 38TB 缓存）。
- README 中列出了已发布的检查点（例如 `deepseek-ai/dspark_qwen3_4b_block7`）—— 这些可直接通过 `--draft_name_or_path` 加载。
- 旧的损坏检查点保留在 `~/checkpoints/deepspec/dspark_block7_qwen3_4b_fp8_toy.bak` 中（如需使用）；`toy_run/eval_smoke.py` 可复用（尝试 `--dataset math500 --num-samples 5`）。

需要我尝试其他内容吗？例如运行更大的评估集，或者一旦你有更多 VRAM 就连接真实发布的 DSpark 检查点？
