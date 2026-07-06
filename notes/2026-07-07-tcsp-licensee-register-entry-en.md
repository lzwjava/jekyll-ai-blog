---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCSP Licensee Register Entry
translated: false
type: note
---

**Question:** What is this table I'm looking at — a row listing "TC010660, Hong Kong Blue Bridge International Business Limited" with a business address in Kwai Chung?

**Answer:**

What you've pasted is a row from Hong Kong's **public Register of TCSP Licensees** — the searchable database maintained by the Companies Registry at tcsp.cr.gov.hk. TCSP stands for **Trust or Company Service Provider**.

Here's the background. Before March 2018, anyone in Hong Kong could set up shop and register companies for clients without much scrutiny. That changed when the Anti-Money Laundering and Counter-Terrorist Financing Ordinance (AMLO, Cap. 615) came into effect — from then on, corporate-service work required licensing, fit-and-proper testing, and compliance audits, supervised by the Companies Registry through a dedicated TCSP licensing office. Operating a trust or company service business without a licence is an offence, punishable by a fine of up to HK$100,000 and up to 6 months' imprisonment.

A TCSP licensee is a firm legally permitted to do things like: forming companies, acting as (or arranging) directors or company secretaries, providing a registered office or business/correspondence address, and acting as trustee of an express trust or nominee shareholder. Each licence is valid for 3 years and records the licensee's name and business address — which is exactly what your row shows:

- **Licence No.** — `TC010660`, the unique licence identifier
- **Name (EN/中文)** — the licensed entity, here a company in Kwai Chung
- **Business Address** — the registered place of business
- **Remarks** — usually flags conditions, suspensions, or status notes

The register itself is open data: the full list of TCSP licensees is published on DATA.GOV.HK by the Companies Registry, updated monthly, downloadable as XLSX, CSV, or via API. So if you want to scrape or analyze it programmatically (e.g., to find corporate-secretary firms for your HK entity), you don't need to scrape the search UI — pull the CSV directly.

**Why this matters for you specifically:** when you register your Hong Kong entity (playbook item #8), the firm you hire for incorporation, company secretary, and registered address services *must* appear in this register. Checking the licence number here is your due-diligence step — an unlicensed provider is a red flag. Also note "Blue Bridge International Business" is a typical incorporation-agency name; thousands of these exist (~7,000 licensees as of mid-2024), so compare pricing and reputation, not just licence status.

**References:**

- [Register of TCSP Licensees — public search](https://www.tcsp.cr.gov.hk/tcspls/search/public-search)
- [List of TCSP Licensees — DATA.GOV.HK open dataset](https://data.gov.hk/en-data/dataset/hk-cr-crtcspdata-list-tcsp-licensees)
- [Complete Guide to Obtaining a TCSP Licence in Hong Kong](https://kyc.management/en-hk/resources/a-complete-guide-to-obtaining-a-tcsp-licence-in-hong-kong)
