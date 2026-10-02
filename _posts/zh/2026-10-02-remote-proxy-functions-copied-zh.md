---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 远程代理函数已复制
translated: true
type: note
---

一切就绪！您本地 `~/.zprofile` 中的函数已复制到远程机器的 `~/.profile` 和 `~/.bashrc`。

现在在远程机器上，您可以使用：

| 命令 | 操作 |
|------|------|
| `start_proxy` | 开启代理 → `http://127.0.0.1:7890` |
| `stop_proxy` | 关闭代理 |
| `start_proxy_without_prefix` | 不带 `http://` 前缀的代理 |
| `start_git_proxy` | 设置 git 代理 |
| `stop_git_proxy` | 取消 git 代理 |
| `checkproxy` | 显示当前代理设置 |

这些命令将在下次登录时生效，或立即执行 `source ~/.profile` 以在当前会话中使用。