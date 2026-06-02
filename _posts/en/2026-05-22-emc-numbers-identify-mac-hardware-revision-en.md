---
audio: false
generated: true
image: false
lang: en
layout: post
title: EMC Numbers Identify Mac Hardware Revision
translated: false
type: note
---

**Question:** What does "EMC" mean in the context of Apple Mac models?

**Answer:**

**EMC = Electro-Magnetic Compatibility** — but in Apple's context it's used as an **internal model identifier number**, not a description of electromagnetic properties.

Apple assigns an EMC number to every product they submit for FCC/regulatory certification. It's essentially Apple's internal revision code stamped on the bottom of the machine and used in regulatory filings.

**Why it matters practically:**

The same model name (e.g. "MacBook Pro 13-inch A1708") can have **multiple hardware revisions** with different EMC numbers:

| EMC | Year | CPU Generation |
|-----|------|---------------|
| EMC 2978 | Late 2016 | Skylake (i5-6360U) |
| EMC 3164 | Mid 2017 | Kaby Lake (i5-7360U) |

Both are A1708, but different EMC = different internals. When buying parts (battery, screen, keyboard), the EMC number ensures you get the **exact right part** for your specific revision — even when the outer model number is identical.

**Where to find it:**

- Printed on the bottom case of the Mac
- Apple menu → About This Mac → System Report → Model Identifier area
- On the original box

**TL;DR:** EMC is Apple's regulatory filing revision number, repurposed as a hardware revision tag. When buying replacement parts, match the EMC number to guarantee compatibility.
