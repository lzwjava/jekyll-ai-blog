---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 莎士比亚模型训练进度
translated: true
type: note
---

运行成功！仅用10.65M参数模型训练500次迭代后，已经能生成带莎士比亚风格（虽仍有些混乱）的文本。以下是摘要：

**训练结果：**
- 模型：10.65M参数，6层字符级GPT
- 损失：从4.28降至1.71（验证集），训练500步（总计约30秒）
- 检查点已保存至`out-shakespeare-char/`

**使用提示语`"To be or not to be"`生成的样本**显示模型已学会：
- 英语单词与基础语法
- 部分莎士比亚式词汇（"Madam", "noble", "thee/thou"）
- 类似舞台对白的换行格式
- 但500次迭代后仍存在不连贯问题——需训练至5000次以获得更高质量

若要获得合格的莎士比亚风格文本，请完整运行5000次迭代：
```bash
python3 train.py config/train_shakespeare_char.py
```
