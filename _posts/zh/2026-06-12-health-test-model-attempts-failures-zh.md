---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 健康测试模型尝试失败
translated: true
type: note
---

以下是三次尝试的情况：

## 健康测试总结

### 尝试1：`unsloth/Qwen3-8B`（4位量化，7.5GB）

- **状态**：已终止 —— 下载速度过慢
- **问题**：HuggingFace下载速度约300KB/s，下载7.5GB需要约7小时
- hf-mirror.com稍快（约470KB/s），但仍需约4.5小时

### 尝试2：`Qwen/Qwen3.5-9B`（已缓存，18GB）

- **状态**：失败 —— 模型类型错误
- **问题**：Qwen3.5-9B是**视觉语言模型**（Qwen3VLProcessor），而非纯文本模型。Unsloth成功加载，但VL处理器中不存在`tokenizer.vocab_size`属性。

### 尝试3：`Qwen/Qwen3-4B-FP8`（已缓存，4.9GB）

- **状态**：已终止 —— 加载时挂起
- **问题**：FP8量化模型与Unsloth的4位BNB加载流程不兼容。进程占用31%CPU但仅使用309MB GPU —— 卡在权重转换环节。

## 实际可用的资源（已确认）

- 所有Python导入：✅ torch 2.10+cu128、unsloth、datasets、trl、peft、frontmatter、tiktoken
- CUDA：✅ 检测到RTX 4070，可用显存11.5GB
- 数据集：✅ 21,234条训练数据 + 200条评估数据正确加载
- 对话模板：✅ 正常工作

## 根本问题

本地未缓存兼容模型。需要下载正确的模型（`unsloth/Qwen3-4B-unsloth-bnb-4bit`或`unsloth/Qwen3-8B-unsloth-bnb-4bit`），但当前HuggingFace速度缓慢。

## 可选方案

1. **夜间下载**：`huggingface-cli download unsloth/Qwen3-4B-unsloth-bnb-4bit` —— 约4GB，当前速度下需3-4小时
2. **使用Qwen3-0.6B**（小型模型，下载快，适合流程验证）
3. **使用已缓存的模型** —— 但已缓存的模型（Qwen3.5-9B-VL、Qwen3-4B-FP8、Mistral-Small-3.2）均与Unsloth SFT流程不兼容
4. **等待网络条件改善**

需要我在后台开始下载Qwen3-4B，以便明天能直接用吗？还是先尝试0.6B模型快速验证流程？
