---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lenovo Xiaoxin VMD Missing BIOS Option
translated: false
type: note
---

Question: Lenovo Xiaoxin BIOS has no Intel VMD/RST option. What should you do next?

Answer:

That is common. Many **Lenovo Xiaoxin (小新)** models hide the VMD/RST switch completely in consumer BIOS. The absence of the option does **not** rule out VMD, but we need to verify instead of guessing.

The other agent's theory is still possible, but let's collect evidence.

---

## 1. Check if Windows PE sees the SSD through VMD

You are currently in Windows Setup. Press:

```
Shift + F10
```

Run:

```cmd
diskpart

list disk
```

Tell me the output.

Example:

### Case A — normal NVMe

```
Disk 0    512 GB
```

### Case B — VMD/RST

Sometimes you see the disk but Windows installer needs Intel RST driver.

---

## 2. Check storage controller name

In the same command prompt:

```cmd
wmic path Win32_PnPEntity get Name
```

Look for:

```
Intel(R) Volume Management Device
Intel RST
VMD
```

or:

```
Standard NVM Express Controller
```

If you see:

```
Intel(R) Volume Management Device
```

then VMD is active.

---

## 3. Lenovo hidden BIOS menu

Some Lenovo BIOS versions hide the option. Try:

Enter BIOS:

```
F2
```

Then:

```
Configuration
```

Look for:

```
Storage
SATA Controller Mode
```

or:

```
Intel Rapid Storage Technology
```

If nothing exists, do not spend time hunting it.

---

## 4. Another likely cause: Windows installed, but boot entry failed

Your logs showed:

```
Setup Phase: [4]
Overall progress: [11%]
```

This is interesting.

The failure is very early in the "install mode" transition.

Check after failure:

Press:

```
Shift + F10
```

Run:

```cmd
diskpart

list vol
```

Look for:

```
EFI
FAT32
100-300MB
```

If missing, the disk partitioning is wrong.

---

## 5. My updated probability

After knowing:

* USB is correct ✅
* Lenovo BIOS hides VMD option ✅

I would change:

| Cause                   | Probability |
| ----------------------- | ----------: |
| EFI/GPT partition issue |         40% |
| Intel VMD/RST           |         35% |
| Driver issue            |         15% |
| USB                     |         <5% |

The previous "VMD 60%" was too aggressive without BIOS evidence.

---

## Fastest test

Since you are doing a clean install, I would do:

1. Boot installer
2. At disk selection press:

```
Shift + F10
```

3. Run:

```cmd
diskpart

list disk

select disk 0

clean

convert gpt

exit
```

4. Install again.

This removes all Lenovo recovery partitions and old metadata.

Before doing that, send me the output of:

```cmd
diskpart
list disk
list vol
```

That will tell us whether this is VMD or partition metadata.
