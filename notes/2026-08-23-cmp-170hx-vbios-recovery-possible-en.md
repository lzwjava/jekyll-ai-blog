---
audio: false
generated: true
image: false
lang: en
layout: post
title: CMP 170HX VBIOS Recovery Possible
translated: false
type: note
---

Question: **Is this CMP 170HX 8GB VBIOS situation actually OK based on the `nvflash --list` result?**

Answer:

This result is **much better than a dead card**. The card is probably recoverable.

From the screenshot:

```
lspci | grep -i nvidia

03:00.0 VGA controller: NVIDIA GA102 [GeForce RTX 3080]
03:00.1 Audio device: NVIDIA GA102 HDMI Audio

04:00.0 3D controller: NVIDIA GA100 [CMP 170HX]
```

and:

```
nvflash --list

<0> GeForce RTX 3080
<1> Graphics Device
    (10DE,20C2,10DE,1585)
```

Important points:

### Good signs ✅

1. **PCIe enumeration works**

The system sees:

```
10DE:20C2
```

That is the CMP 170HX device ID.

The GPU core, PCIe interface, and basic firmware initialization are alive.

2. **nvflash can see it**

This is the biggest positive sign.

If VBIOS was completely broken, usually:

```
nvflash --list
No NVIDIA display adapters found
```

or only PCIe appears without firmware access.

Here nvflash detects:

```
Graphics Device
```

meaning the SPI ROM is probably readable.

---

### Why "Graphics Device" instead of "CMP 170HX"?

This suggests the VBIOS is wrong.

Normally you want something like:

```
CMP 170HX
GA100
```

Instead it is generic:

```
Graphics Device
```

Common after:

* flashing wrong GA100 BIOS
* modified BIOS
* missing board strings

So the likely state:

```
GPU hardware       OK
HBM memory         unknown but likely OK
PCIe               OK
VBIOS              wrong
driver init        fails
```

---

## Before paying 2500 CNY, ask seller for one more command

Run:

```bash
sudo ./nvflash -i 1 --save cmp170hx_backup.rom
```

If it succeeds:

```
Firmware image saved
```

then recovery risk is low.

Then flash correct 8GB BIOS:

```bash
sudo ./nvflash -i 1 -6 correct_170hx_8gb.rom
```

---

## My price judgement changes after seeing this

Before screenshot:

> 2500 CNY = too risky

After screenshot:

> 2500 CNY = maybe acceptable, but still negotiate

I would value it:

* nvflash readable + backup possible: **2000-2500 CNY**
* after successful VBIOS restore: **3000+ CNY**
* if seller refuses backup test: **≤1500 CNY**

This is not a "dead mining card". It is more like a "firmware repair project".

Given you already run CUDA/Linux, this is actually a reasonable gamble.

The next critical test is:

```bash
sudo ./nvflash -i 1 --save backup.rom
```

If that works, I would be quite confident.
