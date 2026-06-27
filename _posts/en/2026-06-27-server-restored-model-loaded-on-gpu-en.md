---
audio: false
generated: true
image: false
lang: en
layout: post
title: Server Restored, Model Loaded on GPU
translated: false
type: note
---

Done. Everything is back up. Here's the summary:

== RESTORED ==

  - Killed jupyter-lab that was hogging port 8888
  - Installed missing deps (fastapi, uvicorn, pydantic, transformers)
  - Started server.py on port 8888 (PID 1045)
  - Model loaded on GPU, inference working

== STATUS ==

  Health:  https://gq8kq409jjxh7r-8888.proxy.runpod.net/health  -> ok
  Chat UI: https://gq8kq409jjxh7r-8888.proxy.runpod.net/        -> SEC EDGAR GPT-124M Chat
  Inference test: returns SEC filing text (not great quality, but model is working)

== NOTE ==

  The server runs via nohup so it survives SSH disconnects, but if the pod restarts again you'll need to re-run it. To make it persistent across restarts, you'd want a startup script or screen/tmux session.
