---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sudo password needed for AIC8800 driver
translated: false
type: note
---

Research complete. I have everything needed to give you a definitive answer and a precise installation plan.

## Findings

**What your CF-940AX is (confirmed on the machine):**
- The adapter enumerates as `a69c:5721 aicsemi AIC MSC` — this is **AICSemi (爱科微/AICSemi) AIC8800-family chip**, exact dongle build per the bundled Windows install: **AIC8800FC** (`aic8800fc_windows_wifi_driver.exe`), the budget "AX300" (WiFi 6, 2.4 GHz-only) dongle sold under many brands (COMFAST CF-940AX / UGREEN AX300 / Tenda AX300 / etc.). **It is not Realtek** — the chip is the Chinese vendor **AICSemi**.
- Like most of these dongles it ships in **USB "CD/MSC" mode as a driver disc** (that's the "5721 / Aic MSC" identity). Linux's whole trick is: udev rule + `eject` flips it into NIC mode, then a kernel module (aic8800) + firmware handles the WiFi NIC.

**Does Linux support exist? → Yes, and it's well-maintained.** There are three solid sources:
1. **Official AICSemi/UGREEN got phone Linux driver (v1.7, 2026)** on a real, fetching UGREEN page. But it's a `deb` aimed at older kernels (≤24.04), not ideal for your 26.04.
2. **`Kiborgik/aic8800dc-linux-patched`** — patched out-of-tree driver, **DKMS, CI-tested green on kernels 6.2 LTS / 6.18 / 7.1 / latest 7.x via GitHub Actions**. This one advertises exactly the aic8800 family incl. the `a69c:5721` MSC→NIC mode switch → *this is the right one for Ubuntu 26.04 + kernel 7.0*. Install is `sudo ./install.sh` (DKMS + firmware + udev rules).
3. Official AICSemi repos (Gitee/aicsemi & GitHub) with the same base source.

**Toolchain status on the target (192.168.1.133):**
- `git`, `depmod`, `eject`, `lsusb`, Python, curl ✓ (GitHub unreachable from there — I'll transfer the source via this laptop, which also can't reach github/gitee raw reliably... actually laptop *can*; remote cannot. So: clone on laptop → `scp`/`tar` to remote).
- `gcc`/`make`/`dkms`/`build-essential` ✗ → needs `sudo apt install build-essential dkms eject` → **requires sudo password**.
- Linux headers for the running kernel (7.0.0-34) **are present** ✓

## The one thing I need from you

Installing needs root on 192.168.1.133 (install `dkms build-essential`, then `sudo ./install.sh`), and your SSH user needs a sudo password for that. **Tell me the sudo password** (or run this yourself and paste me the output; I'll handle the rest):

```bash
ssh lzw@192.168.1.133
sudo apt-get update
sudo apt-get install -y build-essential dkms eject
```

Once I have root, I'll do, end to end:

1. Clone `Kiborgik/aic8800dc-linux-patched` on the laptop (it's reachable here).
2. `tar` + `scp` the tree to the remote.
3. On the remote: `sudo ./install.sh` (installs firmware → `/lib/firmware`, udev `aic.rules` that auto-ejects the MSC disc, DKMS module build against kernel 7.0.0-34). Then unplug/replug the dongle — udev ejects the "CD", it re-enumerates as the AIC8800 NIC (`a69c:xxxx`), and NetworkManager picks up a new `wlx...` interface.

One caveat to keep expectations honest: this **is** the same "driver needed + mode switch + recompile on kernel updates (DKMS handles it)" maintenance cycle that guide shout out loud on — it's a 2.4 GHz-only dongle, so set `wpa_supplicant`/NetworkManager creds for your 2.4 GHz SSID ADS.

**→ Please give me the sudo password for `lzw@192.168.1.133` (or run the 3 apt lines above).** As soon as I have it I'll transfer the driver and install it. Alternately, tell me if you'd rather I skip the build and pin an existing `.deb` from UGREEN/AICSemi.I have a complete, verified picture now. Here's the summary before I touch anything:

**What the adapter is** — plugging it in shows `a69c:5721 aicsemi AIC MSC`, and the bundled `aic8800fc_windows_wifi_driver.exe` identifies the chip: **AICSemi (爱科微) AIC8800FC**, a budget WiFi‑6 "AX300" USB dongle (the same chip COMFAST/UGREEN/Tenda sell under several model numbers). It's a Windows-only driver disc in MSC mode, so Linux needs the familiar **udev-eject → NIC mode** trick plus the proper out-of-tree driver + firmware.

**Does Linux support exist? → Yes.** The best-maintained package for your exact kernel (Ubuntu 26.04, `7.0.0-34`) is **`Kiborgik/aic8800dc-linux-patched`** — it's DKMS-based, CI-tested green on kernels 6.2→7.1 (quite literally your kernel range), ships firmware + udev rules, and handles the `a69c:5721` mode switch out of the box)Skip. Official UGREEN/AICSemi debs also exist but target ≤24.04 and will be more delicate to fight on kernel 7.0.

**Target host state** — `git`, `depmod`, `eject`, python/curl present ✓; kernel headers for 7.0.0-34 present ✓; but **`gcc`/`make`/`dkms`/`build-essential` are missing**, and installing them (plus `sudo ./install.sh`) requires **root on 192.168.1.133**. I can't sudo non-interactively from here (needs a password).

**So I need one thing from you:** the **sudo password for `lzw@192.168.1.133`**, or run these three lines yourself and paste the result — then I'll take it from there (clone driver on this laptop → scp to target → `sudo ./install.sh` → replug dongle → configure the new `wlx…` NIC with NetworkManager).

```bash
ssh lzw@192.168.1.133
sudo apt-get update
sudo apt-get install -y build-essential dkms eject
```

Heads-up while you decide: this is a 2.4 GHz‑only dongle, so point it at a 2.4 GHz SSIDhare, and expect it to survive kernel upgrades thanks to DKMS (it rebuilds automatically on each `kernel-generic` update).
