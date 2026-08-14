---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 诊断torch.compile的CUDA内存不足
translated: true
type: note
---

问题：为什么会出现这个 `torch.compile` / Inductor 错误，应该怎么做？

答案：

关键部分**不是** `scalar_tensor` 本身。

你真正的错误是：

```text
torch._dynamo.exc.BackendCompilerFailed:
backend='inductor' raised:
AcceleratorError: CUDA error: out of memory
```

有趣的是，它发生在 Inductor 编译你的代码时：

```python
loss = F.cross_entropy(
    logits.view(-1, logits.size(-1)),
    targets.view(-1),
    ignore_index=-1,
)
```

### 1. 正在发生什么

你可能会有这样的代码：

```python
model = torch.compile(model)
```

执行路径大致如下：

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

注意这里：

```text
While executing %scalar_tensor:
    aten.scalar_tensor.default
    args = (0,)
    device = cuda:0
```

这**并不意味着创建 `tensor(0)` 正在占用你的整个 GPU**。

Inductor 正在进行图级优化，恰好在评估这个节点时发现了 OOM。

因为 CUDA 操作是异步的，回溯中显示的操作也可能**晚于真正耗尽内存的操作**。

---

## 2. 为什么 `torch.compile` 会让这个问题变得令人困惑

不使用编译时：

```python
loss = F.cross_entropy(...)
```

大致执行：

```text
logits
  ↓
log_softmax
  ↓
NLLLoss
  ↓
loss
```

使用：

```python
model = torch.compile(model)
```

PyTorch 做的事情更接近于：

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

Inductor 可能在编译/运行时分配额外的临时缓冲区。

所以你可能遇到：

```text
normal eager mode       → fits
torch.compile(mode=...) → OOM
```

即使数学模型完全相同。

---

# 3. 我会做的第一件事

禁用编译：

```python
# model = torch.compile(model)

model = model.cuda()
```

运行一个训练步骤。

如果这样能正常工作：

```text
eager       ✓
torch.compile  ✗
```

那么你就把问题定位到了编译路径，而不是模型本身。

这是最快的诊断方法。

---

# 4. 然后检查实际的 GPU 内存

运行：

```bash
watch -n 0.5 nvidia-smi
```

以及在 Python 中：

```python
print(torch.cuda.memory_summary())
```

更有用的方式：

```python
print(
    f"allocated={torch.cuda.memory_allocated()/1024**3:.2f} GB",
    f"reserved={torch.cuda.memory_reserved()/1024**3:.2f} GB",
)
```

这两者的区别很重要：

```text
allocated
    memory currently occupied by tensors

reserved
    memory held by PyTorch's CUDA allocator
```

例如：

```text
allocated = 10.8 GB
reserved  = 11.9 GB
GPU       = 12 GB
```

你基本上已经接近极限了。

---

# 5. 如果你在 12 GB 4070 上运行 nanoGPT

这种情况尤其可能。

最危险的张量通常是：

```python
logits.shape
=
(B, T, vocab_size)
```

假设：

```text
B = 8
T = 1024
V = 50,000
```

那么：

```text
8 × 1024 × 50,000
= 409,600,000 elements
```

如果 logits 是 FP16：

```text
409.6M × 2 bytes
≈ 819 MB
```

如果是 FP32：

```text
409.6M × 4 bytes
≈ 1.64 GB
```

而这**仅仅是 logits**。

在训练过程中，你还有：

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

所以最终的投影层：

```python
logits = x @ lm_head.weight.T
```

可能就是所有内存突然爆掉的地方。

---

# 6. 特别重要的 nanoGPT 优化

如果你在训练 GPT 风格的模型，尝试减小：

```python
batch_size
block_size
```

例如：

```bash
--batch_size=4 \
--block_size=1024
```

而不是：

```bash
--batch_size=8 \
--block_size=1024
```

内存大致与以下内容成比例：

```text
B × T
```

对于许多激活张量来说。

所以：

```text
B: 8 → 4
```

可以将大部分激活内存几乎减半。

---

# 7. 也单独测试一下 `torch.compile`

尝试：

```python
model = torch.compile(model, backend="inductor")
```

如果那会 OOM，测试：

```python
# no compile
```

然后尝试：

```python
model = torch.compile(
    model,
    backend="inductor",
    mode="reduce-overhead",
)
```

`reduce-overhead` 可能会改变内存行为，因为 Inductor 会使用 CUDA graphs 或相关机制。

但不要盲目认为它更好。要对其进行基准测试。

---

# 8. 检查 OOM 是否确实来自 loss

一个非常有用的实验是：

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

如果内存在这里附近急剧增加：

```python
F.cross_entropy(...)
```

那么罪魁祸首很可能就是 logits/loss 这一路径。

---

# 9. 更好的解决方案：不要物化不必要的 logits

在 nanoGPT 训练中，输出投影是：

```python
logits = self.lm_head(x)
```

其中：

```text
x:      [B, T, C]
weight: [V, C]

logits: [B, T, V]
```

巨大的维度是：

```text
V = vocabulary size
```

如果内存紧张，一个非常有效的策略是分块计算 loss，而不是保存整个 `[B,T,V]` 张量。

概念上：

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

这会用计算/内核启动开销来换取更低的峰值内存。

对于 12 GB GPU，这可能比与 Inductor 斗争有用得多。

---

# 10. 同时验证混合精度

你需要类似这样的代码：

```python
with torch.autocast(
    device_type="cuda",
    dtype=torch.bfloat16,
):
    logits, loss = model(idx, targets)
```

或者如果 BF16 不适用于你的 GPU/模型，也可以使用 FP16。

检查：

```python
print(next(model.parameters()).dtype)
print(logits.dtype)
```

如果你意外看到：

```text
torch.float32
```

对于巨大的激活/logits，内存使用量大约是 FP16/BF16 的 **2 倍**。

---

# 11. 你回溯中的调试命令

你可以运行：

```bash
CUDA_LAUNCH_BLOCKING=1 python train.py
```

这会使 CUDA 执行同步。

通常情况下：

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

错误可能出现在 B 处，即使是由 A 引起的。

使用：

```bash
CUDA_LAUNCH_BLOCKING=1
```

你会更接近：

```text
launch A
wait
launch B
wait
```

所以回溯更加可信。

**但它无法解决 OOM。** 它只是帮助定位问题。

---

# 12. 我推荐的调试顺序

请严格按照这个顺序操作：

```bash
# 1. kill stale processes
nvidia-smi

# 2. run without compile
python train.py
```

如果急切模式（eager mode）正常工作：

```python
# 3. compile
model = torch.compile(model)
```

然后如果编译失败：

```bash
CUDA_LAUNCH_BLOCKING=1 python train.py
```

然后减小：

```text
batch_size
↓
block_size
```

然后检查：

```python
print(logits.shape)
print(logits.dtype)
print(torch.cuda.memory_summary())
```

最后测试：

```python
torch.cuda.empty_cache()
```

**注意：** `empty_cache()` 并不能解决真正内存不足的问题。它只会释放未使用的缓存块。

---

## 心智模型

关键的区别在于：

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

你的回溯表明**流程的最后部分达到了显存上限**。

这行代码：

```python
F.cross_entropy(...)
```

是可疑的，因为它操作的张量非常大：

```text
[B, T, vocab_size]
```

logits 张量，但 `scalar_tensor(device=cuda)` 这行几乎可以肯定是**观察到 OOM 的位置，而不一定是造成 OOM 的位置**。

如果你是在 **12 GB RTX 4070** 上运行 nanoGPT，我的首要猜测是**峰值激活/logits 内存 + Inductor 开销**，而不是 PyTorch 的 bug。

参考资料：

* [PyTorch `torch.compile` documentation](https://docs.pytorch.org/docs/stable/torch.compiler.html?utm_source=chatgpt.com)
* [PyTorch CUDA memory management](https://docs.pytorch.org/docs/stable/notes/cuda.html?utm_source=chatgpt.com#cuda-memory-management)
* [PyTorch Inductor](https://docs.pytorch.org/docs/stable/torch.compiler_inductor.html?utm_source=chatgpt.com)
* [PyTorch repository](https://github.com/pytorch/pytorch?utm_source=chatgpt.com)
