---
audio: false
generated: true
image: false
lang: en
layout: post
title: Redundancy Fixes Data Transmission Errors
translated: false
type: note
---

Question: Briefly describe the basic principle of error-correcting coding.

Answer: 

The basic principle of **error-correcting coding** (also known as channel coding) is to enhance the reliability of data transmission over noisy channels by introducing controlled redundancy. The process involves the following key steps:

1.  **Addition of Redundancy**: At the transmitter, specific redundant bits (check bits) are added to the original data bits according to a predefined mathematical rule or algorithm. These redundant bits do not carry new information but establish a specific logical relationship or constraint with the data bits.
2.  **Transmission**: The combined sequence of original data bits and redundant bits is transmitted through the communication channel.
3.  **Detection and Correction**: At the receiver, the incoming bit stream is checked against the same predefined rules.
    *   **Error Detection**: The receiver verifies if the relationship between the data bits and the redundant bits holds true. If the relationship is violated, it indicates that errors have occurred during transmission.
    *   **Error Correction**: In more advanced codes (Forward Error Correction - FEC), the specific pattern of the violation allows the receiver not only to detect the presence of errors but also to locate and correct them automatically without needing a retransmission.

In essence, error coding trades transmission efficiency (by sending extra bits) for increased reliability, allowing the system to detect and often correct errors caused by noise, interference, or signal attenuation.

References: