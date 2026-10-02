---
audio: false
generated: true
image: false
lang: en
layout: post
title: "P100: Budget Middle Ground GPU"
translated: false
type: note
---

Question: **How does the Tesla P100 compare with the M40 and the T10 for your cheap-LLM/GPU-lab use?**

Answer: **P100 is a very interesting middle ground, especially the 16GB PCIe version.** Its biggest feature is not raw VRAM capacity but **732 GB/s HBM2 bandwidth + Pascal compute capability 6.0**.

### P100 16GB PCIe

![Image](https://images.openai.com/static-rsc-4/A9zAO6NkPOhwzH6U0tDcrgbHLUVmTXHPcesk9-OTFM4IsLH2Wix3UVcbXQkV1gv9iBtJdZWv7thjr8tZSytKKAmi084s_w5U4bg-wvMn_1qN0w6e_nVjB8u3hIe8UIlHgce-MhX4Q7PjkJxP5Mxhnny2itx7jfROYpq6Tn2pvYo-Z9Y8mG_reWuri0x1XiKS?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/R0rv-32wdtLtgRiO_L8x4jeE11lYqb-jqqnMuMLU0D_An1oj1Ixs45m3j0TQ-BPEB875UoxHY2XedAzcTF4l-bxzOJ-H7trwJBFxrvqBFzW6_xcOblOW8J0czE-a5AIPAbrHiD9VejfxQx0oUF2KJxXYPgPyuKcjZoyOYG7XKKcQaGIsjBfNbglbbYdOxEhO?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/1BOKJWq4-z4gpHXXmK9p71acVp9d8HE7ufUOGXKzi78fxippGHu2ml97myKd41IXTXJD9V9ll8w9u5q71Wk4-rglMnA2en1jNxljPnsp68tD3cwBzVHq2DVPkOt4G4HcNHk6DebQq2lHW3ePyRATO_NpD7s4SCF1TGwZlZjcBvh6L5nanCeHSibRY41k7kzs?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/V_STFlI__dFZvDQrsYGY8-oe6xsp7gfLbOjMHDu9w2Ab_kBTp80PKoUW4PbaRJKXPg5pqHD0uVXbBCVqxbCdaoM85zI7vv-3FAJMOxEUY7-GYa9L_6AtgnSIej1aT81b-2vnMXl0rAzXlvlcN7zOZ1xZkG5o_6_PU4vMouMZwbtFTHTZ7K3MpM1khytNcyfs?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Bk4dROXKwwb8mSAbl05XA5ZAAdLYb94ckPmdB-yM9D6PdrKGxJAG9Q2-SiibySEzOg8mY1IZ6vu-gbIhPDA5YUW-ogb0Egnt89pxzIQrcZ92yKMd9iO0Jm2H6qTUz2zZOHesOUYANTPZsXfQ5qZVF40PNX2mwMlN40Zkne3RmegQRHQejPiN22H0NfavWgwM?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/qj5vb3CQAkKYV4y8Er9EeWBkAMmJkTg82hcIBvDt1g_zwAyoJWzRcaydH1mxSPIymVDxogH_5BajAy9crmcslGcTBVkb9_8nAsnTTNG0Tw_RGNTNRTC2LkpOxIlREyA-bx4NBlBOQAn1MS9W7tgLE9mQmLUyek5BuWm5Sv_B67lu44Qpjx3ugeDf4BDfvLit?purpose=fullsize)

The important specs are:

```text
Tesla P100 PCIe 16GB

Architecture       Pascal / GP100
CUDA cores         3,584
VRAM               16 GB HBM2
Memory bandwidth   732 GB/s
FP32               9.3 TFLOPS
FP16               18.7 TFLOPS
FP64               4.7 TFLOPS
Compute capability 6.0
PCIe               Gen3 x16
TDP                250 W
ECC                Yes
```

NVIDIA confirms the 16GB PCIe P100 uses HBM2 at up to 732 GB/s and provides 9.3 TFLOPS FP32 / 18.7 TFLOPS FP16. ([NVIDIA][1])

### The three cards

|                    | **M40 24GB** |  **P100 16GB** | **T10 24GB*** |
| ------------------ | -----------: | -------------: | ------------: |
| Architecture       |      Maxwell |     **Pascal** |        Turing |
| Compute capability |          5.2 |        **6.0** |          ~7.5 |
| VRAM               |     **24GB** |           16GB |      **24GB** |
| Memory             |        GDDR5 |       **HBM2** |         GDDR6 |
| Bandwidth          |     288 GB/s |   **732 GB/s** |     ~624 GB/s |
| FP32               |    ~7 TFLOPS | **9.3 TFLOPS** |    ~14 TFLOPS |
| Tensor Cores       |           No |             No |       **Yes** |
| TDP                |         250W |           250W |         ~260W |

M40's official figures are 3,072 CUDA cores, 24GB GDDR5, 288 GB/s and compute capability 5.2. ([NVIDIA Developer][2])

So the interesting thing is:

```text
M40
24 GB
288 GB/s
   ↓

P100
16 GB
732 GB/s
   ↓

T10
24 GB
~624 GB/s
```

### For LLM inference

The P100's **732 GB/s** is excellent for its age.

For a memory-bandwidth-bound operation such as roughly:

```python
# simplified decode intuition

for token in tokens:
    for layer in model:
        weights = load_weights_from_vram()
        x = matmul(weights, x)
```

the GPU repeatedly streams model weights from VRAM.

Therefore:

```text
P100:
16 GB / 732 GB/s

M40:
24 GB / 288 GB/s
```

The P100 can move data through its memory subsystem **~2.5× faster** than M40.

That's why a P100 can feel surprisingly fast despite having only 16GB.

### But P100 has a serious modern-software problem

This is the part I'd care about in **2026**.

P100 is:

```text
Pascal
  ↓
sm_60
  ↓
CUDA Compute Capability 6.0
```

NVIDIA's current legacy GPU table still identifies P100 as CC 6.0. ([NVIDIA Developer][3])

Modern CUDA support is moving away from Pascal. In particular, CUDA 12.7 dropped native support for Pascal GPUs. ([GPU Database][4])

So you can end up with:

```text
P100
   ↓
excellent hardware
   ↓
old CUDA architecture
   ↓
modern PyTorch / CUDA / kernels
can become annoying
```

This is **much better than M40**, but still nowhere near the convenience of Turing/Ampere.

### P100 vs M40 specifically

For your GPU repair/lab project, I'd think of them like this:

**M40 24GB**

```text
+ 24GB
+ extremely cheap
+ useful for old CUDA experiments
+ huge VRAM for its price

- only 288 GB/s
- CC 5.2
- increasingly painful software compatibility
- no Tensor Cores
```

**P100 16GB**

```text
+ 732 GB/s HBM2
+ CC 6.0
+ much better FP64
+ much better memory subsystem
+ originally designed specifically for HPC/AI
+ 250W
- only 16GB
- passive cooling
- old Pascal software ecosystem
- no Tensor Cores
```

For **LLM inference**, I'd generally rather have a P100 than an M40 if the prices are close.

But if your model **needs >16GB**, the M40's 24GB becomes decisive.

### And then T10 changes the equation

If your T10 listing really is a **24GB Turing TU102-based card**, then I'd rank the hardware characteristics like:

```text
                    VRAM      BW       Architecture
M40                 24GB      288      Maxwell
P100                16GB      732      Pascal
T10                 24GB      ~624     Turing

                                    ↓
                            much newer CUDA
                            + Tensor Cores
```

So for your particular goal of building a cheap **LLM/GPU experimentation lab**:

```text
T10 24GB       ← very interesting
P100 16GB      ← very interesting if cheap
M40 24GB       ← primarily a cheap-VRAM experiment card
```

One particularly interesting card you should also look at is **Tesla P40 24GB**. It is Pascal **6.1**, 24GB GDDR5 and ~346 GB/s; unlike P100, it gives you **24GB** while being considerably newer than M40. ([NVIDIA Developer][3])

For your use case, **P40 24GB vs P100 16GB vs T10 24GB** is probably the more useful three-way comparison than M40 vs P100.

[1]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/nvidia-tesla-p100-PCIe-datasheet.pdf?utm_source=chatgpt.com "NVIDIA
® TESLA
® P100
GPU ACCELERATOR
World’s mo"
[2]: https://developer.nvidia.com/blog/accelerating-hyperscale-datacenter-applications-tesla-gpus/?utm_source=chatgpt.com "Accelerating Hyperscale Data Center Applications with NVIDIA M40 and M4 GPUs | NVIDIA Technical Blog"
[3]: https://developer.nvidia.com/cuda/gpus/legacy?utm_source=chatgpt.com "Legacy CUDA GPU Compute Capability | NVIDIA Developer"
[4]: https://gpus.axiomgaming.net/gpu/tesla-p100-pcie-16-gb?utm_source=chatgpt.com "Tesla P100 PCIe 16 GB Specifications - NVIDIA GPU Database"
