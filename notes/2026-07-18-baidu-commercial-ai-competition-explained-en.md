---
audio: false
generated: true
image: false
lang: en
layout: post
title: Baidu Commercial AI Competition Explained
translated: false
type: note
---

Question: What's CTI (百度商业智能大赛)?

Answer:

CTI here means **百度商业AI技术创新大赛** (Baidu Commercial AI Technology Innovation Competition), not the common meanings like "Computer Telephony Integration" or "Cyber Threat Intelligence". ([cti.baidu.com][1])

It is an AI competition organized by Baidu's commercial AI team. The goal is to explore **industrial AI + business scenarios**, especially recommendation, advertising, large-model optimization, and AI engineering talent. It started in 2023 and is open to universities, research institutes, and industry participants. ([cti.baidu.com][1])

The interesting part is that it is not a pure Kaggle-style accuracy competition. It is closer to **real-world AI engineering**:

### Typical tracks

**1. Commercial prediction / recommendation**

* User behavior prediction
* CTR (click-through rate) prediction
* Conversion prediction
* Advertising ranking models

Example:

```
user history
     |
     v
embedding + features
     |
     v
Transformer / DeepFM / DIN / DLRM
     |
     v
P(click | user, ad)
```

The goal is maximizing business metrics like CTR/CVR. ([cti.baidu.com][2])

**2. Large model inference optimization**

This is closer to AI infra:

```
LLM model
   |
   +-- quantization
   +-- KV cache optimization
   +-- CUDA kernels
   +-- batching
   +-- memory optimization
   |
   v
lower latency / higher throughput
```

For example, the 2023 competition included AIGC inference optimization, focusing on improving large-model serving efficiency. ([cti.baidu.com][2])

**3. Generative recommendation / advertising**

Recent competitions moved toward:

* Transformer-based recommendation
* Generative ranking
* Long user behavior sequence modeling
* High-performance inference

The 2026 competition focuses on "生成式推荐广告排序推理性能优化" (generative recommendation advertising ranking inference optimization). ([cti.baidu.com][1])

For someone with your background (nanoGPT, GPT-2 training, GPU/ROCm experiments), the interesting part is probably **not the traditional recommendation model**, but:

```
AI Infra
    |
    +-- vLLM style serving
    +-- CUDA/ROCm optimization
    +-- quantization
    +-- distributed inference
    +-- model compression
```

This is actually close to what companies need:

* A model that scores 1% better but costs 10x more GPU → bad
* A model that is 95% accuracy but serves 100x cheaper → valuable

Commercial AI is often an optimization problem:

[
\text{Business Value} =
\frac{\text{Model Quality} \times \text{Traffic}}{\text{Compute Cost} \times \text{Latency}}
]

The competition is basically training people to solve that equation. ([cti.baidu.com][2])

References:

* 百度商业AI技术创新大赛官网 ([cti.baidu.com][1])
* 2023 百度商业AI技术创新大赛介绍 ([cti.baidu.com][2])

[1]: https://cti.baidu.com/?utm_source=chatgpt.com "百度商业AI技术创新大赛"
[2]: https://cti.baidu.com/2023/index.html?utm_source=chatgpt.com "百度商业AI技术创新大赛"
