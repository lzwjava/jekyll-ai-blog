---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 三个独立约束的碰撞
translated: true
type: note
---

原因归结为三个相互独立的约束发生了冲突，而不是单一因素。

**1. sglang 对 torch 的硬性固定。** sglang 0.4.x 并非宽松地依赖 torch——它固定到特定的构建版本，因为它附带了针对特定 torch C++ ABI 和 CUDA 版本编译的自定义内核（flashinfer、其自有的 attention/sampling 操作）。Torch 的 C++ ABI（`libtorch`）在小版本之间不稳定；针对 2.5.1 头文件编译的内核 `.so` 在加载到 2.7.1 时会出现符号/ABI 不匹配，反之亦然。因此，“torch 2.5.1+cu124”不是你可以随意覆盖的建议——而是 sglang 预编译 wheel 所期望的版本，而原本计划的组合根本不是 sglang 0.4.x 实际构建所针对的那个。

**2. triton 由 torch 间接固定，不能自由选择。** 每个 torch 发行版都附带了经过测试/编译的特定 triton 版本（torch 在其自身的依赖元数据中硬编码了 triton）：

- torch 2.5.x → triton 3.1.0
- torch 2.7.x → triton 3.3.x

triton 负责在运行时编译融合内核（由 `torch.compile`、flashinfer 和 sglang 自身操作使用的 `@triton.jit` GPU 代码生成路径）。如果 triton 的代码生成、PTX/ABI 期望或指针算术语义偏离了 torch 和内核所假设的内容，就会得到编译错误的内核——这表现为 **段错误**，而不是干净的 Python 异常，因为失败发生在 Python 层之下的生成的 GPU/主机代码中。因此你不能混搭：triton 3.3.1 属于 torch 2.7.x 系列，在 2.7.1 下强制使用 3.1.0（或者在此栈中任何位置使用 3.5/3.6）会破坏约定。

**3. CUDA 标签（cu124 vs cu126）是第三个轴。** `+cu124` / `+cu126` 后缀表示 torch wheel 是针对哪个 CUDA 工具包构建的。flashinfer/sglang 的预编译 wheel 也带有 CUDA 版本标签。cu124 torch + 基于 cu126 构建的 sglang 内核 = CUDA 运行时符号不匹配。它们必须全部一致。

**为什么 3.3.1 特别有效：** 它是 torch 2.7.1 自带的 triton，因此 torch↔triton ABI 契约自然得到满足。而且它早于 triton 3.5/3.6 系列，后者引入了 flashinfer/sglang 0.4.x 内核未曾针对其构建或测试的代码生成/IR 更改——这些更改正是你之前遇到的段错误的来源。因此 3.3.1 是个最佳点：足够新，是 sglang 0.4.x 实际所需的 torch 版本的匹配伙伴；足够旧，仍处于内核兼容窗口内。

思维模型：**sglang 选择 torch，torch 选择 triton，CUDA 标签必须三者匹配。** 你没有三个自由变量——只有一个（sglang 版本），其他一切都是确定的。最初计划之所以失败，是因为它把 torch/triton/cuda 当作可独立选择的变量，而实际上它们是由 sglang 0.4.x 编译所针对的单一锁定元组决定的。

如果你想验证确切的固定版本，而不是凭经验相信当前有效的组合，真实依据在 sglang 的 `pyproject.toml` / `setup.py` 中（针对 0.4.x 标签）以及 torch 自身的 `setup.py` 中的 triton 固定——值得 grep 一下来确认，以免下次升级时再通过段错误来重新发现。
