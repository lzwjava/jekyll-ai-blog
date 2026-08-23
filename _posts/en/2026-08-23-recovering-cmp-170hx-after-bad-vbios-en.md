---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recovering CMP 170HX After Bad VBIOS
translated: false
type: note
---

Question: **Can a CMP 170HX 8GB that detects the card but cannot install the driver after a bad VBIOS flash be fixed?**

Answer:

Yes, **probably recoverable**, because the symptom:

> "能认卡, 驱动打不上"
> "刷了vbios就驱动认不了"
> "默认坏卡出售"

usually means the GPU silicon is alive, PCIe enumeration works, but the **VBIOS/firmware state is invalid**.

For CMP 170HX, random VBIOS flashing is especially dangerous. The card is not a normal GeForce card. Many "unlock PCIe 4.0 / A100 BIOS" guides online are wrong or incomplete. The known unlock path does **not require VBIOS flashing**; it happens through driver-side runtime patches. ([GitHub][1])

## Recovery path

### 1. First check whether the GPU is still visible

Boot Linux:

```bash
lspci -nn | grep -i nvidia
```

Expected:

```
NVIDIA Corporation Device 20c2
```

For CMP 170HX 8GB, PCI ID is usually:

```
10de:20c2
```

([GitHub][2])

Then:

```bash
lspci -vv -s <GPU_BUS>
```

If PCIe sees it, the GPU core is likely OK.

---

## 2. Dump current VBIOS first

Before touching anything:

```bash
sudo nvflash --save backup.rom
```

If nvflash cannot access it, use:

* another working NVIDIA card as primary display
* Linux
* SPI programmer (CH341A) as last resort

CMP 170HX recovery often requires an external SPI flash programmer if the ROM area is corrupted. ([GitHub][1])

---

## 3. Flash the correct stock CMP 170HX ROM

You need the **exact 8GB ROM**, not:

* A100 BIOS ❌
* 10GB CMP 170HX BIOS ❌
* random mining BIOS ❌

Known 8GB CMP 170HX VBIOS examples:

```
92.00.67.00.01
92.00.6D.00.0A
```

([GitHub][2])

Flash:

```bash
sudo nvflash -6 stock_170hx_8gb.rom
```

If nvflash refuses:

```bash
sudo nvflash --protectoff
sudo nvflash -6 stock_170hx_8gb.rom
```

---

## 4. If nvflash says firmware mismatch

Because CMP cards have security checks, software flashing may fail.

Then:

### SPI programmer method

Hardware:

```
CH341A
SOIC8 clip
backup ROM
```

Procedure:

1. Remove cooler
2. Find SPI flash chip
3. Read original ROM
4. Write clean ROM
5. Verify
6. Boot

The community documentation also notes that external SPI is the reliable recovery path after bad VBIOS writes. ([GitHub][1])

---

## 5. After recovery, do NOT flash BIOS for unlock

For CMP 170HX 8GB:

The safer route:

```
stock VBIOS
        |
        v
Linux
        |
        v
patched NVIDIA driver
        |
        v
64GB unlock
```

The known unlock changes runtime driver/GSP behavior; it does not flash VBIOS. ([GitHub][3])

---

## Quick diagnosis table

| Symptom                        | Meaning                         | Fix               |
| ------------------------------ | ------------------------------- | ----------------- |
| `lspci` sees GPU, driver fails | VBIOS mismatch/corruption       | restore stock ROM |
| no PCIe device                 | hardware damage or bad power    | check board       |
| nvflash can read/write         | easy recovery                   | flash correct ROM |
| nvflash blocked                | security lock                   | SPI programmer    |
| fans spin, no driver           | firmware initialization failure | ROM recovery      |

My guess from your description:

> "一开始是好的，乱刷 VBIOS 后坏"

= **90% chance this is just wrong VBIOS, not dead GPU**.

The important question is:

1. What does `lspci -nn` show?
2. What error does `nvidia-smi` give?
3. Can `nvflash --save backup.rom` read the current BIOS?

Those three outputs determine whether it is software recovery or SPI recovery.

[1]: https://github.com/Consensus-Protocol/cmp170hx/blob/main/docs/hardware/vbios.md?utm_source=chatgpt.com "cmp170hx/docs/hardware/vbios.md at main · Consensus-Protocol/cmp170hx · GitHub"
[2]: https://github.com/Consensus-Protocol/cmp170hx/blob/main/docs/start/identify-your-card.md?utm_source=chatgpt.com "cmp170hx/docs/start/identify-your-card.md at main · Consensus-Protocol/cmp170hx · GitHub"
[3]: https://github.com/Consensus-Protocol/cmp170hx/blob/main/docs/unlock/overview.md?utm_source=chatgpt.com "cmp170hx/docs/unlock/overview.md at main · Consensus-Protocol/cmp170hx · GitHub"
