---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU 瓶颈诊断总结
translated: true
type: note
---

以下是我得出该诊断和解决方案的逐步推理：

## 步骤 1：识别核心异常

**每迭代 21 秒** 在 H200 GPU 上立即令人怀疑。作为背景：
- 单张 H200 可以达到 ~300-500 TFLOPs (FP16/BF16)
- GPT-2 XL (1.5B params) 在 1M tokens 上的 forward+backward 应该在该硬件上花费 **~0.5-1.5 秒**
- 即使有开销，超过 3-5 秒的任何时间都表明存在瓶颈

**150%+** 的 MFU 读数确认测量有问题，而不是计算本身出了故障。

## 步骤 2：计算实际数据负载

查看您的配置：
```
batch_size = 16
block_size = 1024
gradient_accumulation_steps = 64
```

每迭代：
- 每个 micro-batch：16 × 1024 = 16,384 tokens
- 64 次累积 = **1,048,576 tokens 每迭代**
- 那大约是 4MB 数据（每个 token 4 bytes）
- 但关键在于：**每迭代 64 次独立的磁盘读取**

## 步骤 3：在 nanoGPT 中追踪数据路径

nanoGPT 中的标准 `get_batch()`：
```python
def get_batch(split):
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    return x, y
```

这会**对 numpy/内存映射数组进行随机索引**。当 `gradient_accumulation_steps=64` 时，您会执行：
- 每迭代 64 次 `get_batch()` 调用
- 每次调用：16 个随机索引 × 1024 个 token 查找 = 16,384 次随机内存访问
- 每迭代总计：**1,048,576 次随机内存访问**

即使使用 SSD，这种规模的随机访问也是致命的。

## 步骤 4：考虑 DigitalOcean 上的存储位置

DigitalOcean 的 H200 droplets 通常具有：
- **Boot disk**：网络附加，中等 IOPS (2,000-5,000)
- **Scratch NVMe**：本地，高 IOPS (100,000+)

如果您的 `fineweb` 数据集位于 boot disk 上，每迭代 1M 次随机访问将被限制在 ~5,000 IOPS → ~200 次随机访问每毫秒 → 仅 I/O 等待至少 5 秒。再加上 Python 开销，21 秒就合情合理了。

## 步骤 5：计算时间损失

21s/iter × 10,000 iters = 210,000 秒 = **58 小时**

但如果修复到 1s/iter = 10,000 秒 = **2.8 小时**

这是等待解锁的 **20x 加速**。

## 步骤 6：关联到 nanoGPT 的已知问题

我回忆起 nanoGPT 仓库中有一个特定 PR：“Fix for gradient_accumulation_steps training slow”。问题正是这个：较大的累积值会导致重复数据加载，因为 `get_batch()` 调用发生在累积循环内部，而不是外部。

## 步骤 7：优先级排序修复

按影响最大排序：
1. **减少 `gradient_accumulation_steps`** → 将磁盘读取减少 16x
2. **增加 `batch_size`** → 每次读取更少的随机索引
3. **使用 `DataLoaderLite`** → 高效预取和批处理
4. **迁移到 NVMe** → 随机访问快 100x

MFU 异常只是干扰——这是 `torch.compile` 无法正确计入 I/O 等待时间导致的误报。先修复 I/O，然后 MFU 会降到现实的 40-60%。

**底线**：您的 H200 在那 21 秒中有 20 秒在等待数据，而不是计算。修复方法是更快、更少地提供数据。