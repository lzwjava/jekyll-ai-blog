---
audio: false
generated: true
image: false
lang: en
layout: post
title: Authentic .edu, Unaccredited For-Profit College
translated: false
type: note
---

## Findings: `https://www.cstu.edu/`

**Verdict: This is the authentic website of California Science and Technology University — a real, state-licensed private college — but it is a small for-profit career college, not an accredited research university. The ●strongest evidence of authenticity is the `.edu` domain itself.**

### 1. WHOIS (authoritative registry: EDUCAUSE — `.edu` is strictly regulated)

- **Domain:** `CSTU.EDU`
- **Registrant:** California Science and Technology University, 1601 McCarthy Blvd, Milpitas, CA 95035, USA
- **Admin/Tech:** Glen Qin, `glen.qin@cstu.org` (+1-408-666-3690)
- **Registered:** 23-Jun-2022 · **Expires:** 23-Jun-2028 · Last updated: 25-Apr-2025

### 2. How strong the `.edu` evidence really is

`.edu` is not open to everyone. EDUCAUSE only issues it to **US degree-granting institutions accredited by a Department of Education–recognized accreditor** (or certain foreign institutions). So:

- A `.edu` that was vetted and registered in 2022 is a big authenticity signal.
- Registrant name/address match exactly what the site claims — no impersonation signs (not a lookalike of Caltech, MIT, etc.).

### 3. DNS / infrastructure

| Item | Value | Reading |
|---|---|---|
| A record (www + apex) | `18.118.195.140` | AWS us-east-2 (Ohio) |
| Name servers | `awsdns-*` | Routed via AWS Route 53 |
| MX | `aspmx.l.google.com` | Real Google Workspace mail |
| TLS | Let's Encrypt, valid Oct 2026 – Jan 2027 | Valid cert for `www.cstu.edu` |
| Wayback | snapshots of both `cstu.edu` (2026) and older `cstu.org` (2023) | Continuity with their older `.org` identity |

### 4. Red flags / caveats to be aware of

- **"Licensed to operate by BPPE" ≠ accreditation.** BPPE (Bureau for Private Postsecondary Education) is just California's *business license* for private schools. The site's claim (BPPE license, acceptance of transfer credits subject to policy, California-specific disclosures) is the profile of a **for-profit career college**, not a regionally/university-accredited institution.
- **Dated infrastructure and content:** site runs on **nginx/1.10.3 (Ubuntu)** (a ~2016 build), and the homepage curriculum listings stop at **2018–2019** despite the domain being registered in 2022 and claimed founding in 2011.
- The **Accreditation page 404s** (`/accreditation.html`), even though it's linked in the nav — they don't prominently publish a USDE-recognized accreditation, consistent with the for-profit, non-accredited profile.

### Bottom line

- **Authenticity:** Yes — genuinely the site of California Science and Technology University (Milpitas, CA). The EDUCAUSE `.edu` registration is the strongest independent proof; everything (registrant, contact, site content) is internally consistent.
- **Status:** A small private, BPPE-licensed college — again, licensing ≠ accreditation. Treat diplomas/transfer credits accordingly, and verify their live BPPE registration at `bppe.ca.gov` before enrolling or trusting credentials.

If you want, I can follow up with the BPPE school-lookup result via their web form, or probe deeper (e.g., subdomain enumeration, email server checks) for a phishing-style reassessment.
