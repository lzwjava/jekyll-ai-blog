---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 华为交换机上STP的默认优先级
translated: true
type: note
---

**问题：** 在华为交换机上，STP (Spanning Tree Protocol) 的默认优先级值是多少？
A) 0
B) 4096
C) 32768
D) 61440

**答案：**

正确答案是 **C) 32768**。

这是华为交换机在 STP/RSTP/MSTP 中设备的默认网桥优先级值。网桥优先级构成 Bridge ID (BID) 的高位部分，值越低，交换机成为根网桥的可能性越大。优先级必须是 4096 的倍数，范围从 0 到 61440。

- 当配置交换机作为主根网桥时（使用 `stp root primary`），优先级设置为 0。
- 当配置为备用根网桥时（使用 `stp root secondary`），优先级设置为 4096。
- 61440 是最大可能优先级（最不可能成为根网桥）。

华为官方文档和配置指南一致确认 32768 为默认值。

**参考资料：**

- [华为支持：stp priority command reference](https://support.huawei.com/enterprise/en/doc/EDOC1100064352/80de11d5/stp-priority)（多处提及：“By default, the priority of the switching device in a spanning tree is 32768.”）
- [华为配置指南：Optional Configuring a Priority for a Switch](https://support.huawei.com/enterprise/en/doc/EDOC1000178310/ecb5760f/optional-configuring-a-priority-for-a-switch-in-an-msti)（“The default priority value of the switch is 32768.”）
- [IPCisco Huawei STP Lesson](https://ipcisco.com/lesson/stp-configuration-on-huawei/)（确认默认网桥优先级是 32768）
