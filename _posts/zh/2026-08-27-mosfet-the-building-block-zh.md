---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MOSFET：构成模块
translated: true
type: note
---

**问题：** 什么是 MOSFET？

**答案：**

---

## 🔬 MOSFET — 金属-氧化物-半导体场效应晶体管

MOSFET 是一种**晶体管**——现代电子学中最基本的构建模块。它充当由电压控制的**开关**或**放大器**。

---

## 🧱 物理结构（内部构造）

```
        Gate (G)
          |
  ┌───────┴───────┐
  │   Oxide Layer │  ← insulating SiO₂ (the "oxide")
  │───────────────│
  │  Metal gate   │  ← the "metal" (now usually polysilicon)
  └───────────────┘
  Source (S)     Drain (D)
     │                │
  [N+ region]    [N+ region]
  ───────────────────────────
         P-type silicon body (substrate)
```

三个端子：
| Terminal | 功能 |
|---|---|
| **Gate (G)** | 控制输入 — 此处电压决定导通/关断 |
| **Source (S)** | 电流流入（或流出）端 |
| **Drain (D)** | 电流流出（或流入）端 |

---

## ⚡ 工作原理 —— 核心概念

> **栅极电压控制漏极与源极之间是否有电流流过。**

1. **栅极电压 = 低电平 (0V)** → 无沟道形成 → 晶体管**关断** → 无电流 → 相当于**断开开关**
2. **栅极电压 = 高电平 (如 5V)** → 电场吸引载流子 → 源极与漏极之间形成**导电沟道** → 晶体管**导通** → 有电流 → 相当于**闭合开关**

栅极通过薄氧化层与衬底**绝缘**，因此控制时几乎**不消耗电流**——效率极高。

---

## 🔁 两种主要类型

| 类型 | 载流子 | 栅极为……时导通 |
|---|---|---|
| **N沟道 (NMOS)** | 电子 | 高电平 |
| **P沟道 (PMOS)** | 空穴 | 低电平 |

在 GPU 的 VRM 中，**两种类型配对使用**（称为**互补/半桥**），以高效地推动和拉取电流。

---

## 🎮 MOSFET 在 GPU 中的作用（如 RTX 4070）

在 **VRM（电压调节模块）**中，MOSFET 以**每秒数百万次**（数百 kHz）的频率开关，将 12V 输入电压斩波为精确调节的低电压（例如 GPU 核心的 ~1.0V）：

```
12V ──► [高端 MOSFET] ──► 快速开关导通/关断
                                ↓
                      [电感平滑滤波]
                                ↓
                      ~1.0V 稳定输出 ──► GPU 芯片
```

这种技术称为 **PWM 开关**（脉冲宽度调制）。导通时间与关断时间的比例决定输出电压。

---

## 📦 它们在 PCB 上的外观

在 GPU 板上，MOSFET 通常表现为：
- 靠近电源输入区域的**黑色小矩形芯片**（DrMOS 封装）
- 排列在粗大的电感（线圈）旁边的**行**中
- 负载时**发热严重**，因此 GPU 散热器也会覆盖此区域

---

## 🌍 规模 —— GPU 芯片中的 MOSFET

RTX 4070 的 AD104 芯片包含约 **358 亿**个 MOSFET —— 每个大小仅 **4–5 纳米**，肉眼不可见。这些是 CUDA 核心、缓存单元、逻辑门 —— 芯片内部的一切。

因此，MOSFET 在 GPU 上存在于**两个尺度**：
- **宏观尺度** —— 可见的 VRM 功率晶体管（毫米级）
- **纳米尺度** —— 数十亿个蚀刻在硅芯片内部

---

**参考文献：**
- [MOSFET Explained — Electronics Tutorials](https://www.electronics-tutorials.ws/transistor/tran_6.html)
- [How VRMs Work — Gamers Nexus](https://www.gamersnexus.net/guides/voltage-regulator-module-explained)
- [NVIDIA AD104 Die — TechPowerUp GPU Database](https://www.techpowerup.com/gpu-specs/geforce-rtx-4070.c3924)