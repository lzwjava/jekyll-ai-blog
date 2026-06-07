---
audio: false
generated: false
image: true
lang: zh
layout: post
title: 神经网络、Transformer与GPT
translated: true
type: post
---

### 目录

1. [AMD MI300X 与继续学习 Transformer](#amd-mi300x-与继续学习-transformer)
   - 在 RTX 4070 和 AMD MI300X 上训练 GPT-2
   - 在 PyCharm 中调试

2. [我如何理解 Transformer 中的 KQV 机制](#我如何理解-transformer-中的-kqv-机制)
   - Query、Key、Value 矩阵表示 token 之间的交互
   - 理解需要知道维度和形状
   - 初始概念随时间变得清晰
   - AI 时代提供了丰富的学习资源
   - 激励人心的故事推动持续学习

3. [从神经网络到 GPT](#从神经网络到-gpt)
   - 从头实现神经网络以理解
   - Transformer 通过嵌入和编码处理文本
   - 自注意力计算词之间的相似度
   - 观看基础讲座并阅读代码
   - 跟随好奇心通过项目和论文

4. [神经网络如何工作](#神经网络如何工作)
   - 反向传播算法更新权重和偏置
   - 输入数据通过网络层激活
   - 前向传播通过 sigmoid 计算层输出
   - 误差计算指导学习调整
   - 维度理解至关重要



## AMD MI300X 与继续学习 Transformer

*2026.06.08*

- 开始在 RTX 4070 和 AMD MI300X 上更广泛地训练 GPT-2。

- 在 PyCharm 中调试训练流程。

![在 PyCharm 中调试 GPT-2 训练](/assets/images/kqv-transformers/pycharm-debug-2026-06-08.jpg)


## 我如何理解 Transformer 中的 KQV 机制

*2025.07.16*

在阅读了 [K, Q, V Mechanism in Transformers](https://lzwjava.github.io/notes/2025-06-02-attention-kqv-en) 之后，我不知怎地理解了 K、Q 和 V 是如何工作的。

Q 代表 Query，K 代表 Key，V 代表 Value。对于一个句子，Query 是一个矩阵，存储一个 token 需要询问其他 token 的值。Key 代表 token 的描述，Value 代表 token 实际含义的矩阵。

它们有特定的形状，因此需要知道它们的维度和细节。

我大约在 2025 年 6 月初理解了这一点。我第一次了解这个大概是在 2023 年底。那时我阅读了类似 [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) 的文章，但理解得不多。

大约两年后，我发现现在更容易理解了。在这两年里，我专注于后端工作和准备副学士学位考试，没有太多阅读或学习机器学习。然而，我在开车或做其他事情时会不时思考这些概念。

这让我想起了时间的作用。我们可能第一次看到很多内容时并不理解多少，但不知怎地，它触发了我们思考的起点。

随着时间的推移，我发现对于知识和发现，第一次很难思考或理解，但后来似乎更容易学习和掌握。

一个原因是，在 AI 时代，学习变得更容易，因为你可以深入任何细节或方面来解决疑惑。还有更多相关的 AI 视频可用。更重要的是，你看到很多人都在学习和构建基于此的项目，比如 [llama.cpp](https://github.com/ggml-org/llama.cpp)。

Georgi Gerganov 的故事鼓舞人心。作为大约 2021 年开始学习机器学习的新手，他在 AI 社区产生了巨大影响。

这种事情会一次又一次地发生。所以，对于强化学习和最新的 AI 知识，尽管我仍然无法投入大量时间，但我想我能找到一些时间快速学习并努力多思考。大脑会完成它的工作。

---

## 从神经网络到 GPT

*2023.09.28*

### YouTube 视频

Andrej Karpathy - Let's build GPT: from scratch, in code, spelled out.

Umar Jamil - Attention is all you need (Transformer) - Model explanation (including math), Inference and Training

StatQuest with Josh Starmer - Transformer Neural Networks, ChatGPT's foundation, Clearly Explained!!!

Pascal Poupart - CS480/680 Lecture 19: Attention and Transformer Networks

The A.I. Hacker - Michael Phi - Illustrated Guide to Transformers Neural Network: A step-by-step explanation

### 我如何学习

当我读了《Neural Networks and Deep Learning》这本书的一半时，我开始复现识别手写数字的神经网络示例。我在 GitHub 上创建了一个仓库 <https://github.com/lzwjava/neural-networks-and-zhiwei-learning>。

这才是真正的难点。如果一个人能不复制任何代码从头编写，那他就理解得很透彻。

我的复现代码仍然缺少 update_mini_batch 和 backprop 的实现。然而，通过仔细观察加载数据、前向传播和评估阶段的变量，我对向量、维度、矩阵和对象的形状有了更好的理解。

然后我开始学习 GPT 和 transformer 的实现。通过词嵌入和位置编码，文本变成了数字。本质上，它和识别手写数字的简单神经网络没有区别。

Andrej Karpathy 的讲座 "Let's build GPT" 非常好。他解释得很清楚。

第一个原因是它真的是从头开始。我们首先看到如何生成文本，这有点模糊和随机。第二个原因是 Andrej 能非常直观地讲解。Andrej 做了 nanoGPT 项目几个月。

我刚刚有了一个新的想法来判断讲座的质量：作者真的能写出这些代码吗？为什么我不理解，作者遗漏了哪些主题？除了这些优雅的图表和动画，它们的缺点和缺陷是什么？

回到机器学习主题本身。正如 Andrej 提到的，dropout、残差连接、Self-Attention、Multi-Head Attention、Masked Attention。

通过观看更多上面的视频，我开始理解一点。

通过使用 sin 和 cos 函数进行位置编码，我们得到一些权重。通过词嵌入，我们把单词转换成数字。

$$
    PE_{(pos,2i)} = sin(pos/10000^{2i/d_{model}}) \\
    PE_{(pos,2i+1)} = cos(pos/10000^{2i/d_{model}})
$$

> The pizza came out of the oven and it tasted good.

在这个句子中，算法如何知道 "it" 指的是 "pizza" 还是 "oven"？我们如何计算句子中每个词的相似度？

我们想要一组权重。如果我们用 transformer 网络做翻译任务，每次输入一个句子，它就能输出另一种语言的对应句子。

关于这里的点积。我们使用点积的一个原因是点积会考虑向量中的每一个数字。如果我们使用平方点积呢？我们先计算数字的平方，然后做点积。如果我们做一些反向的点积呢？

关于这里的 masking，我们将矩阵的一半数字改为负无穷。然后使用 softmax 使值范围在 0 到 1。如果我们把左下角的数字改为负无穷呢？

### 计划

继续阅读代码、论文和观看视频。享受乐趣，追随好奇心。

<https://github.com/karpathy/nanoGPT>

<https://github.com/jadore801120/attention-is-all-you-need-pytorch>

---

## 神经网络如何工作

*2023.05.30*

我们直接讨论神经网络的核心，也就是反向传播算法：

1. 输入 x：为输入层设置对应的激活 $$a^{1}$$。
2. 前向传播：对于 l=2,3,…,L，计算 $$z^{l} = w^l a^{l-1}+b^l$$ 和 $$a^{l} = \sigma(z^{l})$$
3. 输出误差 $$\delta^{L}$$：计算向量 $$\delta^{L} = \nabla_a C \odot \sigma'(z^L)$$
4. 反向传播误差：对于 l=L−1,L−2,…,2，计算 $$\delta^{l} = ((w^{l+1})^T \delta^{l+1}) \odot \sigma'(z^{l})$$
5. 输出：代价函数的梯度由 $$\frac{\partial C}{\partial w^l_{jk}} = a^{l-1}_k \delta^l_j$$ 和 $$\frac{\partial C}{\partial b^l_j} = \delta^l_j $$ 给出。

这是从 Michael Nelson 的书《Neural Networks and Deep Learning》中抄来的。是不是让人不知所措？第一次看可能如此。但学习一个月后就不会了。让我解释一下。

### 输入

有五个阶段。第一阶段是输入。这里我们使用手写数字作为输入。我们的任务是识别它们。一个手写数字有 784 个像素，即 28*28。每个像素有一个灰度值，范围从 0 到 255。激活是指我们使用某个函数来激活它，将其原始值转换为一个新值以便于处理。

假设我们现在有 1000 张 784 像素的图片。我们训练它来识别它们显示的数字。现在有 100 张图片来测试学习效果。如果程序能识别出 97 张图片的数字，我们就说它的准确率是 97%。

所以我们会循环处理这 1000 张图片，训练出权重和偏置。每次给一张新图片学习时，我们让权重和偏置更正确。

一次小批量训练的结果要在 10 个神经元上体现。这里，10 个神经元代表 0 到 9，它们的值在 0 到 1 之间，表示对其准确性的置信度。

输入是 784 个神经元。我们如何将 784 个神经元减少到 10 个？是这样的。假设我们有两层。层是什么意思？第一层有 784 个神经元。第二层有 10 个神经元。

我们给 784 个神经元中的每一个赋予一个权重，比如：

$$w_1, w_2, w_3, w_4, ... , w_{784}$$

并给第一层一个偏置，即 $$b_1$$。

那么对于第二层的第一个神经元，其值为：

$$w_1*a_1 + w_2*a_2+...+ w_{784}*a_{784}+b_1$$

但这些权重和偏置是针对 $$neuron^2_{1}$$（第二层的第一个）的。对于 $$neuron^2_{2}$$，我们需要另一组权重和偏置。

sigmoid 函数呢？我们使用 sigmoid 函数将上述值的范围映射到 0 到 1。

$$
\begin{eqnarray}
  \sigma(z) \equiv \frac{1}{1+e^{-z}}
\end{eqnarray}
$$

$$
\begin{eqnarray}
  \frac{1}{1+\exp(-\sum_j w_j x_j-b)}
\end{eqnarray}
$$

我们也用 sigmoid 函数激活第一层。也就是说，我们将灰度值转换到 0 到 1 之间。现在，每一层的每个神经元的值都在 0 到 1 之间。

那么对于我们的两层网络，第一层有 784 个神经元，第二层有 10 个神经元。我们训练它得到权重和偏置。

我们有 784 * 10 个权重和 10 个偏置。在第二层中，对于每个神经元，我们将用 784 个权重和 1 个偏置来计算它的值。代码如下：

```python
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]
```

### 前向传播

> 前向传播：对于 l=2,3,…,L，计算 $$z^{l} = w^l a^{l-1}+b^l$$ 和 $$a^{l} = \sigma(z^{l})$$

注意，这里我们使用上一层的值 $$a^{l-1}$$ 和当前层的权重 $$w^l$$ 以及其偏置 $$b^l$$ 进行 sigmoid 运算，得到当前层的值 $$a^{l}$$。

代码：

```python
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
```

### 输出误差

> 输出误差 $$\delta^{L}$$：计算向量 $$\delta^{L} = \nabla_a C \odot \sigma'(z^L)$$

我们来看看 $$\nabla$$ 是什么意思。

> Del，或 nabla，是数学（特别是向量微积分）中使用的算子，作为向量微分算子，通常用 nabla 符号 ∇ 表示。

$$
\begin{eqnarray}
  w_k & \rightarrow & w_k' = w_k-\eta \frac{\partial C}{\partial w_k} \\
  b_l & \rightarrow & b_l' = b_l-\eta \frac{\partial C}{\partial b_l}
\end{eqnarray}
$$

这里 $$\eta$$ 是学习率。我们使用代价函数 C 分别对权重和偏置的导数，即它们之间的变化率。下面的 `sigmoid_prime` 就是它的导数。

代码：

```python
        delta = self.cost_derivative(activations[-1], y) * \
            sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
```

```python
    def cost_derivative(self, output_activations, y):
        return (output_activations-y)
```

### 反向传播误差

> 反向传播误差：对于 l=L−1,L−2,…,2，计算 $$\delta^{l} = ((w^{l+1})^T \delta^{l+1}) \odot \sigma'(z^{l})$$

```python
     for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)
```

### 输出

> 输出：代价函数的梯度由 $$\frac{\partial C}{\partial w^l_{jk}} = a^{l-1}_k \delta^l_j$$ 和 $$\frac{\partial C}{\partial b^l_j} = \delta^l_j $$ 给出。

```python
    def update_mini_batch(self, mini_batch, eta):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]
```

### 总结

这是一篇简短的文章。大部分内容只是展示了代码和数学公式。但对我来说很好。在写这篇文章之前，我理解得并不清楚。在写完之后，或者只是从代码和书中复制片段之后，我理解了大部分内容。在从老师王垠那里获得信心、阅读了约 30% 的《Neural Networks and Deep Learning》一书、听了 Andrej Karpathy 的斯坦福讲座和 Andrew Ng 的课程、与我的朋友 Qi 讨论、以及调整 Anaconda、numpy 和 Theano 库使多年前的代码运行起来之后，我现在理解它了。

其中一个关键点是维度。我们应该知道每个符号和变量的维度。它只是做可微分的计算。最后以王垠的语录作为结束：

> 机器学习真的很有用，甚至可以说是一种美丽的理论，因为它仅仅是经过改头换面的微积分！它是牛顿、莱布尼茨古老而伟大的理论，以更简单、优雅而强大的形式呈现。机器学习基本上是利用微积分来推导和拟合一些函数，而深度学习则是拟合更复杂的函数。

> 人工智能中没有‘智能’，神经网络中没有‘神经’，机器学习中没有‘学习’，深度学习中没有‘深度’。这个领域真正起作用的东西叫做‘微积分’。所以我更喜欢称这个领域为‘可微分计算’，而构建模型的过程称为‘可微分编程’。