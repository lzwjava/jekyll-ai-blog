---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SEC-EDGAR-GPT论文更新
translated: true
type: note
---

这些只是第一次 pdflatex 编译时出现的标准“未定义引用”警告——预先存在，并非由我的修改引起。没有错误。

已完成。对 `/Users/lzwjava/projects/sec-edgar-gpt/sec-edgar-gpt.tex` 进行了两项修改：

1. 标题更新为：“SEC-EDGAR-GPT：基于 SEC EDGAR 文件从头训练的 GPT-2（124M）语言模型”

2. 新增第 8 节“模型服务”（位于讨论与结论之间），包含四个小节：
   - bias=False 转换问题——关于为何 Hugging Face 转换存在风险的核心正确性论证（融合的 c_attn 权重布局、转置错误）
   - 采样一致性——nanoGPT 的 10 行 generate() 函数与 Hugging Face 的 2000 行调度器对比
   - 依赖开销——仅需 torch+tiktoken，无需 transformers/safetensors/tokenizers
   - 何时优先选择 Hugging Face 或 vLLM——坦诚说明权衡（批量服务、生态系统、from_pretrained 接口）

PDF 编译干净，共 21 页。