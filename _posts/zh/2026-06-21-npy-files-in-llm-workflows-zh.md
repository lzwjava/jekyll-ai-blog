---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM工作流中的NPY文件
translated: true
type: note
---

**问题：** 什么是 `.npy` 文件，它们在 LLM 工作流中如何使用？

**回答：**

`.npy` 是 NumPy 的原生二进制序列化格式。它以紧凑、可内存映射的文件存储单个 ndarray——包括 dtype、shape 和原始数据。

**格式内部结构：**

```
magic: \x93NUMPY          (6 字节)
version: 1.0 或 2.0      (2 字节)
header_len                (2 或 4 字节)
header: 包含 shape、dtype、fortran_order 的字典 (ASCII)
data: 原始 C 连续字节
```

无压缩，无额外开销。加载本质上就是一个 `mmap` 调用。

---

**它们在 LLM 流水线中的出现位置：**

**1. 分词后的数据集存储（最常见）**

对原始文本运行分词器后，将 token ID 以 `uint16` 或 `uint32` 数组的形式转储：

```python
import numpy as np

# nanoGPT 风格 — train.bin / val.bin 实际上是原始的 uint16
ids = np.array(tokenized_ids, dtype=np.uint16)
ids.tofile("train.bin")  # 原始二进制，不是 .npy，但思路相同

# .npy 版本保留 shape/dtype 元数据
np.save("train.npy", ids)
```

nanoGPT 使用 `.bin`（更原始），但许多流水线出于相同目的使用 `.npy`。Fineweb、RedPajama 的预处理脚本将分片保存为 `.npy`。

**2. 内存映射的训练数据**

杀手级特性：`np.load(..., mmap_mode='r')` 允许你索引一个 200GB 的数据集，而无需将其全部加载到 RAM 中：

```python
data = np.load("train.npy", mmap_mode='r')
batch = data[offset : offset + block_size]  # 操作系统仅按需分页加载
```

这就是你在 RTX 4070 / MI300X 上训练比 RAM 还大的数据集的方法。

**3. 嵌入缓存**

预先计算的嵌入保存下来供检索或微调使用：

```python
np.save("embeddings.npy", model.encode(texts))  # shape: (N, D)
# 之后：
embs = np.load("embeddings.npy")
```

**4. 检查点分片（现在不太常见）**

在 safetensors 成为标准之前，人们将权重张量保存为 `.npy` 或 `.npz`（压缩的多数组文件）。在较旧的 Hugging Face 代码中仍能看到。

**5. 用于可解释性的激活 / 注意力转储**

```python
# 钩入某一层，保存激活值用于分析
np.save(f"layer_{i}_attn.npy", attn_weights.cpu().numpy())
```

---

**`.npy` 与其他格式的对比：**

| 格式 | 用途 | 备注 |
|------|------|------|
| `.npy` | 单个数组 | 快速，可内存映射 |
| `.npz` | 多个数组 | 压缩，较慢 |
| `.bin` | 原始字节 | nanoGPT 风格，无元数据 |
| `.safetensors` | 模型权重 | 安全、快速，目前更受青睐 |
| `.pt` / `.ckpt` | PyTorch 张量 | 基于 pickle，安全性较低 |
| Arrow / Parquet | 结构化数据集 | Hugging Face Datasets 默认格式 |

---

**具体到你的 nanoGPT 场景：**

nanoGPT 中的 `prepare.py` 执行：

```python
train_ids = np.array(enc.encode_ordinary(train_data), dtype=np.uint16)
train_ids.tofile(os.path.join(os.path.dirname(__file__), 'train.bin'))
```

这里使用的是原始的 `.bin`，但模式与 `.npy` 相同——由 dtype 同构的 token ID 组成的扁平数组，在训练期间通过以下方式内存映射：

```python
data = np.memmap('train.bin', dtype=np.uint16, mode='r')
```

原理相同，只是跳过了 NumPy 的头部。`.npy` 增加了约 128 字节的头部，以换取自描述的元数据。