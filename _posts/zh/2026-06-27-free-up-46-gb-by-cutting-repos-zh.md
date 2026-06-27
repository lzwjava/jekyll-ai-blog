---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过删除仓库释放46 GB
translated: true
type: note
---

~/projects 总计：144 GB  
repos.json 中的仓库：50 GB（170 个仓库）  
非 repos.json 仓库：22 GB  
lzwjava.github.io：72 GB（博客 + 笔记，不在 repos.json 中）

你的磁盘还剩 116 MB 空间，需要立即采取行动。

以下是我的建议：从 repos.json 中删除约 56 个仓库（170 个仓库中的约 1/3），按类别分组：

**操作系统内核 — 从 repos.json 移除，本地删除（节省 12.0 GB）**  
这些仅供参考，你可以随时重新克隆或在 GitHub 上浏览：  
- `linux`（7.4 GB）  
- `freebsd-src`（2.2 GB）  
- `wireguard-linux`（2.0 GB）  
- `xnu`（183 MB）

**大型工具链源码 — 移除，按需重新克隆（节省 6.4 GB）**  
你很少需要本地检出这些：  
- `jdk`（2.4 GB）— OpenJDK 源码  
- `vscode`（1.8 GB）— VS Code 源码  
- `rust`（1.4 GB）— Rust 编译器源码  
- `OpenROAD`（2.4 GB）— EDA 工具  
- `rocBLAS`（957 MB）— AMD GPU 库源码

**大型 AI 仓库（已包含模型权重或数据文件）（节省 13.3 GB）**  
- `Qwen2.5-Coder`（3.5 GB）— 仓库中很可能包含权重  
- `openai-cookbook`（1.7 GB）— 笔记本 + 数据文件  
- `evals`（1.6 GB）— OpenAI 评测及测试数据  
- `litellm`（1.3 GB）— 对 Python 库来说异常大  
- `claw-code`（1.2 GB）  
- `weaviate`（1.1 GB）  
- `TensorRT-LLM`（978 MB）— NVIDIA SDK，很少需要完整检出  
- `mlflow`（693 MB）

**未在积极使用的 AI 应用（节省 3.4 GB）**  
- `llama_index`（814 MB）  
- `LibreChat`（519 MB）  
- `open-webui`（495 MB）  
- `crewAI`（579 MB）  
- `AutoGPT`（258 MB）  
- `voice-changer`（244 MB）  
- `nexa-sdk`（229 MB）  
- `h2ogpt`（108 MB）  
- `quivr`（130 MB）  
- `llm-app`（88 MB）  
- `localGPT`（7 MB）  
- `anything-llm`（37 MB）

**AI 推理工具 — 重叠/重复工具（节省 1.2 GB）**  
你已有 llama.cpp、ollama、vllm、sglang、text-generation-webui、llamafile、ktransformers、TensorRT-LLM、ggml、mlx、mlx-examples。最多保留 3-4 个：  
- 移除：`ggml`（64 MB）、`mlx-examples`（108 MB）、`text-generation-webui`（56 MB）、`ktransformers`（167 MB）、`nexa-sdk`（229 MB）、`nougat`（8 MB）、`dinov2`（8 MB）

**未在积极使用的平台/基础设施（节省 1.1 GB）**  
- `greptimedb`（571 MB）  
- `Telegram-iOS`（595 MB）

**开发工具 — 操作系统/杂项项目，无需留在 repos.json 中（节省 4.6 GB）**  
- `bun`（581 MB）  
- `warp`（821 MB）  
- `fineract`（234 MB）  
- `netty`（163 MB）  
- `dubbo`（101 MB）  
- `desktop`（155 MB）— GitHub Desktop  
- `miu2d`（143 MB）  
- `verilator`（111 MB）  
- `tiny-gpu`（42 MB）  
- `vortex`（310 MB）  
- `ramulator2`（4 MB）  
- `openlane2`（23 MB）  
- `ChezScheme`（43 MB）  
- `terminal`（118 MB）— Windows Terminal

**总计：移除约 55 个仓库，释放约 46 GB**

这将使 repos.json 从 170 个仓库降至约 115 个，并释放足够空间让你喘口气。另外考虑以下两点：

1. **lzwjava.github.io 体积达 72 GB，是你最大的单项** — 它可能包含大型二进制资源。运行 `du -sh ~/projects/lzwjava.github.io/.git` 查看是否为 git 历史导致。如果是，重新克隆时使用 `git clone --depth 1` 可单独节省 50 GB 以上。

2. **非 repos.json 仓库（22 GB）** 包含例如 `gcc`（1.5 GB）、`open-liberty`（1.2 GB）、`true-question`（1.4 GB）、`WeFriends`（844 MB）等，其中许多看起来是旧项目，你也可以一并删除。

需要我生成精简后的 repos.json 以及对应的 `rm -rf` 删除命令吗？