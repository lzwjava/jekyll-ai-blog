---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 极简nanoGPT风格项目
translated: true
type: note
---

已完成。在 `/mnt/data/igpt` 中创建了一个 nanoGPT 风格的项目：

| 文件 | 用途 |
|------|------|
| `train.py` | 整个项目整合在一个文件中（750 行） |
| `README.md` | 安装、快速开始、工作原理、参数说明、扩展方案 |
| `.gitignore` | Python + `data/`、`out/`、检查点、编辑器/操作系统文件 |

### `train.py` 包含的内容

- **数据准备** — 自动下载 tiny shakespeare（或使用 `--dataset path/to.txt`），一次性 tokenize 后缓存为 `train.bin`/`val.bin`（uint16）和 `meta.pkl`
- **分词器** — `CharTokenizer`（自包含，约 65 词表）和 `BPETokenizer`（通过 `tiktoken` 实现的 GPT-2 BPE），使用相同的 `encode`/`decode` 接口
- **模型** — 仅解码器 GPT：pre-LN 模块、通过 `F.scaled_dot_product_attention(is_causal=True)` 实现因果注意力、GELU MLP、权重共享、GPT-2 初始化（带残差缩放，默认约 10.7M 参数）
- **训练** — AdamW（仅对矩阵参数进行权重衰减）、预热 + 余弦学习率调度、梯度累积、bf16/fp16 AMP（配合 `GradScaler`）、梯度裁剪、最佳验证集检查点保存、断点续训、`torch.compile`、通过 `torchrun` 支持 DDP
- **采样** — `--sample` 加载 `out/ckpt.pt`，无需加载数据集；支持 temperature + top-k

### 端到端验证

- 字符 + BPE 分词器，CPU（fp32）和 CUDA（bf16，融合版 AdamW）
- `--init_from resume`、`--sample`、`--eval_only`、`--help`、分词器往返断言
- 实际收敛运行（CUDA，默认配置，300 次迭代）：**验证损失 4.30 → 1.92**，采样结果：

```
ROMEO:
You before will and is and the a see bood to take
Or them all and bart that us hall but comel.
```

快速开始：
```bash
python train.py
python train.py --sample --prompt "ROMEO:" --num_samples 3
```

这三个文件在 `main` 分支上尚未被跟踪（仓库尚无任何提交）——如果您希望我进行首次提交，请告知。