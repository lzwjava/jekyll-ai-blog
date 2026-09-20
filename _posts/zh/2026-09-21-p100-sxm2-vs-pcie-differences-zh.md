---
audio: false
generated: true
image: false
lang: zh
layout: post
title: P100 SXM2与PCIe的差异
translated: true
type: note
---

**问题：** NVIDIA Tesla P100 SXM2 与其 PCIe 版本之间有哪些区别？

**回答：**

Tesla P100 SXM2 和 PCIe 版本共享相同的 GP100 核心和 CUDA 核心数量（3,584 个），但在多个重要方面存在差异：

---

### 1. 外形尺寸与安装方式

SXM2 版本采用 NVIDIA 专有模块，通过 SXM2 插槽直接连接到主板，而非像普通扩展卡那样插入标准 PCIe 插槽。这意味着 SXM2 需要专用的兼容服务器平台（如 NVIDIA DGX-1 或 HGX 主板），而 PCIe 卡可安装到任何标准服务器中。

---

### 2. 计算性能（时钟频率与 FLOPS）

与 SXM2（NVLink）版本相比，PCIe P100 的性能略有降低：

| 指标 | PCIe | SXM2（NVLink） |
| --- | --- | --- |
| 双精度 | 4.7 TFLOPs | 5.3 TFLOPs |
| 单精度 | 9.3 TFLOPs | 10.6 TFLOPs |
| 半精度 | 18.7 TFLOPs | 21.2 TFLOPs |

加速时钟也更低——PCIe 为 1,303 MHz，而 SXM2 为 1,480 MHz。

---

### 3. 内存带宽与容量

12 GB PCIe 版本使用更窄的 3072 位 HBM2 接口，带宽为 549 GB/s，而 16 GB PCIe 版本及所有 SXM2 版本均使用 4096 位接口，带宽高达 732 GB/s。因此，12 GB PCIe 变体在内存带宽方面明显处于劣势。

---

### 4. GPU 间互联（NVLink）

SXM2 版本支持 NVLink，GPU 间带宽为 160 GB/s，而 PCIe 版本无 NVLink，仅受限于 32 GB/s 的 PCIe 带宽。对于多 GPU 工作负载而言，这是最关键的差异。

---

### 5. TDP 与供电

SXM2 需要 300 W 供电，并通过 SXM2 插槽直接取电——无需外部电源线。PCIe 版本的 TDP 较低，更适合标准服务器的电源预算。

---

### 6. 散热

供电由 SXM 插槽处理，加上水平安装方式，可实现更高效的散热机制，使基于 SXM 的 GPU 能够在比 PCIe 版本更高的 TDP 下运行。

---

### 总结表格

| 特性 | P100 SXM2 | P100 PCIe |
| --- | --- | --- |
| 外形尺寸 | 专有 SXM2 插槽 | 标准 PCIe 插槽 |
| 加速时钟 | 1,480 MHz | 1,303 MHz |
| FP32 性能 | 10.6 TFLOPs | 9.3 TFLOPs |
| 内存 | 16 GB HBM2 | 12 GB 或 16 GB HBM2 |
| 内存带宽 | 732 GB/s | 549 GB/s（12 GB）/ 732 GB/s（16 GB） |
| NVLink | 160 GB/s | 无 |
| TDP | 300 W | ~250 W |
| 服务器兼容性 | 需要 NVLink/HGX 平台 | 任何标准服务器 |

**核心结论：** 追求极致性能和多 GPU 扩展（AI/HPC 集群）时选择 SXM2；需要更广泛的硬件兼容性和更低的基础设施成本时选择 PCIe。

---

**参考资料：**

- [NVIDIA Developer Blog – P100 Specs](https://developer.nvidia.com/blog/?p=6535)
- [TechGage – PCIe vs NVLink P100](https://techgage.com/?p=37889)
- [Wikipedia – SXM Socket](https://en.wikipedia.org/wiki/SXM_(socket))
- [IT Creations – Tesla P100 SXM2](https://www.itcreations.com/nvidia-gpu/nvidia-tesla-p100-sxm2-gpu)
