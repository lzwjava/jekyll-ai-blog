---
audio: false
generated: true
image: false
lang: en
layout: post
title: 5G SA Deployment by Country
translated: false
type: note
---

**Question:** Which companies and countries have deployed 5G Standalone (SA) networks so far?**Answer:**

Here's the global picture as of mid-2026:

---

## Global 5G SA Deployment Status

As of April 2025, 163 operators across 65 countries are investing in public 5G SA networks, with 73 operators in 39 countries having launched or soft-launched services. But coverage and quality vary wildly.

---

## Leaders by Region

### 🇨🇳 China — SA Launched, But You May Not Be On It

This is the critical one for you. As of November 2021, China Mobile, China Unicom, and China Telecom had all achieved large-scale deployment of 5G SA networks, with the SA core operational. China Mobile is operating the world's largest centralized, all-cloud, fully integrated 5G SA core network.

**So why are you still on NSA?** Your CGNAT evidence is damning — your hotspot (iPhone personal hotspot) is likely not being provisioned for SA, or your specific cell tower hasn't been migrated. SA core exists in China, but device+SIM+tower all need to align.

### 🇺🇸 USA

T-Mobile US was one of the few high-profile large-scale SA deployments outside China before 2025. AT&T and Verizon have been slower.

### 🇩🇪 Europe — Germany Leading

Germany's three national MNOs now have live 5G SA — Telekom Deutschland announced nationwide 5G SA coverage in July 2025, alongside Vodafone's nationwide activation and O2 Telefónica's "5G Plus" service.

### 🇪🇸 Spain

Telefónica (Movistar) covers over 94% of the population across 5,700 municipalities with its "5G+" SA network using 700 MHz and 3.5 GHz spectrum.

### 🇦🇪 UAE / GCC — Performance Leader

The GCC has established itself as the global 5G SA performance leader. The UAE reached a median SA download speed of 1.24 Gbps — exceptional even compared to full-fiber broadband.

### 🇰🇷 South Korea

KT is currently the only operator with a fully operational nationwide standalone core. The South Korean government mandated all 5G base stations be connected to standalone core equipment by 2026.

### 🇮🇳 India

Reliance Jio was one of the few large-scale SA deployments outside China.

---

## Global Reality Check

Globally, 5G SA availability based on Speedtest sample share reached only 17.6% in Q4 2025 — roughly 1 in 6 5G speed tests worldwide occurs on a standalone network. So even where SA is "deployed," most users aren't actually on it.

---

## What This Means for You Specifically

China has SA infrastructure, but your hotspot likely isn't hitting it because:

1. **iPhone personal hotspot** — the modem may fall back to NSA for hotspot mode even if your direct connection is SA
2. **Tower-level migration** — not every cell tower in Guangzhou is SA-migrated yet
3. **SIM provisioning** — China Telecom SA may require specific plan/APN config

To actually verify: field test mode on iPhone (`*3001#12345#*` → call) shows the NR connection type. Look for `NR SA` vs `NR NSA` in the cell info. China Mobile, China Telecom, and China Unicom were early adopters of 5G SA and have since launched 5G-Advanced — so SA *exists* on your carrier, you just need to confirm if your specific tower and SIM are on it.

References:

- [5G Standalone State of Play — Opensignal Feb 2026](https://insights.opensignal.com/2026/02/5g-standalone-state-of-play-architecture-deployed-monetisation-pending/dt)
- [Global Reality Check on 5G SA 2026 — Ookla/Omdia](https://www.communicationstoday.co.in/a-global-reality-check-on-5g-sa-and-5g-advanced-in-2026-ookla/)
- [GSA 5G Standalone April 2025](https://gsacom.com/paper/5g-standalone-april-2025/)
