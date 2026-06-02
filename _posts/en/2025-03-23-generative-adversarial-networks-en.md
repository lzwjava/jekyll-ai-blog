---
audio: false
generated: true
lang: en
layout: post
title: Generative Adversarial Networks (GANs)
translated: false
type: note
---

**Definition**:
GANs are a class of machine learning frameworks where two neural networks, the **generator** (\\(G\\)) and the **discriminator** (\\(D\\)), compete adversarially. The generator creates synthetic data, while the discriminator evaluates whether the data is real (from the training set) or fake (from \\(G\\)). Through this competition, \\(G\\) improves its ability to generate realistic data, and \\(D\\) becomes better at distinguishing real from fake.

---

### Mathematical Formulation

The adversarial training is formalized as a **minimax game** with the value function \\(V(D, G)\\):

\\[
\min_G \max_D V(D, G) = \mathbb{E}_{x \sim p_{\text{data}}[x](\log D(x)) + \mathbb{E}_{z \sim p_z(z)}[\log(1 - D(G(z)))]
\\]

- **Discriminator Loss**: Maximize the probability of correctly classifying real and fake data:
  \\[
  L_D = -\left[\mathbb{E}[\log D(x)] + \mathbb{E}[\log(1 - D(G(z)))]\right]
  \\]

- **Generator Loss**: Minimize the probability of the discriminator correctly identifying fake data (non-saturating version for better gradients):
  \\[
  L_G = -\mathbb{E}[\log D(G(z))]
  \\]

---

### Code Example (PyTorch)

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Hyperparameters
latent_dim = 100
img_dim = 784  # 28x28 MNIST
batch_size = 64
epochs = 50
lr = 0.0002

# Generator Network
class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, img_dim),
            nn.Tanh()  # Outputs in [-1, 1]
        )

    def forward(self, z):
        return self.model(z)

# Discriminator Network
class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(img_dim, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 1),
        )

    def forward(self, img):
        return self.model(img)

# Initialize models, optimizers, and loss
generator = Generator()
discriminator = Discriminator()
optimizer_G = optim.Adam(generator.parameters(), lr=lr)
optimizer_D = optim.Adam(discriminator.parameters(), lr=lr)
criterion = nn.BCEWithLogitsLoss()

# Data loading (MNIST)
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))  # Normalize to [-1, 1]
])
dataloader = DataLoader(
    datasets.MNIST("./data", train=True, download=True, transform=transform),
    batch_size=batch_size,
    shuffle=True
)

# Training loop
for epoch in range(epochs):
    for i, (real_imgs, _) in enumerate(dataloader):
        real_imgs = real_imgs.view(-1, img_dim)
        batch_size = real_imgs.size(0)

        # Generate fake images
        z = torch.randn(batch_size, latent_dim)
        fake_imgs = generator(z)

        # Train Discriminator
        optimizer_D.zero_grad()

        # Loss on real images
        real_labels = torch.ones(batch_size, 1)
        real_outputs = discriminator(real_imgs)
        d_loss_real = criterion(real_outputs, real_labels)

        # Loss on fake images
        fake_labels = torch.zeros(batch_size, 1)
        fake_outputs = discriminator(fake_imgs.detach())
        d_loss_fake = criterion(fake_outputs, fake_labels)

        d_loss = d_loss_real + d_loss_fake
        d_loss.backward()
        optimizer_D.step()

        # Train Generator
        optimizer_G.zero_grad()

        # Fool the discriminator
        outputs = discriminator(fake_imgs)
        g_loss = criterion(outputs, real_labels)
        g_loss.backward()
        optimizer_G.step()

    # Print losses or generate samples periodically
    print(f"Epoch [{epoch}/{epochs}] | D Loss: {d_loss.item():.4f} | G Loss: {g_loss.item():.4f}")

# Generate samples
z = torch.randn(1, latent_dim)
generated_img = generator(z).view(28, 28).detach().numpy()
```

---

### Explanation of Code

1. **Networks**:
   - **Generator**: Transforms noise (\\(z\\)) into images (MNIST-like) using linear layers and `LeakyReLU`.
   - **Discriminator**: Classifies images as real/fake using linear layers and `LeakyReLU`.

2. **Training**:
   - **Discriminator**: Maximizes \\(\log D(x) + \log(1 - D(G(z)))\\).
   - **Generator**: Minimizes \\(\log(1 - D(G(z)))\\) (or equivalently, maximizes \\(\log D(G(z))\\)).

3. **Data**:
   - MNIST images are normalized to \\([-1, 1]\\) to match the generator's `Tanh` output.

4. **Optimization**:
   - Adam optimizer for both networks.
   - BCEWithLogitsLoss combines sigmoid activation and binary cross-entropy.

---

### Sample Output

After training, the generator can produce MNIST-like digits. Use matplotlib to visualize the generated images:

```python
import matplotlib.pyplot as plt

# Generate and plot an image
z = torch.randn(1, latent_dim)
generated_img = generator(z).view(28, 28).detach().numpy()
plt.imshow(generated_img, cmap="gray")
plt.axis("off")
plt.show()
```

This code provides a foundational understanding of GANs, their math, and implementation. For improved performance, consider deeper networks, convolutional layers, and advanced techniques like learning rate scheduling or gradient penalties.
