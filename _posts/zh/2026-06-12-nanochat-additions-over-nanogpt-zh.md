---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat在nanoGPT之上的新增功能
translated: true
type: note
---

以下是 nanochat 在 nanoGPT 基础上新增功能的完整说明：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  nanochat vs nanoGPT — 新增内容
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT 仅是一个预训练工具，包含：

- model.py（约 340 行）：标准 GPT-2 架构（LayerNorm、GELU、可学习位置嵌入、权重共享、线性层带偏置）
- train.py（约 300 行）：在原始文本上的预训练循环
- sample.py：基础文本生成
- 仅此而已，共 2 个 Python 文件。

nanochat 在一个仓库中实现了完整的 LLM 生命周期。以下是每一项主要新增功能：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 模型架构（gpt.py）—— 显著升级
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| 特性                  | nanoGPT                  | nanochat                          |
|--------------------------|--------------------------|-----------------------------------|
| 位置编码               | 可学习（wpe 嵌入）      | 旋转位置编码（RoPE）—— 无需 wpe   |
| 归一化                | LayerNorm（可学习）      | RMSNorm（无可学习参数）            |
| 激活函数               | GELU                     | ReLU²（relu 平方）                 |
| 注意力机制            | 合并的 c_attn 单个层     | 分离的 c_q、c_k、c_v、c_proj      |
| KV 头                 | 仅多头注意力（MHA）      | 分组查询注意力（GQA）              |
| QK 归一化             | 无                       | 有（q、k 在 RoPE 后归一化）        |
| 偏置                  | 有（可配置）            | 无任何偏置                         |
| 权重共享              | 有（wte = lm_head）      | 无 —— 嵌入层不共享                 |
| Dropout               | 有                       | 完全无 Dropout                     |
| Logit 软上限          | 无                       | 有（tanh 软上限，范围 ±15）        |
| 滑动窗口注意力        | 无                       | 有（按层采用 SSSSL 模式）          |
| 值嵌入                | 无                       | ResFormer 风格的值残差              |
| Smear（前一个 token 混合）| 无                       | 门控混合前一个 token 嵌入          |
| Backout（中间层减法） | 无                       | 减去一半的残差流                   |
| 残差缩放              | 固定                     | 按层的 resid_lambdas + x0          |
| Flash Attention       | PyTorch SDPA             | FA3 → FA2 → SDPA 降级链            |
| KV 缓存               | 无（基于裁剪）          | 用于推理的 FA3 KV 缓存              |
| FP8 训练              | 无                       | 动态张量级 FP8（e4m3/e5m2）        |
| 优化器                | 单一 AdamW               | MuonAdamW（矩阵用 Muon，            |
|                          |                          | 嵌入/标量用 AdamW）                 |
| 权重初始化            | Normal(0, 0.02)           | 注意力层用均匀分布，投影层用零，    |
|                          |                          | 显式按层初始化 resid/x0           |
| 词汇表填充            | 是（填充至 50304）       | 是（填充至最近的 64）               |

关键架构更改说明：

  RoPE vs 可学习位置编码：nanoGPT 为每个位置添加可学习嵌入（wpe）。nanochat 使用旋转位置嵌入——通过复数空间中的旋转编码相对位置。更好的长度泛化。

  ReLU² vs GELU：`F.relu(x).square()` —— 更简单、更快，在此规模下经验上具有竞争力。无需计算 erf。

  GQA：n_kv_head 可以小于 n_head。例如，6 个查询头但只有 6 个 KV 头（此处相等，但基础设施支持 GQA 比例）。推理时节省 KV 缓存内存。

  滑动窗口：`SSSL` 模式意味着 3 层使用短窗口（1/4 上下文），1 层使用完整上下文。按层平铺。最后一层始终为完整上下文。在大多数层节省 FLOP，同时保持长程能力。

  值残差（ResFormer）：每隔一层具有可学习的逐 token 嵌入（value_embeds），通过门控注入到 V 张量中。`v = v + gate * ve`。交替层，最后一层始终包含。

  Smear：通过可学习门控将前一个 token 的嵌入混合到当前 token。嵌入级别的廉价二元信息流。`x = x + sigmoid(gate(x)) * x_prev`

  Backout：在中间层缓存残差流。在最终归一化之前，减去 `lambda * x_backout` 以在 logit 投影前移除低级特征。

  Muon 优化器：矩阵参数使用 Muon（动量 + Newton-Schulz 正交化），嵌入使用 AdamW。每个参数组有独立的学习率调度。对于大型矩阵参数效率更高。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. SFT —— 监督微调（chat_sft.py）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT 没有 SFT。nanochat 包含完整的 SFT 流水线：

SFT 的作用：
  将预训练的基础模型在对话（用户/助手对）上进行微调，使其学习遵循指令并进行对话。

在 nanochat 中的工作方式：

  a) 对话渲染（tokenizer.render_conversation）：
     - 对话使用特殊 token 进行分词：
       <|bos|> <|user_start|> ... <|user_end|> <|assistant_start|> ... <|assistant_end|>
     - 生成损失掩码：仅助手 token 的 mask=1
     - 用户提示、BOS、特殊 token 的 mask=0（不参与训练）

  b) 数据混合（TaskMixture）：
     - SmolTalk：460K 行通用对话
     - CustomJSON：1000 行合成身份对话（"你是谁？" "我是 nanochat..."）
     - MMLU：100K 行 × 3 轮次（多项选择知识）
     - GSM8K：8K 行 × 4 轮次（带工具使用的数学题）
     - SimpleSpelling：200K 行（拼写单词 'apple'）
     - SpellingBee：80K 行（'strawberry' 中有多少个 'r'）

  c) BOS 对齐打包（bestfit）：
     - 使用最佳适应算法将对话打包成固定长度行
     - 不丢弃 token（用带掩码的目标填充代替）
     - 每行以 BOS 开头

  d) 工具使用支持：
     - tokenizer 包含 <|python_start|> <|python_end|> <|output_start|> <|output_end|> 这些 token
     - GSM8K 训练模型调用 Python 计算器工具
     - 推理时，Engine 实际计算 Python 表达式并反馈结果

  e) SFT 期间的 ChatCORE 评估：
     - 每 N 步运行 6 个基准测试：ARC-Easy、ARC-Challenge、MMLU、GSM8K、HumanEval、SpellingBee
     - ChatCORE = 均值中心化准确率（相对于随机基线归一化）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. RL —— 强化学习（chat_rl.py）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT 没有 RL。nanochat 在 GSM8K 上实现了一个简化的 GRPO/REINFORCE：

流水线：

  1. 加载 SFT 模型
  2. 对于每个 GSM8K 问题：
     - 从模型生成 N=16 个样本
     - 检查每个样本与标准答案
     - 奖励：正确为 1，错误为 0
  3. 计算优势：reward - mean_reward（不是 z-score，仅减去均值）
  4. 策略梯度：loss = -sum(logp * advantage) / num_valid_tokens
  5. 无 KL 惩罚，无 PPO ratio/clip——纯在策略 REINFORCE

为何称为“受 GRPO 启发”但简化：

- 无信任区域 / 对参考模型的 KL 散度
- 在策略（无需 PPO ratio + clip）
- DAPO 风格的 token 级归一化
- 优势 = (r - mu) 而非 (r - mu)/sigma

跟踪 pass@k 指标：k 个样本中至少有一个正确的概率。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. 推理引擎（engine.py）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT：基本的 generate() 函数，裁剪到 block_size，无缓存。

nanochat：完整的推理引擎，包含：

- KV 缓存（原生 FA3，预分配张量）
- Prefill：batch=1 的提示前向传播，然后为 N 个样本复制缓存
- 工具使用状态机：检测 <|python_start|>，计算表达式，注入结果
- 多样本生成（并行生成 N 个补全）
- 流式输出（每步返回 token_column, token_masks）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. 评估套件（tasks/ + core_eval.py + chat_eval.py）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT：仅在 OpenWebText 上计算验证损失。

nanochat 包含 8 个评估任务：

  分类（基于 logit，速度快）：
    - ARC-Easy / ARC-Challenge（科学推理，4 选 1）
    - MMLU（57 个学科，4 选 1）

  生成（采样 + 检查）：
    - GSM8K（数学应用题）
    - HumanEval（Python 代码生成）
    - SpellingBee（字母计数）
    - SimpleSpelling（单词拼写）

  预训练指标：
    - DCLM CORE 分数（基于 5 个任务的困惑度）
    - val_bpb（每字节比特数，与词汇表大小无关）

  ChatCORE：所有 6 个聊天评估任务的复合指标，相对于随机基线中心化。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. 分词器（tokenizer.py）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT：使用 tiktoken（GPT-2 编码）或训练字符级分词器。无特殊 token。

nanochat：自定义 BPE 分词器（训练用 RustBPE，推理用 tiktoken）：

- 32K 词汇表（可配置）
- 9 个特殊 token：<|bos|>、<|user_start|>、<|user_end|>、<|assistant_start|>、<|assistant_end|>、<|python_start|>、<|python_end|>、<|output_start|>、<|output_end|>
- render_conversation() 方法：将聊天消息转换为 token ID + 损失掩码
- render_for_completion()：为 RL 生成移除最后一条助手消息
- visualize_tokenization()：带颜色编码输出的调试助手

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. 其他基础设施
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- 检查点管理器：保存/加载模型 + 优化器 + 每个阶段的元数据（base/sft/rl）
- MLflow 记录器：wandb 的实验跟踪替代方案
- 缩放定律支持：miniseries.sh、scaling_laws.sh、--depth 作为单一控制参数
- 报告系统：评估结果的结构化日志
- 聊天 UI：基于网页的类 ChatGPT 界面（scripts/chat_web.py）
- 聊天 CLI：终端聊天界面（scripts/chat_cli.py）
- 分布式训练：带 Gloo 补丁的 proper DDP
- compute_init/cleanup：设备检测、分布式设置

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  总结：完整的 LLM 流水线
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT 覆盖：
  [预训练] → [生成文本]

nanochat 覆盖：
  [训练分词器] → [预训练] → [评估 CORE] → [对话 SFT] →
  [数学任务 RL] → [评估 ChatCORE] → [通过聊天 UI 提供服务]

最重要的概念新增功能：

  1. SFT：通过对话微调将基础模型训练成聊天助手
  2. RL：通过基于奖励的策略梯度改进数学/工具使用能力
  3. 工具使用：模型可以调用 Python 计算器并获得结果反馈
  4. 完整评估套件：6+ 个基准测试，附带复合指标（ChatCORE）
  5. 现代架构：RoPE、GQA、滑动窗口、值残差、ReLU²、Muon 优化器
