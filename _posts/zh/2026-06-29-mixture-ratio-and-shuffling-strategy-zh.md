---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 混合比例与洗牌策略
translated: true
type: note
---

Question: 训练 nanoGPT（或类似模型）时，如果使用 50% FineWeb / 50% GitHub 代码的混合数据，每个批次是否应该一半是代码一半是自然语言，并且训练数据是否应该被打乱？

Answer:

简短回答：你希望**混合比例在期望上成立**，而不是每个批次精确相等。并且是的，要打乱——但**打乱的方式**比“是否打乱”本身更重要。

## 不需要每个批次恰好一半一半

强制每个批次精确为 50% 代码 / 50% 文本属于**分层抽样**。这并非错误，但通常没必要且增加复杂性。对于一个 1024 序列的批次，从 50/50 的池中随机抽样自然会产生每批次约 512±16 个代码序列（二项式标准差 ≈ √(1024·0.5·0.5) ≈ 16）。梯度在几步之内就能看到正确的比例。这种方差是 SGD 可以很好吸收的噪声。

当每批次平衡**确实**重要时：

- **极小的批次**（例如 8–16 个序列），此时二项式方差相对于批次大小较大。
- **领域条件损失 / 每个领域指标**，你希望每一步都稳定。
- **课程学习或损失加权**方案，对不同领域区别对待。

对于标准预训练，期望混合是常规做法。这正是大型实验的做法——为每个数据源设置采样权重并随机抽取。

## 真正的问题：token 比例 vs 文档比例

“50/50”是模糊的。你是指 50% 的**文档**，还是 50% 的 **token**？这两者差异很大，因为代码和散文的 token 化方式不同（代码有更多空白、更短的行、更多标点）。你几乎总是想要 **50% 的 token**，因为模型从 token 学习，而不是文档。先计算每个语料库的 token 数量，然后设置采样权重以达到你想要的 token 比例。

## 打乱：nanoGPT 的现实

nanoGPT 在训练时并不打乱文档列表。它预先将所有内容 token 化成一个巨大的扁平 `train.bin`（一个 `uint16` 的 memmap），然后随机采样偏移量：

```python
# nanoGPT 数据加载的实际机制
data = np.memmap('train.bin', dtype=np.uint16, mode='r')

def get_batch():
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([torch.from_numpy(data[i:i+block_size].astype(np.int64)) for i in ix])
    y = torch.stack([torch.from_numpy(data[i+1:i+1+block_size].astype(np.int64)) for i in ix])
    return x, y
```

因此“打乱”实际上是**随机偏移采样**，而不是列表排列。关键后果：**.bin 的排列方式决定了你的混合方式。** 如果你先写入所有 FineWeb，再写入所有 GitHub，那么随机偏移仍然会在一个 epoch 内均匀覆盖两个区域——但任何*单个*批次的组成取决于偏移落在哪里，并且跨越边界序列是垃圾数据。

两种清晰的做法：

**方法 A — 写入时交错（单个 .bin）：**
在 token 化之前打乱文档，使代码和文本在扁平缓冲区中交错排列。然后随机偏移采样自然会产生混合批次。

```python
import numpy as np, random

# docs: token 数组列表，每个标记来源
docs = fineweb_docs + github_docs
random.shuffle(docs)  # 在缓冲区中交错排列来源

# 在文档之间用文档分隔符（EOT token）连接
sep = np.array([eot_token], dtype=np.uint16)
buf = np.concatenate([np.concatenate([d, sep]) for d in docs])
buf.tofile('train.bin')
```

**方法 B — 独立的 .bin 文件 + 加权采样（更清晰，易于控制比例）：**
将 `fineweb.bin` 和 `github.bin` 分开，然后按权重选择每个序列的来源。这样将混合比例与磁盘布局解耦，并且可以在不重新 token 化的情况下更改混合比例：

```python
fw = np.memmap('fineweb.bin', dtype=np.uint16, mode='r')
gh = np.memmap('github.bin',  dtype=np.uint16, mode='r')

# token 加权：w = 你希望从每个来源获得的 token 比例
weights = {'fw': 0.5, 'gh': 0.5}

def get_batch(batch_size, block_size):
    xs, ys = [], []
    for _ in range(batch_size):
        src = fw if random.random() < weights['fw'] else gh
        i = random.randint(0, len(src) - block_size - 1)
        xs.append(torch.from_numpy(src[i:i+block_size].astype(np.int64)))
        ys.append(torch.from_numpy(src[i+1:i+1+block_size].astype(np.int64)))
    return torch.stack(xs), torch.stack(ys)
```

我会使用**方法 B**。这是生产环境数据加载器的工作方式（想想 Megatron 的 blended dataset / DataMix），能精确控制比例，并且可以廉价地扫描不同的混合比例。

## 两个人们常犯的错误

1. **文档之间的 EOT 分隔符。** 如果没有在连接的文档之间插入文本结束符，序列会跨越文档边界，模型会学到从 FineWeb 散文到代码文件的虚假延续。始终在文档之间插入 EOT token（对于 GPT-2 BPE 为 `<|endoftext|>` = 50256）。

2. **代码的 tokenizer。** GPT-2 的 BPE 对代码处理不佳（没有良好的空白/缩进处理——空格序列会导致 token 数量激增）。如果代码占数据的 50%，这很重要。考虑使用具有空白合并功能的 tokenizer（通过 tiktoken 使用 GPT-4 的 `cl100k`/`o200k`，或在混合语料上训练自己的 BPE）。这也修正了你的 token 比例计算，因为 FineWeb 散文和代码在每 token 字节数上差异很大。

## 总结

- **按期望混合**，而不是每个批次精确相等——随机抽样处理其余部分。
- 以 **token** 比例为目标，而不是文档比例。
- 在 nanoGPT 中“打乱” = 随机偏移采样；确保你的**布局或加权采样器**提供混合，**独立的 .bin 文件 + 加权抽取**是最清晰的方式。
- 在文档之间插入 **EOT token**，如果代码占数据的一半，请重新考虑 **tokenizer**。

参考文献：

- [nanoGPT — karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
- [tiktoken](https://github.com/openai/tiktoken)
- [Megatron-LM blendable dataset](https://github.com/NVIDIA/Megatron-LM)
