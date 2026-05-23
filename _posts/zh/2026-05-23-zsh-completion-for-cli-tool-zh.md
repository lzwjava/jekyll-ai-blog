---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CLI工具的ZSH补全
translated: true
type: note
---

以下是完整总结：

构建内容：

1. 补全脚本：/Users/lzwjava/projects/ww/completions/_ww  
   - 476 行 zsh 补全代码  
   - 覆盖所有 33 个顶层命令组  
   - 覆盖每个组的子命令（github, git, macos, image, proc, utils, java, network, search, pdf, copilot, sync, read, llm, openrouter, env, display, degree, whisper, host, linux, cloudflare, ghostty, clash, latest, note, screenshot）  
   - 覆盖嵌套的子子命令（例如 sync bashrc back/forth, sync hermes back/forth）  
   - 覆盖标志（--no-push, --only-message, --json, --days, --model, --debug, --top-k, --pages, --dir, --type）  
   - 在适当位置覆盖文件补全（whisper → 音频文件, marp/pdf → .md 文件, read index → 目录）

2. 添加到 ww/main.py 的 CLI 命令：  
   - `ww completion install` — 将 _ww 复制到 ~/.zsh/completions/ 并打印设置说明  
   - `ww completion script` — 将补全脚本输出到标准输出  
   - 帮助文本更新，新增“Completion:”部分

3. Shell 配置：  
   - 在 ~/.zprofile 中添加 `fpath=(~/.zsh/completions $fpath)` 和 `autoload -Uz compinit && compinit`（第 70-72 行）  
   - 同时在 ~/.zshrc 中也存在（第 24-25 行），用于非 Ghostty 终端  
   - 实际生效的是 .zprofile — Ghostty 启动时会加载它

4. 修改的文件：  
   - ww/main.py — 添加补全处理程序 + 帮助文本  
   - completions/_ww — 新的 zsh 补全脚本  
   - ~/.zprofile — 添加 fpath + compinit

Git：已提交为 main 分支上的 1eed8fc，并推送到远端。

重启 Ghostty 后验证：
  ww <TAB>           → 显示所有 33 个命令组  
  ww github <TAB>    → 显示 info, repos, starred, followers, following, notifications, rate, gitmessageai  
  ww git <TAB>       → 显示 amend-push, classify, find-commit, delete-commit, diff-tree, ...  
  ww sync bashrc <TAB> → 显示 back, forth  
  ww clash <TAB>     → 显示 select-provider, speed, run, top-proxies, ...  
  ww github gitmessageai <TAB> → 显示 --no-push, --only-message, --allow-pull-push, --type