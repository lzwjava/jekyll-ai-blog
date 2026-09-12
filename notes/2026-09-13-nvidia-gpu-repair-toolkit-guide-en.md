---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nvidia GPU Repair Toolkit Guide
translated: false
type: note
---

Question: **Introduce this page: Levirepair’s “Nvidia MATS & MODS USB stick (with NVMT)” thread.**

Answer:

This is essentially a **community-maintained GPU repair / VRAM diagnostics toolkit** for NVIDIA cards, hosted on the Levirepair forum.

![Image](https://images.openai.com/static-rsc-4/0a9txzFEdY5EeOfS3rDyd3lkUCYUr98hgMBGUDdkL1AaXa3Dmsnuzda_WGAD4uo2pDFJtz2r5XREK3nYbU4En2ZC2mAI7rDHdm59tSwmUtapKUaRX52vwwbFqW0kwp-DI2NhdCyS5uIUBcFa2J9AZBOwf2BNpw7ThVHUaefJUWc-kpVKKdNczTRZvISjRZc2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/g_Iw6v4d9XzTa5U3YF1ZnJTIV2kLaN3iw1UPaTK-IMVk8KkBaka_lGehwepPEAYs7epfxGXH42PP8qZQY_hS-SmYr1f4nj9t18BZVsmAP4obXMLZEsrRdLgwDtoX3bEqgR14ccQGSz5XBB-x4zoPp5OSKeESgLNpcAG-JMhoMUN6iLJuQ0veSlZct60RvnrF?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/pDIgSFXpZk4j2xMVLQJmnNJ5ttkqU5OiLA_Ce56mnx1KSNEibBaelV-MxCyl02y4e1hZmXrFv0TtuqLwJd0Cf0KtbkndP3ekYRfdmlvgMUb1sU74cWM_iKKI0S0v4ej8sBGgYZUDNnHsZe-NxGYPP30a4X8e8n1NGhWIqWqTGpzZJlkzNiqcm6BWafmhkQw3?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/dS0rPB1ZVoGVMP4_6jbYNkp7GPOG-FzjmZa_1mV14T17pIJ9oFnS9j3LUMYYiOaxIkZwN7BfUWojvLKS89bjVvlFMRVqfkd_mtmANL58tjSYZ2Dr0AnAcQdZ_FFuRQ6gBvpv1Ym9a1yw_SYC0w9MFVP-D0dAZ7L8yO9zWdoOkyVKc7s7pYzQaGiwMqBUKVcu?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3gLxDoAXamQ-uJBYwuo0uPdlF1XnbbeRnVAzJ-o6a9Zdr-3Gxn1Hg5kH9nY_XzFST-4wq6QzyTItzjPO1qPf55qroy7N_hwgrKRxwIddzmq1cEhMB5eDbN7Nw0xubSFFpCP49gFFhmeXFg505IP3AfybBe6Jlrgegk6Iv_H31b0ZwxJUUBPoX6x2-965GBo_?purpose=fullsize)

### What it contains

* **MATS** — memory diagnostic/testing for NVIDIA GPUs. The thread describes it as testing GPU memory only. ([Levirepair][1])
* **MODS** — broader GPU testing, including GPU + memory. ([Levirepair][1])
* **NVMT** — NVIDIA-related low-level tooling, including VBIOS/device information and analysis commands. ([Levirepair][1])
* A **bootable Linux USB environment** containing different MATS/MODS versions for generations from older GT cards through RTX 40-series, with additional RTX 50-series notes. ([Levirepair][1])
* Practical **VRAM repair notes**, including GDDR6/GDDR6X memory layouts, Micron part compatibility, channel mapping, and temperature-based testing. ([Levirepair][1])
* Example diagnostic commands such as:

  ```bash
  mods
  mats
  mats -n 1
  nvmt ts > log.txt
  ```

  The thread also documents `modsinit` for testing a GPU as a secondary adapter when it cannot produce display output. ([Levirepair][1])

### Why it's interesting

The useful part isn't really the USB image itself. It's the **workflow around isolating bad VRAM**.

For example, the thread describes disabling individual memory channels with `-floorsweep`, then progressively combining channels to identify a failing section. It also includes GDDR6X mapping references and a MODS script for correlating VRAM temperature behavior with failures. ([Levirepair][1])

So I'd classify it as:

> **A field manual + bootable toolkit for NVIDIA board-level GPU diagnostics, especially VRAM failure analysis and repair.**

It is particularly relevant if you're doing **GPU board repair, GDDR6/GDDR6X replacement, NVIDIA memory-channel diagnosis, or reverse-engineering GPU test behavior**.

The thread is actively maintained: the page shows updates through **January 2026**, with earlier posts subsequently edited in 2026. ([Levirepair][1])

[Open the original Levirepair thread](https://levirepair.eu/infusions/forum/viewthread.php?thread_id=3&utm_source=chatgpt.com)

References:

* [Levirepair — Nvidia MATS & MODS USB stick (with NVMT)](https://levirepair.eu/infusions/forum/viewthread.php?thread_id=3&utm_source=chatgpt.com) 
* [Levirepair GPU repair forum](https://levirepair.eu/infusions/forum/index.php?forum_id=3&viewforum=&utm_source=chatgpt.com) 

[1]: https://levirepair.eu/infusions/forum/viewthread.php?thread_id=3 "Nvidia MATS & MODS USB stick (with NVMT): Forum - Levirepair"
