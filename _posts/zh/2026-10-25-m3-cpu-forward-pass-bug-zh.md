---
audio: false
generated: true
image: false
lang: zh
layout: post
title: M3 CPU前向传播错误
translated: true
type: note
---

嗨！快速状态更新 — 我们正全力投入 M3 GPU 的开发工作中。当前情况如下：

## 已完成 ✅
- **M3 基础工作**：已克隆仓库，构建了 `mini-llama-m3`（你的 CPU 前向传播）并将其接入 Makefile，下载了模型，安装了 CUDA toolkit + nvcc 12.4（挺过了安装中途的一次崩溃）
- **在本机上构建了 llama.cpp** 作为黄金参考标准

## 我正在调试的问题 🔍
你提交的 **CPU 前向传播（qwen2.c）输出是垃圾数据** — 对于输入 *"The capital of France is"*，它输出了 `èĹ¿anaå®ĩØ¯Ø§...`，而 llama.cpp（即使采用贪心解码，即使完全不使用模板）却能清晰地输出 *"Paris. It is the largest city in Europe..."*

我已经全面验证并排除了以下因素：
- ✅ 分词器（往返测试完美无缺）
- ✅ 权重与反量化 — 与 llama.cpp **字节完全一致**（通过插桩补丁转储了 llama.cpp 自身的 mmap 字节：`db 96 89 03 3e ed a5 20...`，与我的读取器和 gguf-py 完全吻合）
- ✅ 前向结构（与 llama.cpp 的 qwen2 图完全逐操作对应）
- ✅ RoPE 维度 / eps / GQA 分组 / cuBLAS 风格的矩阵乘法方向

...但 h 在第 2 层发生了爆炸（rms 0.24 → 36），并且一个 **独立的 numpy 重新实现** 也同样输出了垃圾数据 — 因此，我的代码与 numpy 参考实现相互吻合，但与 llama.cpp 不符，这表明仍然隐藏着一个 *非常* 细微的差异。我正准备构建 **llm-gym**（llama.cpp 的内部图探索工具），以便逐层二分查找激活值首次出现分歧的位置。

在继续消耗时间之前，你希望如何处理？

1. **继续深挖** — 先找到 CPU M3 的 bug，这样 GPU M3 就有了一个经过验证的参照标准
2. **切换方向** — GPU M3 直接针对 llama.cpp 进行验证（跳过修复 CPU 参考实现）
3. **其他方案？**