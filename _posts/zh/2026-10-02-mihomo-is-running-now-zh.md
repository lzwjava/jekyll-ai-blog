---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mihomo 正在运行
translated: true
type: note
---

Mihomo 已启动！ 🎉

```bash
● mihomo.service - active (running)
   Main PID: 11130
```

**状态：**

| 端口 | 协议 | 状态 |
| ------ | ---------- | -------- |
| 7890 | HTTP 代理 | ✅ |
| 7891 | SOCKS 代理 | ✅ |
| 7892 | 混合代理 | ✅ |
| 9090 | API 控制器 | ✅ |

**注意：** DNS 在端口 53 上失败（需要 root 权限）——没关系，代理仍然正常工作。

请重新尝试下载：

```bash
wget "https://huggingface.co/unsloth/Qwen3.8-27B-GGUF/resolve/main/Qwen3.8-27B-UD-IQ1_M.gguf?download=true"
```

如果通过代理下载成功，您可以稍后通过撤销配置更改（从 `~/.config/mihomo/config.yaml.bak` 恢复 `tun:` 部分）重新启用 TUN 模式。
