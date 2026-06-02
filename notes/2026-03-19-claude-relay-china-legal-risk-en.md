---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Relay Services China Legal Risk
translated: false
type: note
---

**Question:** If someone runs these Claude relay services in China, will it violate Chinese law?

**Answer:**

Running a Claude API relay service (such as claude-relay-service or commercial "中转站" proxies) in China exists in a **legal gray area**. It is **not explicitly criminalized** like fraud or drug trafficking, and thousands of such services operate openly on Taobao, WeChat, Xianyu, and public websites with domestic Alipay/WeChat Pay. However, it can potentially violate several Chinese regulations depending on scale, how it is run, and whether proper compliance steps are taken. Here is a clear breakdown:

### 1. Main potential violation: Generative AI Service Regulations
China’s **Interim Measures for the Management of Generative Artificial Intelligence Services** (2023, enforced by CAC) require any provider offering generative AI (including foreign models via relay) to the Chinese public to:
- File/register with the Cyberspace Administration of China (CAC).
- Implement content safety filters to prevent illegal, harmful, or politically sensitive output.
- Label AI-generated content and keep records.
- Comply with "core socialist values".

Most small personal or group-run relays (like the GitHub claude-relay-service hosted on overseas VPS) skip this filing entirely. Large commercial platforms sometimes claim compliance or use loopholes (e.g., "only for research"). Failure to register can lead to fines, service shutdown orders, or account blocks, but enforcement is inconsistent for small operators.

### 2. Data security and cross-border transfer (PIPL & Data Security Law)
- User prompts and outputs are sent to Anthropic’s US servers.
- This counts as exporting personal information abroad.
- You must conduct a security assessment or sign a Standard Contract for cross-border data transfer if handling significant data.
- Most relays do not do this → technical violation of Personal Information Protection Law (PIPL) and Cybersecurity Law.

### 3. Internet service licensing
- If the relay dashboard or API endpoint is hosted on a mainland Chinese server, you need an ICP license (互联网信息服务增值电信业务经营许可证).
- Most operators host on overseas VPS (US, Singapore, Hong Kong) to avoid this, which is common and rarely punished for individuals.

### 4. VPN / circumvention aspect
- Using or providing VPN/proxy access itself is **not illegal** for end users.
- However, providing unlicensed VPN services for commercial profit can violate telecom regulations (but your Claude relay is not a general VPN; it is a specific API proxy).

### 5. Real-world practice (2026 situation)
- Hundreds of Claude relay services advertise openly ("无需翻墙、直连Claude、支付宝支付").
- No public reports of arrests or prosecutions specifically for running Claude relays.
- Risks that do happen: Anthropic bans the master accounts (especially after their 2025 policy blocking Chinese-controlled entities), payment platforms freeze accounts if flagged, or CAC issues takedown notices if the service spreads sensitive content.
- Government sectors and banks are now restricted from foreign AI proxies, but private individuals and small businesses face low enforcement.

**Bottom line**
For a single person or small group self-hosting claude-relay-service on an overseas server and sharing with friends or a few paying users → **very low legal risk** from Chinese authorities (mainly Anthropic ToS and account ban risk).
For a public commercial service selling to thousands of users without CAC filing or data export compliance → **technically violates regulations** and could face fines or shutdown if reported or scaled too big.

Most Chinese operators treat it as a gray-area business and accept the risk, similar to how ChatGPT/GPT proxies have run for years. Always consult a Chinese lawyer for your specific setup if you plan to run it commercially.

**References:**
- [Interim Measures for the Management of Generative Artificial Intelligence Services (official CAC rules)](https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm)
- [Anthropic 2025 China ban policy & relay context](https://www.anthropic.com/news/updating-restrictions-of-sales-to-unsupported-regions)
- [V2EX discussion on compliance for Claude in China](https://v2ex.com/t/1183984)
- [Example commercial relay (mentions domestic payment & no VPN)](https://www.yiboot.com/article/userguide/claude-4-5-02.html)
- [Zhihu guide explicitly stating VPN use is not illegal under Chinese law](https://aifreeapi.com/zh/posts/claude-unsupported-region-solution)
