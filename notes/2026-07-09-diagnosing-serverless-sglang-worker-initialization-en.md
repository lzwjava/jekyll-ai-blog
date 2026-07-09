---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diagnosing Serverless SGLang Worker Initialization
translated: false
type: note
---

Question: Why are my RunPod Serverless SGLang workers stuck in `initializing` with `0 running workers` and `2 jobs waiting in queue`?

Answer:

Your endpoint hasn't finished starting. The important part is:

```
0 running workers
2 jobs waiting in queue

Worker 1: initializing
Worker 2: initializing
```

This means **the Kubernetes pods never became Ready**, so no worker is available to process requests.

For SGLang on an RTX 4090, the most common causes are:

| Cause                        | Symptoms                    | Check       |
| ---------------------------- | --------------------------- | ----------- |
| Model download still running | `initializing` for 5–30 min | Worker logs |
| Hugging Face authentication  | 401/403 errors              | Logs        |
| Out of disk space            | Download fails              | Logs        |
| Container crashes            | Restart loop                | Worker logs |
| CUDA/OOM                     | Worker dies before Ready    | Logs        |
| Wrong startup command        | Never starts server         | Logs        |

## 1. Look at the Worker logs

Don't look at the endpoint logs first.

Go to

```
Workers
    ↓
click a worker
    ↓
Logs
```

or

```
Releases
    ↓
Latest
    ↓
Logs
```

The last 20–50 lines usually tell you exactly why initialization failed.

Typical messages are:

```
Downloading model...
```

which means just wait.

Or

```
401 Unauthorized
```

meaning your `HF_TOKEN` is missing.

Or

```
CUDA out of memory
```

meaning the model is too large.

Or

```
Killed
```

meaning the container exceeded RAM or was OOM-killed.

---

## 2. Which model are you loading?

Earlier you mentioned

```
unsloth/gemma-4-e4b-it-gguf
```

If you're still trying to run that in SGLang, that's likely the issue.

SGLang **does not serve GGUF models directly**.

It expects Hugging Face Transformers checkpoints, such as:

```
Qwen/Qwen3-8B
meta-llama/Llama-3.1-8B-Instruct
Qwen/Qwen2.5-7B-Instruct
```

If you specify a GGUF model, initialization may fail.

---

## 3. Is the model gated?

If using models like

```
meta-llama/*
google/gemma*
```

you must provide

```
HF_TOKEN=<YOUR_TOKEN>
```

Otherwise the worker cannot download weights.

---

## 4. Is the model simply huge?

An RTX 4090 has **24 GB VRAM**.

Approximate requirements:

* 7B FP16 → ~14 GB ✅
* 8B BF16 → ~16 GB ✅
* 14B FP16 → ~28 GB ❌
* 27B → ❌
* 70B → impossible

If you accidentally selected a large model, initialization will never succeed.

---

## 5. Is it still downloading?

The first startup can easily take

* 5 minutes
* 10 minutes
* 20+ minutes

depending on:

* model size
* Hugging Face speed
* region
* cache

The status remains

```
initializing
```

until the download finishes.

---

## What I need to diagnose it

Please provide **either**:

1. the last **50 lines** of the worker logs, or
2. your endpoint configuration:

   * model name
   * environment variables
   * startup command

With those, I can usually identify the problem within a minute.
