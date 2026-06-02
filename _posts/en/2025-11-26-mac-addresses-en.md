---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Understanding MAC Addresses
translated: false
type: note
---

Yes, you're basically correct! Here's a clear and complete explanation of what a **MAC address** (always written in uppercase as **MAC**) is:

### What is a MAC address?

- **MAC** = **Media Access Control** address
- It's a **unique 48-bit hardware identifier** (usually written as 6 groups of 2 hexadecimal digits, e.g., `00:1A:2B:3C:4D:5E` or `00-1A-2B-3C-4D-5E`)
- It is **burned into the hardware** of a network interface (Ethernet card, Wi-Fi card, Bluetooth chip, etc.) by the manufacturer at the factory.
- It operates at **Layer 2 (Data Link layer)** of the OSI model — used for local network communication (within the same LAN/broadcast domain).

### Key characteristics you got right

- **Hardware-bound**: Yes, it's tied to the physical network interface controller (NIC).
- **Assigned at factory**: The first half (first 3 bytes = 24 bits) is the **OUI** (Organizationally Unique Identifier), assigned by the IEEE to the manufacturer (e.g., Apple, Intel, Realtek, etc.).
- **Globally managed**: The IEEE maintains a public registry so (in theory) no two devices in the world should have the same MAC if properly manufactured.
- **Not supposed to change**: The real hardware MAC is permanent.

### But… there are important exceptions (software can override it)

Even though the real burned-in MAC is fixed, **most operating systems allow you to temporarily change/spoof the MAC address in software**:

- Windows: Through device manager or tools like TMAC
- Linux/macOS: `ifconfig`, `ip link`, or `macchanger`
- Purpose: Privacy (e.g., on public Wi-Fi), testing, bypassing MAC-based restrictions, etc.

When you spoof it:

- The device tells the network: "Hi, my MAC is now XX:XX:XX:XX:XX:XX"
- This change is **temporary** — disappears after reboot (unless scripted)
- The **real burned-in MAC** remains unchanged in the hardware

### Summary table

| Property                    | True for real MAC? | Can be changed in software? |
|-----------------------------|--------------------|-----------------------------|
| Assigned by manufacturer    | Yes                | No                          |
| Globally unique (ideally)   | Yes                | Only if not spoofed         |
| Burned into NIC hardware    | Yes                | No                          |
| Used for local LAN delivery | Yes                | Yes (even if spoofed)       |
| Can be temporarily changed  | —                  | Yes (spoofing)              |
| Survives OS reinstall       | Yes                | No (spoofed one is lost)    |

### Quick way to see your current MAC

- Windows: `getmac` or `ipconfig /all`
- Linux/macOS: `ifconfig` or `ip link`

So yes — you're 95% correct: the **real** MAC address is permanent, hardware-bound, and globally administered. The only reason people say "MAC can be changed" is because of software spoofing, which doesn't touch the actual hardware value.
