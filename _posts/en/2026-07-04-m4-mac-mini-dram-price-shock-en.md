---
audio: false
generated: true
image: false
lang: en
layout: post
title: M4 Mac Mini DRAM Price Shock
translated: false
type: note
---

**Question:** The base M4 Mac mini now costs ~5,000 CNY in China because of the memory price surge. But Apple uses "unified memory" — is that DRAM too?

**Answer:**

Yes — unified memory **is** DRAM. Specifically, the M4 uses **LPDDR5X** (Low-Power DDR5X), which is just a mobile-optimized variant of DRAM made by the same three vendors driving this price cycle: Samsung, SK Hynix, and Micron. So Apple is fully exposed to the shortage.

**What "unified memory" actually means (and doesn't mean)**

"Unified memory" is an *architecture* term, not a *memory technology* term. The stack looks like this:

```
Memory cell technology:   DRAM (1 transistor + 1 capacitor per bit)
├── DDR5      → desktop DIMMs
├── LPDDR5X   → Apple M-series, phones      ← still DRAM
├── GDDR7     → discrete GPUs               ← still DRAM
└── HBM3E     → AI accelerators (MI300X)    ← still DRAM
```

What Apple does differently is **packaging and addressing**:

1. **Packaging:** LPDDR5X dies sit on the same package substrate as the SoC (not soldered on the motherboard, not socketed DIMMs). Short traces → wide bus (128-bit on base M4, ~120 GB/s) at low power.
2. **Unified address space:** CPU, GPU, and Neural Engine share one physical pool with a single memory controller. No PCIe copy between "system RAM" and "VRAM" — which is exactly why your 16GB M-series Mac can run LLM inference that would need a 16GB discrete GPU on PC.

But the silicon inside those packages is commodity DRAM cells from the same fabs, on the same wafers, competing for the same capacity that HBM is now eating.

**Why Apple got hit hard**

The AI datacenter buildout redirected fab capacity toward HBM (which uses ~3x the wafer area per bit due to TSV stacking), squeezing LPDDR/DDR supply. The numbers this cycle: DDR5 prices up over 300% since September 2025, and LPDDR4X/LPDDR5X contract prices jumped ~90% QoQ in Q1 2026 — the largest quarterly increase on record. LPDDR5X is literally what's inside your M4's package.

Apple's response timeline:

- **April 2026:** Top-spec Mac mini/Mac Studio delivery times stretched to 16–18 weeks; the higher the memory config, the longer the wait
- **May 2026:** The 16GB+256GB base config (4,499 CNY) was pulled from Apple's store globally; the cheapest config became 16GB+512GB at 5,999 CNY. Cook admitted Apple underestimated demand for local AI workloads and cut high-memory SKUs to protect base model supply
- **June 25, 2026:** Apple raised Mac and iPad prices globally by roughly 15–25% on average; the Mac mini saw the steepest hike (+41% in Hong Kong, from HK$4,599 to HK$6,499)

So the ~5,000 CNY you're seeing on third-party channels (JD/Pinduoduo) for the old 256GB config is actually *cheap* relative to Apple's official 5,999 CNY floor now. On V2EX people note it was 2,999 CNY before Chinese New Year — and blame the agent-farm crowd buying them up for openclaw-style workloads.

**Practical takeaway for you**

- The "memory always gets cheaper" heuristic is broken until at least H2 2026, possibly 2027 — new fabs won't come online before late 2027, though some Huaqiangbei traders bet on a crash in H2 2026. It's a genuine uncertainty, not a consensus.
- If you were eyeing a Mac mini as a cheap always-on agent box (Claude Code / iclaw runner), the arbitrage window mostly closed. Your RTX 4070 workstation at 192.168.1.36 is unaffected — its GDDR6 is already paid for.
- Same force is inflating your MI300X cloud economics indirectly: HBM3 demand is *the* root cause of this whole cycle.

**References:**

- [苹果M4版Mac mini取消256GB入门配置，起售价涨至5999元 — 新浪财经](https://finance.sina.com.cn/roll/2026-05-03/doc-inhwqvrp0970331.shtml)
- [受内存短缺影响，苹果下架多款高内存配置MAC设备 — CFM闪存市场](https://www.chinaflashmarket.com/newsflash/37443)
- [Mac 和 iPad 全線即日起加價，Mac mini 加價逾四成 — Unwire.hk](https://unwire.hk/2026/06/25/apple-price-hike-mac-mini-ramageddon-2026/notebook/)
- [内存涨价300%！这波"超级周期"要涨多久 — 21经济网](https://www.21jingji.com/article/20260120/herald/0d00b19fda01cb66284fc926da5c86b8.html)
- [内存价格罕见回调，"超级周期"什么时候走到拐点 — 证券时报](https://stcn.com/article/detail/3630474.html)
