---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 欠训练模型退化吸引子
translated: true
type: note
---

问题：为什么我的 GPT-2 / nanoGPT 模型在使用 GitHub 代码（HuggingFace 的 BigCode/The Stack）训练时，会退化为重复的 `.S.S.S.S` 循环？

回答：

这个 `.S.S.S.S` 循环并非代码数据的问题。它是**训练不足的模型**在采样温度下落入退化吸引子的典型特征。让我解析一下实际机制，因为这个症状具有诊断意义。

## 从机制上看你看到的现象

你的提示回放很干净（第 1–48 行），因为这只是模型复制上下文中的内容——通过归纳头复制电路，对提示的注意力非常简单，即使在接近随机的模型中也有效。当它必须*生成*时，它就崩溃了。这种差距——干净复制、垃圾生成——告诉你模型学会了**局部 n-gram / 复制统计，但没有学会代码的实际分布**。

具体到 `.S`：`S` 很可能是你词表中一个高频 BPE 标记（想想 `System`、`String`，Java 中到处都是 `.S` 前缀的合并——你的提示中*充满*了 `System.out.println`）。模型发现 `.` → `S` → `.` → `S` 是一个高概率的局部转移，而在没有学到其他东西的情况下，采样就落入了这个 2-循环。一旦进入，每一步都会强化它。这是一个**重复陷阱**：分布的近似 argmax 区域是一个短循环，而 `top_k=200, temp=0.8` 不足以提供逃脱的熵，因为循环标记占据了概率质量的绝大部分。

## 真正原因：就是训练不足，没有其他

一个从头训练的 GPT-2 760M 需要大约 **Chinchilla 最优的 ~20 tokens/param ≈ 至少 150 亿 token** 才能产生连贯的文本，对于代码来说实际还需要更多。如果你训练的数据远少于这个量（几亿 token，几千次迭代），这个输出*完全*符合预期。nanoGPT 自身的 GPT-2 复现实验在 8×A100 上花费许多小时，在 OpenWebText 上训练了约 3000 亿 token。在单个 MI300X 上你也可以做到，但你需要足够的 token 预算。

快速自查清单——在假设任何特殊情况之前先运行这些：

```python
# 1. 你的实际损失是多少？代码应该达到训练损失约 1.0-1.5 才能连贯。
#    如果损失在 3.0 以上，模型基本上还没学会语言。

# 2. 你实际看到了多少 token？
tokens_seen = iter_num * batch_size * block_size * grad_accum_steps
print(f"tokens seen: {tokens_seen/1e9:.2f}B")  # 对于 760M 模型，需要 >>1B

# 3. 你的数据是否使用了代码分词器进行分词？
#    用 GPT-2 BPE 处理代码效率很低——缩进/空白会暴增 token 数量。
#    改用 StarCoder/BigCode 分词器。
```

## 具体的修复方案，按优先级排序

**1. 首先检查损失。** 如果训练损失没有降到约 2.0 以下，下游的一切都无关紧要。给出你的损失曲线。损失平坦或过高 = 有 bug（学习率过高/过低、数据未打乱、掩码错误）或者只是步骤不够。

**2. 使用 BigCode/StarCoder 分词器，而不是 GPT-2 BPE。** GPT-2 的词表是基于网络文本构建的，对代码进行分词时效果很差——每一级缩进都会消耗 token，标识符也会碎片化。这不仅浪费了你的 token 预算，还会产生那种病态的高频片段（如 `.S`），从而困住采样。

```python
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("bigcode/starcoder2-15b")  # 49k 词表，代码感知
# tok.encode("System.out.println") → 更少、更具语义的 token
# 使用这个分词器重新对 The Stack 进行分词，重建你的 .bin 分片。
```

**3. 在推理时添加重复惩罚** 以确认诊断（这是权宜之计，并非修复）：

```python
def sample_with_rep_penalty(logits, generated_ids, penalty=1.3):
    # 将已生成 token 的 logit 除以惩罚项（CTRL 论文，Keskar 2019）
    for tid in set(generated_ids):
        logits[tid] /= penalty if logits[tid] > 0 else penalty
    return logits
```

如果重复惩罚让输出*看起来*更好，但语义上仍然是垃圾，那就证实了训练不足——你只是压制了症状。治疗方法是更多 token，而不是惩罚。

**4. 降低温度在这里没有帮助**——反直觉的是。退化循环*就是*高概率区域，所以降低温度会使其*更*确定地进入循环。提高温度会增加噪声，但会牺牲连贯性。两者都无法修复训练不足的模型。不要通过调整采样参数来逃避训练问题。

## 关于使用 The Stack 进行训练

在使用 BigCode/The Stack 时，有几个常见陷阱：

- **去重至关重要。** 使用 `the-stack-dedup`，而不是原始版本。近似重复的代码（fork、vendor 依赖、自动生成的文件）会以低信息量的重复膨胀 token 计数，并*鼓励*你看到的复制循环行为。
- **根据星级/质量过滤。** The Stack 包含大量低质量和自动生成的代码。先在上训练 `bigcode/the-stack-smol` 或经过星级筛选的子集，可以获得更干净的信号。
- **文档打包 + 正确的注意力重置。** 如果你将多个文件打包到一个 block_size 序列中，而没有在文档边界处重置注意力，模型会学习在不同文件之间混叠上下文——这会降低生成质量。

## 我对你情况的判断

鉴于你在 MI300X（192GB——你有足够的内存余量来大幅提高 batch size）上运行 GPT-2 760M，瓶颈几乎肯定是**token 预算和/或分词器**，而不是架构。输出不是“权重损坏”——而是模型只看到了所需 token 的 1–5%。设定一个目标，至少使用 StarCoder 分词器训练 100–150 亿代码 token，观察损失降至 1.5 以下，`.S.S.S` 循环会自行消失。

你目前的迭代次数、batch×block×grad_accum 和训练损失是多少？有了这三个数字，我可以精确告诉你训练不足的程度，以及需要多少 MI300X 小时才能达到连贯性。

参考资料：

- [nanoGPT — Karpathy](https://github.com/karpathy/nanoGPT)
- [The Stack / BigCode 数据集](https://huggingface.co/datasets/bigcode/the-stack-dedup)
- [StarCoder2 分词器](https://huggingface.co/bigcode/starcoder2-15b)
- [CTRL: 重复惩罚 (Keskar et al., 2019)](https://arxiv.org/abs/1909.05858)
- [训练计算最优的 LLM (Chinchilla, Hoffmann et al., 2022)](https://arxiv.org/abs/2203.15556)