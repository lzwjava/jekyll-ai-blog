---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RS-232C 串行通信指南
translated: true
type: note
---

# RS-232C：全面介绍

---

## 1. 什么是 RS-232C？

RS-232C 是长期确立的 RS-232 标准较早的版本之一，它定义了计算机和相关设备之间相对低速串行数据通信的物理接口。“RS” 代表 “Recommended Standard”（推荐标准），“C” 指修订版本。

RS-232C 是一种串行通信协议，允许设备之间交换数据。最初于 1960 年代开发，它奠定了计算机和外围设备通信的基础。串行通信是一种通过单通道逐位传输数据的方法——可以将其想象成一条单车道公路，汽车（数据位）一个接一个行驶，而不是多车道高速公路上并排行驶的多辆汽车（并行通信）。

---

## 2. 历史与演变

RS-232 于 1960 年由 EIA 引入。1969 年 8 月，EIA 发布了 EIA RS-232-C，将电压降低到 12 Vpp，并引入了 Data Communication Equipment (DCE) 调制解调器。1975 年，修改导致了其所谓继任者 EIA RS-422 标准的创建。然而，RS-232 在计算领域越来越受欢迎，并被更新以适应遗留系统。1981 年，EIA 将标准重新发布为 EIA-232-C。1991 年，TIA 和 EIA 共同发布了 ANSI/EIA/TIA-232-E。当前版本 TIA-232-F 于 1997 年发布。

---

## 3. DTE 与 DCE

RS-232C 连接两种类型的设备：DTE（Data Terminal Equipment，数据终端设备）和 DCE（Data Communication Equipment，数据通信设备）。计算机是 DTE；调制解调器是 DCE。DTE 通常配备公连接器，而 DCE 配备母连接器。要识别 DTE 设备，请使用电压表测量 DB-9 连接器的 Pin 3 和 Pin 5——如果得到 -3V 到 -15V 的电压，则它是 DTE 设备。

虽然 RS-232C 专用于 DTE 和 DCE 之间的通信，但该接口也可以通过使用 null modem cable（也称为 crossover cable，交叉电缆）直接连接两个 DTE 设备或两个 DCE 设备，该电缆会翻转其中一个连接器的发送和接收引脚。

---

## 4. 电气特性

RS-232C 使用 **negative logic**（反转电压方案），这与标准 TTL logic 相反：

| State | Meaning | Driver Voltage | Receiver Threshold |
| --- | --- | --- | --- |
| **MARK / Logic 1** | Binary "1" | **-5V to -15V** | -3V to -25V |
| **SPACE / Logic 0** | Binary "0" | **+5V to +15V** | +3V to +25V |
| **Undefined** | Invalid zone | -3V to +3V | — |

Mark 状态是用负电压表示的二进制 1 的高位。发送电压范围为 -5V 到 -15V；接收为 -3V 到 -25V。Space 状态是用正电压表示的二进制 0 的低位。

---

## 5. 连接器与引脚定义

RS-232 数据通过 DB9 连接器的 9 个引脚系列或 DB25 连接器的 25 个引脚传输，尽管并非所有引脚都用于每个应用。

RS-232C（“Recommended Standard 232C”）是一个广泛使用的版本，采用 25 引脚连接器，而后续修订引入了 22 引脚配置。现代实现通常使用 9 引脚 D 型公连接器（DB9），其中包含实际通信所需的最基本信号。

**DB-9 连接器** 的关键引脚：

| Pin | Signal | Direction | Function |
| --- | --- | --- | --- |
| 1 | DCD | In | Data Carrier Detect |
| 2 | RXD | In | Receive Data |
| 3 | TXD | Out | Transmit Data |
| 4 | DTR | Out | Data Terminal Ready |
| 5 | GND | — | Signal Ground |
| 6 | DSR | In | Data Set Ready |
| 7 | RTS | Out | Request to Send |
| 8 | CTS | In | Clear to Send |
| 9 | RI | In | Ring Indicator |

---

## 6. 关键信号说明

**TXD & RXD** 是串行数据线。TXD 将传出数据发送到 DCE；RXD 从 DTE 接收传入数据。**RTS & CTS** 处理握手：发送方在需要传输数据时激活 RTS；接收方激活 CTS 以告知发送方其是否准备好接收。**DTR & DSR** 通知每个设备准备状态——DTR 告知 DCE DTE 已上线；DSR 告知 DCE 已准备好通信。

---

## 7. 数据帧结构

RS-232 使用 **asynchronous communication**（异步通信）——没有共享时钟信号。相反，它在每个字节中插入 Start/Stop 位来同步通信。一个通信数据包（帧）包括：**Start bit**、**Data bits**（7 或 8 位）、**Parity bit**（可选）和 **Stop bit(s)**。Baud rate 表示每秒位传输数量（例如，19200 baud = 19200 bits per second）。

典型数据帧如下所示：

```
[Start bit | D0 D1 D2 D3 D4 D5 D6 D7 | Parity | Stop bit]
```

---

## 8. 奇偶校验与错误检查

Parity 是一种简单的错误检查方法。选项包括 Even、Odd、Mark、Space 或 None。对于 Even parity，串行端口设置 parity bit，使逻辑高位的总数为偶数。对于 Odd parity，parity bit 确保总数为奇数。Mark parity 将位设置为逻辑高；Space 将其设置为逻辑低。

---

## 9. 规范与限制

原始 RS-232 标准设计用于高达 **20 kbps** 的数据交换速率，距离高达 **50 feet (15 meters)**。

RS-232 将 2 个不同设备的地线连接在一起——这是 “unbalanced”（非平衡）连接。非平衡连接更容易受到噪声影响，并有 50 ft（约 15 米）的距离限制。

然而，使用适当的 line drivers，可以实现 2000 米的 RS-232 电缆长度。

---

## 10. 流控制

RS-232C 支持两种类型的流控制：

- **Hardware flow control**：使用专用的 RTS/CTS 信号线，在接收缓冲区满时暂停/恢复数据传输。
- **Software flow control (XON/XOFF)**：在数据流中发送特殊字符来启动（XON = 0x11）或停止（XOFF = 0x13）数据传输。

---

## 11. RS-232C 与现代标准比较

| Feature | RS-232C | RS-422 | RS-485 | USB |
| --- | --- | --- | --- | --- |
| Topology | Point-to-point | Point-to-point | Multi-point | Bus |
| Max Distance | ~15 m | ~1200 m | ~1200 m | 3–5 m |
| Max Speed | 20 kbps | 10 Mbps | 10 Mbps | 480 Mbps+ |
| Noise Immunity | Low | High | High | Medium |
| Wiring | Unbalanced | Balanced | Balanced | Differential |

RS-232 相对于 USB 的优势在于，RS-232 较少受电磁干扰 (EMI) 影响，并且标准定义的最大电缆长度更长（RS-232 为 15 米，USB 为 3–5 米）。如今，RS-232 在个人计算机的本地通信中大多已被 USB 取代。

---

## 12. 应用

RS-232 广泛用于工业通信设备。某些类型的可编程逻辑控制器 (PLCs)、变频驱动器、伺服驱动器和计算机数控 (CNC) 设备可以通过 RS-232 编程。RS-232 端口也常用于与无头系统（如服务器）通信，这些系统未安装显示器或键盘，在启动时无法建立网络连接。在实验室自动化或测量等领域，RS-232 设备仍在继续使用。

---

## 总结

RS-232C 是一种基础串行通信标准，定义了数十年来计算机和外围设备交换数据的方式。尽管在消费产品中已被 USB 和 Ethernet 大多取代，但其简单性、鲁棒性和使用适当驱动器的长距离能力，确保其在工业自动化、嵌入式系统、实验室仪器和遗留设备集成中仍然不可或缺。

References:

- [RS-232 – Wikipedia](https://en.wikipedia.org/wiki/RS-232)
- [RS-232C Definition – TechTarget](https://www.techtarget.com/searchnetworking/definition/RS-232C)
- [RS232 Serial Communication Protocol – CircuitDigest](https://circuitdigest.com/article/rs232-serial-communication-protocol-basics-specifications)
- [RS232C for Data Transfer – GeeksforGeeks](https://www.geeksforgeeks.org/rs232c-for-data-transfer/)
- [Understanding RS-232 Devices – CommFront](https://www.commfront.com/pages/3-easy-steps-to-understand-and-control-your-rs232-devices)
- [What is RS-232? – Cable Matters](https://www.cablematters.com/Blog/Computer-Accessories/what-is-rs232)
- [RS-232C: The Essential Guide – InvGate Blog](https://blog.invgate.com/rs-232c)
