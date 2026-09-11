---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disable Secure Boot on ASUS A68HM-E
translated: false
type: note
---

Question: **How do I disable Secure Boot on the ASUS A68HM-E UEFI BIOS?**

Answer: On the **ASUS A68HM-E**, Secure Boot is under **Boot → Secure Boot**. The A68HM-E manual explicitly shows both **CSM** and **Secure Boot** in the Boot menu. ([ASUS Download Center][1])

### Disable it

1. Enter BIOS with **Del** during power-on.
2. Press **F7** → **Advanced Mode**.
3. Go to:

```text
Boot
 ├── CSM (Compatibility Support Module)
 └── Secure Boot
```

4. Open **Secure Boot**.
5. Look for:

```text
OS Type
```

Set it to:

```text
Other OS
```

rather than:

```text
Windows UEFI mode
```

On ASUS UEFI firmware, `Other OS` is the setting intended for non-Secure-Boot operating systems. ([ASUS Download Center][2])

6. Press **F10** → **Yes** to save and reboot.

### If `Secure Boot State` still says Enabled

On this generation of ASUS firmware, you may also need to deal with **CSM**.

Try:

```text
Boot
  → CSM
      → Launch CSM = Enabled
```

For an old test/repair machine, **CSM Enabled + Secure Boot effectively not enforced** is usually what you want, especially if you're booting older Linux/tools or legacy Option ROMs. ASUS documents that CSM is specifically for compatibility with non-UEFI devices. ([ASUS Download Center][2])

For your **GPU repair/MATS/MODS test machine**, I'd actually use:

```text
Boot
├── CSM
│   └── Launch CSM = Enabled
│
└── Secure Boot
    └── OS Type = Other OS
```

That gives you maximum compatibility with old GPUs, legacy boot media, and diagnostic environments.

If you show me a **photo/screenshot of the A68HM-E's current Secure Boot page**, I can tell you exactly which field to change.

I can also walk through the **A68HM-E BIOS settings specifically for using the iGPU as primary display while testing a bad discrete GPU**, which is probably the more useful configuration for your MATS work.

[1]: https://dlcdnet.asus.com/pub/ASUS/mb/SocketFM2/A68HM-E/E9808_A68HM_Series_Manual_Print_vendor_only.pdf?utm_source=chatgpt.com "2.8 Boot menu"
[2]: https://dlcdnets.asus.com/pub/ASUS/mb/SocketFM2/A68HM-F/E10355_A68HM-F_Manual_WEB.pdf?utm_source=chatgpt.com "Launch CSM [Enabled]"
