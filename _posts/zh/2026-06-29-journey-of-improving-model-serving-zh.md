---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 提升模型服务之旅
translated: true
type: note
---

这是改进模型服务的完整历程：

== 问题 ==

RunPod 上的服务器产生了退化、重复且不连贯的输出 —— 将“石油和天然气行业”与“医疗行业”混杂在一起，重复短语，并生成“ivableivable...”之类的垃圾内容。

== 发现的根本原因 ==

1. 错误的模型转换（nanoGPT → HuggingFace）
   - nanoGPT 将 Linear 权重存储为 [out_features, in_features]
   - HF GPT2Conv1D 期望 [in_features, out_features]
   - 转换脚本转置了权重，这对非方阵是正确的
   - 但模型同时使用了错误的词表加载（50304 填充 → 50257 修剪），添加了零偏置，并且 transformers generate() 内部 logit 处理不同
   - 结果：transformers 版本产生的输出明显差于原生 nanoGPT

2. 糟糕的采样参数
   - 服务器使用了 top_p=0.9（核采样）
   - nanoGPT 使用 top_k=200
   - 在小型 124M 模型上使用 top_p 会将概率泄露给不太可能的 token → 文本不连贯

3. SEC_SYSTEM 前缀污染
   - 每个提示前都添加了：
     “以下摘录自上市公司向美国证券交易委员会提交的 SEC EDGAR 文件。”
   - 模型并未使用此前缀训练 → 上下文混乱 → 重复性垃圾输出

4. 换行符修剪器截断了输出
   - Chat 端点包含：`if "\n" in text[20:]: text = text[:text.index("\n", 20)]`
   - SEC 文件文本自然在早期出现换行符 → 输出被截断至约 134 个字符

== 已应用修复 ==

| 修复项 | 修复前 | 修复后 |
|------|--------|-------|
| 模型加载 | HF transformers GPT2LMHeadModel + 转换后的 safetensors | 原生 nanoGPT model.py + 原始 ckpt.pt (1.4GB) |
| 分词器 | transformers AutoTokenizer | tiktoken GPT-2 BPE |
| 采样方式 | top_p=0.9 | top_k=200 |
| 温度 | 0.7 | 0.8 |
| 默认 max_tokens | 100 | 1000 |
| SEC_SYSTEM 前缀 | 每个提示前都添加 | 移除 |
| 换行符修剪器 | 在第一个 \n 处截断聊天输出 | 移除 |
| 依赖项 | torch + transformers + accelerate + fastapi | torch + tiktoken + fastapi |

== 结果 ==

修复前：
  “我们的主营业务是位于加利福尼亚州旧金山的主要行政办公室，位于旧金山，加利福尼亚州……”

修复后：
  “在截至 2016 年 12 月 31 日的一年中，公司确认了 0.1 百万美元的非现金减值费用……坏账费用。详情请参见注释 9。”

== RunPod 上的文件 (/workspace/model/) ==

  ckpt.pt       1.4GB   原始 nanoGPT 检查点（47k 步，验证损失 2.2778）
  model.py      8.6KB   nanoGPT 模型定义（原生，非 HF）
  server.py     4.5KB   使用原生模型的 FastAPI 服务器
  index.html    聊天 UI
  hf-model/     622MB   旧 HF 模型（备份，未使用）