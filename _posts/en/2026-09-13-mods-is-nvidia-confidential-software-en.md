---
audio: false
generated: true
image: false
lang: en
layout: post
title: MODS is NVIDIA Confidential Software
translated: false
type: note
---

MODS is **not publicly available for download**. It's **NVIDIA confidential** software, as clearly stated throughout the document:

> *"The information in this document is confidential and is the property of NVIDIA Corporation. This document may not be distributed without prior NVIDIA authorization."*

> *"NVIDIA CONFIDENTIAL | Prepared and Provided Under NDA"*

## How to get MODS

**1. For NVIDIA partners/customers** — contact your **NVIDIA representative**:
> *"Please contact your NVIDIA representative about moving to Linux MODS."*

The document mentions MODS is distributed in packages with part numbers like **"618-60506-3501-CX0"** which have been qualified for specific products.

**2. For NVIDIA employees** — available on **NVIDIA's internal network**:
> *"NVIDIA distributes a turnkey Linux package that can be obtained on the internal NVIDIA network."*

**3. For everyone else** — you **cannot** download MODS directly. It's not on NVIDIA's public website, GitHub, or any public repository. It's provided exclusively to:
- NVIDIA's board partners (OEMs/ODMs)
- NVIDIA internal engineering teams
- Customers under NDA (Non-Disclosure Agreement)

## If you need GPU diagnostics

If you're not an NVIDIA partner and want to test consumer GPUs:

- **NVIDIA's public tools**: There is no public equivalent of MODS for end users
- **Standard NVIDIA driver**: Includes limited diagnostic capabilities via `nvidia-smi` and `nvidia-settings`
- **Third-party GPU tools**: Tools like GPU-Z, FurMark, OCCT, or 3DMark can do basic stress testing, but they don't have the low-level register/hardware access that MODS provides
- **For manufacturing defects**: Use the GPU vendor's RMA/warranty process

**Bottom line**: MODS is an internal NVIDIA manufacturing diagnostic tool. Unless you have an NDA/partnership with NVIDIA, you won't be able to obtain it.
