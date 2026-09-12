---
audio: false
generated: true
image: false
lang: en
layout: post
title: MODS Basic Test Commands
translated: false
type: note
---

Based on the MODS diagnostic document, here's how to run basic tests:

## Basic MODS Test Commands

### 1. Run the standard manufacturing test suite
```bash
mods gputest.js -mfg
```
This runs the full manufacturing test suite on all detected GPUs.

### 2. Run a specific test by ID
```bash
mods gputest.js -mfg -test <test_number>
```
For example, test 58 = Random2D, test 61 = GpuDmaTest, test 2 and 79 for GLStress/TurboCipher, etc.

### 3. Skip specific tests
```bash
mods gputest.js -mfg -skip <test_number>
```

### 4. Target a specific GPU device
```bash
mods gputest.js -mfg -dev <device_id>
```
For example, `-dev 0` for the first GPU, `-dev 1` for the second, etc.

### 5. Run tests on all GPUs concurrently
```bash
mods gputest.js -mfg -concurrent_devices
```

### 6. Run different tests per GPU
```bash
mods gputest.js -mfg -concurrent_devices -test 58 -dev 0 -test 61 -dev 1 -test 2 -test 79 -concurrent
```
This runs Random2D on GPU 0, and concurrently runs GLStress & TurboCipher on GPU 1.

### 7. Save/load custom test specifications
```bash
# Save current spec to a file
mods gputest.js -mfg -savespec my_spec.txt

# Run using a saved spec
mods gputest.js -readspec my_spec.txt
```

### 8. Run a background test while main tests run
```bash
mods gputest.js -mfg -threadid -dev 1 -bgtest_flags 16 disp,roe -dev 0 -skip 24 -skip 17
```
This runs test 16 as a background thread on device 1 (with display + run-on-error), while running the full suite minus tests 24 & 17 on device 0.

### 9. Enable thread logging
```bash
mods gputest.js -mfg -threadid
```
Prepends thread ID info to each log line for debugging.

---

**Key flags summary:**
| Flag | Purpose |
|---|---|
| `-mfg` | Manufacturing test specification |
| `-slt` | System-level test specification |
| `-test N` | Run specific test number N |
| `-skip N` | Skip test number N |
| `-dev N` | Target GPU device N |
| `-concurrent_devices` | Run on all GPUs simultaneously |
| `-bgtest N` | Run test N as background thread |
| `-threadid` | Show thread IDs in logs |
| `-concurrent` | Run tests concurrently on the same GPU |

The MODS tool is JavaScript-driven, so you can also write custom test scripts using MODS's JavaScript API (e.g., `g.Thermal.SetFanSpeed()`, `this.SignalSetupCompleteAndWait()`, etc.).
