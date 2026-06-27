---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 可靠硬件，破碎工具链
translated: true
type: note
---

完全正确。

RTX 4070 上的 Ada 核心（sm_89）运行 FP16/BF16 注意力机制和矩阵乘法内核时毫无问题——它与 vLLM/SGLang 在生产环境中使用的架构类别相同。硬件层面没有任何限制。

失败纯粹出在工具链层面：Triton 的 JIT 编译器将你的内核通过 `triton.compile` → LLVM → PTX → `ptxas`（CUDA 13.0 的汇编器）→ SASS 进行降级。那里的段错误是编译器崩溃，而非 GPU 故障。你可以通过以下命令确认具体阶段：

```bash
TRITON_DEBUG=1 python -c "import torch; ..." 2>&1 | tail -40
# 或捕获 IR 转储
MLIR_ENABLE_DUMP=1 TRITON_KERNEL_DUMP=1 python your_script.py
```

如果在 SASS 生成之前就崩溃，那是 Triton 的 MLIR/LLVM 阶段的问题。如果崩溃发生在 `ptxas` 中，则是 CUDA 13.0 汇编器在处理 Triton 生成的 PTX 时出错。不管是哪种情况：都是软件问题。

关于“纯粹是软件问题”的一点补充——Triton/CUDA 版本矩阵首先针对数据中心 SKU（H100/A100）进行验证。消费级 Ada 获得的覆盖测试较少，因此你会遇到大型硬件不会出现的边界错误。硬件本身是具备能力的；只是测试过的支持表面在消费级显卡上有所滞后。从功能上讲，这仍然是一个可以通过固定版本来解决的软件栈问题，而非 RTX 4070 的限制。

在 RTX 4070 上搭建可用栈的最快路径：

```bash
# 方案 A：使用已知稳定的 CUDA 12.4 轮子，完全跳过 CUDA 13
pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu124
pip install triton==3.1.0   # 3.1.x 版本在 cu124 + Ada 上稳定

# 方案 B：使用 vLLM，它自带经过验证的 torch+triton+cuda 版本锁定
pip install vllm   # 让它为你解析整个依赖矩阵
```

vLLM 是更简洁的路径，正是因为它冻结了一个经过冒烟测试的 triton/torch/cuda 组合，而不是让你与 pip 的解析器搏斗来维持一个运行时会撤销的降级版本。