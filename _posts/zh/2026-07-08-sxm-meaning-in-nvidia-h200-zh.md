---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA H200中SXM的含义
translated: true
type: note
---

问题：NVIDIA H200中的 **SXM** 是什么意思？

答案：

**SXM = SXM 外形规格（Socket eXchange Module）**。在 NVIDIA GPU 产品中，它指的是**服务器模块封装形式**，而非 GPU 架构。

对于 NVIDIA H200 Tensor Core GPU，通常有两种物理版本：

1. **H200 SXM**
   * 专为大型 AI 服务器设计
   * 使用 NVIDIA 的 SXM 连接器
   * 通过 NVIDIA NVLink 实现 GPU 间直连
   * 带宽和功耗上限更高

2. **H200 PCIe**
   * 标准 PCIe 卡（类似普通 GPU 扩展卡）
   * 更容易集成到现有服务器中
   * GPU 间通信带宽较低

"SXM" 模块看起来更像一块密集的加速板，插入定制的 NVIDIA 基板：

```
HGX H200 系统

CPU
 |
PCIe / NVLink
 |
+----------------+
| H200 SXM       |
| GPU 模块       |
+----------------+
 |
NVLink 互联
 |
+----------------+
| H200 SXM       |
| GPU 模块       |
+----------------+
```

对于 AI 训练，SXM 是更强大的版本，原因如下：

* 更高功耗：
  * H200 SXM：~700W
  * H200 PCIe：~350W

* 更大内存带宽：
  * H200 SXM：~4.8 TB/s HBM3e 带宽
  * PCIe 版本受限更多

* 更好的 GPU 间扩展：
  * SXM 使用 NVLink/NVSwitch
  * PCIe 更依赖 PCIe 通道

因此，当 NVIDIA 工程师提到：

> "SM120"

他们指的是**GPU 计算架构/流式多处理器代次**（Blackwell SM 版本）。

当提到：

> "H200 SXM"

含义为：

```
H200        = GPU 产品
SXM         = 物理模块/封装
```

类似示例：

```
A100 SXM4
A100 PCIe

H100 SXM5
H100 PCIe

H200 SXM
H200 PCIe
```

对于 LLM 训练集群（GPT 规模），几乎所有严肃的系统都使用 **SXM + NVLink + NVSwitch**，因为 GPU 之间的通信会成为瓶颈。
