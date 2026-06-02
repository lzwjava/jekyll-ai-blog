---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT-2 XL 训练存储需求
translated: true
type: note
---

**问题：** 从头训练 GPT-2 XL，需要多大存储空间来存放所有内容——原始文本数据、分词后的数据以及所有检查点？

**回答：**

## 首先了解 GPT-2 XL 模型大小

```
GPT-2 XL: 1.5B 参数
float32:  1.5B × 4 字节 = 每份检查点 6GB
float16:  1.5B × 2 字节 = 每份检查点 3GB
bfloat16: 1.5B × 2 字节 = 每份检查点 3GB
```

加上优化器状态（AdamW 存储两个动量项）：
```
float32 模型 + AdamW:
  params:          6GB
  grad:            6GB
  动量 (m):        6GB
  方差 (v):        6GB
  总计:          每份训练检查点约 24GB
```

## 完整细分

| 项目 | 大小 | 说明 |
|------|------|------|
| 原始文本（WebText 规模） | 40GB | OpenWebText 压缩后约 40GB |
| 分词后的 `.bin` 文件 | 40GB | 经 GPT-2 BPE 处理后大小大致相同 |
| 模型检查点（fp32+AdamW） | 24GB | 完整训练状态 |
| 保留最近 3 份检查点 | 72GB | 安全回滚 |
| 最佳检查点（仅推理） | 3GB | 仅 fp16 权重 |
| 日志、TensorBoard、杂项 | 2GB | |
| **总计** | **约 157GB** | |

## 建议

**200GB 卷**——给你约 40GB 的余量。

```
$0.00015/GB/小时 × 200GB = 静止状态下 $0.03/小时
$0.03 × 24 × 30 = 约 $21.60/月
```

相比于在每小时 $2 的 GPU 训练过程中磁盘写满，这点成本很划算。

## 卷上的目录布局

```bash
/mnt/data/
├── raw/
│   └── openwebtext/        # 约 40GB 原始文本
├── tokens/
│   ├── train.bin           # 约 40GB 分词后数据
│   └── val.bin
├── checkpoints/
│   ├── ckpt_step_10000.pt  # 每个约 24GB
│   ├── ckpt_step_20000.pt
│   └── ckpt_best.pt        # 约 3GB fp16
└── logs/
    └── tensorboard/
```

## 实际 nanoGPT 配置示例

```python
# 在 train.py / config 中设置
out_dir = '/mnt/data/checkpoints'
dataset = '/mnt/data/tokens'

# 每 N 步保存一次，保留最近 3 份
save_interval = 1000
keep_last_n = 3
```

## 总结

选择 **200GB** → 静止状态下每小时成本 **$0.03**，空闲时每月约 $21。相比之下，训练到第 50,000 步时因磁盘满而中断，完全不值得。
