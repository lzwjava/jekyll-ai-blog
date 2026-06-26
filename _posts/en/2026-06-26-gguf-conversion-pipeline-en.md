---
audio: false
generated: true
image: false
lang: en
layout: post
title: GGUF Conversion Pipeline
translated: false
type: note
---

Question: How do I convert my model to GGUF format using the conversion script?

Answer:

The `gguf` pip package alone doesn't do the conversion — it's just the writer library. You need `convert_hf_to_gguf.py` from the llama.cpp repo, then quantize with the `llama-quantize` binary.

Here's the full pipeline:

```bash
# On the remote box (213.173.x.x)
cd /workspace

# 1. Get llama.cpp (the convert script lives here, not in pip gguf)
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
pip3 install -r requirements.txt   # numpy, gguf, sentencepiece, transformers, etc.

# 2. Convert HF checkpoint -> GGUF (fp16 first, lossless)
python3 convert_hf_to_gguf.py /workspace/model \
  --outfile /workspace/model-f16.gguf \
  --outtype f16

# 3. Build the quantizer
cmake -B build && cmake --build build --config Release -j$(nproc)

# 4. Quantize fp16 -> Q4_K_M (best size/quality default)
./build/bin/llama-quantize \
  /workspace/model-f16.gguf \
  /workspace/model-Q4_K_M.gguf \
  Q4_K_M
```

A few things specific to your situation:

**`--outtype` options:** `f16` (16-bit, full quality, big), `bf16`, `q8_0` (near-lossless, fast), or `f32`. Always convert to `f16`/`bf16` first, then quantize separately — converting directly to a low-bit type via the script skips the better k-quant imatrix paths.

**Quant types** worth knowing: `Q4_K_M` (~4.5 bpw, the standard), `Q5_K_M` (better quality), `Q6_K` (near-fp16), `Q8_0` (basically lossless). For a "pro" model you're testing locally, `Q5_K_M` or `Q6_K` is a good tradeoff if disk allows.

**If it's a MoE or a newer arch** (mimo-v2.5 — check the config), `convert_hf_to_gguf.py` must explicitly support the architecture. If you hit `Model architecture 'XXX' not supported`, the converter doesn't know it yet — you'll need a llama.cpp version with a matching `@Model.register("XXX")` entry in `convert_hf_to_gguf.py`, or it simply can't be converted to GGUF.

**Then run it** with the llama-cpp-python you already installed:

```python
from llama_cpp import Llama
llm = Llama(model_path="/workspace/model-Q4_K_M.gguf", n_gpu_layers=-1, n_ctx=4096)
print(llm("Hello", max_tokens=64)["choices"][0]["text"])
```

One caveat: the progress bar in your screenshot looks like a download still at 8% (86.7K/1M, ~1h48m left). Let that finish before converting — a partial checkpoint will fail with a safetensors/shard error.

What's the actual architecture in `/workspace/model/config.json`? That determines whether GGUF conversion will even work for mimo-v2.5.
