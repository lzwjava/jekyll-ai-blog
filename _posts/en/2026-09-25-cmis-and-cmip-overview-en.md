---
audio: false
generated: true
image: false
lang: en
layout: post
title: CMIS and CMIP Overview
translated: false
type: note
---

**Question:** What are CMIS and CMIP in networking, and how do they relate to each other?

**Answer:**

CMIS and CMIP are a pair of closely related OSI network management standards — CMIS defines the *what* (the service interface), and CMIP defines the *how* (the protocol that implements it).

---

### CMIS — Common Management Information Service

CMIS is the service interface specified in ITU-T Recommendation X.710 / ISO/IEC 9595, employed by OSI network elements for network management. It defines the service interface that is implemented by CMIP (X.711), and is part of the Open Systems Interconnection (OSI) body of international network standards.

CMIS defines a message set used by peer processes to exchange information and commands for the purpose of network management. In concept, it is similar to SNMP, but more powerful — and hence more complex.

The services CMIS provides (through what's called the **CMISE** element) are:


- **M-CREATE** – Create an instance of a managed object
- **M-DELETE** – Delete an instance of a managed object
- **M-GET** – Request managed object attributes (for one or a set of objects)
- **M-CANCEL-GET** – Cancel an outstanding GET request
- **M-SET** – Set managed object attributes
- **M-ACTION** – Request an action to be performed on a managed object
- **M-EVENT-REPORT** – Send events occurring on managed objects


---

### CMIP — Common Management Information Protocol

CMIP is the OSI-specified network management protocol, defined in ITU-T Recommendation X.711 / ISO/IEC 9596-1. It provides an implementation for the services defined by CMIS, allowing communication between network management applications and management agents. CMIP models management information in terms of managed objects and allows both modification and performing actions on them. Managed objects are described using GDMO (Guidelines for the Definition of Managed Objects) and can be identified by a Distinguished Name (DN) from X.500.

CMIP also provides good security — supporting authorization, access control, and security logs — as well as flexible reporting of unusual network conditions.

**Implementation stack:** CMIP is implemented in association with the ACSE and ROSE protocols, both Layer 7 OSI (Application Layer) protocols. ACSE manages associations between management applications (i.e., connections between CMIP agents), while ROSE is employed for all data exchange interactions.

---

### CMIS vs CMIP — How They Relate

Think of it like this:

| | CMIS | CMIP |
|---|---|---|
| **Role** | Service definition (the API) | Protocol implementation (the wire format) |
| **Standard** | ITU-T X.710 / ISO 9595 | ITU-T X.711 / ISO 9596-1 |
| **Defines** | *What* operations are available | *How* those operations are transmitted |
| **Layer** | Application Layer (interface) | Application Layer (protocol) |

> Note: the term CMIP is sometimes used erroneously when CMIS is intended.

---

### CMIS/CMIP vs SNMP

CMIP's functionality is higher and more complex than SNMP in both management operations and managed information. GDMO (used by CMIP) is also more complex than SMI (used by SNMP).

CMIS/CMIP is most often used in telecommunications applications; in other areas, SNMP has become more popular.

---

**References:**
- [CMIS – Wikipedia](https://en.wikipedia.org/wiki/Common_Management_Information_Service)
- [CMIP – Wikipedia](https://en.wikipedia.org/wiki/Common_Management_Information_Protocol)
- [RFC 1189 – CMOT and CMIP (IETF)](https://www.rfc-editor.org/rfc/rfc1189.html)
- [CMIS – FOLDOC](https://foldoc.org/CMIS)
