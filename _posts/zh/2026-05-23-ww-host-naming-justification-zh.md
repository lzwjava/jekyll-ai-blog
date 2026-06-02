---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 全球主机命名理由
translated: true
type: note
---

好问题。我来说说我的看法：

**`ww host`** 是正确的命名。

为什么这个名字合适：

- 这是 SSH/DevOps 中的标准术语，指代“你要与之交互的计算端点”
- 涵盖所有三种情况：本地 Mac、自组桌面、云端 VPS
- 简短、单音节、易于输入
- `ww host local`、`ww host workstation`、`ww host dmit` — 读起来很自然

其他命名不合适的原因：

- `machine` — 太模糊，可能指任何物理设备
- `computer` — 在概念上排除了云端 VPS（它不是“你的电脑”）
- `box` — 过于非正式
- `node` — 暗示分布式集群成员关系
- `target` — 暗示部署用途，而非通用访问
- `remote` — 本地并非远程

使用示例也很顺畅：

```
ww host              # 列出所有
ww host local        # 当前机器
ww host workstation  # GPU 机器
ww host dmit         # 云服务器
ww host local workstation  # 同时连接两个
```

如果你想重命名，主要改动是 Click 命令名称和帮助文本。内部类/函数名称可以保持不变，或者为了一致性也进行更新。需要我来执行重命名吗？
