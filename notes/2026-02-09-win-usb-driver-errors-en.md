---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5.2
title: Windows USB Driver Load Missteps
translated: false
type: note
---

Question: Why does Windows still fail to find/load drivers from my FAT32 USB during installation on Lenovo Xiaoxin 14 IAH8 even though BIOS is already set to AHCI?

Answer:

Good check — if **AHCI is already enabled**, then we can rule out Intel VMD/RST as the blocker. In that case, the issue is **not a BIOS storage mode problem**, but a **misunderstanding of what Windows Setup can load as a “driver.”**

Below is the **correct root cause analysis** for your situation.

---

## 1. Windows Setup Does **Not** Load `.exe` Files (At All)

This is the key point.

During installation, Windows Setup:

* **cannot execute `.exe` installers**
* **only scans for `.inf` driver definition files**
* ignores everything else silently

So when you plug in a USB that contains only files like:

* `chipset-KZSC030FLWDYANE0.exe`
* `intelVGA-KZSG0A0FT22GJNE0.exe`
* `audio-*.exe`
* `RTKwlan-*.exe`

Windows Setup will show:

* **empty list**
* or “No signed drivers were found”

This is **expected behavior**, not a fault.

> Even if the SSD is visible, the *Load Driver* dialog will never show `.exe` files.

---

## 2. With AHCI Enabled, You Usually Don’t Need Any Driver at All

Important clarification:

* **Windows 10 / 11 already include a generic NVMe + AHCI driver**
* If BIOS = **AHCI**
* And SSD = **standard NVMe**
* Then **Windows Setup should detect the disk automatically**

If the disk **does appear**, then:

* You do **not** need to load any driver
* Just delete partitions and continue install

If the disk **does NOT appear**, then one of the following is true.

---

## 3. Why the SSD Still Might Not Appear (Even in AHCI)

### Case A — Windows installer is too old

If you are using:

* Windows 10 **1809 or earlier**
* Or a heavily modified ISO

Then NVMe support may be incomplete.

**Fix**

* Use **Windows 10 22H2** or **Windows 11 23H2+**
* Recreate USB with **Microsoft Media Creation Tool** or **Rufus (GPT + UEFI)**

---

### Case B — You are confusing “Load driver” with “missing disk”

Many users do this:

* Disk **is visible**
* But Windows warns: *“Windows cannot be installed to this disk”*
* User clicks **Load driver**, thinking a driver is missing

In reality, the problem is:

* Partition style mismatch (MBR vs GPT)
* Leftover Intel RAID metadata
* Or Secure Boot leftovers

**Fix**
At disk screen:

1. Press **Shift + F10**
2. Run:

   ```
   diskpart
   list disk
   select disk 0
   clean
   convert gpt
   exit
   ```

3. Close CMD → Refresh → Install

---

### Case C — Secure Boot + non-official ISO

If:

* Secure Boot is ON
* ISO is unofficial / modified

Then Windows may block disk access.

**Fix**

* Temporarily disable **Secure Boot**
* Install Windows
* Re-enable Secure Boot later

---

## 4. Why Lenovo Driver `.exe` Files Are Useless During Setup

Lenovo drivers are designed for **post-install** usage:

| Driver type | Purpose         | Setup usable? |
| ----------- | --------------- | ------------- |
| Chipset     | Enables devices | ❌             |
| VGA         | Graphics        | ❌             |
| Audio       | Sound           | ❌             |
| WLAN        | Network         | ❌             |
| Camera / FP | Peripherals     | ❌             |

They:

* contain installers
* extract files dynamically
* require Windows services

Windows Setup environment (**WinPE**) cannot use them.

---

## 5. What You Should Do Right Now (Checklist)

Since AHCI is already correct:

1. ✅ **Ignore “Load driver” entirely**
2. ✅ Use **latest Windows ISO**
3. ✅ Delete all partitions (`diskpart clean`)
4. ✅ Install to unallocated space
5. ✅ After first boot:

   * Install Lenovo Vantage
   * Let Windows Update pull drivers
   * Then manually install Lenovo `.exe` drivers if needed

---

## Bottom Line

* Your USB is fine
* FAT32 is correct
* BIOS AHCI is correct
* **The issue is that `.exe` drivers are not drivers in Windows Setup terms**
* You almost certainly **do not need to load any driver at all**

If you want, tell me:

* Windows version (10/11 + build)
* Whether the SSD is visible or invisible
* Exact error text (if any)

I can pinpoint it in one step.
