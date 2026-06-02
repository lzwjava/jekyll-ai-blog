---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解数据集变化与分词
translated: true
type: note
---

你说得对——它们**不是**重复的。以下是各自的具体情况：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  /root/zz/datasets/fineweb-edu/     (40 GB)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  14 个 parquet 文件（每个 2.2-2.3 GB）
  来自 HuggingFace FineWeb-Edu 的原始文本
  人类可读，可重新处理
  来源：https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  /root/nanoGPT/data/fineweb/edu_fineweb100B/  (28 GB)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  147 个 .npy 文件（每个 191 MB）
  使用 GPT-2 BPE 分词器进行分词处理
  机器可读的 token ID numpy 数组
  可直接用于训练——这是 train.py 读取的内容

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

为什么分词后体积更小：

- 分词会压缩文本（常见单词 → 单个 token ID）
- 没有元数据开销（仅 uint16 数组）
- Parquet 包含行组、列元数据、压缩字典

两者是互补的，并非重复：

- **Parquet** = 数据源，人类可读，可重新处理
- **NPY** = 训练就绪，支持 DataLoader 快速随机访问

**可以删除 parquet 吗？** 可以，前提是：

- 你不打算使用其他分词器重新分词
- 不需要更改预处理（分块大小、过滤）
- NPY 文件已就绪（是的，你已有 147 个文件，28 GB）

```bash
# 释放 40 GB 空间——如果不再重新分词则安全
rm -rf /root/zz/datasets/fineweb-edu
```

但如果你之后想切换到 nanochat（它使用自己的分词器/预处理），就需要重新下载 parquet 文件。这取决于你自己决定。
