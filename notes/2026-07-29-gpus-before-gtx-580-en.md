---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPUs Before GTX 580
translated: false
type: note
---

Question: What GPUs existed before the NVIDIA GTX 580?

Answer:

Before the **NVIDIA GeForce GTX 580 (2010)**, the GPU landscape was mostly about graphics and early CUDA computing. The GTX 580 was the peak of NVIDIA's **Fermi** generation, but it came after several important generations.

![Image](https://images.openai.com/static-rsc-4/DmevK_vQrcZm9CTO35MiBcb1OWw-i8jWLUkcOC3zc5j4texXDGCX6TLOcI-ssnOoju_cU2oOsl-7J11SFwnVL94C8New4QvG43cG4bkWFAYzeY_AfyhjBcq5hEjfpj-yJS5scNkTON5rzArq2sqvOTjN0wzUfqvhAjTGq9X5MuaBRvJq_vdRUZnp-YlA8fbE?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Q2SGf2fm382wjq2wWxSBxbpVJzrAiZdsptDRJzSEf3lDOS06MHHR3wSWY0t6ujKbslh5LA9TE5EbiiABB2S519OsduYzXzRDVOsvZKlOpQ4O8hLETqW_9Y6LNJWksjM8LRkHrm5T9-SLcXL2P-dRzSZRjvEjTZaQb2YLi7RO0hZUQz9HteiWSia8e8MKcRRq?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/S5f6FzwbzO72SG3Djl4n9ye6Hmmn8oy3XEYnluw_d-tf6PNklYX6YnjtFhpPiEJ5n5TUMOfbGTDkH1GknzBWV8kU3glDrgaUcyWfhRO6w3cocJMpvhNxBIp3ReJLJ0jlKk9BhH9r2-DRe2u6QZ_9mXuAsbyzNnmuILH4nwFgRMq-_GZBA8jH9dSAhZqQctXi?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/KiiQuOzE7Pb2hWVcRES3fD80a1sk7hzeaBZGaVFC4v_oT9tLeJ1gSVre5uOqRcfM03vH739S8TqyPYyzRsrONArvH21cxqUuSFfM76tLFOFtqXcNCEXpvrqEG0ZBeGQXSiD1l6bOc0KXUefyXsnPSLc20hdlPeDgxlzUg8LTzsg8gws8ccJsuhuGEJX0M9dz?purpose=fullsize)

## NVIDIA GPU timeline before GTX 580

| Year | GPU              | Architecture  | CUDA cores |  VRAM | Importance                  |
| ---- | ---------------- | ------------- | ---------: | ----: | --------------------------- |
| 2006 | GeForce 8800 GTX | Tesla         |        128 | 768MB | First CUDA-era GPU          |
| 2008 | GeForce GTX 280  | Tesla         |        240 |   1GB | Early GPGPU                 |
| 2009 | GeForce GTX 285  | Tesla refresh |        240 |   1GB | Popular compute card        |
| 2010 | GTX 480          | Fermi         |        480 | 1.5GB | First true CUDA compute GPU |
| 2010 | **GTX 580**      | Fermi refresh |        512 | 1.5GB | AlexNet-era GPU             |

---

## The important one: GeForce 8800 GTX (2006)

NVIDIA GeForce 8800 GTX was a historic GPU.

Why?

Before this:

```
GPU = fixed-function graphics pipeline
```

After G80 architecture:

```
GPU = programmable parallel processor
```

NVIDIA introduced:

* CUDA (2007)
* unified shader architecture
* general-purpose GPU computing (GPGPU)

Many researchers started asking:

> "Can we run neural networks on this massive parallel chip?"

---

## The GPU evolution toward deep learning

### 1. Pre-CUDA era (before 2006)

GPUs were mainly:

```
CPU
 |
 +-- GPU
      |
      +-- triangles
      +-- pixels
      +-- shaders
```

Programming was difficult.

---

### 2. CUDA era begins (2006-2010)

Example:

GTX 280:

```
240 CUDA cores

each core:
    small floating point unit

parallel:
    thousands of threads
```

Researchers could write:

```cpp
kernel<<<blocks, threads>>>(data);
```

and run scientific workloads.

---

### 3. Fermi generation (2010)

GTX 480 / GTX 580 were designed more like compute accelerators:

```
Fermi GPU

SM
 |
 +-- CUDA cores
 +-- shared memory
 +-- L1 cache
 +-- double precision units
```

This was closer to today's AI GPUs.

---

## Did early deep learning use GTX 280/285?

Yes.

Before AlexNet, groups including Hinton's lab were already experimenting with GPUs.

Examples:

* CUDA implementations of neural networks
* GPU-accelerated convolution
* restricted Boltzmann machines (RBMs)

Hinton's group used GPUs around 2009–2011 to make deep learning practical.

But AlexNet was the moment where:

```
GPU + CNN + huge dataset + ReLU
=
modern deep learning
```

---

## Interesting comparison with your RTX 4070

Your RTX 4070:

```
Ada Lovelace
2023

5888 CUDA cores
12GB VRAM
~29 TFLOPS FP32
```

GTX 580:

```
Fermi
2010

512 CUDA cores
1.5GB VRAM
~1.5 TFLOPS FP32
```

The RTX 4070 is roughly:

* ~20× FP32 compute
* 8× VRAM
* much better memory efficiency
* dedicated Tensor Cores for AI

A single consumer RTX 4070 today is far beyond the entire AlexNet training setup.

The surprising part is not that AlexNet used weak hardware — it is that they discovered the right scaling law before anyone else:

```
more data
+ bigger neural networks
+ GPUs
+ better optimization
=
deep learning revolution
```
