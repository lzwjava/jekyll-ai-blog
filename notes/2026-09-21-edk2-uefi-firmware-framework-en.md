---
audio: false
generated: true
image: false
lang: en
layout: post
title: EDK2 UEFI Firmware Framework
translated: false
type: note
---

**Question:** What is tianocore/edk2 and what does it do?

**Answer:**

**EDK II (EFI Development Kit II)** is a modern, open-source firmware development framework maintained by the TianoCore community. It is described as a modern, feature-rich, cross-platform firmware development environment for the UEFI and PI specifications from <www.uefi.org>.

In plain terms, it is the codebase used to build **UEFI firmware** — the software that initializes hardware and boots an operating system on most modern PCs, servers, and embedded devices.

**Key characteristics:**

- **Language:** Primarily C and Python
- **License:** BSD-2-Clause Plus Patent License (with some components under Apache, OpenSSL, etc.)
- **Hosted by:** TianoCore project (tianocore.org)
- **Stars / Forks:** ~6.2k stars, ~3.3k forks — a well-established, active project

**Major packages in the repository** (each is a self-contained module):

| Package | Purpose |
| --- | --- |
| `MdePkg` | Core UEFI library definitions |
| `MdeModulePkg` | Common UEFI drivers and applications |
| `OvmfPkg` | UEFI firmware for QEMU/KVM virtual machines |
| `ArmPkg` / `ArmVirtPkg` | ARM architecture support |
| `NetworkPkg` | Network stack (PXE, TLS, HTTP boot) |
| `SecurityPkg` | Secure Boot, TPM support |
| `ShellPkg` | UEFI Shell (a command-line environment) |
| `CryptoPkg` | Cryptographic libraries (OpenSSL, MbedTLS) |
| `EmulatorPkg` | Run UEFI in a host OS emulator for testing |

**CI support:** The project runs continuous integration across Windows (VS, CLANGPDB) and Ubuntu (GCC, CLANGPDB, CLANGDWARF) toolchains.

**Who uses it?** EDK II is the upstream foundation for firmware shipped in Intel platforms, QEMU/OVMF (used extensively in Linux virtualization), and many embedded/server platforms.

References:

- [tianocore/edk2 on GitHub](https://github.com/tianocore/edk2)
- [TianoCore Official Site](http://www.tianocore.org)
- [Getting Started with EDK II](https://www.tianocore.org/tianocore-wiki.github.io/development/tutorials-howto/getting_started_with_edk_ii.html)
