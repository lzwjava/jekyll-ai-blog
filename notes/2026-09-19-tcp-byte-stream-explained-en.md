---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCP Byte Stream Explained
translated: false
type: note
---

Question: How does TCP rely on a byte stream?

Answer:

The key idea is:

> **TCP does not transmit “messages”; it transmits an ordered stream of bytes.**

Think of TCP as a **pipe** between two applications.

```text
Sender application
      |
      | write("HELLO")
      | write("WORLD")
      v
   TCP sender
      |
      |  byte stream: H E L L O W O R L D
      v
   ===== network =====
      |
      v
   TCP receiver
      |
      | read(...)
      v
Receiver application
```

### 1. TCP gives every byte a sequence number

Suppose the application sends:

```text
HELLO WORLD
```

Conceptually TCP numbers the bytes:

```text
H E L L O _ W O R L D
0 1 2 3 4 5 6 7 8 9 10
```

TCP segments the stream into packets:

```text
Segment A:
seq = 0
data = HELLO

Segment B:
seq = 5
data = " WOR"

Segment C:
seq = 9
data = LD
```

The actual segmentation is determined by TCP/network conditions, **not by application write boundaries**.

---

### 2. Therefore, one `send()` does NOT equal one TCP packet

For example:

```c
send(sock, "HELLO", 5, 0);
send(sock, "WORLD", 5, 0);
```

The receiver might see:

```c
recv(...) -> "HELLOWORLD"
```

or:

```c
recv(...) -> "HEL"
recv(...) -> "LOWO"
recv(...) -> "RLD"
```

or even:

```c
recv(...) -> "HELLOWORLD"
```

There is **no guarantee that the receiver sees the same boundaries**.

That's what people mean by TCP being a **byte-stream protocol**.

---

### 3. TCP guarantees byte order

If the sender's stream is:

```text
ABCDEFGHIJ
```

TCP guarantees that the receiver's TCP layer delivers:

```text
ABCDEFGHIJ
```

not:

```text
ABCDIJEFGH
```

TCP uses sequence numbers and acknowledgments to handle:

```text
loss
reordering
duplication
retransmission
```

For example:

```text
Sender                       Receiver

ABCDE  -------------------->
      seq=0

FGHIJ  ----X   (lost)

KLMNO  -------------------->
      seq=10

                             "I have 0-9,
                              but I'm missing 5-9"

        <---------------- ACK/retransmission

FGHIJ  -------------------->
```

The receiving TCP stack reconstructs the continuous byte stream.

---

### 4. TCP is different from UDP here

UDP preserves **datagram/message boundaries**.

```text
send("HELLO")
send("WORLD")

UDP receiver:

recv() -> "HELLO"
recv() -> "WORLD"
```

TCP:

```text
send("HELLO")
send("WORLD")

TCP receiver could get:

recv() -> "HELLOW"
recv() -> "ORLD"
```

So:

|                    | TCP         | UDP      |
| ------------------ | ----------- | -------- |
| Abstraction        | Byte stream | Datagram |
| Message boundaries | ❌           | ✅        |
| Ordering           | ✅           | ❌        |
| Reliable delivery  | ✅           | ❌        |
| Flow control       | ✅           | ❌        |
| Congestion control | ✅           | ❌        |

### 5. This is why applications need framing

Suppose you implement a protocol:

```text
client -> {"name":"Zhiwei"}
client -> {"name":"Alice"}
```

You **cannot** assume:

```python
recv() == one JSON message
```

because TCP might produce:

```text
{"name":"Zhiwei"}{"name":"Alice"}
```

in one `recv()`.

Or:

```text
{"name":"Zhi
```

followed by:

```text
wei"}{"name":"Alice"}
```

So application protocols build their own **message framing** on top of TCP:

```text
[length][message]
[length][message]
[length][message]
```

For example:

```text
00017{"name":"Zhiwei"}
00017{"name":"Alice"}
```

TCP provides the reliable ordered **byte pipe**; your application decides how those bytes are divided into messages.

**The most important mental model:**

```text
Application protocol
       ↓
   messages
       ↓
   TCP byte stream
       ↓
     IP packets
       ↓
   physical network
```

TCP knows **bytes**, not your application's messages.
