---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: SenseTime AI Models Lag Rivals
translated: false
type: note
---

### Understanding SenseTime's DayDayNew and Riri Xin Models

SenseTime, one of China's "AI dragons," has been a leader in computer vision and facial recognition since 2014. In the generative AI era, they've pivoted to large language models (LLMs) under the SenseNova umbrella. "DayDayNew" (often stylized as "日日新" in Chinese) refers to their interactive AI platform and model series, with the latest DayDayNew 6.5 unveiled at the World Artificial Intelligence Conference (WAIC) in late October 2025. It's designed for multimodal tasks like processing text, images, and videos, with strong emphasis on enterprise applications, API integrations, and hardware tie-ins (e.g., Xiaomi AI glasses). "Riri Xin" (日日新 integrated model) is a related lightweight multimodal LLM launched earlier in 2025, focusing on deep reasoning, cross-modal generation, and efficiency for consumer devices.

These models aim to compete in China's hyper-competitive AI landscape but have indeed lagged in raw performance benchmarks compared to frontier players like DeepSeek (DeepSeek-V3), Kimi (Moonshot AI's Kimi series), and MiniMax (ABAB series). For context, in mid-2025 SuperCLUE benchmarks (a key Chinese LLM evaluation for reasoning, math, and general capabilities), DeepSeek-V3 topped overall scores (~85/100), Kimi K2 hit ~82, and MiniMax ABAB ~80, while SenseNova variants (including Riri Xin integrations) hovered around 70-75, often losing to MiniMax in reasoning and coding tasks. Similar gaps appear in global evals like MMLU or HumanEval, where SenseTime prioritizes multimodal over pure text reasoning.

### Why the Lag Behind DeepSeek, Kimi, and MiniMax?

Several factors explain this, rooted in SenseTime's legacy, market dynamics, and external pressures:

1. **Late Pivot from Computer Vision to LLMs**: SenseTime built its empire on perception AI (e.g., surveillance tech), only fully entering generative LLMs with SenseNova in 2023. This delayed their scaling compared to LLM-native startups. DeepSeek (founded 2023) and Moonshot AI (Kimi, 2023) started with a laser focus on efficient, open-weight models, iterating rapidly on architectures like sparse attention for cost-effective training. MiniMax, despite being younger (2021), optimized for consumer apps like video gen (Hailuo) from day one.

2. **US Entity List Sanctions**: Blacklisted by the US in 2019 for alleged human rights issues, SenseTime faces restricted access to advanced chips (e.g., NVIDIA GPUs) and US tech. This hampers training at the scale of rivals—DeepSeek uses domestic Huawei Ascend chips innovatively, while Kimi and MiniMax leverage hybrid setups without the same export curbs. Result: Slower model updates and higher costs, widening the performance gap.

3. **Agile Startups vs. Established Giant**: SenseTime is a public company (HKEX-listed) with ~$1B+ revenue, serving enterprise clients (e.g., banks, governments). This brings bureaucracy and a focus on compliant, multimodal solutions over bleeding-edge benchmarks. In contrast:
   - DeepSeek emphasizes "fast, cheap, open" models, topping open-source leaderboards with low inference costs.
   - Kimi excels in long-context reasoning (up to 200K tokens), rivaling OpenAI's o1.
   - MiniMax shines in multimodal (text-to-video) and efficiency, often beating SenseTime head-to-head.

   Ironically, MiniMax's founders (Yan Junjie and Zhou Yucong) are ex-SenseTime engineers who led deep learning toolchains there. They left to build a nimbler startup, taking that expertise to outpace their old employer—highlighting how talent mobility fuels China's AI arms race.

4. **Benchmark and Hype Dynamics**: Chinese evals like SuperCLUE reward reasoning/math, where startups over-index. SenseTime's strength is integration (e.g., SenseCore cloud for fine-tuning), but they underperform in "frontier" tests. Less hype means fewer users/data for iteration, creating a feedback loop. As of October 2025, SenseTime holds ~14% AIGC market share (top 3), but that's revenue, not capability.

### Recent News and What SenseTime Has Been Doing

News on SenseTime has been quieter than the startup frenzy (e.g., DeepSeek's viral R1 release), but they're active in enterprise/gen AI growth:

- **April 2025**: Launched SenseNova V6 Omni, China's "most advanced" multimodal model per their claims, with upgrades to SenseCore 2.0 infrastructure for better model understanding.
- **June 2025**: Joined ByteDance/Alibaba in model updates amid the AI race, emphasizing cost-efficient APIs.
- **August 2025**: DayDayNew platform integrated with Xiaomi AI glasses; revenue surged 21% YoY from gen AI demand (training/inference services).
- **September 2025**: Spun off non-core units to streamline gen AI focus, pushing toward profitability.
- **October 2025**: DayDayNew 6.5 and Mynie platform at WAIC, boosting multimodal interaction (e.g., video comprehension up 30%).

They're doubling down on B2B (e.g., cloud services, device embeds) rather than consumer chatbots, which explains the "no news" vibe—less viral demos, more quiet enterprise wins. Still, with sanctions easing talks and domestic chip advances, they could close the gap by 2026.

In short, SenseTime's legacy weighs it down in a startup sprint, but their multimodal bet positions them for practical wins over pure benchmark chases.

[ChinAI #324: SuperCLUE Benchmarks —2025 Midyear Check-in](https://chinai.substack.com/p/chinai-324-superclue-large-model)
[SenseTime's SenseNova Foundation Models Among Top Three](https://www.sensetime.com/en/news-detail/51169429?categoryId=1072)
[An Overview of Chinese AI Tigers](https://www.topbots.com/chinese-ai-tigers-overview/)
[China's SenseTime Reshapes to Focus on Generative AI Growth](https://www.reuters.com/technology/artificial-intelligence/chinas-sensetime-reshapes-focus-generative-ai-growth-2024-12-04/)
[SenseTime Unveils DayDayNew 6.5 AI Model](https://forntend-test-5sqwmq-3a22a9-107-172-80-230.traefik.me/sensetime-unveils-daydaynew-6-5-ai-model-and-mynie-platform-1753705726167)
