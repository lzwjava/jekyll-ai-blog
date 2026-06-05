---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat 训练状态更新
translated: true
type: note
---

这是来自 tmux 会话 0 的 nanochat 训练状态（会话 7/12 不存在——只有 0 和 14 是活跃的，两者显示相同的训练输出）：

```
Progress:  step 60841 / 87,000  (69.93%)
Loss:      ~2.99  (healthy, stable)
LR:        0.49
Speed:     ~55,660 tok/sec, ~1,177 ms/step
Elapsed:   1,193 minutes  (~19.9 hours)
ETA:       ~513 minutes   (~8.5 hours)
Epoch:     1
GPU:       RTX 4070 @ 100% util, 55% mem, 66°C, 211W
```

总结：
- 已完成约 70%，剩余约 26,160 步
- 按约 1.18 秒/步，还需约 8.6 小时（ETA 确认约 513 分钟）
- Loss 稳定在 2.98-3.02 左右——训练健康
- GPU 满载，运行温度 66°C，状态良好

因此，如果没有中断，预计今晚约 9-10 点完成训练。