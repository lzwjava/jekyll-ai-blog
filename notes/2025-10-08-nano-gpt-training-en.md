---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Training Custom Datasets with nanoGPT
translated: false
type: note
---

### Preparing and Training a Custom Text Dataset with nanoGPT

nanoGPT is designed for easy training on text data, including custom datasets. The process involves preparing your text into binary token files, configuring the training parameters, and running the training script. Below, I'll outline the steps based on the repository's examples (e.g., Shakespeare or OpenWebText). You'll need Python 3.8+ and a GPU for efficient training (CPU works but is slower).

#### 1. Install Dependencies
First, set up the environment:
```
pip install torch numpy transformers datasets tiktoken wandb tqdm
```
- `torch`: For PyTorch (install with CUDA if using GPU: e.g., `pip install torch --index-url https://download.pytorch.org/whl/cu118`).
- Others handle tokenization, data loading, and logging.

#### 2. Prepare Your Custom Dataset
nanoGPT expects your data as binary files (`train.bin` and `val.bin`) containing tokenized integers. You'll need to write a simple preparation script to process your raw text.

- **Place Your Text File**: Put your raw text (e.g., `input.txt`) in a new folder under `data/`, like `data/my_dataset/`.

- **Create a Preparation Script**: Copy and adapt an example from the repo (e.g., `data/shakespeare_char/prepare.py` for character-level or `data/openwebtext/prepare.py` for GPT-2 BPE token-level).

  **Example for Character-Level Tokenization** (simple for small datasets; treats each character as a token):
  ```python
  # Save as data/my_dataset/prepare.py
  import os
  import requests
  import numpy as np
  from torch.utils.data import Dataset, random_split

  # Load your text (replace with your file path)
  with open('data/my_dataset/input.txt', 'r', encoding='utf-8') as f:
      text = f.read()

  # Encode as characters
  chars = sorted(list(set(text)))
  vocab_size = len(chars)
  stoi = {ch: i for i, ch in enumerate(chars)}
  itos = {i: ch for i, ch in enumerate(chars)}
  def encode(s): return [stoi[c] for c in s]
  def decode(l): return ''.join([itos[i] for i in l])

  # Tokenize the entire text
  data = torch.tensor(encode(text), dtype=torch.long)

  # Split into train/val (90/10)
  n = int(0.9 * len(data))
  train_data = data[:n]
  val_data = data[n:]

  # Save as .bin files
  train_data = train_data.numpy()
  val_data = val_data.numpy()
  train_data.tofile('data/my_dataset/train.bin')
  val_data.tofile('data/my_dataset/val.bin')

  # Print stats
  print(f"Length of dataset in characters: {len(data)}")
  print(f"Vocab size: {vocab_size}")
  ```
  Run it:
  ```
  python data/my_dataset/prepare.py
  ```
  This creates `train.bin` and `val.bin`.

- **For GPT-2 BPE Tokenization** (better for larger datasets; uses subwords):
  Adapt `data/openwebtext/prepare.py`. You'll need to install `tiktoken` (already in deps) and handle your text similarly, but use `tiktoken.get_encoding("gpt2").encode()` instead of character encoding. Split your text into train/val chunks (e.g., 90/10), then save as NumPy arrays to `.bin`.

- **Tips**:
  - Keep your dataset clean (e.g., remove special chars if needed).
  - For very large files, process in chunks to avoid memory issues.
  - Vocab size: ~65 for chars (Shakespeare); ~50k for BPE.

#### 3. Configure Training
Create a config file by copying an example (e.g., `config/train_shakespeare_char.py`) to `config/train_my_dataset.py` and edit it.

Key parameters to tweak:
```python
# Example config snippet
out_dir = 'out-my_dataset'  # Output folder for checkpoints
dataset = 'my_dataset'      # Matches your data folder name
batch_size = 64             # Adjust based on GPU memory (e.g., 12 for small GPU)
block_size = 256            # Context length (tokens per example)
n_layer = 6                 # Transformer layers
n_head = 6                  # Attention heads
n_embd = 384                # Embedding dimension
max_iters = 5000            # Training steps
lr = 6e-4                   # Learning rate
dropout = 0.2               # Dropout rate
init_from = 'scratch'       # 'scratch' for new model; 'gpt2' to load pretrained
```
- For finetuning (start from pretrained GPT-2): Set `init_from = 'gpt2'` (or 'gpt2-medium').
- For Apple Silicon: Add `device = 'mps'`.
- Save checkpoints every 500 iters by default.

#### 4. Run Training
Train from scratch or finetune:
```
python train.py config/train_my_dataset.py
```
- For multi-GPU (e.g., 8 GPUs): `torchrun --standalone --nproc_per_node=8 train.py config/train_my_dataset.py`.
- Monitor with WandB (logs losses, samples; enable in config with `wandb_log = True`).
- Training time: Minutes for tiny models on GPU; hours/days for larger ones.

#### 5. Generate Samples (Test the Model)
After training, sample text:
```
python sample.py --out_dir=out-my_dataset --start="Your prompt here"
```
This loads the latest checkpoint and generates.

#### Common Issues
- **Memory Errors**: Reduce `batch_size` or `block_size`.
- **No GPU**: Add `--device=cpu --compile=False` to commands.
- **Large Datasets**: Use distributed training for scaling.

For more details, check the repo's README and data/config examples.

[nanoGPT GitHub](https://github.com/karpathy/nanoGPT)
