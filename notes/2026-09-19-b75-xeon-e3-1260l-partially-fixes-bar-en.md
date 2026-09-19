---
audio: false
generated: true
image: false
lang: en
layout: post
title: B75 Xeon E3-1260L Partially Fixes BAR
translated: false
type: note
---

Question: Would an ASUS B75 board with Intel Xeon E3-1260L fix the Tesla M40 BAR allocation problem?

Answer:

This is a **significantly better platform** for the M40. Let me break it down:

---

## Hardware Profile

| Item | Detail |
| --- | --- |
| Board | ASUS B75 series (B75M-A / P8B75-M / etc.) |
| CPU | Intel Xeon E3-1260L (Sandy Bridge, LGA1155, 45W TDP) |
| Chipset | Intel B75 Express |
| PCIe | Gen 3.0 x16 (from CPU directly) |
| RAM support | Up to 32 GB DDR3 ECC |
| GPU | Tesla M40 12 GB |

---

## Does It Solve the BAR Problem?

**Partially better, but the core issue remains firmware-dependent.**

### ✅ What improves

| Factor | A68HM-E | B75 + E3-1260L |
| --- | --- | --- |
| PCIe version | Gen 2.0 | Gen 3.0 → 2× bandwidth |
| ECC RAM support | No | **Yes** — E3-1260L supports ECC, pairs well with M40 |
| Platform maturity | Budget 2014 APU board | Mainstream 2012 workstation chipset |
| BIOS options | Very limited | More complete AMI UEFI |
| Xeon validation | N/A | M40 is a Xeon-class companion card |

### ⚠️ The BAR problem — still depends on BIOS

The Intel B75 chipset **does support Above 4G Decoding in principle**, but whether ASUS exposes it in the BIOS depends on the specific board revision and BIOS version.

**Key fact:** B75 was a mainstream/budget chipset (below Z77/H77). ASUS did not always expose Above 4G Decoding on B75 boards — it was more commonly found on Z77 and server boards (C216).

---

## Check Matrix

| Board | Above 4G Likely? | Notes |
| --- | --- | --- |
| ASUS P8B75-M | Uncertain | Check latest BIOS |
| ASUS B75M-A | Uncertain | Check latest BIOS |
| ASUS P8B75-V | More likely | Larger board, more BIOS options |
| **Intel DQ77MK** | **Yes** | Q77 chipset, confirmed Above 4G |
| **ASUS P8Z77-V** | **Yes** | Z77, best consumer option |
| **Server board (C216)** | **Yes** | Best choice for M40 |

---

## The Xeon E3-1260L Specifically

This CPU is actually an excellent match for the M40:

- **ECC support** — the M40 uses ECC internally; having ECC system RAM too means a fully error-corrected compute stack
- **45W TDP** — very low power for a quad-core Xeon, good for a system that also has a 250W passive GPU
- **VT-d support** — enables GPU passthrough to VMs if needed
- **No iGPU** — the 1260L has **no integrated graphics**, same situation as the Athlon X4 850, so you still need a separate display adapter or run headless

---

## Honest Recommendation

If you're choosing between the two boards:

```
A68HM-E + Athlon X4 850   →  Poor choice for M40
B75 + Xeon E3-1260L       →  Better, but still uncertain on Above 4G
```

**If you want a guaranteed working platform for the M40, the ideal options are:**

1. **Any Intel C216 server board** (e.g., ASUS P8C WS, Supermicro X9SRA) — designed for Xeon E3 + workstation GPUs, Above 4G is always present
2. **Intel Z77 board** (e.g., ASUS P8Z77-V) — enthusiast chipset, BIOS options are complete
3. **Any modern board (200-series Intel or newer)** — Above 4G Decoding is standard since Kaby Lake era

---

## Bottom Line

The B75 + E3-1260L **might work** if that specific ASUS board's BIOS exposes Above 4G Decoding. Before buying or swapping, check:

```bash
# On the B75 system, boot into BIOS and look for:
Advanced → System Agent Configuration → Above 4G Decoding
# or
Advanced → PCI Subsystem Settings → Above 4G Decoding
```

If the option is there → **M40 will very likely work on that board.**
If it's absent → same dead end as the A68HM-E.

Would you like me to help identify a specific ASUS B75 board model you have, or recommend the cheapest confirmed-working platform for the M40?
