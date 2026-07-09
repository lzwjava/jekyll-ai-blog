---
audio: false
generated: true
image: false
lang: en
layout: post
title: From Training to Serving AI
translated: false
type: note
---

Question: You deployed an SGLang Serverless endpoint on RunPod successfully, while vLLM wasn't working. Is that a good direction? Right?

Answer:

Yes. From what you posted, your **SGLang Serverless deployment is working**.

Evidence:

* Your request status is `"COMPLETED"`.
* A worker processed the request:

  * `"workerId": "grr2baqhs9xjvr"`
* The model generated a valid OpenAI-compatible response:

  ```json
  {
    "object": "chat.completion",
    "model": "HuggingFaceTB/SmolLM2-1.7B-Instruct",
    "choices": [...]
  }
  ```

* The endpoint returned usage statistics (`prompt_tokens`, `completion_tokens`, etc.), meaning the inference stack completed end-to-end.

So your deployment pipeline is:

```
Client
    ↓
RunPod Serverless Endpoint
    ↓
SGLang Worker
    ↓
HF Model
    ↓
OpenAI-compatible JSON
```

That's exactly what you want.

As for **vLLM vs. SGLang**, the landscape in mid-2026 looks roughly like this:

* **vLLM**

  * Excellent general-purpose inference engine
  * Very mature OpenAI-compatible server
  * Huge ecosystem
  * Strong continuous batching

* **SGLang**

  * Optimized for agentic workloads
  * Faster structured decoding
  * Better support for reasoning models and tool use
  * Increasing adoption by newer model releases

Many recent open-weight reasoning models (including several Tencent Hunyuan releases and other frontier open models) provide first-class SGLang support, so it's not surprising that you found SGLang to be the smoother path for those models.

Since you're building AI infrastructure and agents, learning **both** is valuable:

```
vLLM
    ↓
general inference
OpenAI API
batch serving

SGLang
    ↓
reasoning
tool calling
agents
structured generation
```

From your recent conversations, you've now gone through the whole deployment cycle:

* ✅ trained a GPT model from scratch
* ✅ experimented with vLLM
* ✅ deployed an SGLang Serverless endpoint on RunPod
* ✅ exposed an OpenAI-compatible API endpoint

That means you're moving beyond model training into **LLM serving infrastructure**, which is another core piece of the stack.

The next natural step would be to benchmark your endpoint:

```bash
# latency
time curl ...

# throughput
hey -n 1000 -c 20 ...

# or
wrk

# streaming latency
curl -N ...
```

Measure metrics like:

* Time to First Token (TTFT)
* tokens/sec
* concurrent request throughput
* cold-start time
* cost per 1M output tokens

Those numbers become much more informative than simply verifying that the endpoint responds.
