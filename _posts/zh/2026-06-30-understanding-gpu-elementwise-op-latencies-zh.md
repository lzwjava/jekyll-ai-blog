---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解GPU逐元素操作延迟
translated: true
type: note
---

问题：请解释这些针对1024×1024 FP16张量的逐元素/运算延迟数据，并确认单位（μs是否等于1×10⁻⁹秒？）。

回答：

首先，关于单位。不——μs是**微秒 = 1×10⁻⁶秒**。1×10⁻⁹秒是**纳秒（ns）**。因此：

```
1 秒   = 1000 毫秒
1 毫秒 = 1000 微秒   (10^-3 秒)
1 微秒 = 1000 纳秒   (10^-6 秒)
1 纳秒 = 1000 皮秒   (10^-9 秒)
```

你看到的约4–7微秒 ≈ 每个操作4000–7000纳秒。

## 这些数字实际测量的是什么

一个1024×1024的FP16张量 = 100万个元素 × 2字节 = **2 MB**。关键洞察：这些操作大部分是**内存带宽受限，而非计算受限**。GPU并非忙于执行数学运算——而是忙于将2 MB数据移入和移出HBM。

### Roofline模型验证——为什么add/mul/relu约4微秒

像`add`这样的逐元素操作会：

- 读取2 MB（输入A）+ 2 MB（输入B）= 4 MB
- 写入2 MB（输出）
- 总数据流量 ≈ 6 MB
- FLOPs = 100万（每个元素一次加法）→ 微不足道

在RTX 4070（约480 GB/s）或MI300X（约5.3 TB/s）上，下限是`字节数 / 带宽`：

```python
bytes_moved = 6e6          # 6 MB for a+b -> c
bw_4070     = 480e9        # B/s
bw_mi300x   = 5.3e12

print(bytes_moved / bw_4070  * 1e6, "μs")  # ~12.5 μs（理论下限）
print(bytes_moved / bw_mi300x * 1e6, "μs")  # ~1.1 μs
```

你看到的约4微秒意味着高带宽GPU（MI300X级别，或使用了读取更少数据的融合内核）。关键在于：**算术强度约为0.17 FLOP/字节**——极度受内存限制。现代GPU在计算roofline处可达到100+ FLOP/字节，因此你使用的ALU不到1%。一旦数据到达，操作立即完成。

### 为什么softmax（约7微秒）和layer_norm（约6微秒）耗时更多

这些是**归约操作**——它们无法像`add`那样通过单次流式传输完成：

- **softmax**：需要先对行取`max`（数值稳定性），然后计算`exp`，再计算`sum`，最后做除法。逻辑上需要对数据进行3次遍历（max、sum、归一化），尽管好的内核会将其融合为约2次读取。更多的数据流量+同步=更高的延迟。
- **layer_norm**：在归一化之前需要计算均值和方差（两次归约）。同样是多遍操作。

```python
# softmax前向传播，融合内核将"安全"的3遍逻辑压缩
def softmax(x):           # x: [N, D], 沿D维度归约
    m = x.max(-1, keepdim=True).values      # 第1遍：max
    e = (x - m).exp()                        # 第2遍：exp
    return e / e.sum(-1, keepdim=True)       # 第3遍：sum + div
```

相比`add`多出的约50–75%延迟来自额外的读取操作和跨线程束归约（warp shuffle + 共享内存），而非`exp`计算本身昂贵。

### 为什么matmul*仅*约6微秒——令人惊讶

朴素计算下，一个1024³的matmul需要**2·N³ = 21亿FLOP**，而`add`只需100万FLOP——计算量相差2000倍。然而延迟却处于同一量级。为什么？

因为matmul是这里唯一**受计算限制且硬件为此优化**的操作：

```python
flops = 2 * 1024**3        # 2.1e9
# MI300X FP16约1300 TFLOP/s（含稀疏性/张量核心）
print(flops / 1.3e15 * 1e6, "μs")   # ~1.6 μs 计算下限
```

张量核心（NVIDIA）/矩阵核心（MI300X上的CDNA）在约1–2微秒内完成乘加运算；其余时间是启动开销和分块。对于方形matmul，算术强度为`N/3 ≈ 341 FLOP/字节`——远超计算roofline，因此ALU实际上是瓶颈（这是理想情况）。

## 需要记住的心智模型

```
                 算术强度              瓶颈                为什么延迟大致相等
add/mul/relu     ~0.17 FLOP/字节      内存带宽            2 MB输入/输出占主导
softmax          ~0.2  FLOP/字节      内存 + 归约         额外遍历/同步
layer_norm       ~0.2  FLOP/字节      内存 + 归约         均值和方差遍历
matmul           ~341  FLOP/字节      计算（张量核心）    N³ FLOP但硬件能消化
```

在这些小规模下，每个数字中很大一部分也是**固定的内核启动开销**（主机→设备路径约2–5微秒）。这就是为什么无论操作多么简单，延迟都不会低于约4微秒——你遇到了启动下限，而这正是**内核融合**（FlashAttention融合softmax+matmul、融合LayerNorm）如此重要的原因：它分摊了固定成本，并避免了操作之间将2 MB数据往返于HBM。

## 自行验证

```python
import torch, torch.nn.functional as F
x = torch.randn(1024, 1024, dtype=torch.float16, device='cuda')

def bench(fn, iters=1000):
    fn()  # 预热 + 编译JIT
    torch.cuda.synchronize()
    start = torch.cuda.Event(True); end = torch.cuda.Event(True)
    start.record()
    for _ in range(iters): fn()
    end.record(); torch.cuda.synchronize()
    return start.elapsed_time(end) / iters * 1e3  # μs

print("add    ", bench(lambda: x + x))
print("relu   ", bench(lambda: F.relu(x)))
print("softmax", bench(lambda: F.softmax(x, -1)))
print("ln     ", bench(lambda: F.layer_norm(x, (1024,))))
print("matmul ", bench(lambda: x @ x))
```

在你的RTX 4070和MI300X上运行这段代码——你会看到逐元素操作几乎完全按带宽比例缩放（约11倍），而matmul则按FP16张量吞吐量缩放。这种对比*就是*实际测量到的roofline模型。
