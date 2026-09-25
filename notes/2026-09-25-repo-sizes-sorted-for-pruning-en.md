---
audio: false
generated: true
image: false
lang: en
layout: post
title: Repo sizes sorted for pruning
translated: false
type: note
---

Here's a full breakdown of the repos from `repos.json` sorted by size. I'll organize it clearly so you can decide what to prune.

## Repos from `repos.json` sorted by disk usage

**📦 >1GB (top candidates to remove):**

| Size | Repo | Category |
|------|------|----------|
| **3.4G** | Qwen2.5-Coder | ai-models |
| **2.2G** | TensorRT-LLM | ai-inference |
| **1.7G** | openai-cookbook | ai-apps |
| **1.6G** | evals | ai-models |
| **1.5G** | greptimedb | infra-network |
| **1.2G** | litellm | ai-apps |
| **1.2G** | claw-code | ai-agents |
| **1.1G** | weaviate | infra-network |

**📦 500MB–1GB:**

| Size | Repo | Category |
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

**📦 100–500MB:**

| Size | Repo | Category |
|------|------|----------|
| 478M | ll | *(not in repos.json)* |
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

*(rest under 100MB omitted)*

## My recommendations for removal

**Top picks — likely not needed on MacBook Air (big + NVidia-specific or rarely used):**

1. **TensorRT-LLM** (2.2G) — NVIDIA-only inference engine, useless on Mac
2. **openai-cookbook** (1.7G) — just Python examples/docs
3. **evals** (1.6G) — OpenAI eval framework
4. **greptimedb** (1.5G) — time-series DB, rarely used
5. **weaviate** (1.1G) — vector DB
6. **LibreChat** (726M) — chat UI alternative
7. **AutoGPT** (567M) — agent, largely outdated
8. **warp** (789M) — Rust terminal source (you already have the app)
9. **bun** (687M) — JS runtime source
10. **Telegram-iOS** (609M) — iOS app source
11. **mlflow** (753M) — ML experiment tracking
12. **crewAI** (701M) — agent framework
13. **nanochat** (1.0G) — not even in repos.json
14. **claw-code** (1.2G) — agent

That would free up **~16GB**.

Want me to go ahead and remove specific ones? Which ones should I keep vs remove?
