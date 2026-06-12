---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Unsloth的双语SFT
translated: true
type: note
---

完成。以下是 `/mnt/data/zz/finetune/` 中的内容：

```
finetune/
├── README.md              # 完整使用指南
├── requirements.txt       # pip 依赖
├── build_dataset.py       # 提取中英文帖子 → JSONL
├── train.py               # 使用 Unsloth 进行 QLoRA SFT
├── eval.py                # 对比微调后与基础模型
├── export_gguf.py         # 导出 GGUF 供 ollama 使用
├── notes_sft.jsonl        # 21,434 条样本 (86MB)
├── notes_sft_train.jsonl  # 21,234 条训练样本 (85MB)
└── notes_sft_eval.jsonl   # 200 条评估样本 (820KB)
```

数据集统计：
- 10,726 条英文 + 10,708 条中文 = 共 21,434 条
- 2510 万 token，平均每样本 1169 token
- 跳过 30 条帖子（过短，少于 100 字符）
- 200 条留作评估，其余用于训练

在 RTX 4070 上训练：

```bash
cd /mnt/data/zz/finetune
pip install unsloth          # 或者: pip install -r requirements.txt
python train.py              # Qwen3-8B QLoRA 4-bit，约 2-4 小时
python train.py --model unsloth/Qwen3-4B   # 更小、更快
```