---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI50 Dual 8-Pin PCIe Power Connectors
translated: false
type: note
---

Question: On the AMD Instinct MI50, what are the two power connector ports, and are the two 8-pin connectors the same type or different?

Answer:

The MI50 (Vega 20, 7nm, passive dual-slot card, 300W TDP) uses **two identical 8-pin PCIe-style power connectors** — not a 6+8 combo, not one CPU/EPS + one PCIe. Multiple retail listings confirm this directly: its maximum power draw of 300W comes from 2x 8-pin power connections, and the servershop24 SKU spec explicitly lists it as "300W / 2x8P-PCIe".

So to answer directly: **yes, the two 8-pin ports are the same type** — both are standard 8-pin PCIe (6+2 pin) connectors, same as what you'd plug into a normal gaming GPU. They're not keyed differently, and you don't need to worry about which cable goes into which port — either PCIe 8-pin cable from your PSU works in either connector, same wiring (12V rails + sense pins), same current rating (~150W per connector spec, 300W combined).

**Caveat on older reporting**: one 2018 Tom's Hardware article claimed a 6-pin + 8-pin combo relies on a combination of a 6-pin and 8-pin PCIe power connectors — this appears to be an early/incorrect report at launch time; every actual hardware listing and spec sheet since (technical.city, itcreations, servershop24) confirms 2x 8-pin, not 6+8. Trust the hardware listings over the launch-day article.

**One real-world nuance if you're building a rig**: some OEM server chassis (HPE ProLiant) ship the MI50 with a proprietary power harness — an "8-pin to 2x 8-pin (PCIe)" cable kit — meaning a single 8-pin from the server backplane splits into the two 8-pin GPU inputs. If you're pulling an MI50 out of an HPE server chassis for a DIY build (which is common since these show up cheap secondhand from decommissioned Radeon Instinct/MI50 clusters), you'll need standard dual PCIe 8-pin cables from your PSU, not the HPE proprietary splitter — that splitter is chassis-specific and won't map correctly to a normal ATX PSU's rail layout.

Practical check for your rig: if you're running this alongside your RTX 4070 workstation or building a multi-GPU inference box, just run two separate PCIe 8-pin cables straight from PSU to card (avoid daisy-chaining off a single PSU cable with two connectors — at 300W combined draw you want two separate rails/cables where possible to stay within each cable's ~150W safe margin).

References:

- [AMD Radeon Instinct MI50 - technical.city](https://technical.city/en/video/Radeon-Instinct-MI50)
- [AMD Radeon Instinct MI50 GPU - itcreations.com](https://www.itcreations.com/amd-gpu/amd-radeon-instinct-mi50-gpu)
- [AMD RADEON INSTINCT MI50 GPU - Servershop24](https://www.servershop24.de/en/amd-radeon-instinct-mi50-gpu/a-133803/)
- [PCIe 8-pin vs EPS-12V 8-pin power connections - Exxact](https://support.exxactcorp.com/hc/en-us/articles/20180443940119-PCIe-8-pin-vs-EPS-12V-8-pin-power-connections)
