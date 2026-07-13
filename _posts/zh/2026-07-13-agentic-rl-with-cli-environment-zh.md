---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于CLI环境的智能体强化学习
translated: true
type: note
---

Question: 鉴于我目前的项目组合（从头预训练 GPT-2 124M/760M、nanoGPT 分支、DeepSeek-V2-Lite MoE 推理、代理 CLI 工具 ww/iclaw/zz、大量生产级 LLM 使用），以及我朋友的框架（① 逆向工程目标公司需求，② 选择一个前沿方向然后找到对应公司）——我该如何在下一季度选择一个研究方向，而不是分散在 MoE/KL/RL/MLA/Rotary/Muon/证书上？

Answer:

你的两个“朋友”策略其实并不冲突——它们会指向同一个答案，基于你已经构建的内容。不要在这两者之间选择，而是找到它们的交集。

**交集：基于智能体的 RL 后训练，使用你自己预训练的模型 + 你自己的 CLI 工具作为环境。**

理由：

- 路径 ①（公司驱动）：你已经在付费作为 API 客户使用的每个中国实验室（小米 MIMO、MiniMax、DeepSeek 系列）都在招聘后训练/RL 岗位，而不是预训练。预训练岗位在行业范围内几乎冻结；RLHF/RLVR/agentic-RL 团队正在扩张。你的 token 消费数据本身就表明你已经是那些公司的重度用户，而这些公司目前的招聘瓶颈正是能够调试奖励黑客和 KL 爆炸的 RL 工程师。
- 路径 ②（前沿驱动）：2026 年的前沿方向是 agentic RL——通过 RL 训练模型正确使用工具，而不仅仅是 SFT 模仿工具轨迹。你已经构建了这个环境却没有意识到：`iclaw` 和 `ww` 就是字面意义上的工具执行框架。这占了 RL 环境的 80%（env.step()、退出码/测试通过/diff 正确性奖励）。

所以：不要把“MoE”、“KL”、“RL”、“MLA”、“Rotary/Muon”当作五个独立的任务。将它们合并成一个实验：**使用你自己的智能体的 shell/工具调用任务作为环境，在你的 GPT-2 760M 上运行 GRPO，并加上 KL-to-reference 项。**

具体的决定，而不是“看情况”：在接下来的 90 天内按顺序完成以下工作：

1. **第 1-2 周——先做奖励和环境，而不是算法。** 你的模型太小/训练不足，无法处理真正的编码任务，所以选择一个狭窄的可验证任务：给定一个损坏的 shell 命令或一个失败的 Python 片段（从你的 `zz` 数据集脚本中提取），如果模型的工具调用修复了它（测试通过），奖励 = 1，否则为 0。直接将其连接到 `iclaw` 的工具调用循环——你已经有了这个框架，不需要重做。

2. **第 2-4 周——从零开始实现带显式 KL 的 GRPO，而不是使用 TRL。** 自己编写损失函数，这样你才能真正理解它（Karpathy 风格，没有库的魔法）：

```python
import torch, torch.nn.functional as F

def grpo_loss(logp_new, logp_old, logp_ref, advantages, mask, eps=0.2, beta=0.04):
    # logp_*: (B, T) 当前/旧/参考策略下的每个 token 的 log-prob
    # advantages: (B,) 组归一化奖励，广播到 (B, T)
    ratio = torch.exp(logp_new - logp_old)                     # (B, T)
    unclipped = ratio * advantages
    clipped = torch.clamp(ratio, 1 - eps, 1 + eps) * advantages
    pg_loss = -torch.min(unclipped, clipped)

    # k3 估计器（低方差、无偏 KL 近似），每个 token
    log_ratio_ref = logp_ref - logp_new
    kl = torch.exp(log_ratio_ref) - log_ratio_ref - 1          # >= 0

    per_token_loss = (pg_loss + beta * kl) * mask
    return per_token_loss.sum() / mask.sum()

def group_advantages(rewards, group_size):
    r = rewards.view(-1, group_size)
    mean, std = r.mean(dim=1, keepdim=True), r.std(dim=1, keepdim=True) + 1e-4
    return ((r - mean) / std).view(-1)
```

这里的 KL 项正是 DeepSeekMath 的 k3 估计器——它是 KL(π_θ‖π_ref) 的无偏低方差 MC 估计器，也是你正准备去读论文的那个。当两个策略接近时，它是一个低方差、几乎无偏的 KL 散度蒙特卡洛估计器。值得注意：最近的开源工作如 Open-Reasoner-Zero 表明 KL 项对于 GRPO 并非严格必要，TRL 现在默认 β=0——所以把 KL 当作一个稳定性旋钮来消融，而不是一个神圣的项。在你的 760M 模型上做那个消融（β=0 vs β=0.04）比再读五篇相关论文更值得花一周时间。

3. **第 4-8 周——在线策略蒸馏，这实际上是你列表中的第 2 项，这里可以免费得到。** 一旦 GRPO 运行起来，将 RL 改进后的策略蒸馏到一个更小/更快的在线学生中（学生采样，教师评分/重排序，学生更新），使用相同的奖励信号。这与第 2 步的基础设施相同，只是教师 = 760M / 学生 = 124M。

4. **只有当这些完成后——把 MLA/MoE 作为架构替换，而不是一个新项目。** 你已经在 `zz` 中有了 DeepSeek-V2-Lite 推理脚本。不要抽象地“学习 MoE”——实现一个最小的 MLA + 共享/专家路由 MoE 块，将其替换到你的 nanoGPT 分支中，用 124M 配置重新训练，比较困惑度和吞吐量与原始注意力机制的差异。一旦你不再同时切换背景到 RL 理论，这只是一个 3-4 天的练习。

本季度明确降低优先级的事项：Rotary 和 Muon 是即插即用的——你可以在一个下午把 RoPE 加到 nanoGPT 中，并在无聊时用配置标志把 AdamW 换成 Muon，它们不值得“聚焦”地位。NCP-GENL 证书（九月）——保持为背景任务，而不是研究方向；这是资历认证，不是研究。“追赶所有 2022 年后的论文”——停止将其作为独立活动；当你执行上述每一步时，你会提取你实际需要的 5-10 篇论文（GRPO、DAPO、DeepSeek-V2 MLA、DeepSeek-V3 MoE 路由）。

回答你朋友的单句总结：**“基于智能体的 RL 后训练，带有显式 KL 控制，使用我自己的预训练模型和我自己的工具调用代理作为环境——因为这是我已经在使用的实验室正在招聘的方向，也是我唯一已经拥有整个栈而不是重新实现别人成果的前沿方向。”**

参考文献：

- [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO source paper)](https://arxiv.org/pdf/2402.03300)
- [Deep Dive into GRPO — implementation walkthrough](https://medium.com/@abhirupgupta123/deep-dive-into-grpo-03826359836c)
- [An unusual look at the KL-divergence term in DeepSeek R1 (k3 estimator explained)](https://aiwithmike.substack.com/p/an-unusual-look-of-the-kl-divergence)
- [TRL GRPO Trainer docs — β=0 default, KL ablation context](https://huggingface.co/docs/trl/main/en/grpo_trainer)
- [RLHF Book, ch. 6.3.6 — GRPO KL term derivation](https://arxiv.org/pdf/2504.12501)
- [Your own portfolio](https://lzwjava.github.io/ai-portfolio-en)
