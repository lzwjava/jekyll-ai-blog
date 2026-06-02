---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 多仓库Git更新脚本摘要
translated: true
type: note
---

命令执行成功——llama.cpp 只是一个较大的仓库，拉取需要一些时间。以下是摘要：

```
完成！以下是构建的内容：

修改的文件：
  ~/projects/ww/ww/git/git_update.py   — 重写为基于配置的仓库列表
  ~/projects/ww/ww/projects/repos.json — 8 个类别共 60 个仓库（新文件）
  ~/projects/ww/main.py                — 更新了帮助文本
  ~/.zsh/completions/_ww               — 更新了补全文本

命令：
  ww projects update              # 拉取全部 60 个仓库（默认）
  ww projects update --list       # 按类别显示仓库
  ww projects update @ai-agents   # 仅拉取某个类别
  ww projects update llama.cpp    # 拉取单个仓库
  ww projects update @ai-models pytorch  # 混合类别和名称

类别（共 60 个仓库）：
  ai-models      (13) — DeepSeek, Qwen, GPT-2, CLIP, Whisper, llama3, Kimi...
  ai-training    (14) — pytorch, Megatron-LM, nanoGPT, llm.c, bitsandbytes...
  ai-inference    (5) — llama.cpp, sglang, ktransformers, dinov2, nougat
  ai-apps         (7) — open-webui, dify, ComfyUI, stable-diffusion-webui...
  ai-agents       (4) — hermes-agent, codex, claw-code, gpt-researcher
  dev-tools       (8) — git, rust, jdk, react, vscode, terminal, alacritty, uv
  infra-network   (5) — openwrt, searxng, shadowsocks-rust, greptimedb, netty
  web-platforms   (4) — jekyll, kramdown, huggingface_hub, Telegram-iOS

定时任务：
  weekly-repo-update — 每周日 9:00 AM 运行（任务 ID: d3991577b9ca）
  下次运行：2026-06-07

编辑仓库：vim ~/projects/ww/ww/projects/repos.json
添加仓库：直接在任意类别下添加目录名即可
```

参考：
- [git_update.py](/Users/lzwjava/projects/ww/ww/git/git_update.py)
- [repos.json](/Users/lzwjava/projects/ww/ww/projects/repos.json)
