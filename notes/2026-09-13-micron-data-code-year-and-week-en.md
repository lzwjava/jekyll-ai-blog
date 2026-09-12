---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Micron Data Code: Year and Week?"
translated: false
type: note
---

Question: **Can the Micron data code tell us the manufacturing year and week?**

Answer: **Yes, generally — but not from `D9WCW` itself.**

In a Micron marking such as:

```text
D9WCW
8YA77
```

* `D9WCW` is the **Micron FBGA part/marking identifier** (the die/package code).
* `8YA77` is a **data/lot code**, and the relevant portion can encode manufacturing/trace information.
* The `77` at the end is **not simply “week 77”**. You need Micron's specific date/lot-code decoding scheme for that generation.

For the 2018-era Micron sheet you're quoting, the distinction between:

```text
8**77
8YA77
8ZA77
```

is therefore useful for identifying **manufacturing/lot variants**, but I wouldn't assume `8YA77 → year 2018, week 77`.

If you have a **photo of the actual marking on the GDDR6 chip**, I can decode the marking character-by-character and see whether we can determine the production date/week.

The particularly interesting question is whether the **`8` = year/period and `77` = fab/lot/week encoding**, because Micron's coding changed across product generations.
