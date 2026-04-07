---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gemma 4B Q5 Performance Review
translated: false
type: note
---

## Journey & Findings: gemma-4-E4B-it-Q5_K_M.gguf on RTX 4070

### What We Started With

- **Previous model**: `gemma-4-26B-A4B-it-UD-IQ2_M.gguf` — the 26B MoE model with aggressive IQ2_M quantization
- **New model**: `gemma-4-E4B-it-Q5_K_M.gguf` — 5.5GB, Q5_K_M quantization (much higher quality quant)
- **Hardware**: RTX 4070 (12GB VRAM), 20 layers offloaded to GPU, 32k context, port 8081

### The Switch

Killed the old process (PID 135703), launched the new one. Server came up cleanly in ~5 seconds with 4 slots, each allocated 32768 tokens context. No issues during model loading.

### Test 1: Moderate Prompt (~7.3k tokens)

- 200 repetitive topic descriptions
- **Result**: Success, 7320 prompt tokens processed
- Took ~14.8 seconds total
- Server stable

### Test 2: Heavy Prompt (~26k tokens)

- 310 paragraphs of dense technical text — pushing close to the 32k limit
- **Result**: Success, 26157 prompt tokens
- **Key discovery**: This is a **thinking model**. The response has `reasoning_content` (internal chain-of-thought) and `content` (final answer). With only 100-200 max_tokens, all budget went to thinking — the visible `content` was empty
- **Speed**: ~10.8 tokens/sec generation, ~92ms per token
- **Prompt caching worked**: second request hit cache (26156/26157 tokens cached), prompt eval dropped to 96ms for just 1 new token
- **Memory**: RSS grew from ~5GB to ~6.5GB under the heavy prompt — well within the machine's 64GB RAM

### Test 3: Over-Limit Prompt (~76k tokens)

- 800 paragraphs, blew past 32k context
- **Result**: Server returned HTTP 400 with a clear error message: "request (76612 tokens) exceeds the available context size (32768 tokens)"
- **No crash**, no hang, no corruption. Server continued serving normally after

### Key Findings

| Metric | Value |
|---|---|
| Model size on disk | 5.5 GB |
| Quantization | Q5_K_M (high quality) |
| RSS under load | ~6.5 GB |
| Generation speed | ~10.8 tok/s |
| Prompt eval (cached) | 96ms for 26k cached tokens |
| Thinking model | Yes — uses `reasoning_content` field |
| Stability | No crashes across all tests |
| Context limit handling | Graceful 400 error |

### Observations

1. **E4B vs 26B-A4B**: The E4B model name suggests this might be a smaller/different MoE configuration than the 26B-A4B you were running before. The Q5_K_M quant is significantly higher quality than IQ2_M — less compression artifacts, better output quality at the cost of larger file size.

2. **Thinking model behavior**: If you're using this via an API client, you need to account for thinking tokens eating into `max_tokens`. Set `max_tokens` higher (e.g., 1024+) to leave room for actual output after reasoning.

3. **Performance is solid**: ~10.8 tok/s is usable for interactive chat. The prompt caching is a nice bonus — repeat/similar prompts get near-instant prompt evaluation.

4. **No crash with 32k context**: The main question you asked — it handles long prompts fine. Server stays stable even when requests exceed the limit.