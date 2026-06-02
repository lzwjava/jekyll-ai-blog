---
audio: false
generated: true
image: false
lang: en
layout: post
title: RMON Enables Row Creation Deletion
translated: false
type: note
---

Question: Without modifying or violating the SNMPv1 management framework, what operations does the RMON specification provide?

Answer:

The correct answer is **C: Row creation and row deletion operations**.

### Explanation:
- **SNMPv1 Limitations**: The original SNMPv1 framework (defined in RFC 1157) has significant limitations regarding table manipulation. While it supports `GET`, `GETNEXT`, `SET`, and `TRAP`, it lacks a standardized, atomic mechanism for creating new rows in a table or deleting existing rows. The `SET` operation can modify individual cells, but ensuring the integrity of a whole row (e.g., creating all necessary columns simultaneously) is not natively supported in a robust way.
- **RMON Solution**: The Remote Monitoring (RMON) specification (originally RFC 1271, later RFC 2819) was designed to work within the existing SNMPv1 framework without requiring changes to the core protocol. To overcome the table manipulation limitation, RMON introduced a set of **textual conventions** and **procedural rules**.
- **Row Status**: A key part of this solution is the concept of "Row Status" (often using an integer column to control the state of a row, such as `createRequest`, `active`, `destroy`, etc.). This allows a management station to logically **add (create)** and **delete** rows in RMON tables (like the `etherStatsTable`) using standard SNMP `SET` operations on specific control columns, adhering to the defined procedural rules.
- **Why other options are incorrect**:
    - **A**: Retrieving unknown objects is generally handled by `GETNEXT`, which is part of standard SNMPv1, not a specific addition by RMON for this purpose.
    - **B**: Retrieving table objects is done via `GETNEXT` in standard SNMPv1.
    - **D**: Setting or updating variable values is a fundamental `SET` operation in SNMPv1, not a new capability provided specifically by RMON to fix a framework gap.

Therefore, RMON specifically fills the gap for **row creation and deletion** (Option C).

References:

- [RFC 2819: Remote Network Monitoring Management Information Base](https://datatracker.ietf.org/doc/html/rfc2819)
- [RFC 1157: Simple Network Management Protocol (SNMP)](https://datatracker.ietf.org/doc/html/rfc1157)
