---
audio: false
generated: true
image: false
lang: en
layout: post
title: Type A Network Service Basics
translated: false
type: note
---

Question: According to user requirements and the nature of errors, network services are divided into three types. Which of the following describes Type A network service?

Answer:

**Type A Network Service** is characterized by having **acceptable residual error rates** and **acceptable failure notification rates**.

In the context of network service classifications (often associated with the OSI model and transport layer services):

- **Type A**: The underlying network provides reliable service with low error rates. Therefore, the transport layer does not need to implement extensive error recovery mechanisms. Both the residual error rate and the failure notification rate are considered acceptable for the user's needs.
- **Type B**: The network has an acceptable residual error rate but an unacceptable failure notification rate (e.g., failures are not signaled properly).
- **Type C**: The network has an unacceptable residual error rate, requiring the transport layer to handle significant error detection and recovery.

Since Type A represents the highest quality of underlying service where both metrics meet user requirements, the correct description is that it possesses acceptable rates for both residuals errors and failure notifications.

**Correct Option:** C

References:

- [OSI Transport Layer Services Overview](https://www.geeksforgeeks.org/types-of-services-in-transport-layer/)
