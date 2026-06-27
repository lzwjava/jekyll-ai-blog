---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Netris: AI Cloud Networking Automation"
translated: false
type: note
---

Question: What is Netris, the GPU-related company that a16z invested in?

Answer:

I need to search for this—Netris isn't a company I can confirm details about from memory, and "a16z invested" is exactly the kind of fact that needs verification.Question: What is Netris, the GPU-related company that a16z just invested in?

Answer:

Netris isn't a GPU company per se — it's the **networking automation layer for GPU clouds**. a16z led a $15M Series A (announced June 25, 2026), with partner Guido Appenzeller joining the board. Worth understanding the technical wedge, because it's directly relevant to the AI infra stack you care about.

## The actual problem they solve

When you build a neocloud (a GPU-first AI cloud), securing the H100s/MI300Xs is the easy part. The hard part: getting a data center ready for AI inference and training can take months of work — and the longer it takes, the more those expensive GPUs sit idle. Netris automates the network fabric configuration so operators go live in weeks instead of quarters.

The architectural insight is the key bit. Modern AI data centers have **two** networks:

1. **Front-end network** — classic fat-tree of switches for server↔server, server↔storage, server↔internet (PCIe NICs).
2. **Back-end network** — a second network that directly connects GPUs with each other. This is the NVLink/InfiniBand fabric. This architectural change is exactly why NVIDIA became a major networking vendor alongside protocols like NVLink and Infiniband.

For your training mental model: when you do distributed training (data/tensor/pipeline parallelism), the all-reduce and all-to-all collectives ride the back-end fabric. Training runs for LLMs require near-perfect synchronization across thousands of GPUs, where even microseconds of latency can torpedo performance. That's the back-end network doing its job — and it's brutal to configure correctly across thousands of links.

## What the product actually is

It's called NAAM — Network Automation, Abstraction, and Multi-Tenancy. Mechanically: Netris installs agents that run on the network switches, plus a control-plane platform that connects to those switches to automate setup, configuration, and operations. The TechBuzz framing is the cleanest analogy — think of it as Kubernetes for the network layer: a cloud-like control plane for physical network infrastructure, letting operators manage switching fabric through APIs rather than CLI and manual configs.

The multi-tenancy piece matters for the business model: it isolates servers and resources at the hardware layer so neoclouds can serve multiple customers — i.e. hardware-enforced VPCs, not software overlays.

## The contrarian technical bet — and why it's interesting for you

This is the part worth internalizing given your AI-native bias: **Netris deliberately uses no AI in its product.** It relies on deterministic algorithms developed before the AI boom. Saroyan's reasoning is sharp: "AI is not deterministic... for changing many thousands of switch configurations, you don't need to be creative. You need to be very persistent and repeatable."

This is a useful counter-example to hold against your "favor the AI-native approach" heuristic. Network config is a domain where **determinism is the entire value proposition** — a non-deterministic agent flipping switch configs on a billion-dollar cluster is a liability, not a feature. The lesson generalizes: AI-native wins where exploration/creativity/ambiguity dominate; deterministic systems win where correctness and repeatability are non-negotiable. Knowing which regime you're in is the skill.

Why traditional approaches fell short: data centers used SDN (software-defined networking), but SDN falls short because it's software — and for AI, the traffic volume is so high that everything must be hardware-accelerated.

## Why a16z specifically

This isn't a random infra bet — it's a band reunion. Appenzeller led the round (ex-Big Switch Networks co-founder, ex-VMware Cloud/Networking CTO), supported by Martin Casado and Raghu Raghuram. Casado founded Nicira — the startup that pioneered SDN, acquired by VMware in 2012 — and Raghuram became VMware's CEO. The thesis in one line: Netris could become the NSX of AI clouds — i.e. reinventing SDN for the AI era the way NSX did for the virtualized data center.

## Traction (the numbers that justified the round)

- 800% annual recurring revenue growth, live at 35+ GPU clusters totalling roughly one million GPUs.
- Previously 622% YoY ARR growth in 2025; had raised under $6M total before this round.
- Customers: Lightning AI, TensorWave, Foxconn-backed Visionbay (Taiwan's largest GPU cluster), Firmus (Australia's largest renewable-powered sovereign AI factory), TELUS, HPE.
- Founded 2018, Santa Clara HQ, with teams across the US, UK, Taiwan, Australia, Armenia, and India. The Armenia footprint tracks — Saroyan and the founding team have Armenian roots.

If you want, I can sketch out what the back-end GPU fabric (rail-optimized topology, NCCL collectives over RoCE/InfiniBand) actually looks like at the packet level — that's the layer Netris abstracts, and it's directly relevant to multi-node training on your MI300X.

References:

- [Investing in Netris — a16z](https://a16z.com/announcement/investing-in-netris/)
- [Netris raises $15M Series A from a16z — TechCrunch](https://techcrunch.com/2026/06/25/netris-raises-15m-series-a-from-a16z-to-help-ai-neoclouds-go-live-faster/)
- [Why a16z and Netris are getting the SDN band back together — Futuriom](https://www.futuriom.com/articles/news/why-a16z-and-netris-are-getting-the-sdn-band-back-together/2026/06)
- [Netris secures $15M Series A — Crypto Briefing](https://cryptobriefing.com/netris-a16z-series-a-ai-networking/)
