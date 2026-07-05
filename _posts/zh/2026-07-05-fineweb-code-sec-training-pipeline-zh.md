---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Fineweb-代码-SEC训练流水线
translated: true
type: note
---

## 综合摘要 — code-sec-fineweb 项目

### 我们构建了什么

一个完整的训练流水线：原始数据 → 预训练模型 → SFT 微调。

### 阶段 1：数据流水线 — `/mnt/data/zz/prepare_data.sh`

| 数据集 | 来源 | 格式 | 大小 | 目的 |
| --- | --- | --- | --- | --- |
| **github-code** | `codeparrot/github-code`（1126 分片中的 38 个） | Parquet，`content` 列 → 转换为 `text` 列 | 11 GB | 代码理解（Python、JS、Go 等） |
| **sec-edgar** | SEC 10-K 申报文件（17 个文件） | Parquet，提取 `text` 列 | 2.6 GB | 金融文档理解 |
| **fineweb-edu** | `HuggingFaceFW/fineweb-edu`（9 个分片） | Parquet，`text` 列 | 20 GB | 通用网络文本知识 |
| **合并后** | 所有 3 个数据集通过符号链接放入同一目录 | 64 个 Parquet 文件（63 个训练 + 1 个验证） | 34 GB | 混合训练数据 |

转换脚本：

- `scripts/extract/convert_github_code_for_nanochat.py` — 将 `content` 列重命名为 `text`
- `scripts/extract/convert_sec_edgar_for_nanochat.py` — 提取 `text` 列
- 在混合数据上训练的 tokenizer：`python -m scripts.tok_train`（32k 词表，2B 字符）

### 阶段 2：预训练 — 在 RTX 4070 上耗时 16.5 小时

```
bash /mnt/data/zz/fineweb-code-sec-gpt.sh
```

**模型：** d12（286M 参数），n_embd=768，n_head=6，seq_len=2048，window=L

**训练进度：**

```
Step   5000 | val_bpb: 1.680 | loss: 1.397 | 1.6h
Step  25000 | val_bpb: 1.568 | loss: 1.136 | 8.2h
Step  50000 | val_bpb: 1.418 | loss: 1.062 | 16.5h
```

检查点：`/home/lzw/.cache/nanochat/base_checkpoints/d12/`（每 5k 步，每个 793MB）

### 阶段 3：SFT 微调 — 正在运行

```
bash /mnt/data/zz/fineweb-code-sec-gpt/sft_code_sec.sh
```

**基础模型：** d12 step 50k → 在对话数据上微调

**SFT 数据混合（1,071,759 行）：**

| 数据集 | 行数 | 目的 |
| --- | --- | --- |
| **SmolTalk** | 460K | 通用对话 |
| **MMLU** x3 | 300K | 多项选择推理 |
| **SimpleSpelling** | 200K | 拼写任务 |
| **SpellingBee** | 80K | 字母计数 |
| **GSM8K** x4 | 32K | 数学应用题 |
| **Identity** | 1K | 模型身份/人格 |
| **自定义代码+SEC** | **1K** | 我们精选的代码和 SEC 对话 |

自定义数据格式（`prepare_sft_data.py`）：

```python
# JSONL 每行：
[{"role":"user","content":"写一个 Python 函数..."},
 {"role":"assistant","content":"def fibonacci(n):..."}]
```

SFT 使用 loss 掩码 — 仅训练 **assistant token**（mask=1），user/BOS/工具输出被忽略（mask=0）。对话格式使用特殊 token：`<|user_start|>`、`<|user_end|>`、`<|assistant_start|>`、`<|assistant_end|>`。

**SFT 状态：Step 1,591 / ~9,000（17.7%）**

```
Loss: 1.47（从 2.4 下降 → 表明模型正在学习对话格式）
速度：51,450 tok/s，1.27s/step
运行时间：已过 33 分钟，完成一个 epoch 还需约 2.5 小时
```

第一次验证评估在 step 500（尚未达到 — eval-every=500）。检查点保存到 `~/.cache/nanochat/chatsft_checkpoints/d12/`。

### 待完成事项

1. **SFT 完成** — 完整 epoch 将在约 2.5 小时内结束
2. **测试生成** — 运行 `run_prompts.py --step=<sft_step>` 比较预训练模型与 SFT 模型的质量
3. **GGUF 导出** — 转换为 GGUF 格式用于 llama.cpp 服务

### `/mnt/data/zz/` 中的脚本

```
fineweb-code-sec-gpt.sh        # 预训练（50k 步）
prepare_data.sh                # 完整数据流水线
train_log.sh                   # 监控工具

fineweb-code-sec-gpt/
  prepare_sft_data.py          # 创建 1000 条代码+SEC 对话 JSONL
  sft_code_sec.sh              # SFT 微调
  run_prompts.py               # 从任意检查点生成样本
  prompt_*.txt                 # 13 个测试提示（代码/SEC/通用）
  results.txt                  # 生成结果（预训练模型）
```
