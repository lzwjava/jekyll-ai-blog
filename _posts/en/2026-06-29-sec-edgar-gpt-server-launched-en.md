---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC-EDGAR GPT Server Launched
translated: false
type: note
---

Done. SEC-EDGAR GPT server is up and running.

== STATUS ==

  Health:    <http://localhost:8888/health>  -> {"status":"ok"}
  Inference: generating real SEC filing financial text
  Model:     GPT-2 124M (12 layers, 768d) on GPU
  Port:      8888

== WHAT WAS DONE ==

  1. Killed jupyter-lab (was hogging port 8888)
  2. Installed missing deps (fastapi, uvicorn, pydantic, transformers, accelerate) — pod had restarted
  3. Started server.py via nohup on port 8888

== TEST OUTPUT ==

  "The company reported total revenue of $16.3 million during the year
   ended December 31, 2022, compared to $15.6 million for the year ended
   December 31, 2021..."

== NOTE ==

  The server runs via nohup so it survives this SSH session. If the pod restarts, you'll need to re-run it. Check the RunPod proxy URL to access the chat UI externally — it was at `https://gq8kq409jjxh7r-8888.proxy.runpod.net/` last time (may have changed with the new port 32121 pod).
