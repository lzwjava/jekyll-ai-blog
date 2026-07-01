---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimize by Doing Not Just Reading
translated: false
type: note
---

**Question:** For optimization learning (e.g., AMD ROCm kernel optimization), the key is to find something real to optimize and iterate with AI assistance, rather than just reading — is that right?

**Answer:**

Yes, exactly. This is the Karpathy principle applied to systems work:

> *"Don't be a tourist. Write the code."*

Reading ROCm docs or CUDA papers gives you vocabulary. Actually profiling and optimizing a real kernel gives you **intuition** — and intuition is what compounds.

## The Learning Loop That Works

```
Pick a real bottleneck → measure it → form hypothesis →
change code → measure again → ask AI to explain the delta → repeat
```

The AI is most useful **inside the loop**, not before it. You don't ask "explain ROCm memory coalescing" in the abstract — you paste your HIP kernel, your `rocprof` output, and ask "why is this 3x slower than expected?"

## Concrete Example: ROCm Kernel Optimization

**Step 1: Find something real**

```python
# You're running a transformer — profile the attention kernel
import torch
x = torch.randn(32, 512, 512).to("cuda")  # ROCm = same API

# Measure
torch.cuda.synchronize()
start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)
start.record()
out = torch.softmax(x @ x.transpose(-1,-2), dim=-1) @ x
end.record()
torch.cuda.synchronize()
print(f"{start.elapsed_time(end):.2f} ms")
```

**Step 2: Write a naive HIP kernel**

```cpp
__global__ void naive_matmul(float* A, float* B, float* C, int N) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    float sum = 0.0f;
    for (int k = 0; k < N; k++)
        sum += A[row * N + k] * B[k * N + col];
    C[row * N + col] = sum;
}
```

**Step 3: Profile with rocprof**

```bash
rocprof --stats -o profile.csv ./my_kernel
# Look at: FETCH_SIZE, L2CacheHit, wavefront occupancy
```

**Step 4: Ask AI with evidence**

```
Here's my kernel: [paste]
Here's my rocprof output: [paste]
L2 hit rate is 23%. My hypothesis is that the B matrix access
pattern is non-coalesced. Is that right? What's the fix?
```

Now you're using AI as a **senior engineer pair**, not a textbook.

## The Real Insight

Most optimization knowledge is **not in the reading** — it's in the gap between:

- what you *thought* would be fast
- what the profiler *says* is actually happening

That gap is where learning lives. AI accelerates closing it because you can explain the gap and get a targeted hypothesis in 30 seconds instead of digging through docs for 3 hours.

## Applied to Your Situation

You train GPT-2 on H100/H200. That's your real workload. Concrete things to optimize right now:

| Target | Tool | What you'll learn |
| --- | --- | --- |
| Attention FLOP efficiency | `nsys` / `rocprof` | Memory bandwidth vs compute bound |
| DataLoader bottleneck | `py-spy` | CPU/GPU pipeline overlap |
| All-reduce in DDP | NCCL logs | Communication hiding |
| Flash Attention vs naive | Triton kernel | Tiling, SRAM usage |

Each of these is a 1-week project that will teach you more than a month of reading optimization papers — because you'll have **numbers** to explain, not abstractions.

The reading then becomes a reference, not the lesson.
