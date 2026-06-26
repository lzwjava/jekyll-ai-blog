---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复GPT-2模型退化输出
translated: true
type: note
---

## 综合摘要

### 问题描述

RunPod 上的 SEC-EDGAR GPT-2 124M 模型产生了**退化输出**——无论采用何种服务方式、采样策略或提示，都会出现重复循环，例如 "ivableivable..."。这是一个**模型质量问题**，而非服务缺陷。

### 根本原因分析

存在**两个独立的问题**叠加在一起：

**1. RunPod 上的旧模型**（`/workspace/model/hf-model/`，vocab_size=50304）：

- 已正确转换为 HF 格式（权重形状正确为 `[768, 2304]`，所有偏置均存在）
- 但来自 nanoGPT 的 **填充词表**：`vocab_size=50304`（50257 个真实词 + 47 个填充至最近的 64）
- server.py 中有一个运行时补丁，将嵌入层从 50304 裁剪为 50257
- **该模型产生了退化输出**——裁剪补丁只是权宜之计，底层训练权重可能已损坏或来自错误检查点

**2. 来自 HF 的新模型**（`lzwjava/sec-edgar-gpt-124m-hf`）：

- 具有 `vocab_size=50257`（正确，无填充）——这是修复方案
- 但 **safetensors 文件直接从 nanoGPT 保存，未进行正确转换**：
  - 线性权重形状**转置**：`[2304, 768]` 而非 `[768, 2304]`
  - **所有偏置缺失**（ln_1, ln_2, c_attn, c_proj, c_fc, c_proj）
- RunPod 上的 transformers 5.5.0 拒绝加载，提示 `RuntimeError: shape mismatch`

### 已完成的工作

1. **更新了本地 server.py**——移除了 18 行的嵌入裁剪补丁，简化为直接加载
2. **备份了 RunPod 上的旧模型** → `hf-model-old/`
3. **从 HF 下载了新模型到 RunPod** → `hf-model/`（7 个文件，650MB safetensors）
4. **服务器崩溃**——transformers 因权重形状不匹配而拒绝加载
5. **编写了转换脚本**（`scripts/convert_nanogpt_to_hf.py`），该脚本：
   - 将线性权重从 `[out, in]` 转置为 `[in, out]`
   - 为所有缺失参数添加零偏置
   - 保存包含 transformers 元数据的正确 config.json
   - 复制 tokenizer 文件

### 仍需完成的工作

1. **在 RunPod 上运行转换脚本**，生成 `hf-model-converted/`
2. **将 `hf-model/` 替换为转换后的版本**
3. **使用新模型重启服务器**
4. **测试生成效果**——验证不再出现退化循环
5. **（可选）** 将修正后的模型重新上传至 HF，使其格式正确，方便他人使用

### 关键架构说明

| 组件 | 详情 |
|-----------|---------|
| RunPod GPU | RTX 2000 Ada 16GB（EU-RO-1） |
| 服务器 | FastAPI + transformers，端口 8888 |
| Nginx | 8081→8888 反向代理 |
| 模型 | GPT-2 124M，12 层，768 维，12 头，1024 上下文 |
| 词表 | 50257（标准 GPT-2，无填充） |
| API | 兼容 OpenAI 的 `/v1/completions` 和 `/v1/chat/completions` |

需要我在 RunPod 上运行转换并启动服务器吗？
