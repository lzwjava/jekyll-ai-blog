---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Pod重启后的端口冲突
translated: true
type: note
---

== 诊断 ==

Pod 在约 3 分钟前**重启**（运行时间：3 分钟）。重启后：

1. **端口冲突**：RunPod 默认的 jupyter-lab 重新占用了端口 8888
   - jupyter-lab（PID 129）正在监听 0.0.0.0:8888
   - RunPod 代理 URL（gq8kq409jjxh7r-8888）直接映射到端口 8888
   - 所以现在你访问的是 jupyter-lab，而不是聊天应用

2. **server.py 未运行**：FastAPI 聊天服务器在重启时被终止，且未重新启动

3. **GPU 空闲**：RTX 2000 Ada，0 个进程，已用 2MiB VRAM

4. **模型文件完好**：/workspace/model/hf-model/ 包含 model.safetensors（652MB）、tokenizer、config —— 一切正常

== 操作建议 ==

两个选项：

选项 A（快速 —— 杀掉 jupyter-lab，使用端口 8888）：

- 杀掉 jupyter-lab
- 在端口 8888 上启动 server.py
- 代理 URL 立即生效
- 缺点：丢失 jupyter-lab

选项 B（两者保留 —— 使用 nginx 端口 8081）：

- 在端口 8080（或任意空闲端口）上启动 server.py
- 添加 nginx 路由：8081 → localhost:8080
- 使用 RunPod 代理：gq8kq409jjxh7r-8081
- 缺点：URL 不同

选项 C（最佳 —— 重新分配端口）：

- 将 jupyter-lab 移至 8889 或停止它
- 在 8888 上运行 server.py
- 使用与之前相同的代理 URL

你选择哪个选项？我可以现在 SSH 进去修复。
