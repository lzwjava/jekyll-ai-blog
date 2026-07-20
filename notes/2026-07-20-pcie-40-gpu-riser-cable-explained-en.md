---
audio: false
generated: true
image: false
lang: en
layout: post
title: PCIe 4.0 GPU Riser Cable Explained
translated: false
type: note
---

Question: What is this PCI-E 4.0 GPU riser/extension cable, and what is it used for?

Answer:

This is a **PCIe 4.0 x16 riser cable (显卡延长线 / PCI-E延长线)**. It allows you to physically move the GPU away from the motherboard while keeping the PCIe connection electrically active.

![Image](https://images.openai.com/static-rsc-4/1KoRFOzCI7jvPqqvWIDP16m_VjdqJUgasi9IfND3wAS7d88_z_qyC-4KRaPfDqKCzW898xVxo2kBtqhy5rXaKK1wYjcfiKjZ-gvAuVji3nFICn5sAM2gChpf9zoZeY_n2S0kVcyoQmNzMJ-Ng4QvqWuiOYE1VYNjh_3VF7X1_rWcHjlQVIQnVweyz2yJiU9f?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/xumO9qZW0sCCVau5kYZqfZR38uhJWc9ngsQwXQBUS84gGHTtr_Pp22xpMC2yHZh5BSt37GlNxv84ZmDgQ1ym4wRFo5I_e0IwSGR-fRiLKzSO8ZkrIugSdE_JYQd-9KVr1IZAdvJ-Un4dwQAQfy_1lR_wNL8oGT5JcxRy3gf5duQVFPXJX3RdvhMxCGrwUJKZ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/DG-B5MOmTaIIj64xSuqUEXO2HhXeB0z0kAztyKFO5gt6XhvZNl17OokxJ3JJgFSyU3UDO2bQVTQN9EdhXqHeZu-wnbTBEJFq1qCudpwqYcrcPuPEIqSxMwYNH_CNfx3RM-6yOboxqqQrkwTr08Vr4UqTrHjgIvONuXc1lNUKb0ymOauY65Kb2-CylUWiCOsS?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/jHg-AoDf7BPPKfaWBtylxZZGFhNfX6ikF33a1BPylzqvKGyJTDU4WRipMVl2BC_1-OhA6XSPTuzG_imdJlXyiws8yxngVn6Q__SPBXnpAH3o_CmHejLGK0cJJ-AP1VrRZC3hPuXXD-oGDKQpsQWrU3TaEqrxvaQNcAgflQyuscFVEsnuKAFXGTHimf3ihT45?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/nLOHFiVPQwMeOlFcAwxUe6Yy6GAM4ECeu1Gh0qGQOyFa0njaQgW3h7QAhwK2c51OGgGKP6VYOWNr3a90xPB0HrSJgF1WTakaNjv6BN2fq9ek72fYATIKXaDOcmI52FNBrzagvlrqOcIVs8MbvrkXBSznHWwjox3brmfuk2ZJC6niqbsE4Ab9q-csAc5xZ78j?purpose=fullsize)

### What it does

Normally:

```
GPU
 |
PCIe x16 slot
 |
Motherboard
```

With a riser:

```
GPU
 |
PCIe x16 riser cable
 |
Motherboard PCIe x16 slot
```

The GPU can be mounted vertically or in a separate position.

Common uses:

* **ITX / SFF cases**

  * K39, K55, Ghost S1-style cases
  * GPU is too large to fit horizontally
* **GPU vertical mounting**

  * Showcase builds
* **Multi-GPU spacing**

  * Improve airflow between GPUs
* **GPU test benches**

---

### Meaning of the specs

#### PCIe 4.0

Supports PCIe Gen4 signaling:

* PCIe 4.0 x16 bandwidth:

  * ~32 GB/s bidirectional
* PCIe 3.0 x16:

  * ~16 GB/s bidirectional

Modern GPUs usually work fine with PCIe 4.0.

Example:

RTX 4070:

```
GPU PCIe interface: PCIe 4.0 x16
```

Using this cable:

```
RTX 4070
    |
PCIe 4.0 riser
    |
B760 motherboard PCIe 4.0 slot
```

should work normally.

---

### "双反向设计"

Means **double reverse design**.

In riser cable marketing, it usually means:

* connector orientation is reversed on both ends
* easier routing in small cases
* the cable does not need aggressive twisting

Example:

Normal:

```
Motherboard slot
     |
     |
GPU
```

Reverse:

```
Motherboard slot
     \
      \
       GPU
```

Useful for sandwich-layout ITX cases.

---

### "X16直通"

Important phrase.

It means:

> Full physical x16 connector passthrough

But note:

Physical x16 ≠ electrical x16.

Cheap risers sometimes have:

```
Physical x16
Electrical x4
```

because only 4 PCIe lanes are wired.

A good one:

```
Motherboard x16
       |
       |
Cable
       |
       |
GPU x16
```

All lanes connected.

---

### Length

This one:

* 18.5 cm
* 20 cm

is very short.

Good for:

* ITX builds
* vertical GPU mounting

Not ideal for:

* GPU farms
* multi-GPU servers

For AI rigs, people usually use:

* 30 cm
* 50 cm
* 60 cm

PCIe risers.

---

### For AI / multi-GPU usage

For your RTX 4070 / possible RTX 3090 style setups:

This cable is **not really for increasing GPU count**.

Example:

```
B760 motherboard
PCIe x16
 |
riser
 |
RTX3090
```

works.

But:

```
B760 motherboard
PCIe splitter
 |
5 GPUs
```

is a different problem.

You need:

* motherboard PCIe lanes
* PCIe bifurcation support
* enough PSU
* physical spacing
* cooling

---

### PCIe 4.0 riser reliability

Cheap risers can cause:

* GPU not detected
* random CUDA crashes
* training failures
* PCIe link downgrade

For AI training:

Check:

```bash
lspci -vv | grep -i lnk
```

Example:

Good:

```
LnkSta: Speed 16GT/s, Width x16
```

PCIe 4.0 x16.

Bad:

```
LnkSta: Speed 8GT/s, Width x4
```

PCIe 3.0 x4.

---

### For your use case

Given your interest in:

* RTX 4070
* RTX 3090
* multi-GPU AI workstation

This ¥70 cable is useful for:

✅ fitting a large GPU into a small case
✅ improving GPU spacing
✅ vertical mounting

Not useful for:

❌ adding more GPUs
❌ overcoming motherboard PCIe lane limits
❌ making consumer boards into 4/8 GPU AI servers

For AI multi-GPU, the more relevant hardware is:

```
EPYC motherboard
+
PCIe x16 slots
+
PCIe riser cables
+
blower GPUs
+
large PSU
```

like Gigabyte G292-Z20 / MZ01 platforms you were looking at.
