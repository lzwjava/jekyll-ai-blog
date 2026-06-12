---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 博客笔记的微调流水线
translated: true
type: note
---

## 综合总结 — lzwjava 笔记微调流程

### 目标
对大型语言模型进行微调，使其学习 lzwjava 在 `jekyll-ai-blog` 中约 16k 篇博客笔记（英文+中文）的写作风格和回答方式。

---

### 1. 创建 `/mnt/data/zz/finetune/` 流程

**数据集提取** (`build_dataset.py`)：
- 从 `_posts/en/` 和 `_posts/zh/` 中解析带有 YAML 前置数据的 Jekyll markdown 文件
- 清理 Liquid 标签 `{% %}`、kramdown `{: .class}`、图片引用和说明文字
- 未做过滤 — 按需求包含 AI 生成的文章
- 输出：`{question: title, answer: body}` 对话格式

| 统计项 | 数值 |
|---|---|
| 英文文章 | 10,726 |
| 中文文章 | 10,708 |
| 总样本数 | 21,434 |
| 总 Token 数 | 25.1M |
| 平均每样本 Token 数 | 1,169 |
| 训练集 | 21,234 |
| 评估集 | 200 |
| 跳过（过短） | 30 |

**训练脚本** (`train.py`)：
- 经过三次迭代才成功：
  1. **基于 Unsloth** — Triton kernels 在 RTX 4070 上出现段错误（torch 2.10+cu128，Triton 3.6.0）
  2. **使用 `UNSLOTH_DISABLE_TRITON=1` 的 Unsloth** — 仍然出现段错误
  3. **纯 transformers + peft** — 完美运行
- 最终技术栈：`transformers` loader + `peft` LoRA + `trl.SFTTrainer`
- 配置：Qwen3-4B，4-bit，LoRA r=32，6600 万可训练参数（1.6%）
- 修复 TRL 0.24 API：使用 `processing_class` 代替 `tokenizer`，不在 SFTConfig 中设置 `max_seq_length`
- 训练时禁用评估（完整词表 logits 计算导致 OOM）
- 仅保存 LoRA adapter（4-bit 模型无法在内存中合并为 16-bit）

**辅助脚本**：
- `eval.py` — 在保留标题上比较微调模型与基础模型
- `export_gguf.py` — 导出 GGUF 格式用于 ollama/llama.cpp
- `README.md` — 完整使用指南
- `requirements.txt` — pip 依赖

---

### 2. 模型下载历程

| 模型 | 大小 | 尝试方式 | 结果 |
|---|---|---|---|
| `unsloth/Qwen3-8B` (4-bit) | 7.5GB | 直接下载 + hf-mirror | 速度太慢（300-470KB/s），中断 |
| `Qwen/Qwen3.5-9B`（缓存） | 18GB | 直接加载 | 视觉语言模型，类型错误 |
| `Qwen/Qwen3-4B-FP8`（缓存） | 4.9GB | 直接加载 | 与 Unsloth 配合时卡死，不兼容 |
| **`unsloth/Qwen3-4B-unsloth-bnb-4bit`** | **3.4GB** | **curl 直接下载** | **可用** |

最终下载：直接从 `huggingface.co` 下载，速度约 37MB/s（网络恢复）。手动设置 HF 缓存结构并创建符号链接，因为 `hf` CLI 和 `hf-mirror.com` 都没有这个模型。

---

### 3. Unsloth Triton 问题调查

段错误模式：
- 训练和推理在第 0 步时崩溃
- 退出代码 139（SIGSEGV）
- 在全 LoRA（7 个目标模块）和最小 LoRA（2 个模块）时均发生
- `UNSLOTH_DISABLE_TRITON=1` 无效
- 环境：torch 2.10+cu128，CUDA 12.8，Triton 3.6.0，RTX 4070（compute 8.9）

解决方案：完全放弃 Unsloth。纯 transformers + peft 可以运行，约 1.25 秒/步。

---

### 4. Git 记录

```
8292db9  添加 lzwjava 笔记 SFT 微调流程
9aaa8f3  修复 train.py：使用纯 transformers+peft，修复 TRL 0.24 API
```

已推送到 `github.com:lzwjava/zz.git`。JSONL 文件和输出目录已在 .gitignore 中忽略。

---

### 5. 当前训练状态

大约 17:18 在 tmux 会话中启动：

```
模型：      Qwen3-4B-unsloth-bnb-4bit（4-bit，3.4GB 缓存）
LoRA：       r=32，6600 万参数，所有投影层
数据集：     21,234 样本，25.1M token
配置：       batch 16（2×8），余弦学习率 2e-4，2 个 epoch
步数：       400 / 2,656（15%）
损失：       2.86 → 1.70
GPU：        11.5GB，100% 利用率
检查点：     已保存第 10、200、400 步
预计剩余时间：约 9 小时（明天约 04:00）
输出目录：   /mnt/data/zz/finetune/lzw-notes-lora/
```

---

### 6. 训练后计划

```bash
# 测试 adapter
python3.11 eval.py

# 导出为 GGUF 格式用于 ollama
python3.11 export_gguf.py

# 或使用 vLLM 提供服务
vllm serve ./lzw-notes-lora --max-model-len 4096
```