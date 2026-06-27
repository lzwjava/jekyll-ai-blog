---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CUDA 12.4修复路径
translated: true
type: note
---

工作站当前堆栈：

```
Driver:   580.126.20  (支持 CUDA 12.0–13.0)
torch:    2.11.0+cu130
triton:   3.6.0
sglang:   0.5.9
Python:   3.11 (虚拟环境中无 pip)
GPU:      RTX 4070 (sm_89, Ada Lovelace)
```

问题链条：`torch 2.11.0` 固定了 `triton>=3.5`，而 Triton 3.5/3.6 的 JIT 在 CUDA 13.0 和 sm_89 上会崩溃。不使用 `--no-deps` 无法降级 triton，即使降级，torch 也可能在运行时拒绝它。

三种修复方案，按优先级排列：

```
1. 最干净 —— 使用 CUDA 12.4 轮子创建新虚拟环境：
   Driver 580.x 向后兼容 CUDA 12.x。
   torch 2.5.1+cu124 + triton 3.1.0 = 在 Ada 上已知稳定。
   sglang 0.4.x 与该组合兼容。

2. 最快 —— 在现有虚拟环境中安装 vLLM：
   pip install vllm — 它会自带经过验证的堆栈。
   但可能与现有 sglang 依赖项冲突。

3. 有风险 —— 使用 --no-deps 固定 triton 版本：
   pip install --no-deps triton==3.4.0
   Torch 可能在运行时拒绝它。不稳定。
```

方案一最可靠。需要我在工作站上设置一个带有 cu124 轮子的新虚拟环境吗？
