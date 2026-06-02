---
audio: false
generated: true
image: false
lang: zh
layout: post
title: nanochat代码库架构指南
translated: true
type: note
---

现在我对代码库有了全面的理解。以下是指南：

---

nanochat 代码库指南
========================

nanochat（作者 Andrej Karpathy）是一个极简的端到端 LLM 训练框架，涵盖所有主要阶段：分词、预训练、SFT、RL、评估、推理以及类 ChatGPT 网络 UI。核心理念是：一个旋钮（`--depth`）控制模型大小，其他一切自动推导。

---

1. 架构概览

-------------------------

项目包含 4 个目录：

```
nanochat/     -- 核心库（模型、数据、优化器、引擎）
scripts/      -- 可执行入口点（训练、评估、聊天）
tasks/        -- 评估任务定义（MMLU、GSM8K 等）
runs/         -- 完整训练流程的 Shell 脚本
```

训练流程如下：

  分词器训练 -> 基础预训练 -> SFT 微调 -> RL（可选）-> 聊天

所有中间产物存放于 `~/.cache/nanochat/`（可通过 `$NANOCHAT_BASE_DIR` 覆盖）。

---

2. 核心库（`nanochat/`）

-----------------------------

**gpt.py** -- GPT Transformer 模型

- `GPTConfig` 数据类：sequence_len、vocab_size、n_layer、n_head、n_kv_head、n_embd、window_pattern
- `GPT(nn.Module)`：完整模型。关键架构选择：
  - 旋转位置嵌入（无学习位置嵌入）
  - 旋转后的 QK 归一化
  - 解绑的词嵌入（`wte`）和输出投影（`lm_head`）
  - MLP 中的 ReLU²（平方 ReLU）激活
  - RMSNorm（归一化中无可学习参数）
  - 所有线性层无偏置
  - 分组查询注意力（GQA）：n_kv_head <= n_head 以实现高效推理
  - 每层可学习标量：`resid_lambdas`（残差缩放）和 `x0_lambdas`（初始嵌入混合）
  - Smear：将前一个 token 的嵌入混合到当前位置（廉价二元信息）
  - Backout：在最终归一化前减去中间层残差以移除低级特征
  - 值嵌入（ResFormer 风格）：交替层获得学习的值嵌入，按头门控
  - Logit softcapping（15.0）以防止极端 logits
  - 词汇表填充至 64 以提高 DDP/张量核心效率
  - 滑动窗口注意力模式：例如 "SSSL" = 3 短 + 1 长，在各层间平铺
- `init_weights()`：精细初始化方案（权重均匀分布、投影为零、嵌入正态分布）
- `setup_optimizer()`：返回混合 Muon+AdamW 优化器，含独立参数组和学习率缩放
- `forward()`：完整前向传播。处理训练（给定目标）和推理（kv_cache）
- `generate()`：朴素自回归生成（无 KV 缓存，用于测试）

**engine.py** -- 高效推理引擎

- `KVCache`：为 Flash Attention 3 预分配的缓存（B, T, H, D 布局，非 B, H, T, D）
- `Engine`：封装模型 + 分词器。采用预填充后解码策略：
  - 对提示进行批大小为 1 的预填充 -> 为 N 个样本克隆 KV 缓存 -> 并行解码
- `RowState`：每行跟踪，用于工具使用状态机（Python REPL）
- `use_calculator()`：Python 工具调用的安全 eval（数学表达式 + `.count()`）
- 支持工具使用的 token：`<|python_start|>` / `<|python_end|>` / `<|output_start|>` / `<|output_end|>`

**flash_attention.py** -- 统一 Flash Attention 接口

- 在 Hopper（sm90）GPU 上自动检测 FA3，否则回退到 PyTorch SDPA
- 导出 `flash_attn` 模块作为即插即用替代：`flash_attn_func()` 和 `flash_attn_with_kvcache()`
- SDPA 回退手动处理滑动窗口、GQA 和 KV 缓存管理

**optim.py** -- 混合 Muon + AdamW 优化器

- `adamw_step_fused`：`@torch.compile` 融合 AdamW 步骤（权重衰减 -> 动量 -> 偏差校正 -> 更新）
- Muon 优化器：用于正交化的 Newton-Schulz 迭代 + Polar Express 符号方法 + NorMuon 方差减少
- `MuonAdamW`：单 GPU 版本。`DistMuonAdamW`：分布式版本，带跨 rank 的全规约
- 矩阵参数（注意力 + MLP 权重）-> Muon；嵌入、lm_head、标量 -> AdamW

**tokenizer.py** -- BPE 分词器

- 两个后端：`HuggingFaceTokenizer`（训练+推理）和 `RustBPETokenizer`（rustbpe 训练 + tiktoken 推理）
- 9 个特殊 token：`<|bos|>`、`<|user_start/end|>`、`<|assistant_start/end|>`、`<|python_start/end|>`、`<|output_start/end|>`
- `render_conversation()`：将聊天格式字典转换为 token ID + 损失掩码（mask=1 表示 assistant token 需要训练）
- `render_for_completion()`：相同但删除最后一条 assistant 消息（用于 RL 中的 rollout）
- GPT-4 风格分割模式，使用 `\p{N}{1,2}`（非 1-3，针对小词汇量优化）
- 默认词汇量：32768

**dataloader.py** -- BOS 对齐的最佳适应打包

- 文档使用最佳适应算法打包（最小化裁剪）
- 每行以 BOS token 开始（更干净的注意力模式）
- 100% 利用率（无填充），在 T=2048 时约 35% 的 token 被裁剪
- `_document_batches()`：在 parquet 文件上的无限多轮迭代器，支持 DDP 分片

**dataset.py** -- 数据下载/管理

- 从 HuggingFace 下载预训练数据分片（parquet 文件）
- 默认数据集：NVIDIA ClimbMix（当前速度跑中使用）

**common.py** -- 工具函数

- `COMPUTE_DTYPE`：自动检测（Ampere+ 上为 bf16，否则为 fp32）。可通过 `$NANOCHAT_DTYPE` 覆盖
- `compute_init()`：种子、精度、DDP 设置（torchrun 环境检测）
- `get_peak_flops()`：硬编码的 BF16 峰值 FLOPS 表，用于 MFU 计算
- `print0()`、`DummyWandb`、彩色日志

**checkpoint_manager.py** -- 保存/加载

- 三个检查点目录：`base_checkpoints/`、`chatsft_checkpoints/`、`chatrl_checkpoints/`
- 每步文件：`model_XXXXXX.pt`、`optim_XXXXXX_rankN.pt`、`meta_XXXXXX.json`
- `build_model()`：元设备初始化 -> 加载状态字典 -> 修补缺失键以向后兼容
- `load_model(source)`：便捷函数；source 为 "base"、"sft" 或 "rl"

**core_eval.py** -- DCLM CORE 指标评估

- 实现 DCLM 基准（多项选择、模式、语言建模任务）
- 使用 Jinja2 模板进行少样本提示
- 对 MC 任务使用基于损失的选择，对 LM 任务使用精确匹配

**loss_eval.py** -- 每字节比特数（BPB）评估

- 词汇量不变的损失指标：按 token 字节长度归一化交叉熵
- 特殊 token（BOS 等）从指标中排除

**fp8.py** -- FP8 训练支持（需要 H100+ 和 torchao）

**execution.py** -- 模型的 Python 代码执行工具

---

3. 脚本（`scripts/`）

-----------------------

**base_train.py** -- 预训练（主训练循环）

- 关键参数：`--depth`（单一复杂度旋钮）、`--target-param-data-ratio`、`--fp8`、`--device-batch-size`
- 自动推导：n_embd = depth * aspect_ratio，n_head = n_embd / head_dim 等
- 学习率调度：线性预热 + 余弦降温
- 记录到 wandb：val_bpb、core_metric、MFU、tok/sec、VRAM
- 定期操作：BPB 评估、CORE 指标评估、文本采样、检查点保存

**base_eval.py** -- 评估基础模型（CORE 分数 + BPB + 样本）

**chat_sft.py** -- 监督微调

- 加载基础模型检查点，在聊天格式对话上训练
- 任务混合：SmolTalk + MMLU + GSM8K + SpellingBee + CustomJSON（身份数据）
- 损失掩码：仅训练 assistant token（mask=1）
- 继承预训练检查点的大部分超参数

**chat_rl.py** -- 强化学习（简化版 GRPO/REINFORCE）

- 通过策略梯度在 GSM8K 上训练
- 无 KL 正则化，无 PPO 裁剪（在线策略，无信任区域）
- DAPO 风格 token 级归一化，均值减去的优势
- 在 GSM8K 测试集上评估 pass@k

**chat_eval.py** -- 在任务套件上评估聊天模型

**chat_cli.py** -- CLI 聊天界面

**chat_web.py** -- FastAPI + uvicorn 网络 UI（类 ChatGPT）

**tok_train.py** -- 训练 BPE 分词器

**tok_eval.py** -- 评估分词器压缩率

---

4. 任务（`tasks/`）

-------------------

- `common.py`：`TaskMixture`（加权混合）和 `TaskSequence`（顺序）
- `mmlu.py`：多项选择，57 个科目
- `gsm8k.py`：小学数学（8000 题），支持工具使用（计算器）
- `arc.py`：科学问题（多项选择）
- `spellingbee.py`：字母计数/拼写任务
- `humaneval.py`：简单 Python 编程
- `smoltalk.py`：HuggingFace SmolTalk 对话数据集
- `customjson.py`：加载任意 JSONL 对话

---

5. 运行脚本（`runs/`）

------------------------

- **speedrun.sh** -- 完整 GPT-2 训练流程（8xH100 上约 3 小时）：
  1. 设置 uv venv
  2. 下载数据分片（约 170 个）
  3. 训练分词器（32K 词汇量，基于约 2B 字符）
  4. 使用 FP8 预训练 d24 模型
  5. 评估基础模型
  6. 下载身份对话
  7. SFT 微调
  8. 评估聊天模型
  9. 生成报告

- **miniseries.sh** -- 扫描不同深度以生成缩放律数据
- **scaling_laws.sh** -- 缩放律实验
- **runcpu.sh** -- 在 CPU/MPS 上的小型模型训练（仅用于测试）

---

6. 深度旋钮

-----------------

最重要的概念。设置 `--depth=N` 会自动推导所有内容：

```
n_embd      = depth * aspect_ratio（默认 64）
n_head      = n_embd // head_dim（默认 128）
n_kv_head   = n_head（GQA 可减少此值）
vocab_size  = 32768
sequence_len = 2048
```

GPT-2 能力约在 d24-d26 范围。快速实验约 d12（8xH100 上约 5 分钟）。

---

7. 数据流

------------

```
原始 parquet 分片
    -> dataloader.py（BOS 对齐的最佳适应打包）
    -> 分词后的批次（B, T）整数
    -> 模型前向传播（交叉熵损失）
    -> Muon + AdamW 优化器步骤
    -> 检查点保存
    -> SFT：带损失掩码的聊天格式对话
    -> RL：在线策略 rollout + REINFORCE
    -> Engine 推理（KV 缓存 + 预填充/解码）
    -> CLI 或 网络 UI
```

---

8. 关键设计决策

------------------------

- 无 `torch.amp.autocast`。通过 `COMPUTE_DTYPE` 和自定义 `Linear` 层进行显式 dtype 管理
- 无配置对象/工厂。单一 `GPT` 模块，单一 `GPTConfig` 数据类
- 无框架开销。纯 PyTorch，最小抽象
- 词汇表填充以提高 DDP 效率（避免填充时的 rank 差异）
- 元设备初始化模式（先初始化形状，然后 `init_weights()`）
- BOS 对齐打包以约 35% token 裁剪换取更干净的注意力模式
- 矩阵权重的 Muon 优化器（收敛更快），嵌入/标量的 AdamW
