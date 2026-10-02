---
audio: false
generated: true
image: false
lang: en
layout: post
title: CSM Procedure on MSI Z170A Verified
translated: false
type: note
---

Question: Is the claimed procedure for enabling CSM on the MSI Z170A Gaming M5 accurate?

Answer: Mostly yes, with a few things that are unverified or phrased too confidently.

**What checks out**

- MSI's FAQ gives the path BIOS setup → Settings → Advanced → Windows OS Configuration → Windows 8.1/10 WHQL Support = Disabled, and the Z170A Gaming M5 is on its model list.
- MSI's other FAQ says that when Boot Mode Select is greyed out as [UEFI], you should set Windows 10 WHQL Support to Disabled. The Z170A Gaming M5 is also listed there.
- Boot Mode Select (LEGACY+UEFI / UEFI) becomes un-selectable and is set automatically when WHQL Support is enabled. So the Disabled → check Boot Mode Select sequence is correct.
- MSI has no standalone "CSM" switch on this generation of board. A forum user noted there is no CSM on MSI boards and that the WHQL setting has a similar function.

**What I'd treat with caution**

- **The "Windows 10 WHQL Support = Enabled / UEFI" for Test B is fine.** Enabling it switches the system to UEFI mode. The extra line "CSM = Disabled" is redundant, because enabling WHQL does that for you.
- **"Above 4G Decoding" and "PCIe speed = Gen2" for the M40 are not covered by my sources.** I couldn't confirm that this BIOS has an Above 4G Decoding option, and the pasted text hedges with "if available". The Gen2 suggestion is a troubleshooting idea, not documented MSI guidance.
- **The BIOS version claim is unverified.** The text says the current version is 7977v1I, but I couldn't confirm that from the results. Check MSI's support page directly.
- **I couldn't verify the third MSI link.** The pasted text cites the BIOS manual page, and I didn't retrieve it. The Z170A PC Mate manual I found does show the same menu structure, though.
- **The links carry `utm_source=chatgpt.com` tracking tags,** so they were pulled from ChatGPT. The FAQ numbers (2622 and 2803) are real, though.

**Bottom line:** The core instruction is correct. Set Windows 10 WHQL Support to Disabled, then pick Legacy+UEFI under Boot Mode Select. Verify the M40-specific tweaks on your own board.

References:

- [MSI USA FAQ 2622: Windows OS Configuration](https://us.msi.com/faq/2622)
- [MSI FAQ 2803: Boot mode select greyed out](https://www.msi.com/faq/mb-2803)
- [MSI Z170A PC Mate manual: Windows OS Configuration](https://www.manualslib.com/manual/1020804/Msi-Z170a-Pc-Mate.html?page=45)
- [Tom's Hardware: BIOS settings for Win10 UEFI install](https://forums.tomshardware.com/threads/bios-settings-for-win10-uefi-install.3573007/)
