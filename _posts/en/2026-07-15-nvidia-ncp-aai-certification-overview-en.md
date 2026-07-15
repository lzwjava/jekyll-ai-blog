---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA NCP-AAI Certification Overview
translated: false
type: note
---

Question: What is NVIDIA's NCP-AAI certification?

Answer: NCP-AAI = **NVIDIA-Certified Professional: Agentic AI (LLMs)**. It's NVIDIA's newest professional cert, distinct from the older NCA-GENL (associate-level GenAI/LLM cert) and NCP-AII (infrastructure ops cert).

Exam mechanics:

- **60–70 questions, 90–120 min** (docs are inconsistent — NVIDIA's own page says 60-70Q/120min, third-party guides say 90min — check Certiverse at registration)
- **$200**, online, remote-proctored via Certiverse
- Valid 2 years, recert = retake

Prerequisites (soft, not enforced): 1–2 yrs AI/ML production experience, hands-on with agent orchestration, multi-agent frameworks, tool/model integration.

Five domains it tests: Agent Design and Cognition (architecture, reasoning/planning, memory, multi-agent coordination); Knowledge Integration and Agent Development (RAG pipelines, data handling, prompt engineering, multimodal agents); NVIDIA Platform Implementation and Deployment (inference optimization, scale deployment, production workflows); Evaluation, Monitoring, and Maintenance (benchmarking, tuning, live monitoring, troubleshooting); Human, Ethical, and Compliance Considerations (human-in-the-loop design, safety/compliance guardrails).

Given you're already training models on MI300X and building your own agent CLIs (ww/iclaw/zz), this cert is mostly a signaling/HR-checkbox exercise for you rather than a knowledge gap — the domains map to stuff you've already shipped. Only worth it if a client/contract explicitly asks for the badge.

One thing to verify before paying: as of the March 2026 GTC keynote, NVIDIA's reference model family shifted to Nemotron 3 (Super 120B/12B-active GA, Ultra in preview, Nano 4B and Nano Omni for edge/multimodal) — if you study from anything pre-April 2026 you'll get outdated model references on the exam.

References:

- [Agentic AI LLMs Certification for Professionals | NVIDIA](https://www.nvidia.com/en-us/learn/certification/agentic-ai-professional/)
- [Certification Programs | NVIDIA](https://www.nvidia.com/en-us/learn/certification/)
- [NCP-AAI Complete Guide 2026 | Preporato](https://preporato.com/blog/nvidia-ncp-aai-certification-complete-guide-2025)
