---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模型上传的ECS访问选项
translated: true
type: note
---

我无法 SSH 到 `iZj6civepr8vf1085n7x0uZ`——这是一台阿里云 ECS，我没有它的 IP 或凭据。我需要访问它来分析模型内容。

两个选项：

1. 给我 IP（在那台机器上运行 `curl ifconfig.me`）+ 确认这里允许 root SSH 连接
2. 直接从该机器上传——我会给你需要执行的确切命令

对于选项 2，请以 root 身份在该 ECS 上运行以下命令：

```bash
# 安装 hf CLI
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv tool install huggingface-hub

# 登录（粘贴你的 HF token）
hf auth login

# 先在 HF 上创建仓库
hf repos create lzwjava/sec-edgar-gpt-124m-hf --type model

# 分析目录内容
ls -la ~/sec-edgar-gpt-124m-hf/
du -sh ~/sec-edgar-gpt-124m-hf/*
cat ~/sec-edgar-gpt-124m-hf/config.json 2>/dev/null

# 上传文件夹
hf upload lzwjava/sec-edgar-gpt-124m-hf ~/sec-edgar-gpt-124m-hf/
```

哪个选项适合你？
