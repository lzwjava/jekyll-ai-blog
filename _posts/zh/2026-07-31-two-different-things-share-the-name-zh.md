---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 两个不同的事物同名
translated: true
type: note
---

问题：当前策略蒸馏（经典强化学习意义和在线策略大语言模型意义）处于什么状态？

答案：

两个不同的东西共享同一个名称。既然你自己在训练模型，值得把它们清晰区分开。

**1. 经典策略蒸馏（Rusu 等人，DeepMind 2015）**

训练一个小型网络来匹配大型 DQN 教师（或多个针对特定游戏的教师→一个通用模型）的*动作分布*。损失函数只是教师 softmax(Q/τ) 与学生 softmax(Q/τ) 之间的 KL 散度，而不是直接匹配 Q 值——策略上的交叉熵在经验上优于 Q 值的回归。这基本上就是 Hinton 蒸馏在 Atari 策略上的应用。但这并不是驱动 2026 年讨论的关键——下面的大语言模型变体才是。

**2. 在线策略蒸馏——这才是当前真正热门的东西**

普通 SFT 蒸馏的核心问题：学生在教师的 token 上训练，但在推理时，学生必须基于*自己*生成的前缀进行条件计算。一旦它偏离分布（累积误差/暴露偏差），教师在这些状态上的监督在训练期间从未被看到过。经典的 DAgger 问题。

在线策略蒸馏的解决方案：从**学生**中采样 rollout，然后用**教师**对这些相同的 token 进行评分，最小化反向 KL：

$$
D_{KL}(\pi_\theta \| \pi_T) = -\mathbb{E}_{o \sim \pi_\theta}\left[\log \frac{\pi_T(o|q)}{\pi_\theta(o|q)}\right]
$$

这等价于最大化教师与学生之间对数似然比的期望。由于是反向 KL（寻求模式，避免覆盖质量），梯度只需要教师对学生自身样本的对数概率——不需要教师生成 rollout，不需要奖励模型，不需要 PPO 机制。最小可行循环：

```python
# 每一步，给定提示批次
student_out = student.generate(prompts, sample=True)          # 在线策略：学生自己的 token
with torch.no_grad():
    teacher_logp = teacher.log_prob(student_out)               # 教师对学生 token 进行评分
student_logp = student.log_prob(student_out)

# 每个 token 的反向 KL，教师的对数比率就是隐式奖励
per_token_reward = teacher_logp - student_logp
loss = -(per_token_reward.detach() * student_logp).mean()      # REINFORCE 风格，或者如果你有完整的 logits 访问权限，可以直接对教师 softmax 做密集交叉熵
loss.backward()
```

如果你有完整的教师 logits（相同分词器，白盒），可以完全跳过 REINFORCE，直接做密集的 token 级别 KL——这就是 GKD（Agarwal 等人，2024）的方法，方差低得多，这也是大多数 2026 年论文的基础。

为什么它会从强化学习中抢占预算：在线策略蒸馏已迅速成为大语言模型后训练的核心技术，Qwen3、MiMo 和 GLM-5 都在其后训练流程中采用了在线策略蒸馏，并报告了相较于传统 SFT 和结果奖励强化学习的显著提升。Thinking Machines Lab 以极少的强化学习计算成本复现了 Qwen3 的在线策略蒸馏配方——这就是那篇一直在流传的"在线策略蒸馏"文章/博文。在理论上：在线策略蒸馏已被形式化为密集 KL 约束强化学习的一种特例，其中教师的每个 token 对数比率是一个隐式奖励，将该奖励扩展到其标准权重之外，可以推动学生超越教师自身的表现。最后这部分是反直觉的——过度加权教师信号不仅仅是"克隆教师"，它可以产生一个超越教师的学生，因为奖励倾斜的作用类似于强化学习，拥有一个免费、密集、每个 token 的奖励，而不是每个回合一个标量。

针对你的设置（GPT-2 760M 规模训练运行）的实际框架：在线策略蒸馏提供了强化学习形状的、密集的信用分配，而无需奖励模型或 PPO 的方差/不稳定性——实现成本更低，运行成本更低，属于同一概念家族。DeepSeek-V4 走得最远，完全用多教师在线策略蒸馏取代了其混合强化学习阶段，用于模型整合。如果你正在从任何大型开源教师模型对学生进行蒸馏，将其转化为你自己的小模型，这严格优于普通的基于教师补全的 SFT，而且与你已有的代码相比，只需很小的改动（从你的模型采样，通过反向传播计算与冻结教师前向传播的 KL 散度）。

参考文献：
- [重新思考大语言模型的在线策略蒸馏：现象学、机制与配方](https://arxiv.org/html/2604.13016v1)
- [大语言模型在线策略蒸馏综述](https://arxiv.org/html/2604.00626v3)
- [通过松弛在线策略蒸馏高效扩展推理能力](https://arxiv.org/pdf/2603.11137)
- [Awesome-LLM-On-Policy-Distillation（论文列表）](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation)
- [GKD：广义知识蒸馏（Agarwal 等人，2024）](https://arxiv.org/abs/2306.13649)