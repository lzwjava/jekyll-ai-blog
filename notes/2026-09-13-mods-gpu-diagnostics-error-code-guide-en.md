---
audio: false
generated: true
image: false
lang: en
layout: post
title: MODS GPU Diagnostics Error Code Guide
translated: false
type: note
---

Here's how MODS helps diagnose a card that's detected but failing, and how to read its error codes.

## How MODS Diagnoses a Card

Once the GPU is detected by the system, MODS runs targeted hardware tests that exercise specific parts of the card:

| Test # | Test Name | What it catches |
|---|---|---|
| **3** | **MatsTest** | Memory array coupling faults — detects bad VRAM chips, which memory lane failed, whether read or write failure |
| **18** | **ByteTest** | Same as Mats but byte-level — catches narrow memory faults |
| **19** | **FastMatsTest** | Hardware-accelerated VRAM test with DMA — catches memory timing/stress issues |
| **52** | **MarchTest** | "Marching ones and zeros" memory pattern — catches DRAM cell retention issues |
| **2** | **GLStress** | GPU core rendering pipeline — detects pixel miscompares, shader/core issues |
| **9** | **Random2D** | 2D rendering engine test |
| **127** | **CudaColumnTest** | Long-term DRAM data retention test |
| **17** | **ValidSkuCheck** | Validates fusing, GPC/TPC/FBP/ROP counts — detects disabled/broken units |
| **50** | **I2CTest** | Checks if GPU's I2C bus has pull-up resistors (common on dead boards) |

## How to Read MODS Error Codes

When a test fails, MODS outputs lines like this in `mods.log`:

```
Exit 19083: FastMatsTest.Run golden value miscompare [5.293 seconds]
```

Since MODS R367, error codes are **12 digits** with this structure:

```
X  YYY  ZZ  NNN  EEE
│   │   │    │    │
│   │   │    │    └── 3-digit error code (1-999)
│   │   │    │
│   │   │    └─────── 3-digit test number
│   │   │
│   │   └──────────── 2-digit P-state (00, 01, 05, 08, etc.)
│   │
│   └──────────────── 3-digit PState info (type, rail, clock domain)
│
└──────────────────── 1-digit V-F curve info
                      (0=static, 1=switching inflection points, 2=sweeping)
```

### Example from the document:

```
Error code: 271108119083
```

Broken down:

| Digits | Field | Value | Meaning |
|---|---|---|---|
| **2** | V-F curve | 2 | Sweeping the V-F curve |
| **711** | PState info | 7,11,0 | Intersection, multiple intersect params |
| **08** | P-State | 08 | P-State 8 |
| **119** | Test number | 119 | CudaRandom test |
| **083** | Error code | 83 | Golden value miscompare (CRC mismatch) |

So: **CudaRandom test (#119) failed with a golden value miscompare (error 83) while sweeping the V-F curve at P-State 8**.

## Common Error Codes (from the document)

| Error | Meaning |
|---|---|
| **1** | Exit (normal) |
| **7** | Bad command line argument |
| **9** | Cannot allocate memory |
| **15** | User aborted the script |
| **49** | Timeout error |
| **83** | Golden value miscompare (CRC mismatch — most common GPU failure) |
| **115** | Cannot initialize OpenGL (driver issue) |
| **118** | OpenGL error (various) |
| **131** | Invalid encryption key |
| **132** | Decompressed data differs from expected |
| **137** | EDC detected memory-bus error |
| **138** | Encryption/decryption failed |
| **140** | Temperature limits exceeded / thermal sensor bad |
| **144** | PCI Express bus error |
| **145** | CUDA error / cuInit failed |
| **152** | Compute test failed |
| **160** | CRC values not unique |
| **173** | ECC single-bit error |
| **174** | ECC double-bit error |
| **265** | Bad RAM in the GPU |
| **266** | GPU didn't get expected number of PCIe lanes |
| **649** | Bad RAM in the GPU |
| **650** | GPU did not get the expected number of lanes |
| **823** | FB link training failure |
| **824** | FB memory error |
| **825** | PMU error |

## Practical Diagnostic Flow with MODS

```bash
# 1. Run full manufacturing test suite
sudo ./mods gputest.js -mfg -l mods.log

# 2. Check the log for failures
grep "Exit " mods.log

# 3. Focus on memory tests if card is unstable
sudo ./mods gputest.js -mfg -test 3    # MatsTest (memory)
sudo ./mods gputest.js -mfg -test 52   # MarchTest (memory)
sudo ./mods gputest.js -mfg -test 19   # FastMatsTest (stress memory)

# 4. Test rendering pipeline
sudo ./mods gputest.js -mfg -test 2    # GLStress

# 5. For extra memory info
sudo ./mods gputest.js -mfg -test 3 -matsinfo   # detailed memory lane failures
```

### Key indicators:

- **Error 83 (golden miscompare)** on Mats/MarchTest → **Bad VRAM chip** (note which bit lane)
- **Error 137 (EDC memory-bus error)** → **VRAM power/data integrity issue**
- **Error 649 (Bad RAM in GPU)** → **Definitive memory failure**
- **Error 144 (PCIe error)** → **Bad PCIe connection or link issue**
- **Error 152 (compute test failed)** → **GPU core/shader failure**
- **Test 17 (ValidSkuCheck)** failure → **Misconfigured fusing or disabled units**

## TL;DR

For a "dead" card that's at least detected:

1. `mods gputest.js -mfg` → runs everything
2. Look for `Exit XXXX` lines in `mods.log`
3. Parse the **12-digit error code** to identify which test and what failed
4. Memory errors (test 3, 19, 52) = **bad VRAM** — most common on dead cards
5. If all memory tests fail → could be **power delivery to VRAM**, not the chips themselves
