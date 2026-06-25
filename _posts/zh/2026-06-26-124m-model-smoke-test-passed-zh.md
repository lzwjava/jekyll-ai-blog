---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 124M模型冒烟测试通过
translated: true
type: note
---

烟雾测试顺利通过。结果如下：

- 加载了16个训练分片 + 1个验证分片
- 1.2359亿参数，无显存问题
- 每次迭代约700毫秒（未编译），MFU约12.8%
- 损失：25步内从11.0降至5.8（学习过程）

使用 compile=True 后，完整配置应能更快一些。完整运行 = 47,400步 × 约32,768 token/步 ≈ 15.5亿 token ≈ 1个 epoch。

命令如下：

```
cd /mnt/data/nanoGPT && python3 train.py config/train_sec_edgar_124m.py
```

已创建的配置：
- `/mnt/data/nanoGPT/config/train_sec_edgar_124m.py`（完整版，47,400步，compile=True）
- `/mnt/data/nanoGPT/config/train_sec_edgar_124m_smoke.py`（烟雾测试版，25步）

我还修改了 train.py，当找不到 `edufineweb_*.npy` 时，会回退到 `train_*.npy` / `val_*.npy` 的 glob 模式，以便它能识别你 sec-edgar 分片的命名方式。