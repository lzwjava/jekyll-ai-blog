---
audio: false
generated: true
image: false
lang: en
layout: post
title: SNMP MIB-2 Core Operations
translated: false
type: note
---

Question: What operations can an SNMP entity perform on objects in MIB-2?

Answer: 

The correct answer is **D: Get, Set, Trap**.

### Explanation:
In the Simple Network Management Protocol (SNMP), an SNMP entity (typically a manager or an agent) interacts with managed objects defined in the Management Information Base version 2 (MIB-2). The fundamental operations defined in SNMP for interacting with these objects are:

1.  **Get**: Used by the SNMP manager to retrieve the value of a specific object instance from the agent.
2.  **Set**: Used by the SNMP manager to modify or set the value of a specific object instance on the agent.
3.  **Trap**: An asynchronous notification sent by the SNMP agent to the manager to report significant events or errors (e.g., link down, authentication failure). While technically a PDU (Protocol Data Unit) type initiated by the agent rather than an operation "performed on" an object in the same way Get/Set are, in the context of SNMP operations involving MIB objects and communication flows, it is grouped as one of the primary actions.

**Why the other options are incorrect:**
*   **GetNext**: This is indeed a valid SNMP operation used to retrieve the next object instance in the MIB tree (essential for walking tables). However, looking at the specific grouping in standard exam questions of this type, the trio **Get, Set, and Trap** is often cited as the core set of functional capabilities (Read, Write, Notify). 
    *   Option A includes Trap and GetNext but misses **Get**, which is the most basic read operation.
    *   Option C includes Trap and GetNext but misses **Set**.
    *   Option B includes Get, Set, and GetNext but misses **Trap**.
    
    *Note: In strict technical terms, SNMPv1 defines five PDUs: GetRequest, GetNextRequest, SetRequest, GetResponse, and Trap. SNMPv2c adds GetBulkRequest and InformRequest. However, based on the provided "Detailed Explanation" in your prompt ("SNMP实体可以对MIB-2中的对象执行的操作有：Get,Set,Trap"), the specific curriculum or exam board this question comes from categorizes the primary operations as Get, Set, and Trap, likely treating GetNext as a variant of Get or focusing on the distinct functional categories of Retrieval, Modification, and Notification.*

Given the explicit explanation provided in your source material confirms the set is **Get, Set, Trap**, Option D is the intended correct answer.

References: