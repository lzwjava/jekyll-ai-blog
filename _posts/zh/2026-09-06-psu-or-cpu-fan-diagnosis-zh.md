---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 电源或CPU风扇诊断
translated: true
type: note
---

**问题：** 风扇短暂闪烁后停止——如何判断 ATX 12V 引脚问题是电源还是 CPU 引起的？

---

**答案：**

"风扇闪烁后熄灭"的症状是**保护电路触发**的典型表现——某处存在故障，主板立即自行关闭。以下是系统排查的方法。

---

### 🔍 逐步诊断

**步骤 1 — 先检查最明显的：ATX 12V 4-pin 是否真的插上了？**

此症状的常见原因之一就是 CPU 附近主板上没有插入 ATX 12V 4-pin 连接器。请仔细检查是否牢固插入。

---

**步骤 2 — 测试电源本身是否有问题**

使用**回形针测试**在不连接主板的情况下测试电源：
1. 拔掉电源与所有设备的连接
2. 取一个回形针，弯成 U 形
3. 将 20-pin 连接器上的**绿线（PS_ON）**与任意**黑线（GND）**短接
4. 将电源插上墙插并打开开关
5. ✅ 如果电源风扇持续转动 → 电源正常
6. ❌ 如果没有任何反应 → 电源已损坏

---

**步骤 3 — 精简到最小配置**

移除所有部件，只保留：
- CPU + 散热器/风扇
- 1 根内存条
- 主 20-pin 电源
- ATX 12V 4-pin 电源

仅安装一根内存条和 CPU 的情况下，如果 CPU 风扇仍然转动几秒后停止，且无蜂鸣声，则故障指向主板或 CPU。

---

**步骤 4 — 关键线索：拔掉 ATX 12V 4-pin 后尝试**

如果断开 CPU 的 ATX 12V 4-pin 电源后系统保持通电（但无法点亮），这强烈表明问题出在 CPU 或其供电部分，而非电源。如果即使未连接 4-pin 系统也会关闭，则主板可能短路。

---

**步骤 5 — 检查 CPU 散热器**

一个常见原因：散热器安装方向错误或接触不良。CPU 内部温度传感器会立即检测到过热并关闭所有设备。重新安装散热器，确保导热膏涂抹正确。

---

### 🧭 快速诊断汇总表

| 症状 | 最可能原因 |
|---|---|
| 风扇闪烁，电源回形针测试失败 | **电源已损坏** |
| 风扇闪烁，回形针测试通过 | **主板或 CPU** |
| 无 4-pin 时保持通电，插入 4-pin 后关闭 | **CPU 或主板上的 VRM** |
| 安装内存条后无任何蜂鸣声 | **主板很可能故障** |
| 听到蜂鸣声 | **内存问题——尝试重新插拔** |

---

### ⚠️ 你的情况中最可能的元凶

鉴于你使用的是**航嘉 280W 电源**（老旧、低瓦数），电源是首要怀疑对象。旧电源随时间老化，可能无法在负载下提供稳定的 12V 电压——如果电源无法满足系统功率需求，风扇转动一秒后系统就会断电。

---

**参考来源：**
- [风扇转动半秒后停止 — Tom's Hardware](https://forums.tomshardware.com/threads/hit-power-buton-cpu-fan-spins-for-half-a-second-then-stops-spin-and-stop-forever-no-booting.3034486/)
- [无法点亮，风扇转动后停止 — AnandTech](https://forums.anandtech.com/threads/no-post-fan-spins-cuts-out-doesnt-cut-when-cpu-not-plugged-in.1277027/)
- [开机后 CPU 风扇转动 1 秒后关机 — AnandTech](https://forums.anandtech.com/threads/power-on-cpu-fan-spins-for-1-sec-then-power-down.1608528/)