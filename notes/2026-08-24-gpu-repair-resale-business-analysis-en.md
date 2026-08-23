---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Repair Resale Business Analysis
translated: false
type: note
---

Question: Is buying broken high-end GPUs, repairing them, and reselling better than doing customer repair work?

Answer:

I think the first model (**buy broken cards → repair → sell**) is much more scalable, but it is also more like a **hardware trading + repair business**. The second model (**customer brings card → repair → return**) is a service business with lower inventory risk.

For high-end NVIDIA cards (4090, 5090, RTX 6000 Ada/Pro, H100, etc.), the first model has some strong advantages:

### Model 1: Buy broken → repair → sell

Example:

* Buy broken RTX 4090: ¥3,000
* Repair cost:

  * components: ¥200–800
  * technician time: ¥200–500
* Total cost: ¥3,500–4,300
* Sell working: ¥6,000–8,000

Potential margin:

* ¥1,500–3,000/card

If you can repair 10 cards/month:

* profit maybe ¥15k–30k/month

If you scale:

* 50 cards/month:
* ¥75k–150k/month

The key advantage:

* You control the process.
* You can buy only models you understand.
* You can test, repair, grade, and sell with warranty.

This is closer to what GPU refurbishing companies do.

---

### Model 2: Customer repair

Example:

Customer brings RTX 4090.

You charge:

* diagnosis: ¥100–300
* repair: ¥500–2000

Problem:

You spend time communicating:

* "Can you repair?"
* "How much?"
* "Should I repair?"
* "It failed again"
* "Why is my card slower?"

Many customers don't understand hardware.

Your income is limited by labor hours.

A good technician can maybe repair 3–5 cards/day.

---

The difficult part of Model 1:

You need **diagnostic ability**.

Most broken GPUs are not simple:

Common failures:

1. VRAM failure

* bad memory chip
* memory channel dead

2. Power circuit failure

* MOSFET
* PWM controller
* short circuit

3. GPU core damage

* basically dead

4. BIOS/VBIOS issue

* very profitable because easy if you know it

5. Mining cards

* dirty
* modified BIOS
* high wear

You need equipment:

* thermal camera
* microscope
* multimeter
* oscilloscope
* DC power supply
* hot air station
* BGA rework machine
* VRAM tester (advanced)

---

The biggest opportunity IMO is not normal gamers.

Better customers:

### 1. AI companies / small labs

They buy:

* RTX 4090
* RTX 5090
* RTX 6000
* A6000
* H100

A repaired GPU with 30–90 day warranty is attractive.

### 2. Mining farms

They have hundreds of cards.

They don't care about beauty.

They care:

* cheap
* working
* fast replacement

### 3. AI training freelancers

Many people want cheap VRAM.

Example:

* RTX 3090 24GB
* RTX 4090
* used RTX 6000 Ada

---

For you specifically, because you understand AI/GPU infrastructure, I think this direction is more interesting than normal electronics repair.

You can combine:

```
GPU repair
    +
AI workstation building
    +
LLM consulting
    +
GPU rental
```

Example:

Customer:
"I need a local AI server."

You sell:

* repaired RTX 4090 x4
* workstation build
* CUDA setup
* vLLM deployment
* model optimization

The GPU becomes the entry product.

---

But I would not start with H100/5090.

Start with:

1. RTX 3090 24GB
2. RTX 4090
3. A6000/A5000
4. CMP mining cards

Reason:

* cheaper inventory
* easier testing
* more buyers

A broken H100 is a different world:

* expensive parts
* multilayer PCB
* very low tolerance
* enterprise buyers require certification.

My view:

**Buying broken GPUs, repairing, and reselling is the better business model.**
But the moat is not soldering. The moat is **diagnosis + sourcing + trust + warranty**.

A small shop that can say:

> "Tested RTX 4090, repaired, 90-day warranty, CUDA verified"

can sell much easier than a random used GPU seller.
