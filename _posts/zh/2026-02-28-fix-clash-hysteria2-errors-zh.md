---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Clash Hysteria2 错误修复指南
translated: true
type: note
---

**问题：** 运行 `./clash-darwin-amd64` 时如何修复错误 “FATA[0000] Parse config error: proxy 1: unsupport proxy type: hysteria2”？

**回答：**

这个错误是因为 `hysteria2` (hy2) proxy type **不被** standard Clash core 或较旧的 Clash Premium builds 支持。你的当前二进制文件 (`clash-darwin-amd64`) 很可能是一个经典的 Clash 或旧版的 Clash Premium，只认识较旧的 proxy types (ss, vmess, trojan, snell 等)。

Hysteria2 支持在 **Clash Meta** (mihomo) core 中从大约 version 1.16+ (2023年底/2024年初) 开始添加，现在在 2025–2026 builds 中支持非常完善。

### 快速修复选项 (Mac)

1. **推荐：切换到 mihomo (Clash Meta core)**
   从官方 MetaCubeX/mihomo releases 下载最近的 macOS AMD64 二进制文件：

   - 前往 → <https://github.com/MetaCubeX/mihomo/releases>
   - 找到最新版本 (例如 2026 年的 v1.18.x 或更新版本)
   - 下载文件名大致为：`mihomo-darwin-amd64` 或 `mihomo-alpha-darwin-amd64` 或 `clash.meta-darwin-amd64`
   - 如需可重命名为 `clash` 或 `mihomo`
   - 对文件执行 `chmod +x`
   - 用这个新二进制文件替换旧的 `./clash-darwin-amd64`
   - 再次运行 → `./mihomo-darwin-amd64 -d .` (或你平时启动的方式)

   macOS 上的大多数现代 Clash GUI 客户端 (Clash Verge Rev、Mihomo Party、FlClash 等) 已经内置了最近的 mihomo cores，并开箱即用支持 hysteria2。

2. **备选：使用现代 GUI 客户端代替命令行二进制文件**
   2025–2026 年 macOS 的热门选择：

   - **Clash Verge Rev** → <https://github.com/clash-verge-rev/clash-verge-rev/releases>
     (维护非常活跃，优秀的 hysteria2 / TUIC / VLESS Reality 支持)

   - **Mihomo Party** → <https://github.com/pompurin404/mihomo-party>
     (非常用户友好，专为 mihomo 构建)

   - **FlClash** → <https://github.com/chen08209/FlClash>

   这些客户端会自动处理 config 解析、core 更新和 hy2 节点。

3. **如果你必须只使用命令行**
   - 下载 mihomo 二进制文件 (如选项 1)
   - 或从源代码编译：<https://github.com/MetaCubeX/mihomo>
     (go install github.com/MetaCubeX/mihomo@alpha)

### 总结表格

| 当前二进制文件          | 支持 hysteria2？ | 推荐                             |
|-------------------------|------------------|----------------------------------|
| Classic Clash           | 否               | 切换到 mihomo                    |
| Old Clash Premium       | 否               | 切换到 mihomo                    |
| Recent mihomo / Clash Meta | 是             | 使用此版本 (下载最新)            |
| Clash Verge Rev / Mihomo Party | 是         | 最简单且最方便                   |

将二进制文件替换为 mihomo 版本后，config 中的 `type: hysteria2` 节点应该能正常解析并工作。

**参考：**

- <https://github.com/MetaCubeX/mihomo/releases>
- <https://github.com/clash-verge-rev/clash-verge-rev/releases>
- <https://wiki.metacubex.one/en/> (mihomo 文档)
