---
audio: false
generated: true
lang: zh
layout: post
title: DeepSeek R1
translated: true
type: note
---

DeepSeek R1采用了一种新颖的强化学习方法，显著提升了大型语言模型的**推理能力**。该技术与传统的基于人类反馈的强化学习在多个关键方面存在差异。

以下是DeepSeek在R1强化学习中使用的技术解析：

**1. 纯强化学习实现初始推理能力（DeepSeek-R1-Zero）：**

* **无指令监督微调初始化**：与多数先通过人类编写指令进行监督微调的LLM不同，DeepSeek-R1-Zero直接在基础模型上采用**纯强化学习**进行训练
* **群体相对策略优化**：团队采用GRPO作为核心RL算法。相比近端策略优化，GRPO通过消除独立的价值网络需求实现了更高效率。该算法通过比较生成输出的群体质量分配相对分数，激励模型产生优于自身先前尝试的回应
* **基于规则的奖励系统**：在初始RL阶段，DeepSeek-R1-Zero使用**基于规则的奖励系统**而非单纯依赖人类偏好，主要聚焦于：
    * **准确性奖励**：对提供正确答案的模型进行奖励，特别是在数学题等可验证解决方案的任务中
    * **格式奖励**：对遵循特定输出格式的模型进行奖励，特别是使用``标签包裹推理过程，以此促进思维链推理的涌现
* **涌现的推理行为**：这种纯RL方法使DeepSeek-R1-Zero自然发展出令人印象深刻的推理技能，包括自我验证、反思和生成长思维链解释的能力，而无需人类对这些行为进行显式示范

**2. 多阶段训练增强可读性与通用能力（DeepSeek-R1）：**

为解决DeepSeek-R1-Zero的局限性（如可读性差和语言混用），DeepSeek-R1采用了更全面的多阶段训练流程：

* **冷启动数据微调**：在主RL阶段前，基础模型在高质量人类撰写的长思维链推理示例小数据集上进行微调。这种"冷启动"数据引导模型产生更可读、更连贯的推理步骤
* **面向推理的强化学习**：模型随后进行大规模RL第二阶段训练，但额外增加了**语言一致性奖励**，对推理过程中混用语言的行为进行惩罚
* **监督微调**：在推理导向RL后，模型在包含推理数据和通用非推理数据的多样化数据集上进一步微调，旨在提升模型的有用性和无害性，同时保留其强大的推理能力
* **全场景强化学习**：最后使用更广泛场景的提示词进行第三阶段RL训练，以进一步完善模型的整体能力与行为对齐

**与传统RLHF的关键差异：**

* **降低对人类偏好数据的依赖**：虽然合成数据质量评估可能涉及人工评判，但DeepSeek-R1的核心RL训练在初始阶段大量利用基于规则的奖励，这降低了收集大量直接人类偏好对比的成本和复杂度
* **强调涌现推理**：纯RL方法激励模型自主发现有效推理策略，而非仅从人类提供的推理示例中学习
* **多阶段方法**：DeepSeek的流程包含精心设计的预训练、定向微调和具有不同奖励信号的多阶段RL序列，以实现强大的推理和通用语言能力

**强化学习概念代码示例（简化版）：**

由于DeepSeek的RL训练过程复杂度高、规模大，很难提供直接可运行的完整代码示例。以下概念性PyTorch风格代码片段展示了GRPO和基于规则奖励的核心思想：

```python
import torch
import torch.optim as optim
from transformers import AutoModelForCausalLM, AutoTokenizer

# 假设已有预训练语言模型和分词器
model_name = "gpt2"  # 可替换为更合适的基础模型
policy_model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
optimizer = optim.AdamW(policy_model.parameters(), lr=5e-6)
device = "cuda" if torch.cuda.is_available() else "cpu"
policy_model.to(device)

def generate_responses(prompt, num_responses=4, max_length=128):
    input_tokens = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = policy_model.generate(
        input_tokens.input_ids,
        max_length=max_length,
        num_return_sequences=num_responses,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        pad_token_id=tokenizer.eos_token_id
    )
    responses = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    return responses

def calculate_accuracy_reward(response):
    # 数学问题简化示例："2+2等于多少？"
    if "2 + 2" in response and "4" in response:
        return 1.0
    else:
        return 0.0

def calculate_format_reward(response):
    if "" in response:
        return 0.5
    else:
        return 0.0

def calculate_combined_reward(response):
    accuracy_reward = calculate_accuracy_reward(response)
    format_reward = calculate_format_reward(response)
    return accuracy_reward + format_reward

def train_step(prompt, num_samples=4):
    optimizer.zero_grad()
    responses = generate_responses(prompt, num_samples=num_samples)
    rewards = torch.tensor([calculate_combined_reward(resp) for resp in responses]).float().to(device)

    # 简化版GRPO更新：激励高奖励响应
    best_reward_index = torch.argmax(rewards)
    best_response = responses[best_reward_index]
    inputs = tokenizer(prompt + best_response, return_tensors="pt").to(device)
    outputs = policy_model(**inputs, labels=inputs.input_ids)
    loss = outputs.loss
    loss.backward()
    optimizer.step()
    return loss.item(), best_response, rewards.tolist()

# 训练循环（极度简化）
num_episodes = 10
training_prompts = ["求解：2 + 2 = ?", "解释重力概念
