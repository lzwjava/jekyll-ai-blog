---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: LoRA Code Breakdown and Explanation
translated: false
type: note
---

I'll break down the LoRA demo code into key pieces, explaining each part in detail before moving to the next. This will help illustrate how LoRA works in a clear, step-by-step manner. The code is based on the previous example, using PyTorch to implement LoRA for a simple linear layer.

### Code Piece 1: LoRA Layer Definition
```python
import torch
import torch.nn as nn

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
```

#### Explanation
This piece defines the `LoRALayer` class, which implements the LoRA technique. Here's what's happening:

- **Imports and Class Setup**: We import PyTorch (`torch`) and its neural network module (`nn`). The `LoRALayer` class inherits from `nn.Module`, making it a PyTorch module that can be integrated into larger models.
- **Original Linear Layer**: `self.linear = nn.Linear(in_features, out_features)` creates a standard linear layer (like a fully connected layer in a neural network) with `in_features` inputs and `out_features` outputs. This represents the pre-trained weights we want to adapt.
- **Freezing Weights**: `self.linear.weight.requires_grad = False` freezes the original weights of the linear layer, ensuring they aren't updated during training. This is key to LoRA's efficiency, as it avoids modifying the large pre-trained model.
- **LoRA Parameters**: `self.lora_A` and `self.lora_B` are low-rank matrices. `lora_A` has shape `(in_features, rank)`, and `lora_B` has shape `(rank, out_features)`. The `rank` parameter (default=4) controls the size of these matrices, keeping them much smaller than the original weight matrix (shape `in_features x out_features`). These matrices are trainable (`nn.Parameter`) and initialized with random values (`torch.randn`).
- **Scaling Factor**: `self.scaling = 1.0` is a hyperparameter to scale the LoRA adjustment, allowing fine-tuning of the adaptation strength.

This setup ensures that only the small `lora_A` and `lora_B` matrices are updated during training, drastically reducing the number of trainable parameters.

---

### Code Piece 2: LoRA Forward Pass
```python
    def forward(self, x):
        # Original linear transformation + LoRA adjustment
        original = self.linear(x)
        lora_adjustment = self.scaling * torch.matmul(torch.matmul(x, self.lora_A), self.lora_B)
        return original + lora_adjustment
```

#### Explanation
This piece defines the forward pass of the `LoRALayer`, which computes the output of the layer:

- **Input**: The input `x` is a tensor of shape `(batch_size, in_features)`, representing a batch of input data.
- **Original Output**: `original = self.linear(x)` computes the output of the frozen linear layer, applying the pre-trained weights to the input.
- **LoRA Adjustment**: The term `torch.matmul(torch.matmul(x, self.lora_A), self.lora_B)` computes the low-rank adaptation. First, `x` is multiplied by `lora_A` (shape `in_features x rank`), producing a tensor of shape `(batch_size, rank)`. Then, this is multiplied by `lora_B` (shape `rank x out_features`), yielding a tensor of shape `(batch_size, out_features)`—the same shape as the original output. This adjustment represents the task-specific update.
- **Scaling and Combination**: The adjustment is scaled by `self.scaling` and added to the original output, producing the final output. This ensures the model retains the pre-trained knowledge while incorporating task-specific adaptations.

The low-rank structure (`rank` is small, e.g., 4) ensures the adjustment is computationally cheap and parameter-efficient compared to updating the full weight matrix.

---

### Code Piece 3: Toy Dataset and Training
```python
def create_toy_dataset(n_samples=1000):
    X = torch.randn(n_samples, 64)  # Random input features
    y = torch.randn(n_samples, 10)  # Random target outputs
    return X, y

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
```

#### Explanation
This piece creates a toy dataset and trains the LoRA-adapted model:

- **Toy Dataset**: The `create_toy_dataset` function generates synthetic data for demonstration. `X` is a tensor of shape `(1000, 64)` (1000 samples, 64 features), and `y` is a tensor of shape `(1000, 10)` (1000 samples, 10 output dimensions). These are random tensors to simulate input-output pairs.
- **Training Function**: The `train_model` function sets up a simple training loop:
  - **Loss Function**: `nn.MSELoss()` defines mean squared error as the loss, suitable for this regression-like toy task.
  - **Optimizer**: `optim.Adam` optimizes only the trainable parameters (`param.requires_grad` is `True`), which are `lora_A` and `lora_B`. The frozen `linear.weight` is excluded, ensuring efficiency.
  - **Training Loop**: For each epoch, the model computes outputs, calculates the loss, performs backpropagation (`loss.backward()`), and updates the LoRA parameters (`optimizer.step()`). The loss is printed to monitor training progress.

This setup demonstrates how LoRA fine-tunes only the low-rank matrices, keeping the process lightweight.

---

### Code Piece 4: Main Execution and Parameter Count
```python
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
```

#### Explanation
This piece ties everything together and highlights LoRA's efficiency:

- **Random Seed**: `torch.manual_seed(42)` ensures reproducibility of random initializations.
- **Dataset and Model**: The toy dataset is created, and a `LoRALayer` is initialized with `in_features=64`, `out_features=10`, and `rank=4`.
- **Parameter Count**: The code calculates:
  - **Trainable parameters**: Only `lora_A` (64 × 4 = 256) and `lora_B` (4 × 10 = 40), totaling 296 parameters.
  - **Total parameters**: Includes the frozen `linear.weight` (64 × 10 = 640) and `linear.bias` (10), plus LoRA parameters, totaling 946.
  - This shows LoRA's efficiency: only ~31% (296/946) of parameters are trainable, compared to 100% in full fine-tuning.
- **Training**: The `train_model` function is called to fine-tune the LoRA parameters on the toy dataset.

When you run this, you'll see the number of trainable parameters is much smaller than the total, and the model trains quickly due to the low-rank updates.

---

### Running the Code
To run this, you need PyTorch installed (`pip install torch`). Save the full code as a `.py` file and execute it. The output will show the number of parameters and the training loss over 10 epochs, demonstrating LoRA's efficiency in fine-tuning.

[LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)

Let me know if you'd like to dive deeper into any part or modify the example!
