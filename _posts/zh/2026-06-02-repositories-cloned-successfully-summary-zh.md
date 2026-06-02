---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 仓库克隆成功摘要
translated: true
type: note
---

完成。所有28个仓库已克隆，深度为1，采用HTTPS协议。摘要如下：

```
================================================================
  已克隆28个新仓库 — ~/projects/ 现在共有331个仓库
================================================================

--- AI Agents & Coding ---
  claude-code           24M
  anthropic-cookbook    353M
  openai-cookbook        1.6G  ← 较大（notebooks/assets）
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
  llama_index          818M  ← 较大（多个notebooks）
  langchain             58M

================================================================
  总计：28个已克隆，0个跳过，0个失败
  ~/projects/：331个仓库
================================================================

注意：openai-cookbook（1.6G）和llama_index（818M）即使在深度1下也很大——它们目录内包含大量assets/notebooks。
如果磁盘空间紧张，这些是首先可以考虑清理的。
```

小贴士：通过brew安装`lazygit`、`zoxide`、`bat`、`fd`和`delta`——它们是立即能用的CLI工具，你会每天用到：

```
brew install lazygit zoxide bat fd ripgrep delta yazi glow
```