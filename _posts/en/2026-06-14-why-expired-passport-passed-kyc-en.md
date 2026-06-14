---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why Expired Passport Passed KYC
translated: false
type: note
---

Interesting observation. A few likely reasons why an outdated passport passed:

**Why it probably worked:**

1. **Expiry ≠ Invalid identity** — The passport number and personal data (name, DOB, nationality) are still valid identifiers even after expiry. The document proves *who you are*, not that you're currently authorized to travel. Many KYC systems only validate format and data consistency, not expiry date.

2. **OCR/data extraction only** — SoSIM likely runs the passport through an OCR pipeline that extracts fields and checks them against a database or format rules. Expiry date may simply not be a rejection criterion in their validation logic.

3. **Regulatory minimum** — Hong Kong telecom real-name registration (under OFCA requirements) mandates identity verification, but the regulation specifies *type* of document, not necessarily that it must be currently valid. An expired HKID or passport still has a real name attached to a real person.

4. **Risk tolerance** — Prepaid SIM KYC is lower-risk than banking KYC. Banks would reject expired docs. Telcos often don't — the liability is lower and friction reduction matters for conversion.

**The practical takeaway:**

Their verification is likely:

- Document format valid ✓
- Name + DOB extractable ✓
- Document number matches expected pattern ✓
- (Expiry check) → either skipped or soft-warning only

This is common in lower-tier KYC implementations. Not a flaw you exploited — just a design decision they made to reduce registration drop-off.
