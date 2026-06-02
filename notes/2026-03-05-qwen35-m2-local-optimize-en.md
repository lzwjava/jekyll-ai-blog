---
audio: false
generated: true
image: false
lang: en
layout: post
title: Speeding Up Local Qwen3.5 on M2
translated: false
type: note
---

Question: Why does `ollama run qwen3.5:9b` feel slow on a MacBook Air M2 compared to fast online Grok or Mistral, and how can it be improved? Also, do many people run local models?

Answer:

**Yes, `qwen3.5:9b` can still feel noticeably slower on a MacBook Air M2 (especially the base 8GB or 16GB configs) compared to the near-instant streaming of online Grok, Mistral, or similar cloud services — but it's often usable, and many optimizations help close the gap significantly in 2026.**

### Typical Real-World Speed on MacBook Air M2

- Ollama with Metal acceleration (default on Apple Silicon): **~25–45 tokens/second** (t/s) for generation on 16GB M2 Air, depending on context length, quantization, and prompt complexity.
  - Short responses feel quick (~2–5 seconds for a paragraph).
  - Longer or complex reasoning → 10–30+ seconds, which feels "slow" vs. cloud's sub-second start + fast streaming.
- Online services (Grok, Mistral, GPT, Claude): 80–200+ t/s equivalent feel due to massive server GPU clusters, optimized streaming, and no local thermal/power limits.
- MacBook Air M2 specifics: Fanless design → thermal throttling after 1–2 minutes of heavy use drops speed 20–40%. Base M2 has fewer GPU cores than Pro/Max chips.

Many people do run local models in 2026 — local LLM usage has grown massively (tens of millions regularly use tools like Ollama/LM Studio/MLX on personal hardware), driven by privacy, zero cost, offline access, and models like Qwen3.5 rivaling older cloud frontiers. It's especially popular among developers, researchers, and privacy-focused users, though most casual users still prefer cloud for raw speed/convenience.

### How to Improve Speed on Your MacBook Air M2

1. **Use a lighter quantization or smaller model variant**
   - Stick with the default Q4_K_M (~6.6GB), but try Q3_K_M or Q2_K if available (faster, slightly lower quality).
   - Switch to even smaller Qwen3.5 variants: 4B or 2B models run 2–3× faster (~50–80+ t/s) with almost no noticeable quality drop for simple tasks.

2. **Optimize Ollama settings**
   - Limit context size: Edit `~/.ollama/config` or use `--num_ctx 2048` (or 4096 max) to reduce KV cache memory/speed hit.
   - Set fewer threads/parallel: `OLLAMA_NUM_PARALLEL=1` and `OLLAMA_NUM_THREADS=4–6` (prevents overload on Air's limited cores).
   - Force Metal GPU: Ensure `OLLAMA_ORIGINS=*` and Metal is active (default, but confirm no Rosetta).
   - Update Ollama to latest version — 2026 releases have big Metal improvements.

3. **Reduce thermal throttling (critical for fanless Air)**
   - Run in low-power mode off, keep vents clear, use on hard surface.
   - Short bursts only — pause between long generations.
   - Some users disable GPU offload (`num_gpu: 0`) for CPU-only (slower initially but less heat buildup).

4. **Switch to faster frontends or engines**
   - Try **MLX** framework (Apple-optimized): Qwen3.5-9B hits **50–65 t/s** on M2 (faster than Ollama in many tests).
   - Use LM Studio or similar GUI — often feels snappier with streaming + better caching.
   - For API-based apps (e.g., Continue.dev, VS Code), set `"stream": false` if streaming lags badly.

5. **General tips**
   - Close all other apps to free unified memory (16GB+ recommended; 8GB struggles).
   - Keep macOS and Ollama updated for Metal/MLX gains.
   - For coding/chat: Use models like Qwen3.5-Coder variants if available — optimized and fast.

With these tweaks, many M2 Air users report "good enough" daily use (faster than early 2024 local attempts), though cloud still wins for ultra-responsive feel. If speed is priority #1, cloud remains king; for privacy/offline, local (with optimizations) is very viable in 2026.

References:

- [Ollama Qwen3.5:9b model page](https://ollama.com/library/qwen3.5:9b)
- [Best Local LLMs on Apple Silicon 2026 guide](https://apxml.com/posts/best-local-llm-apple-silicon-mac)
- [Reddit discussions on Ollama performance on M2 Air](https://www.reddit.com/r/ollama/comments/1n7uhkv/hows_your_experience_running_ollama_on_apple)
- [MLX vs Ollama speed comparison on M2](https://x.com/StephanFerraro/status/2028723111386915055)
- [Local LLM adoption trends 2026](https://datareportal.com/reports/digital-2026-one-billion-people-using-ai)
