---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Qwen2.5-7B 在远程服务器上运行
translated: true
type: note
---

✅ **完成！** Qwen2.5-7B 模型现在正在远程服务器 `lzw@192.168.1.34` 上运行。

以下是所完成操作的摘要：

| 步骤 | 操作 |
|------|--------|
| 🔍 | 在 `192.168.1.34` 上识别到正在运行的 `llama-server.service`（临时），使用 **Qwen3.8-27B-UD-IQ1_M.gguf**（6.3G） |
| ⏹️ | 通过 `systemctl --user kill llama-server.service` 停止了旧服务 |
| ✅ | 验证了 `Qwen2.5-7B-Instruct-Q4_K_M.gguf`（4.4G）**已经存在** 于模型目录中 |
| ▶️ | 启动了新服务：`systemd-run --user --unit=llama-server /home/lzw/projects/llama-b11344/llama-server -m .../Qwen2.5-7B-Instruct-Q4_K_M.gguf --port 8080 --host 0.0.0.0 -ngl 99 -c 4096` |
| 🧪 | **测试** — API 响应正确：`{"choices":[{"finish_reason":"stop","index":0,"message":{"role":"assistant","content":"Hello!"}}]}` |

**正在运行的模型**：`Qwen2.5-7B-Instruct-Q4_K_M.gguf` 位于端口 **8080**，所有 99 层都已卸载到 GPU，上下文大小为 4096。推理速度很快：提示处理约 11 t/s，文本生成约 19.8 t/s。