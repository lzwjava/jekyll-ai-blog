---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 更新Llama服务配置
translated: true
type: note
---

以下是我们所做工作的总结：

**服务设置**

- 发现两个现有的 llama 服务：`llama-server.service`（正常运行）和 `llama.service`（损坏——路径中的 `P` 为大写导致持续崩溃循环）
- 更新了 `llama-server.service` 以匹配实际运行进程的配置，替代了过时的设置

**配置变更**

| | 变更前 | 变更后 |
|---|---|---|
| 模型 | DeepSeek-R1-0528-Qwen3-8B-Q4_K_M | gemma-4-E4B-it-Q5_K_M |
| 端口 | 11435 | 8081 |
| GPU 层数 | 99 | 43 |
| 上下文长度 | 8192 | 65536 |
| Flash 注意力 | — | 关闭 |

**注意事项**

- `llama.service` 目前仍处于**启用但损坏**状态——每次启动都会持续失败。建议修复路径或禁用该服务：`sudo systemctl disable llama.service`
- 服务仍处于**启用状态**，因此会在下次重启时自动启动——请在准备好时（或当服务器距离较远时！）记得手动启动它
- 停止服务后 GPU 使用量从约 5.7GB 下降至 **166MiB**，温度维持在 35°C 空闲状态
