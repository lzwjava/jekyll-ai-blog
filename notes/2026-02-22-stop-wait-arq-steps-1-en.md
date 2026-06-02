---
audio: false
generated: true
image: false
lang: en
layout: post
title: Stop and Wait ARQ Process Steps
translated: false
type: note
---

Question: In the error control technology of data communication, Stop-and-Wait ARQ is one of the common methods for error detection and retransmission. The diagram below describes the process of using Stop-and-Wait ARQ when the sender and receiver transmit data. Please write out the content of items ① to ⑥ in the diagram based on the provided reference answer logic.

Answer:

Based on the reference answer provided and the standard mechanics of the Stop-and-Wait ARQ protocol (specifically a variant utilizing NAK - Negative Acknowledgment), here is the detailed deduction and explanation for items ① through ⑥:

**The Sequence of Events:**

1. **Context**: The sender has likely just sent `PKT1` and received an acknowledgment, so it is now attempting to send `PKT2`.
2. **Item ①: ACK**
    * **Logic**: Before sending new data (`PKT2`), the sender might be receiving a final acknowledgment for the previous packet (`PKT1`), or this represents the successful acknowledgment of a previous step allowing the sequence to continue. In the context of the reference answer starting with `ACK`, it implies the channel is clear or the previous transaction was successfully closed.
    * **Content**: **ACK** (Acknowledgment)

3. **Item ②: PKT2**
    * **Logic**: Upon receiving the ACK (or as the next step in the sequence), the sender transmits the second data packet.
    * **Content**: **PKT2** (Packet 2)

4. **Item ③: NAK**
    * **Logic**: The receiver gets `PKT2` but detects an error (e.g., via CRC check). Instead of staying silent (which would rely on a timeout), this specific protocol variation sends a **NAK** (Negative Acknowledgment) to immediately inform the sender that `PKT2` was corrupted and needs retransmission.
    * **Content**: **NAK** (Negative Acknowledgment)

5. **Item ④: PKT2**
    * **Logic**: Upon receiving the NAK, the sender immediately retransmits the corrupted packet. It does not move to the next sequence number yet; it must resend `PKT2`.
    * **Content**: **PKT2** (Retransmission of Packet 2)

6. **Item ⑤: ACK**
    * **Logic**: The receiver successfully receives the retransmitted `PKT2`. It verifies the integrity, accepts the data, and sends a positive acknowledgment.
    * **Content**: **ACK** (Acknowledgment for PKT2)

7. **Item ⑥: PKT3**
    * **Logic**: Now that `PKT2` is confirmed, the sender proceeds to send the next packet in the sequence.
    * **Content**: **PKT3** (Packet 3)

**Summary of the Flow:**

* Sender receives **ACK** (①) for previous data.
* Sender sends **PKT2** (②).
* Receiver detects error in PKT2 and sends **NAK** (③).
* Sender re-sends **PKT2** (④).
* Receiver accepts re-sent PKT2 and sends **ACK** (⑤).
* Sender sends next data **PKT3** (⑥).

This scenario highlights the efficiency of using NAKs in Stop-and-Wait ARQ, as it avoids waiting for a timeout period when an error is detected immediately at the receiver.

References:

* [Stop-and-Wait ARQ Protocol - GeeksforGeeks](https://www.geeksforgeeks.org/stop-and-wait-arq/)
* [Error Control: Flow Control & Error Control - Tutorialspoint](https://www.tutorialspoint.com/data_communication_computer_network/error_control.htm)
