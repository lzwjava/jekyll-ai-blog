---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 上传大模型文件选项
translated: true
type: note
---

已上传 ✓  
  config.json (831B)  
  generation_config.json (202B)  
  tokenizer_config.json (286B)  
  tokenizer.json (3.4MB)  
  README.md (2.1KB)  
  .gitattributes (50B)  

尚待处理 — 请自行上传：  
  model.safetensors (475MB)  

你的仓库：<https://huggingface.co/lzwjava/sec-edgar-gpt-124m>  

对于 `model.safetensors`，选择最快的路径：  

```
# 选项 1: hf-mirror.com（中国优化）
HF_ENDPOINT=https://hf-mirror.com hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors

# 选项 2: 通过 DMIT 代理
https_proxy=http://127.0.0.1:<port> hf upload lzwjava/sec-edgar-gpt-124m model.safetensors model.safetensors

# 选项 3: 上传到 AMD Dev Cloud，再从那里上传
scp model.safetensors amd-cloud:~/
ssh amd-cloud 'hf upload lzwjava/sec-edgar-gpt-124m ~/model.safetensors model.safetensors'
```
