---
audio: false
generated: true
image: false
lang: en
layout: post
title: Corporate Quantitative Trading API Application Process
translated: false
type: note
---

**Question:** How can a company use its business license to apply for a quantitative trading API for China A-share stocks?

**Answer:**

In China's A-share market, applying for a quantitative trading API as a **corporate/institutional entity** (using a business license) is a distinct process from individual investor accounts, with stricter requirements and higher capital thresholds. Here's the full breakdown:

---

### Step 1 — Open an Institutional Securities Account

Before applying for any API, the company must first open a **corporate securities account (机构户)** at a licensed broker (券商). As a corporate/institutional investor, you will need to submit: the company's business license (营业执照, original and copy), organization code certificate (组织机构代码证), tax registration certificate (税务登记证), the legal representative's certificate and authorization letter, the legal representative's ID card, the authorized agent's ID card, and the company seal and legal representative seal. This **must be done in-person at a broker branch** (临柜) — it cannot be done online for institutional accounts.

---

### Step 2 — Meet the Capital & Eligibility Requirements

The key differences between personal and institutional accounts for quantitative trading are significant: institutional accounts require the business license, legal representative proof, and organization code certificate. The capital threshold is also considerably higher — some brokers require institutional accounts to have assets of ¥3 million (300万) or more. Institutional investors may also need in-person branch verification, and the overall process is more complex.

---

### Step 3 — Apply for the Quantitative Trading API Permission

Once the account is active, apply for API access through the broker. The main steps are: (1) confirm your qualifications — generally requiring 20 consecutive trading days with average assets above ¥500,000 and 2+ years of trading experience; (2) contact your dedicated account manager (客户经理), state your needs, and submit asset proof and trading records; (3) visit the broker's offline branch to sign the quantitative trading interface usage agreement, after which a technical team will assist with system integration and testing.

---

### Main Brokers Supporting Quant API (2026)

The leading brokers supporting quantitative trading API access include Huatai Securities, Guotai Junan, CITIC Securities, and Galaxy Securities. They commonly support QMT (local deployment, Python/C++) and PTrade (cloud/server-side) platforms. The standard API requires ¥500,000 in assets; high-frequency advanced interfaces require ¥3 million or more.

| Platform | Type | Best For |
|---|---|---|
| **QMT (迅投)** | Local | Complex strategies, Python/C++ |
| **PTrade (恒生)** | Cloud/Server | Grid trading, automation |
| **Broker proprietary API** | Varies | High-frequency, institutional |

---

### Key Points for Corporate Applicants

- **Must go in person** to a broker branch — institutional account opening is not available online.
- The **legal representative** (法人代表) or an **authorized agent** must be present with valid ID.
- Capital minimums are **significantly higher** for institutions than individuals.
- After your account is set up, you must sign a risk disclosure agreement and an interface usage agreement before receiving API access credentials. Always test in a simulation environment (仿真) before going live.
- Compliant brokers include: **Huatai, Galaxy Securities, CITIC, Guotai Junan, Guojin Securities, and CITIC Construction Investment**.

---

**References:**
- [机构开户与量化API差异说明 – 叩富问财](https://licai.cofool.com/ask/qa_4520764.html)
- [2026年券商量化交易接口申请流程 – 叩富问财](https://licai.cofool.com/ask/qa_7321676.html)
- [四大券商量化API接口开通实测 – 叩富问财](https://licai.cofool.com/ask/qa_6005184.html)
- [企业法人证券开户所需材料 – 叩富问财](https://licai.cofool.com/ask/qa_7776.html)
- [上海黄金交易所机构开户指南 (SGEI Guidelines)](https://en.sge.com.cn/upload/file/202205/06/GuidelinesforBrokerageBusinessofInternationalMembersofSGE-Revisedin2020.pdf)
