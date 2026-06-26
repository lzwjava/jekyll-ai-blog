---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 访问RunPod端口8080
translated: true
type: note
---

服务器在 8080 端口运行。你看到的 502 错误是因为 RunPod 不直接通过 IP 暴露端口——你需要使用 RunPod 代理 URL。

RunPod 代理 URL 格式通常为：

```
https://<pod-id>-8080.proxy.runpod.net
```

你可以在 RunPod 仪表盘的 pod "Connect" 标签页 → HTTP ports 中找到它。在那里查找暴露的 8080 端口 URL。

或者，通过 SSH 隧道从你的 Mac 本地访问：

```
ssh -p 28484 -i ~/.ssh/id_ed25519 -L 8080:localhost:8080 root@213.173.110.200 -N
```

然后在浏览器中打开 `http://localhost:8080/v1/models`。你还需要在 RunPod pod 设置中暴露 8080 端口（如果尚未设置为 HTTP 端口）。
