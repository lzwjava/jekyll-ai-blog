---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD CrossFire Bridge Cable Overview
translated: false
type: note
---

Question: What is this AMD CROSS FIRE cable?

Answer:

This is an **AMD CrossFire bridge cable** (also called a **CrossFire interconnect cable**). It is a small physical link used to connect **two AMD Radeon GPUs** for multi-GPU rendering.

![Image](https://images.openai.com/static-rsc-4/CRHxU-qGC5CAZoHeTkh9Ek-j_JxfL7qAcL8q2-DfciNdZ1EDtUpYnPcmH9CQQi0p3HHI7E4lXb4pxmqiSRx8kTD2U_wIwEimRpokdBJB-jfSVJTv7u4R-SFOoMcwf0NWEZxdgnsnF5kHXGJvUNQyiGqxc-_xe45bDYkITV6PjhQHETMasK2MJmnOYOG7Mqml?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/MKx8xLOhmd1GpEML-r8jxszVvjg8jkpzyoytbC01sVQ6s16I8kQCBMmiE24hg7IXWgpQ1x80ODmd0wmqz0mD-JlI0M0_mcfKFCTJmf7yZ62SUpgb743qSgz3c_nHtEQ4T5ZoDymdqhvfq9ucM71_NiPKtOPLwvYba_d5hD1fJ86FhFAON3FtQroZGW2GrIy6?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/lbNKDIlqlxVRpWHS92a2D1yHhVpTu-prtSxxdC-G3A9guzzO1BRUu6xB4X2NFBRPYfurfIgVdARdk6_Kz5l9__b6GfaHwaXs6P-L69Mfa8P44EevsC7iaQoAgmgIth86d2MixRE33o33OW5Q-uHwIxClQCljnCuNdzakeUh11fDCApMF-DILcJfCTJpXMfot?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/bXiOq6NqfjTLPSE79SL7wafx3RakUKbqflxxR2k_GhVUOkRkYV_VepkMMRrgz18X8aooCZU7rIgWzeIyyEYAsvVEUcUEF1-U4HM6WQrtFERW9kIFEbrcnGFfqWAiva1Y3yJyCkFwwA2wfRkWbm7Hn-11J6tBT1JmpwPphLJb2lM5vFsM6vt5i-OO9st9CeP1?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/s0UVSTkGWsKnGzElWwCWaFDMoOWAX5shyV0SOP12nfpN5zcZs_j-5SMuqKuZRRZhrd4vLjdr5yQRkReaGBJqq18PJDeC-qN3wWu_oY5XaMWygOzAeCC20sCu_PX6KnrXTg2pC3cELylMhMuzFJkgW9piRyVL1kYR-jRRbshF1VlPd_8elr3Or6JZ5JNvLP-I?purpose=fullsize)

### What it does

Older AMD Radeon cards had a small connector on the top edge of the GPU:

```
GPU 1  ===== CrossFire Bridge =====  GPU 2
```

The cable allows the two GPUs to exchange some rendering data directly.

Typical use cases:

* Gaming multi-GPU (CrossFire)
* Older professional workloads
* Some OpenCL workloads

### Important: it is mostly obsolete now

Modern AMD GPUs generally **do not use CrossFire bridges**.

Examples:

| GPU                      | CrossFire bridge?                  |
| ------------------------ | ---------------------------------- |
| Radeon HD 7000 series    | Yes                                |
| Radeon R9 280/290        | Usually yes (some use PCIe only)   |
| Radeon RX 400/500        | Mostly no bridge, "XDMA" over PCIe |
| Radeon RX 5000/6000/7000 | No CrossFire support               |

AMD abandoned CrossFire for gaming around the Vulkan/DX12 era because modern APIs allow the application itself to manage multiple GPUs.

### Compared with NVIDIA SLI/NVLink

|                | AMD CrossFire       | NVIDIA SLI          |
| -------------- | ------------------- | ------------------- |
| Bridge         | CrossFire cable     | SLI bridge          |
| Purpose        | Multi-GPU rendering | Multi-GPU rendering |
| Modern support | Almost dead         | Almost dead         |
| AI training    | No                  | No                  |
| VRAM pooling   | No                  | No                  |

For AI/LLM work:

```
2 × RTX 3090
```

does **not** use SLI/NVLink for PyTorch training in most cases.

You normally use:

```python
torch.distributed
DistributedDataParallel (DDP)
NCCL
```

The GPUs communicate through PCIe/NVLink automatically.

### For your GPU experiments

Given your interest in RTX 3090 / Tesla / MI-series / multi-GPU training:

This cable is basically **a collector item today**. It has almost zero value unless you are restoring an old AMD gaming machine.

A dual AMD GPU setup like:

```
R9 290 + R9 290
HD 7970 + HD 7970
```

could use it, but a modern AI workstation would ignore it.
