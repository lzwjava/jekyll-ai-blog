---
audio: false
generated: true
image: false
lang: en
layout: post
title: Suqiao RTX 5090 96GB clamshell mod
translated: false
type: note
---

Question: **How does Suqiao turn an RTX 5090 into a 96GB card? What exactly is being changed?**

Answer:

The key point is: **they are not magically “unlocking” 64GB of hidden VRAM.** The likely approach is a **custom PCB + different GDDR7 population + firmware/VBIOS changes**.

### 1. Start with the GB202 GPU

The RTX 5090 uses NVIDIA's **GB202** GPU.

The interesting part is that **RTX PRO 6000 Blackwell also uses GB202 and officially has 96GB GDDR7**. So the GPU architecture itself is not fundamentally incapable of addressing 96GB. ([Tom's Hardware][1])

Conceptually:

```text
RTX 5090
             ┌───────────────┐
             │     GB202     │
             │     GPU       │
             └───────┬───────┘
                     │
          32 GB GDDR7
          16 × 2 GB chips
```

The stock 5090 has a **512-bit memory interface** and 32GB GDDR7.

---

### 2. The trick is probably "clamshell" memory

This is the interesting hardware hack.

Instead of putting one memory chip on each memory channel location, you can put **two chips electrically associated with the same channel, on opposite sides of the PCB**.

Something conceptually like:

```text
             FRONT OF PCB
       ┌──────────────────────┐
       │ GDDR7 GDDR7 GDDR7 ... │
       │        GB202          │
       │ GDDR7 GDDR7 GDDR7 ... │
       └──────────────────────┘
             BACK OF PCB
       ┌──────────────────────┐
       │ GDDR7 GDDR7 GDDR7 ... │
       │ GDDR7 GDDR7 GDDR7 ... │
       └──────────────────────┘
```

That's **clamshell memory**.

The RTX PRO 6000 is strong evidence that NVIDIA's GB202 platform can work with this kind of high-density memory configuration. Reports on the Suqiao board specifically identify a custom PCB and clamshell arrangement as the likely mechanism. ([The Silicon Report][2])

So the physical modification is approximately:

```text
stock 5090:

GPU ── 16 × 2GB GDDR7
       = 32GB


Suqiao:

GPU ── 32 × 3GB GDDR7
       = 96GB
```

**The important detail is the memory chip density.**

If they really have 96GB, they need something like **3GB-per-chip GDDR7 devices** with 32 devices, or another equivalent high-density topology.

---

### 3. This is why the Alibaba specification is suspicious

The listing reportedly says something along the lines of:

```text
GDDR6X
14 Gbps
96GB
```

Those numbers don't make much sense together.

GDDR6X is generally associated with considerably higher speeds than 14 Gbps, and known 16Gb GDDR6X devices would make a 96GB configuration problematic even with clamshell. ([The Silicon Ledger][3])

For a genuine 96GB Blackwell implementation, **96GB GDDR7 using 3GB-per-device parts** makes considerably more engineering sense.

So I would currently interpret the Alibaba specification as:

> **The product may be real, but the public spec sheet is not technically trustworthy.**

There is still no solid independent teardown/benchmark evidence establishing exactly what Suqiao is shipping. ([NeoTeo][4])

---

### 4. PCB is the really hard part

You can't just desolder the 5090's 32GB and solder more chips onto the original PCB.

You need a PCB designed for the topology.

Think:

```text
                 ┌──────────────┐
                 │    GB202     │
                 └──────┬───────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
     memory          memory          memory
     channel 0       channel 1       channel 2
        │               │               │
     ┌──┴──┐         ┌──┴──┐         ┌──┴──┐
     │     │         │     │         │     │
    front back      front back      front back
```

Now you have to solve:

* high-speed GDDR7 routing
* power delivery for additional memory
* signal integrity
* termination
* memory training
* thermal design
* GPU ↔ memory topology
* VBIOS memory configuration

This is why this is much closer to **ODM engineering** than a normal "GPU mod".

Suqiao reportedly has experience making graphics cards, motherboards and servers, which makes a custom PCB approach plausible. ([Tom's Hardware][1])

---

### 5. Then you need firmware/VBIOS support

This part is easy to underestimate.

The GPU needs to know:

```text
memory type       = GDDR7
memory devices    = ...
capacity/device   = ...
total capacity    = 96GB
channel topology  = ...
timings           = ...
training          = ...
```

So even if you physically solder 96GB onto the board:

```text
GPU
 ↓
"Where the fuck is the extra memory?"
```

won't magically become 96GB.

You need the appropriate **VBIOS / memory configuration / initialization firmware**.

Previous Chinese RTX 4090 48GB modifications demonstrated that increasing VRAM can involve firmware changes in addition to replacing the memory hardware. ([Jagat Review][5])

---

## The more interesting question: why can this be so cheap?

This is where it gets interesting for AI.

NVIDIA already manufactures something conceptually close:

```text
                 GB202
                   │
        ┌──────────┴──────────┐
        │                     │
   RTX 5090              RTX PRO 6000
   32GB                  96GB
   consumer              workstation
```

The GPU die isn't necessarily the expensive/limiting conceptual part.

The huge price difference between a 5090 and PRO 6000 also includes:

* product segmentation
* ECC / RAS features
* workstation validation
* drivers
* warranty
* enterprise support
* board design
* memory
* NVIDIA product positioning

So a Shenzhen ODM can potentially take the **GB202 ecosystem** and build a much cheaper board optimized for:

```text
LLM inference
      ↓
96GB VRAM
      ↓
one GPU
      ↓
no need for NVLink
      ↓
fit larger model in one address space
```

That is a *very* attractive configuration for local inference.

---

## But there is one huge distinction

**96GB capacity ≠ 96GB performance.**

For LLM inference, approximately:

```text
model weights
    ↓
VRAM capacity       → "Can the model fit?"
    ↓
memory bandwidth    → "How fast can I decode it?"
```

A 96GB card running GDDR7 at lower clocks could potentially have dramatically different performance from a 32GB 5090.

So I'd want these numbers before buying:

```bash
nvidia-smi

nvidia-smi --query-gpu=name,memory.total,memory.bus_width,\
memory.clock,clocks.current.memory,power.draw \
--format=csv

nvidia-smi -q
```

And especially:

```text
VRAM = 96GB?
Memory type = GDDR7?
Bus = 512-bit?
Memory clock?
Effective bandwidth?
ECC?
PCIe?
CUDA compute capability?
Driver recognition?
```

Then benchmark actual LLM throughput:

```bash
vllm serve <model> \
  --tensor-parallel-size 1
```

and measure:

```text
prefill tok/s
decode tok/s
VRAM used
power
temperature
long-duration stability
```

### My current engineering model

I'd draw Suqiao's likely design as:

```text
                    ┌──────────────────┐
                    │      GB202       │
                    │  RTX 5090-class  │
                    └────────┬─────────┘
                             │
                       512-bit bus
                             │
              ┌──────────────┴──────────────┐
              │                             │
       FRONT OF PCB                  BACK OF PCB
       ┌──────────────┐              ┌──────────────┐
       │  GDDR7      │              │  GDDR7      │
       │  GDDR7      │              │  GDDR7      │
       │  ...        │              │  ...        │
       └──────────────┘              └──────────────┘
              │                             │
              └──────────────┬──────────────┘
                             │
                           96GB
                             │
                       Custom VBIOS
```

**That is the plausible architecture.** But as of the currently available reporting, the *exact Suqiao implementation has not been independently verified*, and the contradictory Alibaba memory specs are a real red flag. ([NeoTeo][4])

References:

* [Tom's Hardware — 96GB RTX 5090 analysis](https://www.tomshardware.com/pc-components/gpus/china-modified-nvidia-rtx-5090-with-massive-96gb-of-memory-appears-on-alibaba-for-less-than-usd4-000-3x-more-vram-at-65-percent-the-cost-of-the-original?utm_source=chatgpt.com)
* [The Silicon Report — technical analysis of the custom PCB/clamshell approach](https://www.thesiliconreport.com/articles/blackwell-unleashed-shenzhen-odm-re-engineering-yields-96gb-modified-rtx-5090?utm_source=chatgpt.com)
* [NeoTeo — specification inconsistencies and verification status](https://www.neoteo.com/en/alibaba-lists-a-claimed-96gb-geforce-rtx-5090-but-the-hardware-is-unverified?utm_source=chatgpt.com)
* [Igor'sLAB — technical feasibility and caveats](https://www.igorslab.de/zh/rtx-5090-96gb-vram-alibaba-modification-unconfirmed-zh-cn/?utm_source=chatgpt.com)

I can also reverse-engineer the **actual 96GB memory topology** from the RTX PRO 6000/GB202 datasheets and work out exactly how many GDDR7 chips, bus connections, PCB layers, and memory channels Suqiao would need.

[1]: https://www.tomshardware.com/pc-components/gpus/china-modified-nvidia-rtx-5090-with-massive-96gb-of-memory-appears-on-alibaba-for-less-than-usd4-000-3x-more-vram-at-65-percent-the-cost-of-the-original?utm_source=chatgpt.com "China-modified Nvidia RTX 5090 with massive 96GB of memory appears on Alibaba for less than $4,000 - 3x more VRAM at 65% the cost of the original"
[2]: https://www.thesiliconreport.com/articles/blackwell-unleashed-shenzhen-odm-re-engineering-yields-96gb-modified-rtx-5090?utm_source=chatgpt.com "Blackwell Unleashed: Shenzhen ODM Re-Engineering Yields 96GB Modified RTX 5090 | The Silicon Report"
[3]: https://thesiliconledger.com/industry/chinese-manufacturer-offers-modified-rtx-5090-with-96gb-vram-on-alibaba-for-under-4000?utm_source=chatgpt.com "Chinese Manufacturer Offers Modified RTX 5090 with 96GB VRAM on Alibaba for Under $4,000"
[4]: https://www.neoteo.com/en/alibaba-lists-a-claimed-96gb-geforce-rtx-5090-but-the-hardware-is-unverified?utm_source=chatgpt.com "Alibaba lists a claimed 96GB RTX 5090, but the specs do not add up | NeoTeo"
[5]: https://www.jagatreview.com/2026/09/rtx-5090-dimodifikasi-jadi-96gb/?utm_source=chatgpt.com "RTX 5090 Dimodifikasi Jadi 96GB, Harganya Sekitar Rp68 Jutaan • Jagat Review"
