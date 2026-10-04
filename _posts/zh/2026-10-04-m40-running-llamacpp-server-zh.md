---
audio: false
generated: true
image: false
lang: zh
layout: post
title: M40 运行 llama.cpp 服务器
translated: true
type: note
---

完成 — llama.cpp 已克隆、构建（通过预构建的 CUDA 12.8 二进制文件），并**作为实时服务器在 M40 上运行**。🎉

## 运行情况

**llama-server** 已在 `http://192.168.1.34:8080` 上启动（OpenAI 兼容 API），提供 **Qwen2.5-1.5B-Instruct (Q4_K_M)** 模型，完全卸载到 Tesla M40。

已验证端到端连接：

```
POST /v1/chat/completions
→ "A GPU, or Graphics Processing Unit, is a specialized electronic circuit
   designed to rapidly manipulate and alter memory to accelerate the creation
   of images in a frame buffer intended for output to a display."
```

| 指标 | 值 |
| -------- | ------- |
| 健康状态 | `{"status":"ok"}` |
| GPU 利用率 | 96% (峰值) |
| 功耗 | 174 W (空闲 16 W) |
| VRAM 使用量 | ~2.1 GB / 11.4 GB |
| 提示处理 | ~219 t/s |
| 生成 | ~88 t/s |
| 上下文窗口 | 32,768 |

## 文件位置

- 仓库：`~/projects/llama.cpp`
- 二进制文件：`~/projects/llama-b11344/`（CUDA 12.8 预构建 + 捆绑的 libcudart/libcublas）
- 模型：`~/models/qwen2.5-1.5b-instruct-q4_k_m.gguf`（1.04 GB）
- 服务器进程：PID 7946，日志位于 `~/server.log`

## 从局域网内任意机器使用

```bash
curl http://192.168.1.34:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello!"}],"max_tokens":100}'
```

或使用 OpenAI SDK：`base_url="http://192.168.1.34:8080/v1"`.

## 备注

- 我故意使用了 **CUDA 12.8** 构建——CUDA 13.4 构建放弃了对 Maxwell（sm_52）的支持。这些内核可以正常 JIT 编译到 sm_52。
- 这台 M40 大约可以舒适地运行 1.5B 模型；7B Q4（~4.4GB）可以放入 VRAM，但生成速度会降至 ~15–20 t/s，因为 M40 的 FP16 路径较旧且带宽为 288 GB/s。
- 稍后重启：`cd ~/projects/llama-b11344 && LD_LIBRARY_PATH=$PWD nohup ./llama-server -m ~/models/qwen2.5-1.5b-instruct-q4_k_m.gguf --host 0.0.0.0 --port 8080 -ngl 99 </dev/null > ~/server.log 2>&1 &`
- 要我尝试更大的模型（如 Qwen2.5-3B 或 Llama-3.2-3B）来看看 M40 能走多远吗？
