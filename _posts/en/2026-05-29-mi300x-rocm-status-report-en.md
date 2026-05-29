---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X ROCm Status Report
translated: false
type: note
---

Here's the full report:
    
    
    ====================================================================
               COMPREHENSIVE ROCm & GPU STATUS REPORT
    ====================================================================
    
    SYSTEM
    
      Hostname:     snapshots-gpu-mi300x1-192gb-devcloud-atl1
      Kernel:       6.8.0-117-generic (Ubuntu 24.04)
      Arch:         x86_64
    
    ROCm STACK
    
      Version:      7.2.0
      HIP:          7.2.26015 (AMD clang 22.0.0)
      HSA Runtime:  1.18
      ROCk Module:  6.16.13 (loaded)
      Install Path: /opt/rocm-7.2.0 -> /opt/rocm
      Shared Libs:  60 libraries (rocblas, hipfft, rccl, MIOpen, etc.)
      Binaries:     hipcc, rocm-smi, rocminfo, rocgdb, rocprof, hipify-clang, ...
    
    GPU HARDWARE
    
      Device:       AMD Instinct MI300X VF
      GFX Target:   gfx942 (gfx9-4-generic also supported)
      Chip ID:      0x74b5
      SKU:          M3000100
      Compute Units: 304
      SIMDs/CU:     4
      Shader Engines: 32
      Wavefront:    64
      Max Clock:    2100 MHz
      Fast FP16:    Yes
      SRAMECC:      Enabled
      XNACK:        Disabled
    
    MEMORY
    
      VRAM Total:   ~192 GB (205,822,885,888 bytes)
      VRAM Used:    ~299 MB (299,687,936 bytes)
      VRAM Free:    ~191.5 GB
      L1 Cache:     32 KB
      L2 Cache:     4 MB
      L3 Cache:     256 MB
    
    THERMAL & POWER
    
      Junction Temp:    43.0 C
      Memory Temp:      37.0 C
      Current Power:    157.0 W
^[[40;1R      Power Cap:        750.0 W
      Fan:              Not supported (passive/liquid cooling)
    
    CLOCK & PERFORMANCE
    
      fclk:     1300 MHz
      mclk:     900 MHz
      sclk:     131 MHz (idle)
      socclk:   889 MHz
      Perf Level: auto
      GPU Busy:   0% (idle)
    
    CPU
    
      Model:        Intel Xeon Platinum 8568Y+
      Compute Units: 20
      L1 Cache:     32 MB
      System RAM:   ~247 GB
    
    ENVIRONMENT
    
      PATH:         /opt/rocm/bin (added this session + persisted to .bashrc)
      LD_LIBRARY:   /opt/rocm/lib (persisted to .bashrc)
      ROCM_PATH:    Not set
      HIP_PATH:     Not set
      PyTorch:      NOT INSTALLED
    
    STATUS
    
      GPU:          DETECTED & IDLE
      ROCm:         FULLY INSTALLED
      Tools:        ALL PRESENT (hipcc, rocm-smi, rocminfo, rocgdb, rocprof)
      PATH:         FIXED (added /opt/rocm/bin)
      Missing:      PyTorch/ROCm, ROCM_PATH & HIP_PATH env vars
    ====================================================================
    
    
    Key takeaways:
      - ROCm 7.2.0 is fully installed with all dev/debug/profiling tools
      - MI300X (192GB HBM3) is detected, idle, cool (43C), and ready
      - PyTorch is NOT installed — if you need it, I can install the ROCm build
      - ROCM_PATH and HIP_PATH env vars are not set (optional but recommended)
    
    Want me to install PyTorch with ROCm support or set the remaining env vars?