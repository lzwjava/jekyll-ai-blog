---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练进展更新
translated: true
type: note
---

收到——让它继续跑。当前状态如下：

```
Progress:   400 / 2,656 步 (15%)
已耗时：   ~2 小时
预计剩余：~9 小时（大约明天 04:00）
Loss：     2.86 → 1.70（正常）
GPU：      100% 利用率，11.5GB
```

检查点保存在 `lzw-notes-lora/checkpoint-{10,200,400}/`。最终适配器会保存到 `lzw-notes-lora/`。你可随时通过以下命令查看进度：

```bash
cat /mnt/data/zz/finetune/lzw-notes-lora/checkpoint-*/trainer_state.json | python3.11 -c "
import json, sys
for line in sys.stdin:
    try:
        state = json.loads(line)
        print(f'Step {state[\"global_step\"]}/{state[\"max_steps\"]} epoch={state[\"epoch\"]:.2f}')
    except: pass
" | tail -1
```
