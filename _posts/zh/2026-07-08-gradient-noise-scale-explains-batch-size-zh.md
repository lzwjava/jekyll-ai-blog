---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 梯度噪声尺度解释批量大小
translated: true
type: note
---

问题："如果你有大量VRAM，在收敛瓶颈阶段增加batch size会得到更好的结果"——这个技巧背后的机制是什么？为什么有效？

答案：

## 核心思想：随着损失降低，梯度噪声尺度增大

梯度噪声尺度本质上衡量了训练样本间梯度的信噪比，它可以近似预测大量任务中最大有效batch size。McCandlish等人（OpenAI，2018）的关键发现：噪声尺度会随着训练过程中损失的降低而增加，并且其大小主要通过模型性能的提升与模型规模相关。

这直接解释了你的观察。在训练早期，小batch具有数据效率，因为每个样本的梯度高度相关（冗余）。当你接近平台/瓶颈时，相对于缩小的"真实"梯度信号，每个样本的梯度开始产生更多分歧——因此小batch对你实际应移动的方向给出了一个嘈杂、低信噪比的估计。增大batch size可以平均掉这些噪声，给你一个更清晰的下降方向，让你重新取得实际进展，而不是让优化器在平台附近随机游走。

## 数学原理

对损失函数在当前点 $\theta$ 附近进行二阶（二次）展开，设真实最小值 $\theta^*$，Hessian矩阵 $H$：

$$L(\theta) \approx L^* + \tfrac{1}{2}(\theta-\theta^*)^T H (\theta-\theta^*)$$

**真实梯度**：$g_{\text{true}} = H(\theta - \theta^*)$

大小为 $B$ 的小批量梯度估计：$\hat g = g_{\text{true}} + \epsilon$，其中 $\epsilon \sim \mathcal{N}(0, \Sigma/B)$，$\Sigma$ 是每个样本梯度的协方差（大致恒定，由数据集决定——与你离最优点的距离无关）。

- 随着你接近最小值，$\theta \to \theta^*$，因此 $\|g_{\text{true}}\| \to 0$。
- 但 $\Sigma$（来自样本间方差的噪声）不会以相同速率缩小。
- **对于固定 $B$，信噪比 = $\|g_{\text{true}}\|^2 / \text{tr}(\Sigma)/B$ 在收敛附近急剧下降**。

McCandlish的简化噪声尺度（假设Hessian条件良好），本质上衡量了梯度相对于噪声的大小：

$$B_{\text{noise}} = \frac{\text{tr}(\Sigma)}{\|G\|^2}$$

其中 $G$ 是真实（总体）梯度。这实际上就是"关键batch size"——McCandlish等人（2018）提出，存在一个关键batch size（CBS），低于该值训练不会显著降低损失，可以根据训练过程中的梯度噪声尺度来估计。而CBS与梯度噪声尺度之间的这种对应关系，正是训练分布中每个样本梯度的方差。

由于 $B_{\text{noise}} \propto 1/\|G\|^2$，且当损失处于平台时 $\|G\| \to 0$，**有效/关键batch size会随着损失降低而机械地增长**。这就是整个技巧的形式化解释。

## 为何表现为"收敛瓶颈 → 增大batch size有帮助"

更少噪声的梯度估计使SGD类优化器能够迈出更大的步长，从而在更少的迭代次数内收敛。具体来说，在平台期：

1. 小batch的梯度方向主要受每个样本的噪声支配，而非曲率信号。
2. 优化器实际上在局部盆地周围"振动"而不是下降——你会看到损失振荡或爬行。
3. 增大 $B$（通过更大的实际batch，或如果VRAM仅受激活限制则使用梯度累积）会缩小 $\Sigma/B$，恢复信噪比，恢复每一步的有效进展。
4. 在这个阶段，你**不需要**像早期训练线性缩放规则建议的那样按比例提高学习率——关键在于方差缩减，而非步长缩放。

这就是为什么GPT-3风格的训练会在训练过程中逐渐增大batch size（32K → 3.2M tokens），而不是固定一个值——它跟踪增长的临界batch size，而不是一开始就猜一个数字。

## 实用估计器（可用于你自己的MI300X/nanochat运行）

你不需要完整的Hessian矩阵。McCandlish的简单估计器使用两个batch size和梯度范数方差的技巧：

```python
import torch

def per_example_grads(model, loss_fn, x, y):
    """返回每个样本梯度向量的列表（展平后）。"""
    grads = []
    for i in range(x.size(0)):
        model.zero_grad()
        loss = loss_fn(model(x[i:i+1]), y[i:i+1])
        loss.backward()
        g = torch.cat([p.grad.flatten() for p in model.parameters() if p.grad is not None])
        grads.append(g.clone())
    return torch.stack(grads)  # [B, D]

def noise_scale_estimate(model, loss_fn, x, y, b_small, b_big):
    """
    双batch size估计器（McCandlish等，2018，附录A）。
    在训练期间定期运行（例如每N步）。
    """
    g_all = per_example_grads(model, loss_fn, x[:b_big], y[:b_big])  # [b_big, D]

    g_small = g_all[:b_small].mean(dim=0)
    g_big   = g_all.mean(dim=0)

    norm_small_sq = g_small.pow(2).sum().item()
    norm_big_sq   = g_big.pow(2).sum().item()

    # 真实梯度平方（G2）和噪声尺度（S）的无偏估计
    G2 = (b_big * norm_big_sq - b_small * norm_small_sq) / (b_big - b_small)
    S  = (norm_small_sq - norm_big_sq) / (1.0 / b_small - 1.0 / b_big)

    B_noise = S / G2
    return B_noise, G2, S
```

将 `B_noise` 与你的损失曲线一起跟踪。当你看到它在平台附近急剧上升（即 `B_noise` 接近或超过你当前的有效batch size）时，这就是你增大 `B` 的经验信号——可以是实际的微批大小（如果你的192GB HBM3还有空间），也可以是梯度累积步数。这比"损失看起来卡住了，我们多塞点batch"更有原则。

## 一个需要内化的注意事项——在过度应用之前

虽然他们的方法在实践中已被采用，例如在训练GPT-3时，但需要强假设来证明梯度噪声作为CBS的代理是合理的，这使得这种方法在实践中是否可信仍不明确，限制了其适用性。2025年的NeurIPS论文重新审视了这个问题，并提出了一种更直接的实验性CBS估计器，而不是盲目信任噪声尺度代理——如果你正在为DeepSeek v4 MoE规模的运行调优，这值得一读，因为每个专家的梯度统计比McCandlish研究的密集模型情况更复杂。

参考文献：

- [An Empirical Model of Large-Batch Training (McCandlish et al., 2018)](https://arxiv.org/abs/1812.06162)
- [Critical Batch Size Revisited (NeurIPS 2025)](https://arxiv.org/html/2505.23971v1)
