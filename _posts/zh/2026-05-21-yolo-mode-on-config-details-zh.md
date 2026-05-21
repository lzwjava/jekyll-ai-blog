---
audio: false
generated: true
image: false
lang: zh
layout: post
title: YOLO模式开启：配置详情
translated: true
type: note
---

是的——**YOLO已开启**。你的配置中有：

```yaml
approvals:
  mode: false
```

`mode: false`（即`"off"`）意味着所有批准提示都会被跳过——功能上等同于`--yolo`。危险命令会直接通过而不询问，但**硬限制阻止列表**（`rm -rf /`、`dd if=... of=/dev/sda`、`shutdown`等）无论YOLO状态如何，都会无条件阻止。

要关闭它，你可以：
- 在会话中输入`/yolo`进行切换（这是一个斜杠命令）
- 在`~/.hermes/config.yaml`中将`approvals.mode`设置为`manual`以始终提示