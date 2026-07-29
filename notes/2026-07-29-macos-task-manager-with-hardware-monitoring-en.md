---
audio: false
generated: true
image: false
lang: en
layout: post
title: macOS Task Manager with Hardware Monitoring
translated: false
type: note
---

Question: What's `JOHN-decm/MacOS-TSKMGR` GitHub project?

Answer:

[MacOS-TSKMGR GitHub repository](https://github.com/JOHN-decm/MacOS-TSKMGR?utm_source=chatgpt.com) is a **native macOS Task Manager clone inspired by Windows Task Manager**.

Think of it as:

> Windows Task Manager UX + macOS native APIs + hardware monitoring.

The author is building a replacement-style utility for macOS, not a direct clone of Apple's Activity Monitor.

## What it does

It provides pages similar to Windows Task Manager:

* Processes
* Performance graphs
* App history
* Startup programs
* Users
* Details
* Services

It can show:

* CPU usage
* Memory
* Disk
* Network
* GPU
* NPU
* Temperature / cooling information

and actions like:

* End task
* Restart Finder-like processes
* Run new task
* Always-on-top window
* Refresh-rate switching

---

## Interesting engineering parts

The interesting part is not the UI; it is the hardware telemetry.

### 1. macOS system monitoring

It uses native macOS interfaces:

```
sysctl
host_statistics
proc_pidinfo
proc_pid_rusage
IOKit
CoreWLAN
CGWindowList
launchctl
```

instead of Electron/Tauri/web UI frameworks.

Architecture:

```
SwiftUI
   |
   +-- AppKit
   |
   +-- System collectors
          |
          +-- CPU
          +-- Memory
          +-- GPU
          +-- Network
          +-- Sensors
          +-- Processes
```

This is closer to how Apple's own utilities are built.

---

## 2. Apple Silicon NPU / Neural Engine monitoring

This is the most technically interesting piece.

Apple does not expose a nice public API like:

```python
gpu.utilization()
npu.utilization()
```

Instead the project uses lower-level interfaces:

```
IOReport
Energy Model
ANS2 Power
AMC Stats Perf Counters
```

to estimate:

* Neural Engine activity
* power usage
* data movement
* memory usage

This is similar to reverse engineering GPU telemetry tools.

---

## 3. Cooling / temperature monitoring

It reads:

```
AppleSMC
SMC sensors
HID temperature nodes
board sensors
```

to collect:

* CPU temperature
* GPU temperature
* SSD temperature
* WiFi temperature
* SoC temperature
* Logic board temperature
* Fan RPM

---

## Tech stack

Native macOS:

```
Language:
    Swift

UI:
    SwiftUI
    AppKit

Build:
    Xcode

Targets:
    arm64 (Apple Silicon)
    x86_64 (Intel Mac)
```

---

## Why this project is interesting

For someone doing AI + hardware work, the interesting lesson is:

A lot of "AI workstation monitoring" today is missing this layer.

Imagine a local AI agent:

```
Agent
 |
 +-- observes:
 |      GPU VRAM
 |      temperature
 |      power
 |      CPU load
 |      memory pressure
 |
 +-- decides:
        kill process
        restart inference server
        change batch size
        reduce context length
```

This kind of project is basically the foundation for a **local AI operating system agent**.

For example:

```
Hermes agent
      |
      |
      +-- vLLM server
      |
      +-- MacOS-TSKMGR style telemetry
      |
      +-- auto optimize inference
```

---

## Limitations

The difficult parts:

1. Private Apple APIs

```
IOReport
AppleSMC
```

may break after macOS updates.

2. No official signing yet

The author says it is not currently distributed through Mac App Store because there is no Apple Developer Program signing setup.

3. Hardware-specific

Apple Silicon generations differ:

```
M1
M2
M3
M4
```

have different sensors and Neural Engine behavior.

---

My take: this is a very good example of a **small but deep systems project**. It is not huge in LOC, but touches:

* OS internals
* hardware telemetry
* reverse engineering
* native UI
* performance engineering

Similar spirit to:

* `nvtop` for NVIDIA/Linux
* `btop`
* `iStat Menus`
* Windows Task Manager

but focused on modern Mac hardware.

For an AI workstation era, this category (hardware observability + autonomous agents) is likely to become more important.
