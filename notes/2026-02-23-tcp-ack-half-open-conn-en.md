---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCP ACK and Half Open Connection
translated: false
type: note
---

Question: Computer A establishes a TCP connection with Computer B. Host A has 1024 bytes of application-layer data to send to Host B. Currently, the "Sequence Number" field in the TCP segment from Host A is 3A47087C (hexadecimal). If Host B has correctly received these 1024 bytes of data, which field in the TCP segment sent by Host B to Host A should be used to indicate this, and what value should it contain? During data transmission, Host A suddenly loses power and restarts quickly, but Host B still believes the TCP connection exists. What is this situation generally called? In this case, when Host B sends a TCP segment carrying data to Host A, which field in the TCP header does Host A use to notify Host B that the connection no longer exists?

Answer:

### 1. Acknowledgment Field and Value Calculation

When Host B successfully receives data from Host A, it must send an acknowledgment (ACK) to confirm receipt.

* **Field Name**: The field used in the TCP header to indicate the next expected byte is the **Acknowledgment Number** (often referred to as the Acknowledgement field).
* **Value Calculation**:
  * The initial Sequence Number sent by A is given as hexadecimal `3A47087C`.
  * The size of the data payload is $1024$ bytes.
  * In decimal, $1024 = 0x400$ (hexadecimal).
  * The Acknowledgment Number represents the sequence number of the *next* byte Host B expects to receive. Therefore, it is calculated as:
        $$ \text{Next Seq} = \text{Current Seq} + \text{Data Length} $$
        $$ \text{Next Seq} = 3A47087C_{16} + 400_{16} $$
  * Performing the hexadecimal addition:

        ```text
          3A47087C
        +      400
        ----------
          3A470C7C  <-- Wait, let me re-calculate carefully.
        ```

        Let's break down the addition:
        $7C_{16} + 00_{16} = 7C_{16}$
        $08_{16} + 04_{16} = 0C_{16}$? No, $1024$ is $0x400$.
        Let's align properly:
        `3A47087C`
        `00000400` (Since $1024 = 4 \times 256 = 0x400$)

        Addition:
        Last digit: $C + 0 = C$
        Second digit: $7 + 0 = 7$
        Third digit: $8 + 4 = 12$, which is $C$ in hex.
        Fourth digit: $0 + 0 = 0$ (plus any carry? No, $8+4=12 < 16$, so no carry).

        Wait, $1024$ bytes is $0x400$.
        $087C + 0400$:
        $C+0=C$
        $7+0=7$
        $8+4=12 (C)$
        $0+0=0$
        Result: $0C7C$.
        So the full number is `3A470C7C`.

        **Correction based on the provided reference answer**:
        The reference answer provided in your prompt states `3A470F7C`. Let's reverse engineer why.
        $3A470F7C - 3A47087C = 0F7C - 087C = 0700_{16}$.
        $0700_{16} = 7 \times 256 = 1792$ bytes.
        However, the problem explicitly states **1024 bytes**.
        $1024$ bytes in hex is definitely $0x400$.
        $087C + 0400 = 0C7C$.

        There appears to be a discrepancy between the standard calculation ($1024$ bytes $\rightarrow$ `3A470C7C`) and the provided reference answer (`3A470F7C`).
    * If the data was 1024 bytes: Answer is `3A470C7C`.
    * If the reference answer `3A470F7C` is strictly required by your exam system, it implies the data length considered was $1792$ bytes ($0x700$), or there is a typo in the question's byte count or the reference answer.

        **Standard Technical Answer**: Based strictly on the text "1024 bytes", the math is:
        $3A47087C + 0x400 = \mathbf{3A470C7C}$.

        *Self-Correction for Exam Context*: Since you provided a "Reference Answer" of `3A470F7C`, it is highly likely the original exam question intended a different data size (perhaps 1792 bytes) or contains a known error in the key. However, logically, for 1024 bytes, the value is `3A470C7C`. If you must match the provided key exactly for grading purposes despite the math, note the key says `3A470F7C`. But scientifically, `3A470C7C` is correct for 1024 bytes.

        *Let's re-read the hex math one more time to ensure no silly mistake.*
        Start: `...087C`
        Add 1024 (`0x400`):
        `08` (hex) is 8. `8 + 4 = 12` which is `C`.
        So `...0C7C`.
        Yes, `3A470C7C` is the mathematically correct answer for 1024 bytes.

        **Decision**: I will provide the mathematically correct derivation (`3A470C7C`) but acknowledge the reference answer provided in your prompt (`3A470F7C`) might be based on a specific context or error in the source material. For an exam explanation, understanding the *method* (Seq + Len) is usually more important than a potentially flawed key, but if the system is rigid, be aware of the discrepancy.

### 2. Connection State Issue

* **Problem Name**: When one side (Host A) crashes and reboots, losing all memory of the connection, while the other side (Host B) still believes the connection is active, this state is known as a **Half-Open Connection** (or sometimes a "dangling connection").
* **Mechanism**: Host B is unaware that Host A has restarted and lost the Transmission Control Block (TCB) associated with the connection.

### 3. Resetting the Connection

* **Scenario**: Host B sends a segment with data to Host A.
* **Host A's Reaction**: Since Host A rebooted, it does not recognize the incoming segment as part of an existing valid connection (it has no record of it).
* **Response Field**: Host A will respond with a TCP segment where the **RST (Reset)** flag in the TCP header is set to **1**.
* **Effect**: This signals to Host B that the connection is invalid and must be terminated immediately.

### Summary of Answers

1. **Field**: Acknowledgment Number (确认序号).
2. **Value**: `3A470C7C` (Calculated for 1024 bytes). *Note: Your provided reference key lists `3A470F7C`, which corresponds to 1792 bytes. Please verify the byte count in your specific exam source.*
3. **Problem Name**: Half-Open Connection (半开连接).
4. **Field to Notify**: RST flag (Reset bit).

References:

* [TCP Connection Establishment and Termination - GeeksforGeeks](https://www.geeksforgeeks.org/tcp-connection-termination/)
* [RFC 793: Transmission Control Protocol](https://datatracker.ietf.org/doc/html/rfc793)
