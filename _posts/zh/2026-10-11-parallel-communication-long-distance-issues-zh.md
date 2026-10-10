---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 并行通信长距离问题
translated: true
type: note
---

**问题：** 为什么并行通信不适合计算机网络中的长距离通信？

---

**回答：**

并行通信通过多条导线同时发送多个比特。虽然这看起来更快，但几种物理问题使其在长距离传输中不切实际：

**1. Skew（时序偏移）**  
这是最关键的问题。在发送端同时发送的比特到达接收端的时间不同，因为每条导线具有略微不同的电气特性（电容、电阻、电感）。在短距离内，这种差异可以忽略不计——但在长距离下，偏移会增大到足以导致数据损坏。接收端无法再判断哪些比特"属于同一组"。

**2. 信号衰减**  
所有电信号都会随距离增加而减弱（衰减）。在并行通信中，多条导线各自独立且以不同速率衰减，这使得在所有通道上同时保持一致的信号强度越来越困难。

**3. Crosstalk / 电磁干扰（EMI）**  
多条导线长距离并行运行时，会像天线一样相互感应干扰（串扰）并吸收外部电磁干扰。这会破坏单条线路上的数据，且问题随距离加剧。

**4. 高昂的基础设施成本**  
并行总线需要大量物理导线（例如 8、16 或 32 条）。长距离部署几十根电线比单条串行线路昂贵得多——而由于上述问题，实际上并无性能提升。

**5. 时钟同步困难**  
并行通信通常是同步的——所有比特必须同时被时钟采样。在长距离上分发稳定精确的时钟信号在技术上非常困难且维护成本高昂。

---

**为什么串行通信在长距离上更优**

串行通信通过单条导线逐位发送数据。它完全避免了时序偏移问题，只受单条信号路径的衰减影响，且部署成本远低于并行。现代高速串行协议（如 USB、PCIe、以太网和光纤）采用复杂的编码和纠错技术，在长距离上实现了远超并行总线所能达到的速度。

> **简而言之：** 并行 = 理论上快，实际中长距离不可行。串行 = 更简单、更可靠、可扩展。

---

**参考资料：**
- [Serial vs. Parallel Communication – All About Circuits](https://www.allaboutcircuits.com/technical-articles/serial-vs-parallel-transmission/)
- [Signal Integrity and Skew in Digital Systems – Texas Instruments](https://www.ti.com/lit/an/szza036/szza036.pdf)
- [Data Transmission – Parallel vs. Serial – Cisco Networking Academy](https://www.netacad.com/)