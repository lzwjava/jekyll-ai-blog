---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 恢复后的初步步骤
translated: true
type: note
---

训练正在进行中。当前状态如下：

```
配置：window_pattern="L"  ✓  （已固定，无SSSL警告）
恢复点：第10,000步 -> 从第10,001步继续训练
目标：87,000步
速度：~55,700 tok/秒，~1,177ms/步
预计剩余时间：~1,511分钟（约25.2小时）

第10k步的CORE评估：0.1168
验证bpb：0.9402

初始样本（与之前相同——模型尚未学到新内容）：
  - "capital of France" -> 仍然错误（"south of the country"）
  - "5x+3=13" -> 仍在循环
```

前几步训练刚刚开始（10001、10002、10003）。损失约2.97。运行平稳。将在第20k步时保存检查点。