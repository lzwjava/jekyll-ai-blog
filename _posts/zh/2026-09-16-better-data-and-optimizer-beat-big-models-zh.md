---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 更好的数据和优化器击败大模型
translated: true
type: note
---

**问题：Hugo Vergnes 是如何训练 `little-lm` 的，为什么它只花费约 1000 美元却击败了 nanochat 和 GPT-2？**

答案：

关键**并不是某个神奇的架构技巧**，而基本是：

> **更好的数据 + 激进的优化器 + 更好的学习率调度 + 现代架构 + 极致的 GPU 利用率。**

Hugo 使用 **8× B200 训练了 43 小时**，在 **653 亿个 token** 上**从零训练了一个 38.48 亿参数的纯解码器模型**，花费 **998 美元**，达到了 **0.384 CORE**。他的对比是 GPT-2 1.5B = 0.2565，nanochat d32 ≈1B = 0.310。([Hugo Vergnes][1])

![Image](https://images.openai.com/static-rsc-4/4gumHJTx4wSPc1CLSVQdr3evptuk-LQ2fQaDhoGk08OjSCXTnjEs5G-VkBzgPU5bmuTWCe-VlXNwJz0JHOQyhiy0oKXnhPlS9OLS9fE_E7CC7seBVLnidKIvsL-OiwWHkLRxmGmN-l62KUGrd-zXZLomcgnHOCQpncRW8-kHTkPCdvkPE6Ae_cmjhuMZqXWT?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/EoUedrrHBPEbU8iZUD0A95GEb3Mctc0FLS9Y57eSWBVV-Hib5ms3jjpJyC6ahgKD4edOfOMLkHCMjXZlX8TmiEKaSJHfTM5RsnRyZ0ScngPP16Ce0D2WYfP9ccuKsD8TsWxEIXYocVW-fVdD7XltcVRd_8sf1z3d3XkCPe_gw_jPzxUIEURePJsmIVEmzoZ2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/h6V2ERw5OAv_ML07r1KRGDSGE4gq_xhB7wHwi4aMZWv1oyVGugKXYmfkKYKihL_YFs3yO0eB1NUQI85RsnON9bfPNYzrArINohGKZ-Sa8NEsM3J6-gap3wi59Tlsady2u4MWeB8RPWELz_PLca_VxLyR34hVc6BzhCDfyyP0_TlQ7_E0p7kQ1OJRE3BCxcdH?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/zzuPoN2u_1Z8waWRwdsV46xjfW9HEplonJCl5r-dp5vMFfXnKBRWg6OvrTb9Spp24C0NaYSThUGxKD1l2rBnbAQ3Z_vd3PcELKArbzpeH6ItRVMHst_MK8ybv-rxzn_iCbj9-aN2PtTDI7K-QwJARCbYSwubrK3KKOqXM8NRsxj-shcxokY-CUuAw2iKSdOM?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/O9ljkHoYYtvuMxrH9mSpjs1Ykmm9O2RgtR_BFHXOguoPJpE9ZXwsq93zz877s8XIqQJ6EqE2pVxMG3r61tpRPiaoyebb01ciVU65oo7RzXUI50MDQjJY_aVTtYHmBEeYee8jmHNVWbjQVoWHJqPEieiBicWh5DEOuc1FgDw7uHCXGmpcMHT45RwZsv_Jbjgh?purpose=fullsize)

### 1. 第一次尝试其实很糟糕

这可能是最有趣的部分。

他最初训练的是：

```text
8.58 亿参数
FineWeb-Edu
164 亿 token
1× A100
2048 上下文
AdamW
lr = 2.5e-4
余弦衰减 → 0
```

结果：

```text
PIQA = 60.45%
```

而 **GPT-2 1.24 亿 ≈ 63%**。

所以一个大约 **7 倍大** 的模型反而更差。([Hugo Vergnes][1])

损失曲线暴露了问题：余弦衰减过早地降到了接近零，导致最后大约 30% 的计算量基本被浪费了。

这引出了重要的改变。

---

## 2. 实际有效的配方

### 架构

他的最终模型大致如下：

```yaml
model:
  params: 38.48 亿
  layers: 28
  vocab: 50304
  context: 2048

  norm: RMSNorm
  positional: RoPE

  attention:
    type: GQA
    q_heads: 24
    kv_heads: 8
    qk_norm: true

  mlp:
    activation: relu_squared

  logits:
    softcap: true

  residual:
    learnable_layer_scalars: true

  value_embeddings:
    tables: 14
```

不寻常的部分是 **值嵌入（value embeddings）**。

它们增加了大约：

```text
7.21 亿参数
约占模型参数的 19%
```

但它们基本上是查找操作，所以它们增加了参数/内存，却没有按比例增加 FLOPs（浮点运算量）。([Hugo Vergnes][1])

有趣的消融实验：

```text
+ 值嵌入
→ 损失改善 +0.46%
→ CORE 提升 +3.2%
```

并且吞吐量基本保持不变。([Hugo Vergnes][2])

所以，在训练受限于 FLOPs 的（FLOP-bound）情况下，这是一个非常好的**计算-参数权衡**。

---

# 3. 最大的优化器改变：Muon

他不是使用：

```python
AdamW(all_parameters)
```

而是使用：

```python
Muon(matrix_parameters)
AdamW(other_parameters)
```

概念上：

```python
for p in matrix_params:
    p ← Muon(p)

for p in vectors_and_scalars:
    p ← AdamW(p)
```

为什么？

AdamW 为每个参数维护一阶和二阶矩。而 Muon 则对矩阵参数的更新执行近似的正交化。

大致上：

$$
W_{t+1}=W_t-\eta\,\mathrm{Muon}(G_t)
$$

其中 Muon 对梯度/更新应用 Newton-Schulz 式正交化。

重要的实证观察并不是“Muon 每步更便宜”。

它**不是**。

Hugo 在浅梯度累积测试中测量到，每个优化器步骤大约有 **25% 的开销**。但通过梯度累积，这个开销仅占总运行时间的大约 4%，而收敛速度的提升足以使整个运行过程显著加快。([Hugo Vergnes][1])

这是重要的工程经验：

> **优化减少损失的“每单位成本”，而不是孤立地看“每秒 token 数”。**

---

# 4. 学习率调度出奇地重要

初步尝试：

```text
5% 预热
余弦衰减 → 0
```

效果不好。

最终方案：

```text
5% 预热
↓
平稳 / 高学习率
↓
线性冷却
↓
峰值学习率的 5%
```

大致是：

```python
if step < warmup:
    lr = peak * step / warmup

elif step < cooldown_start:
    lr = peak

else:
    lr = peak * linear_decay(
        step,
        cooldown_start,
        total_steps,
        final=0.05,
    )
```

为什么这很重要：

使用余弦衰减到 0，模型实际上在说：

> “我已经学完了。”

而这时仍有大量有用的数据剩余。

最终运行的评估损失在最后一步**仍在下降**。([Hugo Vergnes][1])

这与失败的 8.58 亿参数运行相比，是一个巨大的差异。

---

# 5. 数据：ClimbMix > FineWeb-Edu

这是另一个重大飞跃。

失败的运行使用了：

```text
FineWeb-Edu
```

成功的运行切换到了：

```text
ClimbMix
```

Hugo 将其描述为**“收敛速度的巨大飞跃”**。([Hugo Vergnes][1])

这一点在与 GPT-2 比较时非常重要。

GPT-2 并没有在现代化的精选训练数据上训练。它的 WebText 语料库大约 40GB，由来自 Reddit 高赞链接的网页组成。([Wikipedia][3])

所以说：

> “3.8B > 1.5B”

并不是真正有趣的结论。

有趣的结论是：

> **2026 年的数据 + 架构 + 优化器 + 训练基础设施，使得一个约 1000 美元的单节点实验，在计算效率上远超 2019 年的前沿配方。**

---

# 6. FP8 是巨大的吞吐量倍增器

他对 GEMM（通用矩阵乘法）使用了 FP8 训练：

```text
前向 GEMM → FP8
反向 GEMM → FP8
反向 GEMM → FP8
```

并采用动态张量级缩放。

然后：

```text
词汇表：
50257 → 50304
```

因为 50304 可以被 64 整除，能更好地映射到张量核心硬件。

结合这些因素，粗略产生了：

```text
+33% 吞吐量
```

主要来自 FP8。([Hugo Vergnes][1])

他还使用了融合线性交叉熵，这样庞大的：

$$
[B,T,V]
$$

logit 张量就不需要完整实例化。

当你自己支付 GPU 账单时，这正是那种至关重要的优化。

---

# 7. 最终吞吐量惊人

最终运行：

```text
8 × B200
约 48 万 tokens/秒
573 亿 token
约 33 小时
```

以及 2048 上下文的重新运行：

```text
653 亿 token
43 小时
998 美元
CORE = 0.384
```

GPU 利用率：

```text
92% SM 活动率
40% SM 占用率
```

低占用率不一定是不好的。工作负载主要被大型 GEMM 主导，在这种情况下，寄存器/块利用率可能比最大化占用率更重要。([Hugo Vergnes][1])

他估计大约：

```text
每块 B200 持续 1.047 PFLOP/s
与 Blackwell 密集 FP8 峰值相比，MFU 约 25%
```

重要的是：

> **DDP 就足够了。**

在单节点上训练 38 亿参数模型，不需要 FSDP、ZeRO 或分片优化器。([Hugo Vergnes][1])

---

# 8. 为什么它击败了 nanochat？

这是比较变得有趣的地方。

Hugo 的表格：

| 模型           |     参数   |     Tokens | 硬件       |     成本    |      CORE   |
| -------------- | ---------: | ---------: | ---------- | ----------: | ----------: |
| GPT-2          |       1.5B |         —  | —          |          —  | **0.2565**  |
| nanochat d26   |      ~561M |      11.2B | 8× H100    |          —  | **~0.258**  |
| nanochat d32   |        ~1B |         —  | 8× H100    |    ~$1000   | **0.310**   |
| little-lm      | **3.848B** | **65.3B**  | **8× B200**| **$998**    | **0.384**   |

([Hugo Vergnes][1])

所以，“超越 nanochat”并不是一个神秘的飞跃。

他在相同的约 1000 美元预算下，使用了：

```text
比 nanochat d32 多约 4 倍参数
653 亿训练 token
现代数据
Muon
更好的学习率调度
FP8
现代 Llama 风格架构
B200 而非 H100
```

硬件经济性至关重要。

---

# 9. 真正的公式

我会将 Hugo 的结果总结为：

$$
\boxed{
\text{质量}
\approx
f(
\text{数据质量},
\text{token 数量},
\text{参数量},
\text{优化器},
\text{架构},
\text{计算效率}
)
}
$$

但实际的优化目标是：

$$
\boxed{
\frac{\Delta \text{质量}}
{\$}
}
$$

而不是：

$$
\frac{\text{tokens/秒}}{\$}
$$

或者仅仅是：

$$
\text{参数量}
$$

他失败的 8.58 亿参数实验完美地证明了这一点。

---

## 如果你要复现，我会复制哪些部分

考虑到你使用 MI300X 的经验，我会将配方简化为：

```yaml
model:
  size: ~3B
  architecture: llama-ish
  norm: rmsnorm
  position: rope
  attention: GQA
  qk_norm: true
  mlp: relu2
  value_embeddings: true

data:
  dataset: ClimbMix
  tokens: 500-700 亿

optimizer:
  matrix: muon
  vector: adamw

schedule:
  warmup: 5%
  hold: ~45%
  linear_cooldown: ~50%
  final_lr: 峰值学习率的 5%

precision:
  compute: fp8
  master_weights: bf16

systems:
  vocab_padding: 64
  fused_linear_ce: true
  local_data_shards: true
  DDP: true
```

然后，**不要盲目复制 3.8B 配方**。

我会先运行一个受控的 300M–1B 参数规模的扫描：

```text
                  A          B          C
优化器            AdamW      Muon       Muon
调度              cosine     cosine     trapezoid
数据              FW-Edu     ClimbMix   ClimbMix
架构              基线       基线        最终版
```

并测量：

```text
损失 / 10 亿 tokens
CORE / 10 亿 tokens
tokens/秒
$ / CORE 提升
```

这会告诉你，在你的硬件/数据上，*哪个* 成分真正带来了提升，而不是花费 1000 美元去复现别人调好的最优解。

一个特别重要的注意事项：Hugo 明确表示，他**没有对峰值学习率、QK-norm 或 GQA 比例进行消融实验**，并且最终配方中的一些部分是从 nanochat 继承而来，而非在此规模下独立验证。所以这是一个非常好的经验配方，但并不能证明每个组件都是必需的。([Hugo Vergnes][1])

参考资料：

* [Hugo Vergnes — 以 998 美元训练一个 3.8B LLM 达到 0.384 CORE](https://hugovergnes.github.io/little-lm-3-8b/?utm_source=chatgpt.com)
* [Hugo Vergnes — little-lm 项目页面](https://hugovergnes.github.io/projects/little-lm/?utm_source=chatgpt.com)
* [GPT-2 论文 / 语言模型是无监督多任务学习器](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf?utm_source=chatgpt.com)

我也可以把它变成一个**极简的 `little-lm` 风格 PyTorch 训练栈，并为你推导出在 MI300X 集群上训练 1B 或 3.8B 模型的精确参数/FLOP 预算**。

[1]: https://hugovergnes.github.io/little-lm-3-8b/ "以 998 美元训练一个 3.8B LLM 达到 0.384 CORE | Hugo Vergnes"
[2]: https://hugovergnes.github.io/projects/little-lm/ "little-lm | Hugo Vergnes"
[3]: https://en.wikipedia.org/wiki/GPT-2?utm_source=chatgpt.com "GPT-2"
