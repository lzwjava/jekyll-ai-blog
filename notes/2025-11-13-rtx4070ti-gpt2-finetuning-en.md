---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: RTX 4070 Ti GPT-2 Fine-Tuning Guide
translated: false
type: note
---

## Setting Up Your Environment

Before training, ensure your NVIDIA RTX 4070 Ti is properly set up. This GPU has 12GB of VRAM, which is more than enough for GPT-2 Small (124M parameters) during fine-tuning. Training from scratch on a massive dataset like OpenWebText is impractical on a single consumer GPU due to time and compute requirements—it would take weeks or months. Instead, focus on fine-tuning the pre-trained model on your own dataset for specific tasks.

### 1. Install NVIDIA Drivers and CUDA

- Download and install the latest NVIDIA drivers for your RTX 4070 Ti from the official NVIDIA website. Ensure it's version 535 or higher for full compatibility.
- Install the CUDA Toolkit. The RTX 4070 Ti (compute capability 8.9) supports CUDA 12.x. Recommend CUDA 12.4:
  - Download from the NVIDIA CUDA Toolkit archive.
  - Follow the installation guide for your OS (Windows/Linux).
- Install cuDNN (CUDA Deep Neural Network library) matching your CUDA version (e.g., cuDNN 8.9 for CUDA 12.4).
- Verify installation:

  ```
  nvidia-smi  # Should show your GPU and CUDA version
  nvcc --version  # Confirms CUDA installation
  ```

### 2. Set Up Python Environment

- Use Python 3.10 or 3.11. Install via Anaconda or Miniconda for easier management.
- Create a virtual environment:

  ```
  conda create -n gpt2-train python=3.10
  conda activate gpt2-train
  ```

### 3. Install Required Libraries

- Install PyTorch with CUDA support. For CUDA 12.4:

  ```
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
  ```

  Verify:

  ```
  python -c "import torch; print(torch.cuda.is_available())"  # Should return True
  ```

- Install Hugging Face libraries and others:

  ```
  pip install transformers datasets accelerate sentencepiece pandas tqdm
  ```

## Preparing Your Dataset

- Choose or prepare a text dataset (e.g., a .txt file with one sample per line or a CSV with a 'text' column).
- For example, use a public dataset from Hugging Face Datasets:

  ```python
  from datasets import load_dataset
  dataset = load_dataset("bookcorpus")  # Or your custom dataset: load_dataset("text", data_files="your_data.txt")
  ```

- Split into train/test if needed:

  ```python
  dataset = dataset["train"].train_test_split(test_size=0.1)
  ```

## Fine-Tuning GPT-2 Small

Use the Hugging Face Transformers library for simplicity. Here's a complete script for causal language modeling (predicting the next token).

### Script Example

Save this as `train_gpt2.py` and run with `python train_gpt2.py`.

```python
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset

# Load tokenizer and model (GPT-2 Small)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token  # Set padding token
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Load and preprocess dataset (replace with your dataset)
dataset = load_dataset("bookcorpus")
dataset = dataset["train"].train_test_split(test_size=0.1)

def preprocess(examples):
    return tokenizer(examples["text"], truncation=True, max_length=512, padding="max_length")

tokenized_dataset = dataset.map(preprocess, batched=True, remove_columns=["text"])

# Data collator for language modeling
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Training arguments (optimized for single GPU)
training_args = TrainingArguments(
    output_dir="./gpt2-finetuned",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=4,  # Adjust based on VRAM; start low to avoid OOM
    per_device_eval_batch_size=4,
    num_train_epochs=3,  # Adjust as needed
    weight_decay=0.01,
    fp16=True,  # Mixed precision for faster training and less VRAM
    gradient_accumulation_steps=4,  # Effective batch size = batch_size * accumulation_steps
    save_steps=1000,
    logging_steps=500,
    report_to="none",  # Or "wandb" for tracking
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    data_collator=data_collator,
)

# Train
trainer.train()

# Save the model
trainer.save_model("./gpt2-finetuned")
```

### Running the Training

- Monitor GPU usage with `nvidia-smi` in another terminal.
- If you hit out-of-memory (OOM) errors:
  - Reduce `per_device_train_batch_size` to 2 or 1.
  - Increase `gradient_accumulation_steps` to maintain effective batch size.
  - Use a smaller max_length (e.g., 256 instead of 512).
- Training time: On a 4070 Ti, for a medium-sized dataset (e.g., 100k samples), expect 1-5 hours per epoch depending on batch size.

## Evaluation and Inference

After training:

```python
from transformers import pipeline

generator = pipeline("text-generation", model="./gpt2-finetuned", device=0)  # device=0 for GPU
output = generator("Your prompt here", max_length=50, num_return_sequences=1)
print(output)
```

- Evaluate perplexity (lower is better):

  ```python
  import math
  eval_results = trainer.evaluate()
  perplexity = math.exp(eval_results["eval_loss"])
  print(f"Perplexity: {perplexity}")
  ```

## Tips and Troubleshooting

- Use mixed precision (`fp16=True`) to save VRAM and speed up training.
- If training from scratch (not recommended): Implement a custom transformer architecture (e.g., via NanoGPT or similar repos) and use a huge dataset, but expect very long runtimes.
- For larger datasets, use distributed training if you have multiple GPUs, but that's beyond a single 4070 Ti.
- Common issues: If PyTorch doesn't detect the GPU, reinstall drivers/CUDA. Ensure no other processes are using the GPU.

## References

- [Fine-Tuning GPT-2: A Practical Guide](https://mr-amit.medium.com/fine-tuning-gpt-2-a-practical-guide-2805b4af738b)
- [Training GPT-2 From Scratch: A Step-by-Step Guide](https://youssefh.substack.com/p/training-gpt-2-from-scratch-a-step)
- [How To Train Your Own GenAI Model](https://developer.squareup.com/blog/how-to-train-your-own-genai-model/)
- [How To Make Custom AI-Generated Text With GPT-2](https://minimaxir.com/2019/09/howto-gpt2/)
- [RTX 4070 CUDA version](https://www.reddit.com/r/pytorch/comments/1kwb5fh/rtx_4070_cuda_version/)
- [Geforce RTX 4070 Ti Super CUDA support for Deep Learning](https://forums.developer.nvidia.com/t/geforce-rtx-4070-ti-super-cuda-support-for-deep-learning/282154)
- [CUDA compatibility with RTX 4070](https://forums.developer.nvidia.com/t/cuda-compatibility-with-rtx-4070/287989)
