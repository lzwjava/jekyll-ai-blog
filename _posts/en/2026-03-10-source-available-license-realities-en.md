---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enforcing Source Available Licenses Realities
translated: false
type: note
---

**Question:** How do open-core companies enforce source-available licenses for enterprise customers? What happens if a customer secretly copies and modifies the code?

---

**Answer:**

This is a great question that gets into the realities of software law and practical trust. The honest answer is: **enforcement is imperfect, but the legal teeth are real — and there are also technical and commercial mechanisms beyond just law.**

---

## Layer 1: Legal Enforcement (Copyright Law)

The most important thing to understand: **source-available licenses are not honored on trust alone — they are legally binding under copyright law.**

The first major vindication came in *Jacobsen v. Katzer* (2008), where the Federal Circuit held that a licensee's violation of an open-source license amounted to **copyright infringement**, not merely a breach of contract. The court concluded that conditions like disclosure requirements are entitled to full legal recognition even without a dollar fee attached.

This distinction matters enormously:

- **Breach of contract** → you sue for damages, limited remedies
- **Copyright infringement** → injunctions, statutory damages, forced removal of product from market

Courts have consistently upheld open-source and source-available license terms. The €900,000 fine against French telecom giant Orange (in 2024) sets a precedent that non-compliance can be extremely costly.

So if a customer secretly copies and ships enterprise code without a license, the vendor can sue for **copyright infringement** — which is serious.

---

## Layer 2: How Violations Are Actually *Detected*

This is the practical reality — vendors can't watch every server. Detection happens through several channels:

**a) Competitive intelligence / public releases**
If the customer ships a product or SaaS built on the stolen code, it becomes detectable. Competitors, ex-employees, or researchers may notice similarities.

**b) Software Composition Analysis (SCA) tools**
SCA tools examine software applications to identify third-party and open-source components along with their associated security vulnerabilities or legal license restrictions. Open-source auditors have made many "big saves" for clients, catching unusual compliance issues that could otherwise have been big problems. These tools can fingerprint code and detect copied snippets across products.

**c) Whistleblowers / ex-employees**
Inside a company, engineers who handled the code may leave and disclose violations — especially if they themselves feel uncomfortable with the practice.

**d) License keys / telemetry in the binary**
Many enterprise products phone home, embed license tokens, or have **cryptographic license checks** baked into the binary. If you strip those out, you've already modified the code — triggering the license violation.

---

## Layer 3: Technical Enforcement (Beyond Law)

Companies don't rely only on legal recourse. They build technical barriers:

| Mechanism | How it works |
| --- | --- |
| **License key servers** | Software calls home to validate a license key; offline tampering breaks functionality |
| **Obfuscated / compiled binaries** | Enterprise features shipped as compiled artifacts — hard to modify cleanly |
| **Encrypted modules** | Code is decrypted at runtime using a key tied to the license |
| **Feature flags in SaaS** | For cloud-hosted enterprise, features are toggled server-side — customer never has the code at all |
| **Signed builds** | Tampered binaries break signature verification |

For **pure on-prem deployments with full source access**, these technical controls are weaker — which is why legal frameworks matter more.

---

## Layer 4: The Practical "Gray Zone" — Small Violations Often Go Undetected

Being honest: **small-scale internal use of copied/modified enterprise code that never leaves the company is very hard to detect or enforce.** Companies generally:

- Accept some level of undetectable leakage as a cost of doing business
- Focus enforcement energy on **commercial competitors** redistributing their code
- Use the threat of legal action as a deterrent

There is a growing trend in enforcement — a movement from enforcement by OSS advocacy groups toward enforcement by commercial entities against other companies. For licenses like AGPL, obligations may even be triggered when software is accessed by a third party over a network — even if not distributed.

---

## Layer 5: The Real Deterrent — Commercial Risk

For enterprise buyers (large companies, regulated industries), the **reputational and operational risk** of getting caught is enormous:

- Vendor terminates the license → **system goes dark overnight**
- Vendor sues → **product pulled from market**, executive liability
- News leaks → **trust destroyed with customers and regulators**

If your business is using open-source or source-available code in a way that violates the license, remedy it quickly before it turns into a true legal battle. Non-compliance can lead to active lawsuits, monetary damages, forced injunctions — and your software may be rendered unusable by the court, with rights forfeited.

This commercial risk is far more effective than technical controls for large enterprise customers, because the downside is catastrophic.

---

## Summary

| Enforcement Layer | Strength | Notes |
| --- | --- | --- |
| Copyright law | Strong | Infringement, not just breach of contract |
| SCA / code fingerprinting | Medium | Detects if code is shipped publicly |
| License key / telemetry | Medium | Technical barrier, bypassable but risky |
| Whistleblowers | Unpredictable | Often how large violations surface |
| Commercial deterrence | Very strong for large cos | Existential risk if caught |
| Small internal use detection | Weak | Practically hard to discover |

The short version: **copying enterprise source code secretly is legally very risky, technically harder than it looks, and commercially suicidal for a serious business** — but small-scale internal abuse in a dark corner of a company? It likely goes undetected. The system relies on a mix of legal fear, technical friction, and commercial self-interest rather than perfect enforcement.

---

**References:**

- [Consequences of Violating Open Source Licenses - Berkeley Technology Law Journal](https://btlj.org/2015/11/consequences-violating-open-source-licenses/)
- [Open Source License Compliance Lessons from Court Cases (FOSSID)](https://fossid.com/articles/open-source-license-compliance-lessons-from-two-landmark-court-cases/)
- [Analyzing 5 Major OSS License Compliance Lawsuits (FOSSA)](https://fossa.com/blog/analyzing-5-major-oss-license-compliance-lawsuits/)
- [How to Enforce Open Source Licenses (TermsFeed)](https://www.termsfeed.com/blog/enforce-open-source-licenses/)
- [Open Source Software Policies: Business & Legal Risks (National Law Review)](https://natlawreview.com/article/open-source-software-policies-why-you-need-them-and-what-they-should-include)
