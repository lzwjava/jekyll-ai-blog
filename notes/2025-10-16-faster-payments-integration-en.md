---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Faster Payment System Integration Guidelines
translated: false
type: note
---

The Faster Payment System (FPS) in Hong Kong, operated by Hong Kong Interbank Clearing Limited (HKICL) under the oversight of the Hong Kong Monetary Authority (HKMA), does not provide a publicly available SDK for banks to integrate. Integration is handled through direct connectivity to the FPS infrastructure, with technical specifications shared privately with participating banks (known as Settlement Participants) during the onboarding process. These specs guide banks in enhancing their systems for access, but there are no off-the-shelf SDKs or developer kits mentioned in official documentation.

Regarding APIs, FPS itself does not currently offer dedicated APIs for external or third-party integration. However, it aligns with the HKMA's broader Open API Framework for the Hong Kong Banking Sector (introduced in 2018 and updated through phases up to 2025), which encourages banks to expose certain functions via APIs for third-party service providers (e.g., for account information or payment initiation). FPS transactions can leverage this framework indirectly for features like payment initiation, but no FPS-specific APIs are available yet—access remains restricted on a need-to-know basis for security and regulatory reasons. HKMA continues to monitor and may expand API support in the future.

### Key Integration Details for Banks
- **Connectivity Methods**: Banks connect in real-time mode via IBM MQ messaging for instant processing or batch mode via file transfers (e.g., over HKICL's secure ICLNET network). The system runs 24/7.
- **Messaging Standards**: All communications use the ISO 20022 format, supporting rich data, Chinese characters, and interoperability.
- **Onboarding Process**: Banks enroll with HKMA (for HKD) or Bank of China (Hong Kong) for RMB, sign FPS Rules agreements, adapt systems to the provided specs, undergo HKICL testing, and go live. All licensed banks must participate as direct settlers.
- **Other Features**: Supports proxy IDs (e.g., phone/email), QR codes (EMV standard), and multi-currency (HKD/RMB) transfers. Authentication follows HKMA's two-factor guidelines, with banks setting their own transaction limits.

For detailed technical specs, banks must contact HKICL directly upon enrollment, as they are not publicly downloadable.

[Faster Payment System (FPS) - HKMA](https://www.hkma.gov.hk/eng/key-functions/international-financial-centre/financial-market-infrastructure/faster-payment-system-fps/)
[Scheme Documentation - HKICL FPS](https://fps.hkicl.com.hk/eng/fps/about_fps/scheme_documentation.php)
[World Bank FPS Case Study: Hong Kong](https://fastpayments.worldbank.org/sites/default/files/2021-09/World_Bank_FPS_Hong_Kong_SAR_China_FPS_Case_Study.pdf)
[Open API Framework for the Banking Sector - HKMA](https://www.hkma.gov.hk/eng/key-functions/international-financial-centre/fintech/open-application-programming-interface-api-for-the-banking-sector/)
