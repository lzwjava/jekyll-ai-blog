---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MPS模型性能摘要
translated: true
type: note
---

两个模型在MPS上均运行完美。以下是总结：

```
结果
=======

1. 莎士比亚字符级模型（0.80M参数）
   - 检查点：out-shakespeare-char/ckpt.pt（9.7 MB）
   - 设备：MPS，数据类型：float32
   - 输出：伪莎士比亚风格文本，包含角色名和对话格式
   - 示例："Forstan deefff, here the be dofenink you..."

2. HuggingFace的GPT-2模型（123.65M参数）
   - 加载方式：init_from=gpt2（自动下载权重）
   - 设备：MPS，数据类型：float32
   - 提示词："The future of AI is"
   - 输出：关于AI的连贯且切题的段落

MPS基准测试
  100次1024x1024矩阵乘法：0.136秒
  MPS可用：True
  torch 2.11.0 via python3.14
```

在Mac上运行的关键说明：
- 使用`python3.14`（包含torch 2.11.0及MPS支持）或`python3.13`（torch 2.6.0）
- 参数设置：`--device=mps --dtype=float32`（MPS对bfloat16支持不佳）
- model.py已启用调试打印——前向传播时会显示每层的张量形状。便于学习，但生产环境会显得冗余。

需要我尝试更大的模型（gpt2-medium/large/xl），或在MPS上训练小型模型吗？