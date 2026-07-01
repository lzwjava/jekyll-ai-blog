---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 扩散与迭代优化
translated: true
type: note
---

**问题：** "diffusion in Transformers" 是指生成一张图像，然后反复将其输入回去再次生成吗？

**回答：**

不太准确——你把两件不同的事情混淆了。我来帮你梳理清楚。

## 扩散（Diffusion）过程

扩散模型的工作分为**两个阶段**：

**前向过程（训练时）：** 取一张真实图像，在 T 步内逐步添加高斯噪声，直到变成纯噪声。这个过程是固定的/解析的——不需要神经网络。

**反向过程（推理时）：** 从纯噪声开始，逐步*去噪*——每一步预测并去除一小部分噪声。

```
x_T（纯噪声）→ x_{T-1} → x_{T-2} → ... → x_0（干净图像）
```

没错，你需要运行模型大约 50–1000 次，但**每一步都是去噪，而不是从头再生**。模型每一步预测的是噪声分量 ε，而非直接预测最终图像。

核心公式（DDPM）：

```
x_{t-1} = 1/√α_t * (x_t - (1-α_t)/√(1-ᾱ_t) * ε_θ(x_t, t)) + σ_t * z
```

其中 `ε_θ` 是神经网络（U-Net 或 Transformer）。

---

## Transformer 如何融入其中

**DiT（Diffusion Transformer, Peebles & Xie 2022）** 用 Transformer 取代了 U-Net 骨干网络。其架构：

1. 将带噪潜在特征 `x_t` 分块（patchify）为 tokens
2. 通过 **adaLN**（自适应层归一化）以时间步 `t` 和类别标签为条件
3. 运行标准 Transformer 模块（自注意力 + FFN）
4. 将 tokens 重新拼回（unpatchify）潜在形状

```python
# DiT 前向传播示意
def forward(self, x, t, y):
    x = self.patchify(x)           # [B, N, D]
    x = x + self.pos_embed         # 位置编码
    c = self.adaln_embed(t, y)     # 时间步 + 类别条件
    for block in self.blocks:
        x = block(x, c)            # transformer + adaLN
    x = self.unpatchify(x)         # 预测噪声 ε
    return x
```

这种方法被用在 **Stable Diffusion 3**、**FLUX**、**Sora** 中——它们都使用 DiT 取代了 U-Net。

---

## 推理时的实际循环

```python
x = torch.randn(latent_shape)   # 从噪声开始

for t in reversed(range(T)):    # 例如使用 DDIM 时 T=50
    eps = model(x, t, conditioning)   # transformer 预测噪声
    x = denoise_step(x, eps, t)       # scheduler 去除该噪声

image = vae.decode(x)           # 将潜在特征解码为像素空间图像
```

每次迭代：同一个模型，不同的 `t`，逐步变得干净的 `x`。这不是“生成图像 → 用图像作为提示”——而是“去噪潜在特征 → 再次去噪”。

---

## 你可能想到的（迭代细化）

确实存在更接近你描述的模型：

- **一致性模型（Consistency Models）**——将扩散蒸馏为更少的步骤，可以一步生成
- **流匹配（Flow Matching）**（用于 SD3、FLUX）——使用直线轨迹而非扩散
- **自回归图像模型**（如 LlamaGen、VAR）——顺序预测图像 token，更像语言建模

VAR（Visual AutoRegressive）尤其有趣——先生成粗糙分辨率，然后在更细尺度上细化。这更接近“生成图像 → 用它再次生成”。

---

## 总结

| 概念 | 实际发生了什么 |
| --- | --- |
| 扩散 | 从噪声到图像的迭代**去噪** |
| DiT | Transformer 作为去噪骨干 |
| 你的描述 | 更接近迭代细化 / VAR |

DiT 中的 Transformer 在架构上并没有为扩散做什么特别的事情——它只是比 U-Net 更好的去噪骨干网络，因为自注意力能够捕获卷积 U-Net 在大规模下难以处理的远距离空间依赖。

**参考文献：**

- [DiT 论文 —— Scalable Diffusion Models with Transformers](https://arxiv.org/abs/2212.09748)
- [DDPM —— Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239)
- [VAR —— Visual AutoRegressive Modeling](https://arxiv.org/abs/2404.02905)
