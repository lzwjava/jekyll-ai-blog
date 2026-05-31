---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 并行I/O：线程优于进程
translated: true
type: note
---

很好的问题。让我从基本原理开始分析。

**GIL（全局解释器锁）**

CPython有一个锁，阻止两个Python字节码指令同时在多个CPU核心上运行。这就是著名的GIL。它的含义是：

- 多线程：多个线程共享一个进程、一块内存空间，但同一时刻只有一个线程运行Python代码
- 多进程：每个进程拥有自己的Python解释器、自己的内存，在自己的CPU核心上运行

**`git pull` 时发生了什么？**

你的Python代码调用 `subprocess.run(["git", "pull", ...])`。这个过程如下：

```
Python线程 → fork() → exec("git") → git连接到GitHub → 等待socket → 数据到达 → 返回Python
```

关键部分：当git作为子进程运行时，你的Python线程**阻塞在 `os.waitpid()` 上**——它在内核中休眠，而不是执行Python字节码。当线程在内核中休眠时，**它会释放GIL**。其他线程可以自由运行。

所以，如果用8个线程执行git pull：

```
线程1: fork git → 休眠（GIL释放）──────────── 唤醒 → 完成
线程2: fork git → 休眠（GIL释放）──────────── 唤醒 → 完成
线程3: fork git → 休眠（GIL释放）────────── 唤醒 → 完成
...
全部8个git子进程在8个操作系统进程上并行运行
```

GIL无关紧要，因为你的Python线程99%的时间都在休眠。它们只是短暂唤醒以记录结果。

**为什么多进程在这里浪费资源：**

```
多进程：内存中有8个完整的Python解释器
  - 每个约30-50MB RSS
  - 进程间需pickle/unpickle数据（序列化开销）
  - 生成成本：fork() + import世界

多线程：一个进程中的8个轻量级线程
  - 每个约8KB栈
  - 共享内存（无需序列化）
  - 生成成本：仅创建线程
```

对于网络I/O，两者提供的并行性相同（操作系统无论如何都会调度8个git进程）。但线程在内存和启动上便宜100倍。

**什么时候需要多进程？**

当瓶颈是CPU时——Python字节码在紧密循环中执行。GIL阻止两个线程同时执行字节码。例如：

```python
# 这不会用线程加速——GIL阻止并行执行
def cpu_heavy(n):
    return sum(i * i for i in range(n))

# 这可以用多进程加速——每个进程有自己的GIL
with ProcessPoolExecutor(8) as pool:
    pool.map(cpu_heavy, [10**7] * 8)
```

**决策树：**

```
工作是否是I/O密集型（网络、磁盘、子进程）？
  → 是 → 线程（便宜，GIL无关紧要）
  → 否 → 是否是CPU密集型（数学、解析、ML）？
    → 是 → 多进程（绕过GIL）
    → 否 → 可能不需要并行
```

对于 `git pull`，它100%是网络等待。线程是完美的。多进程也能工作，只是浪费内存而没有任何好处。