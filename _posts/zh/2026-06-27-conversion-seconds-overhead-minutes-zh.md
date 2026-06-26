---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 转换秒数，开销分钟数
translated: true
type: note
---

在将124M模型检查点（约600MB）转换为HuggingFace格式时，瓶颈几乎完全在于`scp`传输和磁盘I/O——而不是计算。实际的转换过程很简单。

**分析如下：**

**scp传输（600MB，局域网内）：** 在典型的千兆局域网（实际吞吐量约110MB/s）上，600MB需要约5-6秒。在WiFi（20-40MB/s）上，需要约15-30秒。但你的脚本传输的是很小的`convert_local.py`，而不是检查点——600MB的`ckpt.pt`已经存在于`192.168.1.36`上。因此模型没有网络开销。

**`torch.load`（从磁盘加载600MB）：** 在SSD上需要约2-5秒，在机械硬盘或内存受限的情况下会更长。

**转换（键重命名、`.float().clone()`）：** 你正在将fp16升格为fp32，因此内存中的模型大小翻倍至约1.2GB。纯CPU张量复制——约1-3秒。

**保存safetensors（约1.2GB fp32输出）：** 这是真正的成本。fp32使磁盘大小比fp16翻倍。向`/tmp`（通常是tmpfs/基于RAM）写入约500MB-1.2GB需要约3-10秒。

**总计：约15-30秒的实际工作。**

你的`04m41s`实际消耗时间具有误导性——这是挂钟时间，包括SSH会话建立、Python解释器+torch导入（仅torch导入冷启动就需要3-8秒），以及终端等待/空闲时间。`weights_only=False`加载还带来了pickle开销。

如果转换本身确实需要几分钟，那么可能的罪魁祸首是：

- **磁盘速度慢**（工作站上为HDD而非SSD）——用`iostat -x 1`检查
- **`/tmp`不是tmpfs**，并且你正在向慢速磁盘写入fp32
- **内存压力**——1.2GB fp32模型加上torch开销在资源受限的机器上导致交换

一个优化：除非必要，跳过fp32升格。HF GPT-2在fp16/bf16下运行良好，可将写入大小减半：

```python
# 将 .float().clone() 替换为保持 bf16：
state_dict[k] = state_dict[k].to(torch.bfloat16).clone()
```

并在配置中设置`"dtype": "bfloat16"`。这将safetensors写入时间大致减半。

要实际测量时间花费在何处：

```bash
ssh lzw@192.168.1.36 "PYTHONUNBUFFERED=1 python3 -X importtime /tmp/convert_local.py 2>&1 | tail -20"
```

或者直接对各个阶段进行计时：

```python
import time
t = time.time()
ckpt = torch.load(CKPT_PATH, map_location="cpu", weights_only=False)
print(f"加载: {time.time()-t:.1f}秒", flush=True)
```

**总结：** 124M/600MB的转换实际计算时间应远低于一分钟。如果你看到4-5分钟，那是导入、SSH和磁盘慢带来的开销，而不是模型大小所致。