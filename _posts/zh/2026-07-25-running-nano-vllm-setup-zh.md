---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 运行Nano-vLLM设置
translated: true
type: note
---

## 如何运行 Nano-vLLM

### 1️⃣ 先决条件

Python 3.10–3.12 和 CUDA 兼容 GPU（或仅 CPU 模式，需设置 `enforce_eager=True`）。

### 2️⃣ 安装依赖

```bash
cd /mnt/data/nano-vllm

# 激活已有的虚拟环境（如果你想使用这里已有的环境之一）
source .venv/bin/activate    # 或 .venv311/bin/activate

# 或者创建一个新的虚拟环境：
python3 -m venv .venv
source .venv/bin/activate

# 以可编辑模式安装包
pip install -e .
```

### 3️⃣ 下载模型

```bash
huggingface-cli download --resume-download Qwen/Qwen3-0.6B \
  --local-dir ~/huggingface/Qwen3-0.6B/ \
  --local-dir-use-symlinks False
```

### 4️⃣ 运行示例

```bash
# 使用 GPU（默认）
python example.py

# 如果没有 GPU / 为避免 CUDA 图编译：
# 编辑 example.py 并确保 enforce_eager=True（已设置）
python example.py
```

### 5️⃣ 运行基准测试

```bash
python bench.py
```

---

### 快速一行命令（如果模型已下载）

```bash
cd /mnt/data/nano-vllm && source .venv/bin/activate && python example.py
```

### 自定义推理

```python
from nanovllm import LLM, SamplingParams

llm = LLM("~/huggingface/Qwen3-0.6B/", enforce_eager=True)
params = SamplingParams(temperature=0.6, max_tokens=256)
outputs = llm.generate(["Hello, world!"], params)
print(outputs[0]["text"])
```