---
audio: false
generated: true
lang: en
layout: post
title: Human Feedback Reinforcement Learning (RLHF) Explained
translated: false
type: note
---

**Reinforcement Learning from Human Feedback (RLHF)** is a machine learning technique used to fine-tune AI models, particularly large language models (LLMs), to better align with human preferences and instructions. Instead of relying solely on predefined reward functions, RLHF incorporates direct feedback from humans to guide the learning process.

**Why is RLHF Important?**

* **Subjective Tasks:** RLHF excels in tasks where the desired outcome is difficult to define with explicit rules or numerical rewards, such as generating creative text, engaging in natural conversations, or producing helpful and harmless content.
* **Nuance and Alignment:** It helps AI models understand and adhere to subtle human preferences, ethical considerations, and desired interaction styles.
* **Improved Performance:** Models trained with RLHF often demonstrate significantly improved performance and user satisfaction compared to those trained solely with traditional reinforcement learning or supervised learning.

**How RLHF Works (Typically in three stages):**

1. **Pre-training and Supervised Fine-tuning (SFT):**
    * A base language model is first pre-trained on a massive dataset of text and code to learn general language understanding and generation.
    * This pre-trained model is then often fine-tuned using supervised learning on a smaller dataset of high-quality demonstrations of the desired behavior (e.g., humans writing ideal responses to prompts). This step helps the model understand the format and style of the expected outputs.

2. **Reward Model Training:**
    * This is a crucial step in RLHF. A separate **reward model** is trained to predict human preferences.
    * Human annotators are presented with different outputs from the SFT model (or a later version) for the same input prompt. They rank or rate these outputs based on various criteria (e.g., helpfulness, coherence, safety).
    * This preference data (e.g., "output A is better than output B") is used to train the reward model. The reward model learns to assign a scalar reward score to any given model output, reflecting how much a human would prefer it.

3. **Reinforcement Learning Fine-tuning:**
    * The original language model (initialized from the SFT model) is further fine-tuned using reinforcement learning.
    * The reward model trained in the previous step serves as the environment's reward function.
    * The RL agent (the language model) generates responses to prompts, and the reward model scores these responses.
    * The RL algorithm (often Proximal Policy Optimization - PPO) updates the language model's policy (how it generates text) to maximize the rewards predicted by the reward model. This encourages the language model to generate outputs that are more aligned with human preferences.
    * To prevent the RL fine-tuning from deviating too far from the SFT model's behavior (which might lead to undesirable outcomes), a regularization term (e.g., KL divergence penalty) is often included in the RL objective.

**How to Do RLHF (Simplified Steps):**

1. **Collect Human Preference Data:**
    * Design prompts or tasks relevant to your desired AI behavior.
    * Generate multiple responses to these prompts using your current model.
    * Recruit human annotators to compare these responses and indicate their preferences (e.g., rank them, choose the best, or rate them).
    * Store this data as pairs of (prompt, preferred response, less preferred response) or similar formats.

2. **Train a Reward Model:**
    * Choose a suitable model architecture for your reward model (often a transformer-based model similar to the language model).
    * Train the reward model on the collected human preference data. The goal is for the reward model to assign higher scores to the responses that humans preferred. A common loss function used is based on maximizing the margin between the scores of preferred and less preferred responses.

3. **Fine-tune the Language Model with Reinforcement Learning:**
    * Initialize your language model with the weights from the SFT step (if you performed one).
    * Use a reinforcement learning algorithm (like PPO).
    * For each training step:
        * Sample a prompt.
        * Have the language model generate a response.
        * Use the trained reward model to get a reward score for the generated response.
        * Update the language model's parameters based on the reward signal to encourage actions (token generation) that lead to higher rewards.
        * Include a regularization term (e.g., KL divergence) to keep the updated policy close to the SFT policy.

**Code Example (Conceptual and Simplified using PyTorch):**

This is a highly simplified conceptual example to illustrate the core ideas. A full RLHF implementation is significantly more complex and involves libraries like Hugging Face Transformers, Accelerate, and RL libraries.

```python
import torch
import torch.nn as nn
import torch.optim as optim
from transformers import AutoModelForCausalLM, AutoTokenizer

# Assume you have collected human preference data:
# List of tuples: (prompt, preferred_response, less_preferred_response)
preference_data = [
    ("Write a short story about a cat.", "Whiskers the cat lived in a cozy cottage...", "A cat story. The end."),
    ("Summarize this article:", "The article discusses...", "Article summary."),
    # ... more data
]

# 1. Load pre-trained language model and tokenizer
model_name = "gpt2"  # Or another suitable pre-trained model
policy_model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
device = "cuda" if torch.cuda.is_available() else "cpu"
policy_model.to(device)

# 2. Define a simple Reward Model
class RewardModel(nn.Module):
    def __init__(self, base_model):
        super().__init__()
        self.base_model = base_model.transformer  # Use the transformer layers
        self.v_head = nn.Linear(base_model.config.n_embd, 1)

    def forward(self, input_ids, attention_mask):
        outputs = self.base_model(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_states = outputs.last_hidden_state
        reward = self.v_head(last_hidden_states[:, -1])  # Get reward from the last token
        return reward

reward_model = RewardModel(policy_model)
reward_model.to(device)
reward_optimizer = optim.AdamW(reward_model.parameters(), lr=1e-5)
reward_criterion = nn.MarginRankingLoss(margin=1.0) # Encourage higher reward for preferred

# Train the Reward Model
num_reward_epochs = 3
for epoch in range(num_reward_epochs):
    for prompt, preferred, less_preferred in preference_data:
        preferred_tokens = tokenizer(prompt + preferred, return_tensors="pt", truncation=True, max_length=128).to(device)
        less_preferred_tokens = tokenizer(prompt + less_preferred, return_tensors="pt", truncation=True, max_length=128).to(device)

        preferred_reward = reward_model(**preferred_tokens)
        less_preferred_reward = reward_model(**less_preferred_tokens)

        labels = torch.ones(preferred_reward.size(0)).to(device) # We want preferred > less preferred
        loss = reward_criterion(preferred_reward, less_preferred_reward, labels)

        reward_optimizer.zero_grad()
        loss.backward()
        reward_optimizer.step()
    print(f"Reward Epoch {epoch+1}, Loss: {loss.item()}")

# 3. Reinforcement Learning Fine-tuning (Conceptual - PPO is complex)
policy_optimizer = optim.AdamW(policy_model.parameters(), lr=5e-6)

num_rl_episodes = 5
for episode in range(num_rl_episodes):
    for prompt in [data[0] for data in preference_data]: # Sample prompts
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

        # (Simplified) Policy Update - In reality, PPO uses more sophisticated methods
        loss = -reward.mean() # Try to maximize reward
        policy_optimizer.zero_grad()
        loss.backward()
        policy_optimizer.step()

    print(f"RL Episode {episode+1}, Reward: {reward.item()}, Response: {generated_response}")

print("RLHF Training Done!")
```

**Key Challenges in RLHF:**

* **Data Collection:** Obtaining high-quality and diverse human preference data can be expensive and time-consuming.
* **Subjectivity and Bias:** Human preferences can be subjective and may contain biases, which can be learned by the reward model.
* **Reward Hacking:** The RL agent might find ways to exploit the reward model that don't align with true human preferences.
* **Scalability:** Scaling RLHF to very large models and datasets requires significant computational resources and careful engineering.
* **Instability:** Training RLHF models can be unstable and require careful hyperparameter tuning.

Despite these challenges, RLHF has proven to be a powerful technique for aligning AI models with human values and is a key component in the development of state-of-the-art language models like ChatGPT and others.
