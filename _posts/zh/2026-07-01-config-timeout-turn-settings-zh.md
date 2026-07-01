---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 配置超时与转向设置
translated: true
type: note
---

由于超时已过期，以下是当前情况的总结：

**当前配置**（`~/projects/config/hermes/config.yaml`）：

```
agent.max_turns: 60        ← 主要交互预算
goals.max_turns: 20
```

**`max_turns: 60`** 表示代理在每个会话中经过 60 轮后停止——即你和 AI 之间的 60 次来回交流。一旦达到该次数，会话结束。

要增加此数值，只需告诉我你想要的值。常见值：
- **100** —— 适度增加
- **200** —— 用于繁重编码会话
- **无限制**（设为 `null`）—— 无限制

如果你有其他笔记本电脑可用（可能通过相同的 GitHub 配置仓库，但从那里推送了不同的提交），我可以尝试从远程拉取，查看是否推送了不同的版本。