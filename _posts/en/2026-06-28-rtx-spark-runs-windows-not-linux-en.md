---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX Spark Runs Windows, Not Linux
translated: false
type: note
---

Question: Does RTX Spark run on Linux?

Answer:

No — **RTX Spark is a Windows-on-Arm platform**, not Linux. That's the whole point of it. Don't confuse it with DGX Spark, which runs Linux.

The split:

- **RTX Spark** (consumer laptops/mini-desktops, N1X chip) → **Windows on Arm**. It was announced jointly by NVIDIA and Microsoft, with Windows providing optimizations for unified memory, workload scheduling on the heterogeneous architecture, power/thermal management, and the Windows 11 Prism emulator for running 32-bit and 64-bit x86 apps on Arm. RTX Spark PCs join the Copilot+ PC category. The marketing line was literally "With RTX Spark and Microsoft Windows, you ask — and the PC does the work."

- **DGX Spark** (the desktop research box, GB10) → **Linux**. It ships with NVIDIA DGX OS, an Ubuntu-based Linux, preloaded with the full NVIDIA AI software stack — CUDA, cuDNN, TensorRT, RAPIDS.

So same underlying GB10/Grace-Blackwell silicon family, two different OS targets: DGX Spark is the Ubuntu/CUDA dev machine, RTX Spark is the Windows-on-Arm consumer device.

A caveat worth flagging for you specifically: because RTX Spark is Arm + Windows-first, your usual terminal-first Linux/CUDA workflow doesn't transfer cleanly. Whether you can put a Linux distro on RTX Spark hardware depends on NVIDIA/OEM providing Arm Linux drivers for the Blackwell GPU block, and at announcement that wasn't promised — the software effort was explicitly pointed at Windows on Arm. If your goal is local CUDA tinkering, DGX Spark (or a GB10 partner box running DGX OS) is the SKU that fits, not RTX Spark.

References:

- [Nvidia RTX Spark - Wikipedia](https://en.wikipedia.org/wiki/Nvidia_RTX_Spark)
- [NVIDIA and Microsoft Reinvent Windows PCs (RTX Spark)](https://nvidianews.nvidia.com/news/nvidia-microsoft-windows-pcs-agents-rtx-spark)
- [NVIDIA DGX Spark First Look - Signal65](https://signal65.com/research/nvidia-dgx-spark-first-look-a-personal-ai-supercomputer-on-your-desk/)
