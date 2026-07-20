---
audio: false
generated: true
image: false
lang: en
layout: post
title: "JittorLLMs: Low-Resource LLM Inference"
translated: false
type: note
---

Question: What is Jittor/JittorLLMs?

Answer: It's an LLM inference library built on **Jittor** (Tsinghua/Feiten-developed deep learning framework, China's answer to PyTorch — uses JIT meta-operator compilation instead of eager/graph execution). Core pitch: run big models on laptops with no GPU, 2GB RAM.

Key mechanics:

- **Model support**: ChatGLM-6B, LLaMA/LLaMA2, ChatRWKV, PanGu-α, Atom-7B (MOSS planned)
- **Memory trick**: dynamic tensor swapping across GPU↔CPU↔disk — they claim to be first framework with automatic dynamic-graph variable swapping (vs static-graph swap techniques used elsewhere)
- **Portability**: `JTorch` — a Jittor-backed drop-in replacement for `torch`, so existing HF Transformers/Megatron code runs unmodified
- **Claims**: 80% lower hardware requirement, 40% faster load (zero-copy), 20%+ faster compute vs comparable frameworks (unverified, no benchmarks published beyond marketing claims)

Usage is genuinely CLI-first, which fits your workflow:

```bash
git clone https://github.com/Jittor/JittorLLMs.git --depth 1
cd JittorLLMs
pip install -r requirements.txt -i https://pypi.jittor.org/simple -I

python cli_demo.py chatglm    # or: pangualpha|llama|chatrwkv|llama2|atom7b
```

Memory limiting via env vars (useful if you're testing on constrained boxes):

```bash
export JT_SAVE_MEM=1
export cpu_mem_limit=16000000000   # 16G
export device_mem_limit=8000000000  # 8G
```

Backend server mode:

```bash
python api.py chatglm
# then: requests.post("http://0.0.0.0:8000", json.dumps({'prompt': '...'}))
```

**Reality check**: 2.4k stars, 187 forks, no releases published, last active development seems tied to the 2023 ChatGLM/LLaMA2-era models — nothing newer (no Qwen3, DeepSeek-V3/R1, Llama 3+). For your GPU cluster work (MI300X, 2B tokens/mo) this is more of a "laptop demo toy" than production infra — llama.cpp/vLLM/SGLang cover the same ground with far more active maintenance and hardware support. Worth knowing about mainly as a Jittor-ecosystem curiosity (JTorch drop-in compat layer is the more interesting technical bit if you're doing custom hardware backends).

References:

- [Jittor/JittorLLMs](https://github.com/Jittor/JittorLLMs)
- [Jittor docs](https://cg.cs.tsinghua.edu.cn/jittor/assets/docs/index.html)
