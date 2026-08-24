---
audio: false
generated: true
image: false
lang: en
layout: post
title: Starting a Hong Kong Company via Shenzhen
translated: false
type: note
---

Question: **How do I start a Hong Kong company, and are there Shenzhen agencies that can do it for me? Do those agencies have some authorization from the Hong Kong government?**

Answer: **Yes. Shenzhen has many agencies that help mainland residents incorporate Hong Kong companies. But the important distinction is: they usually do NOT have some special “Shenzhen government/Hong Kong government right” to create companies.**

They are generally **private professional service firms**, often working with a Hong Kong **TCSP (Trust or Company Service Provider)**.

### 1. You can personally own a Hong Kong company

Hong Kong explicitly allows **non-Hong Kong residents to incorporate a local limited company**. You can be the shareholder and director. ([Companies Registry][1])

For a typical private company limited by shares, you need roughly:

```text
You
 │
 │ 100% shareholder
 ▼
Hong Kong Ltd
 │
 ├── Director: you
 ├── Company secretary: Hong Kong resident / Hong Kong company
 ├── Registered office: Hong Kong address
 └── Business: software / AI consultancy
```

There is **no statutory minimum paid-up capital**. ([Companies Registry][1])

The Companies Registry requires, among other things:

```text
NNC1
Articles of Association
IRBR1
```

and incorporation can be done electronically. For a straightforward private company, the Registry says electronic incorporation can normally be completed **within about 1 hour**. ([Companies Registry][2])

[Hong Kong Companies Registry — Register a new company](https://www.cr.gov.hk/en/services/register-company.htm?utm_source=chatgpt.com)

---

### 2. So what is the Shenzhen agency actually doing?

This is the important part.

A Shenzhen agency might advertise something like:

> 香港公司注册
> 香港公司秘书
> 香港注册地址
> 银行开户
> 做账审计
> 商务秘书服务

They may have a Shenzhen office, but the **actual Hong Kong corporate-services provider** behind the service may be a Hong Kong entity.

For example:

```text
You
 │
 │ contract/pay Shenzhen agency
 ▼
Shenzhen agency
 │
 │ cooperation
 ▼
Hong Kong professional firm / TCSP
 │
 ├── Company incorporation
 ├── Hong Kong company secretary
 ├── Registered office
 ├── Annual return
 └── Accounting / tax services
```

Hong Kong regulates companies providing these services.

A business that, **for money**, forms companies, provides company secretarial services, or provides registered/business addresses generally falls under the **TCSP licensing regime**. A TCSP needs a licence from the Hong Kong Companies Registry. ([TCSP][3])

There is even a public **TCSP licensee registry** where you can check the provider. ([TCSP][4])

[Hong Kong TCSP Licensee Registry](https://www.tcsp.cr.gov.hk/tcspls/search/public-search?utm_source=chatgpt.com)

So if a Shenzhen agency says:

> "We are authorized by the Hong Kong government to register Hong Kong companies."

I'd ask them:

```text
What's the name of your Hong Kong TCSP licensee?
What's the TCSP licence number?
What's the Hong Kong company providing the company-secretary service?
```

Then verify it in the official registry.

**That's much more meaningful than whether the Shenzhen agency itself claims to be "government authorized."**

---

### 3. For your situation, I would use an agency

You don't really need to fly to Hong Kong just to incorporate.

A reasonable setup would be:

```text
Shenzhen agency
       │
       ▼
Hong Kong TCSP
       │
       ▼
Your Hong Kong Ltd
       │
       ├── 100% owned by you
       ├── You = director
       ├── HK company secretary
       ├── HK registered address
       └── HK bank / payment account later
```

You can then operate your **software / AI consultancy** business from Shenzhen/Guangzhou and use the HK company as the contracting entity for international/HK clients.

That is quite different from creating a mainland company.

---

### 4. Don't confuse three things

There are actually three separate layers:

| Thing                                  | Who handles it                                         |
| -------------------------------------- | ------------------------------------------------------ |
| Company incorporation                  | Hong Kong Companies Registry                           |
| Business registration                  | Hong Kong Inland Revenue Department / one-stop process |
| Company secretary / registered address | Private professional service provider                  |

Hong Kong has a **one-stop company + business registration** process, so the incorporation application also handles the business-registration application. ([Government of Hong Kong][5])

The private agency is basically your **outsourced corporate administration layer**, not the government itself.

---

### 5. The minimum structure I'd consider for you

For an AI/software consultancy:

```text
[You]
  │
  │ 100%
  ▼
[XXX AI Limited]
Hong Kong
  │
  ├── Software consultancy
  ├── AI agent development
  ├── LLM training / inference consulting
  ├── AI infrastructure
  └── International clients
```

Initially:

* 1 shareholder: you
* 1 director: you
* Hong Kong company secretary: professional firm
* Hong Kong registered office: professional firm
* Small paid-up capital
* Business scope around software/IT/AI consulting
* Accounting/tax filing outsourced

You don't need a fancy office.

And **incorporation itself is actually the easy part**. The harder parts are later:

```text
Company
   ↓
Bank/payment account
   ↓
Accounting
   ↓
Tax compliance
   ↓
Actual clients/revenue
   ↓
Visa / right to work in HK, if you want to physically work there
```

The last point is important: **owning a Hong Kong company does not automatically give you the right to live/work in Hong Kong.** Company incorporation and immigration status are separate systems.

For what you've been considering recently, **“Hong Kong Ltd + software/AI consulting + initially operate remotely from the mainland + build HK/international clients” is a technically and administratively realistic structure.** ([Invest Hong Kong | InvestHK][6])

### References

* [Hong Kong Companies Registry — Incorporation](https://www.cr.gov.hk/en/services/register-company.htm?utm_source=chatgpt.com)
* [InvestHK — Setting up in Hong Kong](https://www.investhk.gov.hk/en/setting-hong-kong/?utm_source=chatgpt.com)
* [Hong Kong TCSP Registry](https://www.tcsp.cr.gov.hk/tcspls/?utm_source=chatgpt.com)
* [GovHK — Business & Company Registration](https://www.gov.hk/en/business/registration/?utm_source=chatgpt.com)

[1]: https://www.cr.gov.hk/en/faq/local-company/incorporation.htm?print=1&utm_source=chatgpt.com "Companies Registry - FAQ - Local Limited Companies - Incorporation"
[2]: https://www.cr.gov.hk/en/services/register-company.htm?utm_source=chatgpt.com "Companies Registry - How to register a new company?"
[3]: https://www.tcsp.cr.gov.hk/tcspls/portal/guide/1006/eng/TCSP_G1_revised_Mar2025-e.pdf?utm_source=chatgpt.com "Guideline on Licensing of Trust or Company Service Providers"
[4]: https://www.tcsp.cr.gov.hk/tcspls/index?lang=en&utm_source=chatgpt.com "TCSP Registry"
[5]: https://www.gov.hk/en/business/supportenterprises/businesstopics/licensing.htm?utm_source=chatgpt.com "GovHK: Starting a Business (Licensing, Registration & Regulations)"
[6]: https://www.investhk.gov.hk/en/setting-hong-kong/visa-immigration/?utm_source=chatgpt.com "Setting Up in Hong Kong | InvestHK"
