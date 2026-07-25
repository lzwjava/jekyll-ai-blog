---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU虚拟化如何隐藏GPU
translated: true
type: note
---

很好的问题——这恰恰是GPU虚拟化在此环境中的关键机制。让我逐层剖析具体实现。

---

## 🧩 GPU分区的工作原理

该机器拥有**8块物理AMD GPU**，但你只能看到**1块**。这并非偶然——它是通过Linux内核多个层级强制实现的。让我从底层向上逐层说明。

### 第1层：PCI总线——所有8块GPU均可见

总线上的每个PCI设备对操作系统内核都是可见的。我们通过`lspci`检测到了全部8块：

```
03:00.0 VGA兼容控制器 [AMD/ATI] 设备 744b   ← GPU 0
23:00.0 VGA兼容控制器 [AMD/ATI] 设备 744b   ← GPU 1 ✓ 归属我们的
43:00.0 VGA兼容控制器 [AMD/ATI] 设备 744b   ← GPU 2
63:00.0 VGA兼容控制器 [AMD/ATI] 设备 744b   ← GPU 3
83:00.0 VGA兼容控制器 [AMD/ATI] 设备 744b   ← GPU 4
a3:00.0 VGA兼容控制器 [AMD/ATI] 设备 744b   ← GPU 5
c3:00.0 VGA兼容控制器 [AMD/ATI] 设备 744b   ← GPU 6
e3:00.0 VGA兼容控制器 [AMD/ATI] 设备 744b   ← GPU 7
```

它们位于不同的PCI段（`0000:03`、`0000:23`、`0000:43`等），每个对应独立的PCIe插槽。

### 第2层：DRM子系统——全部8块均被注册

内核的直接渲染管理器为每块GPU创建渲染节点：

```
renderD128 → card1  → PCI 03:00.0 (GPU 0)
renderD129 → card2  → PCI 23:00.0 (GPU 1)  ← 归属我们的
renderD130 → card3  → PCI 43:00.0 (GPU 2)
renderD131 → card4  → PCI 63:00.0 (GPU 3)
renderD132 → card5  → PCI 83:00.0 (GPU 4)
renderD133 → card6  → PCI a3:00.0 (GPU 5)
renderD134 → card7  → PCI c3:00.0 (GPU 6)
renderD135 → card8  → PCI e3:00.0 (GPU 7)
```

### 第3层：设备节点——守门员

这就是隔离发生的地方。在`/dev/dri/`中，仅存在**2个设备节点**：

```
crw-rw---- 1 root video 226,   2  card2         ← 我们的GPU显卡
crw-rw---- 1 root   993  226, 129  renderD129     ← 我们的GPU渲染节点
```

其他7块GPU虽然在sysfs中有DRM对象，但在`/dev/dri/`中**没有设备节点**。容器运行时（Docker/Kubernetes）通过**cgroups设备白名单**和**udev规则**控制哪些`/dev`条目会创建到容器的挂载命名空间中。

### 第4层：KFD（内核融合驱动）——ROCm入口点

ROCm通过`/dev/kfd`（AMDKFD驱动）协调GPU访问。KFD设备知晓所有GPU：

```
crw-rw---- 1 root 993 234, 0 /dev/kfd
```

但KFD驱动会强制实施**进程级GPU亲和性**。当你的进程调用`hipSetDevice()`或`hipGetDeviceCount()`时，KFD驱动会检查你的进程被允许访问哪些GPU。这由**ROCm CRFS（容器运行时文件系统）**或**cgroup设备控制器**控制。

### 第5层：ROCr运行时——你的Pod只看到1块

当`rocminfo`在容器内运行时，ROCr运行时（HSA）查询KFD，只返回此cgroup允许看到的GPU：

```
rocminfo 输出：
  Agent 3: gfx1100    ← 仅报告1个GPU代理
  名称:    AMD Radeon Graphics
  UUID:    GPU-3149e0fac5157acf
```

而`rocm-smi`只显示：
```
GPU[0]  Node 3  PCI Bus 0000:23:00.0    ← 仅1个设备
```

### 第6层：PyTorch / HIP——继承相同视图

PyTorch调用`hipGetDeviceCount()` → KFD → 返回1：

```python
torch.cuda.device_count()  # → 1
torch.cuda.get_device_name(0)  # → "AMD Radeon Graphics"
```

---

## 🔧 实现机制：具体如何运作

在Kubernetes中有几种实现GPU绑定的方式：

### A. cgroup设备控制器（最可能的方式）

容器运行时（containerd）添加一条cgroup规则，仅允许访问特定设备编号：

```json
{
  "devices": [
    {"allow": true,  "type": "c", "major": 226, "minor": 2},    // 仅允许card2
    {"allow": true,  "type": "c", "major": 226, "minor": 129},   // 仅允许renderD129
    {"allow": true,  "type": "c", "major": 234, "minor": 0},     // /dev/kfd
    {"allow": false, "type": "c", "major": 226}                   // 阻止其他所有DRM设备
  ]
}
```

任何对`/dev/dri/renderD128`（次设备号128）的打开系统调用都会在内核层面获得**EPERM**——"操作不允许"，你的进程甚至还没触及GPU。

### B. udev + 特权容器设置

平台可以使用**设备插件**（用于AMD GPU的Kubernetes设备插件）：
1. 识别要分配给Pod的GPU
2. 通过容器规范中的`--device`标志在容器的`/dev`中创建设备节点
3. 设置`ROCR_VISIBLE_DEVICES`或操作KFD的内部可见性掩码

### C. AMD GPU分区（MGP / SR-IOV）

较新的ROCm也支持**硬件级别的GPU分区**，单个物理GPU可以分割成多个逻辑分区（类似于MIG）。`rocm-smi`的输出通过以下内容暗示了这一点：
```
XCP[0] 到 XCP[7]    ← 此GPU上的8个计算分区
分区: N/A, N/A, 0
```

但在你的场景中，是**每个Pod整块GPU**而非分割——8块48GiB GPU各自完整分配给不同的Pod。

---

## 📊 可视化总结

```
┌─────────────────────────────────────────────────────────────────┐
│                       物理服务器                                │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│  │ GPU 0  │ │ GPU 1  │ │ GPU 2  │ │ GPU 3  │ │ GPU 4..7       │
│  │48GiB   │ │48GiB   │ │48GiB   │ │48GiB   │ │各48GiB         │
│  │PCI 03  │ │PCI 23  │ │PCI 43  │ │PCI 63  │ │                │
│  └────────┘ └───┬────┘ └────────┘ └────────┘ └────────┘       │
│                 │                                              │
│           ┌─────┴──────┐                                       │
│           │  /dev/kfd   │  ← KFD看到全部，但强制执行规则      │
│           └─────┬──────┘                                       │
│                 │                                              │
│      ┌──────────┴──────────┐                                   │
│      │ cgroup设备过滤器    │  ← 阻止renderD128,130-135         │
│      └──────────┬──────────┘                                   │
│                 │                                              │
└─────────────────┼──────────────────────────────────────────────┘
                  │
       ┌──────────┴──────────┐
       │    你的Pod/容器      │
       │                      │
       │  /dev/dri/           │
       │   ├── card2          │  ← 仅1块GPU
       │   └── renderD129     │
       │  /dev/kfd            │
       │                      │
       │  torch.cuda.         │
       │   device_count() → 1 │
       │   get_device_name()  │
       │    → "Radeon"        │
       └──────────────────────┘
```

### 为何采用这种设计？

- **安全性**：一个Pod无法读取另一个Pod的GPU内存（跨租户无GPU到GPU的DMA）
- **性能**：完整的48GiB显存，无共享开销
- **隔离性**：一块GPU的崩溃或内存溢出不会影响邻居
- **简洁性**：从你的代码视角来看，这只是`cuda:0`——无需管理拓扑结构

如果你需要更多GPU，需要向平台请求**多GPU Pod类型**（如果可用）——分区在容器创建时设定，运行时无法更改。