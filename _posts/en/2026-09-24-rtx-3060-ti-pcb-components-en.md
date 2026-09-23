---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 3060 Ti PCB Components
translated: false
type: note
---

Question: **Identify the electrical components visible on this RTX 3060 Ti PCB, and explain what each does.**

Answer:

This is the **GPU-side PCB of an RTX 3060 Ti**, with the cooler removed. The photo is good enough to identify the major power/data components, but **not good enough to read most individual IC part numbers**. RTX 3060 Ti boards vary substantially between vendors, so I won't pretend an exact BOM from the photo.

![Image](https://images.openai.com/static-rsc-4/-KSIMYV-4SIKZBhrkBdL45IIQwyb8m69w9KgH9DFQ7s5WdgZhHMpGMcOd66e-jPApAkrdBob-L1y--KLTNbY3Q9GhoebvfclfStgJmZr0sB4_FQ0jKK7jgKVZO6qKqVZv9jV7k2hctXheCiMDvk-D8ovPwR0pjZfiRlMK124Mo3s4kH24LM_kBoNKeHSf_V8?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/J51y_WXS7Z_OINabA3E99uuC_mmzQu88tlvOn0kuoGSB5LyOA7iVWPdbWkH6jSczyUXwACxyxuK_PuTHRpLeWqalsmGsGeUq9EUtRsI7zuwO2_ZUQ24SmUdwxIz-nz5ru-CTvm7P2XKKHBeHoTPhgc7pjz1LsceTkJYEO7jghIm6_3hEojjGXDd9x23HUmZj?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/PyRkAFvug7nhvNxeJGCH2PT5HEWLoC1iaOxua90k02IN3djQrlRARWeq_ZvZSF5DH4EycLLolPfibeZ2-tyV0gfuOcAoK7TzuytAICAVargbGg-LTMj0Imir07do9IGiR3nlSJdL0OiELcuokHJzqcMnhXnh0cSixmekMvYkuoqxlLVA4RytR6VD62M1Gm4F?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3UMdKuEOtW6m0HkF-tp1j13YNS80iZbUAQQ_fO1RoyBeGZ-aRupotZtTk2P-y98nw13VDd1UYGncUmKcL7rs9TTIGiVNckxS6d9jyCbcaQGGVaad2DmyijTzeu6lRhigkalxuV3Dd2WxYBlG8lK1OpPa4ogb2OUl9P-fyE-tohGYjOZ7RAkxuyHtLGGdIoWT?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/IHKvG7KxqTiM3OuReb1CFmx4tlIWyEluds_-j1hKS17MlxVV3_HpR1OM1opwnPWXanyNVGLdxeIiqKq4f3DCTp4GvjTCUHXBoshx9M_g3WAZCqz736KnepkNRDg55WyV9bLVA1CcHwuQ_x8UVEgoSbFGbg1HLZgj9OeHRqRcPVZwRkQZvn5rKB6DERTqiE2q?purpose=fullsize)

### 1. GPU — GA104

**Right side, large green package with exposed silicon die.**

This is the actual GPU:

* NVIDIA **GA104**
* RTX 3060 Ti uses the GA104 family
* ~392 mm² die
* 4,864 CUDA cores
* PCIe interface
* memory controller
* RT/Tensor cores
* display engines, etc.

The large gray material in the middle is old **thermal compound**.

NVIDIA specifies the RTX 3060 Ti as a GA104-based Ampere GPU. ([NVIDIA][1])

---

### 2. GDDR6 VRAM

**Left side — the rectangular black/brown packages.**

I can see approximately **four memory packages on this side**. The other four may be on the opposite side of the GPU / outside this photograph depending on the exact PCB.

A normal 8 GB RTX 3060 Ti uses:

```text
8 × 1 GB GDDR6
        │
        ├── 256-bit total bus
        └── 8 GB
```

Many 3060 Ti boards use Samsung `K4Z80325BC-HC14`, although some cards use Micron/Hynix and therefore **I cannot identify your exact memory vendor from this photograph**. Multiple 3060 Ti teardowns confirm eight 1-GB GDDR6 devices. ([Overclocking.com][2])

---

# 3. GPU VRM

This is the most interesting part of your photo.

**Immediately to the left of the GPU:**

```text
        GPU
         │
         │ ~0.8–1.1 V
         ▼
     VRM output
         │
   ┌─────┴─────┐
   │           │
 MOSFET      MOSFET
   │           │
 Inductor    Inductor
   │           │
   └─────┬─────┘
         │
       GPU
```

The GPU cannot run directly from PCIe's 12 V supply. The VRM converts roughly 12 V into a **very low GPU core voltage at very high current**.

### 3.1 Black rectangular inductors

**The vertical row of large black rectangular blocks in the center-left.**

These are **power inductors/chokes**.

They are one of the easiest components to identify in your photo.

Each phase roughly looks like:

```text
12 V
 │
 ▼
MOSFET/DrMOS
 │
 ▼
INDUCTOR  ← black block
 │
 ▼
GPU Vcore
```

The inductor stores/releases magnetic energy and smooths the switched current from the MOSFET stage.

Your board appears to have around **6 GPU-side phases**, but I would not call that certain from this photograph alone.

A documented RTX 3060 Ti board using a similar physical arrangement has **6 GPU phases + 2 memory phases**. ([XFastest][3])

---

# 4. MOSFET / DrMOS power stages

These are located **around/beside the inductors**, mostly the small black power packages.

Their job is essentially high-frequency switching:

```text
12 V
 │
 ├──── High-side MOSFET
 │
 └──── Low-side MOSFET
          │
          ▼
       INDUCTOR
          │
          ▼
         GPU
```

On modern GPUs these are often **DrMOS / integrated power stages**, meaning:

```text
High-side MOSFET
Low-side MOSFET
Gate driver
Current sensing
       ↓
  one package
```

That's why you don't necessarily see three separate components per phase.

For example, one documented RTX 3060 Ti design uses **Alpha & Omega AOZ5311NQI DrMOS** devices for its GPU phases. Other 3060 Ti models use completely different MOSFETs. ([XFastest][3])

**Important:** I cannot reliably read the marking on yours, so don't assume yours is AOZ5311NQI.

---

# 5. Blue cylindrical capacitors

You have a very obvious vertical group of these:

```text
○
○
○
○
○
○
○
```

These are **power capacitors**, most likely solid/polymer capacitors based on their physical construction.

Their job is:

* output ripple filtering
* transient current delivery
* stabilizing GPU Vcore
* reducing voltage fluctuations caused by rapidly changing GPU load

Conceptually:

```text
VRM ──── L ─────── GPU
         │
         C
         │
        GND
```

The capacitors work together with the inductors as the VRM's output filter.

There are also many tiny MLCC ceramic capacitors around the GPU and VRM that perform higher-frequency filtering.

---

# 6. Tiny MLCC ceramic capacitors

There are **hundreds of tiny components** scattered around the GPU/VRM.

The small beige/gray rectangles are predominantly:

* MLCC capacitors
* resistors
* occasionally ferrite beads / inductors

The GPU needs enormous amounts of local decoupling because its internal current changes extremely quickly.

You can think of them as microscopic local batteries:

```text
VRM ─────────────── GPU
                    │
                 ┌──┴──┐
                 │ MLCC │
                 └──┬──┘
                    GND
```

A typical RTX PCB schematic contains many values such as:

```text
0.1 µF
0.22 µF
1 µF
4.7 µF
10 µF
22 µF
...
```

The actual values cannot be determined visually.

A published RTX 3060 Ti schematic/BOM, for example, shows 0.1 µF, 4.7 µF, 10 µF, etc. around PCIe/GPU power rails. ([Scribd][4])

---

# 7. Memory VRM

The GDDR6 doesn't run directly from 12 V either.

There is a **separate smaller VRM** for the memory.

Typical architecture:

```text
12 V
 │
 ▼
Memory PWM
 │
 ▼
MOSFETs
 │
 ▼
Inductor
 │
 ▼
GDDR6 VDD / VDDQ
```

A documented RTX 3060 Ti design uses:

* `uP1666Q` memory PWM
* 2 memory phases
* integrated MOSFETs
* inductors
* polymer capacitors

But again, your exact board may differ. ([XFastest][3])

---

# 8. PWM VRM controller

There should be one or more small controller ICs controlling the power stages.

Typical 3060 Ti examples include:

```text
GPU VRM:
uP9512R
     │
     ├── phase 1
     ├── phase 2
     ├── ...
     └── phase N

Memory VRM:
uP1666Q
     │
     ├── phase 1
     └── phase 2
```

These chips don't carry the GPU's hundreds of amps themselves.

They generate the control signals:

```text
PWM controller
      │
      │ PWM
      ▼
Gate driver / DrMOS
      │
      ▼
MOSFET switching
```

On the NVIDIA RTX 3060 Ti Founders Edition specifically, a teardown identifies **uP9512R** as the GPU VRM controller and a **7-phase GPU VRM + 2-phase memory VRM**. ([Overclocking.com][2])

Your board appears to be a different/custom PCB, so its phase count and controller can differ.

---

# 9. Small resistors

The tiny rectangular components around the VRM/GPU include lots of resistors.

They perform things like:

```text
voltage feedback
current sensing
gate control
pull-up / pull-down
signal termination
power sequencing
```

The VRM controller needs feedback:

```text
             ┌──────────────┐
             │ PWM controller│
             └──────┬───────┘
                    │
                  PWM
                    ▼
                 VRM
                    │
                    ▼
                   GPU
                    │
                    │ VFB
                    └──────────► controller
```

That feedback network consists partly of tiny resistors/capacitors.

---

# 10. Ferrite beads / small inductors

There are also tiny inductive components mixed into the SMD population.

They are generally used to isolate/filter power domains:

```text
12V ── ferrite bead ──► sensitive circuit
```

For example:

```text
digital power
      │
      ├── ferrite ──► analog power
      │
      └── ferrite ──► PLL / clock / memory
```

They look similar to tiny resistors, so **I cannot distinguish every individual one from this photograph**.

---

# 11. BIOS / SPI flash

The GPU board must have a small nonvolatile flash chip containing firmware/VBIOS.

Typically:

```text
SPI NOR Flash
   │
   ├── GPU BIOS
   ├── board configuration
   ├── power/clock parameters
   └── fan/display configuration
```

Common chips are things like Winbond/GigaDevice/MXIC 8-pin SPI NOR devices.

It is likely on the board, but **the resolution/angle here doesn't let me confidently point to its exact package**.

---

# 12. Clock oscillator

There should also be one or more crystal/oscillator components providing reference clocks.

Conceptually:

```text
25/27 MHz reference
       │
       ▼
     GPU PLL
       │
       ├── core clock
       ├── memory clock
       └── PCIe clock domains
```

Again, the exact oscillator isn't readable in this photograph.

---

# 13. PCIe edge connector

**Bottom of your image.**

The long gold-finger connector is:

```text
PCI Express x16
```

It carries:

* PCIe differential TX/RX lanes
* reference clock
* 3.3 V
* auxiliary power/signals
* sideband signals
* ground

The GPU communicates with the CPU/chipset through this interface.

---

# 14. External 12 V power

Your particular board has an external GPU power input somewhere on the card, though it isn't clearly visible in this crop.

Electrically:

```text
PSU
 │
 │ 12 V
 ▼
GPU connector
 │
 ├──────── GPU VRM
 │
 ├──────── VRAM VRM
 │
 └──────── auxiliary regulators
```

The RTX 3060 Ti reference specification is around **200 W board power**, with NVIDIA specifying an 8-pin PCIe supplementary connector for the reference design. Custom cards can differ. ([NVIDIA][1])

---

# 15. Display-output circuitry

On the bracket side you can see the **DisplayPort/HDMI connector area**.

The connectors themselves aren't particularly interesting electrically; behind them are:

* high-speed differential traces
* ESD protection
* common-mode filtering
* termination/passive components
* GPU display PHY connections

The RTX 3060 Ti supports HDMI and DisplayPort outputs. ([NVIDIA][1])

---

# 16. ESD protection

Near external connectors there will normally be tiny ESD protection arrays.

For example:

```text
GPU ───────────── HDMI connector
                  │
                  ▼
              ESD TVS
                  │
                 GND
```

Their job is to absorb electrostatic discharge entering through an external connector instead of letting it reach the GPU.

These are tiny IC packages and aren't reliably distinguishable in your photograph.

---

# 17. Power-management auxiliary regulators

Besides the big GPU/VRAM VRMs, the board needs smaller rails such as:

```text
12 V
 │
 ├── ~1 V      GPU core
 ├── ~1.35 V   GDDR6
 ├── 1.8 V
 ├── 3.3 V
 ├── 5 V
 └── other auxiliary rails
```

Small buck converters/LDOs generate these.

For example, some RTX 3060 Ti boards use `GS9216` converters for auxiliary rails. ([Russerver][5])

---

## The important physical map of your photo

```text
                    TOP
 ┌──────────────────────────────────────────────┐
 │                                              │
 │   GDDR6       GPU VRM                       │
 │  ┌─────┐      ┌─────────┐                   │
 │  │ VRAM│      │ caps    │                   │
 │  ├─────┤      │  ○ ○ ○  │                   │
 │  │ VRAM│      │         │                   │
 │  ├─────┤      │ MOSFETs │                   │
 │  │ VRAM│      │ ███████ │                   │
 │  ├─────┤      │         │                   │
 │  │ VRAM│      │ inductors│                  │
 │  └─────┘      │ ███████ │                   │
 │               └────┬────┘                   │
 │                    │                         │
 │                    │ VCORE                   │
 │                    ▼                         │
 │              ┌─────────────┐                 │
 │              │             │                 │
 │              │   GA104     │                 │
 │              │    GPU      │                 │
 │              │             │                 │
 │              └─────────────┘                 │
 │                                              │
 └──────────────────────────────────────────────┘
                    BOTTOM
```

### What I can identify with high confidence from your actual photo

| Visible item                          | Identification                 | Confidence |
| ------------------------------------- | ------------------------------ | ---------- |
| Large green package                   | GA104 GPU package/die          | **High**   |
| Large black rectangular row           | VRM inductors/chokes           | **High**   |
| Blue cylindrical parts                | Polymer/solid power capacitors | **High**   |
| Rectangular chips left                | GDDR6 memory                   | **High**   |
| Black power packages around inductors | MOSFET/DrMOS stages            | **High**   |
| Tiny beige/black SMDs                 | Resistors/MLCCs/etc.           | **High**   |
| Gold edge connector                   | PCIe x16                       | **High**   |
| Small ICs around VRM                  | PWM/driver/regulator circuitry | **Medium** |
| Exact MOSFET model                    | e.g. AOZ5311NQI/etc.           | **Low**    |
| Exact PWM controller                  | uP9512R/etc.                   | **Low**    |
| Exact capacitor values                | µF/voltage                     | **Low**    |
| Exact resistor values                 | Ω                              | **Low**    |
| BIOS flash                            | SPI NOR                        | **Medium** |
| Clock oscillator                      | reference clock                | **Medium** |

### The key thing

The giant GPU is actually **not the most electrically interesting part of this particular photograph**. The critical power path is:

```text
PSU 12 V
   │
   ▼
┌─────────────┐
│ PWM control │
└──────┬──────┘
       │ PWM
       ▼
┌─────────────┐
│ MOSFET/DrMOS│  ← switches hundreds of watts
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  INDUCTOR   │  ← black blocks
└──────┬──────┘
       │
       ├────── capacitors
       │
       ▼
    ~1 V VCORE
       │
       ▼
     GA104
```

For a **component-level repair**, the next useful photo is a **straight-on, high-resolution shot of both sides of the entire PCB**, ideally with the component markings in focus. Then I can go component-by-component and produce something like:

```text
Uxxx = PWM controller
Qxxx = MOSFET/DrMOS
Lxxx = xx µH inductor
Cxxx = xx µF / xx V
Rxxx = xx Ω
Uxxx = SPI BIOS
Uxxx = VRAM
...
```

That would get much closer to an actual **RTX 3060 Ti PCB BOM/schematic-level identification**, rather than just recognizing component classes. ([Scribd][4])

References:

* [NVIDIA GeForce RTX 3060 Family specifications](https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3060-3060ti/?utm_source=chatgpt.com)
* [RTX 3060 Ti Founders Edition PCB/VRM analysis](https://overclocking.com/test-nvidia-rtx-3060-ti-founders-edition/3/?utm_source=chatgpt.com)
* [RTX 3060 Ti PCB and 6+2-phase VRM analysis](https://www.xfastest.com/thread-247420-1-30.html?utm_source=chatgpt.com)
* [RTX 3060 Ti PCB schematic/BOM reference](https://www.scribd.com/document/765910143/Asus-Rtx-3060ti-Cg190pi-1-00?utm_source=chatgpt.com)

[1]: https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3060-3060ti/?utm_source=chatgpt.com "GeForce RTX 3060 Family | NVIDIA"
[2]: https://overclocking.com/test-nvidia-rtx-3060-ti-founders-edition/3/?utm_source=chatgpt.com "Test : NVIDIA RTX 3060 Ti Founders Edition - Spécifications et PCB : sur 13 - Overclocking.com"
[3]: https://www.xfastest.com/thread-247420-1-30.html?utm_source=chatgpt.com "INNO3D GeForce RTX 3060 Ti iCHILL X3 開箱測試 / 三風扇六熱導管，優質散熱的好選擇-iCHILL,INNO3D,RTX 3060 Ti,NVIDIA -"
[4]: https://www.scribd.com/document/765910143/Asus-Rtx-3060ti-Cg190pi-1-00?utm_source=chatgpt.com "Asus RTX 3060ti Cg190pi 1.00 | PDF"
[5]: https://www.russerver.com/blog/videokarta-s-aliexpress.-razborka-i-obsluzhivanie.?utm_source=chatgpt.com "Видеокарта с AliExpress. Разборка и обслуживание."