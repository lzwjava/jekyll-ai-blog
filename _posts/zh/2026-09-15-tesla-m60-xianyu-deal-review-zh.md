---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 闲鱼Tesla M60交易评测
translated: true
type: note
---

**问题：** 闲鱼上在售的 Tesla M60 16GB（描述为服务器拆机、外观有磨损、功能正常、无修、即插即用）值得买吗？卖家声称适合 AI、渲染、建模、虚拟化，并注明风扇外壳已拆除。

**回答：**

我先直说：M60 和 P100 **是完全不同的显卡**，卖家的一些说法存在误导甚至错误。下面是详细分析：

---

**Tesla M60 的真实定位**

M60 是一款基于 **Maxwell 架构**（2015 年）的 GPU，主要面向 **NVIDIA GRID 虚拟桌面基础设施（VDI）**——也就是企业远程工作站场景，而非计算或 AI 加速。它的规格如下：

- **单卡集成 2× GM204 核心** = 2× 8GB = 总显存 16GB，但两个核心的显存 **不共享统一内存池**——每个 8GB 独立运行
- **FP32 算力：** 双核心合计约 9.6 TFLOPS
- **不支持 FP16 加速**（Maxwell 没有原生 FP16 计算，会回退到 FP32 速度）
- **无 Tensor Core**（Tensor Core 从 2017 年的 Volta 架构才开始引入）
- **TDP：300W** —— 实际上 *比 P100 还高*
- PCIe x16，被动散热（需要服务器风道或直吹风扇，和 P100 情况一样）

---

**卖家声称的评估**

| 声称 | 实际情况 |
|---|---|
| "适合AI" | ❌ 很弱——无 FP16、无 Tensor Core、CUDA 计算效率低 |
| "渲染/建模" | ⚠️ 部分正确——Maxwell 支持 OpenGL/DirectX，但已是十年前的架构 |
| "虚拟化" | ✅ 这正是它的设计用途——GRID vGPU |
| "专业图形加速，CAD/PS/3D" | ❌ 误导——它没有显示输出接口；需要用 Quadro/工作站驱动才能支持 CAD 专业功能 |
| "低功耗静音" | ❌ 错误——300W TDP，被动散热，需要高转速风扇 |
| "即插即用多屏输出" | ❌ 错误——M60 **完全没有视频输出接口**，是一张无头服务器显卡 |
| "风扇外壳拆掉" | ⚠️ 你需要自己 DIY 散热方案，和 P100 一样 |

---

**M60 vs P100 —— 哪个更好？**

| | Tesla M60 | Tesla P100 |
|---|---|---|
| 架构 | Maxwell（2015） | Pascal（2016） |
| 显存 | 2× 8GB（分离式） | 16GB 统一 HBM2 |
| FP16 | ❌ 不支持 | ✅ 支持 |
| Tensor Core | ❌ 无 | ❌ 无（Pascal 代） |
| 显存带宽 | 320 GB/s | **732 GB/s** |
| 最佳用途 | VDI / GRID | 计算 / AI / HPC |
| 市场价格 | 约 30–60 美元 | 约 76–150 美元 |

P100 在几乎所有计算维度上都胜出。M60 的分离式显存架构也是一个实际限制——你无法把 16GB 当作一个连续块来使用。

---

**什么时候 M60 值得买**

- 你在搭建 **VMware Horizon / Citrix / GRID vGPU** 虚拟桌面
- 你需要一块 **便宜的服务器显卡**，且不在意 AI/ML 性能
- 你已有合适的服务器散热方案

**什么时候应该避开：**
- 任何 AI/ML 工作负载——请选 P100 代替
- 任何需要大一统显存的工作负载
- 如果价格接近 P100 水平

---

**最终结论**

M60 是一款被卖家夸大宣传的 VDI 专用卡。在合适的价格（约 200–300 元人民币）下，用于虚拟化还可以。但不要花 P100 的价钱去买它，并且忽略所谓的“AI/渲染”宣传——那只是卖家在广撒网。

---

参考来源：
- [NVIDIA Tesla M60 规格 – TechPowerUp](https://www.techpowerup.com/gpu-specs/tesla-m60.c2760)
- [Tesla M60 vs P100 计算对比 – GPUpoet](https://gpupoet.com)
- [NVIDIA GRID M60 数据表 – NVIDIA](https://images.nvidia.com/content/tesla/pdf/184427-Tesla-M60-DS-NV-Final-designleft.pdf)