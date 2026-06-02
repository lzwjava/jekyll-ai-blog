---
audio: false
generated: true
image: false
lang: en
layout: post
title: BIOS Functions and Key Uses
translated: false
type: note
---

Question: What can we use BIOS for?

Answer:

**BIOS** (Basic Input/Output System) is firmware stored on your computer's motherboard. It serves as the very first software that runs when you power on a PC. While most modern computers (especially after ~2012–2020) have replaced traditional **legacy BIOS** with **UEFI** (a more advanced successor), the term "BIOS" is still widely used to refer to the setup interface even on UEFI systems.

Here are the main things BIOS is used for:

### Core Functions During Startup (Everyone Uses This Automatically)

- Performs the **Power-On Self-Test (POST)** — checks that essential hardware (CPU, RAM, graphics card, storage devices, keyboard, etc.) is present and working correctly.
- Initializes and configures hardware components so they are ready for the operating system.
- Locates a boot device (hard drive, SSD, USB, etc.) and loads the bootloader, which then starts your operating system (Windows, Linux, etc.).

Without this process your computer simply would not start.

### Practical Uses — What Users Do in the BIOS Setup Screen

You can enter the BIOS setup (usually by pressing Del, F2, F10, or Esc during startup — it varies by motherboard) to manually control several important settings:

- Change the **boot order** (e.g., boot from USB first to install Windows or try Linux from a flash drive)
- Enable or disable **Secure Boot** (mostly in UEFI mode — helps prevent malware during boot)
- Turn hardware features on/off (integrated graphics, onboard audio, certain USB ports, TPM for security, etc.)
- Overclock CPU, memory, or adjust voltages and timings (common for gamers and performance enthusiasts — requires caution)
- Set system date and time
- Enable/disable **Fast Boot** or other startup optimizations
- Configure **fan speeds** and cooling profiles (on many modern motherboards)
- Reset settings to default if the system becomes unstable after changes
- View basic hardware information (CPU temperature, detected RAM amount, storage devices, etc.)

### Additional / Less Common Uses

- Update the BIOS/UEFI firmware itself to add support for new CPUs, fix bugs, improve stability, or unlock new features.
- Troubleshoot hardware problems (POST beeps or codes often point to issues BIOS detects).
- In very old systems (pre-UEFI era), BIOS provided direct low-level access for DOS programs to control hardware (keyboard, screen, disks) — this is almost never needed today.

**Important note for 2026**:
Most new motherboards and PCs use **UEFI** instead of classic BIOS. UEFI offers faster boot times, support for drives >2 TB, a graphical mouse-friendly interface, better security, and more features. However, people still say "enter the BIOS" even when they mean the UEFI setup utility.

In short — BIOS (or UEFI) is mainly used to:

- Make the computer start properly every time
- Customize boot behavior and hardware settings
- Solve startup or compatibility problems

References:

- [https://en.wikipedia.org/wiki/BIOS](https://en.wikipedia.org/wiki/BIOS)
- [https://www.techtarget.com/whatis/definition/BIOS-basic-input-output-system](https://www.techtarget.com/whatis/definition/BIOS-basic-input-output-system)
- [https://superops.com/blog/what-is-bios](https://superops.com/blog/what-is-bios)
- [https://www.trentonsystems.com/en-gb/blog/what-is-bios](https://www.trentonsystems.com/en-gb/blog/what-is-bios)
