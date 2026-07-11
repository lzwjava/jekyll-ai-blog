---
audio: false
generated: true
image: false
lang: zh
layout: post
title: JTPM1离散式TPM接口
translated: true
type: note
---

问题：主板上的 JTPM1（TPM 2.0 接口）连接器是做什么用的？

答案：

`JTPM1` 是主板上的一排物理排针（通常是一个小的 14-20 针插槽），用于插入一个**可选的独立 TPM（Trusted Platform Module，可信平台模块）模块**——一种小型附加卡，提供硬件安全芯片。

**从机制层面看，TPM 实际的作用：**

- 它是一个独立于 CPU 的专用加密处理器，拥有自己少量防篡改存储空间。
- 它生成并存储加密密钥（RSA/ECC），使得**私钥永远不会离开芯片**——即使操作系统或磁盘被攻破，密钥也无法被提取，只能通过向 TPM 发起请求来使用。
- 它执行 **measured boot（度量启动） / remote attestation（远程证明）**：在每个启动阶段（UEFI 固件 → 引导加载程序 → 操作系统），它对即将运行的代码进行哈希计算，并将哈希值扩展到 PCR（Platform Configuration Register，平台配置寄存器）槽位中。这会形成一条度量链，后续可以验证其是否被篡改过。
- Windows 将其用于 **BitLocker** 全盘加密（将磁盘加密密钥锁定到已知良好的启动状态）以及 **Windows Hello** / 凭据存储。

**为什么你的主板既有这个接口又不严格需要它：**

大多数现代 Intel/AMD CPU 已经内置了 **fTPM**（firmware TPM，固件 TPM）——Intel 称之为 PTT（Platform Trust Technology，平台可信技术）。你可以在 BIOS 中启用它，无需额外硬件，并且它满足 Windows 11 的 TPM 2.0 要求。物理的 `JTPM1` 接口是为那些希望使用 **独立硬件 TPM** 的人准备的，这种方式在安全性上略高（独立硅片 vs 与其他内容运行在同一芯片上的固件），但除非你有特定的合规/企业需求，否则很少有必要。

**对你而言实际意义：** 你几乎肯定不需要购买独立的 TPM 模块。进入 BIOS，启用 Intel PTT（通常在 Security 或 Advanced > Trusted Computing 下），这就能满足 Windows 11 或任何度量启动场景的 TPM 2.0 要求。在 99% 的装机中，`JTPM1` 接口只是空置未用。
