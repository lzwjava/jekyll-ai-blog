---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 仅阅读不行动不如躬行实践以优化
translated: true
type: note
---

**问题：** 对于优化学习（例如 AMD ROCm 内核优化），关键在于找到一个真实的目标进行优化，并借助 AI 进行迭代，而不是仅仅阅读——这样理解对吗？

**回答：**

是的，完全正确。这就是应用于系统工作的 Karpathy 原则：

> *“不要做观光客。去写代码。”*

阅读 ROCm 文档或 CUDA 论文能让你掌握词汇。而实际分析和优化一个真实的内核能让你获得 **直觉**——而直觉才是能够不断积累的能力。

## 行之有效的学习循环

```
找出一个真实的瓶颈 → 测量它 → 形成假设 →
修改代码 → 再次测量 → 让 AI 解释差异 → 重复
```

AI 在 **循环内部** 最为有用，而不是在循环之前。你不要抽象地提问“请解释 ROCm 内存合并”，而是粘贴你的 HIP 内核、你的 `rocprof` 输出，然后问“为什么这个比预期慢了 3 倍？”

## 具体示例：ROCm 内核优化

**第一步：找到真实的目标**
```python
# 你正在运行一个 Transformer —— 分析注意力内核
import torch
x = torch.randn(32, 512, 512).to("cuda")  # ROCm = 相同 API

# 测量
torch.cuda.synchronize()
start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)
start.record()
out = torch.softmax(x @ x.transpose(-1,-2), dim=-1) @ x
end.record()
torch.cuda.synchronize()
print(f"{start.elapsed_time(end):.2f} ms")
```

**第二步：编写一个简单的 HIP 内核**
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

**第三步：使用 rocprof 进行分析**
```bash
rocprof --stats -o profile.csv ./my_kernel
# 查看：FETCH_SIZE, L2CacheHit, wavefront occupancy
```

**第四步：带着证据向 AI 提问**
```
这是我的内核：[粘贴]
这是我的 rocprof 输出：[粘贴]
L2 命中率为 23%。我的假设是 B 矩阵的访问模式是非合并的。这个判断对吗？如何修复？
```

现在你是在把 AI 当作一位 **资深工程师搭档** 来使用，而不是一本教科书。

## 真正的洞见

大多数优化知识 **并不在阅读中** —— 它存在于以下两者之间的差距中：
- 你 *认为* 会很快的方式
- 分析器 *实际指出* 正在发生的情况

正是这个差距才是学习发生的地方。AI 加速了缩小这个差距的过程，因为你可以解释这个差距，并在 30 秒内得到一个有针对性的假设，而不需要花 3 小时翻文档。

## 应用到你的实际情况

你在 H100/H200 上训练 GPT-2。这是你真实的工作负载。现在可以立即优化的具体事项：

| 目标 | 工具 | 你将学到什么 |
|---|---|---|
| Attention FLOP 效率 | `nsys` / `rocprof` | 内存带宽 vs 计算瓶颈 |
| DataLoader 瓶颈 | `py-spy` | CPU/GPU 流水线重叠 |
| DDP 中的 All-reduce | NCCL 日志 | 通信隐藏 |
| Flash Attention vs 朴素实现 | Triton 内核 | 分块、SRAM 使用 |

每一项都是一个为期一周的项目，能让你学到比阅读一个月的优化论文更多的东西——因为你将拥有 **数字** 来解释，而不是空洞的概念。

这时，阅读便成了参考资料，而不是学习本身。