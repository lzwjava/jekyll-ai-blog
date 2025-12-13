---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 华为交换机STP配置命令
translated: true
type: note
---

问题：华为交换机上Spanning Tree Protocol (STP) 的典型命令是什么？

答案：

华为交换机支持多种生成树模式：STP（传统）、RSTP（快速）和MSTP（多实例，许多型号默认）。配置经典STP需要将模式设置为STP，但如今RSTP或MSTP更为常用。

### 全局配置命令
- `stp mode stp`
  将生成树模式设置为经典STP（选项：stp, rstp, mstp）。

- `stp enable`
  全局启用STP（通常默认启用）。

- `stp disable`
  全局禁用STP。

- `stp priority <value>`
  设置网桥优先级（0–61440，4096的倍数；值越低越优先成为根桥）。

- `stp root primary`
  配置交换机作为主根桥（将优先级设置为0）。

- `stp root secondary`
  配置交换机作为次根桥（将优先级设置为4096）。

### 接口配置命令
首先进入接口视图：`interface <interface-type> <interface-number>`

- `stp enable`
  在特定接口上启用STP。

- `stp disable`
  在接口上禁用STP（适用于边缘端口）。

- `stp cost <value>`
  手动设置端口路径开销。

- `stp edged-port enable`
  将端口配置为边缘端口（迅速转换为转发状态；用于连接终端设备）。

- `stp root-protection`
  启用根保护（如果收到优先级更高的BPDU，则阻塞端口）。

- `stp loop-protection`
  启用循环保护（如果停止接收BPDU，则阻塞端口）。

- `stp bpdu-protection`
  （全局或接口）保护边缘端口免受意外BPDU的攻击。

### 显示和验证命令
- `display stp`
  显示详细的STP状态和拓扑。

- `display stp brief`
  显示STP状态的摘要。

- `display stp interface <interface>`
  显示特定接口的STP信息。

- `display stp region-configuration`
  （在MSTP模式下相关）显示MST域详细信息。

除非另有说明，这些命令均在系统视图下执行。在cloud-engine型号上，配置需要根据需要提交或保存。

参考：

- [https://ipcisco.com/lesson/stp-configuration-on-huawei/](https://ipcisco.com/lesson/stp-configuration-on-huawei/)
- [https://support.huawei.com/enterprise/en/doc/EDOC1100198418/9ccc5041/stp-rstp-mstp-vbst-configuration-commands](https://support.huawei.com/enterprise/en/doc/EDOC1100198418/9ccc5041/stp-rstp-mstp-vbst-configuration-commands)
- [https://support.huawei.com/enterprise/en/doc/EDOC1000178165/9ccc5041/stp-rstp-mstp-vbst-configuration-commands](https://support.huawei.com/enterprise/en/doc/EDOC1000178165/9ccc5041/stp-rstp-mstp-vbst-configuration-commands)