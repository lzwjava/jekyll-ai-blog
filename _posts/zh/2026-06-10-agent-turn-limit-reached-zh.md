---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 智能体回合限制已达
translated: true
type: note
---

**你当前的配置：**

```
agent:
  max_turns: 60        ← 这是你的迭代预算
```

这就是你达到60/60的原因。需要我调高它吗？常见选项：

- `90` — 默认值
- `120` — 充裕的余量
- `200` — 用于繁重任务

另外请注意第366行（`delegation.max_iterations: 50`）独立限制了每个子代理。

需要我把 `max_turns` 改为特定值吗？直接说数字即可。
