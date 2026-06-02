---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 修复NumPy内存映射文件内存泄漏问题
translated: true
type: note
---

### Stack Overflow 帖文解析

该帖文讨论了使用 NumPy 的 `np.memmap` 处理磁盘存储的大型数据集时的常见问题。原问题描述通过遍历巨型矩阵（例如通过打乱索引）以分块读取行时，发现即使每行仅被访问一次，RAM 和虚拟内存使用量仍持续增长，导致系统运行变慢。提问者希望将内存使用限制在当前数据块范围内，并寻求替代方案，例如基于生成器的迭代或直接文件 I/O（但指出后者速度较慢）。

被引用的答案（ID 61472122，已采纳）指出该"内存泄漏"现象源于 NumPy 的 memmap 在只读模式和单次访问场景下仍会缓存整个数组。答案提出两种解决方案：

1. **为每个数据块重新创建 memmap 对象**：在每个批次或数据块处理时删除并重新初始化 `np.memmap`。这种方法可防止完整数组在 RAM 中累积，将内存使用维持在较低水平（与数据块大小相关）。虽然存在重新创建带来的微小 CPU 开销，但可忽略不计。示例代码：
   ```python:disable-run
   def process_chunks(data_filename, chunk_size=4096):
       for start in range(0, total_size, chunk_size):
           # 每次重新创建全新的 memmap
           data = np.memmap(data_filename, dtype=np.float32, mode='r', shape=full_shape)
           # 仅处理当前数据块
           chunk = data[start:start + chunk_size]
           # ... 执行处理操作 ...
           del data  # 显式释放
   ```

2. **使用操作系统内存建议的自定义 mmap**：通过访问 memmap 底层的 `mmap` 对象，利用 Python 3.8+ 的 `madvise` 功能（如 `MADV_DONTNEED` 或 `MADV_DONTDUMP`）通知操作系统释放未使用的内存页。这种方法更底层但避免了重新创建的开销，其中包含从 NumPy 源码提取的 mmap 访问代码片段。

该答案建议使用 `memory-profiler` 等性能分析工具验证修复效果。

### NanoGPT 采用此方法的原因

在 NanoGPT（一个用于语言模型训练的极简 GPT 实现）提供的代码中，`get_batch` 函数内部重新创建 `np.memmap` 的操作完全遵循了上述答案的第一种方案——这是为了避免在从大型二进制文件（如分词后的训练数据）重复采样批次时出现内存泄漏。

NanoGPT 需处理超大规模数据集（例如数十亿个词元），将完整文件加载至内存不可行。虽然使用 memmap 可实现高效的磁盘访问，但若不重新创建映射，随着 NumPy 缓存越来越多文件内容，内存占用会在多个训练周期内持续膨胀。通过在每批次处理时重新建立映射（通过 `if split == 'train': data = np.memmap(...)` 代码行），可确保内存使用保持低位稳定——这对于在单 GPU 等有限硬件上进行长时间训练至关重要。代码注释明确说明了该技巧源自 Stack Overflow 帖文关于"避免内存泄漏"的解决方案。这种方法在实现随机采样（`torch.randint`）生成 x/y 输入-目标对的同时，保持了数据加载器的轻量化特性。

[Stack Overflow: numpy memmap 内存使用 - 需要单次迭代](https://stackoverflow.com/questions/45132940/numpy-memmap-memory-usage-want-to-iterate-once/61472122#61472122)
```
