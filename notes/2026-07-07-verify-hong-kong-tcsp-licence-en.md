---
audio: false
generated: true
image: false
lang: en
layout: post
title: Verify Hong Kong TCSP Licence
translated: false
type: note
---

**Question:** How do I verify a Hong Kong incorporation agent's TCSP licence? Is there an official government site for that?

**Answer:**

Yes — Hong Kong runs an official public register. The search site is <https://www.tcsp.cr.gov.hk/tcspls/search/public-search>, operated by the Registry for Trust and Company Service Providers under the Companies Registry.

How to verify an agent:

1. Ask the agent for their **TCSP licence number** (format like `TC000123`). Any legit agent will print it on their website footer, invoices, or engagement letter — licensed firms typically display it openly, e.g. "TCSP license holder (TC 0007484)". If they hesitate to give it, walk away.
2. Search the register by licence number or company name. Confirm three things: the **exact legal entity name matches** who you're paying (not a lookalike mainland entity), the licence **status is valid/current**, and the business address matches what they told you.
3. Cross-check the entity itself on the Companies Registry's e-Search (<https://www.e-services.cr.gov.hk>) to see incorporation status and filing history.

Why this matters: since AMLO (Cap. 615) took effect, anyone doing company formation for clients must be licensed, and approved firms automatically appear in the public TCSP register. Many cheap ¥4,380-tier "HK company registration" sellers on Taobao/WeChat are mainland intermediaries reselling a licensed HK firm's service — in that case, get the name of the **actual HK TCSP** that will act as your company secretary / registered address, and verify *that* entity.

Bonus, CLI-friendly: the government publishes the full list of TCSP licensees on DATA.GOV.HK as CSV/XLSX/API, updated monthly. So you can just:

```bash
# grab the monthly CSV from data.gov.hk (dataset: hk-cr-crtcspdata-list-tcsp-licensees)
# then:
grep -i "agent name" tcsp_licensees.csv
```

One caveat: a TCSP licence is an AML/fit-and-proper check, not a quality guarantee. It confirms they're legal, not that their year-2 renewal pricing won't triple. So do both: verify the licence *and* get renewal + audit pricing in writing before paying.

**References:**

- [TCSP Public Search — Companies Registry](https://www.tcsp.cr.gov.hk/tcspls/search/public-search)
- [List of TCSP Licensees — DATA.GOV.HK](https://data.gov.hk/en-data/dataset/hk-cr-crtcspdata-list-tcsp-licensees)
- [Registry for Trust and Company Service Providers](https://www.tcsp.cr.gov.hk/tcspls/index)
