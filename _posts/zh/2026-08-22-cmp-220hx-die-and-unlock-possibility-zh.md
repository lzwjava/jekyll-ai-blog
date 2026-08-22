---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CMP 220HX模具解锁无限可能
translated: true
type: note
---

**问题：** CMP 220HX 使用什么芯片，能否像 CMP 170HX 一样通过 cmpunlocker 解锁？

**答案：**

---

### 芯片：GA100（Ampere A100）

CMP 220HX 与 CMP 170HX 使用相同的 **GA100** 芯片——NVIDIA 旗舰级 Ampere 数据中心芯片，采用 **TSMC 7nm** 工艺制造。GA100 芯片面积达 826 mm²，集成 542 亿个晶体管。

170HX 与传闻中的 220HX 之间的关键区别在于芯片的裁剪程度：

- CMP 170HX 仅启用 4,480 个 CUDA 核心——仅为 GA100 完整设计的 54%——并使用 8 GB HBM2e 显存（双堆栈），4096-bit 位宽，带宽约 1,493 GB/s。
- 220HX 预计将启用更多 SM（接近完整 GA100），从而将算力从 170HX 的 165 MH/s 提升至 210 MH/s。

除了 CUDA 核心数外，NVIDIA 还故意限制了其他功能：FP32/BF16 浮点性能被压缩至约 0.39 TFLOPS，PCIe 链路限制为 Gen 1.1 x4——仅 250 MB/s，而现代 PCIe 4.0 x16 可达 32 GB/s。

---

### 能否解锁？

**简短回答：cmapunlocker 仅官方支持 CMP 170HX，不支持 220HX。**

cmapunlocker 工具专为 **NVIDIA CMP 170HX（GA100）** 设计，可恢复完整 SM 计算吞吐量、解锁 HBM2e 显存几何、PCIe Gen 2 速度以及完整 64 GB BAR1 大小——并通过修补内核模块实现重启持久化。

解锁机制技术深度极高：利用 Falcon 固件漏洞——签名固件缓冲区溢出 → 绕过 canary → 执行 Hypervisor 级（HS）代码 → 解锁权限层级掩码（PLM）→ 覆盖源自熔丝的 SM 速率、帧缓冲区和 PCIe 寄存器设置。

由于 **CMP 220HX 从未正式发布**（它仅停留在传闻阶段——NVIDIA 最终出货的是 170HX），因此没有实际硬件可供目标测试。即便存在 220HX 实体，它也会共享相同的 GA100 芯片和固件锁架构，理论上该漏洞可能适用——但尚未有人实际验证。

**cmapunlocker 在 170HX 上解锁的内容：**

| 功能 | 状态 |
| --- | --- |
| Full SM compute throughput | ✓ 可用 |
| Memory: 64 GB (8 GB card) / 40 GB (10 GB card) | ✓ 可用 |
| PCIe Gen 2 | ✓ 可用 |
| Full 64 GB BAR1 | ✓ 可用 |
| Reboot persistence | ✓ 可用 |

要求：Linux x86-64、root 权限、`nvidia-open 610.43.0x`、禁用安全启动。

---

**参考文献：**

- [cmapunlocker GitHub — amoghmunikote](https://github.com/amoghmunikote/cmpunlocker)
- [The almost A100 – NVIDIA CMP 170HX — DevQuasar](https://devquasar.com/hardware/the-almost-a100-nvidia-cmp-170hx/)
- [NVIDIA CMP 170HX Mining Monster Spotted — Tom's Hardware](https://www.tomshardware.com/news/nvidias-cmp170hx-in-the-wild-with-164-mhps-ethereum-mining-performance)
