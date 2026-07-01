---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat在RTX 4070上的训练
translated: true
type: note
---

以下是完整的事件经过：

## RTX 4070 工作站上的 Nanochat 设置总结

### 1. 克隆仓库

通过 SSH 连接到 `lzw@192.168.1.36`，将 `https://github.com/karpathy/nanochat` 克隆到 `/mnt/data/nanochat/`（3.7 MB，纯代码——数据在运行时单独下载）。

### 2. 安装 uv（Python 包管理器）

工作站已有 Python 3.12.3，但没有 `uv`。安装它：

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安装到 `~/.local/bin/uv`。项目的 `pyproject.toml` 需要使用 uv 进行依赖管理——它通过自定义 PyTorch 索引锁定了 `torch==2.9.1+cu128`（CUDA 12.8）。

### 3. 创建虚拟环境并安装依赖

```
cd /mnt/data/nanochat
uv venv                    # 创建 .venv，使用 CPython 3.10.20（自动下载）
uv sync --extra gpu        # 安装 81 个包，包括 torch 2.9.1+cu128
```

关键包：`torch`、`triton`、`nvidia-cudnn`、`nvidia-nccl`、`datasets`、`wandb`、`fastapi`、`tiktoken`、`tokenizers`、`rustbpe`。总下载量约 3 GB。

### 4. 遇到 wandb 问题

首次运行崩溃，因为 `--run=rtx4070-d8` 触发了 wandb 初始化，但未配置 API 密钥。解决方法：在脚本中添加 `export WANDB_MODE=disabled`。代码中有一个 `DummyWandb()` 回退机制（当运行名称为 "dummy" 时启用），但 `WANDB_MODE=disabled` 更干净——它允许使用任何运行名称而无需 wandb 认证。

### 5. 为 RTX 4070（12 GB）编写自定义运行脚本

默认的 `speedrun.sh` 针对 8×H100（每张 80 GB，共 640 GB）。必须为单张 12 GB 显卡缩小所有参数：

| 参数 | speedrun.sh（8×H100） | 我们的运行（RTX 4070） | 原因 |
| ----------- | ---------------------- | -------------------- | ---- |
| `--depth` | 24 | 8 | 更小的模型（约 40M 参数 vs 约 1.6B） |
| `--device-batch-size` | 16 | 4 | 适配 12 GB VRAM |
| `--total-batch-size` | 自动（1M tokens） | 32768 | 单 GPU 合理值 |
| `--max-seq-len` | 2048 | 1024 | 节省 VRAM |
| `--fp8` | 是 | 否 | RTX 4070 为 SM 89，不支持 fp8 |
| `--num-iterations` | 自动（计算最优） | 5000 | 快速演示运行 |
| `--core-metric-every` | 2000 | -1 | 训练期间跳过昂贵的 CORE 评估 |
| GPUs | 8（torchrun） | 1（python -m） | 梯度累积自动处理 |

### 6. 运行时数据流水线

nanochat 在运行时下载自己的数据（不包含在仓库中）：

- **步骤 1**：`python -m nanochat.dataset -n 8` —— 从 HuggingFace 下载 8 个分片（约 2B 字符，约 800 MB）的 ClimbMix 预训练数据，存放至 `~/.cache/nanochat/base_data_climbmix/`
- **步骤 2**：`python -m scripts.tok_train` —— 在下载的数据上训练一个 BPE 分词器（词表大小 32768）
- **步骤 3**：预训练 —— 5000 步，约 103K tok/sec，约 26 分钟
- **步骤 4**：下载 SFT 身份对话（2.3 MB JSONL，来自 Karpathy 的 S3）
- **步骤 5**：SFT —— 1500 步，教会模型对话格式
- **步骤 6**：评估 + 聊天

### 7. 当前状态

在 tmux 会话 `nanochat` 中运行。预训练已完成约 1.6%（第 81/5000 步），损失稳步下降（7.73 → 6.22），VRAM 使用仅 2.7 GB / 12 GB，GPU 利用率 99%。

### 关键要点

nanochat 是自包含的——你只需要一块 GPU 和 uv。它会下载数据、训练分词器、预训练、SFT 并提供聊天 UI，全部通过一个脚本完成。`--depth` 参数自动控制其他所有内容（宽度、注意力头数、学习率、训练轮次）。在 12 GB 显卡上，depth=8 很舒适；如果使用更小的 batch size，可以推到 depth=12-16。
