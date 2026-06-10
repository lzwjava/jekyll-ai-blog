---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 纳米聊天训练深度解析
translated: true
type: note
---

以下是完整的深入解析。

=================================================================
训练期间涉及的文件（base_train.py）
=================================================================

核心流程：

  nanochat/gpt.py          -- 模型架构（GPT、GPTConfig、注意力机制、MLP）
  nanochat/dataloader.py   -- Parquet 数据加载器，带 BOS-bestfit 打包
  nanochat/dataset.py      -- 从磁盘列出 parquet 分片文件
  nanochat/tokenizer.py    -- 自定义分词器（训练/编码/解码）
  nanochat/optim.py        -- MuonAdamW 优化器（矩阵用 Muon，其余用 AdamW）
  nanochat/common.py       -- DDP 初始化、设备检测、print0、COMPUTE_DTYPE
  nanochat/flash_attention.py -- FA3/FA2/SDPA 统一接口
  nanochat/loss_eval.py    -- 用于验证损失的 evaluate_bpb()
  nanochat/checkpoint_manager.py -- 保存/加载检查点
  nanochat/engine.py       -- KVCache + 生成引擎（用于 sample_every）
  nanochat/core_eval.py    -- CORE 指标评估
  nanochat/fp8.py          -- 可选的 FP8 训练（H100+）
  nanochat/mlflow_logger.py -- MLflow 集成
  scripts/base_eval.py     -- base_train 导入的 evaluate_core()

=================================================================
训练逻辑流程
=================================================================

1. 初始化阶段
   - 自动检测 GPU，初始化 DDP（torchrun）或单 GPU
   - 初始化实验追踪器（wandb/mlflow/无）
   - 加载分词器，获取 vocab_size
   - 在 meta 设备上构建模型（不占用内存），然后 .to_empty(device).init_weights()
   - 可选地加载检查点以恢复训练
   - 可选地将 Linear 转换为 Float8Linear（--fp8）
   - torch.compile(model)

2. 缩放定律（智能部分）
   - 在 meta 上构建参考 d12 模型以获取缩放参数
   - 计算最优 token 数 = target_param_data_ratio * scaling_params
   - 通过 Power Lines 计算最优批次大小：Bopt ∝ D^0.383
   - 计算学习率修正：η ∝ sqrt(B/Bref)
   - 计算权重衰减：λ = λref *sqrt(B/Bref)* (Dref/D)  （T_epoch 框架）

3. 优化器
   - 矩阵参数（transformer.h）使用 Muon —— Newton-Schulz 正交化
   - 嵌入层、lm_head、标量（resid_lambdas、x0_lambdas、smear）使用 AdamW
   - 每个参数组有独立的学习率，按 1/sqrt(model_dim/768) 缩放

4. 数据加载
   - 读取 parquet 分片（fineweb-edu）行组
   - BOS-bestfit 打包：每行以 BOS 开头，文档按最佳拟合打包
   - 约 35% 的 token 被裁剪（未浪费，只是不参与训练）
   - GPU 预分配缓冲区，每批次一次 HtoD 拷贝

5. 训练循环
   while step <= num_iterations:
     - 每 eval_every 步：在验证集上运行 evaluate_bpb
     - 每 core_metric_every 步：运行 CORE 评估（ARC、MMLU、GSM8K、HumanEval、SpellingBee）
     - 每 sample_every 步：从固定提示生成样本
     - 每 save_every 步：保存模型 + 优化器 + 元检查点
     - 使用梯度累积进行前向传播（total_batch_size / world_tokens_per_fwdbwd）
     - 学习率调度：线性预热 -> 恒定 -> 线性冷却
     - Muon 动量：预热 0.85->0.97，冷却至 0.90
     - 权重衰减：余弦衰减至零
     - optimizer.step()，zero_grad

=================================================================
与 nano-GPT 的对比
=================================================================

| 特性               | nanoGPT                   | nanochat                     |
|--------------------|---------------------------|------------------------------|
| 优化器             | 仅 AdamW                  | MuonAdamW（矩阵用 Muon，     |
|                    |                           | 嵌入层/标量用 AdamW）        |
| 位置编码           | 学习到的绝对位置嵌入       | 旋转位置嵌入（RoPE）         |
| 注意力归一化       | 无                       | QK 归一化（对 q,k 使用 rms_norm） |
| MLP 激活函数       | GELU                     | ReLU²                        |
| 归一化类型         | LayerNorm                | RMSNorm（无可学习参数）      |
| 归一化位置         | 预归一化                 | 嵌入后归一化 + 块前归一化    |
| 嵌入/反嵌入        | 权重绑定                 | 权重不绑定（独立学习率）     |
| 注意力             | 多头注意力（MHA）         | 支持 GQA（n_kv_head <= n_head） |
| 滑动窗口           | 无                       | 有，可配置模式（SSSL 等）    |
| Flash Attention    | 未内置                   | FA3 > FA2 > SDPA 自动切换    |
| KV 缓存（推理）    | 未内置                   | 完整的 KVCache 类，带 FA3 API |
| 值嵌入             | 无                       | ResFormer 风格值嵌入门控     |
| 残差缩放           | 无                       | 每层 resid_lambdas + x0_lambdas |
| Smear（前一个 token）| 无                     | Smear 门控混合前一个嵌入     |
| Backout            | 无                       | 减去中间层残差               |
| Logit softcap      | 无                       | tanh softcap 为 15           |
| 数据加载           | tiktoken, mmap .bin      | Parquet 分片，BOS-bestfit 打包 |
| 分词器             | tiktoken GPT-2 BPE       | 自定义 sentencepiece 训练的分词器 |
| 缩放定律           | 无                       | 从深度自动计算批次/学习率/冷却参数 |
| FP8 训练           | 无                       | 可选的 FP8（H100+）          |
| 分布式             | 基础 DDP                 | DDP + 梯度累积 + 缩放        |
| 检查点             | 手动保存                 | checkpoint_manager 带状态恢复 |
| 评估               | 手动                     | 自动 CORE 指标、验证 bpb、样本生成 |
| 追踪器             | wandb 手动               | wandb/mlflow/无 自动配置     |
| SFT/聊天流程       | 未包含                   | 完整：chat_sft.py、chat_web.py、chat_cli.py |
| 计算器工具使用     | 无                       | 内置：<|python_start|>...<|python_end|> |

主要结构差异：

- nanoGPT 是单个文件（model.py 约 300 行）。nanochat 是一个完整项目，包含 15 个以上模块、一个三阶段流程（预训练 -> SFT -> RL）以及生产级服务。
- nanoGPT 使用标准 AdamW。nanochat 使用 Muon 优化器（基于 Newton-Schulz）用于权重矩阵，收敛更快。
- nanoGPT 的模型本质上是 GPT-2 架构。nanochat 包含许多现代附加功能：RoPE、GQA、QK 归一化、ReLU²、值嵌入、滑动窗口、smear、backout、logit softcap。

=================================================================
chat_sft.py —— 监督微调
=================================================================

采用预训练的基础模型，在聊天数据上进行微调。

数据混合：

- SmolTalk：46 万行通用对话
- CustomJSON：1000 行身份对话（你是谁？）
- MMLU：10 万行 x3 个 epoch（教授多项选择）
- GSM8K：8000 行 x4 个 epoch（教授数学 + 工具使用）
- SimpleSpelling：20 万行（拼写单词 'apple'）
- SpellingBee：8 万行（'strawberry' 中有几个 'r'？）

与 base_train 的主要区别：

- 加载预训练检查点，继承超参数
- 使用损失掩码：仅助理 token 有损失，用户/填充 token 被掩码（-1）
- 最佳拟合对话打包（算法相同但考虑对话结构）
- 评估 ChatCORE 指标（通过聊天方式评估 ARC、MMLU、GSM8K、HumanEval、SpellingBee）
- 基于进度（0->1）的学习率调度，而非绝对步数
- 权重衰减 = 0（延续预训练结束时的归零状态）
- 保存到 chatsft_checkpoints/ 而非 base_checkpoints/

=================================================================
chat_web.py —— 生产级 Web 服务器
=================================================================

FastAPI 服务器，提供：

- GET /           -> HTML 聊天界面（来自 nanochat/ui.html）
- POST /chat/completions -> 兼容 OpenAI 的流式 API
- GET /health     -> 健康检查
- GET /stats      -> 工作池统计信息

通过 WorkerPool 实现多 GPU：每个 GPU 加载一份完整模型副本，请求轮询分发。
滥用限制：500 条消息/请求，每条消息 8000 字符，总计 32000 字符，温度 0-2，top-k 0-200。

使用 Engine.generate()，该函数带有 KV 缓存（见下文）。

=================================================================
KV 缓存 —— 是的，推理时使用
=================================================================

是的。KV 缓存已在 nanochat/engine.py 中完整实现，并在所有推理场景中使用（chat_cli、chat_web、训练中的 sample_every）。

KVCache 类（engine.py:82-137）：

- 预分配：(n_layers, B, T, H, D) 张量用于 K 和 V
- 通过 cache_seqlens（int32 张量）跟踪位置
- 存储 prev_embedding 用于解码过程中的 smear 机制
- FA3 通过 flash_attn_with_kvcache 就地更新缓存

Engine.generate() 的使用方式：

  1. 预填充：创建 KVCache(batch=1, seq=len(prompt))，将完整提示通过
     model.forward(tokens, kv_cache=kv_cache_prefill) 处理
  2. 克隆：创建 KVCache(batch=num_samples)，.prefill(从预填充缓存复制)
  3. 解码循环：每一步仅输入新 token，模型从缓存中读取
     model.forward(new_token, kv_cache=kv_cache_decode)  # T=1，缓存包含所有先前内容

model.forward()（gpt.py:416）处理两种模式：

- kv_cache=None  -> 训练：完整因果注意力，无缓存
- 给定 kv_cache -> 推理：flash_attn_with_kvcache，缓存感知的旋转偏移

滑动窗口也适用于 KV 缓存：window_size 被传递到
flash_attn_with_kvcache，因此 SSSL 模式在推理时同样适用。

计算器工具使用也在生成期间工作：当引擎检测到
<|python_start|>...<|python_end|> 时，它 eval() 该表达式，并强制将结果 token 作为
<|output_start|>结果<|output_end|> 插入到流中。
