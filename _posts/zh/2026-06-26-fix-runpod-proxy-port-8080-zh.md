---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 RunPod 代理端口 8080
translated: true
type: note
---

代理无法连接到服务器——日志中没有出现代理请求（仅有 localhost）。需要在 RunPod 的 Pod 设置中开放端口 8080。

**修复方法：** 在 RunPod 仪表盘 → 你的 Pod → 设置 → 编辑 "Exposed HTTP Ports" → 添加 `8080` → 保存。之后代理 URL 即可正常工作。

**快速替代方案**——从你的 Mac 使用 SSH 隧道：

```bash
ssh -p 28484 -i ~/.ssh/id_ed25519 -L 8080:localhost:8080 root@213.173.110.200 -N
```

然后在浏览器中访问 `http://localhost:8080/health`。