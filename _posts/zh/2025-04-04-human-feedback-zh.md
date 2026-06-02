---
audio: false
generated: true
lang: zh
layout: post
title: 人类反馈强化学习详解
translated: true
type: note
---

**基于人类反馈的强化学习（RLHF）** 是一种机器学习技术，用于微调人工智能模型（特别是大语言模型），使其更好地符合人类偏好和指令。RLHF 不依赖预设的奖励函数，而是通过融入人类的直接反馈来指导学习过程。

**RLHF 的重要性**

* **主观性任务**：对于难以用明确规则或数值奖励定义期望结果的任务（如生成创意文本、进行自然对话或生成有用无害的内容），RLHF 表现出色。
* **细微差别与对齐**：它帮助 AI 模型理解并遵循微妙的人类偏好、伦理考量和期望的交互风格。
* **性能提升**：与仅使用传统强化学习或监督学习训练的模型相比，经过 RLHF 训练的模型通常展现出显著提升的性能和用户满意度。

**RLHF 的工作原理（通常分为三个阶段）：**

1.  **预训练与监督微调（SFT）**：
    * 首先，一个基础语言模型在大规模文本和代码数据集上进行预训练，以学习通用的语言理解和生成能力。
    * 然后，通常使用监督学习在一个较小的高质量演示数据集上对该预训练模型进行微调（例如，人类针对提示词写出理想回答）。此步骤帮助模型理解期望输出的格式和风格。

2.  **奖励模型训练**：
    * 这是 RLHF 的关键步骤。训练一个独立的**奖励模型**来预测人类偏好。
    * 向人类标注员展示 SFT 模型（或后续版本）针对同一输入提示生成的不同输出。他们根据各种标准（如帮助性、连贯性、安全性）对这些输出进行排序或评分。
    * 这些偏好数据（例如，"输出 A 优于输出 B"）用于训练奖励模型。奖励模型学习为任何给定的模型输出分配一个标量奖励分数，以反映人类对其的偏好程度。

3.  **强化学习微调**：
    * 使用强化学习进一步微调原始语言模型（从 SFT 模型初始化）。
    * 上一步训练的奖励模型充当环境的奖励函数。
    * RL 代理（即语言模型）生成对提示的回应，奖励模型对这些回应进行评分。
    * RL 算法（通常是近端策略优化 - PPO）更新语言模型的策略（其生成文本的方式），以最大化奖励模型预测的奖励。这鼓励语言模型生成更符合人类偏好的输出。
    * 为防止 RL 微调过度偏离 SFT 模型的行为（可能导致不良结果），通常在 RL 目标中包含一个正则化项（例如，KL 散度惩罚）。

**如何进行 RLHF（简化步骤）：**

1.  **收集人类偏好数据**：
    * 设计与期望 AI 行为相关的提示或任务。
    * 使用当前模型为这些提示生成多个回应。
    * 招募人类标注员比较这些回应并表明他们的偏好（例如，排序、选择最佳或评分）。
    * 将这些数据存储为（提示，偏好回应，次选回应）对或类似格式。

2.  **训练奖励模型**：
    * 为奖励模型选择合适的模型架构（通常是与语言模型相似的基于 Transformer 的模型）。
    * 在收集到的人类偏好数据上训练奖励模型。目标是让奖励模型为人类偏好的回应分配更高的分数。常用的损失函数基于最大化偏好回应和次选回应分数之间的间隔。

3.  **使用强化学习微调语言模型**：
    * 使用 SFT 步骤的权重初始化语言模型（如果执行了该步骤）。
    * 使用强化学习算法（如 PPO）。
    * 对于每个训练步骤：
        * 采样一个提示。
        * 让语言模型生成一个回应。
        * 使用训练好的奖励模型为生成的回应获取奖励分数。
        * 根据奖励信号更新语言模型的参数，以鼓励产生更高奖励的动作（令牌生成）。
        * 包含一个正则化项（例如，KL 散度）以保持更新后的策略接近 SFT 策略。

**代码示例（概念性及简化版，使用 PyTorch）：**

这是一个高度简化的概念性示例，用于说明核心思想。完整的 RLHF 实现要复杂得多，并涉及 Hugging Face Transformers、Accelerate 和 RL 库等。

```python
import torch
import torch.nn as nn
import torch.optim as optim
from transformers import AutoModelForCausalLM, AutoTokenizer

# 假设您已收集人类偏好数据：
# 元组列表: (提示, 偏好回应, 次选回应)
preference_data = [
    ("写一个关于猫的短故事。", "Whiskers the cat lived in a cozy cottage...", "一个关于猫的故事。结束。"),
    ("总结这篇文章：", "文章讨论了...", "文章总结。"),
    # ... 更多数据
]

# 1. 加载预训练语言模型和分词器
model_name = "gpt2"  # 或其他合适的预训练模型
policy_model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
device = "cuda" if torch.cuda.is_available() else "cpu"
policy_model.to(device)

# 2. 定义一个简单的奖励模型
class RewardModel(nn.Module):
    def __init__(self, base_model):
        super().__init__()
        self.base_model = base_model.transformer  # 使用 Transformer 层
        self.v_head = nn.Linear(base_model.config.n_embd, 1)

    def forward(self, input_ids, attention_mask):
        outputs = self.base_model(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_states = outputs.last_hidden_state
        reward = self.v_head(last_hidden_states[:, -1])  # 从最后一个令牌获取奖励
        return reward

reward_model = RewardModel(policy_model)
reward_model.to(device)
reward_optimizer = optim.AdamW(reward_model.parameters(), lr=1e-5)
reward_criterion = nn.MarginRankingLoss(margin=1.0) # 鼓励偏好回应获得更高奖励

# 训练奖励模型
num_reward_epochs = 3
for epoch in range(num_reward_epochs):
    for prompt, preferred, less_preferred in preference_data:
        preferred_tokens = tokenizer(prompt + preferred, return_tensors="pt", truncation=True, max_length=128).to(device)
        less_preferred_tokens = tokenizer(prompt + less_preferred, return_tensors="pt", truncation=True, max_length=128).to(device)

        preferred_reward = reward_model(**preferred_tokens)
        less_preferred_reward = reward_model(**less_preferred_tokens)

        labels = torch.ones(preferred_reward.size(0)).to(device) # 我们希望偏好 > 次选
        loss = reward_criterion(preferred_reward, less_preferred_reward, labels)

        reward_optimizer.zero_grad()
        loss.backward()
        reward_optimizer.step()
    print(f"奖励模型训练轮次 {epoch+1}, 损失: {loss.item()}")

# 3. 强化学习微调（概念性 - PPO 很复杂）
policy_optimizer = optim.AdamW(policy_model.parameters(), lr=5e-6)

num_rl_episodes = 5
for episode in range(num_rl_episodes):
    for prompt in [data[0] for data in preference_data]: # 采样提示
        input_tokens = tokenizer(prompt, return_tensors="pt").to(device)
        output_sequences = policy_model.generate(
            input_tokens.input_ids,
            max_length=60,
            num_return_sequences=1,
            do_sample=True,
            top_k=50,
            top_p=0.95,
        )
        generated_response = tokenizer.decode(output_sequences[0], skip_special_tokens=True)

        response_tokens = tokenizer(prompt + generated_response, return_tensors="pt", truncation=True, max_length=128).to(device)
        reward = reward_model(**response_tokens)

        # （简化版）策略更新 - 实际上 PPO 使用更复杂的方法
        loss = -reward.mean() # 尝试最大化奖励
        policy_optimizer.zero_grad()
        loss.backward()
        policy_optimizer.step()

    print(f"RL 轮次 {episode+1}, 奖励: {reward.item()}, 回应: {generated_response}")

print("RLHF 训练完成！")
```

**RLHF 的主要挑战：**

*   **数据收集**：获取高质量、多样化的人类偏好数据可能成本高昂且耗时。
*   **主观性与偏见**：人类偏好具有主观性，可能包含偏见，这些偏见可能被奖励模型学习。
*   **奖励破解**：RL 代理可能找到利用奖励模型但与真实人类偏好不符的方法。
*   **可扩展性**：将 RLHF 扩展到非常大的模型和数据集需要大量的计算资源和精心的工程实现。
*   **不稳定性**：训练 RLHF 模型可能不稳定，需要仔细调整超参数。

尽管存在这些挑战，RLHF 已被证明是一种使 AI 模型与人类价值观对齐的强大技术，并且是开发像 ChatGPT 这样的先进语言模型的关键组成部分。
