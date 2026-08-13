---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RNN被发明的原因
translated: true
type: note
---

问题：为什么发明了RNN？

答案：

前馈网络（MLP、早期CNN）具有固定大小的输入且没有记忆能力。这带来了两个问题：

**1. 变长序列无法适配固定输入向量。**  
句子、时间序列、音频波形——长度任意。若填充/截断到固定窗口，要么浪费容量，要么丢失上下文。RNN每次处理一个token并向前传递状态，因此架构本身不关心序列长度。

**2. 位置间无参数共享 = 无法随时间泛化。**  
若将固定窗口输入MLP，位置1和位置50的权重不同。网络无法识别"我在t=3看到的模式"在t=47再次出现——必须重新学习。RNN在每个时间步重用*相同*的权重矩阵：

```
h_t = tanh(W_xh @ x_t + W_hh @ h_{t-1} + b_h)
y_t = W_hy @ h_t + b_y
```

每个步骤使用相同的`W_xh`、`W_hh`、`W_hy`。这才是真正的发明——不是"带循环的网络"，而是**随时间权重共享 + 隐藏状态作为已见内容的压缩记忆**。`h_t`是`x_1...x_t`的有损摘要。

最小的前向传播实现，使用numpy，无需框架：

```python
import numpy as np

def rnn_forward(xs, h0, Wxh, Whh, Why, bh, by):
    h = h0
    hs, ys = [], []
    for x in xs:                          # x: (input_dim,)
        h = np.tanh(Wxh @ x + Whh @ h + bh)
        y = Why @ h + by
        hs.append(h); ys.append(y)
    return hs, ys

# 玩具维度
in_dim, hid_dim, out_dim = 4, 8, 2
Wxh = np.random.randn(hid_dim, in_dim) * 0.1
Whh = np.random.randn(hid_dim, hid_dim) * 0.1
Why = np.random.randn(out_dim, hid_dim) * 0.1
bh, by = np.zeros(hid_dim), np.zeros(out_dim)

xs = [np.random.randn(in_dim) for _ in range(10)]  # 序列长度 10
h0 = np.zeros(hid_dim)
hs, ys = rnn_forward(xs, h0, Wxh, Whh, Why, bh, by)
print(len(hs), hs[0].shape)  # 10 (8,) — 相同权重，任意序列长度
```

历史背景：Hopfield（1982）展示了循环动力学可以存储记忆/吸引子。Elman（1990）和Jordan（1986）专门针对语言/序列任务提出了简单RNN，因为MLP在处理任何具有时间结构的内容时都失败——Elman的"Finding Structure in Time"是经典的动机论文：语言、运动控制、时间序列都具有顺序依赖性，MLP无法在不导致输入大小组合爆炸的情况下捕捉这种依赖。

RNN随后遇到的问题是：通过`Whh`在长序列上产生梯度消失/爆炸（通过时间反向传播重复乘以相同矩阵），因此LSTM（1997）添加了门控机制来控制`h_t`中哪些信息被保留或遗忘，而Transformer最终通过并行注意力完全取代了RNN，放弃了序列递归。

参考文献：

- [Elman, "Finding Structure in Time" (1990)](https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog1402_1)
- [Karpathy, "The Unreasonable Effectiveness of RNNs"](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)
- [Hochreiter & Schmidhuber, LSTM (1997)](https://www.bioinf.jku.at/publications/older/2604.pdf)
