---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CMP 170HX 可解锁替代方案
translated: true
type: note
---

**问题：** 除了 NVIDIA CMP 170HX 之外，还有哪些类似的显卡可以通过类似 `cmpunlocker` 工具的方式解锁——包括其他 GA100 衍生型号或其他厂商的显卡（如 AMD BC-250）？

**答案：**

`cmpunlocker` 项目利用 Falcon BootROM 固件漏洞，移除硬件上出于产品细分目的而被故意限制的软件/OTP 限制。截至 2026 年中，以下是类似的“可解锁”改造显卡的现状：

---

### NVIDIA CMP 170HX (GA100) —— 目标显卡

CMP 170HX 物理上是一颗完整的 GA100 核心（与 A100 数据中心 GPU 相同的硅片），其计算吞吐量、内存容量及其他功能通过 OTP 保险丝和固件强制寄存器锁定被人为限制。

目前已有 **两个独立的解锁工具** 适用于它：

- **`amoghmunikote/cmpunlocker`** —— 修补开源内核模块，通过持久化服务在重启后依然生效。目标驱动版本为 `nvidia-open 610.43.0x`。
- **`d3dx9/cmpunlocker`** —— 利用 Falcon BootROM `.fwsignature_ga100` 加载漏洞，目标驱动版本为 `nvidia-open` 580.x。解锁在断电后会丢失，但后台守护进程每秒会自动重新应用。

2026 年 6 月，ASU 研究员 Jon Pry 发表了一篇论文，揭示了 NVIDIA Falcon 安全协处理器中的一个栈保护漏洞，从而能够在纯软件层面移除 CMP 170HX 上所有关于计算限制、内存锁定和 PCIe 带宽的限制。

**内存解锁结果：**

- 8GB 版本可解锁至 64GB，10GB 版本可达 80GB——但结果无法保证。据报道，稳定可靠的结果通常更低，32GB 至 40GB 被认为是更现实的水平。

**价格警告：**

- 在此之前，170HX 在 eBay 上的价格约为 250 美元，但随着漏洞利用的传播，价格已飙升至 1000 美元以上。

---

### AMD BC-250 —— AMD 最接近的对应产品

BC-250 最初为以太坊挖矿设计，采用阉割版 PS5 APU：6 个 Zen 2 核心（全部 8 个可解锁）、24 个 RDNA2 计算单元（"Cyan Skillfish"）以及 16GB 共享 GDDR6 显存。

与 CMP 170HX 类似，它也有可通过软件解锁的计算单元：

- GPU 目前有 24 个 CU 处于活动状态（完整 PS5 APU 为 36 个）。两个被禁用的 CPU 核心并未物理熔断，可以重新启用。
- 当应用 CU 解锁补丁后，系统可识别出 40 个 CU——超过 PS5 的 36 个单元规格——在 Furmark 等基准测试中已确认有性能提升。然而，标准散热器仅设计用于 24 个 CU，因此热节流是一个实际隐患。
- 截至 2026 年 8 月，使用内核 7.1.5、修正的 TLB 刷新、硬件调度、40 CU 解锁以及 flush-on-unmap 工作区后，ROCm 计算已实现经验证正确的 GEMM、PyTorch matmul、FP64 以及文本验证的 llama.cpp 推理。Vulkan 仍保有大约 10 倍的提示处理优势，并且仍然是推理的实际默认选择。

社区成员正在积极将其用于 AI：两块 BC-250 通过 llama.cpp RPC 运行，可以在总价约 300 美元的情况下以 Q4 运行 Qwen 27B 和 35B 模型。

---

### 汇总对比

| 显卡 | 芯片 | 解锁类型 | 显存 | 预计价格（2026 年） |
| --- | --- | --- | --- | --- |
| NVIDIA CMP 170HX | GA100（A100 核心） | Falcon BootROM 漏洞（纯软件） | 8/10 GB → 最高 64/80 GB | 1000–2000 美元 |
| AMD BC-250 | PS5 APU（RDNA2） | 内核补丁（纯软件） | 16GB 共享 | 约 100–200 美元 |

这两款显卡的核心故事相同：与另一款被改造的加密设备 AMD BC-250 情况类似——硬件因特定市场被人为阉割，现在正被复活用于 AI 推理工作负载。

**目前没有其他 GA100 显卡** 被认为在 `cmpunlocker` 的适用范围内——CMP 170HX 是唯一一款在二手市场大量流通、可被消费者接触到的 GA100 SKU。

---

**参考资料：**

- [amoghmunikote/cmpunlocker (GitHub)](https://github.com/amoghmunikote/cmpunlocker)
- [d3dx9/cmpunlocker —— 替代解锁工具 (GitHub)](https://github.com/d3dx9/cmpunlocker)
- [Tom's Hardware —— CMP 170HX 解锁报道](https://www.tomshardware.com/pc-components/gpus/nvidia-crypto-mining-gpus-hacked-to-restore-locked-away-vram-in-order-to-feed-ai-boom-software-mod-unlocks-64gb-of-vram-on-usd250-cmp-170hx)
- [AMD BC-250 社区文档](https://elektricm.github.io/amd-bc250-docs/)
- [akandr/bc250 —— BC-250 AI 推理指南 (GitHub)](https://github.com/akandr/bc250)
- [Hackaday —— BC-250 计算单元解锁](https://hackaday.com/2026/06/09/re-enable-all-compute-units-on-the-ps5-like-bc-250-cryptomining-card/)
- [170th Street GitBook —— CMP 170HX 社区资源](https://170th-street.gitbook.io/hx/unlock/current-unlock)
