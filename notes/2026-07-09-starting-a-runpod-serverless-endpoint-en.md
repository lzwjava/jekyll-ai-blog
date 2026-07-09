---
audio: false
generated: true
image: false
lang: en
layout: post
title: Starting a RunPod Serverless Endpoint
translated: false
type: note
---

Question: How do I actually start a RunPod Serverless vLLM endpoint when it shows `0 running workers`, `0 jobs in progress`, and `0 jobs waiting in queue`?

Answer:

That status is **normal**. RunPod Serverless is **scale-to-zero**.

```
0 running workers
0 jobs
```

does **not** mean something is broken. It means:

* No GPU is currently allocated.
* No request has arrived.
* You're not paying for idle GPUs.

The lifecycle is:

```
Create Endpoint
        │
        ▼
0 workers (idle)
        │
        ▼
Send first request
        │
        ▼
RunPod allocates GPU
        │
        ▼
Downloads model
        │
        ▼
Starts vLLM
        │
        ▼
Processes request
        │
        ▼
Returns result
        │
        ▼
After idle timeout
        │
        ▼
Worker shuts down again
```

### Option 1 — Use the RunPod UI (easiest)

Open your endpoint:

```
Requests
```

Use something like:

```json
{
  "input": {
    "prompt": "Hello"
  }
}
```

Click **Run**.

The queue will become

```
1 waiting
```

then

```
1 running
```

then you'll see

```
1 worker
```

during execution. The first request may take a few minutes because RunPod must provision a GPU and download the model. ([Runpod Documentation][1])

---

### Option 2 — Use curl

```bash
curl -X POST \
  https://api.runpod.ai/v2/<ENDPOINT_ID>/runsync \
  -H "Authorization: Bearer <RUNPOD_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {
          "prompt": "Hello"
        }
      }'
```

That single request automatically starts a worker. ([Runpod Documentation][1])

---

### Option 3 — OpenAI-compatible API

The vLLM template also exposes an OpenAI-compatible API after the worker is running, so you can point the OpenAI SDK or LiteLLM/OpenWebUI at it. ([Runpod Documentation][2])

---

### If it stays at 0 workers forever

Then something is wrong. Check:

* Endpoint status is **Active**
* A GPU type is selected
* `MIN_WORKERS` isn't unintentionally set to 0 if you expected an always-warm worker
* The model name is correct (for example `Qwen/Qwen3-8B`)
* Hugging Face token is configured if the model is gated
* Endpoint logs for model download or OOM errors ([Runpod Documentation][1])

---

Since you've been experimenting with **SGLang** and **vLLM** on RunPod, I'd recommend sending a simple `runsync` request first. If you paste:

* the endpoint configuration,
* the selected GPU,
* the model name, and
* the endpoint logs,

I can usually identify the startup issue within a minute.

References:

* [RunPod: Deploy vLLM on Serverless](https://docs.runpod.io/serverless/vllm/get-started?utm_source=chatgpt.com)
* [RunPod vLLM Overview](https://docs.runpod.io/serverless/vllm/overview?utm_source=chatgpt.com)

[1]: https://docs.runpod.io/serverless/vllm/get-started?utm_source=chatgpt.com "Deploy vLLM on Runpod Serverless - Runpod Documentation"
[2]: https://docs.runpod.io/serverless/vllm/overview?utm_source=chatgpt.com "Overview - Runpod Documentation"