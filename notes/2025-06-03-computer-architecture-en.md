---
audio: false
generated: true
lang: en
layout: post
title: Determine Computer Architecture Type
translated: false
type: note
---

To determine if your current computer is running a 64-bit x86 (x64) or ARM64 architecture, follow these instructions based on your operating system:

**Windows:**

1. **Press the Windows key + R** to open the Run dialog box.
2. **Type `msinfo32`** and press Enter. This will open the System Information window.
3. In the System Information window, look for the **"System Type"** entry.
    * If it says **"x64-based PC"**, your computer has a 64-bit x86 (x64) processor.
    * If it says **"ARM64-based PC"**, your computer has a 64-bit ARM (ARM64) processor.

**macOS:**

1. Click on the **Apple menu** in the top-left corner of your screen.
2. Select **"About This Mac"**.
3. In the "Overview" tab, look for the **"Processor"** or **"Chip"** information:
    * If it lists an **Intel processor** (e.g., Intel Core i7, Intel Core i9), your Mac has a 64-bit x86 (x64) processor.
    * If it lists an **Apple silicon chip** (e.g., Apple M1, Apple M2, Apple M3), your Mac has an ARM64 processor.

**Linux:**

1. Open a **terminal** window.
2. Type the following command and press Enter:

    ```bash
    uname -m
    ```

3. The output will indicate the architecture:
    * **`x86_64`** or **`amd64`**: This indicates a 64-bit x86 (x64) processor.
    * **`aarch64`** or **`arm64`**: This indicates a 64-bit ARM (ARM64) processor.
    * Other outputs might indicate a 32-bit system (though less common now).

Based on the components you've listed for your new build, the **Intel Core i9-13900KF** processor is an **x64 (64-bit x86)** architecture processor. Therefore, the new computer you are building will be an **x64-based system**.
