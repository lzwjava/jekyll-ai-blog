---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bifurcation of Global AI Infrastructure
translated: false
type: note
---

**Question:** Given China's aggressive data center expansion in Ulanqab and the West's NVIDIA/OpenAI build-out, what will the future IT infrastructure landscape look like?

**Answer:**

You're watching a **bifurcation of global AI infrastructure** in real-time. Two separate, parallel compute stacks emerging — neither can totally decouple, but friction is rising fast. Here's the structural reality:

**US/Allied Advantage: Hardware Moat**

NVIDIA will invest up to $100 billion in OpenAI to deploy 10 gigawatts of AI data centers using next-generation Vera Rubin systems, with the first phase coming online in H2 2026. America's main hyperscalers—Alphabet, Amazon, Meta, and Microsoft—have plans to spend a total of $650 billion just this year on data centers reaching gigawatt scales with hundreds of thousands of AI accelerators.

This is **compute supremacy through advanced chip manufacturing**. The Trump administration released America's AI Action Plan to accelerate AI innovation and assert American leadership by promoting export of the full American AI technology stack to allies while tightening enforcement on adversaries.

The vulnerability: By mid-2025, US authorities banned even specialized AI chips designed to meet earlier export rules, effectively closing the last major chokepoint for top-tier AI hardware.

**China's Counter-Strategy: Indigenous Stack + Cheap Compute**

Chinese domestic chips made up nearly 41% of China's market in 2025, with approximately half coming from Huawei, up from Nvidia having 90%+ market share before 2023. But here's the catch: Huawei will produce only 200,000 AI chips in 2025, while China legally imported around 1 million Nvidia chips downgraded for the Chinese market in 2024.

China compensates with **scale + cheap infrastructure**:
- Ulanqab model: abundant wind power (pennies per kWh), no land costs, government subsidies
- 10+ data center clusters across the west targeting 1,200+ MW additional capacity
- Can afford to run lower-efficiency hardware at massive scale

**The Math:**

Building one gigawatt of data center capacity costs $50-60 billion, of which ~$35 billion is Nvidia chips.

- **US path:** $100B buys 2-3 GW of cutting-edge Blackwell/Vera Rubin compute
- **China path:** Same $100B buys 5-10 GW of Huawei/domestic chips running at 5-10% lower efficiency, but at 1/3 the power cost

China wins on **volume and cost structure**; US dominates on **performance density and model-to-inference time**.

**The Divergence:**

A complete decoupling of US and Chinese tech spheres could force countries to navigate two separate technology universes with incompatible standards, with data centres, networks and AI ecosystems divided by incompatible standards and mutual suspicions.

Expected outcomes by 2027-2030:

1. **Model Training Split:**
   - US: Training frontier models (GPT-5/6 class) on Nvidia hardware in US/allied data centers
   - China: Training large models (DeepSeek-class) at scale on domestic chips, same capability, longer iteration cycles (lower FLOP efficiency)

2. **Inference Divergence:**
   - US: Inference at scale on proprietary platforms (Azure, AWS, Oracle) — expensive, closed
   - China: Inference distributed across Ulanqab clusters — cheaper, more accessible to Chinese companies

3. **Developer Reality Check:**
   - If you're training cutting-edge models: requires NVIDIA hardware access (expensive or restricted)
   - If you're doing inference at scale: China's infrastructure wins on cost; US wins on latency/quality
   - Small/medium teams: fragmenting into US (cloud APIs: OpenAI, Claude, Anthropic) or China (DeepSeek, Alibaba)

**For AI Engineers Like You (Practical Implications):**

- **If building general AI tooling:** Assume dual-stack support (CUDA + Ascend/DCU) from day one — incompatible APIs are coming
- **If doing research/training:** Nvidia dominance persists for next 2-3 years; after that, domestic Chinese alternatives (Ascend 950PR, Huawei's CUDA-compatible efforts) become viable but with 10-20% performance tradeoff
- **If optimizing inference:** Location matters — US for latency-critical, China for cost-optimized
- **Opportunities:** Anyone who can write portable, hardware-agnostic ML ops (think multi-backend optimization) wins across both ecosystems

**The Wild Card:**

In December 2025, Trump approved conditional export of Nvidia's H200 chip to approved customers in China with 25% US government revenue share — political volatility is the real constraint. Export rules are a **dial being turned by governments**, not a technical moat. Expect continued policy churn.

**Bottom Line:**

By 2027: **Two AI infrastructure worlds** — US/allied with superior chips but constrained by policy/cost, China with sufficient chips but less efficient hardware compensated by scale + cheap operations. Most AI work will run on both, but optimized differently.

For someone at your level trying to build frontier AI systems: **Get comfortable with both stacks now.** DeepSeek already is. Your edge is being able to navigate both ecosystems fluently.

**References:**

- Nvidia plans to invest up to $100 billion in OpenAI (CNBC, Sept 2025)
- AI geopolitics and data in the era of technological rivalry (WEF, July 2025)
- Competing AI strategies for the US and China (Brookings, April 2026)
- How US Export Controls Have (and Haven't) Curbed Chinese AI (AI Frontiers, July 2025)
