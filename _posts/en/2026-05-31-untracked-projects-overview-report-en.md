---
audio: false
generated: true
image: false
lang: en
layout: post
title: Untracked Projects Overview Report
translated: false
type: note
---

Here's the full picture of your ~/projects untracked repos:

== MOST ACTIVE UNTRACKED REPOS (top tier — still very active upstream) ==

  keras              12,433 behind  last 2026-05-29  -- Keras 3.x, massive activity
  Chat2DB             3,893 behind  last 2026-05-28  -- AI-powered DB client, hot project
  simpletransformers  1,954 behind  last 2026-05-29  -- NLP/LLM fine-tuning lib
  claude-relay-service 1,866 behind last 2026-05-24  -- Claude API relay, active
  v2rayN              1,675 behind  last 2026-05-31  -- V2Ray GUI client for Windows
  fineract            1,576 behind  last 2026-05-31  -- Apache Fineract (finance platform)
  seeker                895 behind  last 2026-05-22  -- Rust proxy tool by gfreezy
  ROCm                  17 behind  last 2026-05-29  -- AMD GPU platform docs/tools
  ChezScheme            43 behind  last 2026-05-12  -- Cisco's Chez Scheme compiler

== MODERATE ACTIVITY (worth checking) ==

  FlagEmbedding       158 behind   last 2026-04-22  -- BAAI embedding models
  dubbo                52 behind   last 2026-01-26  -- Apache Dubbo 3.2 branch
  voice-changer      1,743 behind  last 2026-03-21  -- Real-time voice changer (AI)
  h2ogpt             7,982 behind  last 2025-10-09  -- H2O AI LLM platform
  coding-interview-university 2,476 behind  last 2024-12  -- Study guide

== FRESHLY FETCHED (already caught up) ==

  git-credential-manager  0 behind  last 2026-04-28
  Bodhi-AI                0 behind  last 2026-05-16
  Axono                   0 behind  last 2026-02-06

== DEAD / STALE (delete candidates) ==

  char-rnn (Karpathy 2016), seq2seq (Google 2017), Sublist3r (2020),
  TikTok-Clone (2022), stable-diffusion CompVis (2022, replaced by SDXL/SD3),
  v2ray-core (2023, superseded by Xray), OpenWRTInvasion (2023),
  deep-learning-papers (2019), attention-is-all-you-need-pytorch (2021),
  ChatGLM-6B (2024, replaced by GLM-4), freegpt-webui (2023, dead)

== RECOMMENDED ADDITIONS TO repos.json ==

Your tracked repos are all at 0 behind (up to date). The most interesting
untracked repos worth adding:

  AI/ML:
    - keras (12K behind, very active, Keras 3 multi-backend)
    - simpletransformers (2K behind, fine-tuning toolkit)
    - FlagEmbedding (158 behind, BAAI embeddings)
    - ROCm (17 behind, you have MI300X access!)
    - ChatGLM-6B → swap for GLM-4 or drop

  Dev Tools:
    - Chat2DB (4K behind, AI DB client)
    - git-credential-manager (active)
    - ChezScheme (43 behind, interesting compiler)

  Networking:
    - v2rayN (1.7K behind, active V2Ray client)
    - seeker (895 behind, Rust proxy)

  Cleanup candidates (delete from ~/projects):
    - char-rnn, seq2seq, Sublist3r, TikTok-Clone, stable-diffusion (CompVis),
      v2ray-core, OpenWRTInvasion, freegpt-webui, ChatGLM-6B,
      deep-learning-papers, attention-is-all-you-need-pytorch

Want me to update repos.json to add any of these, or clean up the stale ones?