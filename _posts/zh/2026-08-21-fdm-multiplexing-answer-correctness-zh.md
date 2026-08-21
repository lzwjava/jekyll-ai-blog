---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FDM 复用答案正确性
translated: true
type: note
---

问题：这个关于多路复用问题的答案正确吗？请解释原因。

答案：是的，**A（频分多路复用，FDM）** 是正确的。

问题描述将信道带宽**在频域内**划分为多个子信道，然后将原始信号调制到每个子信道的载波信号上，以便多个信号可以在同一信道上同时传输。这正是FDM的定义。

以下是其他选项错误的原因：

- **B — TDM（时分多路复用）**：在**时域**内划分信道，为不同信号分配不同的时隙。
- **C — WDM（波分多路复用）**：FDM的一种特殊形式，用于**光纤**通信，不同波长的光承载不同信号。
- **D — CDM（码分多路复用）**：为每个信号分配一个唯一的**正交码**，使所有信号同时共享相同的频率和时间。

问题中的关键短语是*"在频域内将信道带宽划分为多个子信道"*，这直接指向FDM。

---

参考：
- [频分多路复用 – 维基百科](https://en.wikipedia.org/wiki/Frequency-division_multiplexing)
- [多路复用技术概述 – GeeksforGeeks](https://www.geeksforgeeks.org/multiplexing-channel-sharing-in-computer-network/)