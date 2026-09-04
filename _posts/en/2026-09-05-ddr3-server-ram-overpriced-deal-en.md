---
audio: false
generated: true
image: false
lang: en
layout: post
title: DDR3 Server RAM Overpriced Deal
translated: false
type: note
---

## Question: Is 2×8GB Samsung 2Rx4 PC3L RAM for ¥160 a good deal?

**Answer: No — I would skip it at ¥160.**

The important part is **2Rx4 + PC3L**. This is very likely **DDR3L ECC Registered (RDIMM) server memory**, not normal desktop DDR3.

For example, Samsung M393B1K70DH0-YH9 is:

* **8GB**
* **DDR3L-1333**
* **PC3L-10600R**
* **ECC**
* **Registered / RDIMM**
* **2Rx4**
* **1.35V**
* 240-pin DIMM ([Compuram][1])

The seller saying **“my motherboard doesn't support it”** is actually a strong clue that it's server RDIMM.

### The big compatibility issue

You **cannot normally put RDIMM into an ordinary desktop DDR3 motherboard**.

For example:

```text
DDR3 UDIMM   ← normal desktop RAM
DDR3 ECC UDIMM
DDR3 ECC RDIMM ← this one
DDR3 LRDIMM
```

`RDIMM` has a register/buffer between the memory controller and DRAM chips. The motherboard/CPU must explicitly support it.

### ¥160 for two sticks

That's:

```text
¥160 / 16GB = ¥10/GB
```

That's expensive for old DDR3 server RAM.

Current listings show 8GB Samsung DDR3 ECC RDIMM around **$17–30 per stick** depending on speed/model, and used/server-pull pricing can be considerably lower. ([Newegg.com][2])

### [Samsung 8GB DDR3L 1066 2Rx4 RDIMM](https://www.newegg.com/supermicro-8gb/p/1X5-006W-00492?item=9SIAMBVK924851&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$17.56*

### [Samsung 8GB DDR3 1333 2Rx4 RDIMM](https://www.newegg.com/supermicro-8gb/p/1X5-006W-004B2?item=9SIAMBVK924872&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$17.56*

### [Samsung 8GB DDR3L 1600 2Rx4 RDIMM](https://www.newegg.com/supermicro-8gb/p/1X5-006W-004A0?item=9SIAMBVK924860&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$19.51*

**For your use case, I'd target ~¥30–50 per 8GB stick**, unless these are unusually high-speed or particularly desirable server modules.

If you're buying DDR3 specifically for your old Lenovo/other test machines, **send me the RAM label photo** and I can decode the exact Samsung part number and tell you whether ¥160 is worth it.

[1]: https://www.compuram.biz/memory_module/samsung/m393b1k70dh0-yh9.htm?utm_source=chatgpt.com "Samsung - M393B1K70DH0-YH9 8GB 240Pin DIMM DDR3L - Memory Module"
[2]: https://www.newegg.com/p/1X5-000A-001Z7?utm_source=chatgpt.com "SAMSUNG M393B1K70DH0-YH9Q9 DDR3 1333 8GB ECC REG 2RX4 - Newegg.com"
