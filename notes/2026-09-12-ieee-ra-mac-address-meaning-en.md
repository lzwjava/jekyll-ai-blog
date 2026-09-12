---
audio: false
generated: true
image: false
lang: en
layout: post
title: IEEE RA MAC Address Meaning
translated: false
type: note
---

Question: What does **IEEE RA** mean when assigning a MAC address?

Answer: **IEEE RA = IEEE Registration Authority**.

When you assign MAC addresses, IEEE RA is the organization/service responsible for allocating globally unique MAC-address prefixes (and related identifiers) to companies.

For example:

```text
MAC address:  00:1B:21:12:34:56
              └──────┘
              OUI
```

The first **24 bits** (`00:1B:21`) are typically an **OUI (Organizationally Unique Identifier)** allocated by the IEEE Registration Authority. A company then manages the remaining bits to create unique MAC addresses:

```text
IEEE RA
   │
   └── assigns OUI: 00:1B:21
                    │
                    ├── device 1: 00:1B:21:00:00:01
                    ├── device 2: 00:1B:21:00:00:02
                    └── ...
```

### In practice

If you're looking at an **"Assign MAC Address"** form, "IEEE RA" usually means **you need an identifier allocated by IEEE**, rather than randomly choosing a MAC prefix.

IEEE has several relevant identifier types:

* **MA-L** — traditionally equivalent to an OUI; 24-bit prefix
* **MA-M** — 28-bit prefix
* **MA-S** — 36-bit prefix

For a hardware vendor manufacturing Ethernet/Wi-Fi devices, this is how you get a legitimate globally unique address space.

[IEEE Registration Authority — MAC Address Block Registration](https://standards.ieee.org/products-programs/regauth/tut/mac/?utm_source=chatgpt.com)

If you tell me what **"Assign MAC Address"** screen/form you're looking at, I can explain exactly what value IEEE RA expects there.
