---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络安全中的重传
translated: true
type: note
---

**问题：在网络安全中，重传（retransmission）是什么意思？**

**回答：**

在网络中，**重传** 即 **retransmission**：因为接收方没有正确收到数据包，或者发送方不确定数据包是否到达，所以再次发送相同的数据包。

在基本网络层面：

```
Sender                         Receiver

  Packet #1  ------------------>
             (lost)

  timeout

  Packet #1  ------------------>
             received OK
```

发送方在检测到问题后会重传该数据包。

重传的常见原因：

1. **数据包丢失**

   示例：

   ```
   TCP segment #100
          X  (dropped by router)

   Sender waits...
   Sender sends #100 again
   ```

2. **数据损坏**

   接收方检查校验和：

   ```
   received packet
        |
        v
   checksum OK? ---- no ----> discard
                              |
                              v
                         sender retransmits
   ```

3. **没有确认（ACK）**

   TCP 使用 ACK：

   ```
   Client                         Server

   Data ------------------------>

        <---------------- ACK 100

   ```

   如果 ACK 一直没有到达：

   ```
   Data ------------------------>

   (no ACK)

   timeout

   Data ------------------------>
   ```

---

## 安全意义：重传攻击

在安全领域，“retransmission”经常与 **重放攻击（replay attacks）** 一起讨论。

重放攻击滥用重传：

```
Original communication:

User ---- "Transfer $100" ----> Bank


Attacker captures:

"Transfer $100"


Later:

Attacker ---- "Transfer $100" ----> Bank
```

攻击者并没有创建新数据；他们是在**重放旧的合法数据**。

安全协议通过以下方式防止这种情况：

### 1. Nonce（随机数）

```
Request:
    nonce = 839201

Response:
    sign(nonce + data)
```

带有另一个 nonce 的已捕获旧消息将变得无效。

### 2. 序列号

例如 TCP：

```
Packet:
sequence = 1000
data = hello
```

接收方会记住：

```
already received sequence 1000
```

重复的数据包将被忽略。

### 3. 时间戳

```
message timestamp = 10:30:01

current time = 10:40:00

too old -> reject
```

---

所以：

* **网络：** 重传 = 因为投递失败而再次发送相同的数据包。
* **安全：** 当攻击者重放旧的合法消息时，重传可能变得危险；这被称为 **重放攻击**。

TCP 重传是正常的可靠性行为。重放攻击则是恶意的重传。
