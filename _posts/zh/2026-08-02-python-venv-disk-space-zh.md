---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python venv 磁盘空间
translated: true
type: note
---

问题：Python venv 会占用大量磁盘空间吗？

答案：venv 外壳本身很小（约 10-20MB —— 仅包含一个 Python 符号链接、pip 以及基本的 stdlib 存根）。真正占用空间的是你通过 `pip install` 安装进去的内容，而且除非你去重，否则每个 venv 都会重复占用这些空间。

查看实际占用明细：

```bash
python3 -m venv /tmp/test-venv
du -sh /tmp/test-venv
# 约 10-20MB

source /tmp/test-venv/bin/activate
pip install torch
du -sh /tmp/test-venv
# 2-6GB，取决于 CUDA 构建版本
```

对于你的工作流（GPU/LLM 相关）来说，真正导致膨胀的地方在这里：

```bash
# torch+cuda wheel 是元凶
pip show torch | grep Location
du -sh $(python -c "import torch, os; print(os.path.dirname(torch.__file__))")
# torch 单独：约 2.5GB（捆绑 CUDA 12.x）
```

如果你为每个项目（代理开发、微调实验）都创建一个 venv，那么 N 个 venv × torch = N × 2-6GB。在开发机上很快就会累积起来。

**按实际使用顺序排列的解决方案：**

1. **使用 `uv` 替代 `pip`/`venv`** —— 从全局缓存中对包进行硬链接，因此 10 个包含 torch 的 venv 只占用约 1 份磁盘空间，而非 10 份：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv
uv pip install torch
# 后续安装 torch 的 venv 通过硬链接复用缓存
```

2. **检查/清理 uv 缓存大小：**
```bash
uv cache dir
du -sh $(uv cache dir)
uv cache clean  # 磁盘紧张时清空
```

3. **`pip cache` 也有一定帮助**（不是硬链接，但可以避免重复下载）：
```bash
pip cache info
pip cache purge
```

4. **`--system-site-packages`** 如果你希望共享一个基础 venv，仅隔离少量包：
```bash
python3 -m venv .venv --system-site-packages
```

对于你的配置（MI300X 训练，多个 CLI 代理），`uv` 是真正的解决方案 —— pip/venv 的跨项目重复占用才是实际的磁盘问题，而非 venv 本身。

参考：
- [uv 文档 — 缓存](https://docs.astral.sh/uv/concepts/cache/)
- [uv 安装](https://docs.astral.sh/uv/getting-started/installation/)