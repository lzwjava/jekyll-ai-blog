---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 热门开源AI基础设施项目
translated: true
type: note
---

Question: 当前AI基础设施和LLM领域有哪些热门的开源项目（如nanochat、vLLM、SGLang等）？

Answer:

我没有实时的GitHub star增长速度数据，因此以下列表按层级分组，反映的是当前发布活动最活跃且受生态关注的项目。

**1. 推理引擎**

- **vLLM** 已成为默认选择。其团队成立了Inferact，并于2026年1月融资1.5亿美元以将该项目商业化。HuggingFace TGI已进入维护模式，使得SGLang、vLLM和MAX成为三个主要的开源引擎。
- **SGLang** 是主要挑战者。它首发即支持DeepSeek-V4，并在NVIDIA GB300 NVL72上实现了25倍的性能提升。它也被描述为DeepSeek V3/V4服务的参考实现。其优势在于多轮对话和智能体（agentic）工作负载，得益于RadixAttention。
- **其他值得关注的项目：** TensorRT-LLM（仅限NVIDIA，性能最优但需1-2周设置）、LMDeploy以及适用于本地和边缘场景的llama.cpp。

**2. 集群级服务与编排**

- **NVIDIA Dynamo** 是位于引擎之上的编排层。它不是取代SGLang、TensorRT-LLM或vLLM，而是将它们整合为一个协调的多节点系统。它主要用Rust编写。
- **llm-d**（Red Hat）和 **AIBrix**（ByteDance）在Kubernetes上扮演类似角色。
- **LMCache** 是一个跨引擎共享的KV-cache层。它支持通过NVLink、RDMA或TCP进行prefill到decode的KV传输。解耦的prefill/decode已从实验阶段走向标准应用。

**3. 强化学习（RL）后训练**

- **verl**（ByteDance Seed，现归属于verl-project）持续发展。最近的附加组件包括verl-vla、RL-Insight、uni-agent和verl-SpeCo。
- **slime** 值得关注，因为它是GLM-4.5到GLM-5.2系列模型背后的RL框架。
- **Miles**（来自RadixArk，基于slime）：v0.1于2026年8月发布，并集成了SGLang和Megatron-LM。
- **vime** 是vLLM生态内的RL后训练框架，基于slime构建，连接Megatron与vLLM。

**4. 教育与研究：nanochat**
Karpathy的nanochat是一个完整的ChatGPT风格流程。它大约有8000行代码，涵盖tokenizer、预训练、中间训练、SFT、可选的RL以及带KV cache的推理引擎。该项目仍在快速迭代。2026年3月，它在大约2小时内就在一个8xH100节点上达到了GPT-2级别的训练水平，这得益于NVIDIA ClimbMix和FP8。Karpathy还让自主智能体在仓库上迭代，在约12小时内完成了110次改动。

**总体趋势**

- 引擎和RL框架正在融合：SGLang与Miles配对，vLLM与vime配对。
- KV cache管理和解耦服务是当前的主要前沿领域。
- 智能体工作负载正在推动服务和训练设计。
- 对新开放模型（如DeepSeek-V4、Nemotron 3）的首日支持已成为一项竞争特性。

我发现的部分基准对比来自第三方博客，因此请根据您自己的硬件和模型验证性能声称。

如果您能说明您更关注服务、训练还是学习，我可以将列表缩小到一个更精确的范围。

参考文献：

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
