---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tesla M40与P100对比
translated: true
type: note
---

问题：Tesla M40 相比如何？它能用在我的 B150M + i5-6500 上吗？

回答：**可以，电气上兼容，但针对你的使用场景，除非 M40 便宜很多，否则我会选 P100 而不是 M40。**

### M40 规格

Tesla M40 是一款 **Maxwell** 计算卡：

|                    |       Tesla M40 |      Tesla P100 |
| ------------------ | --------------: | --------------: |
| 架构               |       Maxwell 2 |          Pascal |
| CUDA 核心数        |           3,072 |           3,584 |
| 显存               | **24 GB GDDR5** |   12/16 GB HBM2 |
| 显存带宽           |        288 GB/s |    **732 GB/s** |
| FP32               |       ~7 TFLOPS | **~9.3 TFLOPS** |
| PCIe               |         3.0 x16 |         3.0 x16 |
| 功耗               |       **250 W** |           250 W |
| 散热               |     **被动散热** |          被动散热 |
| 计算能力           |         **5.2** |         **6.0** |

NVIDIA 的 M40 数据表确认了 24 GB GDDR5、PCIe 3.0 x16、250 W 和被动散热。（[NVIDIA Images][1]）

### 你的 B150M + i5-6500

**兼容。**

你的 B150M 主板有一个 PCIe 3.0 x16 插槽，M40 也是 PCIe 3.0 x16。B150 同样支持第六代酷睿 CPU，比如你的 i5-6500。（[MSI USA][2]）

所以：

```text
i5-6500
   │
B150M
   │ PCIe 3.0 x16
   ▼
Tesla M40
   │
   └── 24 GB GDDR5
```

不需要特殊主板。

### ⚠️ 散热问题和 P100 完全一样

M40 是**被动散热**的。

这意味着：

```text
M40 散热片
████████████████
████████████████  ← 无 GPU 风扇
████████████████
       ↑
   需要风道
```

而且这是一块 **250 W** 的卡。

你确实需要高风量的散热配置，风扇直接吹过散热片。在普通台式机机箱里，我会考虑在 M40 前面直接安装一个 **120 mm/140 mm 风扇**。

### 有趣的地方：24 GB vs 16 GB

如果你专门考虑用于 **LLM**，M40 的 24 GB 很有吸引力。

例如：

```text
7B FP16:
7B × 2 bytes ≈ 14 GB
```

所以 24 GB 比 16 GB 的 P100 为模型权重 + KV 缓存提供了多得多的空间。

但 M40 **老得多**，计算能力只有 **5.2**，这会在现代 CUDA/软件兼容性方面带来显著问题。

P100 的 `sm_60` 对现代 CUDA 工作负载友好得多。

### 我的排名

对于 LLM/CUDA 机器：

```text
P100 16GB
  > M40 24GB
```

**除非 M40 非常便宜，而且你确实需要 24 GB。**

如果你是在类似下面这两种价格之间选择：

```text
M40 24GB  → $80
P100 16GB → $100
```

我会选 **P100**。

如果是这样：

```text
M40 24GB  → $50
P100 16GB → $150
```

那 **M40 就有吸引力了**，纯粹是因为 24 GB 显存。

还有一点：**M40 没有显示输出，而且是被动散热**，所以把它当作无头 CUDA 加速器，而不是游戏 GPU。

如果你告诉我你看到的 **M40 / P100 / P40 的价格**，我可以按 **每美元 LLM 推理性能** 为你具体排名。

[1]: https://images.nvidia.com/content/tesla/pdf/78071_Tesla_M40_24GB_Print_Datasheet_LR.PDF?utm_source=chatgpt.com "数据表：Quadro M6000"
[2]: https://us.msi.com/Motherboard/B150M-PRO-VDH/Specification?utm_source=chatgpt.com "规格 B150M PRO-VDH | MSI USA"