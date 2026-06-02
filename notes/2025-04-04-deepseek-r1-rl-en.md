---
audio: false
generated: true
lang: en
layout: post
title: DeepSeek R1
translated: false
type: note
---

DeepSeek R1 employs a novel approach to reinforcement learning (RL) that significantly emphasizes **reasoning capabilities** in large language models (LLMs). Their technique differs from traditional Reinforcement Learning from Human Feedback (RLHF) in several key aspects.

Here's a breakdown of the techniques DeepSeek used in R1's reinforcement learning:

**1. Pure Reinforcement Learning (RL) for Initial Reasoning (DeepSeek-R1-Zero):**

* **No Initial Supervised Fine-tuning (SFT) on Instructions:** Unlike many LLMs that first undergo SFT on human-written instructions, DeepSeek-R1-Zero was trained with **pure RL** directly on the base model (DeepSeek-V3-Base).
* **Group Relative Policy Optimization (GRPO):** They utilized GRPO as their core RL algorithm. GRPO is designed to be more efficient than Proximal Policy Optimization (PPO) by eliminating the need for a separate critic network. It estimates baseline rewards by comparing a group of generated outputs, assigning relative scores based on their quality. This encourages the model to generate better responses compared to its own previous attempts.
* **Rule-Based Reward System:** Instead of relying solely on human preferences for the initial RL phase, DeepSeek-R1-Zero used a **rule-based reward system**. This system primarily focused on:
    * **Accuracy Rewards:** Rewarding the model for providing correct answers, especially in tasks with verifiable solutions like math problems (checking if the final answer is correct).
    * **Format Rewards:** Rewarding the model for adhering to a specific output format, particularly using `<think>` and `</think>` tags to enclose its reasoning process. This encouraged the emergence of chain-of-thought reasoning.
* **Emergent Reasoning Behaviors:** This pure RL approach allowed DeepSeek-R1-Zero to naturally develop impressive reasoning skills, including self-verification, reflection, and the generation of long chain-of-thought explanations, without explicit human demonstrations for these behaviors.

**2. Multi-Stage Training for Enhanced Readability and General Capabilities (DeepSeek-R1):**

To address the limitations of DeepSeek-R1-Zero (like poor readability and language mixing), DeepSeek-R1 employed a more comprehensive multi-stage training pipeline:

* **Cold-Start Data Fine-tuning:** Before the main RL phase, the base model was fine-tuned on a small dataset of high-quality, human-written (or generated and refined) long chain-of-thought reasoning examples. This "cold start" data helped guide the model towards producing more readable and coherent reasoning steps.
* **Reasoning-Oriented Reinforcement Learning (Second RL Stage):** The model then underwent a second phase of large-scale RL (similar to DeepSeek-R1-Zero) but with an additional **language consistency reward**. This reward penalized the model for mixing languages within its reasoning process.
* **Supervised Fine-tuning (SFT):** After the reasoning-oriented RL, the model was further fine-tuned on a diverse dataset that included both reasoning data (synthesized using rejection sampling from the RL model, judged by DeepSeek-V3) and general non-reasoning data (augmented with chain-of-thought). This SFT stage aimed to improve the model's helpfulness and harmlessness while preserving its strong reasoning abilities.
* **RL for All Scenarios (Third RL Stage):** A final RL phase was conducted using prompts from a wider range of scenarios to further refine the model's overall capabilities and alignment with desired behaviors.

**Key Differences from Traditional RLHF:**

* **Reduced Reliance on Extensive Human Preference Data:** While some human evaluation might have been involved in judging the quality of synthesized data, the core RL training in DeepSeek-R1 heavily leveraged rule-based rewards, especially in the initial stages. This reduces the cost and complexity of collecting large amounts of direct human preference comparisons.
* **Emphasis on Emergent Reasoning:** The pure RL approach aimed to incentivize the model to *discover* effective reasoning strategies on its own, rather than solely learning from human-provided examples of reasoning.
* **Multi-Stage Approach:** DeepSeek's pipeline involves a carefully orchestrated sequence of pre-training, targeted fine-tuning, and multiple RL stages with different reward signals to achieve both strong reasoning and general language capabilities.

**Code to Show Reinforcement Learning (Conceptual and Simplified):**

It's challenging to provide a direct, runnable code example that fully replicates DeepSeek's RL training process due to its complexity and scale. However, the following conceptual PyTorch-like snippet illustrates the core idea of GRPO and a rule-based reward:

```python
import torch
import torch.optim as optim
from transformers import AutoModelForCausalLM, AutoTokenizer

# Assume you have a pre-trained language model and tokenizer
model_name = "gpt2"  # Replace with a more suitable base model
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
    # Simplified example for a math problem: "What is 2 + 2?"
    if "2 + 2" in response and "4" in response:
        return 1.0
    else:
        return 0.0

def calculate_format_reward(response):
    if "<think>" in response and "</think>" in response:
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

    # Simplified GRPO-like update: Encourage higher reward responses
    best_reward_index = torch.argmax(rewards)
    best_response = responses[best_reward_index]
    inputs = tokenizer(prompt + best_response, return_tensors="pt").to(device)
    outputs = policy_model(**inputs, labels=inputs.input_ids)
    loss = outputs.loss
    loss.backward()
    optimizer.step()
    return loss.item(), best_response, rewards.tolist()

# Training loop (very simplified)
num_episodes = 10
training_prompts = ["Solve: 2 + 2 = ?", "Explain the concept of gravity <think>", "Write a short story about a cat."]

for episode in range(num_episodes):
    prompt = training_prompts[episode % len(training_prompts)]
    loss, best_response, rewards = train_step(prompt)
    print(f"Episode {episode+1}, Loss: {loss:.4f}, Best Response: '{best_response}', Rewards: {rewards}")

print("Simplified RL Training Done!")
```

**Important Notes on the Code:**

* **Simplification:** This code is a highly simplified illustration. Real RL training for LLMs involves much more complex algorithms (like the full GRPO implementation), reward functions, handling of action spaces, exploration strategies, and stability techniques.
* **Reward Function:** The reward functions here are extremely basic and task-specific. In reality, they would be more nuanced and potentially involve other AI models as reward predictors.
* **GRPO Implementation:** The policy update in this example is a very rough approximation of GRPO. The actual GRPO algorithm involves comparing probabilities of generated tokens within a group and updating the policy based on relative performance.
* **Scale:** Training a model like DeepSeek-R1 requires massive computational resources and datasets, far beyond what can be demonstrated in a simple code snippet.

This explanation and the conceptual code provide a foundational understanding of the innovative reinforcement learning techniques employed by DeepSeek in the development of their R1 model, particularly their focus on pure RL and rule-based rewards for fostering strong reasoning capabilities.
