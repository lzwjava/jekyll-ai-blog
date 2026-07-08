---
audio: false
generated: true
image: false
lang: zh
layout: post
title: BPE训练日志与合并算法
translated: true
type: note
---

问题：这个nanochat rustbpe训练日志中发生了什么，底层的BPE合并算法是如何工作的？

答案：

## 日志展示的内容

这是`rustbpe`——nanochat基于Rust的自定义BPE训练器（之所以不用Python的`tiktoken`/`sentencepiece`训练，是因为对数十亿字节对进行原始计数和合并是一个热循环，Python无法高效处理）。每一行代表一个**合并步骤**：

```
Progress: 97% (31528/32503 merges) - Last merge: (12696, 9604) -> 31783 (frequency: 1090)
```

- `12696, 9604` 是被合并为一个新令牌`31783`的令牌ID
- `frequency: 1090` 表示在当前阶段，该相邻对在训练语料中出现的次数
- 总目标合并次数为`32503`，意味着最终词汇大小 = `256（字节级基础令牌）+ 32503次合并 + 特殊令牌`——这接近nanochat配置的词汇大小（可以查看你的`tokenizer_train.py`中的`--vocab_size`参数，因为如果你得到32503次合并，说明它不是默认的65536）

频率单调递减（1109 → 1090 → 1070 → 1051 → 1033）是BPE的典型特征：早期的合并消耗了非常常见的对（空格+单词、常见双字母组合），随着训练的进行，剩余未合并的对变得越来越稀有。

## 核心算法（rustbpe在底层执行的操作）

BPE训练过程如下：

1. 从基础词汇（256个字节值）开始（nanochat处理原始UTF-8字节，而非预分词单词——因此没有Unicode标准化的意外问题）
2. 统计整个语料库中所有相邻对的频率
3. 将出现频率最高的单个对合并为一个新令牌
4. 重复上述步骤，直到达到`词汇大小 - 256 - 特殊令牌数量`次合并

最小化的Python参考实现（显然这不是rustbpe实际运行的方式——这是每次合并的O(n)重新扫描，因此Karpathy用Rust重写了它，采用优先队列和增量计数更新）：

```python
from collections import Counter

def get_pair_counts(ids):
    counts = Counter()
    for chunk in ids:  # ids：令牌ID序列（文档）的列表
        for a, b in zip(chunk, chunk[1:]):
            counts[(a, b)] += 1
    return counts

def merge(ids, pair, new_id):
    out = []
    for chunk in ids:
        merged = []
        i = 0
        while i < len(chunk):
            if i < len(chunk) - 1 and (chunk[i], chunk[i+1]) == pair:
                merged.append(new_id)
                i += 2
            else:
                merged.append(chunk[i])
                i += 1
        out.append(merged)
    return out

def train_bpe(ids, vocab_size, base_vocab=256):
    ids = [list(bytearray(doc, "utf-8")) for doc in ids]  # 从字节级开始
    merges = {}
    next_id = base_vocab
    num_merges = vocab_size - base_vocab
    for i in range(num_merges):
        counts = get_pair_counts(ids)
        if not counts:
            break
        best_pair = max(counts, key=counts.get)
        ids = merge(ids, best_pair, next_id)
        merges[best_pair] = next_id
        print(f"merge {i+1}/{num_merges}: {best_pair} -> {next_id} (freq {counts[best_pair]})")
        next_id += 1
    return merges
```

这正是你看到的日志模式，只是Python速度而非Rust速度。`rustbpe`相比这个朴素版本的真正优势在于：它不需要每次合并都从头计算`get_pair_counts`（这是性能瓶颈——每次合并对整个语料库重新扫描是O(vocab_size × corpus_size)）。相反，它维护一个实时计数结构，并且只更新每次合并发生的*局部邻域*内的计数，同时使用最大堆实现O(log n)的最佳对查找，而非O(n)线性扫描。这就是"32503次合并耗时161.78秒"与在纯Python中对非平凡语料库处理数小时之间的区别。

## 这对你的MoE/nanochat工作的重要性

鉴于你专注于DeepSeek v4方向，在你的运行中有两件事值得检查：

- **词汇大小与MoE路由**：更大的词汇大小意味着更大的嵌入层和语言模型头矩阵，这对MoE模型影响更大，因为你已经在专家上投入了大量参数预算。DeepSeek v2/v3使用约10万-12.8万词汇（字节级BBPE）——如果你正在实验接近v4规模的方向，你的分词器词汇选择直接影响嵌入表大小，进而影响MI300X运行中的HBM占用。
- **字节级回退**：由于rustbpe（像GPT-2/nanochat一样）从原始字节开始，你可以保证无OOV令牌行为——值得确认你的合并列表没有在来自噪声语料数据的稀有字节序列上浪费槽位（检查你合并日志的尾部——在大语料库上频率接近1000的合并处于临界点；你可以更早停止，并将这些额外槽位用于更多的特殊/保留令牌，用于智能体/工具使用控制令牌，如果你正在走向智能体架构，这很重要）。

如果你愿意，可以贴出你实际的`tokenizer_train.py`参数（词汇大小、语料库大小），我可以帮你调整合并截止点与为结构化控制令牌（工具调用开始/结束、思考标签等）预留槽位之间的平衡——如果你正在构建面向智能体原生的预训练，而不仅仅是复制标准的nanochat，这一点很相关。