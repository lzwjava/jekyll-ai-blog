---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recreate USB Installation Media
translated: false
type: note
---

Question: **Review the Windows 11 installation troubleshooting so far — what is the most likely cause and what should be done next?**

Answer:

Your diagnosis is mostly correct. The troubleshooting path has already eliminated the common causes. I would rank the remaining possibilities like this:

## Probability ranking

### 1. USB installation media problem — ~60%

This is the highest probability.

The key clue:

> Installation fails during "Installing Windows" after partitioning succeeds.

That means:

* BIOS → USB boot works ✅
* Windows PE loads ✅
* Disk is detected ✅
* GPT partitioning works ✅
* Installer starts copying/applying image ❌

A bad ISO download, bad USB write, or flaky USB flash drive often fails exactly here.

Common causes:

* corrupted `install.wim` / `install.esd`
* Rufus write issue
* cheap USB flash controller errors
* USB port instability

I would not reuse the current USB.

Recommended:

1. Download official ISO:

   Microsoft Media Creation Tool is safest.

2. Verify ISO hash if downloading manually.

3. Create USB again:

Rufus:

```
Partition scheme: GPT
Target system: UEFI (non CSM)
File system: NTFS
```

For Windows 11 ISO, Rufus may show bypass options:

* remove TPM requirement
* remove Secure Boot requirement

Do not select unnecessary bypasses on this Lenovo. Keep it standard.

---

### 2. NVMe SSD issue — ~25%

The SSD was previously Linux, but `clean` removed the partition metadata.

However, `clean` does not test the physical drive.

Possible problems:

* NVMe controller firmware bug
* bad NAND blocks
* SSD overheating
* power management issue

The pattern:

```
Partitioning succeeds
Image deployment fails
```

can also happen when writing large amounts of data to a failing SSD.

After another clean install attempt fails, test SSD.

From Linux:

```bash
sudo nvme list

sudo nvme smart-log /dev/nvme0
```

Look for:

```
critical_warning
media_errors
num_err_log_entries
percentage_used
```

---

### 3. RAM issue — ~10%

RAM usually causes:

* random BSOD
* decompression errors
* different failure points

Because Windows installation decompresses several GB of compressed files, bad RAM can trigger:

```
0x80070002
0x8007000D
```

or random corruption.

But your failure point being identical twice makes RAM less likely.

Still, if fresh USB fails:

Run:

```
memtest86+
```

at least one full pass.

---

### 4. Windows Recovery Environment trigger — interesting but probably secondary

Your log:

```
CSetupManager::OnFinishLaunchChoiceAction
Result = 0xC19001F4
```

is interesting.

This usually means Setup thinks:

"installation cannot continue, offer recovery."

But the reason behind it is earlier.

The chain is likely:

```
install image deployment fails
        |
        v
Setup decides installation failed
        |
        v
launch recovery environment
        |
        v
0xC19001F4
```

So don't chase WinRE yet.

---

## One thing I would additionally check

Before reinstalling, enter BIOS.

Check:

### Storage mode

Some Lenovo machines have:

```
Intel VMD Controller
```

or

```
RST mode
```

If enabled:

Windows installer sometimes behaves strangely.

Preferred:

```
Storage:
AHCI
```

However, since your installer already sees the NVMe and partitions it, this is probably not the issue.

---

## My next exact sequence

I would do:

### Step 1

Create new USB.

Prefer:

* different USB stick
* different USB port
* fresh ISO

---

### Step 2

Install with zero interaction.

After clicking:

```
Disk 0 unallocated space
        |
        v
Next
```

do not touch anything.

No:

* mouse
* keyboard
* trackpad
* power button

Wait until OOBE.

---

### Step 3

If failure repeats:

Boot Linux live USB and collect:

SSD:

```bash
sudo nvme smart-log /dev/nvme0
```

RAM:

```
memtest86+
```

---

My guess: **you already fixed the Linux/LVM issue. The remaining failure is probably bad Windows installation media, not the Lenovo hardware.** The fact that the machine reached Windows Setup and consistently gets to the same stage is actually a good sign.
