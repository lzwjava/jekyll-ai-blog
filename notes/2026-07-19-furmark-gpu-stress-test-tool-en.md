---
audio: false
generated: true
image: false
lang: en
layout: post
title: FurMark GPU Stress Test Tool
translated: false
type: note
---

**Question: what is FurMark 1.39 GPU test tool?**

**Answer:**

FurMark is a **GPU stress-test / burn-in tool**. It renders a very heavy "furry donut" OpenGL scene to push the GPU close to maximum load, mainly to test:

* GPU cooling system
* thermal behavior
* power stability
* GPU core stability
* overclock/undervolt stability
* used GPU condition when buying second-hand cards

FurMark 1.39.x is one of the older generation versions from Geeks3D. Version 1.39.0 was released in 2025; 1.39.3.0 is a later 1.39 branch build. ([MajorGeeks][1])

The basic idea:

```
FurMark
   |
   v
generate extreme GPU workload
   |
   v
GPU core -> 99%
VRAM -> active
Power -> near TDP limit
Temperature -> maximum
   |
   v
observe:
  - crashes?
  - artifacts?
  - overheating?
  - clock throttling?
```

It is called a **"GPU burner"** because it intentionally creates an unusually heavy thermal load. ([MajorGeeks][1])

---

### For buying used RTX 3090 / 3060 / 7900 XT (your case)

FurMark is actually useful.

Typical second-hand test:

1. Run GPU-Z first:

   * check GPU model
   * VRAM size
   * BIOS
   * PCIe link

2. Run FurMark:

```
Resolution: 1920x1080
MSAA: 0x
Duration: 10-20 minutes
```

Watch:

### Good RTX 3090 example

```
GPU usage:       99%
Power:           350W+
Temperature:     70-85°C
Clock:           stable
Artifacts:       none
Driver crash:    none
```

### Bad card signs

```
temperature:
95°C+

clock:
1800MHz -> 900MHz

screen:
colored dots
flashing polygons
black screen

driver:
"NVIDIA driver stopped responding"
```

---

### But FurMark is not a real AI workload test

For your LLM/training use case:

FurMark tests:

```
graphics pipeline
OpenGL
shader load
thermal limit
```

It does **not** test:

```
CUDA
Tensor Core
VRAM ECC behavior
PyTorch stability
long training stability
```

For AI GPU checking, I would combine:

### 1. VRAM test

```
python -m pip install gpu-burn
gpu_burn 600
```

or

```
memtest_vulkan
```

### 2. CUDA test

```python
import torch

x = torch.randn(
    (20000,20000),
    device="cuda"
)

for i in range(100):
    y = x @ x
    torch.cuda.synchronize()

print("OK")
```

### 3. Real AI workload

Example:

```
vllm serve Qwen3-32B
```

or

```
torchrun train.py
```

Run several hours.

---

For your second-hand GPU shopping:

* **FurMark + GPU-Z + CUDA test** is a good minimum.
* For RTX 3090 specifically, also check:

  * memory temperature (GDDR6X can hit 100°C+)
  * fan noise
  * power connector condition
  * whether BIOS was modified for mining

FurMark only tells you "the card can survive a torture load"; it does not guarantee healthy VRAM. ([TechPowerUp][2])

References:

* FurMark GPU stress testing overview ([MajorGeeks][1])
* FurMark version history / downloads ([TechPowerUp][2])

[1]: https://www.majorgeeks.com/files/details/furmark.htm?utm_source=chatgpt.com "Download FurMark 1.39.3.0 - MajorGeeks"
[2]: https://www.techpowerup.com/download/furmark/?utm_source=chatgpt.com "Furmark 2.9.0 Download | TechPowerUp"
