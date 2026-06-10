---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CPU分布式训练关键经验
translated: true
type: note
---

## 关键经验 — 深入剖析

### 1. Gloo 与 NCCL：后端差异

**它们是什么：**

- **NCCL**（NVIDIA 集体通信库）— GPU 到 GPU，使用 NVLink/PCIe/InfiniBand。当 CUDA 可用时默认使用。
- **Gloo** — CPU 到 CPU，使用 TCP 套接字。可在任何机器上工作，无需 GPU。

**我们遇到的 API 兼容性缺口：**

nanochat 中的 `DistMuonAdamW` 优化器使用带有 future 的异步操作：

```python
# NCCL：正常工作
work = dist.all_reduce(grad, async_op=True)
future = work.get_future()  # ✅ NCCL 支持此操作
future.wait()

# Gloo：会崩溃
work = dist.all_reduce(grad, async_op=True)
future = work.get_future()  # ❌ RuntimeError: Work::getFuture not implemented
```

Gloo 的 `Work` 对象没有实现 `get_future()`。这是因为 NCCL 使用 CUDA 流实现异步重叠（真正的流水线化），而 Gloo 使用 CPU 线程——这种抽象无法一一对应。

**我们的修复——一个兼容性包装器：**

```python
class _AsyncWorkWrapper:
    def __init__(self, work):
        self._work = work
    def wait(self):
        self._work.wait()  # 对 Work 对象进行同步等待

def _async_op(work):
    try:
        return work.get_future()  # NCCL 路径
    except RuntimeError:
        return _AsyncWorkWrapper(work)  # Gloo 回退
```

这保留了 `DistMuonAdamW` 使用的三阶段异步模式（启动归约 → 计算更新 → 收集结果），即使 Gloo 无法真正重叠通信与计算。

**其他差异：**

- NCCL 在 `init_process_group()` 中使用 `device_id=device` —— Gloo 不使用
- NCCL 自动选择最佳传输方式（NVLink > PCIe > TCP）—— Gloo 始终使用 TCP
- NCCL 要求所有张量在 CUDA 上 —— Gloo 可以使用 CPU 张量
- NCCL 通常达到 10-100 GB/s —— Gloo 受网络带宽限制（在我们的情况下，WiFi 约为 1 Gbps）

---

### 2. torch.compile 在 CPU 上：首次调用延迟

**发生了什么：**
`torch.compile` 使用 `torch.inductor` 将模型的前向传播 JIT 编译为优化的 C++/Triton 代码。在 GPU 上，它会生成 CUDA 内核。在 CPU 上，它会生成带有矢量化内联函数（AVX2/AVX-512）的 C++。

**冷启动问题：**

```
Step 0: dt=28,386ms  (28 秒——包括编译时间)
Step 1: dt=19,493ms  (仍在预热)
Step 2: dt=17,756ms  (趋于稳定)
Step 3: dt=17,408ms  (稳态)
Step 4: dt=17,412ms  (稳态)
Step 8: dt=15,681ms  (最佳)
```

首次调用会触发：

1. **TorchDynamo 追踪** — 将 Python 字节码捕获为图
2. **Inductor 降级** — 将图转换为 C++ 内核代码
3. **C++ 编译** — 使用 gcc/clang 编译（这是 CPU 上慢的部分）
4. **内核缓存** — 后续调用重用编译后的代码

在 GPU 上，Triton 编译 CUDA 内核也很慢（约 10-30 秒），但 GPU 内核的编译流程更简单。带有 AVX 向量化的 CPU C++ 编译更复杂。

**为什么这对 DDP 很重要：** 两个 rank 都必须独立编译（每个都有自己的进程）。如果一个 rank 在另一个之前完成编译，它会在第一个集合操作处阻塞，直到慢的 rank 赶上。这就是为什么第 0 步需要 28 秒——它是两个编译时间的最大值。

---

### 3. CPU DDP 吞吐量缩放

**测量结果：**

```
单进程（1 rank）：  ~45 tok/sec
2 ranks，单节点：     ~89 tok/sec  (1.98x 加速)
2 ranks，2 节点：     ~134 tok/sec (2.98x 加速)
```

**为什么单节点近乎完美缩放：**
在同一台机器上使用 2 个 rank，每个 rank 处理一半数据。通过 Gloo 的梯度同步在回环（localhost）上进行，这基本上是免费的（约 10 GB/s）。因此，你以微不足道的通信成本获得了 2 倍的计算能力。

**为什么多节点缩放低于线性：**
在 WiFi 上使用 2 个节点，梯度同步通过网络进行：

- 模型约有 3700 万个参数 × 4 字节（float32）= 约 148 MB 的梯度
- WiFi 带宽：有效约 50-100 Mbps = 约 6-12 MB/s
- 传输时间：每步约 12-25 秒

但每步总耗时约 16-17 秒。这意味着通信与计算重叠（`DistMuonAdamW` 中的三阶段异步模式），但仍然存在一些序列化开销。134 tok/sec 与理论值 90×2=180 tok/sec 相比，显示了网络瓶颈。

**缩放公式：**

```
加速比 = N / (1 + α(N-1))
其中 α = 通信时间 / 计算时间
```

对于我们的情况：α ≈ 0.15（通信时间占 15%），对于 2 个节点，加速比约为 1.75 倍。

---

### 4. bf16 自动检测 Bug

**该 Bug：**

```python
def _detect_compute_dtype():
    if torch.cuda.is_available():  # ← 检查的是系统能力，而不是训练设备
        capability = torch.cuda.get_device_capability()
        if capability >= (8, 0):
            return torch.bfloat16, "auto-detected: CUDA SM 89"
    return torch.float32, "auto-detected: no CUDA (CPU/MPS)"
```

在 1.36 上，`torch.cuda.is_available()` 返回 `True`（安装了 RTX 4070），即使传递了 `--device-type=cpu`。因此计算 dtype 被设置为 `bfloat16`。

**为什么 bf16 在 CPU 上表现糟糕：**

- CPU 没有原生 bf16 硬件（大多数 CPU 没有用于 bf16 的 AMX/VNNI）
- PyTorch 在 CPU 上通过将 bf16 转换为 float32 进行计算，然后再转换回来来模拟 bf16
- 这意味着每个矩阵乘法都要执行：bf16→fp32→matmul→fp32→bf16 —— 内存带宽翻倍
- i9-13900KF 有用于 fp32 的 AVX-512，但没有 bf16 加速
- 结果：训练挂起或运行速度为 ~0 tok/sec（实际上在仿真层中死锁）

**修复方法：**

```bash
export NANOCHAT_DTYPE=float32  # 强制使用 fp32，绕过 CUDA 自动检测
```

这是在一台装有 GPU 的机器上运行 CPU 训练时的一个常见陷阱。自动检测逻辑假设“如果 CUDA 可用，则使用 CUDA 优化的 dtype”——但当你明确请求 CPU 训练时，这是错误的。

**更广泛的经验教训：** 调试 CPU 训练问题时，始终检查 `COMPUTE_DTYPE` 实际设置为什么。横幅会打印它：

```
COMPUTE_DTYPE: torch.bfloat16 (auto-detected: CUDA SM 89 (bf16 supported))
```

如果你看到 bf16 但你在 CPU 上，那就是你的问题所在。

---

### 5. Gloo 中的 IPv4/IPv6 不匹配

**错误信息：**

```
RuntimeError: ss1.ss_family == ss2.ss_family. 10 vs 2
```

（`10` = AF_INET6，`2` = AF_INET）

**根本原因：** 两台机器都有带有 IPv6 地址的 Tailscale VPN 接口。当 Gloo 自动选择接口时，主节点选择了 Tailscale 接口（IPv6），而工作节点选择了 WiFi 接口（IPv4）。由于使用不同的地址族，它们无法通信。

**修复方法：**

```bash
export GLOO_SOCKET_IFNAME=enp4s0  # 强制主节点使用特定接口
export GLOO_SOCKET_IFNAME=wlp3s0  # 强制工作节点使用特定接口
```

这将 Gloo 固定到每台机器上的物理局域网接口，确保两者通过同一网络使用 IPv4。

**通用规则：** 调试 Gloo 连接问题时，始终检查：

1. 两台机器在指定接口上可以互相访问
2. 防火墙允许该接口上的流量（我们添加了 `ufw allow from 192.168.1.0/24`）
3. 两台机器使用相同的地址族（使用 `GLOO_SOCKET_IFNAME` 固定）
4. 作为额外安全网，使用 `GLOO_IPV6=0`

---

### 6. 分布式训练中的数据一致性

**问题：** 数据加载器按行组索引分片：

```python
rg_idx = ddp_rank       # 从 rank 开始
while rg_idx < pf.num_row_groups:
    yield data[rg_idx]
    rg_idx += ddp_world_size  # 按 world_size 步进
```

如果一台机器有 201 个 Parquet 文件，而另一台有 4 个，它们读取的数据完全不同。优化器会平均来自不同数据集的梯度，这会产生垃圾结果。

**修复方法：** 两台机器必须具有相同的 Parquet 文件。我们使用 `NANOCHAT_DATA_DIR` 将它们指向一个共享的 4 分片子集。

**更广泛的经验教训：** 在分布式训练中，数据一致性与代码一致性同等重要。始终验证：

- 所有节点上相同的数据集文件
- 所有节点上相同的分词器
- 相同数量的分片/行组
- 相同的训练/验证分割逻辑
