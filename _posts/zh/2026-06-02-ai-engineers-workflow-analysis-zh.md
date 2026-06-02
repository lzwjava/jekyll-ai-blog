---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI工程师工作流程分析
translated: true
type: note
---

```
================================================================
                    仓库与使用审计
================================================================

状态：repos.json 中的全部 117 个仓库已在本地克隆。
你的 ~/projects/ 中共有 305 个仓库——117 个被跟踪，186 个为杂项/个人。

================================================================
                    你的常用工具（shell 历史）
================================================================

  546  ww           ← 你的日常驱动
   85  hermes
   46  git
   46  uv
   12  tmux
    6  zed
    6  ssh
    3  codex

  常用 ww 子命令：
  414  ww note       ← 记笔记是 #1 工作流
   45  ww git
   20  ww projects
   16  ww amd-dev-cloud
    9  ww hf
    9  ww github

================================================================
                    你的 Docker 应用
================================================================

  WeChat, Safari, Telegram, Discord, Microsoft To Do,
  Ghostty, Alacritty, Warp, Zed, GitHub Desktop,
  系统设置, 密码, 时钟

================================================================
                    观察
================================================================

1. 你深耕 AI 工程（智能体、训练、推理、模型）
2. 记笔记是你每日最主要的活动（414 次 ww note 调用）
3. 你使用 3 个终端：Ghostty、Alacritty、Warp
4. 你做 GPU 相关的工作（amd-dev-cloud、ROCm）
5. 你关注 AI 智能体（hermes、codex、claw-code、opencode）

基于你的使用模式，以下是你**缺失**但适合你工作流的仓库：

```
================================================================
              推荐克隆的新仓库
================================================================

--- AI 智能体与编码（你最大的兴趣）---
  anthropics/claude-code        # Claude Code CLI——你已在用 codex
  anthropics/anthropic-cookbook  # Anthropic 官方配方/笔记本
  openai/openai-cookbook         # OpenAI 配方——实用的 LLM 模式
  langchain-ai/langgraph        # 智能体图框架——行业标准
  crewAIInc/crewAI              # 多智能体编排
  Significant-Gravitas/AutoGPT  # 开创性的自主智能体
  mem0ai/mem0                   # AI 智能体的长期记忆

--- LLM 训练与研究（你在 H200/RTX 4070 上训练）---
  huggingface/trl               # SFT/DPO/GRPO——你具备微调技能
  huggingface/peft              # LoRA/QLoRA——已在 peft-fine-tuning 技能中
  vllm-project/vllm             # 已克隆，但对你是高优先级
  NVIDIA/Megatron-LM            # 已克隆 ✓
  pytorch/torchtitan            # PyTorch 原生分布式训练
  pytorch/ao                    # PyTorch 架构优化（量化）
  state-spaces/mamba            # 已克隆 ✓

--- LLM 推理与服务 ---
  ggml-org/llama.cpp            # 已克隆 ✓
  oobabooga/text-generation-webui  # 流行的本地 LLM WebUI
  Mozilla-Ocho/llamafile        # 单文件 LLM 二进制——非常便携
  NexaAI/nexa-sdk               # 本地模型服务

--- 开发者工具与 CLI（你整天使用终端）---
  jesseduffield/lazygit         # Git 的 TUI——你使用 git 46 次
  sharkdp/bat                   # 更好的 cat，带语法高亮
  sharkdp/fd                    # 更好的 find
  BurntSushi/ripgrep            # 更好的 grep（你已通过 hermes 使用）
  ajeetdsouza/zoxide            # 更智能的 cd（你 cd 了 107 次）
  astral-sh/ruff                # Python 检查器（已在你的 pyproject.toml 中）
  sxyazi/yazi                   # 终端文件管理器
  charmbracelet/glow            # 终端 Markdown 渲染器
  dandavison/delta              # 更好的 git diff

--- AI 研究论文与笔记本 ---
  karpathy/minGPT               # 最小 GPT 实现（Karpathy）
  karpathy/ng-video-lecture     # Karpathy 讲座的配套代码
  microsoft/autogen             # 已克隆 ✓
  deepseek-ai/DeepSeek-V3      # 已克隆 ✓

--- 向量数据库与 RAG（你有 read/ RAG 模块）---
  chroma-core/chroma            # 已克隆 ✓
  qdrant/qdrant                 # 已克隆 ✓
  weaviate/weaviate             # 流行的向量数据库——缺失
  run-llama/llama_index         # RAG 框架——缺失
  langchain-ai/langchain        # LLM 框架——缺失（尽管有 langchain-test 目录）

--- 监控与可观测性 ---
  langfuse/langfuse             # 已克隆 ✓
  BerriAI/litellm               # 已克隆 ✓
```

我会优先克隆的前 10 个（对你工作流信号最强）：

```
  1. langchain-ai/langgraph       — 智能体图，行业标准
  2. jesseduffield/lazygit        — 你频繁使用 git
  3. ajeetdsouza/zoxide           — 更智能的 cd（你 cd 了 107 次）
  4. anthropics/claude-code       — 你已在用 codex
  5. huggingface/trl              — GRPO/DPO 微调
  6. run-llama/llama_index        — RAG 框架
  7. pytorch/torchtitan           — 分布式训练
  8. Mozilla-Ocho/llamafile       — 便携 LLM 二进制
  9. karpathy/minGPT              — Karpathy 风格的最小实现
 10. crewAIInc/crewAI            — 多智能体框架

需要我克隆其中任何一个吗？请告知（或说“克隆全部前 10 个”）。
```