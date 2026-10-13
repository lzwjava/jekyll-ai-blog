---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nvidia Jetson TX1 Embedded AI Platform
translated: false
type: note
---

Question: What is the Nvidia Jetson TX1 (with carrier board + power supply, running Ubuntu)?

Answer:

The **NVIDIA Jetson TX1** is a compact, high-performance embedded computing platform designed for AI and computer vision tasks. Here's what you have:

---

### 🧩 Module (the "brain")
The Jetson TX1 uses a modular architecture — a **COM (Computer-on-Module)** containing the Tegra X1 SoC, 4 GB LPDDR4 memory, 16 GB eMMC 5.1 flash storage, 802.11ac Wi-Fi/Bluetooth, and Gigabit Ethernet.

| Component | Spec |
|---|---|
| GPU | 256-core NVIDIA Maxwell™ GPU, >1 TFLOP performance |
| CPU | Quad-Core ARM Cortex-A57 MPCore (64-bit) |
| RAM | 4 GB LPDDR4 |
| Storage | 16 GB eMMC 5.1 |
| Power | Under 10W |

---

### 🔌 Carrier Board (底板) — I/O Ports
The COM module mounts on a carrier board that exposes connectors including:
USB 3.0 Type-A, USB 2.0 Micro-AB (recovery/host), HDMI, M.2 Key E, PCIe x4, Gigabit Ethernet, full-size SD card, SATA data+power, display expansion header, and camera expansion header.

There are also two GPIO expansion headers — a **40-pin 2.54mm header** (similar layout to Raspberry Pi) and a **30-pin 2.54mm header** for extra GPIO.

---

### ⚡ Power Supply (电源)
The carrier board requires a **19V DC input** for power.

---

### 🐧 Ubuntu / Software
NVIDIA provides a software development kit (JetPack SDK) including a debugger, compiler, libraries, and tools. The SDK is based on NVIDIA's CUDA parallel programming framework and supports OpenCV, OpenVX, and VisionWorks for image recognition.

Note: JetPack 4.x (based on Jetson Linux r32) is the **last supported version** for Jetson TX1. The TX1 module has reached End-of-Life (EOL). Your Ubuntu system is likely **Ubuntu 18.04** with JetPack 4.x.

---

### 🚀 Typical Use Cases
The small size, low power, and strong GPU processing make the Jetson TX1 ideal for robotics, real-time image and sensor data processing, remote image recognition, and in-vehicle computing applications.

---

References:
- [JetsonHacks – Jetson TX1 Development Kit Overview](https://jetsonhacks.com/2015/11/10/nvidia-jetson-tx1-development-kit/)
- [NVIDIA Developer – Jetson TX1 DevKit](https://developer.nvidia.com/embedded/buy/jetson-tx1-devkit)
- [Linux.com – Jetson TX1 Review](https://www.linux.com/?p=476440)