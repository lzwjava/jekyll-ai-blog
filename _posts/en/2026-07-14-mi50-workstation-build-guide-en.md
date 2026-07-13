---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI50 Workstation Build Guide
translated: false
type: note
---

## AMD MI50 Workstation Configuration

### Important Note on MI50 Availability

**AMD Radeon Instinct MI50** is a data center compute accelerator launched in 2018, based on 7nm Vega 20 architecture with 3840 stream processors and HBM2 memory. It is **not widely available as a new product on JD.com** — most units on the market are second-hand or refurbished server pulls. The card typically comes **without a fan** and requires aftermarket cooling solutions.

---

### Recommended Workstation Configuration

| Component | Recommended Model | JD.com Availability |
|-----------|-------------------|---------------------|
| **GPU** | AMD Radeon Instinct MI50 16GB/32GB | Second-hand market only (not on JD) |
| **CPU** | AMD EPYC 7002 series (e.g., EPYC 7642, 48 cores) | Search "AMD 霄龙" |
| **Motherboard** | Supermicro H11DSi (Dual EPYC, E-ATX, 7 PCIe 4.0 x16 slots) | Search "超微 H11DSi" |
| **Memory** | Samsung DDR4 ECC RDIMM 32GB/64GB (8-channel support) | Search "三星 DDR4 ECC" |
| **Storage** | Samsung 990 PRO NVMe M.2 2TB | Available on JD |
| **Power Supply** | Huntkey IP1650G 1650W Gold (or 1250W) | Search "航嘉 重火力 IP1650G" |
| **Cooling** | DIY fan/heatsink mod for MI50 + CPU tower cooler | Search "AMD MI50 散热" |
| **Chassis** | Dual-tower server/workstation case | Search "工作站 机箱" |

---

### Detailed Component Recommendations

#### 1. GPU: AMD Radeon Instinct MI50

Two variants exist: **16GB** (~¥600-760) and **32GB** (~¥900). The 32GB version is preferred for AI/LLM workloads.

- **Key specs**: 1TB/s memory bandwidth, PCIe 4.0, HBM2 memory
- **Warning**: No built-in fan; requires DIY cooling (turbo fan + heatsink mod costs ~¥70)
- **Driver**: Requires AMD ROCm on Linux (Ubuntu 24.04 recommended)

#### 2. CPU: AMD EPYC 7002 Series

For multi-GPU setups, an EPYC CPU with **128 PCIe lanes** is essential. The **EPYC 7642** (48 cores, 2.3GHz) is a proven choice. Search **"AMD 霄龙"** on JD.

#### 3. Motherboard: Supermicro H11DSi

- Dual SP3 sockets supporting EPYC 7001/7002 series
- 16× DDR4 DIMM slots, supports up to 2TB ECC memory, 8-channel
- 7 PCIe 4.0 x16 slots — ideal for multi-GPU setups
- E-ATX form factor
- Reference price: ~¥5,500. Search **"超微 H11DSi"** on JD.

#### 4. Memory: Samsung DDR4 ECC RDIMM

- Requires **ECC Registered** memory
- 8-channel support, 2666MHz or higher
- Recommended: 64GB×8 = 512GB for large model inference
- Search **"三星 DDR4 ECC"** on JD

#### 5. Power Supply: 1250W–1650W

Each MI50 draws ~160-190W. For dual-GPU:
- Minimum: 1250W Gold
- Recommended: 1650W Gold
- Search **"航嘉 重火力 IP1650G"** (¥1,199) or **"工作站 电源"** on JD

#### 6. Cooling

**For MI50**: The card lacks a fan. Common DIY solutions:
- Turbo fan + heatsink shell (~¥35 total)
- 50mm fans per GPU (2 fans recommended)
- Water cooling option (~¥59)

**For CPU**: 6-heatpipe tower cooler (e.g., Thermalright PA120SE)

#### 7. Chassis

- Requires **E-ATX** support
- **Dual-tower** case recommended for dual-GPU with water cooling
- GPU length must be under 340mm
- Search **"工作站 机箱"** on JD

---

### Multi-GPU Configuration Examples

| GPUs | Use Case | Reference |
|------|----------|-----------|
| 2× MI50 32GB | 70B parameter models |  |
| 4× MI50 32GB | 30B dense models, fine-tuning |  |
| 8× MI50 32GB | GLM 4.7, MiniMax-M2.1 |  |
| 16× MI50 32GB | DeepSeek v3.2 |  |

---

### Critical Considerations

1. **No warranty**: These are used server pulls with high miner risk
2. **DIY required**: Cooling, drivers, and potential BIOS flashing
3. **Linux recommended**: ROCm support is primary on Linux
4. **Power**: Ensure adequate PSU and proper PCIe power cables
5. **JD.com primarily sells consumer GPUs** — MI50 is mostly found on second-hand platforms like Xianyu (闲鱼)
