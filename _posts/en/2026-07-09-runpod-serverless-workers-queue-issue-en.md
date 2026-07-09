---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Serverless Workers Queue Issue
translated: false
type: note
---

Question: Why are my RunPod Serverless requests staying "in queue" even though there are 2 running workers?

Answer:

This is **not normal**. If you have:

```
2 running workers
0 jobs in progress
2 jobs waiting in queue
```

then those workers are **not actually accepting requests**.

Normally it should look like:

```
2 running workers
1 job in progress
1 job waiting
```

or

```
2 running workers
2 jobs in progress
0 waiting
```

## Most likely causes

### 1. vLLM is still loading the model (most common)

The worker is "Running" from RunPod's perspective, but inside the container vLLM is still doing:

* downloading model
* loading weights
* allocating KV cache
* compiling CUDA kernels

If you're loading a 30B+ model, this can easily take several minutes.

Go to:

```
Workers
→ select a worker
→ Logs
```

If you see something like:

```
Downloading model...
Loading safetensors...
Initializing engine...
```

then this is expected.

---

### 2. Worker never became Ready

Sometimes the container started but your handler never reported readiness.

Typical logs:

```
Starting...
```

and then nothing.

or

```
Waiting for health check...
```

The request stays queued forever.

---

### 3. vLLM crashed during startup

Example:

```
CUDA out of memory

Killed

Segmentation fault

ImportError
```

RunPod may still be trying to restart workers while your requests remain queued.

---

### 4. Wrong endpoint configuration

For example:

* wrong port
* wrong health endpoint
* wrong handler
* container never listens

Then workers appear alive but cannot receive inference requests.

---

### 5. Model is larger than GPU memory

For example:

```
72B FP16
```

on

```
RTX 4090
16GB GPU
```

The worker repeatedly dies while RunPod keeps retrying.

---

## First thing I'd check

Open **Workers → Logs**.

The last lines should end with something similar to:

```
INFO Engine initialized
INFO Uvicorn running
INFO Ready
```

or

```
Server started
```

If instead they stop at

```
Loading checkpoint shards...
```

then you're simply waiting for model initialization.

---

## Your current situation

Since **both workers** are queued and **0 jobs are running**, I suspect one of these:

* ✅ workers are still loading the model (≈70% probability)
* ✅ startup failed (≈25%)
* ✅ endpoint configuration issue (≈5%)

---

If you can paste the **Worker Logs** (especially the last 50–100 lines), I can usually identify the exact cause within a minute.
