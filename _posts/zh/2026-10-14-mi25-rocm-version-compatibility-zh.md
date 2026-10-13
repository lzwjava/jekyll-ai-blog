---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI25 ROCm 版本兼容性
translated: true
type: note
---

对于 **MI25 16GB**，实际答案如下：

| ROCm 版本 | MI25（`gfx900`）状态 |
|---|---|
| ROCm 4.x | 历史上官方支持 |
| ROCm 5.x | 官方支持已移除 |
| ROCm 6.0–6.2 | 未官方支持；社区变通方法可能有效 |
| ROCm 6.3 | 社区报告表明某些配置可以使用 |
| ROCm 6.4+ | 未官方支持；兼容性取决于社区构建和补丁 |
| ROCm 10.1 | 未官方支持 |

来源：[Arch Linux Wiki — MI25](https://wiki.archlinux.org/title/AMD_Radeon_Instinct_MI25) 和 [AMD 当前的 GPU support matrix](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html)。[wiki.archlinux.org](https://wiki.archlinux.org/title/AMD_Radeon_Instinct_MI25?utm_source=chatgpt.com)

### 我的建议

如果你找到非常便宜的 MI25，可以尝试 **ROCm 6.3 和兼容的 PyTorch 构建**，但不要假设所有操作都能正常工作。

例如，某些应用程序可能可以运行，而另一些则会失败，因为它们的预编译 GPU 内核不包含 `gfx900`。

如果你的目标是尝试 LLM 推理，请在购买多张卡之前测试 GPU、ROCm、PyTorch 和推理软件的确切组合。