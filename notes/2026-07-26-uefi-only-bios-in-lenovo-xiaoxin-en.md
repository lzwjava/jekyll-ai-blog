---
audio: false
generated: true
image: false
lang: en
layout: post
title: UEFI-Only BIOS in Lenovo Xiaoxin
translated: false
type: note
---

Question: Can't find a UEFI/Legacy toggle in Lenovo Xiaoxin BIOS (id string LACN36WW) — where is it, or does it even exist?

Answer: I couldn't find exact documentation for `LACN36WW` specifically, but based on the naming pattern (`XXCN36WW`), this matches recent Lenovo consumer BIOS builds (Insyde H2O firmware) used on 2022+ Xiaoxin/IdeaPad/gaming models. **Important: most of these newer Xiaoxin models don't have a Legacy/CSM toggle at all — they ship UEFI-only.** So if you're not finding it, that's likely because it genuinely isn't there, not because you're looking in the wrong place.

To confirm, get into BIOS first:
1. Power off completely.
2. Press the **Novo button** (tiny pinhole button on the side, next to power port) with a paperclip, OR power on and immediately mash `Fn+F2` or `F2`.
3. You'll land in Insyde H2O setup — tabs across the top: **Main / Configuration / Security / Boot / Exit**.
4. Check **Boot** tab — look for "Boot Mode," "UEFI/Legacy," or "CSM Support." If it's just showing **"Boot Mode: UEFI"** with no dropdown/other option, that confirms UEFI-only firmware — nothing to change here.
5. Check **Security** tab for **Secure Boot** — this is more likely to matter on these models. Try toggling it **off** if it's on (Windows 11 installs fine either way, but sometimes a fresh GPT disk with Secure Boot enabled + missing ESP trips up).

**Given this, my earlier "CSM/Legacy mismatch" theory is probably wrong for your hardware** — since it's UEFI-only anyway, the missing ESP on Disk 0 was actually caused by something else: likely you ran `convert gpt` on a disk that Windows Setup then still treated with an MBR-style partition creation because the **partition style flag was stale** from the previous `clean` — or Setup was in a weird state from the earlier failed attempt.

**Simplest fix, skip the BIOS hunt:** just redo the diskpart clean fully fresh:
```
diskpart
list disk
select disk 0
clean
convert gpt
exit
```
Then Refresh → select unallocated → Next, and check carefully this time whether **EFI System Partition** appears in the list after Setup auto-creates partitions (before you click Next again). If it appears, you're fine regardless of BIOS boot mode.

References:
- [Lenovo BIOS builds reference - Wim's BIOS](https://www.wimsbios.com/biosupdates/lenovo.jsp)
- [Insyde H2O UEFI setup navigation](https://neosmart.net/wiki/enable-uefi-boot/)
