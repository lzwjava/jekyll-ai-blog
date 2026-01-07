---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Avoid Proof of Concepts in Production
translated: false
type: note
---

Question: Due to restrictions in the banking environment, many software/libraries cannot be installed in the production environment. For technical reasons, is it better to conduct some technical Proof of Concept (POC) tests directly in the production environment as well? For example, Python/Java API tests are easy because they require minimal libraries, while Selenium needs specific drivers and is more complicated. Is this correct?

Answer: 

Yes, your observation is largely correct, but with important caveats—especially the part about running POCs in production.

### Key Points in Banking/Regulated Environments

- **Strict restrictions on production**: In banking and other highly regulated industries (finance, healthcare, etc.), production environments are tightly controlled. Installing new software, libraries, drivers, or even running experimental code is usually prohibited or requires extensive change management, approvals, and auditing. This is to ensure stability, security, and compliance (e.g., PCI-DSS, SOX, GDPR, or local banking regulations).

- **POC should almost never be done in production**: Performing technical Proof of Concept directly in production is generally considered a bad practice and often a policy violation. Risks include:
  - System instability or outages
  - Security vulnerabilities
  - Compliance breaches (audit trails, segregation of duties)
  - Data leakage or corruption (even if using masked data)

  Instead, best practice is to build representative non-production environments (e.g., staging, pre-prod, or dedicated sandbox/integration environments) that mirror production as closely as possible in terms of OS version, network rules, installed base software, and restrictions.

### Technology-Specific Considerations

- **Python/Java API tests**: Yes, these are usually easier and lower risk.
  - They typically depend only on standard language runtimes and common libraries that are often already approved/whitelisted.
  - HTTP/client libraries (requests, urllib, Apache HttpClient, etc.) are lightweight and commonly pre-installed or easily approved.
  - Tests can often run with minimal dependencies.

- **Selenium/WebDriver tests**: Much more challenging in restricted environments.
  - Requires browser-specific drivers (ChromeDriver, GeckoDriver, etc.)
  - Often needs the actual browser installed (or headless equivalents)
  - May require graphical environment access (X11, display server) or specific OS permissions
  - Additional dependencies like fonts, libraries for rendering, or even GPU access in some cases
  - In locked-down banking servers (often headless Linux without GUI), running Selenium usually requires significant workarounds or approvals.

### Recommended Approach

1. Perform initial POC in development or local environments (unrestricted).
2. Move to a staging/pre-production environment that replicates production constraints (same OS, same base image, same security policies).
3. Validate there that your solution (e.g., Selenium setup) works under real restrictions.
4. Only after successful validation in pre-prod, and with proper change approval, deploy to production.

In summary: You're right that some technologies (like Selenium) are far more painful in restricted banking environments than simple API tests. But running POCs directly in production is almost always the wrong approach—use mirrored non-prod environments instead to simulate the constraints safely.