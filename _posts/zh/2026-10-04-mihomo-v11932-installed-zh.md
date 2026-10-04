---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mihomo v1.19.32 已安装
translated: true
type: note
---

完成 ✅ mihomo v1.19.32 已安装在 `lzw@192.168.1.46` 上。

## 摘要

| 项目 | 值 |
| ------ | ----- |
| **二进制文件** | `/usr/local/bin/mihomo` |
| **版本** | Mihomo Meta v1.19.32 (linux amd64, go1.26.8) |
| **编译方式** | `compatible` — 因远端 CPU (AMD Athlon X4 850) 缺少 AVX2 而选择 |
| **安装方法** | 本地下载 → SCP → `sudo install` (因远端无法直接访问 GitHub) |

已验证：该二进制文件在远端 CPU 上运行正确，且 `mihomo -v` 报告了正确的版本。

## 备注 / 后续步骤（尚未完成）

二进制文件已安装，但 mihomo **尚未配置或以服务形式运行**：

- ❌ 配置文件不存在于 `/etc/mihomo/config.yaml`
- ❌ 没有 systemd 服务（因此不会自动启动）

要让它真正工作，你需要一个代理配置（订阅地址或自定义规则）。需要我：

1. **创建 `/etc/mihomo/config.yaml`** — 粘贴配置或提供订阅地址，以及
2. **设置 systemd 服务** 使其开机自启？

请告诉我你希望如何进行。
