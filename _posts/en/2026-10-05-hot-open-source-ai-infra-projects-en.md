---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hot Open-Source AI Infra Projects
translated: false
type: note
---

Question: What are the hot open-source projects in AI infra and LLMs right now (nanochat, vLLM, SGLang, etc.)?

Answer:

I don't have live GitHub star-velocity data, so this list reflects what's getting the most release activity and ecosystem attention, grouped by layer.

**1. Inference engines**
- **vLLM** is the default choice. Its team formed Inferact, which raised $150M in January 2026 to commercialize the project. HuggingFace TGI has entered maintenance mode, leaving SGLang, vLLM, and MAX as the three primary open-source engines.
- **SGLang** is the main challenger. It shipped day-0 support for DeepSeek-V4 and posted a 25x performance gain on NVIDIA GB300 NVL72. It's also described as the reference implementation for DeepSeek V3/V4 serving. Its sweet spot is multi-turn and agentic workloads thanks to RadixAttention.
- **Others to watch:** TensorRT-LLM (NVIDIA-only, maximum performance but 1-2 weeks of setup), LMDeploy, and llama.cpp for local and edge use.

**2. Cluster-scale serving and orchestration**
- **NVIDIA Dynamo** is an orchestration layer above the engines. It doesn't replace SGLang, TensorRT-LLM, or vLLM; it turns them into a coordinated multi-node system. It's written mostly in Rust.
- **llm-d** (Red Hat) and **AIBrix** (ByteDance) fill a similar role on Kubernetes.
- **LMCache** is a KV-cache layer shared across engines. It supports prefill-to-decode KV transfer over NVLink, RDMA, or TCP. Disaggregated prefill/decode has moved from experimental to standard.

**3. RL post-training**
- **verl** (ByteDance Seed, now under verl-project) keeps growing. Recent add-ons include verl-vla, RL-Insight, uni-agent, and verl-SpeCo.
- **slime** is notable because it's the RL framework behind the GLM-4.5 through GLM-5.2 models.
- **Miles** (from RadixArk, built on slime): v0.1 was released in August 2026 and integrates SGLang and Megatron-LM.
- **vime** is an RL post-training framework within the vLLM ecosystem, built on slime and connecting Megatron with vLLM.

**4. Education and research: nanochat**
Karpathy's nanochat is a full ChatGPT-style pipeline. It's about 8,000 lines covering tokenizer, pretraining, midtraining, SFT, optional RL, and an inference engine with KV cache. It's still moving fast. In March 2026 it reached GPT-2-level training in about 2 hours on one 8xH100 node, helped by NVIDIA ClimbMix and FP8. Karpathy also had autonomous agents iterate on the repo, making 110 changes in about 12 hours.

**Broad trends**
- Engines and RL frameworks are converging: SGLang pairs with Miles, vLLM with vime.
- KV cache management and disaggregated serving are the main frontier.
- Agentic workloads are driving both serving and training design.
- Day-0 support for new open models (DeepSeek-V4, Nemotron 3) has become a competitive feature.

Some of the benchmark comparisons I found are from third-party blogs, so verify performance claims against your own hardware and model.

If you tell me whether you care more about serving, training, or learning, I can narrow this to a shortlist.

References:
- [SGLang GitHub (news section)](https://github.com/tocque/sglang)
- [Open-source LLM inference engines compared 2026 – Fish Audio](https://fish.audio/blog/open-source-llm-inference-engines-2026/)
- [Local LLM Inference Tools, July 2026 – DEV Community](https://dev.to/sreeraj-sreenivasan/the-complete-guide-to-local-llm-inference-tools-in-july-2026-llamacpp-ollama-vllm-sglang-and-4mh1)
- [vLLM vs Ollama vs SGLang vs TensorRT-LLM](https://theaiengineer.substack.com/p/vllm-vs-ollama-vs-sglang-vs-tensorrt)
- [NVIDIA Dynamo (GitHub mirror)](https://github.com/waynehacking8/dynamo)
- [LMCache GitHub](https://github.com/lmcache/lmcache)
- [verl-project/verl](https://github.com/verl-project/verl)
- [Miles (radixark)](https://github.com/radixark/miles)
- [slime](https://github.com/HJSang/slime)
- [Announcing vime – vLLM blog](https://vllm.ai/blog/2026-06-09-announcing-vime)
- [Karpathy's nanochat announcement on X](https://x.com/karpathy/status/1977755427569111362)
- [nanochat 2-hour GPT-2 training](https://blockchain.news/ainews/karpathy-s-nanochat-hits-2-hour-gpt-2-training-on-8x-h100-fp8-and-nvidia-climbmix-boost-throughput-2026-benchmark-analysis)