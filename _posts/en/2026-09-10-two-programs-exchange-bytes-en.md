---
audio: false
generated: true
image: false
lang: en
layout: post
title: Two Programs Exchange Bytes
translated: false
type: note
---

Question: **How should I understand data communication as something that happens between two programs?**

Answer:

The cleanest mental model is:

> **Two programs communicate by writing bytes into a communication channel, and the other program reads those bytes.**

The network is just one kind of channel.

### 1. Start with two processes

Imagine:

```text
Program A                         Program B
┌─────────────┐                   ┌─────────────┐
│ application │                   │ application │
│             │                   │             │
│ "hello"     │                   │             │
└──────┬──────┘                   └──────▲──────┘
       │                                 │
       │ write bytes                     │ read bytes
       ▼                                 │
   ┌─────────────────────────────────────────┐
   │          communication channel          │
   └─────────────────────────────────────────┘
```

Suppose A wants to send:

```text
hello
```

At the lowest level, it becomes bytes:

```text
h     e     l     l     o
01101000 01100101 01101100 01101100 01101111
```

Program A does something conceptually like:

```python
socket.send(b"hello")
```

Program B does:

```python
data = socket.recv(1024)
```

That's the fundamental operation.

---

### 2. Where does the data actually go?

For two programs on **different machines**:

```text
Program A
   │
   ▼
socket
   │
   ▼
TCP
   │
   ▼
IP
   │
   ▼
Ethernet / Wi-Fi
   │
   ▼
========= network =========
   │
   ▼
Ethernet / Wi-Fi
   │
   ▼
IP
   │
   ▼
TCP
   │
   ▼
socket
   │
   ▼
Program B
```

This is why networking is often described as a **layered communication system**.

Your program doesn't directly manipulate Ethernet frames.

It says:

```python
send(b"hello")
```

The OS/network stack progressively wraps the data.

Conceptually:

```text
Application:
    "hello"

TCP:
    [TCP header]["hello"]

IP:
    [IP header][TCP header]["hello"]

Ethernet:
    [Ethernet header][IP header][TCP header]["hello"]
```

Then the bits physically travel through the network.

At B, the reverse happens:

```text
Ethernet
    ↓
IP
    ↓
TCP
    ↓
application
    ↓
"hello"
```

---

### 3. The important distinction: process vs machine

This is a very useful way to think about networking:

```text
Process A
    │
    │ socket
    ▼
Operating System A
    │
    │ network
    ▼
Operating System B
    │
    │ socket
    ▼
Process B
```

**TCP/IP doesn't fundamentally connect "machines".**

It provides communication between **endpoints**, which applications access through sockets.

For example:

```text
10.0.0.5:5000
       │
       │ TCP connection
       ▼
10.0.0.8:8000
```

You can think:

```text
process A
   ↕
10.0.0.5:5000
   ↕
     TCP
   ↕
10.0.0.8:8000
   ↕
process B
```

The IP identifies the host/interface; the port identifies the endpoint/application service on that host.

---

### 4. But what exactly is being communicated?

This is where **protocols** become important.

TCP doesn't know that you're sending:

```json
{"name": "Zhiwei", "age": 31}
```

To TCP, it's just:

```text
bytes bytes bytes bytes ...
```

Your application protocol gives those bytes meaning.

For example HTTP:

```text
GET /hello HTTP/1.1
Host: example.com
```

HTTP says:

> "These bytes represent an HTTP request."

TCP says:

> "I'll provide a reliable ordered byte stream."

IP says:

> "I'll try to deliver this packet to this IP address."

Ethernet says:

> "I'll transport this frame over this local link."

Each layer has a different job.

---

### 5. This explains the TCP "stream" concept

Suppose A executes:

```python
send(b"hello")
send(b"world")
```

B is **not guaranteed** to receive:

```python
recv() -> b"hello"
recv() -> b"world"
```

It might get:

```python
recv() -> b"helloworld"
```

or:

```python
recv() -> b"hel"
recv() -> b"loworld"
```

because TCP provides a **byte stream**, not a message stream.

Therefore application protocols often need framing:

```text
[length][payload]
[length][payload]
[length][payload]
```

For example:

```text
0005 hello
0005 world
```

Now B knows where one application message ends.

This is one of the most important things to understand about data communication.

---

### 6. Then distinguish three different things

When studying computer networks, don't mix these up:

```text
                    DATA COMMUNICATION

Application protocol
        │
        │ "What do these bytes mean?"
        ▼
TCP / UDP
        │
        │ "How are bytes/datagrams transported?"
        ▼
IP
        │
        │ "Where should packets go?"
        ▼
Link layer
        │
        │ "How do I move frames over this link?"
        ▼
Physical medium
        │
        │ electrical / optical / radio signals
        ▼
       bits
```

So when your textbook says **data communication**, mentally translate it to:

> **Program A produces information → the OS/network stack transforms it into signals → another OS/network stack reconstructs bytes → Program B interprets those bytes.**

That's the whole picture.

A very effective next step is to build this yourself with a tiny Python TCP client/server and observe `send() → TCP → packets → recv()` using `tcpdump`/Wireshark. I can walk you through that experiment from raw bytes upward.
