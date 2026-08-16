---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mini-SGLang 已部署并正常运行
translated: true
type: note
---

完成 — Mini-SGLang 已启动并通过验证。✅

## 发生了什么

首次启动尝试看似卡住，实际原因是**模型下载缺失**，而非代码问题：

1. **根本原因**：`Qwen/Qwen3-0.6B` 仅部分缓存（8月3日的分词器/配置文件，但1.5GB的权重文件从未完成下载——仅存一次失败尝试留下的16MB碎片）。
2. 服务器在 HuggingFace 的 **Xet 下载后端** 受阻，在 Clash 代理下，下载进度卡在87.6%（约1.31/1.5GB）。
3. **解决方案**：我终止了卡住的进程，并设置 `HF_HUB_DISABLE_XET=1` 后重新启动——此时后台下载已完成，新启动的进程直接从缓存加载权重（无需重新下载）。

## 当前状态

| 项目 | 值 |
| --- | --- |
| 服务器 | `http://localhost:1919`（兼容 OpenAI 接口） |
| 模型 | `Qwen/Qwen3-0.6B`（bf16） |
| 进程 | PID 1668187，日志位于 `/tmp/minisgl.log` |
| KV 缓存 | 73,288 tokens（约7.8 GiB），可用0.84 GiB |
| 验证结果 | `/v1/models` 和 `/v1/chat/completions` 均正常响应 |

该模型甚至能在测试提示中运行其 Qwen3 思考模式。请注意，GPU 当前显示**已使用11.3 GiB**（12GB显卡）——此模型尚可容纳，但类似 Qwen3-4B 会显得紧张；Qwen2.5-3B-Instruct（也已缓存）则是更宽裕的选择。

日后可用的命令：

```bash
curl http://localhost:1919/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen3-0.6B","messages":[{"role":"user","content":"hi"}]}'
```

一个小建议：如果再次启动，请在环境变量中保留 `HF_HUB_DISABLE_XET=1`，以避免不可靠的 Xet 后端。需要我尝试其他模型、运行基准测试，还是配置客户端脚本？
