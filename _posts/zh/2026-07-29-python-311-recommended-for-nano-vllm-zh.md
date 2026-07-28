---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 建议使用 Python 3.11 运行 nano-vllm
translated: true
type: note
---

本项目（**nano-vllm**）的 `pyproject.toml` 文件中定义了：

```toml
requires-python = ">=3.10,<3.13"
```

因此有效的选择是 **Python 3.10**、**3.11** 或 **3.12**。

### 推荐：**Python 3.11**

原因如下：

| 因素 | 3.11 | 3.12 |
| --- | --- | --- |
| **triton 支持** ✅ | 表现优异，经广泛测试 | 良好，但历史上存在少数边缘情况 |
| **torch 兼容性** ✅ | 完全支持 | 支持 |
| **CUDA graph 稳定性** ✅ | 经过最多实战检验 | 尚可，但更新 |
| **包生态系统** ✅ | 机器学习生态兼容性最佳 | 部分包较晚才提供支持 |

由于本项目依赖 `triton>=3.0.0` 和 `torch>=2.4.0`，并使用 **CUDA graphs** 和 **tensor parallelism**（以GPU为核心的机器学习），**Python 3.11** 是最安全、最经过实战检验的选择。

### 如何在 Zed 中设置

1. 打开命令面板（`Cmd+Shift+P`）
2. 运行 **"Zed: Select Python Environment"**
3. 选择你的 **Python 3.11** 解释器

或者在项目根目录创建 `.python-version` 文件：

```bash
echo "3.11" > /mnt/data/nano-vllm/.python-version
```

然后在 Zed 中选择该虚拟环境/解释器。
