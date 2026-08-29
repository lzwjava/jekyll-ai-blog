---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 显卡万用表蜂鸣含义
translated: true
type: note
---

**问题：** 使用晨洲导 8901S 万用表的通断/蜂鸣模式测量 GPU 板时，触碰 HDMI 端口及附近的元件/焊点会发出“嘀”声，这代表什么？

**回答：**

**蜂鸣声表示您触碰的两个点之间存在电气导通。**

---

**通断（蜂鸣）模式的作用：**
- 该模式会在两支表笔之间施加一个微小电流
- 如果两点之间的电阻**非常低（通常 < 30–50Ω）**，万用表会**发出蜂鸣声**
- 这确认了两点之间存在**电气连接**

---

**在 GPU 板靠近 HDMI 端口的位置，蜂鸣声可能表示：**

| 场景 | 含义 | 正常还是异常？ |
|---|---|---|
| 触碰相互连通的 **GND 焊点** | 正常的地网络 | ✅ 正常 |
| 触碰**同一走线/网络上的两个点** | 它们共享同一电路路径 | ✅ 正常 |
| 触碰 **HDMI 引脚 → 附近的旁路电容** | 该电容位于该信号线上 | ✅ 正常 |
| 触碰**两个本不该相连的点** | 存在短接 | ❌ 问题 |
| **HDMI 引脚 → GND** 立即蜂鸣 | 该引脚可能对地短路 | ❌ 需排查 |

---

**关键点——如何判断：**

> 蜂鸣声本身**并不自动代表异常**。您需要知道**电路图**或预期的连接关系，才能判断两点之间**应该或不应该**存在导通。

- 如果您在进行**故障诊断**，在**电源引脚与 GND 之间**测量——此处蜂鸣通常意味着**短路**，属于问题。
- 如果您在进行**走线通断检查**，蜂鸣声仅确认铜走线完好——这是好的。

---

**GPU 板诊断实用提示：**

1. **始终将一支表笔放在已知的 GND 点上**（金属屏蔽罩、GND 焊盘）
2. 用另一支表笔触碰 HDMI 引脚、电容和电感周围
3. **意外的蜂鸣声**（本该隔离的引脚）= 潜在短路
4. **期望有蜂鸣声却没有** = 走线断裂或焊盘脱落（断路）

参考资源：
- [How to Use Continuity Mode on a Multimeter](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter/continuity)
- [Using a Multimeter for PCB Fault Finding](https://www.electroschematics.com/using-multimeter-for-pcb-fault-finding/)
- [GPU Repair – Short Circuit Detection Guide](https://www.youtube.com/results?search_query=gpu+repair+short+circuit+multimeter+continuity)