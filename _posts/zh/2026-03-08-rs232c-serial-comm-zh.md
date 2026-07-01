---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RS-232C 串行通信详解
translated: true
type: note
---

问题：什么是 RS-232C 的全面介绍？

答案：

## RS-232C：全面介绍

---

### 1. 什么是 RS-232C？

RS-232C 是长期确立的标准 RS-232 的早期版本之一，它定义了计算机和相关设备之间相对低速串行数据通信的物理接口。“RS” 代表 “Recommended Standard”（推荐标准），“C” 表示版本（RS-232 的第四次修订）。

RS-232C（也称为 EIA/TIA-232 或 V.28/V.24）是由 Electronics Industry Alliance 制定的异步串行通信接口标准。它定义了 Data Terminal Equipment (DTE)——如计算机或终端——与 Data Circuit-Terminating Equipment (DCE)——如调制解调器或其他串行通信设备——之间的信号和接口。

---

### 2. 历史与演变

最初由 Electronic Industries Association (EIA) 于 1962 年开发，RS-232 定义了 DTE 和 DCE 之间用于串行二进制数据交换的接口。

1969 年 8 月，EIA 发布了 EIA RS-232-C，将电压降低至 12 Vpp，并引入了使用标准 DCE 调制解调器。1975 年，对 RS-232 标准的修改导致了其所谓继任者 EIA RS-422 标准的创建。1981 年，EIA 放弃了所有已发布标准的 “Recommended Standard” 命名，并将其重新发布为 EIA-232-C。1991 年，TIA 和 EIA 联合发布了 ANSI/EIA/TIA-232-E-1991，添加了较小的 26 针 “Alt A” 连接器，并提高了与 ITU-T 标准的兼容性。当前版本的标准是 1997 年发布的 TIA-232-F。

---

### 3. 核心概念：DTE 与 DCE

RS-232 标准详细说明了串行数据传输方法，重点关注称为 Data Terminal Equipment (DTE) 的中央系统与称为 Data Circuit-Terminating Equipment (DCE) 的连接外围设备之间的通信。

- **DTE** (Data Terminal Equipment)：例如，个人计算机或终端
- **DCE** (Data Communication Equipment)：例如，调制解调器或串行转换器

尽管 RS-232C 标准专用于 DTE 和 DCE 之间的通信，但该接口也可用于直接连接两个 DTE 设备或两个 DCE 设备。这可以通过使用 null modem cable（也称为 crossover cable）来实现，该电缆在连接器之一中翻转发送和接收引脚。

---

### 4. 电气特性

RS-232 标准的电气特性部分指定了电压水平、信号水平的變化率以及线路阻抗。驱动器输出的高电平定义为 +5V 至 +15V，低电平定义为 -5V 至 -15V。接收器逻辑电平定义为提供 2V 噪声裕度——接收器的高电平为 +3V 至 +15V，低电平为 -3V 至 -15V。

RS-232 中的逻辑 '1' 被描述为电压范围 -15V 至 -3V，逻辑 '0' 被描述为电压范围 +3V 至 +15V——即低电平电压为逻辑 '1'，高电平电压为逻辑 '0'。历史上，逻辑 '1' (-15V 至 -3V) 被称为 **Marking**，逻辑 '0' (+3V 至 +15V) 被称为 **Spacing**。-3V 至 +3V 之间的任何电压都被视为未定义的逻辑状态。

**关键电气限制：**

- 最大上升率：30 V/ms，以减少相邻信号之间的串扰。最大数据率：20 kbps。驱动器看到的负载阻抗：3 kΩ 至 7 kΩ。原始电缆长度限制：15 米（后来修订为最大电容负载 2500 pF）。

---

### 5. 数据帧格式

RS-232C 串行通信使用发送 (Tx)、接收 (Rx) 和地线进行数据传输。数据沿 Tx 和 Rx 线以预定义帧的形式逐位串行传输。起始位和停止位框定数据位，以标记传输的开始和结束。奇偶校验位也可用于基本错误检查。RS-232C 通信可以是全双工的，允许两个方向的同时传输。

典型数据帧包括：

- **1 个起始位**（始终逻辑 0 / space）
- **5–8 个数据位**
- **可选奇偶校验位**（Even、Odd 或 None）
- **1 或 2 个停止位**（逻辑 1 / mark）

---

### 6. 连接器和引脚定义

RS-232 标准采用 DB9 和 DB25 连接器，每种连接器均以 D 形外观为特征。由于各种行业应用中 25 针连接器的多数引脚利用率有限，制造商采用了 9 针连接器，因为它节省成本并占用更少的物理空间。

**Key DB9 pin signals:**

- **TXD (Transmit Data)**：串行数据线；TXD 从 DTE 向 DCE 发送传出数据。
- **RXD (Receive Data)**：从 DCE 接收传入数据。
- **RTS (Request to Send)**：发送器在需要传输数据时激活此信号；通信停止时停用。
- **CTS (Clear to Send)**：接收器激活此信号，以告知发送器是否准备好接收数据。
- **DTR (Data Terminal Ready)**：DTE 通知 DCE 它处于在线模式，可以进行通信。
- **DSR (Data Set Ready)**：通知 DCE 已准备好进行通信。

---

### 7. 流控制

RS-232C 支持两种流控制类型，以防止缓冲区溢出：

- **Hardware (RTS/CTS) flow control**：使用专用控制引脚 (RTS 和 CTS) 在设备之间信号准备就绪。
- **Software (XON/XOFF) flow control**：在数据流中使用特殊 ASCII 字符 (XON = 0x11, XOFF = 0x13) 来暂停和恢复传输。

---

### 8. Null Modem (DTE 到 DTE 连接)

要直接连接两个 DTE 设备，而无需 DCE 设备，null modem cable 会仔细反转两端 Pin 2 和 Pin 3 之间的 TXD (发送数据) 和 RXD (接收数据) 信号。这是 PC 到 PC 直接串行通信的基础。

---

### 9. 优势

- **Simple wiring**：RS-232C 仅需几根线即可在两个设备之间传输数据。
- **Wide compatibility**：自 1960 年代以来 RS-232C 被广泛采用，并支持大量计算机、调制解调器、工业机器和其他设备。
- **Noise robustness**：信号电压范围为 -15V 至 +15V，RS-232C 通信在电气噪声环境中鲁棒，能抵抗较小电压摆幅的干扰。

---

### 10. 限制

- 不能用于芯片到芯片或芯片到传感器的设备通信。
- 在噪声存在下性能下降，并且由于 DTE 和 DCE 之间有公共地，需要更短的电缆。
- 随着 RS-232C 接口需要单独的收发芯片，系统成本增加。
- 传输速度高时，性能仅限于短距离。

RS-232C 不允许多点连接——它限于两个设备通过专用链路进行串行通信。其他标准可以在共享总线上实现多个设备之间的通信。

---

### 11. 应用

RS-232 仍用于连接旧设计的外围设备、工业设备如 PLC、控制台端口和专用设备。RS-232 端口也常用于与无头系统（如服务器）通信，这些系统未安装显示器或键盘，在操作系统尚未运行的引导过程中。在实验室自动化或测量等领域，RS-232 设备继续被使用。某些类型的可编程逻辑控制器、变频驱动器、伺服驱动器和计算机数控 (CNC) 设备可以通过 RS-232 进行编程。

---

### 12. RS-232C 与现代标准对比

| Feature | RS-232C | USB | RS-485 |
| --- | --- | --- | --- |
| Topology | Point-to-point | Point-to-point (hub) | Multi-drop (up to 32 nodes) |
| Max Speed | 20 kbps | 480 Mbps (USB 2.0) | 10 Mbps |
| Max Distance | ~15 m (spec) / ~2000 m (practical) | 5 m | 1200 m |
| Noise Immunity | Moderate | Lower | High (differential) |
| Complexity | Simple | Complex | Moderate |

如今，在个人计算机的本地通信中，RS-232 大多已被 USB 取代。与 RS-232 相比，USB 的优势在于速度更快且使用较低电压。然而，USB 更容易受到电磁干扰，其最大电缆长度更短——USB 为 3–5 米，而 RS-232 为 15 米（使用适当线路驱动器可更长）。

---

### 总结

RS-232C 是塑造了几十年计算机外围接口的串行通信基础标准。尽管在消费电子领域大多被 USB 和 Ethernet 取代，但它仍深嵌于工业自动化、嵌入式系统和遗留硬件中——因其相对于 USB 的简单性、噪声容忍度和长距离能力而备受重视。

参考文献：

- [RS-232 - Wikipedia](https://en.wikipedia.org/wiki/RS-232)
- [RS-232C: The Essential Guide to Serial Communication - InvGate](https://blog.invgate.com/rs-232c)
- [RS232 Serial Communication Protocol - CircuitDigest](https://circuitdigest.com/article/rs232-serial-communication-protocol-basics-specifications)
- [What is RS-232C? - TechTarget](https://www.techtarget.com/searchnetworking/definition/RS-232C)
- [Fundamentals of RS-232 Serial Communications - Analog Devices](https://www.analog.com/en/resources/technical-articles/fundamentals-of-rs232-serial-communications.html)
- [RS232C for Data Transfer - GeeksforGeeks](https://www.geeksforgeeks.org/rs232c-for-data-transfer/)
- [RS-232 Protocol in Industrial Automation - SolisPLC](https://www.solisplc.com/tutorials/rs232)
- [What is RS-232C? - NinjaOne](https://www.ninjaone.com/it-hub/it-service-management/what-is-rs-232c/)
- [RS232 Explained: A Beginner's Guide - ElectronicsHub](https://www.electronicshub.org/rs232-protocol-basics/)
