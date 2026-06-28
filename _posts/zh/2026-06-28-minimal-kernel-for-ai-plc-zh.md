---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI PLC精简内核
translated: true
type: note
---

Question: Linux 变得过于臃肿了。能否有一个极简内核，只运行带网络功能的 agent？"AI PLC 主板"这个想法可行吗？

Answer:

这里涉及两个独立的想法。让我按顺序来，因为第一个是现实存在的，而第二个比听起来更有趣。

## 1. "极简内核 + agent + 网络"

你说得对，Linux 非常庞大——约 4000 万行代码，其中大部分是你永远不会碰的驱动。但你不必为了得到你想要的东西而 fork Linux。"agent 运行时即操作系统"这个想法已经有多条趋同的发展路径：

**路径 A — Unikernel。** 将你的 agent + 极简网络栈 + 一个 libos 编译成一个可引导的单一镜像。没有系统调用边界，没有通用内核。

```
# Unikraft: 构建一个 unikernel，直接启动进入你的 Rust/C agent 二进制文件
git clone https://github.com/unikraft/unikraft
# kraft build --target qemu/x86_64
# 启动时间约10ms，镜像大小为个位数MB，仅包含所需的网络驱动 + lwIP
```

其思维模型：你的 agent *就是* PID 1，没有 PID 2。lwIP 用约 40KB 提供了 TCP/IP。这确实是 "最小的能做网络并运行一个程序的内核"。

**路径 B — 裸机上的 Rust no_std。** 如果你想像 Karpathy 那样真正学习底层，就自己写内核。`bootloader` + `x86_64` crate 能让你在一个周末内运行到 `_start`，而 `smoltcp` 是一个纯 Rust 的 TCP/IP 栈，无需分配器即可运行。

```rust
// smoltcp: 一个完整的 TCP/IP 栈，约 15k 行代码，no_std，无需堆
// 这就是你极简操作系统的 "网络" 部分
use smoltcp::iface::{Config, Interface};
use smoltcp::wire::{IpAddress, IpCidr};
// device = 你的网卡驱动（virtio-net 在 QEMU 下启动大约需要 200 行代码）
// 然后：agent 从 socket 读取字节，调用推理端点，完成。
```

诚实的限制：一旦你的 agent 需要运行*本地* LLM，你就又需要 CUDA/ROCm/Vulkan 驱动了——这正是你想摆脱的那 3000 万行代码。所以清晰的方案是：**极简内核运行 agent 循环 + 网络，推理通过网络完成**（远程 API 或独立的加速节点）。内核根本不需要 GPU 驱动。

**路径 C — 但经过裁减的 Linux。** `tinyconfig` + buildroot 可以得到一个可启动的 5MB 以下 Linux。不那么纯粹，但当你最终需要驱动生态系统时，你还能保留它。

一个有趣的边界想法，符合你的 AI-native 倾向：**调度器是一个 agent**，而不是固定算法。进程提交意图；LLM 参与的循环策略决定排序/资源分配。这是一个研究方向（见下面的 AIOS），还不是产品，但它是 "agent + 极简内核" 版本中真正新颖的东西，而不仅仅是 "小型 Linux"。

## 2. "AI PLC 主板"

这是个更好的想法，值得精确解释*为什么*。

PLC（可编程逻辑控制器）是工业自动化的核心——工厂流水线、HVAC、水处理。市场由西门子（S7）、罗克韦尔/艾伦-布拉德利、三菱主导。编程模型停留在 1980 年代：梯形图、IEC 61131-3、扫描周期执行。工程师实际上还在画继电器图。它是计算领域中与 AI 最不相关的角落，但涉及数十亿美元的流动。

"将 AI/agent 层放在 PLC 硬件上" 这个论点是真实的，但朴素版本会因一个硬约束而失败：**PLC 是硬实时且安全等级的。** 每个扫描周期必须在 1-10ms 内确定性地完成，每个周期，永远如此。LLM 不能放在那个循环里——非确定性延迟，以及控制输出上的幻觉可能致人死亡或毁坏机器。SIL-2/SIL-3 认证的存在正是为了禁止这种情况。

因此可行的架构是**两层拆分**，这恰好完美映射到你的极简内核想法上：

```
┌─────────────────────────────────────────────┐
│  第 2 层：Agent 平面（你的极简内核盒子）         │
│  - LLM/agent：异常检测、优化、                    │
│    自然语言配置、预测性维护                      │
│  - 软实时，网络化，可以远程                       │
│  - 提出设定值，从不直接执行                      │
└───────────────┬─────────────────────────────┘
                │ 受监督、速率受限、有界命令
┌───────────────▼─────────────────────────────┐
│  第 1 层：确定性控制平面                        │
│  - 经典 PLC 扫描循环 / RTOS                     │
│  - 硬实时，经过认证，笨但安全                    │
│  - 对第 2 层命令强制执行安全边界                │
└─────────────────────────────────────────────┘
```

这正是市场发展的方向，也是真正的机遇所在：

- **控制器上的边缘 AI。** 西门子已经推出了 S7-1500 TM NPU 模块和 "Industrial Edge"；Beckhoff TwinCAT 运行在 x86 上，并添加了 ML 推理运行时。因此现有厂商已经验证了需求，但实现方式笨拙。一个全新设计的板卡，其中 AI 平面是一等公民而非附加卡，是一个真正的突破口。
- **agent 的真正工作不是控制——而是人机界面和优化层。** "为什么 3 号线停了？" → agent 读取标签数据库、历史数据、报警日志，用自然语言回答。"在不降低吞吐量的情况下减少能耗" → agent 运行优化，提出新的设定值，确定性层验证并应用。这是现有厂商不擅长的可防御价值。
- **硬件已经商品化。** 一块 AI-PLC 板卡 = 一个工业 SoC（NXP i.MX，或 RISC-V 芯片）+ 一个 NPU + 加固的 I/O + 一个实时核心。许多 SoC 已经在单晶片上同时提供了 Cortex-M 实时核心和 Cortex-A 应用核心——所以你的两层拆分可以在一个芯片上实现：M 核心上运行 RTOS，A 核心上运行你的极简 agent 内核。这就是关键。

困难之处依次在于：安全认证（缓慢、昂贵，是现有厂商真正的护城河）、工业销售周期（12-24 个月，保守的买家）、以及现场可靠性（20 年的部署寿命，不是快速迭代、打破常规的那一套）。这不是快速迭代的消费品玩法——与你通常的循环相反。

但从战略上看，它异常适合你的情况：它是 AI-native 的，是一个现有厂商结构上不擅长的领域，硬件便宜，一个人带着 agent 就可以在 50 美元的开发板上原型化软件层。正确的第一步实验不是一块板卡——而是**针对模拟或廉价的真实 PLC（OpenPLC 是开源的，运行在树莓派上，使用 Modbus 协议）运行 agent 层**。在触及硅片之前，先证明 agent 平面能在真实工业协议上带来价值。

最小初步构建：

```bash
# 在 Pi/VM 上运行 OpenPLC 运行时 = 你的确定性层，免费
git clone https://github.com/thiagoralves/OpenPLC_v3
# 使用 Modbus TCP。你的 agent 以 Modbus 主站身份连接：
pip install pymodbus
```

```python
from pymodbus.client import ModbusTcpClient
c = ModbusTcpClient("<IP_ADDRESS>", port=502)
# Agent 循环：读取过程标签，推理，提出有界的设定值写入
regs = c.read_holding_registers(0, count=10).registers
# -> 将 regs + 报警上下文输入 LLM -> 获取提议操作
# -> 钳位到安全边界 -> c.write_register(addr, clamped_value)
```

这就是 20 行代码的整个论点：AI 从不接触安全循环，它推理过程并提议有界操作。*令人信服地*构建出这个原型之后，"AI PLC 主板" 就变成了硬件封装决策，而非研究风险。

参考资料：

- [Unikraft](https://github.com/unikraft/unikraft)
- [smoltcp — Rust TCP/IP 栈](https://github.com/smoltcp-rs/smoltcp)
- [Writing an OS in Rust (Phil Opp)](https://os.phil-opp.com/)
- [AIOS: LLM Agent Operating System](https://github.com/agiresearch/AIOS)
- [OpenPLC Project](https://www.openplcproject.com/)
- [Siemens S7-1500 TM NPU](https://www.siemens.com/global/en/products/automation/systems/industrial/plc/simatic-s7-1500/ai.html)