---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Go-Back-N滑动窗口协议
translated: true
type: note
---

**Go-Back-N（GBN）** 是一种构建在不可靠网络之上的可靠数据传输协议。其核心思想是：

> 发送多个数据包而无需等待每个 ACK，但如果某个数据包丢失，则重传该数据包 **及其之后的所有数据包**。

### 1. 停止等待 → 滑动窗口

停止等待：

```text
发送方                         接收方
  | ---- 数据包 0 ------------> |
  | <---- ACK 0 --------------- |
  | ---- 数据包 1 ------------> |
  | <---- ACK 1 --------------- |
```

同时只能有一个数据包“在途”。

GBN 允许一个 **窗口** 的数据包：

```text
发送方                         接收方

  | ---- 数据包 0 ------------> |
  | ---- 数据包 1 ------------> |
  | ---- 数据包 2 ------------> |
  | ---- 数据包 3 ------------> |
  | <---- ACK 0 --------------- |
  | <---- ACK 1 --------------- |
```

如果：

```text
窗口大小 = 4
```

则发送方最多可以有 4 个未确认的数据包。

---

### 2. 发送方窗口

假设：

```text
seq = 0 1 2 3 4 5 6 7 ...
             ^
          窗口 = 4
```

初始状态：

```text
[0 1 2 3] 4 5 6 7
 ^       ^
base    nextseqnum
```

* `base` = 最老的未确认数据包
* `nextseqnum` = 下一个可发送的数据包
* `N` = 窗口大小

发送方在满足以下条件时可以发送：

```python
nextseqnum < base + N
```

当 ACK 到达时，窗口滑动：

```text
ACK 0

    [1 2 3 4] 5 6 7
```

然后：

```text
ACK 1

      [2 3 4 5] 6 7
```

因此称为 **滑动窗口**。

---

### 3. 重要的 GBN 行为

考虑：

```text
发送方                         接收方

数据包 0 --------------------> OK
数据包 1 --------------------> OK
数据包 2 --------X             丢失
数据包 3 --------------------> 
数据包 4 -------------------->
```

接收方期待数据包 `2`。

它收到了 `3`，但：

```text
期望 = 2
收到 = 3
```

GBN 接收方通常 **丢弃数据包 3**。

然后也丢弃 4。

它持续发送对最后一个正确接收的 **按序** 数据包的 ACK：

```text
ACK 1
```

最终发送方对数据包 2 的定时器超时：

```text
超时(数据包 2)
```

然后：

```text
数据包 2 -------------------->
数据包 3 -------------------->
数据包 4 -------------------->
```

这就是名称的由来：

> **Go back to N** — 回到丢失的数据包并从此处开始重传。

---

### 4. 最小的发送方状态

你可以把 GBN 基本上理解为：

```python
base = 0
next_seq = 0
N = 4

while True:
    if next_seq < base + N:
        send(packet[next_seq])
        next_seq += 1

    ack = receive_ack()

    if ack is not None:
        # 累积 ACK
        base = ack + 1

        if base == next_seq:
            stop_timer()
        else:
            restart_timer()
```

关键特性是 ACK 通常是 **累积的**。

如果接收方发送：

```text
ACK 4
```

大致意味着：

```text
“我已按序收到 0..4”
```

因此发送方可以前进：

```text
base = 5
```

---

### 5. 接收方极其简单

概念上：

```python
expected = 0

while True:
    pkt = receive()

    if pkt.seq == expected:
        deliver(pkt)
        send_ack(expected)
        expected += 1
    else:
        # 乱序
        discard(pkt)
        send_ack(expected - 1)
```

这种简单性是 GBN 的主要特点之一。

接收方 **不会** 缓冲乱序的数据包。

---

### 6. GBN 与 Selective Repeat 的比较

这个区别是重点：

```text
                 丢失 2

GBN:

0 ✓
1 ✓
2 ✗
3 丢弃
4 丢弃

超时 →

2 重传
3 重传
4 重传
```

Selective Repeat：

```text
0 ✓
1 ✓
2 ✗
3 缓冲 ✓
4 缓冲 ✓

超时 →

仅重传 2
```

因此：

|                      | Go-Back-N        | Selective Repeat   |
| -------------------- | ---------------- | ------------------ |
| 乱序数据包           | 丢弃             | 缓冲               |
| ACK                  | 累积             | 通常为单独确认     |
| 数据包 2 丢失       | 重传 2,3,4       | 仅重传 2           |
| 接收方复杂度         | 低               | 较高               |
| 带宽效率             | 较低             | 较高               |

---

### 7. 为什么需要窗口？

因为网络延迟代价很高。

假设：

```text
RTT = 100 ms
数据包传输时间 = 1 ms
```

停止等待：

```text
发送 1ms
等待 ~99ms
发送
等待
...
```

链路利用率大约是：

```text
1 / 100 = 1%
```

使用：

```text
窗口 = 100
```

你可以流水线式发送数据包：

```text
0 1 2 3 4 5 6 7 8 9 ...
→ → → → → → → → → →
```

而较早的数据包正在网络中传输。

保持管道满的基本条件是：

```text
窗口大小 ≳ 带宽 × RTT / 数据包大小
```

或以数据包计：

```text
W ≳ RTT / 数据包传输时间
```

这是 **滑动窗口与高吞吐可靠传输** 之间的核心联系。

---

### 8. 心智模型

将 GBN 想象为：

```text
                 发送方窗口
                       ↓
        ┌──────────────────────────┐
        │  10  11  12  13  14     │
        └──────────────────────────┘
         ↑              ↑
       base          next_seq

                 网络
                    ↓
             10 → 11 → 12 → 13
                       X
                     丢失

超时(12)
    ↓

重传：

             12 → 13 → 14
```

需要内化的三个概念是：

```text
滑动窗口
      +
累积 ACK
      +
超时 → 重传丢失之后的所有内容
      =
Go-Back-N
```

参考资料：

* [RFC 793 — Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc793)
* [Computer Networking: A Top-Down Approach — Reliable Data Transfer](https://gaia.cs.umass.edu/kurose_ross/online_lectures.htm)
