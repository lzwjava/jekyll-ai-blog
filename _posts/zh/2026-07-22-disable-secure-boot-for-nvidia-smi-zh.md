---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 禁用nvidia-smi的安全启动
translated: true
type: note
---

Agent 无法运行 `reboot` —— 你需要直接在终端中执行此操作。

在工作站上，运行：

```bash
sudo reboot
```

然后在 POST 阶段（黑屏，刚开机时），**反复按 DEL 键**进入 BIOS。

在 BIOS 中：

1. **Settings** → **Security** → **Secure Boot** → **Disabled**
2. **F10** → **Yes** 保存并退出

再次重启，然后 `nvidia-smi` 应该可以工作了。
