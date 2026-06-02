---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FDM 中的带宽划分详解
translated: true
type: note
---

问题：在物理信道的可用带宽超过单个原始信号所需带宽的情况下，可以将物理信道的总带宽分成几个与传输单个信号所需带宽相同（或略宽）的子信道，每个子信道承载一个信号。这种技术称为

A. Frequency Division Multiplexing
B. Time Division Multiplexing
C. Wavelength Division Multiplexing
D. Space Division Multiplexing

您的答案：B
正确答案：A

答案：

正确答案是 **A. Frequency Division Multiplexing (频分多路复用, FDM)**。

**解释：**

Frequency Division Multiplexing (FDM) 的工作原理是将物理信道的总可用带宽分成多个较小的频带（子信道）。每个子信道占用不同的频率范围，并承载一个独立的信号。

这种方法正是用于信道带宽远宽于单个信号所需的情况。通过将每个信号分配到自己的非重叠（或略带保护间隙）的频带中，多个信号可以同时在同一物理介质上传输，而不会相互干扰。

**为什么其他选项不正确：**

- **B. Time Division Multiplexing (时分多路复用, TDM)**
  TDM 通过**时间**划分信道，而不是通过频率。不同的信号在分配的时间段内轮流使用**整个带宽**。它**不**将带宽分成子信道。

- **C. Wavelength Division Multiplexing (波分多路复用, WDM)**
  WDM 在概念上类似于 FDM，但专门用于**光纤**通信。它划分光谱（不同波长的光），而不是电频率带。虽然原理类似，但在一般（尤其是非光纤）通信语境中，此描述的标准术语是 FDM。

- **D. Space Division Multiplexing (空分多路复用, SDM)**
  SDM 使用物理分离的路径（不同的电缆、不同的天线、光纤束中的不同光纤、MIMO 空间流等）来承载不同的信号。它**不**涉及划分单个物理信道的带宽。

**总结**
问题中描述的技术——将一个物理信道的**总带宽**分成几个**频率子带**，每个子带承载一个信号——是 **Frequency Division Multiplexing (FDM)** 的经典定义。

因此，正确选择是 **A**。

参考文献：

- 无（数据通信和计算机网络的标准教科书概念）
