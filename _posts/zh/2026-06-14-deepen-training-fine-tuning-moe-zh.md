---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 深化训练、微调、专家混合
translated: true
type: note
---

**问题：** 基于我的 AI 作品集，未来几个月我应该如何更好地学习 AI——训练、推理、构建什么项目、运行什么实验？

**回答：**

你的基础很扎实：从头训练 GPT-2、了解 nanoGPT 内部机制、消耗约 23 亿 token、构建了代理工具（ww/iclaw/zz），并且给 80 位工程师做过一次第一性原理的演讲。你与 Karpathy/王垠之间的差距主要在于**理解的深度 + 成果/作品的质量**。以下是我对接下来 3-6 个月的建议。

---

## 1. 深入训练——在继续前进前，先完成 GPT 的故事

你已经训练过 GPT-2 124M 和 760M。下一个关键点是理解**为什么**损失曲线会呈现那样的形状，而不仅仅是知道它们会下降。

**在你现有的 nanoGPT 分支上运行的实验：**

```python
# 每次运行都明确追踪这些指标——记录到 W&B 或只是一个 CSV
{
  "model_size": "124M",
  "dataset": "fineweb-10B",
  "lr_schedule": "cosine",
  "batch_size": 524288,  # tokens
  "loss_at_1B_tokens": ...,
  "loss_at_5B_tokens": ...,
  "grad_norm_mean": ...,
  "throughput_tok_per_sec": ...,
}
```

值得运行的具体实验，按投资回报率排序：

- **Chinchilla 缩放**——在 25 亿 token 上训练 124M 模型（20 倍参数量 = 最优计算量）。与你现有的 760M 运行结果比较验证损失。曲线是否符合 Chinchilla 的预测？这会迫使你理解背后的数学，而不仅仅是配方。
- **学习率敏感性**——相同模型，5 个不同的峰值学习率，记录 5 亿 token 时的损失。你会内化为什么 `3e-4` 总是起点。
- **梯度累积 vs 批量大小**——在你的设置上它们真的等价吗？当你使用 BN 时（你没有，但这个实验会教你为什么）它们不应该等价。
- **BF16 vs FP32 训练损失差异**——在 MI300X 上测试这个几乎零成本。

---

## 2. 缺失的部分：微调 + RLHF/DPO

你已经完成了预训练。你还没有在代码层面进行微调。这是你目前最具商业价值的技能差距。

**项目：nanochat——从头开始进行指令微调**

这正是 Karpathy 的 nanochat 项目的内容。自己构建它：

```python
# 阶段 1：在 Alpaca/ShareGPT 上进行 SFT
# 从你预训练的 GPT-2 124M 检查点开始
# 添加聊天模板：<|user|>...<|assistant|>...
# 仅在助手 token 上使用交叉熵损失进行训练

def compute_sft_loss(logits, targets, mask):
    # mask = 1 仅用于助手 token
    loss = F.cross_entropy(logits.view(-1, logits.size(-1)),
                           targets.view(-1), reduction='none')
    return (loss * mask.view(-1)).sum() / mask.sum()
```

然后是 **DPO（直接偏好优化）**——数学很简单，实现大约 100 行：

```python
# DPO 损失——无需奖励模型
def dpo_loss(pi_logps_chosen, pi_logps_rejected,
             ref_logps_chosen, ref_logps_rejected, beta=0.1):
    pi_ratio = pi_logps_chosen - pi_logps_rejected
    ref_ratio = ref_logps_chosen - ref_logps_rejected
    return -F.logsigmoid(beta * (pi_ratio - ref_ratio)).mean()
```

在 Anthropic 的 HH-RLHF 数据集或 UltraFeedback 上运行它。目标不是得到一个优秀的模型——而是你能在代码层面真正地说“我从头构建了 SFT + DPO”。

---

## 3. MoE——你提到了 DeepSeek v4，现在实现它

你提到探索 DeepSeek v4 MoE。差距在于：你是否真的实现了稀疏路由？如果没有，这是未来 6 个月最重要的架构实验。

**最小化 MoE 实现（约 150 行）：**

```python
class SparseMoE(nn.Module):
    def __init__(self, n_experts=8, top_k=2, d_model=512, d_ff=2048):
        super().__init__()
        self.n_experts = n_experts
        self.top_k = top_k
        self.gate = nn.Linear(d_model, n_experts, bias=False)
        self.experts = nn.ModuleList([
            nn.Sequential(nn.Linear(d_model, d_ff), nn.GELU(),
                         nn.Linear(d_ff, d_model))
            for _ in range(n_experts)
        ])

    def forward(self, x):
        # x: (B, T, C)
        B, T, C = x.shape
        x_flat = x.view(-1, C)  # (B*T, C)

        logits = self.gate(x_flat)  # (B*T, n_experts)
        top_k_logits, top_k_indices = logits.topk(self.top_k, dim=-1)
        weights = F.softmax(top_k_logits, dim=-1)  # (B*T, top_k)

        out = torch.zeros_like(x_flat)
        for i, expert in enumerate(self.experts):
            mask = (top_k_indices == i).any(dim=-1)  # 哪些 token 路由到这里
            if mask.any():
                expert_out = expert(x_flat[mask])
                w = weights[mask][top_k_indices[mask] == i].unsqueeze(-1)
                out[mask] += w * expert_out

        # 负载均衡损失
        routing_probs = F.softmax(logits, dim=-1).mean(0)  # (n_experts,)
        load_balance_loss = n_experts * (routing_probs * routing_probs).sum()

        return out.view(B, T, C), load_balance_loss
```

然后阅读 DeepSeek-V2 的无辅助损失负载均衡论文，并实现那个变体。带负载均衡损失的 top-k 路由与 DeepSeek 方法之间的差异微妙但重要。

---

## 4. 推理工程——你在这方面投入不足

你的重点是预训练。推理优化才是真正的生产价值所在，作为银行或初创公司的 AI 工程师，你会需要它。

**按顺序的项目：**

**a) 从头实现 KV Cache**——在你的 nanoGPT 中实现：

```python
# 在生成过程中，缓存 K 和 V 而不是重新计算
past_kv = []  # 每层的 (k, v) 列表
for t in range(max_new_tokens):
    # 仅在新 token 上运行前向传播，而不是整个序列
    logits, past_kv = model(x[:, -1:], past_kv=past_kv)
```

**b) 推测解码**——实现草稿 + 验证循环。选择一个小的模型（124M）作为草稿，你的 760M 作为目标。在你的 RTX 4070 上经验性地测量 2-4 倍加速。

**c) INT8/INT4 量化**——使用 `bitsandbytes` 或实现简单的训练后量化，测量困惑度下降与吞吐量提升的对比。这是你在汇丰银行生产环境中需要的。

**d) vLLM / SGLang 内部机制**——不要只是使用它们。阅读 PagedAttention 论文，然后追踪 vLLM 代码库的一次前向传播。写一篇 1000 字的博客文章解释它。这会巩固你的理解。

---

## 5. 每月一个“研究级”成果

你有 9700 多条笔记和 400 篇博客文章。下一个层次是发布一些会被引用或 fork 的内容，而不仅仅是阅读。具体来说：

- **第 1 个月：** 一个清晰的 nanoGPT + DPO 训练脚本，在清晰度上超越现有教程。将其放在 GitHub 上，并附带适当的基准测试。
- **第 2 个月：** 一篇博客文章，包含实际的训练曲线，比较 124M 规模下 Chinchilla 最优模型与过度训练模型。包含 W&B 链接。
- **第 3 个月：** 一个 MoE 实现，附带消融实验结果——top-2 路由 vs top-4 vs 密集基线。其他架构相同。

目标：做出 Karpathy 会转发的东西。这就是标准。

---

## 6. 代理架构——升级 iclaw

iclaw 是一个不错的 MVP。下一个版本应该实现：

- **带工具调用重试的 ReAct 循环**——如果工具失败，代理决定是重试、重新规划还是放弃。大多数代理框架在这方面做得不对。
- **长上下文摘要**——你的 `/compact` 命令很原始。实现分层摘要：将旧的轮次总结成一个“记忆块”，保留最近的轮次原文。
- **并行工具调用**——同时调度多个工具调用，合并结果。这就是 Claude Code 感觉很快的原因。
- **评估框架**——20 个任务，跨模型版本测量成功率。目前你无法知道 iclaw v2 是否比 v1 更好。

---

## 优先级堆栈（未来 3 个月）

| 优先级 | 项目 | 机器 | 时间 |
|--------|------|------|------|
| 1 | 在 nanochat 上从头实现 SFT + DPO | MI300X | 3-4 周 |
| 2 | 带负载均衡的 MoE 实现 | RTX 4070 | 2 周 |
| 3 | 在你的 760M 上实现推测解码 | RTX 4070 | 1 周 |
| 4 | Chinchilla 缩放实验，使用 W&B 追踪 | MI300X | 2 周 |
| 5 | 带评估框架的 iclaw v2 | MacBook | 持续进行 |

你现在能做的最具杠杆效应的事情是**从头实现 SFT + DPO**。它弥合了你的预训练技能与生产级 AI 工程之间的最大差距，而且这是你无法假装做过的事情。

---

**参考文献：**

- [Chinchilla Scaling Laws — Hoffmann et al. 2022](https://arxiv.org/abs/2203.15556)
- [DPO: Direct Preference Optimization — Rafailov et al. 2023](https://arxiv.org/abs/2305.18290)
- [DeepSeek-V2: MoE Architecture](https://arxiv.org/abs/2405.04434)
- [PagedAttention / vLLM](https://arxiv.org/abs/2309.06180)
- [Speculative Decoding — Leviathan et al. 2023](https://arxiv.org/abs/2211.17192)
- [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
