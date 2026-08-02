---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 机器学习虚拟环境的磁盘空间成本
translated: true
type: note
---

问题：具体到AI/ML工作，由于torch体积巨大，虚拟环境会占用大量磁盘空间吗？

回答：是的——torch + CUDA才是真正的体积驱动因素，而非虚拟环境机制。具体数据：

```bash
# 包含捆绑CUDA库的torch
pip install torch  # 约2.5-3GB（CUDA 12.x的wheel捆绑了cudnn、cublas、nccl等）

# 检查实际占用空间的内容
du -sh $(python -c "import torch,os; print(os.path.dirname(torch.__file__))")
du -sh $(python -c "import torch,os; print(os.path.dirname(torch.__file__))")/lib/*.so*
```

用于LLM工作的完整技术栈会迅速增加体积：

| 包 | 大小 |
|---|---|
| torch (cuda) | 约2.5-3GB |
| transformers | 约50-100MB |
| flash-attn (编译后) | 约500MB-1GB构建产物 |
| vllm | 约1-2GB（自带torch + CUDA依赖） |
| deepspeed | 约200MB + 编译后的算子 |
| datasets/tokenizers | 约50MB |

一个用于完整微调技术栈的虚拟环境：**轻松达到4-8GB**。十个项目虚拟环境，无去重：**消耗40-80GB**。

**真正关键的因素——去重策略：**

```bash
# 1. uv通过硬链接在虚拟环境间共享同一缓存——这是最大的优化
uv venv .venv1 && uv pip install torch vllm
uv venv .venv2 && uv pip install torch transformers
# 两个虚拟环境共享底层数据块，实际磁盘用量约1倍而非2倍
uv cache dir
du -sh $(uv cache dir)

# 2. 仅用于CPU开发/测试的虚拟环境使用无CUDA的torch构建（体积小得多）
pip install torch --index-url https://download.pytorch.org/whl/cpu
# 约200MB vs 3GB

# 3. 跳过捆绑的CUDA，使用系统CUDA + 单独安装的cudnn
# （仅当您已经在手动管理驱动/工具包版本时才值得）

# 4. 不要为每个虚拟环境重新编译flash-attn——构建一次，复用wheel
pip wheel flash-attn -w /tmp/wheels
# 然后在每个虚拟环境中：pip install /tmp/wheels/flash_attn-*.whl
```

针对您的MI300X配置特别说明——ROCm torch构建同样有数GB大小（约3-4GB），情况相同。无论CUDA还是ROCm，`uv` + 共享缓存都是解决方案。

实际预期数字：使用`uv`去重后，N个包含完整LLM技术栈的虚拟环境大约消耗**1倍基础安装量（约5-8GB）+ 每个虚拟环境的小幅增量**，而非N倍。

参考：
- [PyTorch安装矩阵](https://pytorch.org/get-started/locally/)
- [uv缓存/去重文档](https://docs.astral.sh/uv/concepts/cache/)