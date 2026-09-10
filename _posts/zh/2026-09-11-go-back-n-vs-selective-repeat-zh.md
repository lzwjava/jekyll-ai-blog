---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 后退N帧与选择重传
translated: true
type: note
---

Question: Explain **Go-Back-N ARQ** and **Selective Repeat ARQ**.

Answer:

两者都是 **ARQ（自动重传请求）** 协议。基本思想是：

> 发送方发送数据包 → 接收方检测到丢失/错误 → 接收方请求重传。

关键区别在于 **当单个数据包丢失时，重传哪些数据包**。

### 1. Go-Back-N ARQ（回退 N 步）

假设发送方发送：

```text
Sender:   [1] [2] [3] [4] [5] [6]
                    X
                  lost
```

数据包 **3** 丢失。

接收方收到：

```text
1 ✓
2 ✓
3 ✗
4 ✓   ← 已接收，但因 3 缺失而被丢弃
5 ✓   ← 被丢弃
6 ✓   ← 被丢弃
```

接收方实际上发送：

```text
ACK 2
```

意思是：

> “我已成功接收到数据包 2 为止的所有内容。请从数据包 3 开始重新发送。”

因此发送方 **回退到 3**：

```text
             retransmit
                  ↓
Sender:   [3] [4] [5] [6]
```

这就是为什么它被称为 **Go-Back-N**。

#### 示例

```text
Send:       1  2  3  4  5
                X

Receive:    1  2     4  5
            ✓  ✓     ✗  ✗

Retransmit:       3  4  5
```

尽管数据包 4 和 5 已成功接收，它们仍被重新发送。

**优点：** 接收方实现简单。

**缺点：** 当数据包丢失率高时浪费带宽。

---

### 2. Selective Repeat ARQ（选择重传）

相同的情况：

```text
Sender:   [1] [2] [3] [4] [5]
                    X
```

接收方收到：

```text
1 ✓
2 ✓
3 ✗
4 ✓
5 ✓
```

与 Go-Back-N 不同，接收方 **缓存 4 和 5**。

它告诉发送方：

```text
ACK 1
ACK 2
ACK 4
ACK 5
```

或者等价地指示：

```text
3 需要重传
```

然后发送方仅重传：

```text
[3]
```

收到 3 后：

```text
1 2 3 4 5
✓ ✓ ✓ ✓ ✓
```

所以：

> **选择重传仅重传实际丢失或损坏的数据包。**

---

### 核心区别

|                                        | Go-Back-N           | Selective Repeat  |
| -------------------------------------- | ------------------- | ----------------- |
| 数据包 3 丢失                           | 重传 3,4,5...       | 仅重传 3          |
| 接收方是否缓存乱序数据包？             | 通常不              | 是                |
| 实现复杂度                             | 较简单              | 更复杂            |
| 带宽效率                               | 较差                | 更好              |
| 高丢包率网络                           | 效率较低            | 效率较高          |
| 接收方内存需求                         | 较低                | 较高              |

### 类比 TCP

想象你在下载：

```text
1 2 3 4 5 6 7 8
```

数据包 3 丢失。

**Go-Back-N：**

```text
1 2 [3 4 5 6 7 8]
      ↑
    resend all
```

**Selective Repeat：**

```text
1 2 [3] 4 5 6 7 8
      ↑
    resend only 3
```

基本的权衡是：

```text
Go-Back-N
    ↓
接收方更简单
    ↓
更多重传

Selective Repeat
    ↓
接收方更多状态/缓存
    ↓
更少重传
```

一个细微之处：**现代 TCP 并非纯粹的 Go-Back-N 或纯粹的 Selective Repeat**。TCP 的累积 ACK 行为类似于 Go-Back-N，而 **SACK（选择性确认）** 使其具有类似选择性重传的重传行为。

我还可以详细讲解 **带序列号和 ACK/超时定时的滑动窗口 ARQ**，这会让 GBN 与 SR 的对比更加直观。