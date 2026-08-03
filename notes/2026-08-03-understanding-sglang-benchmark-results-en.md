---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding SGLang Benchmark Results
translated: false
type: note
---

Question: How to understand the output of an `sglang test` benchmark?

Answer:

This test is basically a **health check + latency benchmark** for your running SGLang inference server.

You have:

```
URL:      http://localhost:30010
Model:    Qwen/Qwen2.5-0.5B-Instruct
Max ctx:  32,768 tokens
Max out:  128 tokens per request
```

Meaning:

* SGLang server is running on port `30010`
* Model loaded:

  ```
  Qwen/Qwen2.5-0.5B-Instruct
  ```

  0.5B parameter instruction model
* Context window:

  ```
  32,768 tokens
  ```

  The model can theoretically read ~32k tokens in one request.
* Each request allows max generation:

  ```
  128 output tokens
  ```

---

## 1. Probe

```
Probe (non-stream): 20ms, 33 in / 3 out -> 'OK.'
```

This is a simple request:

Input:

```
33 tokens
```

Output:

```
3 tokens
```

Latency:

```
20ms
```

It checks:

* HTTP endpoint works
* tokenizer works
* model can generate
* response format is correct

Equivalent:

```bash
curl http://localhost:30010/generate \
  -d '{"text":"hello","max_new_tokens":3}'
```

---

## 2. Main benchmark table

Example:

```
case      input     TTFT    total    out    tok/s
tiny        11t      10ms    36ms      9    252.0
```

Each row sends a prompt of different size.

---

# Column explanation

## input

Example:

```
4,711t
```

means:

```
4,711 input tokens
```

Important:

Tokens ≠ words.

Roughly:

```
1 token ≈ 0.75 English words
```

So:

```
4711 tokens
≈ 3500 words
```

---

## TTFT

Time To First Token.

Example:

```
TTFT = 15ms
```

Meaning:

User sends request:

```
prompt
 |
 |
 v
SGLang
 |
 |
 v
first generated token
```

Time:

```
15ms
```

This measures:

* request overhead
* prompt processing
* KV cache initialization
* scheduler delay

For chat applications:

TTFT is very important.

A user feels:

```
100ms  -> instant
500ms  -> okay
2s     -> slow
```

---

## total

Total request time.

Example:

```
total = 218ms
```

Timeline:

```
request
 |
 |---- 14ms ----|
 first token

 |--------------|
 generation

 finish
```

Formula:

```
total ≈ TTFT + generation_time
```

---

## out

Generated tokens.

Example:

```
out = 67
```

The model generated:

```
67 tokens
```

---

## tok/s

Generation speed.

Example:

```
307.9 tok/s
```

Means:

after the first token:

```
model generates ~308 tokens/sec
```

For your setup this is extremely fast because:

* Qwen2.5 0.5B is tiny
* probably running on GPU
* SGLang has efficient runtime

---

## finish

```
stop
```

Means generation ended naturally.

Other possibilities:

```
length
```

means:

```
hit max_tokens limit
```

Example:

```json
max_tokens:128
```

and model produced exactly 128 tokens.

---

# Why does huge input have faster total time?

You see:

```
long:
1189 input
TTFT 14ms
total 218ms
67 output

huge:
4711 input
TTFT 15ms
total 125ms
35 output
```

It looks strange.

Why is 4711 tokens faster?

Because:

Generation length differs.

Compare:

```
long:
67 output tokens

huge:
35 output tokens
```

Generation dominates.

Approx:

```
time =
prompt processing
+
output generation
```

For SGLang:

prompt processing:

```
4711 tokens -> ~15ms
```

very optimized.

Generation:

```
67 tokens / 308 tok/s
≈217ms
```

matches:

```
total 218ms
```

---

# What this test proves

Your SGLang deployment:

```
[ OK ] tiny
[ OK ] short
[ OK ] medium
[ OK ] long
[ OK ] huge
```

means:

### 1. Server works

```
HTTP
 ↓
SGLang runtime
 ↓
CUDA kernel
 ↓
model
```

all good.

### 2. Long context works

You tested:

```
4,711 tokens
```

without failure.

Not full:

```
32,768
```

but enough to verify.

---

# For real LLM serving, you care about different numbers

A production benchmark usually measures:

## Prefill throughput

Processing input:

```
tokens/sec during prompt ingestion
```

Example:

```
5000 input tokens
```

How fast can GPU digest them?

## Decode throughput

Generation:

```
output tokens/sec
```

Your number:

```
~300 tok/s
```

for Qwen2.5-0.5B.

## Concurrent users

The important SGLang feature is:

continuous batching.

Example:

User A:

```
generate 100 tokens
```

User B arrives:

```
generate 100 tokens
```

SGLang batches them:

```
GPU:
A token
B token
A token
B token
...
```

instead of:

```
A complete
then B complete
```

---

For your previous GPU experiments (RTX 4070 12GB), a more meaningful next test would be:

```bash
python -m sglang.bench_serving \
  --backend sglang \
  --model Qwen/Qwen2.5-7B-Instruct \
  --num-prompts 100 \
  --request-rate 10
```

That measures real serving behavior:

```
requests/sec
latency p50/p95
input tok/s
output tok/s
```

This small `sglang test` only proves **"the engine works"**. It is like a unit test, not a production benchmark.
