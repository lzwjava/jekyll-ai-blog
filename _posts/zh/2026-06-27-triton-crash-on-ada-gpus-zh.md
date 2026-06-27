---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Triton在Ada GPU上崩溃
translated: true
type: note
---

**发生了什么：**

1. 在工作站（lzw@192.168.1.36，RTX 4070）上使用 Qwen/Qwen2.5-1.5B-Instruct 启动了 sglang
2. Triton 3.5.1 在 JIT 期间发生段错误 —— 先在图捕获时出现，后在推理阶段再次出现
3. 尝试 `--attention-backend torch_native --disable-cuda-graph` —— 仍然崩溃，且 sglang 消耗了大量资源导致 SSH 连接断开
4. 尝试降级 Triton 到 3.4.0 —— pip 依赖解析将其自动回退到 3.6.0
5. 当前安装版本：torch 2.11.0+cu130、triton 3.6.0、sglang 0.5.9、驱动 580.126.20（CUDA 13.0）

**根本原因：**

Triton 3.5/3.6 的 JIT 编译在 CUDA 13.0 + 消费级 Ada 架构（sm_89）上崩溃。段错误发生在 Triton 的编译器流水线（MLIR → LLVM → PTX → ptxas）中，而非 GPU 计算过程。数据中心 GPU（H100/A100）已事先验证通过，消费级显卡遇到的是边界错误。硬件本身完全具备能力——纯属工具链不兼容问题。

**为何简单修复方案无效：**

- `--attention-backend torch_native` —— sglang 流水线中仍有地方会触发 Triton
- `pip install triton==3.4.0` —— torch 2.11.0 要求 triton>=3.5，pip 会再次升级
- `--no-deps` 固定版本 —— torch 可能在运行时拒绝更低版本的 triton

**建议修复方案：**

使用 CUDA 12.4 版 wheel 创建新的 Python 虚拟环境：torch 2.5.1+cu124 + triton 3.1.0。这是已知在 Ada GPU 上稳定的组合。驱动 580.x 向后兼容 CUDA 12.4。安装与该 torch 版本兼容的 sglang 0.4.x。

**替代方案：** 在新虚拟环境中使用 vLLM——它自带已验证的 torch+triton+cuda 版本绑定，可减少手动版本管理。

**状态：** 已完成分析，尚未采取行动。等待您决策采用哪种方案。