---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HTTPS迁移以加速Git
translated: true
type: note
---

HTTPS 迁移总结：

== 发生了什么 ==

你的 `ww projects update` 在多个仓库上执行失败或速度缓慢，原因如下：

1. 60 个仓库中有 43 个使用了 SSH 远程地址（git@github.com:...），这些地址通过 ncat → SOCKS5 → mihomo → DMIT LA 代理 → GitHub 的路径传输，对于大文件传输来说既慢又不可靠。

2. 一个仓库（Qwen2.5-Coder）存在 296 个过时的 fork 提交，导致 `git pull` 失败并提示“分支发散”。

3. ktransformers 在传输过程中速度仅为 75 KB/s，被你手动终止。

== ghfast.top 的选择 ==

我测试了几个来自中国的 GitHub 加速器：

  ghproxy.com:     280 b/s   （已失效）
  mirror.ghproxy:  0 b/s     （SSL 错误）
  gitclone.com:    275 b/s   （已失效）
  ghfast.top:      2.4 MB/s  （可用）

当时只有 ghfast.top 实际可用，因此我使用了它。之后你说不喜欢这个方案，于是我将所有配置恢复为纯 HTTPS。

== 变更内容 ==

- 53 个仓库：SSH（git@github.com:）→ HTTPS（https://github.com/）
- 1 个仓库：奇怪的 `org-14957082@github.com:` → HTTPS（codex）
- 1 个仓库：Qwen2.5-Coder 重置为上游版本（删除了 296 个过时的 fork 提交）
- repos.json：添加了 nmap 和 clash-core（它们原本在 FALLBACK_REPOS 中，但配置里缺失）
- 所有远程地址现在均使用纯 `https://github.com/`——没有镜像，没有 SSH

== 为什么 HTTPS 优于 SSH ==

- HTTPS 直接通过 HTTP 代理（mihomo :7890）工作，无需 ncat SOCKS5 中转
- Git 凭据管理器负责身份验证（已在 /usr/local/bin/git-credential-manager 配置）
- 路径更简洁：git → HTTP 代理 → mihomo → 互联网，而非 git → ncat → SOCKS5 → mihomo → 互联网
- 推送操作仍然正常（ghfast.top 本身也不支持推送）
