---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Microduck开源双足机器人
translated: true
type: note
---

**问题：** GitHub 上的 `microduck` 项目是什么？

**回答：**

**Microduck** 是一个由 [Pollen Robotics](https://pollen-robotics.com/microduck) 构建的开源微型双足鸭子机器人 🦆。以下是详细介绍：

**它是什么**

它是一个使用强化学习策略移动的微型双足机器人。高约25厘米，重约800克，运行在 Rockchip RK3566 SoC 上，以50Hz的控制循环驱动十五个舵机，这些舵机由神经策略、无线电、摄像头和一个能够在不损坏设备的情况下推送新软件的更新系统控制。

**它能做什么**

- 行走（游戏手柄控制）
- 滚动（更换轮子后）
- 拾取物品（嘴部触地，一键操作）
- 被推倒后自行站立
- 踢球、坐下、发出鸭叫声等

**它是如何构建的——内部架构**

它使用 Rust 编写，没有框架，作为一个工作空间。关键守护进程包括：`robotd`（控制循环和电机总线）、`updaterd`（安装签名版本并在失败时回滚）、`configd`（WiFi 和身份）、`btd`（手机蓝牙路径）、`padd`（游戏手柄输入）、`mediad`（WebRTC 摄像头流）和 `tofd`（深度传感器）。它们通过 Unix 套接字上的共享 JSON-RPC 协议进行通信——每个客户端（应用、控制台、游戏手柄、脚本）发送相同的调用。

**AI / 策略方面**

策略在配套仓库 `microduck_rl` 中使用 MuJoCo 和 PPO（一种强化学习算法）进行训练，通过领域随机化实现从仿真到现实的迁移，并导出为 ONNX 格式，然后由本仓库加载。

**目标用户**

该仓库面向两类用户：拥有 Microduck 的用户（快速参考、游戏手柄设置、更新）以及希望在其基础上进行开发或训练新策略的开发者。

---

**参考资料：**

- [pollen-robotics/microduck — GitHub](https://github.com/pollen-robotics/microduck)
- [microduck_rl (策略训练仓库)](https://github.com/pollen-robotics/microduck_rl)
- [架构概览](https://github.com/pollen-robotics/microduck/blob/main/docs/design/architecture.md)
