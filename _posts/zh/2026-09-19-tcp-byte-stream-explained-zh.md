---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TCP字节流详解
translated: true
type: note
---

问题：TCP 如何依赖字节流？

答案：

关键思想是：

> **TCP 不传输“消息”；它传输有序的字节流。**

把 TCP 想象成两个应用程序之间的 **管道**。

```text
发送端应用
      |
      | write("HELLO")
      | write("WORLD")
      v
   TCP 发送方
      |
      |  字节流: H E L L O W O R L D
      v
   ===== 网络 =====
      |
      v
   TCP 接收方
      |
      | read(...)
      v
接收端应用
```

### 1. TCP 为每个字节分配一个序列号

假设应用发送：

```text
HELLO WORLD
```

从概念上讲，TCP 对字节进行编号：

```text
H E L L O _ W O R L D
0 1 2 3 4 5 6 7 8 9 10
```

TCP 将流分割成数据包：

```text
数据段 A：
seq = 0
data = HELLO

数据段 B：
seq = 5
data = " WOR"

数据段 C：
seq = 9
data = LD
```

实际的分割由 TCP/网络条件决定，**而不是应用的写入边界**。

---

### 2. 因此，一个 `send()` 并不等于一个 TCP 数据包

例如：

```c
send(sock, "HELLO", 5, 0);
send(sock, "WORLD", 5, 0);
```

接收方可能看到：

```c
recv(...) -> "HELLOWORLD"
```

或：

```c
recv(...) -> "HEL"
recv(...) -> "LOWO"
recv(...) -> "RLD"
```

甚至：

```c
recv(...) -> "HELLOWORLD"
```

**不能保证接收方看到相同的边界。**

这就是人们所说的 TCP 是一个 **字节流协议** 的含义。

---

### 3. TCP 保证字节顺序

如果发送方的流是：

```text
ABCDEFGHIJ
```

TCP 保证接收方的 TCP 层交付：

```text
ABCDEFGHIJ
```

而不是：

```text
ABCDIJEFGH
```

TCP 使用序列号和确认来处理：

```text
丢失
乱序
重复
重传
```

例如：

```text
发送方                       接收方

ABCDE  -------------------->
      seq=0

FGHIJ  ----X   (丢失)

KLMNO  -------------------->
      seq=10

                             "我收到了 0-9，
                              但缺少 5-9"

        <---------------- ACK/重传

FGHIJ  -------------------->
```

接收方的 TCP 栈重建连续的字节流。

---

### 4. TCP 在这方面与 UDP 不同

UDP 保留 **数据报/消息边界**。

```text
send("HELLO")
send("WORLD")

UDP 接收方：

recv() -> "HELLO"
recv() -> "WORLD"
```

TCP：

```text
send("HELLO")
send("WORLD")

TCP 接收方可能得到：

recv() -> "HELLOW"
recv() -> "ORLD"
```

所以：

|                    | TCP         | UDP      |
| ------------------ | ----------- | -------- |
| 抽象               | 字节流      | 数据报   |
| 消息边界           | ❌           | ✅        |
| 有序性             | ✅           | ❌        |
| 可靠交付           | ✅           | ❌        |
| 流量控制           | ✅           | ❌        |
| 拥塞控制           | ✅           | ❌        |

### 5. 这就是为什么应用程序需要消息分帧

假设你实现一个协议：

```text
client -> {"name":"智维"}
client -> {"name":"Alice"}
```

你**不能**假定：

```python
recv() == 一条 JSON 消息
```

因为 TCP 可能在一个 `recv()` 中产生：

```text
{"name":"智维"}{"name":"Alice"}
```

或者：

```text
{"name":"智
```

接着是：

```text
wei"}{"name":"Alice"}
```

因此，应用程序协议在 TCP 之上构建自己的 **消息分帧**：

```text
[长度][消息]
[长度][消息]
[长度][消息]
```

例如：

```text
00017{"name":"智维"}
00017{"name":"Alice"}
```

TCP 提供可靠有序的 **字节管道**；你的应用程序决定如何将这些字节分割成消息。

**最重要的思维模型：**

```text
应用协议
       ↓
   消息
       ↓
   TCP 字节流
       ↓
      IP 数据包
       ↓
   物理网络
```

TCP 知道的是 **字节**，而不是应用的消息。