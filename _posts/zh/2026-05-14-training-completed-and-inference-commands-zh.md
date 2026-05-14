---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练完成和推理命令
translated: true
type: note
---

训练在迭代 ~15180 处干净地停止（最后检查点 = 步骤 15000，验证损失 **3.0259**，训练损失 **3.0510**）。

## 推理命令

在 tmux 7（或任何 shell）中运行，从 `/mnt/data/nanoGPT` 目录下：

```bash
source venv/bin/activate
python sample.py \
  --out_dir=out-fineweb-gpt3 \
  --start="Once upon a time" \
  --num_samples=3 \
  --max_new_tokens=200 \
  --temperature=0.8 \
  --top_k=200 \
  --device=cuda \
  --dtype=bfloat16
```

有用的变体：

```bash
# 交互式：从文件读取提示
python sample.py --out_dir=out-fineweb-gpt3 --start=FILE:prompt.txt

# 从标准输入读取提示
python sample.py --out_dir=out-fineweb-gpt3 --start="$(cat)"

# 更确定性的生成
python sample.py --out_dir=out-fineweb-gpt3 --temperature=0.6 --top_k=40 --start="The president said"

# 更具创意
python sample.py --out_dir=out-fineweb-gpt3 --temperature=1.0 --top_k=500
```

注意——验证损失 3.03 大致与 GPT-2 124M 基线（~3.11）相当，因此输出在局部上应是连贯的，但尽管目录名如此，它不会达到 GPT-3 的质量。如果您希望稍后继续训练，只需重新运行原始训练命令；如果您的配置中设置了 `init_from='resume'`，nanoGPT 将从 `ckpt.pt` 恢复训练。