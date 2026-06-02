---
audio: false
generated: true
image: false
lang: en
layout: post
title: DigitalOcean Volume Size Requirements
translated: false
type: note
---

The AMD Dev Cloud volume UI likely expects a specific format or unit. Let me check.Key finding: AMD Dev Cloud is actually built on DigitalOcean under the hood — it redirects to DigitalOcean and deploys GPU Droplets. So the volume UI is DigitalOcean's.

**The issue:** DigitalOcean Volumes have a **minimum size of 1 GiB and the field expects an integer in GiB**, but there's also a **minimum of 1 GiB and maximum of 16,384 GiB**. The most common cause of "invalid size" when typing `200` is:

1. **You're in the wrong field** — it might expect `200 GiB` but the UI shows a dropdown for units (GiB vs TiB) and you may have the unit set wrong, making it interpret as TiB (which at 200 TiB exceeds the 16 TB max)
2. **The field requires a minimum** — DO Volumes minimum is **1 GiB**, but some GPU Droplet volume configs have a higher minimum (sometimes 10 GiB)
3. **Trailing space or non-numeric character** got pasted in

**Quick fixes to try:**

- Type `100` instead of `200` — rule out a max cap
- Check if there's a unit selector next to the field — make sure it's set to **GiB** not **TiB**
- Try `50` to confirm the field works at all
- Clear the field completely and retype (don't paste)

Since it's DO under the hood, the valid range is **1–16384 GiB** — so `200` as GiB should be fine in theory. Most likely it's a unit mismatch in the UI dropdown.
