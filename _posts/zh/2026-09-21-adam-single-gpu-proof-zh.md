---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Adam 单GPU证明
translated: true
type: note
---

完成。我编写了单机版本到 `adam/`，并在你的 RTX 4070 上验证了它可以运行。

## 我创建的内容

| 文件 | 用途 |
| ------ | --------- |
| `adam/train_adam_proof.py` | 单 GPU 实验，比较 Adam 与 SGD/RMSProp/AdaGrad |
| `adam/README.md` | 设置及运行说明 |
| `adam/optimizer_comparison.png` + `results.json` | 2 epoch 冒烟测试的输出 |

## 与分布式版本的主要差异

- 移除了所有 DDP/NCCL 代码——现在是纯单 GPU 脚本
- 在训练损失之外添加了**验证准确率**（更有力的证明）
- 添加了 `--seed` 以保证每个优化器的模型初始化可复现
- 添加了 `--epochs`、`--batch-size`、`--max-train-samples` CLI 参数
- 使 matplotlib 无头安全（`Agg` 后端）

## 环境说明（重要）

你的机器上有**两个 Python**：

- Homebrew Python 3.14（`python3` → `2.10.0+cu128`）
- **系统 Python 3.12**（`/usr/bin/python3.12` → `2.11.0+cu130`，CUDA 可用）

根据你的指示，我使用了系统版本。它已经有 `torch`/`torchvision`；我只安装了 `matplotlib`。

## 运行方法

```bash
cd /mnt/data/zz/adam
/usr/bin/python3.12 train_adam_proof.py            # 完整的 20 epoch 运行
```

## 已可见的验证结果

RTX 4070 上的 2 epoch 冒烟测试已经展示了 Adam 的优势：

| 优化器 | 第 2 轮训练准确率 |
| ----------- | ------------------- |
| **Adam** | **75.2%** |
| SGD+mom | 37.1% |
| RMSProp | 50.2% |
| AdaGrad | 50.2% |

运行完整的 20 个 epoch，可以看到干净的损失曲线（以及 AdaGrad 后期的降速），这与 Adam 论文中的结果相呼应。
