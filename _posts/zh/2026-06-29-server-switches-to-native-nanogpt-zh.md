---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 服务器切换到原生nanoGPT
translated: true
type: note
---

完成。服务器现在使用原生 nanoGPT 模型 — 与工作站的 sample.py 完全相同。

== 变化内容 ==

  server.py 现在通过 nanoGPT 的原生 GPT 类（model.py）加载 ckpt.pt，
  而不是使用转换后的 HF transformers 模型。编码使用 tiktoken。

  RunPod 上的文件（/workspace/model/）：
    ckpt.pt          1.4GB  — 原始 nanoGPT 检查点（47k 步）
    model.py         8.6KB  — nanoGPT 模型定义
    server.py        4.6KB  — 重写，无 transformers 依赖
    hf-model/        622MB  — 旧 HF 模型（作为备份保留）

== 对比（相同提示：“The Company reported total revenue of”） ==

  之前（transformers + top_p）：
    “Our principal business is our principal executive office in San Francisco,
     California and is located in The San Francisco, California...”

  之后（原生 nanoGPT + top_k=200）：
    “$2.0 million during the year ended December 31, 2016, the Company
     recognized non-cash impairment charges of $0.1 million... bad debt
     expense. See Note 9 for further details.”

  工作站 sample.py（参考）：
    “$167.0 million for the year ended December 31, 2023... The following
     table shows the Company's net revenue by geographic location...”

  两者现在都能生成带有财务数据的合规 SEC 文件语言。

== 状态 ==

  Health:    <http://localhost:8888/health> -> ok
  Server:    原生 nanoGPT, top_k=200, temp=0.8
  Model:     124M 参数, vocab 50304, bias=False
  Checkpoint: 47k 步（验证损失 2.2778）
  无 transformers 依赖 — 仅使用 torch + tiktoken + fastapi
