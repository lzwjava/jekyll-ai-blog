---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sulaiman Ghori on xAI Internals
translated: false
type: note
---

Question: What does Sulaiman Ghori say about how xAI/Grok works internally?

Answer: Ghori was a Member of Technical Staff at xAI (March 2025–Jan 2026) who worked on Grok/X integration, then gave a widely-shared interview on the *Relentless* podcast about xAI's internals — apparently detailed enough that he was reportedly terminated as a result of disclosing proprietary information. Key technical/operational claims from that interview:

**Speed over process**
xAI prioritizes speed and leverages its hardware infrastructure to achieve daily model iterations, challenging conventional timelines. Model iterations happen daily, sometimes multiple times a day — even from pre-training, and hardware racks start training within hours of setup, versus days or weeks elsewhere.

**Musk's hands-on bottleneck-clearing**
Musk's hands-on approach quickly resolves bottlenecks, such as deploying patches overnight to run models on new hardware. Musk is described as excelling at forecasting bottlenecks months to years ahead and working backwards from them; teams mirror this by focusing on core financial/physical metrics.

**Colossus / infra as the actual moat**
The Colossus data center — the cluster Grok trains on — was completed in 122 days, which he frames as the real edge over other labs, not just algorithms.

**Removing artificial software overhead**
xAI achieves 2x to 8x improvements in software performance by removing artificial overhead and focusing on fundamental physical limits (i.e. treating latency/throughput as a physics problem, not a config problem).

**Culture: no assigned role, bottom-up**
His onboarding: he received a laptop and a badge but no specific instructions or team assignment, and spent his first days finding projects to help with, eventually working on Grok's integration with the X platform. The company values engineers who can find simple solutions and challenge requirements, fostering a bottom-up culture where good ideas are quickly implemented.

**Beyond-chatbot roadmap**
xAI is working on "MacroHard," a human emulator, and is exploring using Tesla car computers for deployment — i.e. using idle FSD-chip compute in cars as a distributed inference/training network instead of building more datacenters, aiming eventually at emulating millions of humans via distributed Tesla chips.

None of this is architecture-level detail (no attention variant, MoE config, context length internals) — it's org/infra/culture, which is consistent with what actually got him let go rather than a leaked spec.

References:
- [WTF is happening at xAI — Sulaiman Ghori, Relentless (Podwise)](https://podwise.ai/dashboard/episodes/6885430)
- [Podcast Notes: WTF is happening at xAI](https://www.podchemy.com/notes/wtf-is-happening-at-xai-sulaiman-ghori-48474640483)
- [Inside xAI's Culture of Relentless Speed and Hardware Leverage — StartupHub.ai](https://www.startuphub.ai/ai-news/ai-video/2026/inside-xais-culture-of-relentless-speed-and-hardware-leverage)
- [Inside xAI and Future of Millions of Emulated Humans — NextBigFuture](https://www.nextbigfuture.com/2026/01/inside-xai-and-future-of-millions-of-emulated-humans.html)
- [Sulaiman Khan Ghori — Grokipedia](https://grokipedia.com/page/Sulaiman_Khan_Ghori)
