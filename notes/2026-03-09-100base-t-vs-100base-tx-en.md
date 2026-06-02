---
audio: false
generated: true
image: false
lang: en
layout: post
title: 100BASE-T vs 100BASE-TX Explained
translated: false
type: note
---

Question: What is the difference between 100BASE-TX and 100BASE-T?Question: What is the difference between 100BASE-T and 100BASE-TX?

Answer:

## The Short Answer

**100BASE-T** and **100BASE-TX** are basically the same thing in most practical usage. Technically, 100BASE-T is the **umbrella/generic term** that encompasses all Fast Ethernet copper standards, while 100BASE-TX is one **specific subset** under that umbrella.

---

## 100BASE-T — The Family Name

**100BASE-T** is a technical term that defines the **family** of physical layer (PHY) standards supporting 100 Mbps networks over twisted pair cables. Under the IEEE 802.3u standard released in 1995, it defines three specific 100 Mbps Ethernet variants: **100BASE-TX**, **100BASE-T4**, and **100BASE-T2**.

So think of **100BASE-T** as a **category**, not a single standard.

---

## 100BASE-TX — The Specific Standard

**100BASE-TX** is the **predominant and most popular** form of Fast Ethernet. It runs over **two pairs of wire** inside a Category 5 or above cable, with a maximum cable distance of **100 metres** between nodes. One pair is used for each direction, providing **full-duplex** operation at 100 Mbps in each direction.

The "TX" (sometimes referred to simply as "T") means it's a Cat5 UTP straight-through cable using **two of the four available pairs**, supporting speeds up to 100 Mbps.

---

## What About the Other Members of the 100BASE-T Family?

| Standard | Wire Pairs Used | Cable Required | Notes |
|---|---|---|---|
| **100BASE-TX** | 2 pairs | Cat5 or above | Most common; used everywhere |
| **100BASE-T4** | 4 pairs | Cat3 or above | Older; designed for lower-quality cable |
| **100BASE-T2** | 2 pairs | Cat3 or above | Rare; largely unused |
| **100BASE-FX** | N/A (fiber) | Multimode fiber | Not copper; uses light signals |

The T4 variant uses **all four available pairs** in a Cat5 UTP cable and also supports speeds up to 100 Mbps with the same 100-metre maximum length.

---

## Key Takeaway

The term **100BASE-T** might sometimes be used in a broader sense or refer to earlier/less specific implementations of Fast Ethernet, while **100BASE-TX** precisely denotes the standard requiring **Category 5 cabling** for 100 Mbps Ethernet over two twisted pairs. In many practical discussions, 100BASE-T and 100BASE-TX are used **interchangeably** to refer to the same thing.

In short:

- **100BASE-T** = the whole Fast Ethernet family on twisted pair
- **100BASE-TX** = the specific, most widely used member of that family

References:

- [Fast Ethernet – Wikipedia](https://en.wikipedia.org/wiki/Fast_Ethernet)
- [100BaseTX: Implementation and Troubleshooting – Network Encyclopedia](https://networkencyclopedia.com/100basetx/)
- [100Base-TX/T4/FX – Firewall.cx](https://www.firewall.cx/networking/network-cabling/network-cabling-100basetx.html)
- [Difference between 100BaseT & 100BaseTX – Cisco Community](https://community.cisco.com/t5/other-network-architecture-subjects/difference-between-100baset-100basetx/td-p/240154)
