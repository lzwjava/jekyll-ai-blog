---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Electron下载卡顿问题已修复
translated: true
type: note
---

确认 — `Electron.app` 已解压，`path.txt` 解析正确。桌面依赖已完全安装。

## 已完成

卡顿问题已修复并验证：

|                 | 之前                         | 之后                             |
| --------------- | ---------------------------- | --------------------------------- |
| `npm ci`        | 无限挂起                     | 约21秒内退出，返回0               |
| Electron 二进制  | 在 GitHub CDN 直连时卡住     | 通过 `npmmirror` 下载 109 MB      |
| `Electron.app`  | 缺失                         | ✓ 存在且已解压                    |

**根本原因：** Electron 的 postinstall 脚本直接从 GitHub 下载二进制文件，绕过了你的 `localhost:7890` 代理 → 导致卡顿 → `npm ci` 无法返回 → `hermes update` 在 `subprocess.wait()` 中被阻塞。

**修复方案：** `~/.npmrc` 已将 `electron_mirror`（以及 `electron_builder_binaries_mirror`）指向 `npmmirror.com`。此配置为持久化设置，后续安装不会再遇到此问题。

现在可以重新运行 `hermes update` — 由于 Node 端已完成并缓存，Python/依赖步骤将顺利执行。如果重新运行 `npm ci`，由于二进制文件已缓存，几乎瞬间完成。

注意：之前的 `hermes update` 实际上已完成 Python 部分的工作（在进入 Node 步骤前已将 `hermes-agent` 从 0.15.1 升级至 0.17.0），因此仅 Node 依赖阶段未完成 — 现已解决。
