---
audio: false
generated: true
image: false
lang: en
layout: post
title: Backend Detection Test Results Explained
translated: false
type: note
---

Question: What does this backend detection test output mean?

Answer:

This script is trying to infer **what inference backend** (vLLM, SGLang, TGI, OpenAI-compatible server, etc.) is running behind an OpenAI-compatible API. None of these methods are definitive—they're heuristics.

Let's go through it.

### 1. Model

```text
Model: tencent/hy3-preview
```

You're sending requests to a model named `tencent/hy3-preview`.

This tells us nothing about the backend. The same model could be served by:

* vLLM
* SGLang
* TensorRT-LLM
* TGI
* a custom inference stack

---

### 2. Proxy

```text
HTTP_PROXY=http://127.0.0.1:7890
```

Your requests are going through a local proxy (probably Clash, V2Ray, or similar).

Not related to inference.

---

### 3. Streaming request

```
Response id:
gen-1783677403-Ki1BBI5Ijd0hQgrOz3XX
```

Your script expected certain ID formats.

For example:

OpenAI often returns

```
chatcmpl-xxxxxxxx
```

vLLM commonly returns

```
chatcmpl-...
```

Some providers return

```
cmpl-...
```

Your provider returns

```
gen-1783677403-Ki1BBI5Ijd0hQgrOz3XX
```

which isn't recognized.

Therefore:

```
Backend:
unknown
```

This **does not mean the backend is unknown internally**.

It means

> "I cannot identify the backend from this ID format."

---

### 4. Delta keys

```
delta keys:
['content', 'role']
```

Streaming chunks looked like

```json
{
  "choices":[
    {
      "delta":{
          "role":"assistant",
          "content":"Hello"
      }
    }
  ]
}
```

Many servers do this.

For example:

* OpenAI
* vLLM
* SGLang
* LiteLLM
* TGI (OpenAI mode)

So this isn't enough to identify anything.

---

### 5. TTFT

```
TTFT:
4.319s
```

TTFT = Time To First Token.

This measures

```
network latency
+
queue
+
prefill
+
first decode
```

4.3 seconds is relatively high.

---

### 6. Server header

```
Server:
cloudflare
```

This is important.

Your request is reaching

```
You
 ↓
Cloudflare
 ↓
Provider
 ↓
Inference backend
```

Cloudflare hides the real server.

If it had said

```
Server: uvicorn
```

or

```
Server: nginx
```

or

```
Server: envoy
```

that might provide hints.

Cloudflare tells us almost nothing about the inference engine.

---

### 7. Prefix cache test

This is the most interesting part.

You sent two prompts:

```
Request A

<2000 tokens identical>

Question A
```

then

```
Request B

<same 2000 tokens>

Question B
```

Results:

```
Cold:
7.703s

Warm:
2.674s
```

TTFT became

```
2.674 / 7.703

≈ 0.347
```

Only **34.7%** of the original latency.

That strongly suggests the provider reused the KV cache for the shared prefix.

Your script therefore reports:

```
Likely cache HIT
```

---

## Why prefix caching helps

Without caching:

```
Prompt

token1
token2
...
token2000

↓

Transformer processes all 2000 tokens
↓

Generate answer
```

With caching:

```
Prompt A

2000 tokens
↓

Store KV cache
```

Later:

```
Prompt B

same 2000 tokens

↓

Reuse KV cache

↓

Only compute the new suffix
```

This often reduces TTFT by **2–10×**, depending on hardware and prompt length.

---

## Can we identify the backend?

Based on this output alone:

| Observation               | Meaning                            |
| ------------------------- | ---------------------------------- |
| `gen-...` response ID     | Custom API wrapper or gateway      |
| Cloudflare                | Hidden behind CDN                  |
| Standard OpenAI streaming | Many backends support this         |
| Prefix cache works        | Backend supports KV/prefix caching |

The evidence is **insufficient** to distinguish between:

* vLLM
* SGLang
* TensorRT-LLM
* TGI
* a proprietary inference engine

All of these can expose an OpenAI-compatible API and support prefix caching.

---

## What this probably tells you

The provider is likely using:

* an OpenAI-compatible API gateway,
* Cloudflare in front,
* an inference backend that supports prefix/KV cache,
* and a custom response ID format (`gen-...`).

The actual backend remains hidden, so your detection script correctly reports `unknown`.

References:

* vLLM Documentation — [https://docs.vllm.ai/](https://docs.vllm.ai/)
* SGLang Documentation — [https://docs.sglang.ai/](https://docs.sglang.ai/)
* OpenAI Chat Completions API — [https://platform.openai.com/docs/api-reference/chat](https://platform.openai.com/docs/api-reference/chat)
