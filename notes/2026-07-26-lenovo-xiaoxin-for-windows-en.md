---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lenovo Xiaoxin for Windows
translated: false
type: note
---

Question: Should I install Windows on a Lenovo Xiaoxin or a MacBook Pro 2017?

Answer:

For **Windows**, use the **Lenovo Xiaoxin**. It is the better Windows machine.

Comparison:

|                   | Lenovo Xiaoxin       | MacBook Pro 2017      |
| ----------------- | -------------------- | --------------------- |
| Windows support   | ⭐⭐⭐⭐⭐ Native         | ⭐⭐⭐⭐ Boot Camp        |
| Drivers           | Excellent            | Good but aging        |
| CPU               | Newer Intel/AMD      | Intel 7th gen         |
| Battery           | Usually better       | Battery may degrade   |
| SSD               | Faster PCIe NVMe     | PCIe SSD              |
| RAM               | Usually 16GB+        | 8/16GB                |
| GPU               | Newer integrated GPU | Intel Iris/Radeon Pro |
| Linux support     | Easier               | More annoying         |
| AI/ML development | Better               | Poor                  |
| Repair/upgrade    | Easier               | Difficult             |

## Lenovo Xiaoxin

It is basically designed for Windows:

```
Lenovo Xiaoxin
      |
      +-- UEFI BIOS
      |
      +-- Windows 11
      |
      +-- Lenovo drivers
      |
      +-- WSL2 / Docker / CUDA GPU (if NVIDIA)
```

Good for:

* Visual Studio Code
* Python
* Java
* Docker
* WSL2
* AI development
* Daily Windows apps

---

## MacBook Pro 2017

It is a nice machine, but Windows is not its "native home":

```
MacBook Pro 2017

Apple EFI
   |
Boot Camp layer
   |
Windows
   |
Apple drivers
```

Problems:

* Older Intel CPU
* No official Windows 11 support
* Boot Camp drivers are aging
* Touch Bar drivers can be annoying
* Apple keyboard layout is different
* Cooling is not great under Windows
* If you compile kernels, you may spend time fixing hardware compatibility

It is better used as:

```
MacBook Pro 2017
       |
       +-- Ubuntu/Linux
       |
       +-- macOS
       |
       +-- Development machine
```

---

Given your use case (Linux kernel compilation, AI, PyTorch, LLM experiments):

I would do:

```
Lenovo Xiaoxin
    |
    +-- Windows 11
    |
    +-- WSL2 Ubuntu
    |
    +-- Docker
    |
    +-- Python/PyTorch

MacBook Pro 2017
    |
    +-- Ubuntu
    |
    +-- kernel experiments
    |
    +-- lightweight coding
```

The Lenovo gives you fewer hardware fights. The MacBook Pro 2017 is interesting for learning EFI/Linux internals, but not the best Windows laptop in 2026.
