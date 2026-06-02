---
audio: false
generated: true
image: false
lang: en
layout: post
title: DMIT LAX Eyeball Plan Details Explained
translated: false
type: note
---

Question: What is the DMIT LAX AN5 EB TINY plan? Does it have 1500GB traffic? What is the price? Why do some listings show only 1000GB traffic?

Answer:

## DMIT LAX.AN5.EB.TINY — Full Breakdown

### What Does the Name Mean?

DMIT's product naming follows a standard structure: **Location + Hardware Platform + Network Line + Plan Size**. So `LAX.AN5.EB.TINY` means:
- **LAX** = Los Angeles datacenter
- **AN5** = AMD EPYC 9005 (AN5) hardware platform
- **EB** = Eyeball Network routing
- **TINY** = Entry-level plan size

---

### Specs of LAX.AN5.EB.TINY

The LAX.AN5.EB.TINY plan includes:
- **vCPU:** 1 vCore
- **RAM:** 2.0 GB
- **Storage:** 20 GB SSD
- **Routing Profile:** Eyeball (EB)
- **IPv4:** 1 IPv4
- **IPv6:** 1 IPv6 /64
- **DDoS Protection:** Standard
- **Transfer:** Bidirectional **1500 GB** @ 2 Gbps
- **Unmetered fallback:** @ 4 Mbps (after quota exceeded)
- **Price: $12.98/month**

---

### What is the "Eyeball" (EB) Network?

The LAX.AN5.EB profile includes Tier 1 + Reasonable Effort For China Routing via CMIN2 or similar Chinese ISPs.

More specifically: The LA Eyeball series uses CMIN2 routing — China Telecom and Unicom go out via CN2 premium routes, China Mobile uses CMIN2, and all three carriers return via CMIN2. IPv6 also runs CMIN2 bidirectionally.

---

### Price

The standard monthly price is **$12.98/month**. However, there is a notable promo code available:

Use code `LAX-EB-LAUNCH-NON-MONTHLY-RECURRING-20OFF` to get a **permanent 20% recurring discount** on the LAX Eyeball series when paying quarterly or annually. This is not a one-time discount — it recurs every billing cycle and works on TINY plans and above.

So with the promo code on quarterly/annual billing, the effective price drops to approximately **~$10.38/month**.

---

### Why Do Some Listings Show 1000GB Instead of 1500GB?

This is a key distinction between the **EB (Eyeball)** and **Pro (Premium)** series at the TINY tier:

The **LAX.AN5.Pro.TINY** (Premium/CN2 GIA routing) gives only **1000 GB** bidirectional traffic at 1 Gbps for $12.98/month, while the EB.TINY gives **1500 GB** at 2 Gbps for the same price.

EB plans give significantly more transfer quota than Pro at the same price — worth it if you don't specifically need CN2 GIA routing.

In short, the **1000GB** figure you see belongs to the **Pro (CN2 GIA) TINY** plan, not the EB TINY. The routing is different:
- **Pro** = CN2 GIA (higher quality for China Telecom, but less bandwidth quota, 1 Gbps port)
- **EB** = CMIN2 Eyeball (more bandwidth quota 1500GB, 2 Gbps port, slightly less premium routing)

---

### What Happens After You Exceed the Quota?

DMIT doesn't cut you off when you exceed your bandwidth allocation. Instead, they throttle your speed. For LAX.EB.TINY (and Pro.TINY), the throttle after quota is exceeded is **4 Mbps** — your service stays online, just slower. This is more predictable than surprise overage charges or sudden service interruptions.

---

### Summary Table

| Feature | LAX.AN5.EB.TINY | LAX.AN5.Pro.TINY |
|---|---|---|
| Traffic | **1500 GB** (BIDI) | **1000 GB** (BIDI) |
| Port Speed | 2 Gbps | 1 Gbps |
| Price | $12.98/mo | $12.98/mo |
| Routing | CMIN2 Eyeball | CN2 GIA Premium |
| After quota | 4 Mbps throttle | 4 Mbps throttle |
| Availability | In Stock | Often Out of Stock |

References:

- [DMIT Pricing Page](https://www.dmit.io/pages/pricing)
- [DMIT Shopping Cart (Live Specs)](https://www.dmit.io/cart.php)
- [DMIT Cloud Instance Page](https://www.dmit.io/pages/cloud-instance)
- [AN5 Platform Upgrade Details (GitHub)](https://github.com/yygr61/dmit-an5-premium-plans)
- [DMIT Promo Codes 2026 (GitHub)](https://github.com/jjleyw3/DMIT)
