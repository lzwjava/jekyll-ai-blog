---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fiber Optic Connector Type Guide
translated: false
type: note
---

Question: What does LC-LC, SC-SC, etc. mean for fiber optic cables?

Answer:

**LC-LC**, **SC-SC**, and similar notations describe **fiber optic patch cables** (also called jumper cables) by specifying the **connector types** on each end.

- **LC-LC** means the cable has an **LC connector** on both ends.
- **SC-SC** means the cable has an **SC connector** on both ends.
- Other common examples include **LC-SC** (LC on one end, SC on the other), **ST-ST**, **FC-FC**, **MTP-MTP**, and so on.

These are the most widely used types of **duplex** (two-fiber) patch cords in networking, data centers, telecom, and fiber-to-the-home installations.

### What do LC and SC stand for?
- **LC** → **Lucent Connector** (also called Little Connector or Local Connector)
  - Uses a small **1.25 mm** ceramic ferrule.
  - Very compact size (about half the footprint of SC).
  - Uses a small latch clip to lock in place (similar to an RJ45 clip).
  - Dominant in modern high-density environments like data centers, SFP/SFP+/QSFP transceivers, and high-speed switches/routers.

- **SC** → **Subscriber Connector** (also called Square Connector or Standard Connector)
  - Uses a larger **2.5 mm** ceramic ferrule.
  - Square-shaped body with a push-pull mechanism and a locking tab.
  - Very common in older telecom equipment, PON networks (GPON/EPON), cable TV, and many enterprise installations from the 1990s–2010s.

### Quick comparison of LC vs SC

| Feature              | LC Connector                  | SC Connector                  |
|----------------------|-------------------------------|-------------------------------|
| Ferrule diameter     | 1.25 mm                       | 2.5 mm                        |
| Size / footprint     | Small / high-density          | Larger                        |
| Latching mechanism   | Small latch clip              | Push-pull with tab            |
| Typical use today    | Data centers, 10G/25G/40G/100G+ | Telecom, PON, older equipment |
| Density in panels    | Higher (more ports per space) | Lower                         |
| Insertion / durability | Good, but smaller latch       | Very robust, easy to handle   |

Both LC and SC provide excellent optical performance (low insertion loss and high return loss) and can be used with **single-mode** or **multi-mode** fiber.

### Other common notations you might see
- **LC-SC** → Hybrid cable (one end LC, one end SC) — often used when connecting new equipment to older infrastructure.
- **LC-LC Duplex** → Specifies two fibers (most common patch cable style).
- **LC/UPC-LC/UPC** → Adds polish type (UPC = Ultra Physical Contact, most common; APC = Angled Physical Contact for lower reflection in some single-mode applications).

In short: **LC-LC** = both ends are small modern LC connectors, **SC-SC** = both ends are larger classic SC connectors.

References:

- [Fiber Optic Connector Types Explained | FiberCablesDirect](https://fibercablesdirect.com/content/23-fiber-optic-connector-types-explained)
- [LC vs SC Connectors: Which to Choose? - VCELINK](https://www.vcelink.com/blogs/focus/lc-vs-sc-connectors)
- [Comparing SC and LC Fibre Optic Connectors | iTel Networks](https://itel.com/blog/comparing-sc-and-lc-fibre-optic-connectors)
- [Fiber-optic connectors: SC vs. LC | Arrow.com](https://www.arrow.com/en/research-and-events/articles/fiber-optic-connectors-sc-vs-lc)
