---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek-V4-Pro 架构与代码概述
translated: true
type: note
---

以下是完整的说明：

## DeepSeek-V4-Pro 推理代码

位置：~/projects/deepseek-v4-inference/

### 架构（来自 config.json）

DeepSeek-V4-Pro 是一个庞大的混合专家模型：
- 129,280 词表大小，7168 隐藏维度，61 层
- 384 个路由专家，1 个共享专家，每个 token 激活 6 个专家
- 128 个注意力头，512 头维度（含 64 维 RoPE 组件）
- 低秩 Q 投影：q_lora_rank=1536
- 低秩 O 投影：o_lora_rank=1024，16 组
- 滑动窗口注意力（128 tokens）+ KV 压缩（每层不同比率）
- 评分函数：sqrtsoftplus，route_scale=2.5
- 默认量化：FP8 权重 + FP4 专家（UE8M0 缩放格式）
- YaRN 缩放 RoPE 用于长上下文（original_seq_len=65536）

### 文件说明

**model.py**（38K，827 行）——核心文件：
- `ModelArgs` 数据类：所有超参数
- `ParallelEmbedding`：词表分片嵌入，带 all-reduce
- `Linear` / `ColumnParallelLinear` / `RowParallelLinear`：支持 BF16、FP8、FP4 权重格式，带逐块缩放
- `RMSNorm`：标准实现，以 fp32 存储以确保精度
- `precompute_freqs_cis`：YaRN 缩放旋转嵌入
- `Compressor`：可学习的门控池化，用于压缩 KV 缓存（压缩比 4 或 128）。同时处理预填充和增量解码。压缩比为 4 时使用重叠窗口
- `Indexer`：通过可学习评分选择 top-k 压缩 KV 位置，自带 Compressor（使用 Hadamard 旋转 FP4 量化）
- `Attention`：多头潜在注意力（MLA）——低秩 Q（wq_a -> q_norm -> wq_b），滑动窗口 + 压缩 KV，分组低秩 O 投影（wo_a -> wo_b），可学习的 attn_sink 偏置
- `FFNSwiGLU`：标准 SwiGLU，可选 swiglu_limit 截断
- `MOE`：top-k 路由，使用 sqrtsoftplus 评分，共享专家，e_score_correction_bias
- `TransformerBlock`：层类型由 `compress_ratios` 控制——哈希层（压缩比 128）使用 HC 注意力，其他层使用标准 MLA + MoE
- `HCAttention`：哈希压缩注意力——新机制，通过 Sinkhorn 归一化实现多头压缩路由
- `Transformer`：完整模型，包含 `ParallelEmbedding`、层、`RMSNorm`、`lm_head`、KV 缓存管理

**kernel.py**（22K，536 行）—— tilelang JIT 内核：
- `act_quant_kernel`：逐块 FP8 量化（块大小 128），可选的原地量化-反量化
- `fp4_quant_kernel`：逐块 FP4 量化（块大小 32），2 的幂次缩放
- `fp8_gemm_kernel`：FP8 矩阵乘法，逐块 A/B 缩放，L2 交错，4 级流水线
- `fp4_gemm_kernel`：FP8 激活 x FP4 权重 GEMM——加载 FP4，转换为 FP8，分别应用激活（128）和权重（32）缩放
- `sparse_attn_kernel`：FlashAttention 风格的在线 softmax，带索引收集的 top-k KV，可学习 attn_sink
- `hc_split_sinkhorn_kernel`：HC（哈希压缩）路由的 Sinkhorn 归一化——迭代归一化组合矩阵的行/列

**generate.py**（6.1K，155 行）——入口点：
- `sample()`：Gumbel-max 技巧（在 GPU 上比多项式采样更快，避免 CPU 同步）
- `generate()`：批量生成，使用左填充，预填充 + 解码阶段
- 交互模式：聊天循环，支持 `/exit` 和 `/clear` 命令
- 批处理模式：读取由空行分隔的提示
- 多节点：通过 torchrun 使用 NCCL
- 使用来自外部 `encoding` 模块的 `encode_messages` / `parse_message_from_completion_text`（未包含——../encoding/encoding_dsv4.py）

**convert.py**（6.9K，168 行）——权重转换：
- 将 HuggingFace safetensors 转换为模型并行分片
- 将 HF 权重名称映射为内部名称（例如 self_attn -> attn，mlp -> ffn）
- 处理 FP4 到 FP8 的无损转换（e2m1fn 到 e4m3fn），注意缩放处理
- 支持 expert_dtype fp8 或 fp4
- 对 MoE 按专家索引分片，对嵌入/投影按维度分片
- 将分词器文件与权重一起复制

**requirements.txt**：
- torch>=2.10.0，transformers>=5.0.0，safetensors>=0.7.0
- fast_hadamard_transform（用于 Indexer 中的 rotate_activation）
- tilelang==0.1.8（JIT 内核编译器，用于量化和注意力内核）

### 缺失内容

`../encoding/` 目录中的 `encoding_dsv4.py` 未包含——它处理聊天模板编码/解析。你需要从完整仓库中获取它以使用交互模式。

### 硬件需求

使用 FP8+FP4 量化和 384 个专家，这个模型非常庞大。默认配置需要 8 路模型并行（MP=8）。你的 RTX 4070（12GB）即使一个分片也装不下。AMD 开发云上的 MI300X（192GB HBM3）可以处理——可能需要 1-2 张 MI300X 显卡，具体取决于批次大小。