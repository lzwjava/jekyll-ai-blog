---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI B760M storage upgrade options
translated: false
type: note
---

**Question:** For the workstation described (MSI MAG B760M Mortar WiFi, currently with 1TB NVMe SSD + 2TB HDD), what are the best options to upgrade storage beyond 2TB?

**Answer:**

Your current storage situation:

- **1TB Samsung 980** (PCIe 3.0 x4 NVMe, M.2 slot 1)
- **2TB WD Blue HDD** (SATA)
- Total: ~3TB raw

---

## What Slots Are Available on MSI MAG B760M Mortar WiFi

This mATX board has:

| Slot | Type | Status |
|------|------|--------|
| M.2_1 (Key-M) | PCIe 5.0 x4 / PCIe 4.0 x4, NVMe | Likely occupied by Samsung 980 |
| M.2_2 (Key-M) | PCIe 4.0 x4, NVMe | **Free** |
| M.2_3 (Key-M) | PCIe 4.0 x4 / SATA | **Free** |
| SATA ports | 6× SATA 6Gb/s | 1 used by HDD, 5 free |

You have **two free M.2 slots** and **5 free SATA ports**. Plenty of room.

---

## Upgrade Options

### Option 1: Add another NVMe M.2 SSD (Best for performance)

Drop a 2TB or 4TB Gen4 NVMe into M.2_2.

**Recommended:**

| Drive | Capacity | Speed | Price (CNY) |
|-------|----------|-------|-------------|
| Samsung 990 Pro | 2TB | 7,450/6,900 MB/s | ~799 |
| WD Black SN850X | 2TB | 7,300/6,600 MB/s | ~749 |
| Crucial T500 | 2TB | 7,400/7,000 MB/s | ~599 |
| Crucial T500 | 4TB | 7,400/6,500 MB/s | ~999 |

For ML/AI workloads (datasets, checkpoints), **4TB Gen4** in M.2_2 is the highest-leverage single upgrade.

### Option 2: Add more SATA HDDs (Best for bulk cold storage)

You have 5 free SATA ports and the Aigo case likely fits 2–3 x 3.5" drives. You already have SATA cables.

| Drive | Capacity | Price (CNY) |
|-------|----------|-------------|
| WD Blue 4TB | 4TB | ~499 |
| Seagate Barracuda 4TB | 4TB | ~459 |
| WD Red Plus 4TB (NAS-grade) | 4TB | ~599 |

Good for storing training datasets, model weights, video, backups. Not for active swap/cache.

### Option 3: Replace the 1TB Samsung 980 with a larger Gen4 drive

The 980 is Gen3 and in M.2_1 which supports Gen5/Gen4. Swapping it for a 4TB Gen4 gives you the best slot with the fastest drive. Then repurpose the 980 as secondary or sell it.

---

## Recommended Path for Your Use Case

Given you run ML training (RTX 4070, datasets, checkpoints):

1. **Immediate**: Add **Crucial T500 4TB PCIe 4.0** into M.2_2 (~999 CNY). Fast enough for dataset reads during training, large enough for model weights and checkpoints.
2. **Later**: Add a **4TB WD Blue HDD** into a free SATA port (~499 CNY) for cold archive storage — raw datasets, old checkpoints, backups.

Total cost to go from ~3TB → ~11TB: under 1,500 CNY. No new cables needed for M.2, and you already have SATA cables.

---

## One Thing to Check

Verify the Aigo Yueguangbaohe Jing Mini case physically fits a second 3.5" HDD — mini cases sometimes only have 1–2 HDD bays. If space is tight, prioritize the M.2 SSD upgrade since it's tool-less and takes zero case space.
