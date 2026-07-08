---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python模型训练冒烟测试成功
translated: true
type: note
---

Smoke train 成功完成。在 RTX 4070 上运行：

| 组件 | 时间 | 结果 |
| ----------- | ------ | -------- |
| Tokenizer（4k 词汇表） | 3.6 秒 | 在 5000 万 Python 字符上训练 |
| 预训练（depth=4, 20 步） | ~1 秒 | Loss 8.32→8.19, 310k tok/s, 30% MFU |
| 峰值内存 | 151 MB | 几乎未触及 12 GB |

样本已显示出类似 Python 的输出（`class`、`return`、`import`、许可头）——数据管道端到端工作正常。

实际训练：

```bash
bash /mnt/data/zz/codeparrot/train_codeparrot.sh
```

（depth=12, 87k 步, 286M 参数, 24.7B tokens 时约需 28 小时）
