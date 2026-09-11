---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU板中的化学材料
translated: true
type: note
---

问题：GPU 板卡（例如 NVIDIA RTX 显卡）使用了哪些化学材料？

答案：
现代显卡（例如 NVIDIA RTX 显卡）是一个复杂的电子组件，由多个关键部件组成，每个部件都依赖于特定的化学元素和合成材料：

### 1. Silicon Die（GPU 处理器）

* **超纯硅（$\text{Si}$）：** 构成半导体基质（wafer）的核心组件。
* **Dopants：** 诸如 **硼（$\text{B}$）**、**磷（$\text{P}$）** 和 **砷（$\text{As}$）** 等元素被注入以改变硅的电学性能，从而构建晶体管。
* **Interconnect Metals：** **铜（$\text{Cu}$）**、**铝（$\text{Al}$）**、**钴（$\text{Co}$）** 和 **钨（$\text{W}$）** 用于微观层中以连接晶体管。
* **Dielectrics & Semiconductors：** **二氧化硅（$\text{SiO}_2$）**、**氮化钛（$\text{TiN}$）** 和 **钽/氮化钽（$\text{Ta/TaN}$）** 用作绝缘层和阻挡层。

### 2. Printed Circuit Board（PCB）

* **FR-4 Substrate：** 由机织 **玻璃纤维布** 与 **环氧树脂**（polyepoxide）粘合而成的复合材料，提供结构强度和电气绝缘。
* **Copper Foil：** 纯铜薄片层压到基板上，以创建信号通路、电源线和接地层。
* **Solder Mask：** 通常是一种光敏聚合物环氧树脂（通常为绿色、黑色或定制颜色），用于保护铜走线免受氧化和短路。
* **Surface Finishes：** 化学涂层，如 **ENIG（Electroless Nickel Immersion Gold）** 或 **OSP（Organic Solderability Preservatives）**，保护裸露的焊盘。

### 3. Electrical Components（VRMs, Capacitors, Memory）

* **Capacitors：** 铝聚合物电容（使用 **铝** 和导电聚合物）或 MLCC（多层陶瓷电容），使用 **钛酸钡（$\text{BaTiO}_3$）**、**镍** 和 **锡**。
* **Inductors / Chokes：** 铁氧体磁芯由 **氧化铁（$\text{Fe}_2\text{O}_3$）** 与 **锰**、**锌** 或 **镍** 混合而成，并以合成树脂粘结。
* **Solder Alloys：** 无铅焊料通常由 **锡-银-铜（$\text{SAC305}$: $\text{Sn-Ag-Cu}$）** 或 **锡-铋（$\text{Sn-Bi}$）** 组成，用于表面贴装焊接。

### 4. Thermal & Cooling Systems

* **Thermal Interface Materials (TIM)：**

* **Thermal Paste/Grease：** 硅酮聚合物油与导电陶瓷或金属填料混合，如 **氧化锌（$\text{ZnO}$）**、**氧化铝（$\text{Al}_2\text{O}_3$）** 或微粉化的 **银/铝** 颗粒。
* **Liquid Metal（高端/改装）：** 液态合金，主要由 **镓（$\text{Ga}$）**、**铟（$\text{In}$）** 和 **锡（$\text{Sn}$）** 制成。
* **Phase-Change Materials (PCM)：** 聚烯烃或石蜡与导热填料的混合物，在运行热量下熔化/软化。

* **Heatsink & Heatpipes：** **铜（$\text{Cu}$）** 用于均热板和核心接触面；**铝（$\text{Al}$）** 用于散热鳍片；热管内部含有少量蒸馏 **水** 或 **甲醇**，处于部分真空状态。

### 5. Outer Shroud, Frame, and Packaging

* **塑料：** **ABS（丙烯腈-丁二烯-苯乙烯）** 和 **聚碳酸酯（PC）** 用于风扇叶片和外罩。
* **结构金属：** 阳极氧化 **铝** 或 **钢** 用于背板、PCI 支架和内部结构框架。
