---
audio: false
generated: true
image: false
lang: en
layout: post
title: Swap Caps Lock and Ctrl in PowerToys
translated: false
type: note
---

Question: **In PowerToys, how do I switch Caps Lock and Ctrl keys on Windows?**

Answer:

Use **PowerToys Keyboard Manager** → **Remap a key**. PowerToys supports swapping keys by creating two remaps. ([Microsoft Learn][1])

Steps:

1. Open **PowerToys**
2. Go to:

```
Keyboard Manager
    → Remap a key
```

3. Click:

```
+ Add key remapping
```

4. Add these two mappings:

| Key       | Mapped To |
| --------- | --------- |
| Caps Lock | Left Ctrl |
| Left Ctrl | Caps Lock |

Example:

```
Caps Lock  →  Ctrl (Left)
Ctrl (Left) → Caps Lock
```

5. Click **OK** / **Apply**

PowerToys will warn that a key is being reassigned. Confirm it. ([Microsoft Learn][1])

6. Make sure:

```
PowerToys Settings
    → General
    → Run at startup = ON
```

because Keyboard Manager works while PowerToys is running. ([GitHub][2])

For programmers, a more common setup is:

```
Caps Lock → Ctrl
Left Ctrl → Ctrl (keep normal)
```

because Caps Lock is in a much better ergonomic position for `Ctrl+C`, `Ctrl+V`, `Ctrl+A`, terminal shortcuts, Vim, Emacs, etc.

If you want a **true hardware-level swap** (works before Windows boots, BIOS, Linux, etc.), use keyboard firmware tools like QMK/VIA or registry scancode mapping instead of PowerToys.

[1]: https://learn.microsoft.com/en-us/windows/powertoys/keyboard-manager?utm_source=chatgpt.com "Remap Keys and Shortcuts with PowerToys Keyboard Manager | Microsoft Learn"
[2]: https://github.com/microsoft/PowerToys/wiki/Keyboard-Manager-Overview/c339bd7b3fa4bc152bbb8fcf2f96a696076ecc84?utm_source=chatgpt.com "Keyboard Manager Overview · microsoft/PowerToys Wiki · GitHub"
