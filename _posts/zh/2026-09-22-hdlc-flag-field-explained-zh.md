---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HDLC标志字段详解
translated: true
type: note
---

问题：在HDLC网络中，什么是**F帧**？

回答：

在**HDLC（高级数据链路控制）**中，并没有一个官方称为**“F帧”**的标准帧类型。您可能指的是HDLC帧中的**F（标志）字段**。

### HDLC帧结构

```text
+------+---------+------+-------------+-----+------+
| Flag | Address | Ctrl | Information | FCS | Flag |
+------+---------+------+-------------+-----+------+
  8b      8b       8b       variable    16/32b  8b
```

**标志字段**是：

```text
01111110
```

或：

```text
0x7E
```

它出现在HDLC帧的**开头和结尾**。

### 为什么需要标志？

接收方使用`01111110`来识别**帧边界**：

```text
01111110 | Address | Control | Data | FCS | 01111110
   ↑                                          ↑
 start                                      end
```

因此，如果物理链路只是连续的比特流：

```text
...101100101101011111101011001011...
                  ↑
              frame boundary
```

标志告诉接收方帧的起始/结束位置。

### 有趣的部分：比特填充

因为标志包含：

```text
01111110
```

HDLC必须防止相同的模式意外出现在数据内部。

在**连续五个`1`**之后，发送方插入一个`0`：

```text
Data before stuffing:
01111110

Stuffing:
011111010
       ↑
   inserted 0
```

更准确地说，对于任何数据序列：

```text
11111
```

发送方发送：

```text
111110
```

接收方移除那个填充的`0`。

这意味着标志序列可以保持唯一性：

```text
Flag:       01111110
Data:       011111010
                        ↑
              not interpreted as flag
```

### 最小心智模型

将HDLC视为一种**面向比特的协议**：

```text
          frame
    ┌───────────────────────┐
    ↓                       ↓
01111110  DATA + CONTROL  01111110
   flag                    flag
```

* **标志** → 帧定界符
* **地址** → 目标/站点
* **控制** → 帧类型 + 顺序/控制
* **信息** → 有效载荷
* **FCS** → 错误检测
* **比特填充** → 防止数据看起来像标志

一个重要的区别：**“F帧”中的F很可能被您的课程/教材用来表示标志**，而不是三种标准HDLC帧类型（**I、S、U**）之一。

参考资料：

* [HDLC — ITU-T Recommendation X.25](https://www.itu.int/rec/T-REC-X.25?utm_source=chatgpt.com)
* [HDLC — Wikipedia](https://en.wikipedia.org/wiki/High-Level_Data_Link_Control?utm_source=chatgpt.com)
