---
audio: false
generated: true
image: false
lang: en
layout: post
title: Local Qwen 3.5 27B oMLX Performance
translated: false
type: note
---

Question: How is the local performance of the Qwen 3.5 27B model distilled from Claude 4.6 Opus, particularly when run using oMLX?

Answer:
The **Qwen 3.5 27B Claude 4.6 Opus Reasoning Distill** (often referred to by the community as "Qwopus") has gained significant traction for its exceptional balance of size and intelligence. When paired with **oMLX** (an open-source MLX inference server optimized for Apple Silicon), it creates a highly capable local development environment.

Here is a breakdown of its performance and capabilities based on recent community testing:

### 1. Coding and Agentic Capabilities
* **AI Assistants Integration:** The model is highly praised for driving AI coding assistants like Cursor and OpenCode. Users report that it handles plan mode, agent mode, and ask mode right out of the box with minimal configuration.
* **Tool Calling:** It is highly adept at correct tool calling for tasks such as writing multiple Python scripts, debugging, testing, and executing code.
* **Comparisons:** The local community generally considers this 27B dense model superior to the larger Qwen 3.5 35B MoE (Mixture of Experts) for pure coding tasks. Many users compare its capabilities to frontier models like Gemini 3 Flash and state that it works almost as well as Claude Sonnet for guided refactoring and sub-agent workflows.

### 2. Hardware and VRAM Efficiency
* **Resource Requirements:** A 4-bit quantized version of the 27B model requires roughly 17GB to 22GB of VRAM. This makes it a perfect sweet spot for users with 24GB–32GB discrete GPUs (like an RTX 3090/4090) or Apple Silicon Macs with unified memory.
* **Speed:** On high-end consumer hardware like an RTX 4090 running `llama.cpp`, users are seeing roughly 2,400 tokens per second for prefill and around 40 tokens per second for generation. Speeds on M-series Macs are also highly respectable due to MLX framework optimizations.

### 3. The oMLX Advantage on Apple Silicon
If you are running this model on a Mac using oMLX, the performance is heavily augmented by specific architectural features:
* **Paged SSD Caching:** oMLX persists the KV cache across a hot in-memory tier and a cold SSD tier. This means that if you change context mid-conversation or return to a previous coding session, past context is restored instantly from the SSD instead of being recomputed. This is a massive time-saver for long coding sessions.
* **Continuous Batching:** It natively supports continuous batching and seamless integration with OpenAI-compatible clients, making it incredibly stable for local API usage without the model "overthinking" or looping endlessly.

Overall, the Claude 4.6 Opus distilled version of Qwen 3.5 27B is currently considered one of the most practical and capable open-weights models for daily, local "vibe coding," provided you give it proper planning and clear context.

References:
* [Distilled qwen 3.5 27b is surprisingly good at driving Cursor. : r/LocalLLaMA - Reddit](https://www.reddit.com/r/LocalLLaMA/comments/1s2ql21/distilled_qwen_35_27b_is_surprisingly_good_at/)
* [Running Qwen3.5-27B locally as the primary model in OpenCode : r/LocalLLaMA - Reddit](https://www.reddit.com/r/LocalLLaMA/comments/1s7p0u9/running_qwen3527b_locally_as_the_primary_model_in/)
* [GitHub - jundot/omlx: LLM inference server with continuous batching & SSD caching for Apple Silicon — managed from the macOS menu bar](https://github.com/jundot/omlx)
* [oMLX - open-source MLX inference server with paged SSD caching for Apple Silicon : r/LocalLLaMA - Reddit](https://www.reddit.com/r/LocalLLaMA/comments/1r3qwyi/omlx_opensource_mlx_inference_server_with_paged/)
