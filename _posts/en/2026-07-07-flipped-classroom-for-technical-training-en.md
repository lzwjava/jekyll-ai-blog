---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flipped Classroom for Technical Training
translated: false
type: note
---

**Question:** Is a teaching format of short ~10-minute recorded videos plus live Q&A sessions (Zoom / Tencent Meeting) a good way to teach programming and LLM training/inference?

**Answer:**

Yes — this is basically the "flipped classroom" model, and it's the format that works best for technical teaching. Karpathy's Zero to Hero videos prove the recorded half; the live Q&A is what most creators skip, and it's exactly where the paid value lives. Video knowledge is free and infinite on YouTube; a real human who can debug *your* CUDA OOM error or explain why *your* loss curve exploded is scarce. So the structure should be: video = free/cheap top of funnel, live sessions = the paid product.

A few things that matter for making it work in your context:

**Video design.** 10 minutes is right, but only if each video is one atomic concept with runnable code: "KV cache from scratch in 40 lines," "why RoPE, with the rotation math," "LoRA forward pass in raw PyTorch." Record your terminal, not slides. Your nanochat/DeepSeek MoE work is the content — you're already doing the research, teaching it is just packaging. This also compounds into your AI · Truth brand: every free video is a client acquisition asset, because the companies watching "how to fine-tune for your domain" are exactly your consulting targets.

**Live session design.** Don't do open-ended lectures live — that's what the video is for. Live time should be: students bring their broken code / training runs, you debug on screen, everyone learns from the debugging. This is the highest-value format and impossible to replace with recordings. Cap cohorts small (10–20) so it stays interactive. Tencent Meeting for domestic students, Zoom for HK/international — matches your two-market split.

**Pricing reality check.** Teaching individuals is low-leverage compared to your consulting rates — a cohort of 20 at ¥2,000 each is ¥40K for weeks of effort, versus one enterprise client. So position it either as (a) B2B corporate training — teach a company's engineering team LLM fine-tuning for ¥50–150K per engagement, which fits your Phase 1 perfectly, or (b) a brand engine where the free videos generate consulting leads and the paid cohort is a side revenue stream, not the main one. Corporate training is the sweet spot: it's teaching, but at consulting prices, and it often converts into implementation contracts ("now build the pipeline you just taught us").

One warning: content production eats time nonlinearly. Editing, curriculum design, student support — budget it inside your 20% product-experiment energy, not the 80% revenue core, until it proves it can convert to high-end clients.

So yes, the format is right; the leverage question is *who* you teach. Engineers individually = brand. Companies' teams = revenue.
