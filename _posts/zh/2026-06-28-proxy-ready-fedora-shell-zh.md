---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代理就绪的Fedora Shell
translated: true
type: note
---

已完成。已将 `.bashrc` 从工作站复制并适配到 Fedora。

**新的 `.bashrc` 包含内容：**

- `start_proxy` / `stop_proxy` — 通过 mihomo (127.0.0.1:7890) 切换 HTTP/HTTPS 代理
- `start_git_proxy` / `stop_git_proxy` — 切换 Git 代理
- `checkproxy` — 显示当前代理状态
- `gpa` / `gca` / `gpp` — Git 快捷命令
- Shell 启动时自动启用代理
- `OPENROUTER_API_KEY`、`MODEL=deepseek/deepseek-v3.2`（已遮蔽）
- HISTSIZE 提升至 10000，颜色别名，Python 3.14

**已验证：**

```
HTTP_PROXY: http://127.0.0.1:7890 ✅
Git proxy: 127.0.0.1:7890 ✅
通过代理 curl：出口 IP 69.63.219.52 ✅
Python 3.14.3 ✅
```

Fedora 机器上的新 Shell 将开箱即用地配置好代理和 API 密钥。
