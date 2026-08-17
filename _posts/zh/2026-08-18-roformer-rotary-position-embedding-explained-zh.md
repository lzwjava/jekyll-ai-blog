---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'RoFormer: 旋转位置编码详解'
translated: true
type: note
---

## 问题：解释 arXiv:2104.09864v5 — **RoFormer：增强型Transformer与旋转位置编码（RoPE）**

答案：

这篇论文介绍了**RoPE（旋转位置编码）**，这是许多现代大语言模型使用的位置编码方法：

* LLaMA / LLaMA 2 / LLaMA 3
* Qwen
* Mistral
* DeepSeek
* GPT-NeoX 风格模型

核心思想：

> 不将位置嵌入添加到词元嵌入中，而是根据词元的位置旋转 Query 和 Key 向量，使注意力机制自然学习到相对位置。

论文：（[Star Oceans][1]）

---

# 1. 为什么Transformer需要位置信息？

自注意力本身没有顺序概念。

示例：

```
"The cat eats fish"
"The fish eats cat"
```

词元集合相同：

```
cat
eats
fish
```

注意力只看到向量：

\[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt d})V
\]

没有“词元1”、“词元2”的概念。

因此我们需要位置信息。

---

# 2. 原始Transformer位置嵌入

原始Transformer将位置向量相加：

\[
x_i = token_i + position_i
\]

示例：

```
词元嵌入：

cat  ---> [0.2,0.5,0.1...]

位置：

pos=3 ---> [0.01,0.03,0.02...]

相加：

[0.21,0.53,0.12]
```

这是可行的。

但存在问题：

1. 位置与内容混合在一起。

2. 最大长度固定。

例如：

训练时：

```
上下文长度 = 2048
```

模型学习：

```
位置 0 ... 2047
```

推理时：

```
位置 4096
```

没有学习到的嵌入。

---

# 3. 相对位置思想

人类关心相对距离。

示例：

```
The cat sat on the mat
        ^
        |
        当前词元
```

关系：

```
cat -> sat

距离 = +1
```

比以下更重要：

```
cat 位置 = 2
```

因此我们希望注意力知道：

\[
relative\ distance = m-n
\]

其中：

* m = query 位置
* n = key 位置

---

# 4. RoPE 核心思想

RoPE 指出：

不要添加位置。

旋转向量。

之前：

```
Q
|
|
注意力
|
K
```

应用 RoPE 后：

```
Q ---> 旋转(位置 m) ---> Q'

K ---> 旋转(位置 n) ---> K'

注意力：

Q'K'^T
```

神奇性质：

\[
(R_m q)^T(R_n k)
\]

变为：

\[
q^T R_{n-m} k
\]

含义：

点积仅依赖于：

\[
n-m
\]

即相对距离。

这就是整篇论文的核心。

---

# 5. 直观理解：二维旋转

想象一个向量：

```
        y
        |
        |
        *
       /
      /
-----*---------- x
```

旋转它：

位置 0：

```
角度 = 0°
```

位置 1：

```
角度 = θ
```

位置 2：

```
角度 = 2θ
```

位置 n：

```
角度 = nθ
```

因此位置变成了角度。

---

数学上：

二维旋转：

\[
R(\theta)=
\begin{bmatrix}
cos\theta & -sin\theta\\
sin\theta & cos\theta
\end{bmatrix}
\]

对于位置 m 的词元：

\[
q_m=R(m\theta)q
\]

对于位置 n 的词元：

\[
k_n=R(n\theta)k
\]

注意力：

\[
q_m^Tk_n
\]

变为：

\[
q^TR((n-m)\theta)k
\]

绝对位置消失。

只保留距离。

---

# 6. 扩展到高维

LLM 隐藏层大小：

```
4096
```

不是 2。

RoPE 将维度成对拆分：

示例：

```
隐藏向量：

[x0,x1,x2,x3,x4,x5,...]

成对：

(x0,x1)
(x2,x3)
(x4,x5)
...
```

每对以不同频率旋转。

类似于：

```
维度对 0：

快速旋转

维度对 1：

较慢旋转

维度对 2：

更慢
```

频率：

\[
\theta_i=10000^{-2i/d}
\]

因此：

低维度：

```
高频
（短距离模式）
```

高维度：

```
低频
（长距离模式）
```

类似于傅里叶特征。

---

# 7. PyTorch 实现

简化的 RoPE：

```python
import torch

def rotate_half(x):
    x1 = x[..., :x.shape[-1]//2]
    x2 = x[..., x.shape[-1]//2:]

    return torch.cat(
        (-x2, x1),
        dim=-1
    )


def apply_rope(x, cos, sin):
    return (
        x * cos +
        rotate_half(x) * sin
    )
```

在注意力计算中：

```python
q = apply_rope(q, cos, sin)
k = apply_rope(k, cos, sin)

attn = q @ k.transpose(-2,-1)
```

这基本上就是 LLaMA 的做法。

---

# 8. 为什么 RoPE 对 LLM 效果好

## 性质 1：相对距离

注意力自然知道：

```
词元 A 距离 3 个位置
```

而不是：

```
词元 A 在位置 3812
```

---

## 性质 2：无需学习位置表

旧方法：

```
nn.Embedding(max_position, dim)

2048 个位置
```

RoPE：

```
计算 sin/cos
```

可以扩展长度。

---

## 性质 3：长距离衰减

论文显示：

随着距离增加：

```
注意力分数降低
```

这与语言规律一致。

相邻词：

```
"The cat sat"
       ^
       重要
```

远距离词：

```
"The cat sat ................. yesterday"
```

关联较弱。

---

# 9. 为什么现代 LLM 修改 RoPE

原始 RoPE：

```
上下文 2k
```

现代模型：

```
32k
128k
1M
```

问题出现：

高位位置旋转过多。

示例：

```
位置 0

角度 = 0


位置 100000

角度 = 很大
```

解决方案：

## NTK 缩放

被许多模型使用。

思路：

改变频率：

\[
\theta_i
\]

使得相同旋转覆盖更长上下文。

---

## YaRN

改进了长上下文外推。

---

## LongRoPE

将 RoPE 扩展到数百万词元。

---

# 10. 与傅里叶变换的联系

一个有用的思维模型：

RoPE 是一种对学习友好的傅里叶特征。

傅里叶：

```
信号
 |
不同频率
 |
编码位置
```

RoPE：

```
词元向量
 |
以频率旋转
 |
编码位置
```

不同维度表示不同的“位置时钟”。

---

# 11. 为什么这篇论文变得极其重要

论文本身是关于 RoFormer 的，但更大的影响是：

```
RoPE
 |
 +--> LLaMA
 |
 +--> Qwen
 |
 +--> Mistral
 |
 +--> DeepSeek
 |
 +--> 今天几乎所有的开源 LLM
```

它成为 decoder-only LLM 的默认位置编码。（[Science Stack][2]）

---

一个便于记忆的方式：

```
绝对位置编码：
    词元 + 位置

相对位置编码：
    显式计算距离

RoPE：
    旋转 Q, K
    点积自动变为相对距离
```

数学技巧是：

\[
\boxed{
(R_m q)^T(R_n k)=q^TR_{n-m}k
}
\]

这一个等式就是 RoPE 主导现代 LLM 架构的原因。（[Science Stack][3]）

参考文献：

* RoFormer: Enhanced Transformer with Rotary Position Embedding ([Star Oceans][1])
* RoFormer 总结与性质 ([Science Stack][2])

[1]: https://staroceans.org.s3.amazonaws.com/stable-diffusion/2104.09864v5.pdf?utm_source=chatgpt.com "ROFORMER: ENHANCED TRANSFORMER WITH ROTARY"
[2]: https://www.sciencestack.ai/paper/2104.09864v5?utm_source=chatgpt.com "RoFormer: Enhanced Transformer with Rotary Position Embedding (arXiv:2104.09864v5) - ScienceStack"
[3]: https://www.sciencestack.ai/paper/2104.09864?utm_source=chatgpt.com "RoFormer: Enhanced Transformer with Rotary Position Embedding (arXiv:2104.09864v5) - ScienceStack"
