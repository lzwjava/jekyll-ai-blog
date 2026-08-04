---
audio: false
generated: true
image: false
lang: zh
layout: post
title: nano-vLLM中的CUDA图优化
translated: true
type: note
---

问题：什么是 CUDA Graph，为什么 nano-vLLM 需要它？

答案：

CUDA Graph 是 NVIDIA 的一种 **GPU 执行优化机制**。核心思想：

> 与其每次迭代从 Python/C++ 启动数千个 CUDA 内核，不如一次性记录 GPU 执行过程，然后以几乎为零的 CPU 开销重放它。

这对 LLM 推理非常重要，尤其是 **解码阶段**。

nano-vLLM 包含 CUDA Graph 优化，并捕获类似 `[1,2,4,8,16,...512]` 的解码批次，这样重复的 token 生成可以避免 Python/内核启动开销。([Mintlify][1])

---

## 1. 正常的 PyTorch 推理路径

想象生成一个 token：

```
用户
 |
 | 输入 token
 v
Python
 |
 | model.forward()
 v
PyTorch 分发器
 |
 | 启动内核
 v
GPU

  matmul 内核
  attention 内核
  layernorm 内核
  softmax 内核
  ...
```

对于一个 32 层的 transformer：

```
Python
  |
  +-- 启动 GEMM
  +-- 启动 attention
  +-- 启动 RMSNorm
  +-- 启动 GEMM
  +-- 启动 RoPE
  +-- ...
       数百次内核启动
```

GPU 计算本身可能很快，但每次内核启动都有 CPU 开销。

典型开销：

```
CPU 准备内核
       |
       v
CUDA 驱动
       |
       v
GPU 执行
```

每次启动耗时微秒级。

对于训练来说，这不是问题：

```
大批量
大矩阵乘法
GPU 忙碌数秒
```

但 LLM 解码不同：

```
batch = 1 个 token
小矩阵运算
多层结构
重复数千次
```

GPU 花更多时间等待 CPU。

---

## 2. CUDA Graph 思想

CUDA Graph 改变了：

### 没有图

每个 token：

```
Python 循环：

token 1:
 启动内核 A
 启动内核 B
 启动内核 C

token 2:
 启动内核 A
 启动内核 B
 启动内核 C

token 3:
 启动内核 A
 启动内核 B
 启动内核 C
```

巨大的重复开销。

---

### 使用 CUDA Graph

第一次：

```
CUDA 图捕获：

内核 A
   |
内核 B
   |
内核 C
   |
内核 D

记录此执行图
```

之后：

```
GPU 重放（图）

GPU：
 A -> B -> C -> D

（无需 Python 参与）
```

CPU 基本上说：

```
"执行这个图"
```

而不是：

```
"启动内核 1"
"启动内核 2"
"启动内核 3"
...
```

---

## 3. 为什么 LLM 解码非常适合 CUDA Graph

LLM 推理有两个阶段：

```
提示：
   "解释 CUDA Graph"

        |
        v

预填充阶段
----------------
处理数千个 token

大矩阵乘法
GPU 利用率高


解码阶段
----------------
生成：

token 1
token 2
token 3
...

小批次
重复结构
```

解码看起来像：

```
while 不是 EOS：

    logits = model(last_token, KV_cache)

    next_token = sample(logits)

```

每次迭代的计算几乎完全相同。

这正是 CUDA Graph 喜欢的：

```
相同操作
相同形状
相同内存布局
重复多次
```

---

## 4. 为什么 nano-vLLM 需要 CUDA Graph

nano-vLLM 是一个最小化的 vLLM 实现。它已经拥有：

* continuous batching
* KV cache
* paged attention 思想
* tensor parallel
* CUDA graph 支持

([Awesome Lists][2])

调度器创建解码批次：

示例：

```
batch size = 8

请求：
 A -> 生成 token
 B -> 生成 token
 C -> 生成 token
 ...
```

模型执行形状是可预测的：

```
input_ids:
[8,1]

positions:
[8]

KV cache:
固定块
```

所以 nano-vLLM 可以捕获：

```
graph[1]
graph[2]
graph[4]
graph[8]
graph[16]
...
graph[512]
```

然后：

```
当前批次 = 8

执行 graph[8]
```

而不是每次 token 都重建 PyTorch 执行过程。

([Mintlify][1])

---

## 5. 简单的 PyTorch 示例

不使用 CUDA Graph：

```python
for i in range(10000):
    y = model(x)
```

每次循环：

```
Python
  |
  model.forward()
  |
  CUDA 内核
```

---

使用 CUDA Graph：

```python
graph = torch.cuda.CUDAGraph()

torch.cuda.synchronize()

with torch.cuda.graph(graph):
    y = model(x)


for i in range(10000):
    graph.replay()
```

现在：

```
Python
 |
 replay()
 |
 GPU 执行记录的图
```

---

## 6. 为什么不总是使用 CUDA Graph？

因为 CUDA Graph 有约束。

在捕获期间：

```
形状必须保持不变
内存地址必须稳定
不能动态分配
不能有随机的 Python 控制流
```

错误示例：

```python
if batch_size == 7:
    执行 A
else:
    执行 B
```

图无法轻松处理这种情况。

这就是为什么 vLLM/nano-vLLM 架构分离：

```
CPU 侧：
 调度器
 请求管理
 KV cache 分配

GPU 侧：
 固定执行
```

这种设计使图捕获成为可能。([Ashwing][3])

---

## 7. 为什么 vLLM 很快

一个现代 LLM 服务栈看起来像：

```
                 请求
                    |
                    v

              调度器
              (CPU)

                    |
          选择批次大小

                    |
                    v

           CUDA Graph 重放

                    |
                    v

              GPU 内核

                    |
                    v

              下一个 token
```

性能来自于组合：

```
PagedAttention
+
continuous batching
+
KV cache 管理
+
CUDA Graph
+
优化内核（FlashAttention/Triton）
```

CUDA Graph 只是其中一部分，但对于解码密集型工作负载，它可以带来显著的性能提升。

---

对于你的 RTX 4070 上使用 Qwen/nano-vLLM 的实验，你可以很容易地看到效果：

```bash
CUDA_LAUNCH_BLOCKING=1 python benchmark.py
```

或者对比：

```python
LLM(
    model_path,
    enforce_eager=True   # 不使用 CUDA graph
)
```

和：

```python
LLM(
    model_path,
    enforce_eager=False  # 启用 CUDA graph
)
```

第二个应该能提高解码吞吐量，尤其是在并发请求的情况下。([Mintlify][1])

参考资料：

* CUDA Graphs 编程指南：[https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#cuda-graphs](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#cuda-graphs)
* nano-vLLM：([Awesome Lists][2])
* nano-vLLM 基准测试笔记：([Mintlify][1])

[1]: https://www.mintlify.com/GeeeekExplorer/nano-vllm/guides/benchmarking?utm_source=chatgpt.com "Benchmarking - Nano-vLLM"
[2]: https://awesome.ecosyste.ms/projects/github.com%2FGeeeekExplorer%2Fnano-vllm?utm_source=chatgpt.com "https://github.com/GeeeekExplorer/nano-vllm | Ecosyste.ms: Awesome"
[3]: https://ashwing.github.io/vllm-guide/ch02.html?utm_source=chatgpt.com "nano-vLLM · Ch02 · Architecture"
