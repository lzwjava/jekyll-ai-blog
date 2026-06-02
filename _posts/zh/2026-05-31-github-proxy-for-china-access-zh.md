---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub 中国访问代理
translated: true
type: note
---

**问题：** `https://ghfast.top` 是什么？

**回答：**

这是一个 **GitHub 代理/加速服务**（`GitHub 代理加速`）—— 一种镜像/CDN 服务，用于加速中国大陆用户下载 GitHub 资源（因 GFW 导致速度缓慢或受限）。

它代理以下内容：

- GitHub 文件下载（仓库、发布版、原始文件）
- `github.com` 的发布版资源
- `raw.githubusercontent.com` 内容
- GitHub Gist 文件
- 压缩包下载（`.tar.gz`、`.zip`）

**工作原理：**
在任意 GitHub URL 前加上代理 URL 即可：

```bash
# 直连（在中国大陆速度较慢）
https://github.com/owner/repo/releases/download/v1.0/binary.tar.gz

# 通过 ghfast.top 代理
https://ghfast.top/https://github.com/owner/repo/releases/download/v1.0/binary.tar.gz
```

或者用于 `raw.githubusercontent.com`：

```bash
https://ghfast.top/https://raw.githubusercontent.com/owner/repo/main/file.txt
```

**对你的典型用途：**
如果你在广州的机器（或 Ubuntu 工作站）上使用 `pip install` 或 `wget` 下载 GitHub 托管的模型权重、二进制文件或脚本，且速度极慢——这个代理可以解封。类似的服务还有 `ghproxy.com`、`mirror.ghproxy.com` 等，它们会随 GFW 的调整而出现或消失。

**可信度提示：** 这些是个人运营的第三方代理。不要在不验证校验和的情况下通过它们传输不受信任的二进制文件——务必对每个文件执行 `sha256sum` 校验。
