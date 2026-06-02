---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Default STP Priority on Huawei Switches
translated: false
type: note
---

**Question:** On a Huawei switch, what is the default priority value of STP (Spanning Tree Protocol)?
A) 0
B) 4096
C) 32768
D) 61440

**Answer:**

The correct answer is **C) 32768**.

This is the default bridge priority value for the device in STP/RSTP/MSTP on Huawei switches. The bridge priority forms the higher part of the Bridge ID (BID), and a lower value increases the likelihood of the switch becoming the root bridge. Priorities must be multiples of 4096, ranging from 0 to 61440.

- 0 is set when configuring the switch as the primary root bridge (using `stp root primary`).
- 4096 is set for the secondary root bridge (using `stp root secondary`).
- 61440 is the maximum possible priority (least likely to be root).

Official Huawei documentation and configuration guides consistently confirm 32768 as the default.

**References:**

- [Huawei Support: stp priority command reference](https://support.huawei.com/enterprise/en/doc/EDOC1100064352/80de11d5/stp-priority) (multiple pages state: "By default, the priority of the switching device in a spanning tree is 32768.")
- [Huawei Configuration Guide: Optional Configuring a Priority for a Switch](https://support.huawei.com/enterprise/en/doc/EDOC1000178310/ecb5760f/optional-configuring-a-priority-for-a-switch-in-an-msti) ("The default priority value of the switch is 32768.")
- [IPCisco Huawei STP Lesson](https://ipcisco.com/lesson/stp-configuration-on-huawei/) (confirms default bridge priority is 32768)
