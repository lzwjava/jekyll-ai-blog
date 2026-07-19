---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GPU-T: Linux GPU Diagnostic Tool"
translated: false
type: note
---

Question: Can you explain what the GPU-T repository on GitHub is and what it does?

Answer: **GPU-T** is an open-source, graphics card diagnostic and information utility specifically built for **Linux**. It is heavily inspired by **GPU-Z**, the popular Windows tool used to verify graphics hardware, monitor performance metrics, and view real-time sensor data.

The developer started the project because Linux lacked a direct alternative to GPU-Z that offered a clean, information-dense graphical user interface (GUI).

### Key Features

* **Detailed Hardware Diagnostics:** It identifies the exact GPU make, model, revision, die size, transistor count, and release date using updateable local JSON databases.
* **Real-time Sensor Monitoring:** Tracks live metrics such as core/VRAM clock speeds, temperatures (edge and hotspot), fan speeds, power consumption (board power draw), and supports logging this data to a text file.
* **Advanced Capabilities Detection:** Checks for features like PCIe Resizable BAR (ReBAR) status, driver/BIOS versions, memory type/vendor, and API support (Vulkan, OpenCL, CUDA, Ray Tracing).
* **Multimedia Capabilities:** Offers verification of video codec capabilities such as VA-API (for AMD) and NVENC/NVDEC (for NVIDIA).

### Technical Details & Architecture

* **Framework:** Built using **.NET** and **Avalonia UI**, allowing for a responsive user interface with native support for dark, light, and automatic theme modes.
* **Architecture:** Uses a clean Model-View-ViewModel (MVVM) architecture with a vendor-agnostic design (using a factory pattern). This makes it easy to add support for different vendors without modifying the UI code.
* **No Root Required:** It reads information directly from user-accessible system paths (like `/sys/class/drm`) and standard Linux utilities, meaning it does not require administrative or root privileges to run.
* **Supported Hardware:** Fully implements support for **AMD Radeon** (2014 or later, using the `amdgpu` driver) and **NVIDIA GeForce** (2010 or later, using proprietary drivers). Preliminary architecture is ready for Intel Arc graphics cards.

### Installation

GPU-T is distributed primarily as a self-contained **AppImage** (which bundles the required .NET runtime so you do not need to install it separately). It can also be installed on Arch Linux via the AUR (`gpu-t`) or through the `am` package manager (`amMan`).

References:

* [GitHub - lseurttyuu/GPU-T](https://github.com/lseurttyuu/GPU-T)
