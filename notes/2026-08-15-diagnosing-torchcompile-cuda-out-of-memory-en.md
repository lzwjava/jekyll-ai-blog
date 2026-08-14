---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diagnosing torch.compile CUDA Out of Memory
translated: false
type: note
---

Question: Why does this `torch.compile` / Inductor error happen, and what should you do?

Answer:

The important part is **not** `scalar_tensor` itself.

Your real error is:

```text
torch._dynamo.exc.BackendCompilerFailed:
backend='inductor' raised:
AcceleratorError: CUDA error: out of memory
```

The interesting part is that it happens while Inductor is compiling your:

```python
loss = F.cross_entropy(
    logits.view(-1, logits.size(-1)),
    targets.view(-1),
    ignore_index=-1,
)
```

### 1. What's happening

You probably have something like:

```python
model = torch.compile(model)
```

The execution path is approximately:

```text
model.forward()
    ↓
cross_entropy(logits, targets)
    ↓
torch.compile / Dynamo captures graph
    ↓
Inductor builds optimized graph
    ↓
constant folding
    ↓
CUDA allocation
    ↓
OOM
```

Notice this:

```text
While executing %scalar_tensor:
    aten.scalar_tensor.default
    args = (0,)
    device = cuda:0
```

That **doesn't mean creating `tensor(0)` is consuming your whole GPU**.

Inductor is doing graph-level optimization and happened to discover the OOM while evaluating this node.

Because CUDA operations are asynchronous, the operation shown in the traceback can also be **later than the operation that actually exhausted memory**.

---

## 2. Why `torch.compile` makes this confusing

Without compilation:

```python
loss = F.cross_entropy(...)
```

roughly executes:

```text
logits
  ↓
log_softmax
  ↓
NLLLoss
  ↓
loss
```

With:

```python
model = torch.compile(model)
```

PyTorch does something closer to:

```text
Python
  ↓
TorchDynamo
  ↓
FX graph
  ↓
Inductor
  ↓
kernel generation / fusion / constant folding
  ↓
CUDA kernels
```

Inductor may allocate additional temporary buffers during compilation/runtime.

So you can have:

```text
normal eager mode       → fits
torch.compile(mode=...) → OOM
```

even though the mathematical model is identical.

---

# 3. First thing I'd do

Disable compilation:

```python
# model = torch.compile(model)

model = model.cuda()
```

Run one training step.

If it works:

```text
eager       ✓
torch.compile  ✗
```

then you've isolated the problem to the compiled path rather than your model itself.

This is the fastest diagnostic.

---

# 4. Then check actual GPU memory

Run:

```bash
watch -n 0.5 nvidia-smi
```

and in Python:

```python
print(torch.cuda.memory_summary())
```

More useful:

```python
print(
    f"allocated={torch.cuda.memory_allocated()/1024**3:.2f} GB",
    f"reserved={torch.cuda.memory_reserved()/1024**3:.2f} GB",
)
```

The distinction matters:

```text
allocated
    memory currently occupied by tensors

reserved
    memory held by PyTorch's CUDA allocator
```

For example:

```text
allocated = 10.8 GB
reserved  = 11.9 GB
GPU       = 12 GB
```

You are basically at the limit.

---

# 5. If you're running nanoGPT on your 12 GB 4070

This is especially likely.

The dangerous tensor is usually:

```python
logits.shape
=
(B, T, vocab_size)
```

Suppose:

```text
B = 8
T = 1024
V = 50,000
```

Then:

```text
8 × 1024 × 50,000
= 409,600,000 elements
```

If logits are FP16:

```text
409.6M × 2 bytes
≈ 819 MB
```

If FP32:

```text
409.6M × 4 bytes
≈ 1.64 GB
```

And that's **just logits**.

During training you additionally have:

```text
model parameters
gradients
optimizer states
activations
attention intermediates
MLP intermediates
logits
cross entropy temporaries
Inductor temporaries
CUDA workspace
```

So the final projection:

```python
logits = x @ lm_head.weight.T
```

can be the point where everything suddenly blows up.

---

# 6. The particularly important nanoGPT optimization

If you're training a GPT-style model, try reducing:

```python
batch_size
block_size
```

For example:

```bash
--batch_size=4 \
--block_size=1024
```

instead of:

```bash
--batch_size=8 \
--block_size=1024
```

Memory roughly scales with:

```text
B × T
```

for many activation tensors.

So:

```text
B: 8 → 4
```

can nearly halve a large portion of activation memory.

---

# 7. Also test `torch.compile` separately

Try:

```python
model = torch.compile(model, backend="inductor")
```

If that OOMs, test:

```python
# no compile
```

Then try:

```python
model = torch.compile(
    model,
    backend="inductor",
    mode="reduce-overhead",
)
```

`reduce-overhead` can change memory behavior because Inductor uses CUDA graphs / related mechanisms.

But don't blindly assume it's better. Benchmark it.

---

# 8. Check whether the OOM is actually from the loss

A very useful experiment is:

```python
# temporarily
logits = model(idx)

print(logits.shape)
print(logits.dtype)
print(
    torch.cuda.memory_allocated() / 1024**3,
    torch.cuda.memory_reserved() / 1024**3,
)

loss = F.cross_entropy(
    logits.view(-1, logits.size(-1)),
    targets.view(-1),
    ignore_index=-1,
)
```

If memory jumps dramatically around:

```python
F.cross_entropy(...)
```

then the culprit is likely the logits/loss path.

---

# 9. Better solution: don't materialize unnecessary logits

For nanoGPT training, the output projection is:

```python
logits = self.lm_head(x)
```

where:

```text
x:      [B, T, C]
weight: [V, C]

logits: [B, T, V]
```

The huge dimension is:

```text
V = vocabulary size
```

If memory is tight, one very effective strategy is to compute the loss in chunks instead of holding the entire `[B,T,V]` tensor.

Conceptually:

```python
x = x.view(B * T, C)
targets = targets.view(B * T)

losses = []

for x_chunk, y_chunk in zip(
    x.split(1024),
    targets.split(1024),
):
    logits = self.lm_head(x_chunk)
    losses.append(F.cross_entropy(logits, y_chunk))

loss = torch.stack(losses).mean()
```

This trades compute/kernel-launch overhead for lower peak memory.

For a 12 GB GPU, this can be much more useful than fighting Inductor.

---

# 10. Also verify mixed precision

You want something like:

```python
with torch.autocast(
    device_type="cuda",
    dtype=torch.bfloat16,
):
    logits, loss = model(idx, targets)
```

or FP16 if BF16 isn't appropriate for your GPU/model.

Check:

```python
print(next(model.parameters()).dtype)
print(logits.dtype)
```

If you unexpectedly see:

```text
torch.float32
```

for huge activations/logits, memory usage can be roughly **2×** FP16/BF16.

---

# 11. The debugging command in your traceback

You can run:

```bash
CUDA_LAUNCH_BLOCKING=1 python train.py
```

This makes CUDA execution synchronous.

Normally:

```text
Python A
  ↓
launch CUDA kernel A
  ↓
Python B
  ↓
launch CUDA kernel B
  ↓
CUDA reports error
```

The error may appear at B even though A caused it.

With:

```bash
CUDA_LAUNCH_BLOCKING=1
```

you get much closer to:

```text
launch A
wait
launch B
wait
```

so the traceback is more trustworthy.

**But it won't solve the OOM.** It only helps locate it.

---

# 12. My recommended debugging sequence

Do this in exactly this order:

```bash
# 1. kill stale processes
nvidia-smi

# 2. run without compile
python train.py
```

If eager works:

```python
# 3. compile
model = torch.compile(model)
```

Then if compile fails:

```bash
CUDA_LAUNCH_BLOCKING=1 python train.py
```

Then reduce:

```text
batch_size
↓
block_size
```

Then inspect:

```python
print(logits.shape)
print(logits.dtype)
print(torch.cuda.memory_summary())
```

And finally test:

```python
torch.cuda.empty_cache()
```

**Note:** `empty_cache()` isn't a solution to genuinely insufficient memory. It only releases unused cached blocks.

---

## The mental model

The key distinction is:

```text
Your model's mathematical memory
            +
PyTorch runtime memory
            +
Inductor compilation/runtime buffers
            +
CUDA workspace
            =
actual peak VRAM
```

Your traceback says the **last part of the pipeline hit the VRAM ceiling**.

The line:

```python
F.cross_entropy(...)
```

is suspicious because it operates on the enormous:

```text
[B, T, vocab_size]
```

logits tensor, but the `scalar_tensor(device=cuda)` line is almost certainly **where the OOM was observed, not necessarily where it was caused**.

If this is your nanoGPT run on a **12 GB RTX 4070**, my first bet would be **peak activation/logit memory + Inductor overhead**, not a PyTorch bug.

References:

* [PyTorch `torch.compile` documentation](https://docs.pytorch.org/docs/stable/torch.compiler.html?utm_source=chatgpt.com)
* [PyTorch CUDA memory management](https://docs.pytorch.org/docs/stable/notes/cuda.html?utm_source=chatgpt.com#cuda-memory-management)
* [PyTorch Inductor](https://docs.pytorch.org/docs/stable/torch.compiler_inductor.html?utm_source=chatgpt.com)
* [PyTorch repository](https://github.com/pytorch/pytorch?utm_source=chatgpt.com)