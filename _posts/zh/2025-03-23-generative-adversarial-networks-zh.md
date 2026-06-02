---
audio: false
generated: true
lang: zh
layout: post
title: 生成对抗网络
translated: true
type: note
---

**定义**：
GANs（生成对抗网络）是一类机器学习框架，包含两个相互对抗的神经网络——**生成器**（\\(G\\)）与**判别器**（\\(D\\)）。生成器负责生成合成数据，判别器则判断数据来源是真实训练集还是生成器产生的伪造数据。通过这种对抗竞争，\\(G\\) 会不断提升生成逼真数据的能力，而 \\(D\\) 则会更精准地区分真伪数据。

---

### 数学形式化

对抗训练被形式化为一个带价值函数 \\(V(D, G)\\) 的**极小极大博弈**：

\\[
\min_G \max_D V(D, G) = \mathbb{E}_{x \sim p_{\text{data}}(x)}[\log D(x)] + \mathbb{E}_{z \sim p_z(z)}[\log(1 - D(G(z)))]
\\]

- **判别器损失**：最大化正确分类真伪数据的概率：
  \\[
  L_D = -\left[\mathbb{E}[\log D(x)] + \mathbb{E}[\log(1 - D(G(z)))]\right]
  \\]

- **生成器损失**：最小化判别器识别伪造数据的概率（采用非饱和版本以获得更好梯度）：
  \\[
  L_G = -\mathbb{E}[\log D(G(z))]
  \\]

---

### 代码示例（PyTorch）

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# 超参数
latent_dim = 100
img_dim = 784  # 28x28 MNIST
batch_size = 64
epochs = 50
lr = 0.0002

# 生成器网络
class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, img_dim),
            nn.Tanh()  # 输出范围[-1, 1]
        )

    def forward(self, z):
        return self.model(z)

# 判别器网络
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

# 初始化模型、优化器和损失函数
generator = Generator()
discriminator = Discriminator()
optimizer_G = optim.Adam(generator.parameters(), lr=lr)
optimizer_D = optim.Adam(discriminator.parameters(), lr=lr)
criterion = nn.BCEWithLogitsLoss()

# 数据加载（MNIST）
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))  # 归一化至[-1, 1]
])
dataloader = DataLoader(
    datasets.MNIST("./data", train=True, download=True, transform=transform),
    batch_size=batch_size,
    shuffle=True
)

# 训练循环
for epoch in range(epochs):
    for i, (real_imgs, _) in enumerate(dataloader):
        real_imgs = real_imgs.view(-1, img_dim)
        batch_size = real_imgs.size(0)

        # 生成伪造图像
        z = torch.randn(batch_size, latent_dim)
        fake_imgs = generator(z)

        # 训练判别器
        optimizer_D.zero_grad()

        # 真实图像损失
        real_labels = torch.ones(batch_size, 1)
        real_outputs = discriminator(real_imgs)
        d_loss_real = criterion(real_outputs, real_labels)

        # 伪造图像损失
        fake_labels = torch.zeros(batch_size, 1)
        fake_outputs = discriminator(fake_imgs.detach())
        d_loss_fake = criterion(fake_outputs, fake_labels)

        d_loss = d_loss_real + d_loss_fake
        d_loss.backward()
        optimizer_D.step()

        # 训练生成器
        optimizer_G.zero_grad()

        # 欺骗判别器
        outputs = discriminator(fake_imgs)
        g_loss = criterion(outputs, real_labels)
        g_loss.backward()
        optimizer_G.step()

    # 定期输出损失值或生成样本
    print(f"Epoch [{epoch}/{epochs}] | D Loss: {d_loss.item():.4f} | G Loss: {g_loss.item():.4f}")

# 生成样本
z = torch.randn(1, latent_dim)
generated_img = generator(z).view(28, 28).detach().numpy()
```

---

### 代码解析

1. **网络结构**：
   - **生成器**：通过线性层和`LeakyReLU`将噪声(\\(z\\))转换为图像（类MNIST）
   - **判别器**：使用线性层和`LeakyReLU`对图像进行真伪分类

2. **训练过程**：
   - **判别器**：最大化 \\(\log D(x) + \log(1 - D(G(z)))\\)
   - **生成器**：最小化 \\(\log(1 - D(G(z))\\)（等价于最大化 \\(\log D(G(z))\\)）

3. **数据预处理**：
   - MNIST图像被归一化至 \\([-1, 1]\\) 以匹配生成器`Tanh`的输出范围

4. **优化策略**：
   - 双网络均采用Adam优化器
   - BCEWithLogitsLoss结合了Sigmoid激活函数与二元交叉熵

---

### 输出示例

训练完成后，生成器可生成类MNIST手写数字。使用matplotlib可视化生成图像：

```python
import matplotlib.pyplot as plt

# 生成并显示图像
z = torch.randn(1, latent_dim)
generated_img = generator(z).view(28, 28).detach().numpy()
plt.imshow(generated_img, cmap="gray")
plt.axis("off")
plt.show()
```

本代码为理解GAN的数学原理和实现提供了基础框架。如需提升性能，可考虑使用更深的网络结构、卷积层，以及学习率调度、梯度惩罚等进阶技术。
