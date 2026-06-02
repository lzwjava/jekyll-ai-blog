---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: LoRA Implementation Example with PyTorch
translated: false
type: note
---

Below is a Python code example demonstrating how to implement LoRA (Low-Rank Adaptation) using PyTorch for fine-tuning a simple neural network. This example focuses on adapting a pre-trained linear layer with LoRA, keeping the original weights frozen and introducing low-rank update matrices. The code includes a basic setup with a toy dataset and a minimal training loop to illustrate the concept.

<xaiArtifact artifact_id="1327e99b-24b5-4b0d-9ffd-5b4c2d1472af" artifact_version_id="4053525d-2225-4913-a3b9-b7d66b48daea" title="lora_demo.py" contentType="text/python">
import torch
import torch.nn as nn
import torch.optim as optim

# Define LoRA layer
class LoRALayer(nn.Module):
    def __init__(self, in_features, out_features, rank=4):
        super(LoRALayer, self).__init__()
        # Original frozen weights
        self.linear = nn.Linear(in_features, out_features)
        self.linear.weight.requires_grad = False  # Freeze original weights
        # LoRA parameters: low-rank matrices A and B
        self.lora_A = nn.Parameter(torch.randn(in_features, rank))
        self.lora_B = nn.Parameter(torch.randn(rank, out_features))
        self.scaling = 1.0  # Scaling factor for LoRA updates

    def forward(self, x):
        # Original linear transformation + LoRA adjustment
        original = self.linear(x)
        lora_adjustment = self.scaling * torch.matmul(torch.matmul(x, self.lora_A), self.lora_B)
        return original + lora_adjustment

# Toy dataset for demonstration
def create_toy_dataset(n_samples=1000):
    X = torch.randn(n_samples, 64)  # Random input features
    y = torch.randn(n_samples, 10)  # Random target outputs
    return X, y

# Training function
def train_model(model, X, y, epochs=10, lr=0.01):
    criterion = nn.MSELoss()
    optimizer = optim.Adam([param for param in model.parameters() if param.requires_grad], lr=lr)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

# Main execution
def main():
    # Set random seed for reproducibility
    torch.manual_seed(42)

    # Create toy dataset
    X, y = create_toy_dataset()

    # Initialize model with LoRA
    model = LoRALayer(in_features=64, out_features=10, rank=4)

    # Count trainable parameters
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Trainable parameters: {trainable_params}")
    print(f"Total parameters: {total_params}")

    # Train the model
    train_model(model, X, y)

if __name__ == "__main__":
    main()
</xaiArtifact>

This code defines a `LoRALayer` that wraps a standard linear layer with low-rank adaptation matrices (`lora_A` and `lora_B`). The original weights are frozen, and only the LoRA parameters are updated during training. The toy dataset and training loop demonstrate how LoRA reduces the number of trainable parameters while still allowing fine-tuning. You can run this code with PyTorch installed to see the training process and parameter efficiency in action.

[LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
