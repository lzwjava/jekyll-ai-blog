---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在tmux中运行nanoGPT Fineweb训练
translated: true
type: note
---

```bash
cd /mnt/data/nanoGPT
tmux new -s nano        # 或：tmux attach -t nano

# 不要激活虚拟环境——使用系统自带的 python3.11
PYTORCH_ALLOC_CONF=expandable_segments:True \
python3.11 -u train.py config/train_fineweb_gpt3.py --compile=False 2>&1 \
  | tee -a out-fineweb-gpt3/train.log
```

使用 `Ctrl-b d` 分离，使用 `tmux attach -t nano` 重新连接。

在进程被终止或重启后恢复训练：添加 `--init_from=resume`。

预期：即时模式下约 11 秒/迭代 → 完整运行 19073 次迭代约需 59 小时，每迭代 500 次保存一次检查点。