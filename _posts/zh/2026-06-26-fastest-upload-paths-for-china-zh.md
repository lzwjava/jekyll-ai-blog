---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中国最快上传路径
translated: true
type: note
---

以下是情况说明和选项：

**模型：** 475MB model.safetensors + 3.4MB tokenizer = 约478MB 总计。目标：`lzwjava/sec-edgar-gpt-124m` 在 HuggingFace 上。

**从中国访问慢的原因：** HuggingFace CDN（Cloudflare）被部分中国 ISP 限速/屏蔽。上传过程中会中断。GCS 到 HF 的直接传输也需要快速的美国-欧洲连接。

**排序后的选项（从最优到最差）：**

**选项 1：AMD 开发云（亚特兰大）作为中继 — 最快**
你有 `ssh amd-cloud`（亚特兰大的 MI300X）。美国到 HuggingFace 很快。两个子选项：

  a) 从 Mac 使用 rsync 传输文件到 AMD，然后从 AMD 上传到 HF
  b) 在 AMD 上从 GCS 下载，然后上传到 HF

**选项 2：hf-mirror.com — 对中国友好**
HuggingFace 的官方中国镜像。`huggingface-cli` 可以配置使用它。

**选项 3：你的 DMIT 代理（洛杉矶）**
通过 hysteria2/DMIT 代理（经洛杉矶）路由 `huggingface-cli upload`。位于美国的代理应该对 HF 很快。

让我先尝试最快的方式：直接使用你已有的 DMIT 代理从 Mac 上传。
