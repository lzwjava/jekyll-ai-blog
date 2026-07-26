---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Intel VMD: The Missing Culprit"
translated: false
type: note
---

Good analysis overall — you've correctly identified the key facts and ruled out partition issues. But I think the proposed next steps are **missing the most likely culprit**. Let me dig deeper on `0xC19001F4`.

## My Assessment

### What's Right in Your Summary ✅

- `clean` + `convert gpt` was the correct fix for the Linux LVM/RAID signatures
- Setup's auto-partitioning of unallocated space is fine — no need to manually create partitions
- Hands-off test is a smart debugging step
- Hardware diagnostics are premature right now

### What I'd Re-evaluate 🔍

**The `0xC19001F4` error** at `CSetupManager::OnFinishLaunchChoiceAction(8149)` means Windows Setup is **receiving a signal to abort the install and launch recovery instead** — at the exact same point, twice in a row. That rules out random flakiness. Something deterministic is triggering it.

**The top suspect isn't the USB stick — it's the Intel VMD / RST controller mode.**

### Why I Think This

On many Lenovo laptops (especially Xiaoxin models with Intel 11th/12th/13th Gen), the BIOS has a setting like:

> **"Intel VMD Controller"** or **"Intel RST with Optane"** — typically set to **Enabled**

When VMD is enabled:

1. Windows Setup *can* see the NVMe drive during the WinPE phase (the ISO has basic NVMe drivers)
2. Setup copies files successfully
3. **After first reboot**, Windows boots from the NVMe using its in-box `stornvme.sys` driver
4. That driver **can't talk to the NVMe through the VMD controller** — the drive goes invisible
5. Windows hits a boot failure → launches recovery → Setup sees this and self-aborts with `0xC19001F4`

This explains perfectly why:

- The drive *appears* in the partition selection screen
- The install *starts* copying files
- It fails *consistently at the same point* after the first reboot
- The error is about "launch recovery environment"

### Recommended Next Steps (revised priority)

**Step 1 — Check BIOS for Intel VMD / RST setting** (takes 2 minutes)

Reboot → press `F2` → look for:

- `Intel VMD Controller` → **Disable it**
- `Intel RST with Optane` → set to **AHCI** or **non-VMD/non-RST**

This is the **#1 cause** of this exact failure pattern on Lenovo laptops.

**Step 2 — Fresh ISO + fresh USB** (your original proposal)

If VMD is already off, then yes — new ISO and a different USB stick. SHA-1 verify the download first to save time.

**Step 3 — Hands-off install**

If Steps 1–2 still fail, then do the hands-off test.

**Step 4 — Hardware diagnostics**

Only if Steps 1–3 all fail. MemTest86 and NVMe health check.

---

What do you think? Want to check the BIOS VMD setting first? That's the 5-minute test that's most likely to fix it.
