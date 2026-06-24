---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat与nanoGPT对比：关键升级
translated: true
type: note
---

以下是 nanochat 在 nanoGPT 基础上新增的全部内容详解：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  nanochat vs nanoGPT — 新增内容对比
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT 是一个仅用于预训练的框架。它包含：
  - model.py（约 340 行）：标准 GPT-2 架构（LayerNorm、GELU、可学习位置编码、权重绑定、Linear 中的偏置）
  - train.py（约 300 行）：基于原始文本的预训练循环
  - sample.py：基础文本生成
  - 仅此而已。共 2 个 Python 文件。

nanochat 则在一个仓库中实现了完整的 LLM 生命周期。以下是每项重要新增内容：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 模型架构（gpt.py）—— 显著升级
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| 特性                      | nanoGPT                    | nanochat                            |
|---------------------------|----------------------------|-------------------------------------|
| 位置编码                  | 可学习（wpe embedding）     | 旋转位置编码 RoPE — 无 wpe          |
| 归一化                    | LayerNorm（可学习参数）     | RMSNorm（无可学习参数）             |
| 激活函数                  | GELU                       | ReLU²（relu squared）               |
| 注意力                    | 单一组合 c_attn            | 分离的 c_q, c_k, c_v, c_proj       |
| KV 头                     | 仅 MHA                     | 分组查询注意力 GQA                  |
| QK 归一化                 | 无                         | 有（q、k 在 RoPE 后归一化）         |
| 偏置                      | 有（可配置）               | 全无偏置                            |
| 权重绑定                  | 有（wte = lm_head）        | 无 — 解绑嵌入                       |
| Dropout                   | 有                         | 全无 dropout                        |
| Logit 软上限              | 无                         | 有（tanh 软上限在 ±15）             |
| 滑动窗口注意力            | 无                         | 有（每层 SSSL 模式）                |
| 值嵌入 Value Embeddings   | 无                         | ResFormer 风格的值残差               |
| Smear（前一个 token 混合） | 无                         | 门控混合前一个 token 嵌入           |
| Backout（中间层减法）     | 无                         | 在残差流中途减去一部分              |
| 残差缩放                  | 固定                       | 逐层 resid_lambdas + x0             |
| Flash Attention           | PyTorch SDPA               | FA3 → FA2 → SDPA 回退链             |
| KV 缓存                   | 无（基于裁剪）             | 推断时使用 FA3 KV 缓存              |
| FP8 训练                  | 无                         | 动态张量级 FP8（e4m3/e5m2）        |
| 优化器                    | 单一 AdamW                 | MuonAdamW（矩阵用 Muon，            |
|                           |                            | 嵌入/标量用 AdamW）                 |
| 权重初始化                | Normal(0, 0.02)            | 注意力层均匀初始化，投影层零初始化，|
|                           |                            | 显式逐层 resid/x0 初始化            |
| 词表填充                  | 有（填充至 50304）         | 有（填充至最近的 64）               |

关键架构变化说明：

  RoPE vs 可学习位置编码：nanoGPT 为每个位置添加可学习嵌入（wpe）。nanochat 使用旋转位置编码——通过复数空间旋转编码相对位置。具有更好的长度泛化能力。

  ReLU² vs GELU：`F.relu(x).square()` —— 更简单、更快，在此规模下经验性表现相当。无需计算 erf。

  GQA：n_kv_head 可以小于 n_head。例如，6 个查询头但只有 6 个 KV 头（此处相等，但基础设施支持 GQA 比例）。在推断时节省 KV 缓存内存。

  滑动窗口：`SSSL` 模式表示 3 层使用短窗口（1/4 上下文），1 层使用完整上下文。各层间循环。最后一层始终为完整上下文。在大部分层上节省 FLOPs，同时保持长距离能力。

  值残差（ResFormer）：每隔一层都有可学习的每个 token 嵌入（value_embeds），通过门控注入 V 张量。`v = v + gate * ve`。交替层，最后一层始终包含。

  Smear：通过可学习门控将前一个 token 的嵌入混合到当前 token。在嵌入层实现廉价的二元语法信息流。`x = x + sigmoid(gate(x)) * x_prev`

  Backout：在中间层缓存残差流。在最终归一化之前，减去 `lambda * x_backout` 以在对数投影前移除低级特征。

  Muon 优化器：矩阵参数使用 Muon（动量 + Newton-Schulz 正交化），嵌入参数使用 AdamW。按参数组分别设置学习率调度。对于大型矩阵参数效率更高。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. SFT —— 监督微调（chat_sft.py）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT 没有 SFT。nanochat 包含完整的 SFT 流程：

SFT 的作用：
  基于预训练的基础模型，在对话（用户/助手对）上进行微调，使其学会遵循指令并进行聊天。

在 nanochat 中的工作方式：

  a) 对话渲染（tokenizer.render_conversation）：
     - 对话使用特殊 token 进行分词：
       <|bos|> <|user_start|> ... <|user_end|> <|assistant_start|> ... <|assistant_end|>
     - 生成损失掩码：仅对助手 token 设置 mask=1
     - 用户提示、BOS、特殊 token 设置 mask=0（不参与训练）

  b) 数据混合（TaskMixture）：
     - SmolTalk：46 万行通用对话
     - CustomJSON：1000 条合成身份对话（"你是谁？" "我是 nanochat..."）
     - MMLU：10 万行 × 3 个 epoch（多项选择知识）
     - GSM8K：8000 行 × 4 个 epoch（使用工具的数学题）
     - SimpleSpelling：20 万行（拼写单词 'apple'）
     - SpellingBee：8 万行（'strawberry' 中有几个 'r'？）

  c) 基于 BOS 对齐的打包（bestfit）：
     - 使用最佳适应算法将对话打包成固定长度行
     - 不丢弃任何 token（用掩码目标填充）
     - 每行以 BOS 开头

  d) 工具使用支持：
     - 分词器包含 <|python_start|> <|python_end|> <|output_start|> <|output_end|> 等 token
     - GSM8K 训练模型调用 Python 计算器工具
     - 推断时，Engine 实际执行 Python 表达式并将结果反馈给模型

  e) SFT 期间的 ChatCORE 评估：
     - 每 N 步运行 6 个基准测试：ARC-Easy、ARC-Challenge、MMLU、GSM8K、HumanEval、SpellingBee
     - ChatCORE = 平均中心化准确率（相对于随机基线归一化）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. RL —— 强化学习（chat_rl.py）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT 没有 RL。nanochat 在 GSM8K 上实现了简化的 GRPO/REINFORCE：

流程：
  1. 加载 SFT 模型
  2. 对于每个 GSM8K 问题：
     - 从模型生成 N=16 个样本
     - 检查每个样本与真实答案是否匹配
     - 正确则奖励 = 1，错误则奖励 = 0
  3. 计算优势：奖励 - 平均奖励（不取 z-score，仅减去均值）
  4. 策略梯度：loss = -sum(logp * advantage) / num_valid_tokens
  5. 无 KL 惩罚，无 PPO 比率/裁剪——纯 on-policy REINFORCE

使其“受 GRPO 启发但简化”的原因：
  - 无信任区域 / 与参考模型的 KL 散度
  - On-policy（无需 PPO 比率 + 裁剪）
  - DAPO 风格 token 级别归一化
  - 优势 = (r - mu) 而非 (r - mu)/sigma

跟踪 pass@k 指标：k 个样本中至少有一个正确的概率。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. 推断引擎（engine.py）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT：基础 generate() 函数，裁剪至 block_size，无缓存。

nanochat：完整的推断引擎，包含：
  - KV 缓存（FA3 原生，预分配张量）
  - Prefill：batch=1 的提示前向传播，然后复制缓存用于 N 个样本
  - 工具使用状态机：检测 <|python_start|>，执行表达式，注入结果
  - 多样本生成（并行生成 N 个补全）
  - 流式输出（每步返回 token_column, token_masks）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. 评估套件（tasks/ + core_eval.py + chat_eval.py）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT：仅在 OpenWebText 上计算验证损失。

nanochat 包含 8 个评估任务：

  分类任务（基于 logit，快速）：
    - ARC-Easy / ARC-Challenge（科学推理，4 选 1）
    - MMLU（57 个学科，4 选 1）

  生成式任务（采样 + 检查）：
    - GSM8K（数学应用题）
    - HumanEval（Python 代码生成）
    - SpellingBee（字母计数）
    - SimpleSpelling（单词拼写）

  预训练指标：
    - DCLM CORE 分数（基于 5 个任务的困惑度）
    - val_bpb（每字节比特数，与词表大小无关）

  ChatCORE：涵盖所有 6 个聊天评估任务的复合指标，相对于随机基线中心化。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. 分词器（tokenizer.py）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT：使用 tiktoken（GPT-2 编码）或训练字符级分词器。无特殊 token。

nanochat：自定义 BPE 分词器（训练用 RustBPE，推断用 tiktoken）：
  - 32K 词表（可配置）
  - 8 个特殊 token：<|bos|>, <|user_start|>, <|user_end|>, <|assistant_start|>, <|assistant_end|>, <|python_start|>, <|python_end|>, <|output_start|>, <|output_end|>
  - render_conversation() 方法：将聊天消息转换为 token ID 和损失掩码
  - render_for_completion()：为 RL 生成去掉最后助手消息
  - visualize_tokenization()：带颜色编码的调试辅助工具

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. 其他基础设施
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  - 检查点管理器：按阶段（base/sft/rl）保存/加载模型 + 优化器 + 元数据
  - MLflow 日志记录器：wandb 的实验跟踪替代方案
  - 缩放定律支持：miniseries.sh, scaling_laws.sh, --depth 作为单一旋钮
  - 报告系统：评估结果的结构化日志
  - 聊天 UI：基于 Web 的类 ChatGPT 界面（scripts/chat_web.py）
  - 聊天 CLI：终端聊天界面（scripts/chat_cli.py）
  - 分布式训练：带有 Gloo 补丁的完整 DDP
  - compute_init/cleanup：设备检测、分布式设置

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  总结：完整 LLM 流程
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT 涵盖：
  [预训练] → [生成文本]

nanochat 涵盖：
  [训练分词器] → [预训练] → [评估 CORE] → [对话 SFT] →
  [数学任务 RL] → [评估 ChatCORE] → [通过聊天 UI 提供服务]

最重要的概念性新增内容：
  1. SFT：通过对话微调将基础模型训练成聊天助手
  2. RL：通过基于奖励的策略梯度提高数学/工具使用能力
  3. 工具使用：模型可以调用 Python 计算器并获取结果反馈
  4. 完整评估套件：6 个以上基准测试，配备复合指标 ChatCORE
  5. 现代架构：RoPE、GQA、滑动窗口、值残差、ReLU²、Muon 优化器