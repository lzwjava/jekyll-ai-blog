---
audio: false
generated: true
image: false
lang: en
layout: post
title: LSA Blocks Sangfor VPN DLL
translated: false
type: note
---

This is a great question about Windows security mechanisms. Let me break down why **sangfornspx64.dll** (a Sangfor VPN/network access component) gets blocked by the **Local Security Authority (LSA)** on Windows.

## The Core Reason: LSA Protection (RunAsPPL)

Windows LSA (specifically `lsass.exe`) enforces **Protected Process Light (PPL)** protection starting from Windows 8.1/10. This is a security hardening mechanism designed to prevent credential theft (like Mimikatz) by:

- Preventing non-Microsoft-signed DLLs from loading **into** the LSA process
- Blocking untrusted code from accessing the LSA's protected memory space

**Sangfornspx64.dll** likely attempts to load into or interact with the LSA process (e.g., as a **Security Support Provider (SSP)** or **Authentication Package**) to integrate Sangfor's VPN authentication with Windows logon. However, under LSA Protection:

1. **No Microsoft signature** → The DLL is blocked from loading into LSASS
2. **Not on the approved list** → Only Microsoft-signed DLLs or those from **Microsoft's exclusive whitelist** (e.g., some McAfee, Symantec, SentinelOne components) are allowed

## The Windows Event You'd See

```
Log Name: System
Source: Microsoft-Windows-Security-Mitigations/Kernel Mode
Event ID: 12
Description: "The Windows LSA has blocked an untrusted DLL from being loaded: C:\Program Files\Sangfor\...\sangfornspx64.dll"
```

## Solutions (if you need it to work)

| Method | What It Does | Security Risk |
|--------|-------------|---------------|
| **Disable LSA Protection** | Sets `HKLM\SYSTEM\CurrentControlSet\Control\Lsa\RunAsPPL` to `0` | **High** — exposes LSASS to credential theft |
| **Contact Sangfor** | Request a properly signed + Microsoft-approved version of the DLL | None (best option) |
| **Use a different VPN client** | Switch to one that's LSA-compatible (e.g., OpenVPN, WireGuard) | None |

## Quick Check

You can verify LSA Protection status with:

```powershell
Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" -Name "RunAsPPL"
```

A value of `2` means PPL is enforced (blocking Sangfor's DLL). A value of `0` would allow it — but that's not recommended security-wise.

**Bottom line:** The block is Windows' defense mechanism working as designed. Sangfor needs to submit its DLL to Microsoft for signing/whitelisting to be compatible with modern LSA Protection.