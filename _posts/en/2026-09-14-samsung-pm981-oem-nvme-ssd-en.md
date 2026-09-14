---
audio: false
generated: true
image: false
lang: en
layout: post
title: Samsung PM981 OEM NVMe SSD
translated: false
type: note
---

**Question:** What is the Samsung MZVLB512HAJQ-000L7 drive?

**Answer:**

The **Samsung MZVLB512HAJQ-000L7** is an OEM enterprise/laptop NVMe SSD belonging to the **Samsung PM981 (Polaris)** series. The `-000L7` suffix is a variant code indicating it was supplied to a specific OEM partner (commonly found in Lenovo ThinkPad/ThinkCentre systems).

Here is a full breakdown:

**Identity**

- **Model series:** Samsung PM981
- **Codename:** Polaris
- **Type:** OEM internal SSD (not retail)
- **OEM targets:** Lenovo, Dell, HP, and other system builders

**Physical**

- **Form factor:** M.2 2280 (22 mm wide × 80 mm long)
- **Interface:** PCIe 3.0 x4, NVMe 1.2
- **Dimensions:** ~22 × 80 × 2.38 mm
- **Weight:** ~0.32 oz (~9 g)

**Storage**

- **Capacity:** 512 GB
- **NAND type:** 3D V-NAND (TLC/MLC depending on vendor source)
- **Controller:** Samsung Phoenix (in-house)
- **DRAM cache:** Yes (on-board LPDDR4)

**Performance** (per official Samsung datasheet)

- **Sequential Read:** up to 3,200 MB/s; **Sequential Write:** up to 2,400 MB/s
- **Random Read:** up to 380K IOPS; **Random Write:** up to 440K IOPS (4K blocks, 4 lanes)

**Security**

- **Encryption:** 256-bit AES-XTS hardware encryption, TCG Opal 2.0, Self-Encrypting Drive (SED)

**Reliability**

- **MTBF:** 1,500,000 hours; **Uncorrectable bit error rate:** 1 per 10¹⁵ bits

**Notes**

- As an OEM product, it ships without a retail box, consumer warranty, or official spec sheet. Samsung Magician software does not support this drive.
- It is essentially the OEM precursor to the consumer **Samsung 970 EVO**, offering near-identical performance at a lower OEM price point.
- The PM981 was later succeeded by the **PM981a**, which uses newer 92-layer V-NAND and slightly better efficiency.

---

**References:**

- [Samsung PM981 SSD Review — Tom's Hardware](https://www.tomshardware.com/reviews/samsung-pm981-980-nvme-ssd,5323.html)
- [PM981 Datasheet v1.1 — compuram.biz](https://www.compuram.biz/documents/datasheet/Samsung_PM981_Rev_1_1.pdf)
- [Samsung PM981 MZVLB512HAJQ — SHI Overview](https://www.shi.com/product/36935413/Samsung-PM981-MZVLB512HAJQ)
- [MZVLB512HAJQ-000L7 — HardDiskDirect](https://harddiskdirect.com/mzvlb512hajq-000l7-samsung-solid-state-drive.html)
