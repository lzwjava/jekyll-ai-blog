---
audio: false
generated: true
image: false
lang: en
layout: post
title: Layer 2 Switch Explained Simply
translated: false
type: note
---

Question: When we refer to "Layer 2 switch", does "Layer" mean the OSI layer, specifically one of the 7 layers in the OSI model?

Answer: 

**Yes**, when we say **Layer 2 switch**, the "Layer" refers directly to **Layer 2 of the OSI model**.

The OSI (Open Systems Interconnection) model has **7 layers**:

1. Physical  
2. **Data Link** ← **Layer 2**  
3. Network  
4. Transport  
5. Session  
6. Presentation  
7. Application  

A **Layer 2 switch** operates at the **Data Link layer** (Layer 2) of the OSI model.

### Main characteristics of a Layer 2 switch:
- Makes forwarding decisions based on **MAC addresses** (not IP addresses)
- Maintains a **MAC address table** (also called CAM table)
- Forwards Ethernet frames within the same broadcast domain (VLAN)
- Does **not** perform routing between different IP subnets
- Can support VLANs (802.1Q tagging) — still Layer 2
- Can do basic filtering / security based on MAC addresses
- Common forwarding modes: store-and-forward, cut-through, fragment-free

### Comparison for clarity:

| Device              | OSI Layer | Makes decisions based on | Can route between subnets? | Typical name today       |
|---------------------|-----------|---------------------------|-----------------------------|---------------------------|
| Hub                 | Layer 1   | Electrical signals        | No                          | (almost obsolete)         |
| **Switch**          | **Layer 2**   | **MAC addresses**         | **No**                      | **Layer 2 switch**        |
| Multilayer switch / Router | Layer 3   | IP addresses              | Yes                         | Layer 3 switch / Router   |

So in short:  
**Yes** — "Layer 2" in "Layer 2 switch" refers to **Layer 2 (Data Link layer)** of the classic **7-layer OSI model**.

References:  

- None required for this fundamental networking concept