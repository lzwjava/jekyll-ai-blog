---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gemma 4 E4B 模型已验证并准备就绪
translated: true
type: note
---

成功了！以下是完整验证：

**模型加载并生成文本**："I am a language model, trained by Google."

**架构**：Gemma 4 E4B (7.52B 参数, Q3_K 量化, 3.76 GiB 文件)

**Gemma 4 E4B 关键规格（来自 GGUF 元数据）**：

- 42 层, 2560 嵌入维度, 10240 前馈维度
- 8 注意力头, 2 KV 头 (GQA=4)
- 131K 上下文长度（全局注意力 + 滑动窗口注意力，窗口大小 512）
- BPE 分词器, 262k 词汇量
- 共享 KV 层（18 层共享 — Gemma 4 的层绑定 KV 设计）
- 层输入权重（«per_layer_token_embd», 逐层输入门控/投影 — Gemma 4 的 "Gated Delta Net" 架构）

**在 RTX 4070 12GB 上的性能**：

- 提示评估：291 t/s
- 生成：91 t/s
- 显存使用：2343 MiB 模型 + 14 MiB KV + 开销 → 总计约 3.2 GiB，空间充裕

文件位于 `/mnt/data/models/gemma-4-E4B-it-Q3_K_M.gguf`，已准备就绪。要我启动 `llama-server` 以便你与它聊天，或者在 Hermes 中配置它吗？
