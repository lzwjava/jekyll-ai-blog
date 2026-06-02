---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 以太网交换机帧转发分析
translated: true
type: note
---

问题：在给定的 Ethernet 拓扑（见图 28）和当前 switch forwarding table（见表 28）下，host 00-e1-d5-00-23-a1 向 host 00-e1-d5-00-23-c1 发送一个 data frame。收到 frame 后，host 00-e1-d5-00-23-c1 向 host 00-e1-d5-00-23-a1 发送一个 acknowledgment frame。请回答：(1) switch 分别将 data frame 和 acknowledgment frame 转发到哪些 ports？(2) 根据所述过程，绘制更新后的 switch forwarding table。

答案：

由于问题中提到的“Figure 28”和“Table 28”未在文本中提供，我只能给出此类问题最常见和典型的分析模式。以下答案假设了中国大学网络课程（尤其是 408 考试或类似习题）中非常常见的拓扑和初始表。如果您的实际图/表不同，结论可能会有差异。

**此类问题中最常见的拓扑假设：**

- 有一个 switch（通常有 4 个 ports：1、2、3、4）
- Port 1 连接 host A (00-e1-d5-00-23-a1)
- Port 2 连接 host B（某个中间 host，此过程通常不涉及）
- Port 3 连接 host C (00-e1-d5-00-23-c1)
- Port 4 连接另一个 host 或 uplink（有时不涉及）

**最常见的初始 forwarding table 假设：**

| MAC address           | Port |
|-----------------------|------|
| 00-e1-d5-00-23-a1     | 1    |
| 00-e1-d5-00-23-b?     | 2    |  (有时存在，有时为空)
| (其他条目或为空)      |      |

**典型过程和答案：**

**(1) switch 的转发 ports**

- 当 host A (…-a1) 向 host C (…-c1) 发送 data frame 时：
  → Destination MAC = 00-e1-d5-00-23-c1
  → 此时，switch forwarding table **没有 …-c1 的条目**（此类问题中非常常见）
  → switch 执行 **flooding** → 将 frame 转发到 **除入端口（port 1）外的所有 ports**
  → 因此 data frame 转发到 **ports 2、3、4**（通常 port 3 到达 host C）

- 当 host C (…-c1) 向 host A (…-a1) 发送 ACK frame 时：
  → Destination MAC = 00-e1-d5-00-23-a1
  → switch 已学习到 …-a1 → port 1 的条目（在 A 发送第一个 frame 时学习）
  → switch **unicast** → 仅转发到 **port 1**

**(1) 的答案：**
Data frame：转发到 ports **2、3、4**（flooding）
Acknowledgment frame：转发到 port **1**（unicast）

**(2) 更新后的 switch forwarding table**

经过上述两个 frame 通过 switch 后，switch 一定学习到了 host C 的 MAC address。

更新后的 forwarding table（最常见的最终状态）：

| MAC address           | Port |
|-----------------------|------|
| 00-e1-d5-00-23-a1     | 1    |
| 00-e1-d5-00-23-c1     | 3    |
| (如果之前存在 …-b? → 2，则可能仍保留) |      |

**更新表的文本表示：**

```
MAC address             VLAN    Port    Type    Age
00-e1-d5-00-23-a1              1       dynamic
00-e1-d5-00-23-c1              3       dynamic
(可能其他条目保持不变)
```

**核心学习规则提醒（此类问题的关键点）：**

- frame 到达时，switch 总是学习 **source MAC** → 将其与 **入端口** 关联
- 如果 **destination MAC** 在表中 → unicast 到对应 port
- 如果 **destination MAC** 不在表中 → flood 到所有其他 ports
- 返回的 ACK frame 是 switch 学习目的 host 的 MAC-port 映射的最常见方式

如果您的实际 Figure 28 或 Table 28 显著不同（例如多个 switches、hosts 在不同 ports、已存在 …-c1 条目等），请提供拓扑和初始表内容，我可以给出更精确的答案。

参考文献：

- 无（答案基于标准的 Ethernet switch 自学习行为和中国计算机网络考试题的常见模式）
