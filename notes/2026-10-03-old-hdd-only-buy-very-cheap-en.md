---
audio: false
generated: true
image: false
lang: en
layout: post
title: Old HDD, only buy very cheap
translated: false
type: note
---

Question: How good is this 500GB HGST Z5K500 2.5" 5400 RPM SATA HDD?

Answer: **It’s a usable old laptop HDD, but only worth buying very cheaply.**

* **Model:** HGST Z5K500, 500GB, 2.5", SATA, 5400 RPM, 16MB cache
* **Interface:** SATA, so it should work with ordinary SATA laptop/desktop adapters.
* **Performance:** roughly **80–120 MB/s sequential** when healthy; random I/O will be very slow compared with any SSD.
* **Capacity:** 500GB is useful for bulk storage, Linux testing, ISO/model datasets, logs, etc.
* **Power:** low-power 2.5" mechanical drive, suitable for laptops and small test machines.
* **Age:** This is an **old-generation HGST/Hitachi drive**. "Almost new appearance" doesn't mean the magnetic media or bearings have little operating time.

### The important part: check SMART

Don't buy it just because the seller says "functional." Ask for a screenshot/output of:

```bash
smartctl -a /dev/sdX
```

I'd particularly check:

```text
SMART overall-health
Reallocated_Sector_Ct
Current_Pending_Sector
Offline_Uncorrectable
Power_On_Hours
UDMA_CRC_Error_Count
```

For a used HDD, ideally:

```text
Reallocated_Sector_Ct = 0
Current_Pending_Sector = 0
Offline_Uncorrectable = 0
```

And run a long test if you actually care about the data:

```bash
sudo smartctl -t long /dev/sdX
# wait for completion
sudo smartctl -a /dev/sdX
```

### Price

For your kind of use, I'd roughly value it like:

|      Price | My take                                           |
| ---------: | ------------------------------------------------- |
| **¥20–30** | Very cheap, worth grabbing as a test/storage disk |
| **¥30–50** | Reasonable if SMART is excellent                  |
| **¥50–70** | Only if genuinely low-hours / excellent SMART     |
|   **¥80+** | I wouldn't buy it                                 |
|  **¥100+** | Get a used SATA SSD instead                       |

For **GPU/LLM lab machines**, I wouldn't use this as the OS disk. A cheap 240/480GB SATA SSD will feel dramatically faster. This HDD makes more sense as a **secondary bulk/test disk**.

If you give me the **Xianyu asking price**, I can tell you whether this particular listing is worth buying.
