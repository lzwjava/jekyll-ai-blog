---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Shennan Circuits: 3-In-One Business Model"
translated: false
type: note
---

Question: **What is 深南电路 (Shennan Circuits / SCC)?**

Answer:

![Image](https://images.openai.com/static-rsc-4/wWXFAisRVSBp4FDIFwx1bR42BeZbYiFVFrxoXDK1izC1DHNxK5ApNPuBnQZeVWPy637GuF-PJzKc5L_ilwykDsJTxHrmxecv2uVwOcGFW4n4nQOgjRXi3BoeUkzECC0S-BTxJjt2_C1qfCC4KsRzPq6SCCL3bw5T1Ujxk4sW5b79UomRXKIKlPLi4MF3MSqf?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/y22TF8RVoKn1z7Km4lTMydzkyzSf_8MBPZdLB6FvokyXX4qnVyVGWSKCTjJyu0mifqErAEYmjRRVLtjEhGdpH7YnnbavyGZWAM3C4TDkkoJPSWQr0fRdIHY77PRs75P6rd60LBPoj64ZI_LnLF6n__SjLT3xBQ5r3KffrjV3NzqNwnXK75YrxwrQSzRaFpyt?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/E353jnIsRe7d3wxSPFS-mtzQDXh5uySDI3dXLHvGmmzvg5x9LAZ-QyEoAcKgxJ8hR_BtFsQr2o3iC2gG9ybF8aZYtp0xgZ3nrG8KGjDIg2SzAH7zekSRtSJcOwOyzY_LvVs-0tE11W5RgYYrglKgFKnibQfAV2Y6kzIF8uYTarvxKQGPlrAGcLFr_ypbiB3s?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/kzJj380ecKQrOmNnpMc8mSPXr3U9zsGYTY8B0Uer7LRfx9SlKO32vvekAgowBp2whjbQDaDrdJFiDxcDG1h9xoubTarhArTM_tWS9yqVNIlTxV4ksl0vPtJNcE9eV5T7sx_hRvDFb6EzVft7o1lmBO5Coxnf1F7cAVoBLClKLMTF0N4E3FUGFOtYrHWxr7qP?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/AQhycm0sMOOiqNANYh5f3BJ8MpkJpbDOO1SzMBJR-DwjkrcbG0u0O9K5T1jRk_rkaStLdv6kkBffJTTdZBIA3_bEioHZqmbPaypJ-55xECd-jW0ExmtNkFNVIwmbkbryexhwOMbtnfRIQKtbJiqwJJBm2qRfH3VKoe2gcJCU1fAfaXSBggIm8OrXzvTFRYSV?purpose=fullsize)

**深南电路股份有限公司 (Shennan Circuits, SCC)** is a major Chinese electronics-manufacturing company focused on **PCB, semiconductor packaging substrates, and electronic assembly**. It was founded in **1984**, headquartered in Shenzhen, and is listed on the Shenzhen Stock Exchange as **002916**. ([SCC][1])

The simplest mental model is:

```text
Chip
  │
  ▼
┌─────────────────────┐
│ Packaging substrate │  ← connects chip/package
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│        PCB          │  ← connects components
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       PCBA          │  ← PCB + chips/components
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Electronic system   │
└─────────────────────┘
```

SCC calls this its **"3-In-One"** business model: **PCB + packaging substrate + electronic assembly**. Its manufacturing/service capability covers roughly Level 1–3 of the electronics packaging chain. ([Cninfo][2])

### 1. PCB is still the core business

PCB = **Printed Circuit Board**.

For example, an AI server might contain:

```text
NVIDIA GPU
   ↓
GPU package
   ↓
GPU board / accelerator PCB
   ↓
Server motherboard
   ↓
Network / storage / power boards
```

SCC manufactures the sophisticated PCBs connecting these components.

Its important PCB applications include:

* telecommunications
* data centers / servers
* AI computing infrastructure
* automotive electronics
* industrial control
* medical equipment

The company particularly emphasizes **high-speed, high-frequency, high-layer-count and high-density PCBs**. ([Sina Finance][3])

### 2. Packaging substrates are the semiconductor side

This is probably the more interesting part if you're looking at **AI hardware**.

A packaging substrate sits roughly here:

```text
        Silicon die
           │
           ▼
    ┌──────────────┐
    │   Package    │
    │ ┌──────────┐ │
    │ │   Die    │ │
    │ └──────────┘ │
    └──────┬───────┘
           │
     Package substrate
           │
           ▼
          PCB
```

It is much more precise than an ordinary PCB and provides electrical connections, mechanical support and thermal-related functions between the chip package and motherboard.

SCC produces substrates for:

* memory
* application processors
* RF
* FC-CSP
* FC-BGA
* other semiconductor packages

Its 2025 packaging-substrate revenue was **RMB 4.15 billion**, up **30.8% YoY**, according to its 2025 annual report. ([Sina Finance][3])

It was also building capability for higher-layer **FC-BGA** substrates, with 22-layer-and-below products already in mass production and 24-layer+ products in development/sampling at the time of the report. ([FinancialFilings][4])

### 3. PCBA / electronic assembly

The third business is basically:

```text
Bare PCB
   +
CPU / GPU / memory / PMIC / capacitors / connectors...
   ↓
SMT / THT / assembly
   ↓
PCBA
   ↓
Testing
   ↓
Electronic system
```

So SCC isn't merely selling bare circuit boards. It can participate further downstream in **design → PCB manufacturing → component assembly → testing → system assembly**. ([Cninfo][2])

---

## Scale

2025 was a very strong growth year for SCC.

| 2025                 |        Revenue |         YoY |
| -------------------- | -------------: | ----------: |
| **Total**            | RMB **23.65B** | **+32.05%** |
| PCB                  | RMB **14.36B** | **+36.84%** |
| Packaging substrates |  RMB **4.15B** | **+30.80%** |
| Electronic assembly  |  RMB **3.07B** |  **+8.93%** |

PCB therefore remained the largest business at about **61% of total revenue**. ([Sina Finance][3])

And this is increasingly an **AI infrastructure story**: SCC's 2025 annual report explicitly says growing AI-computing infrastructure investment was driving demand for high-end electronic circuits, and its 2026 strategy focuses on capturing this structural growth. ([Shenzhen Stock Exchange][5])

The company reported that, according to Prismark's 2025 Q4 report, it was expected to rank **4th globally among PCB manufacturers by 2025 revenue**. ([FinancialFilings][4])

### Where it sits in the semiconductor/AI hardware ecosystem

I'd think about the ecosystem like this:

```text
TSMC / Samsung / Intel
        │
        │ wafers / dies
        ▼
Chip designers
NVIDIA / AMD / Broadcom / etc.
        │
        ▼
Packaging / OSAT
        │
        ▼
┌───────────────────────────┐
│     Shennan Circuits      │
│                           │
│  IC substrate             │
│       ↓                   │
│  PCB                      │
│       ↓                   │
│  PCBA / electronic system │
└───────────────────────────┘
        │
        ▼
Server / networking / telecom
        │
        ▼
AI data center
```

So **SCC isn't a chip designer like NVIDIA and isn't a semiconductor foundry like TSMC**.

It's an **electronics interconnect + manufacturing company** sitting between chips and complete electronic systems.

For your interests, the particularly relevant part is that **AI accelerators, high-speed networking, servers and data centers require increasingly sophisticated PCBs and package substrates**. That's one reason SCC has been benefiting from the AI infrastructure capex cycle. ([Cninfo][2])

**References:**

* [Shennan Circuits — Company Profile](https://www.scc.com.cn/scc/gysn/index.html?utm_source=chatgpt.com)
* [Shennan Circuits — 2025 Annual Report](https://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?id=11992852&stockid=002916&utm_source=chatgpt.com)
* [Shennan Circuits — 2026 H1 Report](https://static.cninfo.com.cn/finalpage/2026-08-27/1225512708.PDF?utm_source=chatgpt.com)
* [Shennan Circuits — Products & Technology](https://www.scc.com.cn/scc/cpjs/index.html?utm_source=chatgpt.com)

[1]: https://www.scc.com.cn/scc/gysn/index.html?utm_source=chatgpt.com "深南电路 - 关于深南"
[2]: https://static.cninfo.com.cn/finalpage/2026-08-27/1225512708.PDF?utm_source=chatgpt.com "深南电路股份有限公司 2026 年半年度报告全文"
[3]: https://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?id=11992852&stockid=002916&utm_source=chatgpt.com "深南电路(002916)_公司公告_深南电路：2025年年度报告新浪财经_新浪网"
[4]: https://financialfilings.com/filings/shennan-circuits-co-ltd/annual-report/2026/36790692/?utm_source=chatgpt.com "Shennan Circuits Co., Ltd. - Annual Report 2025 | FinancialFilings"
[5]: https://disc.static.szse.cn/disc/disk03/finalpage/2026-03-13/342c7f6b-cc0c-4592-9d25-9f95ae113d57.PDF?utm_source=chatgpt.com "深南电路股份有限公司 2025 年年度报告全文"
