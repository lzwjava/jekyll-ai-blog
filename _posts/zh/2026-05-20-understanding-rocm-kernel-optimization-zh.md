---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解ROCm内核优化
translated: true
type: note
---

我现在对整个代码库有了透彻的理解。以下是全面的概况：

---

ROCm 内核优化：全貌概览

本仓库（/Users/lzwjava/projects/ROCm）是一个元仓库——即通过 Google 的 `repo` 工具管理约 30+ 子项目的清单文件（default.xml）。实际的内核源代码位于各个独立的仓库中（如 llvm-project、composable_kernel、rocm-libraries 等），需要通过 `repo sync` 拉取。以下是根据文档总结的 ROCm 生态系统中内核优化的运作方式：

---

1. 内核编写——选择你的工具

在 ROCm 上编写内核主要有三条路径：

  **HIP (C++)**：原生方式。使用 HIP 的运行时 API 和内核语言编写 C++ 内核。可借助 hipify-clang 移植现有 CUDA 代码。内核通过 AMDGPU LLVM 后端编译为 GCN/RDNA ISA。

  **OpenCL (C)**：跨平台标准。ROCm 支持 AMD GPU 上的 OpenCL 2.0+。

  **Triton (Python)**：用 Python 编写 GPU 内核。Triton 通过 MLIR → LLVM IR → AMDGPU ISA 的编译流程。在 AI 工作负载中越来越流行。文档中有大量关于 Triton 优化的章节（参见 workload.rst 第 1276-1532 行）。

---

2. 内核优化流水线

**第一步：先做性能分析**
────────────────────
永远不要猜测瓶颈在哪里。ROCm 提供了分层的性能分析工具栈：

  PyTorch Profiler          → 高级时间线（导出到 Perfetto UI）
  ROCm Systems Profiler     → CPU+GPU 跟踪、内存、上下文切换
  ROCProfiler (rocprof)     → 原始 GPU 硬件计数器（文本/CSV 输出）
  ROCm Compute Profiler     → 引导式分析：roofline 模型、光速、内存图、基线对比（GUI + CLI）
  ROCr Debug Agent          → 内存故障捕获、wavefront 转储

快速性能分析示例：
  rocprof --stats ./my_kernel_app          # 收集所有计数器
  rocprof --hip-trace ./my_kernel_app      # HIP API 跟踪

**第二步：识别瓶颈**
───────────────────────────
性能术语表（docs/reference/glossary/performance.rst）定义了关键概念：

  Compute-bound   → 内核受算术吞吐量限制（ALU 忙碌）
  Memory-bound    → 内核受 HBM 带宽限制（加载/存储占主导）
  Occupancy       → 活跃 wavefront 数与每个 CU 最大可能数的比值
  Register pressure → VGPR 过多 = 每个 CU 的 wave 减少，隐藏延迟能力下降
  Bank conflicts  → LDS 访问串行化而非并行化
  Wavefront divergence → 同一 wave 内的线程走不同分支

如果 GPU 是瓶颈（而非 CPU/内核启动开销），则进入内核级性能分析。
ROCm Compute Profiler 会多次运行你的内核，收集不同的计数器集合，然后给出 roofline 模型，精确显示你处于哪个位置。

**第三步：自动调优（最简单 → 最费力）**
─────────────────────────────────────────

**Level 1 — 开启自动调优（零代码修改）：**
  # PyTorch TunableOp：从 rocBLAS/hipBLASLt 中尝试数千个 GEMM 内核
  PYTORCH_TUNABLEOP_ENABLED=1 python my_model.py
  # 然后回放最佳配置：
  PYTORCH_TUNABLEOP_ENABLED=1 PYTORCH_TUNABLEOP_TUNING=0 python my_model.py

  # TorchInductor max-autotune：调优 Triton GEMM/卷积 tile 尺寸
  TORCHINDUCTOR_MAX_AUTOTUNE=1 python my_model.py

  # MIOpen autotune：寻找最佳卷积内核
  MIOPEN_FIND_ENFORCE=3 MIOPEN_FIND_MODE=1 python my_model.py

**Level 2 — Composable Kernel (CK) 后端：**
  # 安装 CK Python 包装器，将 CK 加入自动调优后端
  pip install git+https://github.com/rocm/composable_kernel@develop
  TORCHINDUCTOR_MAX_AUTOTUNE_GEMM_BACKENDS="TRITON,CK,ATEN"

**Level 3 — hipBLASLt 手动调优（TensileLite）：**
  # 为获得最大 GEMM 性能，调优汇编后端生成器
  cd hipBLASLt/tensilelite
  ./Tensile/bin/Tensile config.yaml output_path
  # 7 步调优流水线：基准测试常用参数 → fork → join → 最终

**Level 4 — 在 Triton 或 HIP 中编写自定义调优内核：**

  Triton 自动可调参数（关键旋钮）：
    BLOCK_M, BLOCK_N, BLOCK_K    → tile 尺寸（平衡计算与内存）
    num_stages = 2               → 流水线阶段（单 GEMM 设为 2）
    num_warps                    → 每个工作组中的 wave 数（影响 occupancy）
    waves_per_eu                 → 提示编译器减少 VGPR 使用
    matrix_instr_nonkdim = 16    → MFMA 指令尺寸（在 MI300X 上 16x16 优于 32x32）

---

3. 深度内核优化技术

**内存访问优化：**
  - 合并全局内存访问（优先使用 128 字节事务）
  - 最大化利用 LDS（片上共享内存）—— MI300X 上每个 CU 64KB
  - 最小化全局↔LDS 数据传输（使用分块/阻塞）
  - 避免 LDS 中的 bank 冲突（填充共享内存数组）
  - 向量化：使用 global_load_dwordx4（128 位加载）而非标量加载
  - 对于 MI300X GEMM：避免步长为 512 字节的倍数（Tagram 热点问题）

**计算优化：**
  - MI300X：优先使用 mfma_16x16 而非 mfma_32x32（更好的能效）
  - bf16 矩阵运算明显快于 f16
  - 目标 occupancy：网格中至少 1024 个线程块（工作组）
  - MI300X 有 304 个活跃 CU（8 个 XCD × 每个 XCD 38 个活跃 CU）
  - 使用 WorkGroupMapping 为 8 的倍数（XCD 数量）以提高 L2 缓存效率

**Occupancy 计算（workload.rst 第 1643-1690 行）：**
  1. 从 ISA 中找到 .vgpr_count：N
  2. 找到 LDS 分配：从 MLIR 转储中 grep "triton_gpu.shared" → L 字节
  3. 找到 num_warps：从 MLIR 中 grep "triton_gpu.num-warps" → nW
  4. occ_vgpr = 从 VGPR/occupancy 表中查找
  5. occ_lds = floor(65536 / L)
  6. occ = min(floor(occ_vgpr × 4 / nW), occ_lds) × nW / 4

**ISA 汇编分析：**
  - 设置 export AMDGCN_ENABLE_DUMP=1 转储 ISA
  - 检查 global_load_dwordx4（向量化加载）
  - 检查 LDS 加载/存储是否使用 _b128 后缀（减少指令数）
  - 检查 s_waitcnt(lgkmcnt, vmcnt) 的同步效率
  - 重叠指令以隐藏延迟

**MLIR 分析：**
  - 设置 export MLIR_ENABLE_DUMP=1 查看 Triton 中间表示
  - 识别冗余的 LDS 往返（如加载、转置、重新存储）
  - 检查数据布局：blocked → shared → transpose → blocked → dot_op

---

4. 系统级内核优化

  **CU 掩码（docs/how-to/setting-cus.rst）：**
    # 将特定 CU 绑定到特定 GPU
    HSA_CU_MASK="0:0-19;1:20-39" ./my_app  # GPU 0 使用 CU 0-19，GPU 1 使用 20-39
    ROC_GLOBAL_CU_MASK="0:0-15,32-47" ./my_app  # HIP 级掩码

  **多 GPU（RCCL）：**
    - 始终使用全部 8 个 GPU 进行集合通信（MI300X 全连接拓扑）
    - 禁用 NUMA 自动平衡：sudo sysctl kernel.numa_balancing=0
    - 使用每个 GPU 一个进程（避免串行化内核启动）
    - TORCH_NCCL_HIGH_PRIORITY=1 GPU_MAX_HW_QUEUES=2 用于 FSDP
    - 生产工作负载使用 NCCL_MIN_NCHANNELS=112

  **环境变量速查表：**
    PYTORCH_TUNABLEOP_ENABLED=1          自动选择最佳 GEMM 内核
    TORCHINDUCTOR_MAX_AUTOTUNE=1         调优 Triton tile 配置
    TORCHINDUCTOR_FREEZING=1             内联权重、折叠常量（推理）
    MIOPEN_FIND_ENFORCE=3                自动调优 MIOpen 卷积内核
    FLASH_ATTENTION_TRITON_AMD_ENABLE=FALSE   使用 CK 后端进行 Flash Attention
    HSA_DISABLE_FRAGMENT_ALLOCATOR=1     禁用内存缓存（调试）
    AMDGCN_ENABLE_DUMP=1                 转储 ISA 用于分析
    MLIR_ENABLE_DUMP=1                   转储 Triton MLIR IR

---

5. 关键内核库（已优化，优先使用）

  rocBLAS/hipBLASLt  → GEMM（支持后处理：ReLU、GELU、偏置等）
  Composable Kernel  → 基于模板的内核生成（用于 GEMM/卷积）
  MIOpen             → 卷积原语（Winograd、FFT、直接、隐式 GEMM）
  RCCL               → 多 GPU 集合通信（all-reduce、all-gather 等）
  rocWMMA            → wave 矩阵乘累加（张量核心操作）
  rocFFT             → FFT 运算
  rocRAND            → GPU 上的随机数生成
  rocPRIM/rocThrust  → 并行原语（排序、扫描、规约）

---

总结：优化路径为：性能分析 → 识别瓶颈 → 首先尝试自动调优 → 如果仍不够，手动调优 tile 尺寸/occupancy/指令选择 → 如果需要极致性能，深入 ISA/MLIR 分析并编写自定义内核。大多数用户仅通过 TunableOp + TorchInductor max-autotune + Flash Attention 就能获得巨大提升，而无需编写一行内核代码。