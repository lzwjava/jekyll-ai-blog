---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为修剪排序的仓库大小
translated: true
type: note
---

以下是来自 `repos.json` 的仓库按大小排列的完整细分。我会清晰地整理，以便你决定要清理哪些。

## 来自 `repos.json` 的仓库按磁盘占用排序

**📦 >1GB（最应该移除的候选）：**

| 大小 | 仓库 | 类别 |
|------|------|----------|
| **3.4G** | Qwen2.5-Coder | ai-models |
| **2.2G** | TensorRT-LLM | ai-inference |
| **1.7G** | openai-cookbook | ai-apps |
| **1.6G** | evals | ai-models |
| **1.5G** | greptimedb | infra-network |
| **1.2G** | litellm | ai-apps |
| **1.2G** | claw-code | ai-agents |
| **1.1G** | weaviate | infra-network |

**📦 500MB–1GB：**

| 大小 | 仓库 | 类别 |
|------|------|----------|
| 907M | llama_index | ai-apps |
| 836M | llama.cpp | ai-inference |
| 789M | warp | dev-tools |
| 763M | pytorch | ai-training |
| 753M | mlflow | ai-apps |
| 726M | LibreChat | ai-apps |
| 701M | crewAI | ai-agents |
| 687M | bun | dev-tools |
| 664M | vortex | dev-tools |
| 664M | hermes-agent | ai-agents |
| 609M | Telegram-iOS | web-platforms |
| 567M | AutoGPT | ai-agents |

**📦 100–500MB：**

| 大小 | 仓库 | 类别 |
|------|------|----------|
| 478M | ll | *(不在 repos.json 中)* |
| 475M | open-webui | ai-apps |
| 462M | git | dev-tools |
| 437M | dify | ai-apps |
| 386M | modded-nanogpt | ai-training |
| 382M | anthropic-cookbook | ai-apps |
| 336M | jax | ai-training |
| 294M | cuda-samples | dev-tools |
| 274M | sglang | ai-inference |
| 267M | codex | ai-agents |
| 264M | zed | dev-tools |
| 261M | fineract | dev-tools |
| 247M | ruff | dev-tools |
| 246M | nexa-sdk | ai-inference |
| 244M | verilator | dev-tools |
| 244M | Qwen2.5-VL | ai-models |
| 243M | voice-changer | ai-apps |
| 237M | vllm | ai-inference |
| 235M | Megatron-LM | ai-training |
| 216M | aider | ai-apps |
| 210M | opencode | ai-agents |
| 200M | iclaw | dev-tools |
| 198M | tutorials | ai-training |
| 195M | langchain | ai-apps |
| 181M | ktransformers | ai-inference |
| 173M | miu2d | dev-tools |
| 159M | netty | infra-network |
| 158M | desktop | dev-tools |
| 151M | gemini-cli | ai-agents |
| 146M | ComfyUI | ai-apps |
| 142M | transformers | ai-models |
| 138M | langfuse | ai-apps |
| 138M | anything-llm | ai-apps |
| 134M | terminal | dev-tools |
| 130M | quivr | infra-network |
| 127M | react | dev-tools |
| 124M | mcp | dev-tools |
| 119M | FlagEmbedding | ai-training |
| 116M | nmap | dev-tools |
| 112M | openwrt | infra-network |
| 110M | OpenHands | ai-agents |
| 108M | mlx-examples | ai-inference |
| 107M | h2ogpt | ai-apps |
| 102M | ollama | ai-inference |
| 102M | dubbo | dev-tools |
| 102M | diffusers | ai-training |

*(100MB 以下的已省略)*

## 我建议移除的项目

**首选移除项——在 MacBook Air 上可能不需要（体积大 + 特供 NVidia 或很少使用）：**

1. **TensorRT-LLM**（2.2G）——仅限 NVIDIA 的推理引擎，在 Mac 上无用
2. **openai-cookbook**（1.7G）——只是 Python 示例/文档
3. **evals**（1.6G）——OpenAI 评估框架
4. **greptimedb**（1.5G）——时序数据库，很少使用
5. **weaviate**（1.1G）——向量数据库
6. **LibreChat**（726M）——替代聊天 UI
7. **AutoGPT**（567M）——智能体，基本已过时
8. **warp**（789M）——Rust 终端源码（你已经有这个应用了）
9. **bun**（687M）——JS 运行时源码
10. **Telegram-iOS**（609M）——iOS 应用源码
11. **mlflow**（753M）——ML 实验跟踪
12. **crewAI**（701M）——智能体框架
13. **nanochat**（1.0G）——甚至不在 repos.json 中
14. **claw-code**（1.2G）——智能体

这样可以释放约 **16GB** 空间。

要我直接移除某些仓库吗？哪些应该保留，哪些应该移除？