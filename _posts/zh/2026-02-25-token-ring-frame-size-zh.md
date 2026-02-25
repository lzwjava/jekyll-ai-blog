---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 令牌环帧大小答案
translated: true
type: note
---

问题：在 IEEE 802.5 Token Ring 中，MAC frame 有两种基本格式：token frame 和 data frame。token frame 只有多少字节长？  
A. 2 bytes  
B. 3 bytes  
C. 4 bytes  
D. 5 bytes  

答案：  

**正确答案是 B. 3 bytes。**

**详细解释：**

在 IEEE 802.5 Token Ring 标准中，确实存在两种基本的 MAC frame 格式：

1. **Token frame**（纯 token）  
   - 精确由 **3 bytes** 组成：  
     - Starting Delimiter (SD) → 1 byte  
     - Access Control (AC) → 1 byte  
     - Ending Delimiter (ED) → 1 byte  
   - 总长度 = **3 bytes**

2. **Data frame**（也称为 LLC frame 或当携带数据时的 information frame）  
   - 长度更长且可变  
   - 基本结构：SD (1) + AC (1) + FC (1) + Destination Address (6) + Source Address (6) + [Information field, 可变] + FCS (4) + ED (1) + Frame Status (1)  
   - 最小长度通常约为 19–21 bytes（无数据），但可以更长。

标准和大多数教科书中强调的关键区别是 **token 本身只有 3 bytes 长**。

Starting Delimiter (SD) 和 Ending Delimiter (ED) 各自使用 normal Manchester coding 的特殊违反（J 和 K symbols，表示为 "high-high" 和 "low-low" 电平对）来清晰标记 frame 边界并确保数据透明性。

因此，正确选择是 **B. 3 bytes**。

您之前的答案（A. 2 bytes）是错误的。没有主流版本的 IEEE 802.5 Token Ring 标准定义 2-byte token。

参考文献：  

- IEEE 802.5-1998 standard (Token Ring access method and physical layer specifications)  
- 大多数经典计算机网络教科书（例如，Tanenbaum, Kurose & Ross, Peterson & Davie）将 Token Ring token 描述为 3 bytes