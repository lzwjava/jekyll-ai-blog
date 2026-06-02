---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Engineer's Workflow Analysis
translated: false
type: note
---

Here's the full analysis:

```
================================================================
                    REPO & USAGE AUDIT
================================================================

STATUS: All 117 repos from repos.json are ALREADY cloned locally.
Your ~/projects/ has 305 repos total — 117 tracked, 186 misc/personal.

================================================================
                    YOUR TOP TOOLS (shell history)
================================================================

  546  ww           ← your daily driver
   85  hermes
   46  git
   46  uv
   12  tmux
    6  zed
    6  ssh
    3  codex

  Top ww subcommands:
  414  ww note       ← note-taking is your #1 workflow
   45  ww git
   20  ww projects
   16  ww amd-dev-cloud
    9  ww hf
    9  ww github

================================================================
                    YOUR DOCK APPS
================================================================

  WeChat, Safari, Telegram, Discord, Microsoft To Do,
  Ghostty, Alacritty, Warp, Zed, GitHub Desktop,
  System Settings, Passwords, Clock

================================================================
                    OBSERVATIONS
================================================================

1. You're deep in AI engineering (agents, training, inference, models)
2. Note-taking is your #1 daily activity (414 ww note calls)
3. You use 3 terminals: Ghostty, Alacritty, Warp
4. You do GPU work (amd-dev-cloud, ROCm)
5. You care about AI agents (hermes, codex, claw-code, opencode)
```

Based on your usage patterns, here are repos you're **missing** that would fit your workflow:

```
================================================================
              RECOMMENDED NEW REPOS TO CLONE
================================================================

--- AI Agents & Coding (your biggest interest) ---
  anthropics/claude-code        # Claude Code CLI — you use codex already
  anthropics/anthropic-cookbook  # Official Anthropic recipes/notebooks
  openai/openai-cookbook         # OpenAI recipes — practical LLM patterns
  langchain-ai/langgraph        # Agent graph framework — industry standard
  crewAIInc/crewAI              # Multi-agent orchestration
  Significant-Gravitas/AutoGPT  # Pioneering autonomous agent
  mem0ai/mem0                   # Long-term memory for AI agents

--- LLM Training & Research (you train on H200/RTX 4070) ---
  huggingface/trl               # SFT/DPO/GRPO — you have fine-tuning skill
  huggingface/peft              # LoRA/QLoRA — already in peft-fine-tuning skill
  vllm-project/vllm             # Already cloned but HIGH PRIORITY for you
  NVIDIA/Megatron-LM            # Already cloned ✓
  pytorch/torchtitan            # PyTorch native distributed training
  pytorch/ao                    # PyTorch architecture optimization (quantization)
  state-spaces/mamba            # Already cloned ✓

--- LLM Inference & Serving ---
  ggml-org/llama.cpp            # Already cloned ✓
  oobabooga/text-generation-webui  # Popular local LLM webui
  Mozilla-Ocho/llamafile        # Single-file LLM binaries — very portable
  NexaAI/nexa-sdk               # Local model serving

--- Developer Tools & CLI (you live in terminal) ---
  jesseduffield/lazygit         # TUI for git — you use git 46x
  sharkdp/bat                   # Better cat with syntax highlighting
  sharkdp/fd                    # Better find
  BurntSushi/ripgrep            # Better grep (you already use via hermes)
  ajeetdsouza/zoxide            # Smarter cd (you cd 107x)
  astral-sh/ruff                # Python linter (already in your pyproject.toml)
  sxyazi/yazi                   # Terminal file manager
  charmbracelet/glow            # Markdown renderer in terminal
  dandavison/delta              # Better git diff

--- AI Research Papers & Notebooks ---
  karpathy/minGPT               # Minimal GPT implementation (Karpathy)
  karpathy/ng-video-lecture     # Companion code for Karpathy's lectures
  microsoft/autogen             # Already cloned ✓
  deepseek-ai/DeepSeek-V3      # Already cloned ✓

--- Vector DBs & RAG (you have read/ RAG module) ---
  chroma-core/chroma            # Already cloned ✓
  qdrant/qdrant                 # Already cloned ✓
  weaviate/weaviate             # Popular vector DB — missing
  run-llama/llama_index         # RAG framework — missing
  langchain-ai/langchain        # LLM framework — missing (despite langchain-test dir)

--- Monitoring & Observability ---
  langfuse/langfuse             # Already cloned ✓
  BerriAI/litellm               # Already cloned ✓
```

Top 10 I'd clone first (highest signal for your workflow):

```
  1. langchain-ai/langgraph       — agent graphs, industry standard
  2. jesseduffield/lazygit        — you use git constantly
  3. ajeetdsouza/zoxide           — smarter cd (you cd 107x)
  4. anthropics/claude-code       — you already use codex
  5. huggingface/trl              — GRPO/DPO fine-tuning
  6. run-llama/llama_index        — RAG framework
  7. pytorch/torchtitan           — distributed training
  8. Mozilla-Ocho/llamafile       — portable LLM binaries
  9. karpathy/minGPT              — Karpathy-style minimal impl
 10. crewAIInc/crewAI            — multi-agent framework

Want me to clone any of these? Just say which ones (or "clone all top 10").
```
