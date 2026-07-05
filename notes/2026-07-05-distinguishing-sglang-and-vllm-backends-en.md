---
audio: false
generated: true
image: false
lang: en
layout: post
title: Distinguishing SGLang and vLLM Backends
translated: false
type: note
---

Good question — yes, you can identify SGLang vs vLLM and measure prefix-cache behavior through the OpenAI-compatible API. Here's the practical breakdown:

1. How to Tell SGLang from vLLM via API Response

Both expose /v1/chat/completions, but there are detectable differences:

Aspect vLLM SGLang

id field "chatcmpl-<UUID>" Usually a bare 32-char hex string (no chatcmpl- prefix)

Streaming reasoning delta.reasoning_content (some versions) delta.reasoning (deep thinking models); SGLang also uses reasoning_content: null in first chunk

Server header Server: uvicorn (typical) Sometimes Server: sglang or absent; check /health or /v1/models response structure

Native /generate endpoint {"prompt": "...", "sampling_params": {...}} nested {"text": "...", "sampling_params": {...}} with return_logprob etc.

Quick heuristic: send one streaming request, inspect response.json()["id"]. If it doesn't start with chatcmpl-, it's very likely SGLang.

2. Testing Prefix Cache — Your Idea Is Correct

Your plan is the standard way:

1. Send Request A — long shared system prompt + unique suffix → measure TTFT & total latency (cold, no cache).
2. Send Request B — same long shared prefix + different suffix → measure TTFT again.
3. Compare:
   - Cache hit → TTFT of Request B drops dramatically (only the divergent suffix part is computed).
   - No cache / miss → TTFT of B ≈ A.

SGLang's RadixAttention matches at token level; vLLM's APC (with --enable-prefix-caching) matches at block/page level (typically 16-token blocks), so partial-block tails get recomputed.

Minimal Python test sketch:

from openai import OpenAI
import time

client = OpenAI(base_url="http://localhost:30000/v1", api_key="EMPTY")

SHARED_PREFIX = "你是一个资深Python工程师，请严格按下方要求作答。\n\n" * 200  # long shared part
SUFFIX_A = "问题A：打印1到10。"
SUFFIX_B = "问题B：打印斐波那契数列前10项。"

def ttft(messages):
    t0 = time.perf_counter()
    stream = client.chat.completions.create(
        model="your-model",
        messages=messages,
        max_tokens=64,
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            return time.perf_counter() - t0
    return None

print("Req 1 (cold):", ttft([{"role":"user","content": SHARED_PREFIX + SUFFIX_A}]))
print("Req 2 (cached prefix):", ttft([{"role":"user","content": SHARED_PREFIX + SUFFIX_B}]))


• vLLM needs --enable-prefix-caching at startup to show this effect.

• SGLang RadixAttention is on by default.

3. What Shows Up in User Experience

Dimension SGLang (RadixAttention) vLLM (APC, block-level)

Multi-turn chat / shared sys-prompt Near-immediate TTFT on 2nd+ turn, high hit rate TTFT improves if prefix aligns to block boundary, less aggressive

RAG / template prompts Excellent reuse across users with same template Depends on block alignment; may recompute tail tokens

Throughput under shared prefix Typically higher (less redundant KV compute) Good but generally lower cache efficiency for partial overlaps

OpenAI API fidelity Slightly behind vLLM on some edge fields (e.g. stream_options.include_usage older versions) Very close to official OpenAI spec

4. Server-Side Confirmation (If You Control the Deploy)

• SGLang server logs print KV Cache hit for prefix length XXX when RadixAttention hits.

- vLLM with --enable-prefix-caching logs prefix cache hit stats in its Prometheus metrics (vllm:prefix_cache_hit).

Bottom line: Your latency-based prefix-cache test is the right approach. To identify the backend, check the id format and any reasoning/reasoning_content delta fields in the streaming response. Let me know if you want a curl-based version or a more formal benchmark script!