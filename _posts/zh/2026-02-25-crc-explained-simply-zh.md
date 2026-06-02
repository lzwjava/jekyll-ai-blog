---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CRC 简单清晰详解
translated: true
type: note
---

问题：Cyclic Redundancy Check (CRC) 如何工作？

答案：

## 什么是 CRC？

**Cyclic Redundancy Check (CRC)** 是一种错误检测技术，用于确定数据在传输或存储过程中是否已损坏。它通过将数据视为一个大的二进制数并执行多项式除法来工作——该除法的余数成为 **checksum**（也称为 CRC 值），它被附加到数据末尾，并在接收端进行验证。

---

## 核心概念

基本思想是：

1. 发送方和接收方商定一个 **generator polynomial**（除数）。
2. 发送方从数据计算 CRC 余数并附加它。
3. 接收方执行相同的计算。如果余数为 **zero**，则数据完整。如果 **non-zero**，则发生错误。

---

## 逐步过程

### 发送方侧

1. **选择一个 generator polynomial**（例如，`x³ + x + 1`，表示为二进制 `1011`）。
2. **向原始数据附加零**——零的个数等于多项式的度数（即，如果多项式为 3 度，则附加 3 个零）。
3. 对填充后的数据执行 **Modulo-2 division**（基于二进制 XOR 的除法），除数为 generator polynomial。
4. 该除法的 **remainder** 即为 CRC checksum。
5. **用 CRC remainder 替换附加的零**，并传输完整帧（原始数据 + CRC）。

### 接收方侧

1. 取接收到的数据（包括末尾的 CRC）。
2. 使用 **相同的 generator polynomial** 执行 Modulo-2 division。
3. 如果 **remainder 为 0** → 数据无错误 ✅
4. 如果 **remainder 非零** → 数据已损坏 ❌（请求重传）

---

## 示例（简化）

假设：

- 数据位：`1101011011`
- Generator polynomial（密钥）：`10011`（表示 CRC-4）

步骤：

1. 附加 4 个零：`11010110110000`
2. 执行基于 XOR 的（Modulo-2）除法，除数为 `10011`
3. 得到余数，例如 `1110`
4. 传输：`1101011011` + `1110` = `11010110111110`

接收方将 `11010110111110` 除以 `10011`。如果余数 = `0000`，则数据有效。

---

## Modulo-2 Division（XOR Division）

与常规除法不同，Modulo-2 division 使用 **XOR** 而非减法：

- `0 XOR 0 = 0`
- `1 XOR 1 = 0`
- `0 XOR 1 = 1`
- `1 XOR 0 = 1`

没有借位或进位——这使得它在硬件中实现起来极快且简单。

---

## 常见 CRC 标准

| 标准       | 位长度 | 常见用途                  |
|------------|--------|---------------------------|
| CRC-8     | 8 bits | 简单嵌入式系统            |
| CRC-16    | 16 bits | USB、Modbus、存储         |
| CRC-32    | 32 bits | Ethernet、ZIP、PNG、Wi-Fi |
| CRC-CCITT | 16 bits | 电信                      |

更高位长度的 CRC 更健壮，但需要更多计算。**CRC-32** 可以检测任何单突发错误长达 32 位，并对更长错误遗漏的概率非常低。

---

## CRC 能做什么和不能做什么

**CRC 可以：**

- 检测单比特错误
- 检测突发错误（连续损坏比特），长度高达多项式的度数
- 检测大多数随机错误模式

**CRC 不能：**

- **纠正** 错误——它仅检测错误
- 保证检测所有可能的多比特错误（尽管非常有效）
- 提供加密安全性（它可以被逆向工程）

---

## CRC 的使用场景

- **网络：** Ethernet 帧、Wi-Fi 数据包、USB、Bluetooth、CAN bus
- **存储：** 硬盘、SSD、闪存
- **文件完整性：** ZIP、PNG 等文件格式
- **通信协议：** Modbus、A2B、Hamming codes

---

参考文献：

- [Wikipedia – Cyclic Redundancy Check](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)
- [GeeksforGeeks – CRC and Modulo-2 Division](https://www.geeksforgeeks.org/dsa/modulo-2-binary-division/)
- [Lenovo – What is Cyclic Redundancy Check?](https://www.lenovo.com/us/en/glossary/cyclic-redundancy-check/)
- [Cardinal Peak – Understanding the CRC](https://www.cardinalpeak.com/blog/understanding-the-cyclic-redundancy-check)
- [Huawei – What Is Cyclic Redundancy Check?](https://info.support.huawei.com/info-finder/encyclopedia/en/CRC.html)
