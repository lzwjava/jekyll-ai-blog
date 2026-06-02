---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过错误配置设置进入YOLO模式
translated: true
type: note
---

当前状态：

- **YOLO 标志 (--yolo)：** 本次会话未传递
- **HERMES_YOLO_MODE 环境变量：** 未设置
- **config.yaml 中的 approvals.mode：** `false`

`approvals.mode` 被设置为 `false`，这不是有效值之一（`manual`、`smart`、`off`）。由于 `false` 是 falsy 值，它很可能被视为 "off" —— 意味着跳过审批提示，实际上就是 YOLO 模式。

要明确设置，可以将其设为已识别的值：

```bash
hermes config set approvals.mode off      # 显式 YOLO
hermes config set approvals.mode manual   # 始终提示（默认）
hermes config set approvals.mode smart    # 由 LLM 决定
```

所以，是的 —— 你现在实际上处于 YOLO 模式。
