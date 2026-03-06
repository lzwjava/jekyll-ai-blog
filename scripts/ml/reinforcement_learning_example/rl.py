import torch
import torch.nn as nn
import torch.optim as optim
from transformers import AutoModelForCausalLM, AutoTokenizer

# Sample data
preference_data = [
    (
        "Write a story about a cat.",
        "Whiskers the cat lived in a cozy cottage...",
        "A cat story. The end.",
    ),
]

# Load model and tokenizer
model_name = "gpt2"
policy_model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
device = "cuda" if torch.cuda.is_available() else "cpu"
policy_model.to(device)


# Reward Model
class RewardModel(nn.Module):
    def __init__(self, base_model):
        super().__init__()
        self.base_model = base_model.transformer
        self.v_head = nn.Linear(base_model.config.n_embd, 1)

    def forward(self, input_ids, attention_mask):
        outputs = self.base_model(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_states = outputs.last_hidden_state
        reward = self.v_head(last_hidden_states[:, -1])
        return reward


reward_model = RewardModel(policy_model).to(device)
reward_optimizer = optim.AdamW(reward_model.parameters(), lr=1e-5)
reward_criterion = nn.MarginRankingLoss(margin=1.0)

# Train the Reward Model
num_reward_epochs = 3
for epoch in range(num_reward_epochs):
    for prompt, preferred, less_preferred in preference_data:
        # Tokenize inputs
        preferred_tokens = tokenizer(
            prompt + preferred, return_tensors="pt", truncation=True, max_length=128
        ).to(device)
        less_preferred_tokens = tokenizer(
            prompt + less_preferred,
            return_tensors="pt",
            truncation=True,
            max_length=128,
        ).to(device)

        # Compute rewards, squeezing only the last dimension
        preferred_reward = reward_model(**preferred_tokens).squeeze(-1)  # Shape: [1]
        less_preferred_reward = reward_model(**less_preferred_tokens).squeeze(
            -1
        )  # Shape: [1]

        # Create labels tensor based on batch size
        labels = torch.ones(preferred_reward.size(0)).to(device)  # Shape: [1]

        # Compute loss
        loss = reward_criterion(preferred_reward, less_preferred_reward, labels)

        # Backpropagation
        reward_optimizer.zero_grad()
        loss.backward()
        reward_optimizer.step()

    print(f"Reward Epoch {epoch + 1}, Loss: {loss.item()}")
