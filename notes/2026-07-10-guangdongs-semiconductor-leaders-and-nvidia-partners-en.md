---
audio: false
generated: true
image: false
lang: en
layout: post
title: Guangdong's Semiconductor Leaders and Nvidia Partners
translated: false
type: note
---

Question: In Guangdong, which semiconductor companies are strong performers, and which act as vendors/partners to Nvidia, AMD, etc.?

Answer:

Guangdong (mostly Shenzhen, Dongguan, Guangzhou) doesn't have EUV fabs — that's TSMC/Samsung/SMIC territory (Shanghai, Taiwan). What Guangdong dominates is **IC design, packaging/board assembly, power semiconductors, and downstream board partners**. Breaking it down by category:

### 1. IC Design (fabless) — the real "does well" tier

- **HiSilicon (海思)** — Shenzhen, Huawei subsidiary. Not a vendor to Nvidia — a *competitor*. Ascend 910B/910C chips are China's closest domestic alternative to Nvidia H100/A100 for AI training/inference. In 2019 HiSilicon led Shenzhen IC design sales at 83.4 billion yuan, dwarfing everyone else in the region. This is the one to watch if you're thinking about the "domestic GPU replacement" angle for your DeepSeek/MoE work.
- **Goodix Technology (汇顶科技)** — Shenzhen. Goodix Technology has 3,500 authorized patents, world leader in fingerprint/biometric sensors, expanding into IoT/health sensing.
- **Will Semiconductor (韦尔股份)** — technically Shanghai-HQ'd but heavy Guangdong supply chain presence (via OmniVision). Will Semiconductor has 4,731 authorized patents, the highest in China's fabless 100 — CMOS image sensors, competes with Sony.
- **BYD Semiconductor** — Shenzhen. A powerhouse in automotive-grade IGBT 6.0 and SiC (Silicon Carbide) power modules and MCU chips, controlling the full power chain of EVs. Not GPU-adjacent, but this is where China's power semi moat actually is — relevant if you ever touch power delivery for AI racks.
- **ZTE Microelectronics** — Shenzhen, telecom infrastructure chips, 80 billion yuan in 2019 sales, second only to HiSilicon regionally.
- **GigaDevice (兆易创新)** — technically Beijing HQ but a major NOR/NAND flash and GD32 (ARM MCU) supplier widely used across Guangdong's hardware supply chain as a cost-effective alternative to STMicro.

### 2. Nvidia/AMD board partners (AIB/AIC) physically rooted in Guangdong

These don't make silicon — they license Nvidia/AMD GPU dies and build the actual graphics cards:

- **Baisheng Group (PC Partner)** — manufacturing base in Houjie Town, Dongguan City, Guangdong, responsible for OEM production of Nvidia's public (reference) graphics cards, owns ZOTAC, Inno3D, and Manli brands. Note: PC Partner moved its HQ to Singapore in late 2024 specifically to avoid US export restrictions, though Dongguan manufacturing likely continues.
- **Yeston (影驰/铭瑄-adjacent, distinct brand)** — founded in Shenzhen in 2000, became AMD's highest-level partner in China in 2011, sells AMD graphics cards in the US market.
- **Galax/Galaxy Technology** — HK-registered but mainland China manufacturing/ops footprint; became an Nvidia AIC customer in 1999 and Nvidia's official "Launch Partner".

### 3. EMS / connectors / packaging (the invisible layer of the AI supply chain)

- **Luxshare Precision (立讯精密)** — Dongguan/Kunshan, one of China's biggest connector/EMS players, increasingly moving into server and AI-datacenter connector business (competes conceptually with Amphenol/TE Connectivity in the GB200-style supply chains mentioned in the search results connector and cable houses (Amphenol, Samtec, TE Connectivity) — Luxshare is China's analog).
- **Shennan Circuits (深南电路)** — Shenzhen, high-end PCB/substrate maker, supplies advanced HDI boards used in server and networking gear.
- **Han's Laser** — Shenzhen, laser processing equipment used in semiconductor and PCB manufacturing lines.

### The honest framing for your situation

None of these are direct "Nvidia GPU vendors" in the sense of supplying wafers or HBM (that's TSMC/Samsung/SK Hynix/Micron, all outside Guangdong). Guangdong's actual value in the Nvidia/AMD chain is: **(a)** board assembly/AIB partners (Dongguan/Shenzhen), **(b)** connectors/PCB/EMS feeding into server racks, and **(c)** domestic GPU-alternative design (HiSilicon Ascend) if you're tracking who eventually competes with Nvidia rather than serves it. Given your DeepSeek v4 MoE and Tinker-level infra focus, HiSilicon's Ascend roadmap and CANN (their CUDA-equivalent software stack) is probably more relevant to your consulting angle than the board-assembly companies — that's where high-end clients in the GBA will actually need help (porting kernels/CUDA code to Ascend, or building AMD ROCm equivalents).

If you want, I can dig deeper into HiSilicon Ascend's software stack (CANN) vs CUDA/ROCm — that's the actual technical moat question for anyone consulting in this space in Guangzhou/Shenzhen right now.

References:

- [NVIDIA Supplier List: Find Verified Graphics Card & GPU Suppliers](https://www.accio.com/supplier/nvidia-supplier-list)
- [Top 10 Semiconductor Companies in Shenzhen Ranking: The 2026 Definitive Guide](https://www.hdshi.com/top-10-semiconductor-companies-in-shenzhen-ranking-the-2026-definitive-guide)
- [Power Semiconductors Weekly Vol. 18 - Marketing Psycho](https://www.marketing-psycho.com/power-semiconductors-weekly-vol-18/)
- [China Fabless 100 2024 Edition](https://www.eetimes.com/wp-content/uploads/2024_China-Fabless-100_final_single.pdf)
- [Review | 12 Chinese Brands in the Overseas Gaming Graphics Card Market - EqualOcean](https://equalocean.com/analysis/2023072119940)
- [Tech war: Hong Kong maker of Nvidia graphics cards PC Partner moves to Singapore - SCMP](https://www.scmp.com/tech/big-tech/article/3287101/tech-war-hong-kong-maker-nvidia-graphics-cards-pc-partner-moves-singapore)
