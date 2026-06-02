---
audio: false
generated: true
image: false
lang: en
layout: post
title: Half Duplex Communication Explained
translated: false
type: note
---

Question: What is the term for a communication method where both parties can transmit information, but not simultaneously?

Answer: This type of communication is known as **Half-Duplex** (or **Two-Way Alternate**) communication.

---

### 📡 The Three Modes of Communication

To better understand where **Half-Duplex** fits, it helps to compare it with the other two primary modes:

| Mode | Directionality | Real-World Analogy |
| --- | --- | --- |
| **Simplex** | **One-way only.** One party is always the sender, the other is always the receiver. | A radio broadcast or a TV station. |
| **Half-Duplex** | **Two-way, but not at the same time.** Information can flow in both directions, but only one way at a time. | A **Walkie-Talkie**. You must wait for the other person to stop talking before you can speak. |
| **Full-Duplex** | **Two-way simultaneously.** Both parties can send and receive at the exact same time. | A **Telephone call** or a modern smartphone. |

---

### 🛠️ Technical Context

In networking, **Half-Duplex** was very common in early Ethernet setups that used a **Hub**. Since everyone shared the same wire, if two computers tried to "talk" at once, a **collision** would occur, and the data would be corrupted.

Modern networks (using Switches and Fiber Optics) almost exclusively use **Full-Duplex**, which allows for much higher speeds and zero collisions.

> **Key Rule:** In Half-Duplex, the entire bandwidth of the channel is used by whichever party is currently sending.

---

Would you like me to explain how Ethernet uses **CSMA/CD** to manage these "turns" in a Half-Duplex environment?
