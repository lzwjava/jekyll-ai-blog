---
audio: false
generated: true
image: false
lang: en
layout: post
title: X99 Chinese Knockoff Motherboard
translated: false
type: note
---

Question: What does “X99 必寨板” mean?

Answer: It almost certainly means **“X99 必寨板” = X99 Bìzhài board**, i.e. an **X99 Chinese knockoff / budget motherboard**, not an official Intel motherboard brand.

![Image](https://images.openai.com/static-rsc-4/T0uIh5ohOo1HCV4Eph5Ik1WNKn9NAwvhClyZ1qUwhzdZGEzArvBLFX7WXgb836NtuMu52zaLO90zBkA7so8c5kwRqCAcfmltjUot5q6Y_Wprd2RoYLc2UXMFC_iUa7FWBiGoJlUi1p5TIbufOTn7X8VJEfvYj6V9_9tP58lA_NpCZ0sLWbvWvkgL_RcQNd4N?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/FMC-cBfAjYFoSY-h0hJbYUnsnW_Ak5Lui2mPwWDJTpxCaSfNKLzvKkiiDas6lbAMR8iVLc9uFSLtwUPQ68zzRC3qimh8k8mCmhj_XWosdIOmyVZ4L-9X3pQ0SQyKMwAUKBOIACgKvmacAPK3pflossNaR69UfulEVPdcIVyDW8JEoIop9t2ksmCzdDCOZtQw?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/DtrAW1ST8XEicNtxJSZ4O244Owwo3vH_e1q8WlUIgclwsfV_SOP2hWLnMY9DjQkdmBysR2Ca7Wg0pCdsU68dZoNb29EW3IxrCkgxXN949bB-5NCg4TqQQXQaRfz0NKRa-8szKyQ-P4Z006_DjOaDBx57dYz-8YJAnCFmzhDoQbeT-71VLD0H7i9Jg9YmoECc?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/tLtCTh6JePUYoiDIF43GtrV-1BZLPMc_fnySY-l3w40nmPpmE1P78G8miii4TfaVUr95MkYl41nGz4u_5fuAZCdi-J--suvjLNzmCkXZzSooV2QytgM9JZjRooNPAfomk57rFjqM9WigyFxk9RCt9tj-iUBS0jcnU6135NJwtRa9tSRAgXPaUjBOkLohUocD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/mk7MIauoGpO0UTqFJnVIn4bdqFmWFIunBAZxeJEe68u_RiETq9osHqyYEZ6fiPRrUWh65CR-HvcluwicI9cSxF5CAb_8ARfts8O08dpxmP0CNJ4PtPmEE8uelBzkOXbXuM5DBH_GsqTgPpctY6rHUEIhthIN7J994y4hA51myV5jtgCrKw7FQlB0pss7Q26w?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/TuPqbJ-ZuShmEIHbukvqUqDY8hqszKikMXO3lgcd05FN8609D0mTMJkD4UXQLan9XWz5_3XMndHF-wG07BxzONpjjj51hSKjJvM4Dz_px6sa-S5uC-HSimzRNa7i4XMz5nhv3_bNssIVfQJn9Cn1xYmkqeBV1X8C0Tqn7XtLGJcSeEDQdbPOeYo7OQ5DcxEY?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/1wVWkMaBC2N4GMh9kBQyRFyOyYoR6LNTdtf6zMoodPfWd1AM8X19uZf3M6mQ2IIMcTWhrcCj61vnLJte3POEHY3T1v30FqVqJK_-MJJQfyN2DSnbosI_oXKjBqUHZ4x9h-H4pCX8RFGdULMtNqHdkaooRkIWLbBPfiF1vpVPDqkr1vt5Mts00yh0lp5LzUUH?purpose=fullsize)

### What is X99?

**X99** is Intel's chipset/platform generation for **LGA2011-3** CPUs, mainly around 2014–2016.

Typical CPUs:

```text
Xeon E5-26xx v3/v4
Xeon E5-2680 v4
Xeon E5-2690 v4
Xeon E5-2699 v4
Core i7-5820K
Core i7-5960X
```

The interesting part for GPU repair is that these systems are **cheap on the used market**, but they're relatively old and sometimes quirky.

### What does “寨板” mean?

Chinese PC communities use **寨板** for unofficial/low-cost motherboards, often produced by smaller Chinese manufacturers.

For example:

```text
Original:
ASUS X99-Deluxe
MSI X99A
Gigabyte X99
        ↓
expensive / proper retail boards

寨板:
某某 X99
HUANANZHI X99
JINGSHA X99
Machinist X99
        ↓
cheap / simplified / sometimes weird BIOS
```

“寨” literally means something like **stockade**, but in tech slang it means **knockoff / no-name / highly cost-optimized**.

### Why your friend said “avoid X99”

Your friend's recommendation was:

> 测显卡最好避开 X99，用核显就行
> H81主板，4代U。便宜随便折腾

The important distinction is **GPU repair testing**, not normal PC usage.

An X99 + Xeon system often has:

```text
Xeon E5
   ↓
NO integrated GPU
   ↓
You need a discrete GPU just to get display
   ↓
Testing a "bad GPU" becomes harder
```

Whereas:

```text
H81
+
4th-gen Intel CPU with iGPU
        ↓
Intel HD Graphics
        ↓
Machine can boot/display without your test GPU
        ↓
Insert suspected GPU
        ↓
Test it independently
```

For GPU repair, that's much nicer.

For example:

```text
H81 + i5-4570
        │
        ├── motherboard video output → baseline display
        │
        └── PCIe slot
              │
              └── GPU under repair
```

If the GPU doesn't initialize, you still have the **Intel iGPU** to see BIOS/OS and diagnose what happened.

**So your friend's “H81 + 4代U” recommendation is basically a cheap GPU-repair test platform.**
