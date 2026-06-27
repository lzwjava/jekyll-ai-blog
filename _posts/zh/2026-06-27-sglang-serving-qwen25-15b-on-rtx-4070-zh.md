---
audio: false
generated: true
image: false
lang: zh
layout: post
title: sglang 在 RTX 4070 上服务于 Qwen2.5-1.5B
translated: true
type: note
---

完成。sglang已在RTX 4070上成功运行并提供Qwen2.5-1.5B-Instruct服务。

以下是摘要：

已搭建内容：
  新虚拟环境：~/sglang-env
  torch: 2.7.1+cu126 (CUDA 12.6 运行时)
  triton: 3.3.1（非段错误的3.5/3.6版本）
  sglang: 0.4.10.post2
  sgl-kernel: 0.2.8
  flashinfer: 0.2.9rc2

关键细节：

- 驱动程序580.x向后兼容cu126（无需更改驱动程序）
- cu124的wheel最大支持torch 2.6.0，但sglang 0.4.x硬性固定torch==2.7.1
- 改用cu126的wheel——相同的驱动程序兼容性，torch 2.7.1可用
- triton 3.3.1（随torch 2.7.1捆绑）在Ada/sm_89上不会段错误
- CUDA图形捕获在0.52秒内完成——无崩溃
- 服务器在<http://0.0.0.0:30000响应，提供兼容OpenAI的API>

启动脚本：/tmp/start-sglang.sh
  设置代理（127.0.0.1:7890）和PATH，然后在端口30000运行sglang

后续重启命令：
  ssh lzw@192.168.1.36 "nohup /tmp/start-sglang.sh > /tmp/sglang-server.log 2>&1 &"
