---
audio: false
generated: true
image: false
lang: en
layout: post
title: Connection Oriented Network Basics
translated: false
type: note
---

Question: The process of making a daily phone call is described as "pick up the phone - dial the number - connect and talk - hang up." What is the network service called that is similar to this phone call process?

Answer:

The network service similar to the described phone call process is called a **Connection-Oriented** service (or **面向连接** service in Chinese).

### Explanation

1. **Analogy to Phone Calls**:
    * **Pick up/Dial (Setup)**: Just as you must dial a number and wait for the other party to answer before speaking, a connection-oriented service requires a specific phase to establish a logical path between the sender and receiver before any data is transferred. In networking terms, this is often called a "handshake" (e.g., the TCP three-way handshake).
    * **Talk (Data Transfer)**: Once the connection is established, data flows sequentially and reliably between the two parties, much like a conversation.
    * **Hang up (Teardown)**: After the conversation ends, the line is disconnected. Similarly, a connection-oriented service requires a formal termination phase to release resources and close the connection.

2. **Key Characteristics**:
    * **Setup Phase**: A connection must be established before data transmission.
    * **Reliability**: Data usually arrives in order and without errors (guaranteed delivery).
    * **Stateful**: The network maintains the state of the connection during the session.
    * **Example**: The most common example in the Internet protocol suite is **TCP** (Transmission Control Protocol).

3. **Contrast**:
    * This is opposite to a **Connectionless** service (like sending a letter or using UDP), where each packet is sent independently without prior setup, and there is no guarantee of order or delivery.

References:

* [Transmission Control Protocol (TCP) - Wikipedia](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)
* [Connection-oriented communication - Wikipedia](https://en.wikipedia.org/wiki/Connection-oriented_communication)
