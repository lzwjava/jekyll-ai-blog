---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU代际对比：M40 vs 4070
translated: true
type: note
---

问题：比较你的两个 `nvidia-smi` 快照——Tesla M40 与 RTX 4070。

回答：

这两块 GPU 基本上属于完全不同的世代，你的快照显示了预期的行为。

|                    |       **Tesla M40** |        **RTX 4070** |
| ------------------ | ------------------: | ------------------: |
| 架构               |           Maxwell 2 |        Ada Lovelace |
| 计算能力           |             **5.2** |             **8.9** |
| VRAM               | 11,520 MiB (~12 GB) | 12,282 MiB (~12 GB) |
| VRAM 类型          |               GDDR5 |               GDDR6 |
| 内存带宽           |           ~288 GB/s |           ~504 GB/s |
| CUDA 核心          |               3,072 |               5,888 |
| FP32 性能          |         ~7.0 TFLOPS |        ~29.1 TFLOPS |
| TDP                |               250 W |           200–215 W |
| 张量核心           |                   ❌ |                   ✅ |
| 光线追踪核心       |                   ❌ |                   ✅ |
| NVENC              |    较老一代 |         更新很多 |
| 你的温度           |            **46°C** |            **40°C** |
| 你的功耗           |            **70 W** |            **10 W** |
| 你的负载           |      `llama-server` |       Desktop/GNOME |

### 1. 你的 M40 实际上在执行真正的 LLM 工作

这一行很重要：

```text
Tesla M40
内存: 5144 MiB / 11520 MiB
功耗:   70 W / 250 W

llama-server: 5137 MiB
```

因此，大约 5.1 GB 的 VRAM 分配几乎全部属于你的 `llama-server`。

另外：

```text
GPU-Util: 0%
```

**并不**意味着模型没有加载。

它意味着在 `nvidia-smi` 采样 GPU 的那个瞬间，基本上没有 CUDA 内核在执行。

对于空闲的 llama.cpp 服务器来说，这是正常现象：

```text
VRAM 已分配
      ↓
模型权重常驻
      ↓
GPU 利用率为 0% 等待中
      ↓
请求到达
      ↓
GPU 利用率飙升
```

**5.1 GB 的 VRAM 分配**比 0% 的利用率有趣得多。

---

### 2. 4070 快照基本上是桌面空闲状态

你的 4070 显示：

```text
1180 MiB / 12282 MiB
10 W / 215 W
40°C
P8
```

大约 1.18 GB 主要是图形化桌面的分配：

```text
Xorg             757 MiB
GNOME Shell       41 MiB
Chrome/etc       ~310 MiB
```

所以这基本上就是：

```text
4070
 ├── Xorg
 ├── GNOME
 └── 浏览器
```

没有运行任何有意义的 CUDA 负载。

---

## 3. 真正有趣的对比：M40 与 4070 用于 LLM

你的实验说明了一个重要观点。

M40 的 VRAM 容量与 4070 **大致相同**：

```text
M40: 11.5 GiB
4070: 12.0 GiB
```

但 4070 要新得多。

粗略的原始 FP32 差值约为：

```text
4070 ≈ 29 TFLOPS
M40  ≈  7 TFLOPS
```

因此原始 FP32 吞吐量大约有 **4 倍** 的差距。

但对于现代 LLM 推理来说，差距可能更加显著，因为 4070 拥有：

```text
Ada
 ├── 张量核心
 ├── 更新的 CUDA 架构
 ├── 更快的 FP16/BF16/TF32 路径
 └── 更新的内存子系统
```

而 M40 是：

```text
Maxwell
 └── 无张量核心
```

这就是为什么 M40 是一块有趣的**廉价 VRAM/LLM 实验卡**，而 4070 则是功能强大得多的计算 GPU。

---

## 4. 你的 M40 有一个特别有趣的地方

你的 M40 运行着：

```text
NVIDIA 驱动 580.178.04
CUDA 13.0
```

并且 `nvidia-smi` 正常识别它。

这很有用，因为 M40 是一块**计算能力 5.2** 的 GPU，而且相当老旧。

因此你当前的设置展示了：

```text
现代 Linux
    ↓
580 驱动
    ↓
CUDA 13 运行时/驱动
    ↓
Maxwell M40
    ↓
llama.cpp / llama-server
    ↓
~5.1 GB 模型分配
```

这是一个相当不错的老 GPU LLM 实验室。

需要注意的是，**CUDA 工具链/编译器支持与运行时驱动支持是不同的**。当前的 NVIDIA 驱动能识别这块卡，并不意味着每个现代 CUDA 内核/工具链仍然支持 `sm_52`。

---

### 总结

你的两张截屏基本上就是：

```text
M40:
12 GB VRAM
250 W
46°C
70 W
5.1 GB 已占用
└── llama-server

4070:
12 GB VRAM
215 W
40°C
10 W
1.18 GB 已占用
└── 桌面
```

所以，**目前 M40 被用作你的 LLM GPU**，而 **4070 仅仅驱动着你的 Linux 桌面**。

实际上，这对实验来说是一个有用的设置：你可以让这块老 Maxwell 卡作为专用的推理/计算设备，而把 4070 留给更新的 CUDA/LLM 负载使用。