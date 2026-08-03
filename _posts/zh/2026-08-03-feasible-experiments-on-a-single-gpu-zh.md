---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在单个GPU上可行的实验
translated: true
type: note
---

情况是这样的：**DeepSpec 是一个用于推测解码 draft 模型训练/评估的仓库**，其默认流程是为数据中心节点设计的——8 块 GPU、约 38 TB 磁盘用于存放 target 缓存。这台机器只有 **1 块 RTX 4070（12 GB，约 2 GB 空闲）和 703 GB 可用磁盘**，所以请允许我坦诚说明哪些可以运行，哪些不行。

## 预期工作流程（根据 README）

```bash
# 1. 安装依赖（torch 2.9.1, transformers 5.10.2, ...）
python -m pip install -r requirements.txt

# 2. 数据准备（3 个阶段）：下载 prompts → 使用 target 模型通过 SGLang 重新生成答案 → 预计算 target 缓存（Qwen3-4B 需要约 38 TB！）
bash scripts/data/prepare_data.sh

# 3. 根据缓存的 target 输出训练 draft 模型
bash scripts/train/train.sh          # 每块可见 GPU 启动一个 worker（预期 8 块）

# 4. 在基准测试上评估推测解码的接受率
bash scripts/eval/eval.sh
```

## 在这台机器上可行的事项

**✅ 可行：使用已发布的 checkpoint 进行评估**（HF 可访问，torch 2.10 + CUDA 已安装）：

```bash
cd /mnt/data/DeepSpec
CUDA_VISIBLE_DEVICES=0 python eval.py \
    --target_name_or_path Qwen/Qwen3-4B \
    --draft_name_or_path deepseek-ai/dspark_qwen3_4b_block7 \
    --max-new-tokens 512
```

这将下载 target 和 draft 模型，并运行 9 个基准测试（GSM8K、MATH500、HumanEval 等）。注意事项：它会为每块可见 GPU 启动一个 worker（这里只有 1 块 GPU，没问题）；运行 Qwen3-4B（bf16 格式）加上 draft 模型需要约 8 GB VRAM，因此**请先关闭桌面/GNOME 应用以释放 VRAM**，并且单块 4070 上会较慢。如果你希望减少工作量，可以使用 `--tasks` 参数，但请注意 `eval.py` 中并未实现该参数——它硬编码了 `TASKS`。

**❌ 不可行：训练。** 存在两个障碍：
- 默认的 target 缓存需要 **约 38 TB 磁盘**（你只有 703 GB）。你必须将数据集缩减到极小，并减少 `config/dspark/dspark_qwen3_4b.py` 中的 `model.target_layer_ids`，但这会显著改变结果。
- 训练假设有 8 块 GPU（`train.sh` 使用 `CUDA_VISIBLE_DEVICES=0..7`）；即使 `local_batch_size=1`，单张 12 GB 的显卡也无法实际训练 Qwen3-4B 的 draft 模型。

**❌ 不可行：数据准备。** 需要以 8 块 GPU 运行 SGLang 来服务 Qwen3-4B（`scripts/data/launch_sglang_server.sh` 会启动 8 个 worker）。

## 如果你想在这台机器上运行点实际的东西

**选项 1——对已发布 checkpoint 进行评估（推荐，如上所述）。** 使用 [README 中的已发布 Checkpoints 表格](README.md) 中的任意一行；只需将 `--target_name_or_path` 与对应列匹配即可。

**选项 2——玩具规模的训练运行。** 将数据流程缩减到几百个样本（例如，设置更大的 `--test-size` 或过滤重新生成的 JSONL），减小 `max_length` 和 `target_layer_ids`，将 `data.target_cache_path` 指向一个小的缓存目录，设置 `CUDA_VISIBLE_DEVICES=0`，并将 `train.local_batch_size=1` 降低。你仍然很可能 OOM 或在一块 4070 上运行数天——将其视为冒烟测试，而非实际训练。

**选项 3——克隆到更大的机器上。** 这个仓库实际上是针对 8×80 GB 的节点设计的。如果你能访问这样的节点（或云端的 A100/H100 节点），那么顶部的三条命令就是全部所需。

需要我现在运行评估选项吗（先释放 VRAM），还是用一个小数据集设置一个最小的冒烟测试训练运行？