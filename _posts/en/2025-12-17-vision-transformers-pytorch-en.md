---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Vision Transformers Explained with PyTorch
translated: false
type: note
---

Question: How do Vision Transformers work? Provide some PyTorch examples.

Answer: 

Vision Transformers (ViT) apply the Transformer architecture, originally designed for natural language processing, to computer vision tasks like image classification. Unlike convolutional neural networks (CNNs), which use convolutions to capture local spatial features, ViTs treat images as sequences of patches and rely on self-attention to model global relationships.

### Key Steps in How ViT Works

1. **Patch Embedding**:
   - The input image (e.g., shape `3 × H × W`) is divided into fixed-size patches (typically 16×16 or 32×32 pixels).
   - Each patch is flattened and linearly projected to a fixed embedding dimension `D` (e.g., 768).
   - This results in a sequence of `N = (H × W) / P²` patch embeddings, where `P` is the patch size.

2. **Adding a Classification Token ([CLS])**:
   - A learnable `[CLS]` token is prepended to the sequence. Its final representation after processing is used for classification.

3. **Positional Embeddings**:
   - Learnable (or fixed) positional embeddings are added to the patch embeddings to retain spatial information, since self-attention is permutation-invariant.

4. **Transformer Encoder**:
   - The sequence (length `N+1`) is fed into a stack of Transformer blocks.
   - Each block consists of:
     - Layer Normalization
     - Multi-Head Self-Attention (MHSA): Computes attention across all patches globally.
     - Layer Normalization
     - MLP (Feed-Forward Network): Two linear layers with GELU activation and dropout.
     - Residual connections around both sub-layers.

5. **Classification Head**:
   - The output corresponding to the `[CLS]` token is passed through a linear layer (or MLP) to produce class logits.

ViTs excel with large datasets and pre-training (e.g., on ImageNet), often outperforming CNNs in scalability and efficiency when trained at scale.

### Simple PyTorch Example: Using torchvision's Built-in ViT

PyTorch provides a pre-trained ViT implementation in `torchvision`.

```python
import torch
from torchvision import models, transforms
from PIL import Image

# Load pre-trained ViT-B/16
model = models.vit_b_16(pretrained=True)
model.eval()

# Preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Example: Load an image and predict
img = Image.open("example_image.jpg")  # Replace with your image path
input_tensor = preprocess(img).unsqueeze(0)  # Add batch dimension

with torch.no_grad():
    outputs = model(input_tensor)
    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
    # Get top prediction (requires ImageNet classes list)
```

### Minimal Custom ViT Implementation in PyTorch

Here's a simplified from-scratch ViT for illustration (not production-optimized).

```python
import torch
import torch.nn as nn

class PatchEmbedding(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_channels=3, embed_dim=768):
        super().__init__()
        self.num_patches = (img_size // patch_size) ** 2
        self.proj = nn.Conv2d(in_channels, embed_dim, kernel_size=patch_size, stride=patch_size)
    
    def forward(self, x):
        x = self.proj(x)  # (B, embed_dim, num_patches_h, num_patches_w)
        x = x.flatten(2).transpose(1, 2)  # (B, num_patches, embed_dim)
        return x

class ViT(nn.Module):
    def __init__(self, img_size=224, patch_size=16, num_classes=1000, embed_dim=768, depth=12, num_heads=12, mlp_ratio=4):
        super().__init__()
        self.patch_embed = PatchEmbedding(img_size, patch_size, embed_dim=embed_dim)
        num_patches = self.patch_embed.num_patches
        
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        self.pos_embed = nn.Parameter(torch.zeros(1, num_patches + 1, embed_dim))
        
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, dim_feedforward=embed_dim * mlp_ratio, activation='gelu')
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=depth)
        
        self.mlp_head = nn.Linear(embed_dim, num_classes)
    
    def forward(self, x):
        B = x.shape[0]
        x = self.patch_embed(x)
        
        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)
        
        x = x + self.pos_embed
        x = self.transformer(x)
        
        cls_output = x[:, 0]
        return self.mlp_head(cls_output)

# Usage
model = ViT(num_classes=10)  # e.g., for CIFAR-10
img = torch.randn(2, 3, 224, 224)
outputs = model(img)  # (2, 10)
```

This captures the core mechanics; real implementations add dropout, normalization details, etc.

References:  

- [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (Original ViT Paper)](https://arxiv.org/abs/2010.11929)  
- [torchvision VisionTransformer Documentation](https://pytorch.org/vision/stable/models/generated/torchvision.models.vit_b_16.html)  
- [Wikipedia: Vision Transformer](https://en.wikipedia.org/wiki/Vision_transformer)  
- [V7 Labs: Vision Transformer Guide](https://www.v7labs.com/blog/vision-transformer-guide)  
- [GeeksforGeeks: Vision Transformer Architecture](https://www.geeksforgeeks.org/deep-learning/vision-transformer-vit-architecture/)