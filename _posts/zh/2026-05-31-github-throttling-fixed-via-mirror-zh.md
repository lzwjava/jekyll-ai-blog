---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub限制问题通过镜像解决
translated: true
type: note
---

获取瞬间完成。现在让我给你完整的分析。

== 根本原因 ==

速度慢的原因不是 ncat 或代理，而是中国到 GitHub 的 ISP 限速。

速度测试：
  直连 GitHub：                    33 KB/s
  通过 Hysteria2 代理：           59 KB/s
  通过 ghfast.top 镜像：          2.4 MB/s（快 70 倍）

无论是直连还是代理路径，都受到了中国 ISP 的限速。Hysteria2 代理（DMIT LA）没有帮助，因为瓶颈在于中国的最后一公里出口，而不是代理本身。

== NCAT 源代码 ==

位于 /Users/lzwjava/projects/nmap/ncat/

ncat_connect.c 第 621-921 行：`do_proxy_socks5()` — 标准的 SOCKS5 握手，没有性能问题。
ncat.h 第 140 行：`#DEFAULT_TCP_BUF_LEN = 8192`（8KB 中继缓冲区）— 对于吞吐量来说足够。
ncat_posix.c：中继循环使用 select() + 8KB 读取 — 不是瓶颈。

ncat 本身没有问题。问题出在网络路径上。

== 已应用解决方案 ==

将 Qwen2.5-Coder 远程仓库改为使用 ghfast.top GitHub 镜像：
  <https://ghfast.top/https://github.com/QwenLM/Qwen2.5-Coder.git>

现在获取操作瞬间完成。

注意：该仓库本地有 296 个提交领先于上游（看起来像是一个分支合并历史）。你可能需要变基或重置：
  git rebase origin/main     # 保留本地提交
  git reset --hard origin/main  # 丢弃本地提交

== 适用于所有 GitHub 仓库 ==

要全局应用（所有 GitHub 仓库都使用 ghfast.top）：
  git config --global url.<https://ghfast.top/https://github.com/.insteadOf> <https://github.com/>

或者仅针对单个仓库。注意：通过镜像无法进行推送操作——你需要临时覆盖设置才能推送：
  git push <https://github.com/>... main

需要我设置全局配置吗？
