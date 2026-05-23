---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 最大化 AMD MI300X 开发者访问权限
translated: true
type: note
---

太好了，恭喜你加入 AMD AI 开发者计划！MI300X 的访问权限确实非常有价值——192GB HBM3 足以在完整精度下运行 70B 模型，或进行重要的微调任务。

以下是如何根据你的发展方向充分利用它的建议：

**立即优先事项：**

1. **快速认领你的积分**——AMD 开发者云积分通常有有效期。立即登录会员网站，截图并保存所有信息。

2. **查看 DeepLearning.AI 的促销活动**——可能有免费访问新课程的机会，例如关于 LLM 微调或基于人类反馈的强化学习。即便不马上使用，也值得先拿下。

**根据你的目标，在 MI300X 上实际该运行什么：**

```bash
# MI300X 基于 ROCm，而非 CUDA——关键区别
# 大多数 PyTorch 代码只需微小改动即可运行：
pip install torch --index-url https://download.pytorch.org/whl/rocm6.0

# 检查 GPU 可见性
rocm-smi
# 对比你 4070 上的 nvidia-smi

# HIP（AMD 的 CUDA 等价物）
hipcc --version
```

**对你 AI 工程发展路线具有高价值的实验：**

```python
# 1. 完整精度 70B 推理——你的 4070（12GB）无法做到
#    MI300X 的 192GB HBM3 原生支持
#    使用 llama.cpp 或 vllm（ROCm 后端）

# 2. 中等规模模型的全微调（非 LoRA）
#    GPT-2 XL、Mistral 7B——无需量化

# 3. ROCm 上的 Flash Attention——与 CUDA 对比性能
#    是 lzwjava.github.io 博客的好素材

# 4. 多 GPU 张量并行实验
#    AMD 云上的 MI300X 通常配备多卡配置
```

**需要提前了解的 ROCm 与 CUDA 差异：**

- `torch.cuda.*` 仍然可用——ROCm 会透明映射
- 自定义 CUDA 内核需要移植到 HIP（使用 `hipify-perl`）
- 某些库支持滞后（例如 bitsandbytes 的 ROCm 支持历史上不稳定）
- 使用 `PYTORCH_HIP_ALLOC_CONF` 而非 `PYTORCH_CUDA_ALLOC_CONF`

**第一次会话我会做的事情：**

```bash
# 基准测试基线——始终了解硬件表现
git clone https://github.com/EleutherAI/lm-evaluation-harness
# 运行一个模型，测量 token/秒，与你的 4070 数据对比
# 这个差值 = HBM3 与 GDDR6X 带宽的故事
```

MI300X 对于个人开发者而言确实是前沿硬件。大多数人只运行推理演示——你应该进行训练运行，并在博客上发布性能数据。这类内容在 AI 工程领域更容易引起关注。