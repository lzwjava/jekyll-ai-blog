---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 神经网络、Transformer 和 GPT
translated: true
type: post
---

### 目录

1. [我是如何学习 Transformers 中的 KQV 机制的](#how-i-learned-the-kqv-mechanism-in-transformers)
   - 查询（Query）、键（Key）、值（Value）矩阵代表 token 间的交互
   - 理解需要了解维度和形状
   - 最初的概念会随着时间推移变得更清晰
   - 人工智能时代提供了丰富的学习资源
   - 鼓舞人心的故事激励持续学习

2. [从神经网络到 GPT](#from-neural-network-to-gpt)
   - 从零开始复现神经网络以加深理解
   - Transformers 通过 embedding 和 encoding 处理文本
   - 自注意力机制计算词语间的相似性
   - 观看基础讲座并阅读代码
   - 通过项目和论文追随好奇心

3. [神经网络如何工作](#how-neural-network-works)
   - 反向传播算法更新权重和偏置
   - 输入数据通过网络层激活
   - 前向传播通过 sigmoid 计算层输出
   - 误差计算指导学习调整
   - 理解维度对理解至关重要

## 我是如何学习 Transformers 中的 KQV 机制的

*2025.07.16*

在阅读了 [K, Q, V 机制在 Transformers 中](https://lzwjava.github.io/notes/2025-06-02-attention-kqv-en)之后，我不知怎么地就理解了 K, Q, V 是如何工作的。

Q 代表 Query，K 代表 Key，V 代表 Value。对于一个句子，Query 是一个矩阵，存储一个 token 需要向其他 token 查询的值。Key 代表 token 的描述，Value 代表 token 的实际意义矩阵。

它们有特定的形状，所以需要了解它们的维度和细节。

我在 2025 年 6 月初左右理解了这一点。我最初是在 2023 年底左右接触到它的。那时我读了 [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) 等文章，但并没有理解太多。

大约两年后，我发现现在更容易理解了。在这两年里，我专注于后端工作并准备我的副学士学位考试，并没有大量阅读或学习机器学习。然而，我确实在开车或做其他事情时，不时地思考这些概念。

这让我想起了时间的作用。我们可能刚开始学很多东西，即使理解不多。但不知何故，它触发了我们思考的起点。

随着时间的推移，我发现对于知识和发现，第一次很难思考或理解。但后来，学习和了解似乎变得更容易了。

其中一个原因是，在人工智能时代，学习更容易，因为你可以深入研究任何细节或方面来解决你的疑惑。还有更多相关的 AI 视频可用。更重要的是，你看到如此多的人正在学习并在其基础上构建项目，比如 [llama.cpp](https://github.com/ggml-org/llama.cpp)。

Georgi Gerganov 的故事令人鼓舞。作为一名从 2021 年左右开始的机器学习新手，他在 AI 社区产生了强大的影响。

这种事情会一遍又一遍地发生。所以，对于强化学习和最新的人工智能知识，尽管我仍然无法投入大量时间，但我认为我可以找到一些时间快速学习并尝试多思考它们。大脑会自行发挥作用。

---

## 从神经网络到 GPT

*2023.09.28*

### YouTube 视频

Andrej Karpathy - 让我们从零开始，用代码，逐字逐句地构建 GPT。

Umar Jamil - Attention is all you need（Transformer）- 模型解释（包括数学），推理和训练

StatQuest with Josh Starmer - Transformer 神经网络，ChatGPT 的基础，清晰解释！！！

Pascal Poupart - CS480/680 讲座 19: Attention 和 Transformer 网络

The A.I. Hacker - Michael Phi - Transformer 神经网络图解指南：一步一步的解释

### 我如何学习

当我读完《神经网络与深度学习》一书的一半时，我开始复现识别手写数字的神经网络示例。我在 GitHub 上创建了一个仓库，<https://github.com/lzwjava/neural-networks-and-zhiwei-learning。>

那才是真正困难的部分。如果一个人能从零开始编写代码，而不是复制任何代码，那说明他理解得非常好。

我的复现代码仍然缺少 update_mini_batch 和 backprop 的实现。然而，通过仔细观察加载数据、前向传播和评估阶段的变量，我对向量、维度、矩阵和对象的形状有了更好的理解。

我开始学习 GPT 和 transformer 的实现。通过 word embedding 和 positional encoding，文本变成了数字。然后，本质上，它与识别手写数字的简单神经网络没有区别。

Andrej Karpathy 的讲座“Let's build GPT”非常好。他解释得很清楚。

第一个原因，它确实是从零开始的。我们首先看到如何生成文本。这有点模糊和随机。第二个原因，Andrej 能非常直观地表达事物。Andrej 花了几个月的时间做了 nanoGPT 项目。

我刚刚有了一个新的想法来判断讲座的质量。作者真的能写出这些代码吗？为什么我听不懂，作者遗漏了哪个主题？除了这些优雅的图表和动画，它们的缺点和缺陷是什么？

回到机器学习主题本身。正如 Andrej 所提到的，dropout，residual connection，Self-Attention，Multi-Head Attention，Masked Attention。

通过观看更多的上述视频，我开始有所理解。

通过使用 sin 和 cos 函数进行 positional encoding，我们得到了一些权重。通过 word embedding，我们将单词转换为数字。

$$
    PE_{(pos,2i)} = sin(pos/10000^{2i/d_{model}}) \\
    PE_{(pos,2i+1)} = cos(pos/10000^{2i/d_{model}})
 $$

> 披萨从烤箱里拿出来，味道很好。

在这个句子中，算法如何知道 "it" 指的是披萨还是烤箱？我们如何计算句子中每个词的相似性？

我们想要一组权重。如果我们使用 transformer 网络来做翻译任务，每次我们输入一个句子，它就能输出另一种语言的相应句子。

关于这里的点积。我们在这里使用点积的一个原因是点积会考虑向量中的每个数字。如果我们使用平方点积呢？我们首先计算数字的平方，然后让它们进行点积。如果我们做一些反向点积呢？

关于这里的掩码，我们将一半矩阵的数字改为负无穷。然后我们使用 softmax 使值范围从 0 到 1。如果我们改变左下角的数字为负无穷呢？

### 计划

继续阅读代码和论文，观看视频。只是享受和追随我的好奇心。

<https://github.com/karpathy/nanoGPT>

<https://github.com/jadore801120/attention-is-all-you-need-pytorch>

---

## 神经网络如何工作

*2023.05.30*

让我们直接讨论神经网络的核心，即反向传播算法：

1. 输入 x：为输入层设置相应的激活量 $$a^{1}$$。
2. 前向传播：对于每个 l=2,3,…,L，计算 $$z^{l} = w^l a^{l-1}+b^l$$ 和 $$a^{l} = \sigma(z^{l})$$。
3. 输出误差 $$\delta^{L}$$：计算向量 $$\delta^{L} = \nabla_a C \odot \sigma'(z^L)$$。
4. 反向传播误差：对于每个 l=L−1,L−2,…,2，计算 $$\delta^{l} = ((w^{l+1})^T \delta^{l+1}) \odot \sigma'(z^{l})$$。
5. 输出：成本函数的梯度由 $$\frac{\partial C}{\partial w^l_{jk}} = a^{l-1}_k \delta^l_j$$ 和 $$\frac{\partial C}{\partial b^l_j} = \delta^l_j $$ 给出。

这是从 Michael Nelson 的书《神经网络与深度学习》中复制过来的。是不是很让人不知所措？第一次看到时可能会，但在一个月的学习之后就不会了。让我来解释一下。

### 输入

总共有 5 个阶段。第一个阶段是输入。这里我们使用手写数字作为输入。我们的任务是识别它们。一个手写数字有 784 像素，即 28*28。每个像素都有一个灰度值，范围从 0 到 255。所以，激活意味着我们使用某个函数来激活它，将其原始值改变为一个新值，以便于处理。

比方说，我们现在有 1000 张 784 像素的图片。我们现在训练它来识别它们显示的数字。我们现在有 100 张图片来测试学习效果。如果程序能识别 97 张图片的数字，我们说它的准确率是 97%。

所以我们将遍历这 1000 张图片，训练出权重和偏置。每次我们给它新的图片学习时，我们都会使权重和偏置更加正确。

一个批次训练结果将反映在 10 个神经元中。这里，这 10 个神经元代表从 0 到 9，其值范围从 0 到 1，以表示它们对其准确性的信心。

输入是 784 个神经元。我们如何将 784 个神经元减少到 10 个神经元？这就是关键。假设我们有两层。层是什么意思？就是第一层，我们有 784 个神经元。在第二层，我们有 10 个神经元。

我们给 784 个神经元中的每个神经元一个权重，比如：

$$w_1, w_2, w_3, w_4, ... , w_{784}$$

并给第一层一个偏置，即 $$b_1$$。

对于第二层中的第一个神经元，它的值是：

$$w_1*a_1 + w_2*a_2+...+ w_{784}*a_{784}+b_1$$

但是这些权重和一个偏置是针对 $$neuron^2_{1}$$（第二层中的第一个）。对于 $$neuron^2_{2}$$，我们需要另一组权重和一个偏置。

sigmoid 函数呢？我们用 sigmoid 函数将上述值映射到 0 到 1 之间。

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

我们还使用 sigmoid 函数来激活第一层。也就是说，我们将灰度值改变为 0 到 1 的范围。所以现在，每一层中的每个神经元都有一个介于 0 到 1 之间的值。

所以现在对于我们的两层网络，第一层有 784 个神经元，第二层有 10 个神经元。我们训练它来获得权重和偏置。

我们有 784 * 10 个权重和 10 个偏置。在第二层中，对于每个神经元，我们将使用 784 个权重和 1 个偏置来计算其值。这里的代码如下：

```python
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]
```

### 前向传播

> 前向传播：对于每个 l=2,3,…,L，计算 $$z^{l} = w^l a^{l-1}+b^l$$ 和 $$a^{l} = \sigma(z^{l})$$

请注意，这里我们使用上一层的值，即 $$a^{l-1}$$ 和当前层的权重 $$w^l$$ 及其偏置 $$b^l$$ 进行 sigmoid 运算，以获取当前层的值 $$a^{l}$$。

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

让我们看看 $$\nabla$$ 是什么意思。

> Del，或 nabla，是数学中（尤其是在向量微积分中）用作向量微分算子的运算符，通常用 nabla 符号 ∇ 表示。

$$
\begin{eqnarray}
  w_k & \rightarrow & w_k' = w_k-\eta \frac{\partial C}{\partial w_k} \\
  b_l & \rightarrow & b_l' = b_l-\eta \frac{\partial C}{\partial b_l}
\end{eqnarray}
$$

这里 $$\eta $$ 是学习率。我们使用 C 对权重和偏置的导数，即它们之间的变化率。这就是下面的 `sigmoid_prime`。

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

> 反向传播误差：对于每个 l=L−1,L−2,…,2，计算 $$\delta^{l} = ((w^{l+1})^T \delta^{l+1}) \odot \sigma'(z^{l})$$

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

> 输出：成本函数的梯度由 $$\frac{\partial C}{\partial w^l_{jk}} = a^{l-1}_k \delta^l_j$$
和 $$\frac{\partial C}{\partial b^l_j} = \delta^l_j $$ 给出。

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

这是一篇短文。大部分内容只是展示代码和数学公式。但这对我来说没问题。在写它之前，我并不完全理解。写完或者只是从代码和书中复制片段之后，我理解了大部分。在从老师王垠那里获得信心，阅读了《神经网络与深度学习》约 30% 的内容，听了 Andrej Karpathy 的斯坦福讲座和 Andrew Ng 的课程，和我的朋友 Qi 讨论，以及调整 Anaconda、numpy 和 Theano 库使多年前的代码能够工作之后，我现在理解了它。

关键点之一是维度。我们应该知道每个符号和变量的维度。它只是进行可微计算。让我们以王垠的话作结：

> 机器学习真的非常有用，甚至可以说它是一种美丽的理论，因为它只是微积分经过一番改造！它是牛顿、莱布尼茨古老而伟大的理论，以一种更简单、优雅和强大的形式呈现。机器学习基本上就是利用微积分来推导和拟合一些函数，而深度学习就是拟合更复杂的函数。

> 人工智能中没有什么“智能”，神经网络中没有什么“神经”，机器学习中没有什么“学习”，深度学习中没有什么“深度”。真正起作用的领域叫做“微积分”。所以我更喜欢称这个领域为“可微计算”，而构建模型的过程叫做“可微编程”。
