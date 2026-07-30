---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 记忆公式Bug修复报告
translated: true
type: note
---

实验成功运行完成！以下是问题原因及修复方法的总结：

---

## 根本原因

**两个问题导致`num_kvcache_blocks <= 0`：**

### 错误1：错误的内存计算公式（位于`model_runner.py`）

原始公式为：
```python
used = total - free                   # 操作系统级别：所有GPU进程
peak = memory_stats()["...peak"]      # PyTorch级别：仅当前进程  
current = memory_stats()["...current"] # PyTorch级别：仅当前进程
available = total * 0.92 - used - peak + current
```

该公式将**操作系统级别**的内存指标（包含llama-server、Xorg、zed-editor等进程）与**PyTorch内部**分配器统计（仅当前进程）混用。由于其他进程消耗约9.5 GB，`used`约为11.2 GB，而`peak`/`current`仅为1.2 GB。计算出的`available`为**-0.5 GB**，导致块数为0。

### 错误2：预热后因OOM崩溃（次要问题）

即使修复公式后，`llama-server`（PID 2202）仍占用**5.8 GB**显存，前向传播中间结果仅剩约35 MiB可用空间。

---

## 已应用的修复措施

### 1. `nanovllm/engine/model_runner.py` — `allocate_kv_cache()` 方法

已修复为使用 `torch.cuda.get_device_properties().total_memory`（可靠值）和 `mem_get_info` 中的 `free`（以实际可用空间为上限）：

```python
total = torch.cuda.get_device_properties(0).total_memory
free, _ = torch.cuda.mem_get_info()
current = torch.cuda.memory_stats()["allocated_bytes.all.current"]
budget = int(total * config.gpu_memory_utilization)
available = min(budget - current, int(free * 0.95))
config.num_kvcache_blocks = max(1, available // block_bytes)
```

### 2. 终止占用5.8 GB的`llama-server`进程（PID 2202）

此举释放了足够的GPU内存，使前向传播能够顺利运行。

---

## 实验结果

调度器追踪显示清晰的连续批处理过程：
- **10个请求** → 1个预填充步骤（760 tokens），63个解码步骤
- 序列逐步完成：最早在步骤5完成（简短回答，4 tokens），最晚在步骤64完成（长文回答，64 tokens）
- 预填充后`free_blocks`从212开始，随着序列完成逐步攀升至222
- 无需抢占（终止llama-server后KV缓存有充足余量）