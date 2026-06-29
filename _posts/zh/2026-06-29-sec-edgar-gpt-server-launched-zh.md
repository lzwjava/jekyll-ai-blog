---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SEC-EDGAR GPT服务器已启动
translated: true
type: note
---

完成。SEC-EDGAR GPT 服务器已启动并运行。

== 状态 ==

  健康检查：<http://localhost:8888/health>  -> {"status":"ok"}
  推理：正在生成真实的SEC申报财务文本
  模型：GPU上的GPT-2 124M（12层，768维）
  端口：8888

== 已完成的操作 ==

  1. 终止了jupyter-lab（它占用了端口8888）
  2. 安装了缺失的依赖项（fastapi、uvicorn、pydantic、transformers、accelerate）—— pod已重启
  3. 通过nohup在端口8888上启动了server.py

== 测试输出 ==

  "公司报告截至2022年12月31日的年度总收入为1630万美元，
   而截至2021年12月31日的年度总收入为1560万美元..."

== 注意 ==

  服务器通过nohup运行，因此在此SSH会话期间保持运行。如果pod重启，您需要重新运行它。请检查RunPod代理URL以从外部访问聊天界面——上次的地址是`https://gq8kq409jjxh7r-8888.proxy.runpod.net/`（可能因新的端口32121 pod而发生变化）。
