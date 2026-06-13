---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Zhuohan Li: vLLM Co-Creator"
translated: false
type: note
---

**Question:** Who is Zhuohan Li (李卓涵) in vLLM?

**Answer:**

Zhuohan Li (GitHub: `zhuohan123`) is **co-creator of vLLM**, equal in founding status to Woosuk Kwon. Here's the full picture:

**Origin story:** In summer 2022, Li and fellow researcher Woosuk Kwon were working to make large deep-learning models more efficient by distributing work across GPUs. When they set up a demo, performance was terrible. Li said "We realized memory management was going to be a big bottleneck for serving these models." Over the next couple of months, Li and Kwon dug in and eventually developed PagedAttention, inspired by classical virtual memory and paging techniques.

**Background:** Zhuohan Li is a CS PhD student at UC Berkeley advised by Ion Stoica, focused on efficient ML systems — specifically training and serving large models. His works include Alpa, AlpaServe, Vicuna, and vLLM (PagedAttention). He completed his BS at Peking University and interned at Microsoft Research, Anyscale, and Google Brain.

**PhD thesis:** His 2024 Berkeley thesis "Empowering Large Language Models with Efficient and Automated Systems" covers AlpaServe (model parallelism for serving scalability) and vLLM/PagedAttention (memory utilization and inference throughput).

**Now at Meta + OpenAI stint:** After building vLLM, Li joined OpenAI, where he led infra and inference work that brought GPT-OSS to life. He's currently building vLLM at Meta.

**TL;DR:** Zhuohan Li is **the Chinese co-founder of vLLM** (Peking University undergrad → Berkeley PhD under Ion Stoica), co-invented PagedAttention alongside Woosuk Kwon, then went to OpenAI and is now at Meta continuing vLLM work. He's `zhuohan123` on GitHub/X.
