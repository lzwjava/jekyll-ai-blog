---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diagnose and Repair Broken GPUs
translated: false
type: note
---

Question: **What’s the best way to learn NVIDIA GPU repair from second-hand/Xianyu cards? Should I just buy broken cards and repair them hands-on?**

Answer: **Yes. For you, I’d absolutely learn by doing.** But don't start by randomly heating chips. Treat each broken GPU as a **diagnostic experiment**.

The fastest path is:

```text
cheap dead GPUs
      ↓
visual inspection
      ↓
resistance measurements
      ↓
understand power rails
      ↓
controlled power-on
      ↓
voltage measurements
      ↓
find failed component
      ↓
replace component
      ↓
test
      ↓
write down what you learned
```

A good GPU repair workflow is essentially **electronics debugging**, not "GPU magic." A professional diagnostic flow starts with resistance checks, inspection, rail measurements, controlled power-up, and then thermal/oscilloscope work. ([YouTube][1])

### 1. Buy the right broken cards

Don't start with expensive 4090/5090s.

I'd buy **GTX 10-series → RTX 20-series → RTX 30-series** broken cards from Xianyu.

Look specifically for:

* `不亮`
* `无显示`
* `核心供电短路`
* `12V短路`
* `维修过`
* `烧供电`
* `掉件`
* `显存报错`
* cards explicitly sold as `坏卡`

Avoid cards where the seller says:

> "GPU core probably dead"

Those are terrible learning boards because you can't easily prove what happened.

A card with a blown MOSFET, missing capacitor, shorted rail, damaged connector, etc. is much more educational.

---

### 2. Your first goal isn't "repair"

Your first goal should be:

> **Given a dead GPU, can I explain electrically why it doesn't work?**

For example:

```text
GPU doesn't power on
       ↓
12V input?
       ↓
12V → VRM?
       ↓
3.3V auxiliary?
       ↓
1.8V?
       ↓
PEX?
       ↓
Vcore?
       ↓
VRAM rail?
       ↓
BIOS?
       ↓
GPU initialization?
```

That's much more valuable than learning "replace this MOSFET."

The excellent long-form GPU repair guide from Learn Electronics Repair follows almost exactly this progression: visual inspection → resistance → voltage → practical voltage diagnosis → GPU initialization problems. ([YouTube][1])

---

### 3. Learn VRM extremely well

This is probably your **#1 subject**.

A typical GPU core VRM looks roughly like:

```text
12V
 │
 ├── High-side MOSFET
 │
 ├── Low-side MOSFET
 │
 ▼
 Inductor
 │
 ├──── VCORE
 │
 └──── capacitors
```

with multiple phases:

```text
             ┌─ MOSFET ─ MOSFET ─ Coil ─┐
12V ─────────┼─ MOSFET ─ MOSFET ─ Coil ─┼── VCORE
             ├─ MOSFET ─ MOSFET ─ Coil ─┤
             └─ MOSFET ─ MOSFET ─ Coil ─┘
```

Then learn:

* high-side / low-side MOSFET
* gate
* source
* drain
* PWM controller
* gate driver
* inductor
* output capacitor
* enable signal
* power-good
* feedback
* current sensing

Once you understand that circuit, GPU repair becomes much less mysterious.

---

### 4. Use a schematic + boardview from day one

This is where you should leverage your engineering background.

**Schematic tells you:**

```text
what connects to what
```

**Boardview tells you:**

```text
where it physically is
```

That's an incredibly powerful combination for modern GPUs. ([RC4BD][2])

For example:

```text
Schematic:

PVDD_GPU
   ↓
PUxxx
   ↓
Qxxx
   ↓
FBxxx
   ↓
NVVDD
```

Then BoardView:

```text
FBxxx → physical location on PCB
```

Now your multimeter probe has a reason.

There are GPU-specific boardview databases/tools available; for example, GPU Doctor currently advertises NVIDIA/AMD boardviews covering 500+ GPU models. ([GPU Doctor][3])

---

### 5. Build a repair notebook

This will accelerate your learning enormously.

For every GPU:

```text
GPU: RTX 2060
PCB: MS-Vxxx

Symptom:
No display

Initial resistance:

12V PCIe:       normal
3.3V:           normal
VCORE:          0.8 Ω
Vmem:           35 Ω
PEX:            18 Ω

Power-on:

12V:            12.1V
3.3V:            3.3V
1.8V:            1.8V
Vmem:            1.35V
Vcore:           0V

Diagnosis:
Vcore VRM doesn't start

Next:
Check PWM EN
Check VCC
Check gate signals
```

Then:

```text
Replaced: xxx MOSFET
Result: Vcore = 0.75V
GPU boots
```

After 20–30 boards, you'll have your own **GPU failure database**.

That's much more valuable than watching 100 repair videos.

---

### 6. Don't buy an oscilloscope immediately

I'd go:

```text
multimeter
    ↓
bench PSU
    ↓
hot air + soldering iron
    ↓
microscope
    ↓
thermal camera
    ↓
oscilloscope
```

You can solve a surprising amount with the first four.

The basic GPU repair equipment commonly recommended includes a multimeter, hot-air station, soldering station, and bench PSU, with microscope/BGA equipment becoming useful later. ([Cnblogs][4])

Your engineering background means you'll probably hit the ceiling of the multimeter faster than a normal beginner, though. At that point, an oscilloscope becomes extremely useful for:

```text
PWM
gate drive
clock
reset
PCIe signals
enable
power sequencing
```

---

### 7. Be very systematic about shorts

This is probably the first major skill I'd deliberately train.

Suppose:

```text
12V → short to GND
```

Don't immediately inject power and hope.

Trace:

```text
12V
 │
 ├── VRM #1
 ├── VRM #2
 ├── VRM #3
 ├── filter
 ├── protection
 └── other circuits
```

Then isolate sections.

For a VRM:

```text
12V
 ↓
MOSFET
 ↓
coil
 ↓
VCORE
```

If VCORE is short:

```text
Is it the GPU core?
       or
MOSFET?
       or
capacitor?
       or
another load?
```

That distinction is the actual repair skill.

---

### 8. Don't make BGA reballing your first skill

I'd **avoid starting with GPU core reballing / core replacement / VRAM replacement**.

Those are seductive because they look impressive:

```text
heat GPU
↓
remove GPU
↓
reball
↓
install
↓
pray
```

But you learn very little if the card suddenly works.

Instead:

```text
find short
→ identify component
→ replace component
→ verify rail
→ boot
```

That's where your understanding compounds.

Later:

```text
VRAM
↓
GDDR6
↓
GDDR6X
↓
GPU BGA
↓
core replacement
```

---

## I'd personally structure your first 10 cards like this

| Cards | Objective                                    |
| ----- | -------------------------------------------- |
| 1–2   | Learn PCB layout + multimeter                |
| 3–4   | Find shorts                                  |
| 5–6   | Diagnose VRM                                 |
| 7     | BIOS / SPI                                   |
| 8     | Memory power / VRAM                          |
| 9     | No-display sequencing                        |
| 10    | Full diagnosis without looking at a tutorial |

And **don't care whether you successfully repair all 10**.

If card #3 dies permanently but you can explain:

> "This MOSFET failed, caused a short on PVDD, which prevented the VRM from starting."

that's already a successful learning exercise.

---

## One important rule

Don't let the experiment turn into:

```text
broken GPU
↓
heat everything
↓
replace MOSFET
↓
replace VRAM
↓
reball GPU
↓
still broken
```

Instead:

```text
OBSERVATION
    ↓
HYPOTHESIS
    ↓
MEASUREMENT
    ↓
UPDATE HYPOTHESIS
    ↓
REPAIR
    ↓
MEASUREMENT
```

Basically **scientific method + circuit analysis**.

Given that you're already comfortable with computers, GPUs, Linux, CUDA/ROCm and hardware, I think this is a particularly good hobby for you: you're not learning electronics from zero; you're applying **debugging instincts to physical circuits**.

![Image](https://images.openai.com/static-rsc-4/-8ve_1Mtsf4-iXxohmG_lFElZwTdFdE-qDKcadcLASp4fmtfTQHU1FfMhCigJgPJCfSN4nzPfwL8lqpusB0jAvGaecldd5CbgsG_wOqs_dCPqLFIghdN--1E4dxt1yw_XqBLaW8F5UTOek6EurG0d3D0EWM0WXHZu4hBVzA-Ba5NZTfZzfizHGITotJezRKA?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/nLMC9ujWUn4v1U7p_o3S4e2q3G59SBokeHJNlwDQCzfhrbva7eMRL_bFN1hXz1KL0OJ5bm5f0JmrJ6srcj5Hirn8p8Z3GkJdu2iggbRVHBPo7JL1xwTP-Ha627A4bL3FTDq-RsSyQuJhHVuRRL_bH3II7huLuOae259eLmybQdQOjtfEfmD9YoseH7euFLHk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/F1rlULV95gBsDlLu1hEmprAqibWSZdMLeaFUx-RZt7cr-BP9X0LAC9XVNsOI4Q7Oz7JdqkJ8dT1FVZSNbuXbFb3OBccZwyb7VilOZQNRiDB979hFPQsfVuOXyU007eVFZ34zmSGfqNsXpYx17tsYck9r9oqCURsrAZvwYM1U-9fPYtwWUgtMFn0UcfVEMPg2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/GgA0r3eNMt4UoxAtttbz4uxVRMObc6ZYp90AGgUwK4dDGKGVCWA4lN3mfHxszo2Zoc7Z9zpt27_xr2zh5IIDK7qiOQjXR010yqfSDmZL6gPpFU9rnmbayJ4DE4DS4vVcSNxf7hi9rdqditYIpv0bgwDati6IquLOmr-XzCzYZbUBXwXqz29lUrDLM-gdFlz2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/NZ6nx18tb9sDyP22U5_yyBmBjQ_8UCiR1rXcTBrZClmvZkgggJZyk7wH1akIjau5RkMbnv4iA8XoAKb6pFUHQisSuG9sMptZhYjzf2VuLhXJa0BPCjyFLK0E8ngUcWJ3tV4PSayyMYpHtIgXxiKxZWCUA0qh5dfBDam2Ghd0J5qi3wdNUWf30U2ULVhW5hiG?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/NgsjMF_001ZP-aefXFTxz-mPDdLh6U1E4ZMI_NXrw0Ez3WwKXuRjw8m9fUpBnmoQsp3ENmCbFKZ8Hvd0CUVCsoegcNZZNRWySttQ_77pW89_Iz_w6zjq-EG158d0sBKesWM_mKArdy7AptG60kiYLQbfHEcIoP-MWEtic_Rr6q2HjKP0zmRBi1hUTLzwSs_9?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/9SV7SwNUO8yXQZOj4lCoX_cM1EsWesIlcSB3VH7gc1YxTJWxtYcr3snxYB6LN1xnLkSgqiz6e_FyBwUavPZobOF_17CnIpGZI_9_UEs1rDHIrr-ZLjk8FDlWuqOXR2leyV4O4ApkYAdC-XfFVMcEr28Iw1SB4s3cV6GLLaFzG0By0n7Nc8MtovnZIfD6oWrk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/TE2ZdqwuxyvIvSFtBoYdLvpDa3bPexLFwtJGSUbprfyz-0gWLJSDBMt9dMulvu7Q5UbxD56oOExY8PWjrTAcDL31biIzhDn1sPDUQbIV8Bnh4X4Mwnrz9WoZEoS0FOwouHZ5Ew3k9BbKGo_Hhq2YmfQdT2-TE6wpZdQSiyX19i4O7eXC4b0aKjo_blWtv9S-?purpose=fullsize)

### Best resources to start

* [Learn Electronics Repair — GPU Repair Guide](https://www.youtube.com/watch?v=SmVdl8kew_4&utm_source=chatgpt.com) — probably the best single long-form starting point; it explicitly walks through resistance and voltage diagnosis. ([YouTube][1])
* [GPU Repair Wiki / community resources](https://www.reddit.com/r/GPURepair/?utm_source=chatgpt.com) — useful once you start posting actual measurements and symptoms.
* [GPU Doctor BoardView](https://gpudoctor.com/boardview?utm_source=chatgpt.com) — useful for learning to map schematic references onto physical PCB locations. ([GPU Doctor][3])

**So yes: buy broken Xianyu GPUs and just do it — but make every card a controlled debugging experiment, not a hot-air experiment.**

[1]: https://www.youtube.com/watch?v=SmVdl8kew_4&utm_source=chatgpt.com "The GPU REPAIR GUIDE.  How to fix GPU /Graphics card not detected. AMD Radeon or Nvidia - YouTube"
[2]: https://rc4bd.com/motherboard-schematic-and-boardview-guide/?utm_source=chatgpt.com "motherboardschematicandboardviewguide for Repair Technicians"
[3]: https://gpudoctor.com/boardview?utm_source=chatgpt.com "BoardView Viewer — Interactive GPU PCB Explorer | GPU Doctor | GPU Repair Experts"
[4]: https://www.cnblogs.com/maojun1998/p/16474059.html?utm_source=chatgpt.com "List of GPU Repair Resources (Schematics, Boardviews, Tutorials, Tools, Etc..) - maojun1998 - 博客园"
