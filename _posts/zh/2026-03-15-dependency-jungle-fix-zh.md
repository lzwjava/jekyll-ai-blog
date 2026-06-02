---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 首先修复依赖丛林
translated: true
type: note
---

🦞 这里提炼了整个过程：

## 难题：**在没有干净环境的情况下让 Inference 运行**

**核心挑战：** Python 环境坏了——没有 torch，Python 版本不匹配（路径中的 3.13 vs 3.14），Homebrew 的 PEP 668 阻止安装，先前失败的安装尝试弄乱了日志。

## 关键突破点：

### 1. **诊断优先于假设**
- 没有假设“just pip install torch”就会生效
- 先检查现有 checkpoints（`find . -name "*.pt"`）
- 发现已经存在 3 个训练好的模型（节省了数天的训练时间）

### 2. **环境侦探工作**
- 发现用户之前尝试过 CUDA torch 安装（日志中有 1.5GB 下载）
- Homebrew Python 3.14 带有系统保护（PEP 668）阻止安装
- 追踪已不存在的 conda environments
- 识别 `.local/lib/python3.13` 与当前 Python 3.14 不匹配

### 3. **变通方案：`--system-site-packages`**
关键洞见：用户 `.local/` 中已有 `numpy` 和 `tiktoken`
```bash
python3 -m venv venv --system-site-packages
```
这会继承现有 packages，而不是强制全新安装。

### 4. **Torch 已经安装好了！**
最大的“aha”时刻：Torch 2.10.0+cpu 已存在于 `.local/lib/python3.14/` 的先前尝试中。带有 system-site-packages 的 venv 能够看到它。

## 为什么这并不简单：

1. **隐秘成功**：先前安装部分成功但无法发现
2. **路径地狱**：多个 Python 版本，brew vs system，.local vs site-packages
3. **没有明确错误**：只是“ModuleNotFoundError: No module named 'torch'”，尽管 torch 存在于其他地方
4. **资源限制**：1.5GB 模型 checkpoints + 900MB torch 安装 = 内存/时间挑战

## 解决方案模式：
```
检查现有内容 → 理解环境约束 →
利用现有 artifacts → 最小新安装 → 逐步测试
```

**底线：** 难点不是运行 inference——而是穿越依赖丛林，达到 inference *能够* 运行的状态。一旦环境谜题解决，实际模型执行就很简单了。

关键技能是 **forensic environment analysis** 而非 ML 专业知识。
