---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模型训练完成摘要
translated: true
type: note
---

训练完成！以下是最终报告：

**Done ✓** —— 全部 87,000 步，在 RTX 4070 12GB 上耗时约 30 小时（1802 分钟）

**最终统计：**

- **Val bpb：0.372** —— 对于 286M 参数的代码模型来说表现不错
- 最终损失范围：~1.06-1.13（仍在波动）
- 峰值 VRAM：6,240 MiB（仅占 12GB 的 52% —— 有提升 batch size 的空间）
- 检查点：`~/.cache/nanochat/base_checkpoints/d12/model_087000.pt`

**示例输出（基础模型，未 SFT）：**

```
法国的首都是法国的首都，而法国的首都是法国的首都。
金的化学符号是介于 0 和 9 之间的一个数字。
热的反义词比它本身要复杂一些。
如果 5*x + 3 = 13，那么 x 是 5*x + 3。
```

经典的基础模型行为 —— 识别了模式结构，但不知道事实。它学会了 Python 语法和文本结构（专有名词大写、方程模式、列表枚举），但它是一个 token 预测器，不是问答机器人。需要 SFT 才能将其转化为有用的助手。

**脚本打印的下一步操作：**

```
评估：python -m scripts.base_eval --device-batch-size=8
聊天：python -m scripts.chat_cli -p 'Write a Python function to reverse a linked list'
```

想运行评估或尝试聊天 CLI 吗？
