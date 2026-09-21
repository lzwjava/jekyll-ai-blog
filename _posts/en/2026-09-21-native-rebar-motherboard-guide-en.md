---
audio: false
generated: true
image: false
lang: en
layout: post
title: Native ReBAR Motherboard Guide
translated: false
type: note
---

Question: **Which motherboard should I buy if I want ReBAR to work officially, so I don't need ReBarUEFI?**

Answer: The key distinction is that the ReBarUEFI issue is a list of **boards that need ReBarUEFI**, not a list of boards with official ReBAR support. The issue explicitly marks boards with `UEFIPatch: N` where the reporter got ReBAR working without the ReBarUEFI patch. ([GitHub][1])

If your goal is **“install motherboard → enable Above 4G Decoding + Re-Size BAR in BIOS → no custom UEFI / ReBarUEFI”**, then you should target a **newer platform**, rather than buying one of the old Z170/X99 boards from that list.

### Boards in the ReBarUEFI data that are explicitly reported as not needing the patch

| Motherboard                       | Platform   | GPU tested | ReBarUEFI patch |
| --------------------------------- | ---------- | ---------- | --------------- |
| Gigabyte X470 AORUS GAMING 5 WiFi | X470 / AM4 | Arc A770   | **No**          |
| Gigabyte B450 AORUS ELITE         | B450 / AM4 | RX 590     | **No**          |
| Gigabyte B450 AORUS M             | B450 / AM4 | RX 580     | **No**          |
| Gigabyte B450M Gaming             | B450 / AM4 | RX 6700 XT | **No**          |
| ASUS PRIME A320M-K                | A320 / AM4 | RX 6600    | **No**          |
| MSI B450M PRO-VDH MAX             | B450 / AM4 | RX 580     | **No**          |
| Gigabyte B550I AORUS PRO AX       | B550 / AM4 | RX 5600 XT | **No**          |

For example, the issue specifically says the **X470 AORUS GAMING 5 WiFi** BIOS officially supports ReBAR with Zen 3, while Zen 2 required the ReBarUEFI module. ([GitHub][1])

So if you're building a machine **today**, I would not use that GitHub issue as the motherboard-buying guide. It's primarily documenting how to make *unsupported/older firmware* work.

### The important rule

If you want **zero ReBarUEFI involvement**, buy a motherboard whose manufacturer's BIOS documentation explicitly exposes:

```text
Above 4G Decoding       [Enabled]
Re-Size BAR Support     [Enabled]
```

Modern AMD AM4/AM5 and Intel 10th-gen+ boards commonly have this natively.

For example, rather than buying an ASUS Z170-A because it has a successful ReBarUEFI report, you'd want a board where **ReBAR is a normal BIOS feature from the vendor**.

The ReBarUEFI project itself describes its purpose as adding Resizable BAR to systems that otherwise don't support it, so using a modern native-ReBAR platform makes the project unnecessary. ([GitHub][2])

**If you're specifically trying to build the cheapest machine for a GPU like an RX 6600/6700 XT or RTX 3060/3090, tell me the CPU + GPU you plan to use. I can narrow it down to specific cheap motherboards whose stock BIOS supports ReBAR, rather than relying on ReBarUEFI.**

[1]: https://github.com/xCuri0/ReBarUEFI/issues/11 "List of working motherboards · Issue #11 · xCuri0/ReBarUEFI · GitHub"
[2]: https://github.com/xCuri0/ReBarUEFI "GitHub - xCuri0/ReBarUEFI: Resizable BAR for (almost) any UEFI system · GitHub"