---
audio: false
generated: true
image: false
lang: en
layout: post
title: Repositories Cloned Successfully Summary
translated: false
type: note
---

Done. All 28 repos cloned, depth 1, HTTPS. Here's the summary:

```
================================================================
  28 NEW REPOS CLONED — ~/projects/ now has 331 repos total
================================================================

--- AI Agents & Coding ---
  claude-code           24M
  anthropic-cookbook    353M
  openai-cookbook        1.6G  ← large (notebooks/assets)
  langgraph             18M
  crewAI               365M
  AutoGPT               99M
  mem0                  48M

--- LLM Training & Research ---
  trl                   11M
  peft                  35M
  torchtitan            20M
  ao                    33M

--- LLM Inference & Serving ---
  text-generation-webui  56M
  llamafile             48M
  nexa-sdk              92M

--- Dev Tools & CLI ---
  lazygit               31M
  bat                   12M
  fd                   956K
  ripgrep              4.3M
  zoxide               880K
  ruff                 122M
  yazi                 7.8M
  glow                 1.3M
  delta                5.6M

--- AI Research ---
  minGPT               496K
  ng-video-lecture      1.6M

--- Vector DBs & RAG ---
  weaviate              61M
  llama_index          818M  ← large (many notebooks)
  langchain             58M

================================================================
  Total: 28 cloned, 0 skipped, 0 failed
  ~/projects/: 331 repos
================================================================

NOTE: openai-cookbook (1.6G) and llama_index (818M) are chunky
even at depth 1 — they have large assets/notebooks in-tree.
If disk is tight, these are the first to prune.
```

Pro tip: install `lazygit`, `zoxide`, `bat`, `fd`, and `delta` via brew — they're immediately useful CLI tools you'll use daily:

```
brew install lazygit zoxide bat fd ripgrep delta yazi glow
```
