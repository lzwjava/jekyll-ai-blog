---
audio: false
generated: true
image: false
lang: en
layout: post
title: Top Enterprise Web Security Products
translated: false
type: note
---

Question: Besides Symantec, what other similar or alternative web access control / firewall / proxy products do big corporations use?

Answer:

You're describing the **Secure Web Gateway (SWG)** / **enterprise proxy** category — the thing that intercepts your browser traffic, enforces URL filtering, blocks categories, does TLS inspection, and logs everything. Symantec (the old Blue Coat ProxySG / WSS line, now under Broadcom) is one of the classic players. Here's the landscape big corps actually deploy:

**Cloud-native SASE / SSE platforms (where everything is moving):**

- **Zscaler** (ZIA — Internet Access) — by far the most common Symantec replacement at banks/large enterprises. Pure cloud proxy, no appliance.
- **Netskope** — strong on inline CASB + SWG, popular in finance.
- **Palo Alto Prisma Access** — Palo Alto's SASE; ties into their firewall ecosystem.
- **Cisco Umbrella** (formerly OpenDNS) + Cisco Secure Web Appliance (the old IronPort WSA).
- **Cloudflare Gateway** (part of Cloudflare One / Zero Trust) — increasingly adopted.
- **Microsoft Entra Internet Access** (part of Global Secure Access) — Microsoft's SSE, attractive to M365-heavy shops.

**Next-gen firewalls (NGFW) — the network-layer enforcement:**

- **Palo Alto Networks** (PAN-OS) — dominant in large enterprise/banking.
- **Fortinet FortiGate** — huge install base, often the cheapest-per-throughput.
- **Cisco Firepower / Secure Firewall**.
- **Check Point** — very common in financial institutions, especially EMEA.
- **Juniper SRX**.

**Older proxy/filtering products still found in big corps:**

- **Forcepoint** (formerly Websense + Raytheon) — heavy in government/regulated.
- **McAfee/Skyhigh Web Gateway** (the old Webwasher/MWG lineage).
- **Squid** — open-source, still used internally for caching/filtering layers.

**What you're most likely hitting at a global bank:** Zscaler or Bluecoat/Symantec for the web proxy, plus Palo Alto or Check Point at the perimeter. The TLS-inspection cert your corp laptop trusts is the giveaway — that's the SWG MITM-ing your HTTPS to inspect it.

If you tell me what symptom you're seeing (blocked domain, cert errors on `pip`/`npm`, proxy `407`, etc.), I can give you the exact bypass-within-policy workaround — e.g., configuring `~/.pip/pip.conf` with the corp CA bundle, or `git config http.sslCAInfo <​CA_BUNDLE>`.
