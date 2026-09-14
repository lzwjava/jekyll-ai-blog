---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dual Xeon Tesla P100 GPU Server
translated: false
type: note
---

Here's the full hardware picture of the remote machine:

---

## 🖥️ CPU

| Spec | Value |
|---|---|
| **Model** | 2× **Intel Xeon E5-2650 v4** @ 2.20 GHz |
| **Cores** | 12 cores × 2 sockets = **24 cores / 48 threads** |
| **Cache** | L1: 768 KiB, L2: 6 MiB, L3: **60 MiB** |
| **Max Freq** | 2.90 GHz |
| **Arch** | x86_64, Broadwell-EP |

## 🧮 Memory

| | Size |
|---|---|
| **RAM** | **62 GiB** total (~52 GiB available) |
| **Swap** | **8 GiB** (barely used) |

Most of the 48 GiB is cached/buffered — plenty of headroom.

## 💾 Storage

| Mount | Size | Used | Avail |
|---|---|---|---|
| `/` (overlay) | **32 GiB** | 50 MiB | 32 GiB |

Fairly small root disk — only 32 GB total.

## 🎮 GPUs

| Index | Model | VRAM |
|---|---|---|
| GPU 0 | **Tesla P100-PCIE-12GB** | 12,288 MiB |
| GPU 1 | **Tesla P100-PCIE-12GB** | 12,288 MiB |

Both connected via PCIe Host Bridge (PHB topology) on the same NUMA node (0-47 CPUs).

## 🐧 OS
- **Kernel**: Linux 5.15.0-191-generic (Ubuntu-based, x86_64)
- **CUDA**: 12.8
- **Driver**: 580.178.04

## Summary
This is a **dual-socket Broadwell server** (48 threads) with **62 GiB RAM** and **2× Tesla P100 (12 GB each)** — a capable GPU compute node, though the 32 GB root disk is relatively tight. Good for training/inference workloads that fit in the combined 24 GB of GPU memory.
