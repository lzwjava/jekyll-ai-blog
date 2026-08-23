---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4090 5090 Failure Rates Scams
translated: false
type: note
---

**Question:** What are the defect/failure rates for RTX 4090 and 5090 cards, and what's the situation with broken cards being sold on eBay or Xianyu/Goofish?

**Answer:**

---

## RTX 4090 — Failure Rates

The 4090 launched with what became known as "Cablegate" — the 12VHPWR connector melting issue. The actual numbers:

- Based on information from NVIDIA partners and cable suppliers, the 4090 connector failure rate was estimated at around **0.05–0.1%**.
- A broader analysis of ~193,000 shipped cards found about 260 verified failures — roughly **0.13%** overall. The top failure type (65% of cases) was the 16-pin power connector not being fully seated.
- Separately, a Philippine retailer's 4-year RMA data showed GPU failure rates varied heavily by brand — **Gigabyte at 5%, MSI at 1.5%**.
- A Swiss retailer (Digitec Galaxus) published 24-month data showing brand defect rates, with the worst being **Sapphire at 2.5%**, followed by ASRock (2.1%), XFX (2%), Gigabyte (1.9%), EVGA and Zotac (1.8%).

Beyond the connector, there's a physical damage problem specific to the 4090's sheer size and weight:

- Repair technician NorthwestRepair flagged a wave of 4090s arriving with **ripped PCB pads around the GPU socket**, caused by shipping damage or cards installed without GPU support brackets — potentially irreparable damage.
- Another repair channel, NorthridgeFix, received **19 RTX 4090s from a single customer**, almost all with **cracked PCBs** near the PCIe bracket — a trend linked to increasingly heavy GPUs.

---

## RTX 5090 — Worse Out of the Gate

The 5090 launched with more serious systemic problems:

- NVIDIA confirmed that **less than 0.5%** of RTX 5090/5090D and 5070 Ti GPUs shipped with **one fewer ROP (Render Output Unit) than specified**, causing about a 4% performance drop.
- Early failures were documented across multiple AIB brands — Colorful, Manli, Gigabyte, and ASUS — with cards simply not appearing in Windows Device Manager, BIOS, or NVIDIA drivers at all. Hardware analyst Der8auer concluded this pointed to **a fundamental architecture or driver compatibility issue** rather than isolated manufacturing defects, tied to rushed PCIe Gen 5 implementation.
- The 5090 also repeated the connector melting problem. MSI's own-brand 16-pin cables (single connector) showed far fewer failures, while NVIDIA-supplied adapter cables were the main culprit.
- As recently as August 2026, a PNY RTX 5090 suffered a **capacitor explosion** near the 16-pin connector during video editing — producing smoke, a loud pop, and total display loss.

---

## The Secondary Market — eBay, Xianyu, Goofish

This is where it gets genuinely dangerous for buyers:

**Scam cards — shells with no silicon:**
- Scammers buy broken/stripped 4090s for around $200, then sell them as working cards. Repair channels have exposed boards with **no GPU die and no VRAM at all** — just a heatsink on a blank PCB.
- A popular scam involves removing the GPU core and memory entirely, then flipping those chips for profit or retrofitting them onto other PCBs. <br>In China specifically, **RTX 5090 dies and GDDR7 memory modules are being transplanted onto blower-style cards** compatible with AI servers — leaving hollowed-out retail shells that get resold through second-hand markets, often with no return option.
- The market for these AI-server modifications is huge in China. Leftover cooling and PCB components from the transplant process then get resold to other firms — and eventually reach unsuspecting buyers as apparently complete cards.

**Legitimate broken card market (for repair/parts):**
- Some retailers legitimately sell damaged RTX 5090s for as low as $1,760 — cards damaged during transport but with all components still on the PCB, intended only for repair professionals or recycling.
- Chinese vendors on Xianyu sell individual repair components, like NVIDIA PCIe connectors, letting people attempt board-level fixes on expensive cards rather than scrapping them entirely.

**The fake card problem:**
- Scams have become sophisticated enough that a card sent in for repair turned out to be a **fake with a laser-engraved GPU die** made to look real — the core and VRAM were convincing replicas of no functional value.

---

## TL;DR Summary

| Card | Connector Failure | Overall Defect | Secondary Market Risk |
|---|---|---|---|
| RTX 4090 | ~0.05–0.13% (Cablegate) | 1.5–5% by brand | High — hollowed shells common |
| RTX 5090 | Ongoing (same issue) | ~0.5%+ ROP defect + bricking | Very high — scams + AI part-stripping |

If buying used: **always demand a video of the card booting in a system before payment**, and be extremely skeptical of prices more than ~15–20% below market.

---

**References:**
- [ExpertBeacon — RTX 4090 Failure Rate Analysis](https://expertbeacon.com/what-is-the-failure-rate-of-rtx-4090/)
- [Tom's Hardware — GPU Failure Rates by Brand](https://www.tomshardware.com/news/retailer-shares-failure-rates-for-gpus-motherboards-ssds-more)
- [Tweaktown — Swiss Retailer GPU Defect Data](https://www.tweaktown.com/news/93052/heres-look-at-gpu-failure-rates-and-warranty-claim-times-for-all-major-brands/index.html)
- [TechPowerUp — RTX 5090 Bricking Reports](https://www.techpowerup.com/332047/reports-of-bricked-nvidia-geforce-rtx-5090-and-rtx-5090d-surge)
- [VideoCardz — Scam RTX 5090 Cards in Repair Shops](https://videocardz.com/newz/scam-geforce-rtx-5090-cards-with-missing-gpu-and-memory-now-showing-up-in-repair-shops)
- [Tom's Hardware — Hollowed RTX 5090 Shipped to Customer](https://www.tomshardware.com/pc-components/gpus/retailer-ships-rtx-5090-with-missing-gpu-and-memory-chips-to-customer-defaced-gpu-took-over-a-year-to-ship)
- [TechRadar — Broken 4090s on Secondhand Markets](https://www.techradar.com/computing/gpu/broken-and-gpu-less-rtx-4090s-are-being-sold-secondhand-by-scammers)
- [Wccftech — RTX 5090 Connector Melting Tracker](https://wccftech.com/roundup/nvidia-rtx-5090-16-pin-connector-melting-issues-tracker/)