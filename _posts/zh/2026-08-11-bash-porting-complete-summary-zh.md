---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Bash移植完整总结
translated: true
type: note
---

已完成。所有内容已移植并验证正常工作。

## 写入 `~/.bashrc` 的内容

**从 `.zprofile`（Mac）移植并适配 Linux 的修改：**

- `GLOBAL_PROXY` — 指向 `127.0.0.1:7890`，与已运行的 **mihomo** 实例匹配（端口 7890 混合代理 / 7891 SOCKS / 9090 控制台）
- `start_proxy` / `stop_proxy` — **默认保持关闭状态**（已注释，与你原始配置一致）；`stop_proxy` 现使用 `unset` 而非 `export VAR=`（更简洁）
- `start_git_proxy` / `stop_git_proxy` — Git 全局配置，已验证可用
- `gitpush` / `gitcommit` + 别名 `gpa` / `gca`

**已移除（本机不存在的内容）：**

- `/opt/homebrew` 路径及 `brew shellenv` — Linux 上没有 Homebrew
- `SSL_CERT_FILE=~/bin/cacert.pem` — 文件不存在；未安装 Ruby/Jekyll
- `rougify` 别名 — 无 Rouge 项目
- Mac 系统的 PATH 导出本身

## Ghostty 说明

Ghostty 以 bash 作为你的 shell，由于 `.profile` 会调用 `.bashrc`，这些配置在登录 shell 和交互式 shell 中均可加载——无需额外操作。只需**重启 Ghostty**（或运行 `source ~/.bashrc`），即可使用 `start_proxy`、`gpa` 等功能。

测试确认：在新启动的 bash 中，别名、函数和代理环境变量的设置/取消均工作正常。测试完成后，我已将 Git 代理配置清理回未设置状态。

需注意：`gitcommit`/`gitpush` 会执行 `git add -A` 添加所有文件——与原始配置一致，只是提醒一下，在共享仓库中使用需谨慎。
