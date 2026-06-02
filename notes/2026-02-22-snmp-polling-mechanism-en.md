---
audio: false
generated: true
image: false
lang: en
layout: post
title: SNMP Polling Mechanism Explained
translated: false
type: note
---

Question: A monitor sends a request to an agent asking for specific information values; the agent responds by retrieving the requested values from its Management Information Base (MIB) and returning them to the monitor. What is this communication mechanism called?

Answer:

The correct answer is **A: Polling**.

### Explanation

In network management architectures (such as SNMP - Simple Network Management Protocol), there are two primary methods for a manager (monitor) to obtain data from an agent:

1. **Polling (轮询)**: This is the mechanism described in your question. The manager actively initiates the communication by sending a request to the agent asking for specific data. The agent then retrieves this data from its local Management Information Base (MIB) and sends it back to the manager. This is a "pull" model where the manager controls the timing and frequency of data collection.
2. **Event Reporting / Trapping (事件报告)**: In this mechanism, the agent initiates the communication. When a specific event or threshold is crossed, the agent spontaneously sends a message (Trap or Inform) to the manager without waiting for a request. This is a "push" model.

**Why the other options are incorrect:**

* **B (Event Report)**: This refers to the agent initiating the message upon an event, not responding to a specific query for values.
* **C (Request)**: While the manager does send a "request," the term "Request" alone describes the message type or action, not the overall *communication mechanism* or strategy. The strategy of periodically requesting data is specifically called "Polling."
* **D (Response)**: Similar to "Request," this describes the reply message, not the systemic approach of data collection.

Therefore, the specific communication mechanism where the monitor proactively queries the agent for data is known as **Polling**.

References:

* [SNMP Architecture Overview](https://www.snmp.com/what-is-snmp/)
