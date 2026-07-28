---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GTX 580: The AlexNet GPU"
translated: false
type: note
---

Question: Intro to NVIDIA RTX 580, and did Ilya Sutskever and Hinton use it for AlexNet?

Answer:

There is no NVIDIA **RTX 580**. You probably mean **NVIDIA GeForce GTX 580** (released in 2010). It was one of the GPUs that made the AlexNet breakthrough possible.

![Image](https://images.openai.com/static-rsc-4/7kCeJNL-l4Rk80tBXjG8Rce7M_EtJYvsz6Qbn-AXxG0VAL23mKi7oMycJ44QtUjtULEDmdSlrV-OBPDMcYbWVlupUPdONIZDWyVo_qN3v-MnTUZSnF1ypNPb7el6I_DHoq2ZYgmCyYV3Jx8OOqKdxz_1Oqqy9Lq0RjMXnL3BuYAJvHg6JXKp8YMZPD08bKA4?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Tnq9y-bzdeo_XmDERupKdqMobrjVlSD8ofFyAVxV_Zjp2iWcV8UFeBbcc6VWvR-2jk5MSsLQ0-d88HS5dqg9N2yG5Frt4-9mqaZ7Lcc0jJDbk9yd_T7RSNWPjOCpxh7-jSu1qwVBmTOPvHGrdlTVNXKUHuS82_sapb1N_Rj2SpaQ-rFVUOhArUb3sJMG2Qcb?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/6E3X1mijYM1CfmhLDH0kcJ_KIW7rtECq0CMsYKyOBU2wIx8X7XAr4OA1TOLRbAoGxjr5t2CBk8uimFOpV4p4Fx0AdfqyfIuP8a3n1srG-FKcMjsBjy_JAvYD27wlwEhAnc9VIiQ-9WpJQKzSvuymre2UADX7djyKOdj_u-bpOX9zBh8qO00-jOlOqGvown8O?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/zwGFLcMtny7ZQvQS9MuJ9tJYhBdL8j6t559675XQ7XZA2sk8qN4hD-W63DxVyRz2JOorPR1Szj7zlpEYi5yr0A7GCLQFJGxOPti6KTFImv0s_958NaM5wuID3rvH9wdy4ab3QqAV4Z41rWLk57Ip7v95F6Ja6Bflwgoai5GdInPZ3InT2Dk6SxRn6mrx2Pde?purpose=fullsize)

The **GeForce GTX 580**:

* Architecture: **Fermi**
* Release: November 2010
* CUDA cores: **512**
* VRAM: usually **1.5 GB GDDR5**
* Memory bandwidth: ~192 GB/s
* FP32 compute: ~1.5 TFLOPS
* Power: ~244W TDP

By modern standards it is tiny:

* RTX 4070: ~29 TFLOPS FP32, 12GB VRAM
* RTX 4090: ~83 TFLOPS FP32, 24GB VRAM

But in 2012 it was a monster for deep learning.

---

### Did Ilya Sutskever and Geoffrey Hinton use GTX 580 for AlexNet?

Yes, but the exact GPUs were **not RTX 580**. AlexNet was trained on **two NVIDIA GTX 580 GPUs**.

The famous 2012 paper:

> "ImageNet Classification with Deep Convolutional Neural Networks"

by:

* Alex Krizhevsky
* Ilya Sutskever
* Geoffrey Hinton

used:

* 2 × GTX 580
* 3GB total GPU memory (1.5GB each)
* CUDA
* custom GPU parallelization

The model had:

* 60 million parameters
* 650,000 neurons
* 5 convolution layers
* 3 fully connected layers

The clever trick was splitting the network across two GPUs.

---

### Why was GTX 580 enough?

Because AlexNet was small by today's standards.

A simplified comparison:

| Model          | Parameters | GPU memory needed |
| -------------- | ---------: | ----------------: |
| AlexNet (2012) |        60M |              ~3GB |
| GPT-2 124M     |       124M |              ~GBs |
| Llama 7B       |         7B |       ~14GB+ FP16 |
| GPT-4 class    |    unknown |              huge |

The breakthrough was not raw GPU power. It was realizing:

```
CNN + ReLU + dropout + GPU CUDA
        ↓
train much larger networks
        ↓
beat traditional computer vision
```

---

### Interesting historical connection

Before AlexNet, GPUs were mostly for graphics.

AlexNet showed:

```
GPU
 |
 +-- graphics
 |
 +-- scientific computing
 |
 +-- neural network training
```

This directly created the modern NVIDIA AI business.

Jensen Huang's famous quote:

> "The more GPUs you sell, the more AI gets created."

came from this transition.

The RTX generation came much later:

* GTX 580 → Fermi (2010)
* GTX 680 → Kepler (2012)
* GTX 980 → Maxwell (2014)
* GTX 1080 → Pascal (2016)
* RTX 2080 → Turing (2018)
* RTX 4090 → Ada Lovelace (2022)

Your RTX 4070 today has roughly **20× the compute** and **8× the VRAM** of the two GTX 580s that powered the AlexNet revolution.
