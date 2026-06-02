---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 禁用计划技能与代理委托
translated: true
type: note
---

计划模式是一种技能，但你看到的缓慢现象来自于委派（即生成子代理进行审查）。需要禁用两项功能：

1. **禁用计划技能**，使代理不再编写计划：

```bash
hermes skills config
```

或直接删除：

```bash
rm -rf ~/.hermes/skills/software-development/plan/
```

2. **禁用委派**，以停止生成子代理（这才是真正的瓶颈）：

```bash
hermes config set delegation.max_concurrent_children 0
```

或完全禁用 `delegation` 工具集：

```bash
hermes tools disable delegation
```

完成任意一项更改后，执行 `/reset` 以启动新会话。

委派生成（审查 → 规范检查 → 代码质量审查，每一步都作为独立的子代理）正是消耗时间和 token 的元凶。禁用 `delegation` 工具集会强制代理内联执行所有操作——速度更快，API 调用更少。
