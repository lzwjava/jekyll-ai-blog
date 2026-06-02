---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 使用nanoGPT训练自定义数据集
translated: true
type: note
---

### 使用 nanoGPT 准备和训练自定义文本数据集

nanoGPT 旨在简化文本数据的训练流程，包括自定义数据集的处理。整个过程涉及将文本准备成二进制令牌文件、配置训练参数以及运行训练脚本。下面我将根据代码库中的示例（如莎士比亚作品或 OpenWebText）概述具体步骤。您需要 Python 3.8+ 和 GPU 以实现高效训练（CPU 也可运行但速度较慢）。

#### 1. 安装依赖
首先设置环境：
```
pip install torch numpy transformers datasets tiktoken wandb tqdm
```
- `torch`：用于 PyTorch（如果使用 GPU 需安装 CUDA 版本：例如 `pip install torch --index-url https://download.pytorch.org/whl/cu118`）。
- 其他依赖包用于处理令牌化、数据加载和日志记录。

#### 2. 准备自定义数据集
nanoGPT 要求数据以包含令牌化整数的二进制文件（`train.bin` 和 `val.bin`）形式提供。您需要编写一个简单的准备脚本来处理原始文本。

- **放置文本文件**：将原始文本文件（如 `input.txt`）放入 `data/` 下的新建文件夹中，例如 `data/my_dataset/`。

- **创建准备脚本**：从代码库复制并修改示例脚本（例如，字符级处理使用 `data/shakespeare_char/prepare.py`，GPT-2 BPE 令牌级处理使用 `data/openwebtext/prepare.py`）。

  **字符级令牌化示例**（适用于小型数据集，将每个字符视为一个令牌）：
  ```python
  # 保存为 data/my_dataset/prepare.py
  import os
  import requests
  import numpy as np
  from torch.utils.data import Dataset, random_split

  # 加载文本（替换为您的文件路径）
  with open('data/my_dataset/input.txt', 'r', encoding='utf-8') as f:
      text = f.read()

  # 字符编码处理
  chars = sorted(list(set(text)))
  vocab_size = len(chars)
  stoi = {ch: i for i, ch in enumerate(chars)}
  itos = {i: ch for i, ch in enumerate(chars)}
  def encode(s): return [stoi[c] for c in s]
  def decode(l): return ''.join([itos[i] for i in l])

  # 对整个文本进行令牌化
  data = torch.tensor(encode(text), dtype=torch.long)

  # 按 90/10 比例分割训练集/验证集
  n = int(0.9 * len(data))
  train_data = data[:n]
  val_data = data[n:]

  # 保存为 .bin 文件
  train_data = train_data.numpy()
  val_data = val_data.numpy()
  train_data.tofile('data/my_dataset/train.bin')
  val_data.tofile('data/my_dataset/val.bin')

  # 输出统计信息
  print(f"数据集字符长度: {len(data)}")
  print(f"词汇表大小: {vocab_size}")
  ```
  运行脚本：
  ```
  python data/my_dataset/prepare.py
  ```
  这将生成 `train.bin` 和 `val.bin` 文件。

- **GPT-2 BPE 令牌化**（更适用于大型数据集，使用子词单元）：
  修改 `data/openwebtext/prepare.py`。您需要安装 `tiktoken`（已包含在依赖中），并以类似方式处理文本，但需使用 `tiktoken.get_encoding("gpt2").encode()` 替代字符编码。将文本按比例（如 90/10）分割为训练集/验证集后，保存为 NumPy 数组至 `.bin` 文件。

- **注意事项**：
  - 保持数据集整洁（例如必要时移除特殊字符）。
  - 处理超大文件时，分块处理以避免内存问题。
  - 词汇表大小：字符级约 65（莎士比亚数据集）；BPE 级约 5 万。

#### 3. 配置训练参数
通过复制示例配置文件（如 `config/train_shakespeare_char.py`）创建新配置，保存为 `config/train_my_dataset.py` 并编辑内容。

关键参数调整示例：
```python
# 配置片段示例
out_dir = 'out-my_dataset'  # 检查点输出目录
dataset = 'my_dataset'      # 对应您的数据文件夹名称
batch_size = 64             # 根据 GPU 内存调整（如小显存 GPU 设为 12）
block_size = 256            # 上下文长度（每个样本的令牌数）
n_layer = 6                 # Transformer 层数
n_head = 6                  # 注意力头数
n_embd = 384                # 嵌入维度
max_iters = 5000            # 训练步数
lr = 6e-4                   # 学习率
dropout = 0.2               # 丢弃率
init_from = 'scratch'       # 'scratch' 表示新模型；'gpt2' 表示加载预训练模型
```
- 微调场景（从预训练 GPT-2 开始）：设置 `init_from = 'gpt2'`（或 'gpt2-medium'）。
- Apple Silicon 芯片：添加 `device = 'mps'`。
- 默认每 500 次迭代保存检查点。

#### 4. 运行训练
从头开始训练或进行微调：
```
python train.py config/train_my_dataset.py
```
- 多 GPU 训练（例如 8 GPU）：`torchrun --standalone --nproc_per_node=8 train.py config/train_my_dataset.py`。
- 使用 WandB 监控（记录损失和生成样本；在配置中通过 `wandb_log = True` 启用）。
- 训练时间：GPU 上小型模型需数分钟；大型模型需数小时/天。

#### 5. 生成样本（测试模型）
训练完成后生成文本：
```
python sample.py --out_dir=out-my_dataset --start="您的提示文本"
```
此命令将加载最新检查点并生成文本。

#### 常见问题
- **内存错误**：降低 `batch_size` 或 `block_size`。
- **无 GPU**：在命令中添加 `--device=cpu --compile=False`。
- **大型数据集**：使用分布式训练进行扩展。

更多细节请查阅代码库的 README 文档和数据/配置示例。

[nanoGitHub 项目地址](https://github.com/karpathy/nanoGPT)
