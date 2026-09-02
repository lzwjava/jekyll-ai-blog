---
audio: false
generated: true
image: false
lang: en
layout: post
title: MATS TServer 2in1 pmfx diagnostic image
translated: false
type: note
---

## Question

`Mats-4090_Tserver-6900_2in1.pmfx` — is this the newer **MATS/TServer GPU VRAM diagnostic tool**, and what does the `.pmfx` file mean?

## Answer

Yes. The filename strongly suggests it is a **combined bootable/test image containing both NVIDIA MATS and AMD TServer**, specifically aimed at newer GPUs:

```text
Mats-4090_Tserver-6900_2in1.pmfx
│         │          │
│         │          └── 2-in-1 image
│         └───────────── TServer for AMD / 6900-class cards
└────────────────────── MATS for NVIDIA / RTX 4090
```

The important distinction is:

### 1. MATS = NVIDIA VRAM diagnosis

MATS is a low-level NVIDIA memory test. It writes/reads patterns through the GPU's framebuffer-memory interface and reports errors by **FBIO subpartition/channel**, for example:

```text
FBIOA0   0   0   0
FBIOA1   0   0   0
FBIOB0   0   0   0
FBIOB1   0 560   0   <-- error
FBIOC0   0   0   0
...
```

This is extremely useful for GPU repair because an error such as `FBIOB1` can help you identify **which VRAM chip/channel to investigate**. ([Бытовая техника для дома -][1])

But importantly:

> **MATS reporting a VRAM-channel error does NOT automatically mean the VRAM chip itself is bad.**

The fault can also be:

```text
VRAM chip
   ↓
PCB traces / solder
   ↓
power / signals
   ↓
GPU memory controller
```

A repair reference explicitly warns that MATS errors can originate from the GPU's memory controller or missing signals/voltages to the memory. ([ААНТ КОНТАКТ][2])

### 2. TServer = AMD equivalent

TServer is used for AMD cards. A common memory diagnostic command is:

```bash
./tserver -boardtest=memfa
```

and produces a memory-failure analysis log. ([PPT Online][3])

So a package advertised as:

```text
MATS + TServer
```

is basically a **GPU repair technician's diagnostic environment** for both NVIDIA and AMD.

### 3. Why `4090` and `6900`?

Likely the package was assembled around support for:

```text
NVIDIA:
RTX 4090
       ↓
     MATS

AMD:
RX 6900 XT / 6900-class
       ↓
    TServer
```

The exact supported GPU list depends heavily on the **MATS/MODS build and GPU architecture**. You should not assume that because a filename says `4090`, every Ada card or every 40-series GPU is correctly supported.

This matters a lot: using an inappropriate MATS/MODS version can produce incorrect results. ([ААНТ КОНТАКТ][2])

### 4. What is `.pmfx`?

This is the interesting part.

`.pmfx` is **not the normal MATS executable itself**. It appears to be a packaged/boot-image format used by these prebuilt GPU-diagnostic USB environments.

Think of it more like:

```text
Mats-4090_Tserver-6900_2in1.pmfx
                 │
                 ▼
        bootable diagnostic image
                 │
        ┌────────┴────────┐
        ▼                 ▼
      NVIDIA             AMD
       MATS             TServer
        │                 │
        ▼                 ▼
      VRAM test         VRAM test
```

This is why you'll see people distributing huge "MATS/MODS/TServer" USB images rather than just a single `mats` binary. There are known multi-partition bootable images containing NVIDIA MATS/MODS and AMD TServer environments. ([RMPrepUSB][4])

---

### For your GPU-repair experiments

This is **exactly the kind of tool you want**.

For example, your workflow for a suspected RTX 4090 VRAM problem could become:

```text
RTX 4090
   │
   ├── visual inspection
   │
   ├── resistance-to-ground measurements
   │
   ├── power rails
   │
   ├── PCIe initialization
   │
   ├── MATS
   │      │
   │      └── FBIO? error
   │
   ├── map FBIO channel → physical VRAM chip
   │
   ├── inspect VRAM power / CLK / CMD / DQ
   │
   └── decide:
          VRAM chip?
          solder/BGA?
          PCB?
          GPU memory controller?
```

That's much closer to **actual board-level diagnosis** than simply running FurMark/3DMark.

One useful detail: MATS can be configured to test a specified amount of VRAM, e.g. `-e 20`, or a percentage with `-c`; some environments use a small amount for a quick test and increase it for deeper testing. ([PC1][5])

If you **have the actual `Mats-4090_Tserver-6900_2in1.pmfx` file**, upload it here and I can inspect its structure and tell you **what's inside, how to boot it, which MATS version it contains, whether it really supports 4090, and how to use it to diagnose a dead 4090 step-by-step**.

### References

* [MATS/MODS GPU memory testing explanation](https://xn----9sbnsmbfcfrsidc.xn--p1ai/forum/viewtopic.php?p=7216&sid=43dfddeafc5ecabe5df3f628751b0a85&utm_source=chatgpt.com)
* [MATS/TServer diagnostic commands and examples](https://rmprepusb.blogspot.com/2022/06/run-nvidia-graphics-memory-tests-from.html?utm_source=chatgpt.com)
* [NVIDIA MATS memory-test presentation](https://en.ppt-online.org/632320?utm_source=chatgpt.com)

[1]: https://instrukciya.top/2023/06/27/proverka-pamyati-videokarty-nvidia-na-oshibki-mats/?utm_source=chatgpt.com "Проверка памяти видеокарты nvidia на ошибки mats - Ремонт и установка крупной бытовой техники"
[2]: https://xn----9sbnsmbfcfrsidc.xn--p1ai/forum/viewtopic.php?p=7216&sid=43dfddeafc5ecabe5df3f628751b0a85&utm_source=chatgpt.com "Скачать MATS MODS: Диагностика видеокарт NVIDIA. Тест видеопамяти Nvidia. Пошаговая инструкция для теста vram - Форум по ремонту ноутбуков, моноблоков, мобильной электроники"
[3]: https://en.ppt-online.org/632320?utm_source=chatgpt.com "VGA Test 2019 - online presentation"
[4]: https://rmprepusb.blogspot.com/2022/06/run-nvidia-graphics-memory-tests-from.html?utm_source=chatgpt.com "RMPrepUSB, Easy2Boot and USB booting: Run nVidia/AMD GPU graphics memory tests from an Easy2Boot drive"
[5]: https://pc1.pp.ua/infa/test-pamyati-videokarty-programmoj-mats?utm_source=chatgpt.com "Мастер Ломастер - Тест памяти видеокарты программой MATS"
