---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 奥兹的伊丽莎白·弗莱
translated: true
type: note
---

组变更仅适用于**新的登录会话**。您当前的终端仍在使用旧组。请立即运行以下命令以临时解决此问题：

```bash
sg dialout -c "cargo run -- uno status"
```

该命令会临时使用 `dialout` 组来执行。按 `q` 或 `Esc` 退出。

如果您希望无需 `sg` 即可正常运行，请**注销并重新登录**（或重启），之后可直接运行 `cargo run -- uno status`。