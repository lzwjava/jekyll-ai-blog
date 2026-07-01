---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why Interconnect Bandwidth Matters
translated: false
type: note
---

**Question:** Why does interconnect matter so much? Why is Marvell good at interconnect bandwidth? SK Hynix does bandwidth too — and does NVLink use Marvell?

**Answer:**

Three separate things are getting conflated here, so let's untangle them from first principles. You're mixing up **memory bandwidth** (SK Hynix's layer) with **network interconnect** (Marvell's layer), and NVLink sits in between. They're all "moving bits," but at different physical distances, and the physics at each distance dictates who can play.

## 1. Why interconnect is the bottleneck — the math

Training a large model is fundamentally a communication problem disguised as a compute problem. Take data-parallel training: every step, each GPU must all-reduce its gradients. For a ring all-reduce, each GPU sends/receives:

```python
# Communication volume per GPU per step (ring all-reduce)
P = 70e9            # params (70B model)
bytes_per_grad = 2  # bf16
N = 1024            # GPUs

vol = 2 * (N - 1) / N * P * bytes_per_grad   # ≈ 280 GB per GPU per step!

# At 400 Gbps (50 GB/s) network: 280/50 = 5.6s of pure comms per step.
# A B200 does the compute for that step in well under a second.
# => the GPU sits idle waiting for the network. FLOPs are free; bytes are not.
```

This is why people obsess over overlap (bucketed gradient all-reduce concurrent with backward pass — you've seen this in nanoGPT's DDP), and why frontier labs spend as much on the network fabric as on the GPUs. As clusters scale from 10k → 100k → 1M accelerators, compute scales linearly but communication patterns (all-to-all in MoE, tensor-parallel all-gathers) scale worse. Interconnect bandwidth, optical fabric integration, and rack-scale heterogeneous compute now matter alongside raw performance in who wins infrastructure deals.

The bandwidth hierarchy, by distance:

| Layer | Distance | Tech | Who makes the silicon |
| --- | --- | --- | --- |
| HBM | millimeters (on-package) | DRAM stacks via interposer, ~8 TB/s | **SK Hynix**, Samsung, Micron |
| Scale-up (NVLink) | <1m–rack | Copper SerDes, NVSwitch, ~1.8 TB/s/GPU | **Nvidia** (proprietary) |
| Scale-out network | 3m–500m | 800G/1.6T optical transceivers | **Marvell**, Broadcom (the DSPs inside) |
| DCI | km–100km | Coherent optics (400ZR/800ZR) | **Marvell** (ex-Inphi), Cisco/Acacia |

**Key physics fact:** copper dies at distance. At 112G/224G per lane, passive copper reaches only a few meters before signal integrity collapses. Beyond the rack, every link is optical — and every optical module needs a DSP chip to do PAM4 modulation, equalization, and clock recovery. That DSP market is essentially a Marvell/Broadcom duopoly. Every 1.6T transceiver in a 100k-GPU cluster has one of their chips in it. Count the transceivers in an NVL72 deployment and you see why this is a multi-billion-dollar annuity.

## 2. Why Marvell specifically

Their moat is **high-speed analog mixed-signal design** — the hardest, least-commoditized skill in semiconductors:

- **224G SerDes**: getting 224 Gbps through a single electrical lane is brutal analog engineering (equalization, FFE/DFE, jitter budgets). Marvell has 25+ years of PHY experience going back to their disk-drive read-channel days — read channels are literally signal recovery from noisy analog media, the same core competence.
- **Inphi ($10B, 2021)**: brought the PAM4 DSP franchise and coherent DSPs. This is the crown jewel.
- **Celestial AI**: Marvell acquired Celestial AI in December 2025 for $3.25 billion — its photonic fabric enables row-scale coherent memory and in-network collectives processing, similar to what Nvidia offers in NVSwitch via its Mellanox InfiniBand heritage. In-network all-reduce (SHARP-style) is exactly the AI-native answer to the comms bottleneck above.
- The pitch in their own words: leadership in high-performance analog, optical DSP, silicon photonics and custom silicon.

And the SerDes/optics expertise feeds the XPU business: Marvell's optical expertise is a driver of customer interest in its XPU designs — a custom accelerator is useless if its die-edge bandwidth can't keep up, so the hyperscaler buys the I/O and the chip design from the same vendor.

## 3. SK Hynix — different layer entirely

SK Hynix doesn't compete with Marvell at all. HBM is **memory bandwidth**: DRAM dies stacked with TSVs, sitting millimeters from the compute die on a CoWoS interposer, feeding the tensor cores. It solves "can my matmul read weights fast enough" (arithmetic intensity / roofline). Marvell solves "can GPU #4071 get gradients from GPU #88213." Both are bandwidth, but one is a memory technology and the other is a networking/signaling technology. SK Hynix sells HBM stacks *to* Nvidia and to Marvell's XPU customers — they're complementary, not competitors.

## 4. Does NVLink use Marvell?

**NVLink itself: no.** NVLink and NVSwitch are Nvidia's own proprietary SerDes, protocol, and switch silicon — designed in-house, fabbed at TSMC. Zero Marvell content.

**But the relationship changed in March 2026.** Nvidia invested $2 billion in Marvell and entered a strategic partnership centered on NVLink Fusion, the rack-scale platform that allows third-party silicon to plug directly into Nvidia's proprietary interconnect fabric. The split: Marvell provides custom XPUs and NVLink Fusion-compatible scale-up networking, while Nvidia provides Vera CPUs, ConnectX NICs, BlueField DPUs, NVLink interconnect, and Spectrum-X switches. So Marvell-designed chips can now *speak* NVLink — e.g. AWS has said the future Trainium 4 will support both UALink and NVLink protocols, and Marvell, as AWS's main custom-chip partner, needs access to Nvidia's technology for that.

The strategic read is sharp: Marvell's custom XPU business did $1.5B in fiscal 2026 and is expected to double by fiscal 2028, with 18 active custom silicon projects including 12 for Amazon, Google, Microsoft, and Meta — these chips exist to *displace* Nvidia GPUs. By pulling Marvell into NVLink Fusion, every NVLink Fusion setup requires at least one Nvidia part, so Marvell's ASICs still generate Nvidia revenue, while Broadcom leads UALink, the open alternative to NVLink, on the other side of the fabric war.

**TL;DR:** SK Hynix = bandwidth *into* a chip (HBM). Nvidia = bandwidth *within* a rack (NVLink). Marvell = bandwidth *between* racks and buildings (optical DSPs, SerDes, photonics) — plus, since March 2026, a licensed on-ramp to put NVLink ports on the custom chips it designs.

If you want to feel this viscerally in code, profile a multi-node nanoGPT run with `NCCL_DEBUG=INFO` and watch how much wall-clock goes to `AllReduce` vs compute as you scale nodes — the entire Marvell thesis is in that ratio.

**References:**

- [Nvidia–Marvell NVLink Fusion press release (marvell.com)](https://www.marvell.com/company/newsroom/nvidia-ai-ecosystem-expands-marvell-joins-forces-through-nvlink-fusion.html)
- [The Next Platform: the $2B Nvidia–Marvell deal](https://www.nextplatform.com/connect/2026/03/31/the-2-billion-nvidia-deal-with-marvell-is-about-a-lot-more-than-nvlink-fusion/5213790)
- [TNW: NVLink Fusion as ecosystem lock-in](https://thenextweb.com/news/nvidia-marvell-nvlink-fusion-ecosystem-lock-in)
- [TFN: NVLink Fusion ecosystem analysis](https://techfundingnews.com/nvidia-2-billion-marvell-nvlink-fusion-ai-ecosystem/)
