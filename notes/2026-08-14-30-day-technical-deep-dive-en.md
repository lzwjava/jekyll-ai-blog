---
audio: false
generated: true
image: false
lang: en
layout: post
title: 30-Day Technical Deep Dive
translated: false
type: note
---

I've read enough to give you a well-grounded picture. Here's the summary.

---

# What you did in the last 30 days (Jul 15 → Aug 14, 2026)

**652 notes** this window. The last ~18 days were much denser than the first 10, and five threads dominate:

## 1. LLM serving / inference / GPU stack — your biggest thread (~97 notes)
- **nano-vLLM deep-dive** through July–Aug 1: prefill vs decode, continuous batching, scheduler/queue internals, PagedAttention, KV cache, preemption (swap vs recompute), prefix caching, reading scheduler traces, memory formula bug fixes, CUDA graph optimization.
- **Built and ran SGLang** (Aug 2–3): compiled from source, solved flash-attn/CUDA build issues, benchmarked across 5 input lengths, studied its architecture vs vLLM and chose SGLang for some workloads.
- **Hardcore CUDA/GPU fundamentals** (Aug 1): GEMM/tiling (why 2048 beats 2047), warps, tensor cores, Volta microarchitecture, CUTLASS, FlashAttention, tensor parallelism.
- **Hardware lab**: two-GPU clusters (2080 Ti 22GB mod, RTX 3090, qwen-0.6B on 4070), AMD ROCm work (flash-attention build drama, fixed with CUDA 12.8), MI300X/MI200 research, motherboard choices (Z790 vs B760).

## 2. Model training from scratch — the other big thread (~58 notes)
- Trained **GPT-2 124M → 760M class models** (nanoGPT), toy runs on Macs, GPU memory breakdowns (24GB usage), QLoRA VRAM guides.
- **Bilingual GPT pipeline** (Aug 5 → 13): built a half-English/half-Chinese corpus pipeline with distribution control, trained a **byte-level BPE tokenizer (52-second success)**, hit kernel OOM kills (fixed with 32GB swap), got tokenization + smoke tests passing.
- Deep study notes: attention QKV/MLA via matrix ops, RoPE (outer product, implementation walkthrough), Muon/AdamW from first principles, linear attention, TTT, RNNs vs Transformers, Silu/LoRA/Peft/einsum.

## 3. CLI agents — your "product" thread (35 notes)
- Continued **ww / iclaw / zz** tools: ww note watcher integration with the pi agent's `/note` extension, bash porting, tmux/terminfo fixes, GCP speech transcription, ML pipeline help.
- Studied the agent landscape: DeepSeek Harness (everything-is-a-plugin), long-horizon agents, eval harnesses, Terminal-Bench, GDPval, DeepSpec speculative decoding.
- Aug 14 you wrote an explicit **"Focus on CLI Agent Moat"** plan — treat ww/iclaw/zz as the scalable asset, benchmark them publicly against Claude Code/Aider, and use agent traces for post-training.

## 4. US master's application — an accelerating thread (~19+ notes)
- Researched CMU MS-AII (cost breakdown), Illinois Tech Master of AI, NYU, OMSCS, USC-style programs, GRE requirements.
- **Decided: apply to Illinois Tech for Spring 2027** (window open, priority Oct 1, deadline Nov 15). Prepared English transcript, audited it (found a missing course), calculated Chinese GPA (~2.2), researched recommendation letters, F-1 visa choices, I-20/financial docs, cost (~$60-70k-ish), and B1/B2 tourist-visa strategy.

## 5. Environment, infrastructure & life admin (~94 notes)
- New Ubuntu machine setup (fcitx5/shuangpin Chinese input, Swap 32GB, SSH), Windows 11 install saga on Lenovo Xiaoxin (Ventoy, UEFI/VMD, wimlib).
- **Blog infra**: migrated Jekyll blog to **Cloudflare Pages**, fixed DNS conflicts, AdSense on Cloudflare, YouTube publishing pipeline, audio/PDF pipelines, and **reverted the homepage to show your 12.5k notes** (Aug 14).
- Startup / career thinking: one-person AI lab, AI-native kids creator startup, YC applications, AI age flattening management.

---

# Current state (as of Aug 14)

| Thread | Status |
|---|---|
| Illinois Tech application | **Ready to submit** — transcript done, planning Aug–Sep submission; the binding deadline is Nov 15 |
| Bilingual GPT | Tokenizer ✅, pipeline ✅; **next: actually pretrain** a small model |
| CLI agents (ww/iclaw/zz) | Working tools; **no public benchmark/eval harness yet** |
| nano-vLLM/sglang learning | Deep understanding ✅; **no public proof/contribution yet** |
| Blog | Live on Cloudflare, homepage back to notes, AdSense running |
| Consulting/company | Explored OPC model, Guangzhou company registration research; not registered |

---

# What to do next (in priority order)

**1. Submit the Illinois Tech application by mid-September (highest urgency).**
- Write the SOP telling the *transition* story: 10+ years backend → GPT-2 trained from scratch → nano-vLLM/sglang → CLI agents. Your weak point is credentials, not capability.
- GRE is optional there — skip it if it costs time. Line up recommenders now (Aug 14 note says Aug–Sep is the window). Oct 1 priority gives you buffer for I-20/financial docs before Jan 2027 start.

**2. Ship the CLI agent moat (your own #1 lever, Aug 14 note).**
- Pick **one** of ww/iclaw/zz, build the 200–300-line eval harness from your note, run a fixed task set vs Claude Code / Cursor, and publish numbers + harness on GitHub. This converts 18 months of tools into career capital and directly feeds the application's portfolio too.

**3. Finish the bilingual GPT pretrain.**
- You have the corpus pipeline and trained tokenizer; the natural capstone is a small pretrain run (e.g., ~100–250M on your 4070/3060) followed by 2 blog posts: "byte-level BPE in 52s" and "training a bilingual GPT from scratch." That's the proof artifact for both the lab and the application. Consider SFT/rejection sampling on ww agent traces afterward (per the moat note) instead of a second pretrain.

**4. Turn the vLLM/sglang study into public artifacts.**
- Either implement your own PagedAttention (nano-vLLM is done; this is the suggested next repo) or contribute a small fix/docs/benchmark to SGLang. Pick one, don't do both.

**5. Keep the blog pipeline humming, then go quiet on infra.**
- The site is migrated and working; batch-publish translated notes weekly and stop tweaking the platform.

**Watch out for:** the Oct exam (associate degree), funda.ai interview, and the NVIDIA NCP-GENL exam in September — all already on your TODO list. And you have a decision point lurking: OPC lab vs. US degree in Jan 2027 — start turning consulting clients into design partners *now* so the lab survives the move.

Want me to start on any of these — e.g., draft the SOP, scaffold the eval harness, or set up the bilingual pretrain config?
