---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CMP 90HX 算力解锁项目
translated: true
type: note
---

这是一个针对 **NVIDIA CMP 90HX** GPU 的 **硬件修改/固件解锁项目**。（注意：根据报告将其与 RTX 3090/3080Ti 对比，“CMP90HX”似乎并非 NVIDIA 官方部件号——它看起来是 GA102 核心（用于 RTX 3090）的定制营销矿卡变体。）

以下是该项目各层级的功能说明：

## 项目简介

一个驱动级别的 **算力解锁**（哈希/挖矿算力解锁）工具链，适用于 NVIDIA 开放内核模块 `580.159.03`，运行环境为 Linux/systemd/root。目标是通过 PCI ID `10de:220d / 10de:1555` 识别的显卡。

## 核心技术（补丁）

该 GPU 出厂时算力受限（仅计算型“GSP-RM”固件）。补丁（`patches/0001-58015903-cmp90hx-direct-compute.patch`）修改了 NVIDIA 内核模块的 GSP（图形系统处理器）引导路径，在启动过程中的一个精确窗口内执行以下操作：

1. **打开 PLM** — 写入伪造的“签名”载荷（`CMP90HX_FEAT_OVR_PLM @0x00823804`），并重复调用 V67 引导加载程序两次，直到 PLM（访问门控熔丝）读回 `0xffffffff`（已打开）。
2. **写入计算速度选择器** — 使用已知解锁值写入 `SS0`（`FEAT_OVR_SM_SPD`）和 `SS1`（`FEAT_OVR_SM_SPD_1`），并进行回读验证。
3. **立即恢复原始签名**（以免模块处于被修改状态），然后返回错误强制驱动程序停止——实际持久化更改的 PCIe **总线复位**随后通过 systemd 完成。

该引导过程是临时的：运行一个自定义编译的 `nvidia.ko.bootstrap` 模块，完成写入操作后，一个 systemd 服务执行 2 次 PCIe `bus` 复位，然后恢复为未修改的原始 NVIDIA 驱动程序。

## 运行时系统（systemd）

- `cmp90hx-persistent.service` 在每次启动时运行，**早于** GPU 消费者程序，并且（关键地）早于 HiveOS 的 `hive.service`/`os-core.service`。
- 它会暂停 Hive 服务，**依次**处理显卡（一次一张），执行两次 PCIe 复位，恢复原始驱动程序，然后恢复 Hive 服务。
- `cmp90hx-batch-bus-test.sh` 和 `cmp90hx-v67-one-test.sh` 是工作脚本（`one.sh`/`batch.sh` 是薄封装入口）。

## 分析报告（`分析报告-90HX图形阉割定位.md`）

这是一份独立的调查文档（由贡献者编写），分析了 **该卡游戏/图形性能极差的原因**，与算力解锁不同。关键发现：原因 **并非** 几个寄存器，而是整个 PGRAPH（3D/图形）引擎的私有空间被门控（回读 `0xBADFxxxx`）——因为 GSP-RM 固件完全跳过了图形初始化（纯计算固件变体）。这是一个固件初始化问题，而非硬件熔丝问题（与 170HX 的熔丝限速不同）。该文档还记录了真实的 SKU 级硅片差异（GPC/LTC 数量较少，比 3090 慢约 15-20%），这些差异无法恢复。

## 项目结构

| 文件 | 用途 |
| --- | --- |
| `patches/0001-...patch` | 实际的解锁代码变更 |
| `install.sh` | 验证环境，构建引导模块，安装服务 |
| `verify.sh` / `check.sh` | 启动后验证；`check.sh` 只读读取 9 个 SM 发射速率字段 |
| `remove.sh` | 卸载，恢复原始 `nvidia.ko` |
| `cmp90hx-*.sh` / `defer-services.sh` | 运行时启动脚本 |
| `UPSTREAM_GEN2.md` | 上游 170HX 项目的回顾（明确排除 Gen2 PCIe 路径） |
| `patches/`, `work/`, `scripts/` | 补丁、构建树、Python 辅助脚本 |

**风险提示：** README 强调这是底层内核/驱动/GPU 复位工作，仅适用于此特定硬件+固件组合，需要关闭 Secure Boot，并且在任何 NVIDIA 驱动/内核更新后需要重新验证。在正常使用中，它不会覆盖供应商的运行时模块——它会备份该模块，并仅在短暂的引导窗口期间编辑选择器。
