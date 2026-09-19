---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Tesla M40 BAR Allocation Error
translated: false
type: note
---

Question: How do I fix the Tesla M40 BAR allocation failure on an ASUS A68HM-E with AMD A4-5000 / Athlon X4 850?

Answer:

Your board and CPU change the picture significantly. Let me re-diagnose:

---

## Revised Hardware Profile

| Item | Detail |
|---|---|
| Board | ASUS A68HM-E (AMD FM2+ socket) |
| CPU | Athlon X4 850 (Kaveri/Godavari, FM2+) |
| Chipset | AMD A68H (Bolton D2) |
| PCIe | Gen 2.0 x16 from the APU itself |
| GPU | Tesla M40 12 GB (needs 16 GiB prefetchable BAR) |

---

## The Core Problem is Worse Than Before

The AMD A68H platform has stricter limitations than Intel B150:

**1. Above 4G Decoding — likely absent or broken**
The A68HM-E BIOS options are minimal. ASUS rarely exposed Above 4G Decoding on budget FM2+ boards. Even if the option exists, the Athlon X4 850 (non-APU variant with no iGPU) means the PCIe BAR window budget is entirely consumed by the M40 — there's nothing sharing it, but the firmware still won't allocate a 16 GiB window above 4G without explicit support.

**2. PCIe Gen 2.0 x16 bandwidth**
The M40 will run, but at reduced bandwidth (Gen 2 x16 = ~8 GB/s vs Gen 3 x16 = ~16 GB/s). Not a blocker, just a note.

**3. The Athlon X4 850 has no integrated graphics**
This is actually fine — the M40 has no display outputs anyway. But it means you need to confirm you have a separate display card, or are running headless.

---

## What To Try, In Order

### Step 1 — Check BIOS version and Above 4G option

Boot into BIOS (Del key) and look under:

```
Advanced → System Agent Configuration → Above 4G Memory / Crypto Currency Mining
```
or
```
Advanced → PCIe Configuration → Above 4G Decoding
```

ASUS sometimes hides it. If it's not there, update BIOS first.

Check your current BIOS version:
```bash
sudo dmidecode -s bios-version
```

Then check ASUS's support page for the A68HM-E for the latest BIOS — later versions sometimes unlock this option.

---

### Step 2 — Linux kernel boot parameter workaround

If Above 4G Decoding is not available in BIOS, try forcing it from the kernel side. Edit GRUB:

```bash
sudo nano /etc/default/grub
```

Change this line:
```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
```
To:
```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash pci=realloc=on memmap=16G!4G"
```

Then:
```bash
sudo update-grub
sudo reboot
```

After reboot, check if the BAR was assigned:
```bash
sudo lspci -v -s 01:00.0 | grep -i "memory\|prefetch\|bar"
```

---

### Step 3 — Install the driver (do this regardless)

Even with the BAR problem unresolved, install the driver so it's ready the moment the BAR issue is fixed:

```bash
sudo apt update
sudo apt install build-essential dkms linux-headers-$(uname -r)
sudo apt install nvidia-driver-580
echo -e "blacklist nouveau\noptions nouveau modeset=0" | sudo tee /etc/modprobe.d/blacklist-nouveau.conf
sudo update-initramfs -u
```

Then reboot.

---

### Step 4 — Verify after reboot

```bash
nvidia-smi
```

If you still get "No devices found", the BAR is still not allocated. Check:
```bash
sudo dmesg | grep -i "bar\|pci\|nvidia\|nouveau"
```

---

## Honest Assessment

| Scenario | Outcome |
|---|---|
| BIOS has Above 4G option | Enable it → M40 works |
| BIOS updated, option appears | Enable it → M40 works |
| No Above 4G anywhere, kernel workaround works | M40 works |
| None of the above | M40 cannot initialize on this board |

The A68HM-E is a budget micro-ATX board from ~2014. The Tesla M40 is a datacenter GPU that expects server-class firmware. **There is a real chance this combination simply won't work** without a BIOS that supports Above 4G Decoding.

---

## About the sudo password

I cannot and should not ask for your sudo password directly — please run the commands above yourself in a terminal. If you want me to help interpret any output, paste it here and I'll guide you through the next step.