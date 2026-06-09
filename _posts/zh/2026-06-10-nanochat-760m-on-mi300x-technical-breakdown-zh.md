---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NanoChat 760M 在 MI300X 上的技术详解
translated: true
type: note
---

以下是每个决策的完整技术分解：

============================================================
  综合摘要：NANOCCHAT 760M 在 MI300X 上的运行
============================================================

1. 环境发现
============================================================

首先，我探索了系统以了解我们正在使用的环境：

  主机：       snapshots-gpu-mi300x-192gb-devcloud-atl1 (DigitalOcean GPU 实例)
  操作系统：   Ubuntu 24.04.4 LTS
  CPU：        Intel Xeon Platinum 8568Y+ (20 核, QEMU 虚拟机)
  内存：       235 GB
  GPU：        AMD Instinct MI300X (192 GB 显存, gfx942)
  ROCm：       7.2.0 安装于 /opt/rocm-7.2.0
  PyTorch：    2.9.1+rocm6.4 (系统级，预装)

在磁盘上发现已有项目：
  /root/llama.cpp/    - 为 MI300X 使用 ROCm HIP 构建，服务于 Qwen 122B
  /root/nanoGPT/      - 训练了 GPT-2 760M (在 MI300X 上达到 108-113% MFU)
  /root/zz/           - 训练流程，包含日志和推理审计
  /root/nanochat/     - 新克隆，尚未设置

nanoGPT 760M 训练日志显示：
  - depth=24, n_head=24, n_embd=1536
  - 在 MI300X 上 MFU 为 108-113% (使用 nanoGPT 的自定义 CUDA 内核)
  - 第 29K 步时验证损失约为 3.27
  - 在 FineWeb 数据集上训练

============================================================

2. NANOCCHAT 与 NANOGPT 对比 - 为何选择 NANOCCHAT
============================================================

nanochat 是 Karpathy 对 nanoGPT 的继任者 (于 2025 年 11 月弃用)。
主要区别：

  nanoGPT:                     nanochat:
  - 简单的 300 行 train.py     - 全栈：分词器、预训练、
  - GPT-2 架构                    SFT、评估、聊天 UI、网页 UI
  - 手动超参数                 - 从单个 --depth 参数自动缩放所有超参数
  - 无内置评估                 - 使用 PyTorch SDPA/FA3 (可移植)
  - 自定义 CUDA 内核           - 在 MI300X 上 MFU 为 27% (SDPA 回退)
  - 在 MI300X 上 MFU 为 108-113%

nanochat 用原始内核效率换取了完整的流程。
MFU 较低是因为它使用 PyTorch 的 SDPA 而不是手写 CUDA 内核，
但你可以开箱即用地获得分词器训练、评估、SFT 和聊天 UI。

============================================================

3. 闪存注意力决策
============================================================

这是一个关键架构决策。以下是完整说明：

FLASH ATTENTION 3 (FA3):
  - 通过 'kernels' 包在 nanochat 中可用
  - 需要 Hopper GPU (SM 90) - 仅限 NVIDIA H100/H200
  - nanochat/flash_attention.py 中的检测代码：
      if major != 9:  # 检查 SM 能力
          return None  # 回退到 SDPA
  - MI300X 通过 ROCm 报告 SM 94，但 FA3 内核
    仅为 NVIDIA SM 90 编译 - 它们无法在 AMD 上运行

FLASH ATTENTION 2:
  - flash-attn 包 (由 Tri Dao 开发) 有 ROCm 支持
    但未安装且不易构建
  - 需要：使用 ROCm 编译的 pip install flash-attn
  - 在 ROCm 7.2 上存在构建失败的风险

我们使用的替代方案 - PyTorch SDPA:
  - PyTorch 的 scaled_dot_product_attention 是回退方案
  - 它会调度到最佳可用后端：
    * cuDNN/hipDNN 注意力 (如果可用)
    * 内存高效注意力 (如果可用)
    * 数学实现 (回退)
  - 在 ROCm 上，它通常使用数学实现
  - 这就是 MFU 为 27% 而不是 50-60% 的原因

对训练的影响：
  - SDPA 不支持滑动窗口注意力
  - 这就是我们使用 --window-pattern L (全注意力) 的原因
  - 使用 FA3，我们可以使用 "SSSL" 模式 (3/4 滑动窗口)
    从而节省 4 层中 3 层的计算量
  - 全注意力每个 token 使用更多 FLOPs，因此 MFU 较低
  - 但在 AMD 上能正确且可靠地工作

如何改进：
  选项 A：为 ROCm 安装 flash-attn (有风险，可能无法编译)
  选项 B：等待 ROCm 原生闪存注意力 (AMD 正在开发)
  选项 C：使用来自 ROCm 的可组合内核 (CK) 闪存注意力
  选项 D：接受 27% 的 MFU 并训练更长时间 (约 62 小时 vs 约 20 小时)

为了可靠性，我们选择了选项 D。MI300X 拥有 192 GB 显存，
因此我们不受内存限制 - 我们受限于 SDPA 的计算能力。

============================================================

4. 模型架构决策
============================================================

目标：GPT-2 760M (匹配 nanoGPT 运行)

nanochat 从 --depth 自动缩放所有内容：
  --depth=24 (transformer 层数)
  --aspect-ratio=64 (默认，控制宽度)
  --head-dim=128 (默认，注意力头大小)

计算：
  model_dim = depth × aspect_ratio = 24 × 64 = 1536
  n_heads   = model_dim / head_dim = 1536 / 128 = 12
  n_layers  = depth = 24
  ffn_dim   = 4 × model_dim = 6144

得到：
  n_layer=24, n_head=12, n_kv_head=12, n_embd=1536

注意：原始 nanoGPT 760M 使用 n_head=24 (head_dim=64)，
但 nanochat 默认使用 head_dim=128。总参数量相似，因为：
  - 更少的头 (12 vs 24) 但更大的 head_dim (128 vs 64)
  - 相同的总注意力维度：12×128 = 24×64 = 1536

参数分解：
  wte (词嵌入)：                50,331,648  (32768 词汇表 × 1536 维度)
  value_embeds：                603,979,776  (nanochat 创新)
  lm_head (输出投影)：          50,331,648
  transformer_matrices：        679,478,976  (实际的 GPT 层)
  scalars：                            74    (resid_lambdas, x0_lambdas)
  总计：                     1,384,122,122  (~1.38B)

"value_embeds" 是 nanochat 特有的功能：
  - 每隔一层有一个值嵌入 (类似于 RETRO)
  - 增加了 nanoGPT 没有的约 604M 参数
  - "transformer_matrices" (679M) 更接近 760M 目标
  - 这就是总参数为 1.38B 而不是 760M 的原因

============================================================

5. 超参数决策
============================================================

A. 批次大小：每步 524,288 个 token

  我如何选择：
  - depth=20 的 nanochat 默认值为 524,288
  - 这是 256 个序列 × 每个序列 2048 个 token
  - 对于 500M-1B 范围内的模型是标准配置
  - 匹配 nanoGPT 760M 使用的值

  在 MI300X 上的分解：
  - device_batch_size=32 (每次 GPU 前向传递 32 个序列)
  - 每个微批次的 token 数：32 × 2048 = 65,536
  - 梯度累积步数：524,288 / 65,536 = 8
  - 每一步 = 8 次前向+反向传递，然后 1 次优化器步骤

B. 序列长度：2048

  - nanochat 默认值，上下文与内存的良好平衡
  - 更长的序列 (4096) 会使用更多每个微批次的显存
  - MI300X 可以处理 4096，但 2048 是标准
  - 匹配 GPT-2 的原始上下文长度

C. 窗口模式：L (全注意力)

  - FA3 支持 "SSSL" (在 3/4 层上滑动窗口)
  - SDPA 不支持滑动窗口注意力
  - 必须使用 "L" (所有层上的全注意力)
  - 这意味着每一层都进行完整的 O(n²) 注意力计算
  - 每个 token 计算量更大，但更简单且正确

D. 迭代次数：29,000

  Chinchilla 最优缩放：
  - Chinchilla 论文指出：最优 token 数 = 20 × 参数量
  - 我们的模型：760M 参数 (transformer 矩阵)
  - 目标 token 数：20 × 760M = 15.2B token
  - 所需步数：15.2B / 524,288 = 29,000 步

  这与 nanoGPT 运行相匹配：
  - nanoGPT 760M 以相似的批次大小训练到约 29K 步
  - 此时达到验证损失约 3.27

E. 学习率 (由 nanochat 自动缩放)：

  - embedding_lr: 0.3 (默认)
  - unembedding_lr: 0.008 (默认)
  - matrix_lr: 0.02 (用于权重的 Muon 优化器)
  - scalar_lr: 0.5 (用于 resid_lambdas, x0_lambdas)
  - weight_decay: 0.28 (为 depth 24 缩放)

  nanochat 自动调整：
  - 权重衰减缩放：0.28 × (24/160) ≈ 0.042 对于 depth 24
  - Adam 学习率缩放：1/√(1536/768) = 0.707 对于更大模型

F. 评估设置：

  - eval_every=1000 (每 1000 步验证损失)
  - eval_tokens=1,048,576 (用于验证损失估计的 2M token)
  - core_metric_every=5000 (每 5K 步 DCLM CORE 基准测试)
  - sample_every=5000 (每 5K 步生成文本样本)
  - save_every=5000 (每 5K 步检查点)

============================================================

6. 训练速度分析
============================================================

测量性能：
  第一步 (编译)：  17.5 秒 (JIT 预热)
  后续步骤：         约 7.7 秒每个
  吞吐量：          约 68,000 token/秒
  MFU：             约 27.5% (bf16)
  峰值显存：         105 GB / 192 GB (55%)

时间估计：
  29,000 步 × 7.7 秒/步 = 223,300 秒
  = 3,722 分钟 = 62 小时 ≈ 2.6 天

为什么 MFU 是 27% (不是 50%+)：
  1. SDPA 回退 (无融合注意力内核)
     - H100 上的 FA3：融合、向量化、流水线化
     - MI300X 上的 SDPA：单独的矩阵乘法 + softmax + dropout
  2. 值嵌入增加了约 604M 额外参数
     - 嵌入查找需要更多内存带宽
     - 计算密集度不如纯矩阵乘法
  3. 梯度累积 (8 个微批次)
     - 每个微批次都有内核启动开销
     - 开销 × 8 = 显著时间
  4. 模型对于 GPU 来说较小
     - 760M 参数在 192 GB GPU 上 = 未充分利用
     - 更大的模型 (7B+) 会获得更好的 MFU

与 NANOGPT 的比较：
  同一 MI300X 上的 nanoGPT 760M：108-113% MFU
  同一 MI300X 上的 nanochat 760M：27.5% MFU

  区别在于：
  - nanoGPT 使用自定义 CUDA 内核 (手工调优)
  - nanochat 使用 PyTorch SDPA (可移植但较慢)
  - nanoGPT 没有值嵌入 (更简单)
  - nanochat 有完整流程 (分词器、评估、聊天)

  如果你需要原始速度：使用 nanoGPT
  如果你需要完整流程：使用 nanochat

============================================================

7. ROCm 特定注意事项
============================================================

设置的环境变量：
  HIP_FORCE_DEV_KERNARG=1
    - 强制 HIP 在设备内存中使用内核参数
    - 在某些 ROCm 版本上可以提高性能

  HSA_OVERRIDE_GFX_VERSION=9.4.2
    - 告诉 HIP/HSA 使用 gfx942 目标 (MI300X)
    - 确保使用正确的 ISA

  PYTORCH_ALLOC_CONF=expandable_segments:True
    - PyTorch 内存分配器使用可扩展段
    - 减少大分配的内存碎片

FP8 训练：
  - 已检查：torch._scaled_mm 存在，float8_e4m3fn 存在
  - 但是："Float8_e4m3fn 仅支持 ROCm 6.5 及以上版本"
  - 我们有 ROCm 7.2，但 PyTorch 是针对 ROCm 6.4 构建的
  - 因此 FP8 不可用
  - 使用 FP8，我们可以获得约 2 倍的吞吐量 (类似于 H100 FP8)
  - 需要构建支持 ROCm 7.2 的 PyTorch

DDP (分布式数据并行)：
  - 单 GPU，因此不使用 DDP
  - 如果多 GPU：需要 backend="nccl" (ROCm 有 NCCL)
  - 代码检查 RANK/WORLD_SIZE 环境变量

编译：
  - nanochat 内部使用 torch.compile
  - 由于 JIT 编译，第一步很慢 (17.5 秒)
  - 后续步骤受益于编译后的内核
  - ROCm 的 torch.compile 可以工作，但可能生成次优代码

============================================================

8. 数据流程
============================================================

数据集：ClimbMix-400B
  - URL：huggingface.co/datasets/karpathy/climbmix-400b-shuffle
  - 格式：Parquet 分片 (每个约 810M token)
  - 我们下载了 30 个训练分片 + 1 个验证分片 = 总共 31 个
  - 约 25B token 可用 (超过所需的 15.2B)

分词器：BPE (字节对编码)
  - 在 ClimbMix 数据上训练
  - 词汇表大小：32,768
  - 训练时间：49.77 秒
  - 保存到：~/.cache/nanochat/tokenizer/

数据加载：
  - nanochat 使用流式数据加载器
  - 即时读取 parquet 文件 (不在内存中加载完整数据集)
  - 支持分布式读取 (DDP 安全)
  - 最后一个分片始终是验证集

============================================================

9. 检查点与监控
============================================================

检查点 (每 5000 步)：
  ~/.cache/nanochat/base_checkpoints/d24/
    model_XXXXX.pt      - 模型权重 (每个约 4 GB)
    optim_XXXXX_rank0.pt - 优化器状态 (每个约 5.7 GB)
    meta_XXXXX.json     - 训练元数据

监控：
  - 训练日志：/root/nanochat/run_mi300x_d24.log
  - MLflow 跟踪 (本地文件存储)
  - 实时指标：损失、学习率、MFU、token/秒

从检查点恢复：
  ./run_mi300x_d24_pretrain.sh --resume-from-step=5000

============================================================

10. 训练后会发生什么
============================================================

完整流程 (run_mi300x_d24.sh) 包括：

步骤 4：基础评估
  - 在 DCLM CORE 基准测试上评估
  - 测量各种任务上的每字节比特数 (bpb)
  - 目标：匹配 GPT-2 CORE 分数 (0.2565)

步骤 5：SFT (监督微调)
  - 下载 identity_conversations.jsonl
  - 在聊天数据上微调基础模型
  - 3000 步，使用较小的批次 (262,144)

步骤 6：聊天评估
  - 在聊天基准测试上测试 SFT 模型

步骤 7：交互式聊天
  python -m scripts.chat_cli -p 'Why is the sky blue?'
  python -m scripts.chat_web  # 本地主机上的网页 UI

============================================================

11. 创建的文件
============================================================

/root/nanochat/run_mi300x_d24.sh
  完整流程：数据 → 分词器 → 预训练 → 评估 → SFT → 聊天

/root/nanochat/run_mi300x_d24_pretrain.sh
  仅预训练 (用于恢复或部分运行)

/root/nanochat/run_mi300x_d24.log
  实时训练日志 (使用 tail -f 监控)

~/.cache/nanochat/base_data_climbmix/
  31 个 parquet 分片 (约 25B token)

~/.cache/nanochat/tokenizer/
  BPE 分词器 (32,768 词汇表)

~/.cache/nanochat/base_checkpoints/d24/
  模型检查点 (每 5K 步)

============================================================

12. 潜在改进
============================================================

加速训练：

  1. 安装 ROCm 闪存注意力
     pip install flash-attn  # 可能需要 ROCm 构建标志
     将启用 --window-pattern SSSL (滑动窗口)
     预期：40-50% MFU (当前为 27%)

  2. 在可用时使用 FP8
     需要构建支持 ROCm 7.2 的 PyTorch
     预期：约 2 倍吞吐量提升

  3. 增加 device_batch_size
     当前：32，使用 105 GB / 192 GB
     可以尝试：48 或 64 (可能因 SDPA 内存而 OOM)
     将减少梯度累积开销

  4. 多 GPU 训练
     torchrun --nproc_per_node=N -m scripts.base_train
     将线性扩展吞吐量

  5. 使用 total_batch_size=1048576
     将步数减半 (14.5K 而不是 29K)
     相同的总 token 数，更少的优化器步骤
     可能略微改变训练动态