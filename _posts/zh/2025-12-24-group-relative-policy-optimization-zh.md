---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 群体相对策略优化概览
translated: true
type: note
---

Question: What is GRPO in machine learning?

Answer:

**Group Relative Policy Optimization (GRPO)** 是一种在 machine learning 中使用的 reinforcement learning (RL) 算法，特别适用于对 large language models (LLMs) 进行 fine-tuning，以提高其在数学、coding 和复杂问题解决等任务中的 reasoning 能力。

### Key Features and How It Works

- GRPO 是 **Proximal Policy Optimization (PPO)** 的变体，PPO 是一种流行的 RL 算法。
- GRPO 的主要创新在于它消除了对单独的 "critic" 或 value function model 的需求（PPO 需要该模型来估算 future rewards）。这使得 memory 占用和计算成本降低了约 50%。
- GRPO 不使用 critic，而是采用 **group sampling**：对于每个输入 prompt，模型会生成多个输出 responses（例如 64 个或更多）。reward model（或 verifiable reward function）会对每个 response 进行评分。
- **Advantage**（衡量一个 response 的好坏程度）是相对于该 group 计算的：通常通过减去 group rewards 的平均值并除以其 standard deviation 进行归一化。高于 group 平均水平的 responses 获得 positive advantages（被鼓励），低于平均水平的则获得 negative（被抑制）。
- 随后更新 policy（即 LLM 本身），以增加高 advantage responses 的概率，同时使用 clipping 和 KL-divergence penalties 来确保训练的稳定性。

### Advantages Over Traditional Methods

- 更高的 memory 效率，使其适用于大规模训练。
- 在配合 verifiable rewards（例如数学题的正确/错误答案）时非常有效，减少了对 human feedback 或复杂 reward models 的依赖。
- 有助于防止 reward hacking 等问题，并提高 reasoning 任务中的 generalization 能力。

### Origins and Applications

- 首次在 **DeepSeekMath** 论文 (2024) 中提出，用于增强开源 LLMs 的数学推理能力。
- 随着 **DeepSeek-R1** 模型的出现而声名鹊起，在该模型中，它被用于 reinforcement fine-tuning（通常与 supervised fine-tuning 交替进行），以在 reasoning benchmarks 中达到 state-of-the-art 性能。

GRPO 代表了 RLHF (Reinforcement Learning from Human Feedback) 技术的一次高效演进，尤其适用于具有客观评估标准的领域。

References:

- [DeepSeekMath Paper (arXiv)](https://arxiv.org/pdf/2402.03300)
- [DataCamp: What is GRPO?](https://www.datacamp.com/blog/what-is-grpo-group-relative-policy-optimization)
- [Oxen.ai: Why GRPO is Important](https://ghost.oxen.ai/why-grpo-is-important-and-how-it-works/)
- [Medium: The Math Behind DeepSeek GRPO](https://medium.com/@sahin.samia/the-math-behind-deepseek-a-deep-dive-into-group-relative-policy-optimization-grpo-8a75007491ba)
- [Hugging Face Blog: PPO & GRPO Explanation](https://huggingface.co/blog/NormalUhr/grpo)
