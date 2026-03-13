---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 选择 Mihomo Linux AMD64 二进制指南
translated: true
type: note
---

## 您的系统分析

根据您的 `uname -a` 输出：
```
Linux to 6.8.0-90-generic x86_64 x86_64 x86_64 GNU/Linux
```

关键事实：
- **OS**：Linux (Ubuntu 22.04)
- **Architecture**：`x86_64` (64 位 Intel/AMD)
- **NOT**：Android、macOS 或 ARM

---

## ✅ 要下载的正确文件

**`mihomo-linux-amd64-v1-alpha-0317d9f.gz`**

> 注意：此文件**未在您上面列出的资源中显示** — 您在该部分列表中仅看到 `android-*` 和 `darwin-*` 变体。您需要在 GitHub 发行版页面**向下滚动**以找到 `linux-*` 文件。

---

## 理解 `amd64` 变体

在看到 Linux 文件后，以下是如何在 `amd64` 子变体中选择：

| 变体 | CPU 要求 | 推荐 |
|---|---|---|
| `linux-amd64-v1` | 任何 x86_64 CPU（最广泛兼容） | ✅ **大多数系统的安全默认选择** |
| `linux-amd64-v2` | 需要 SSE4.2（2008 年后 CPU） | 如果您的 CPU 支持，则稍快 |
| `linux-amd64-v3` | 需要 AVX2（2013 年后 CPU） | 现代 CPU 上最佳性能 |

要检查您的 CPU 支持哪个级别：
```bash
# 检查 v2 支持
grep -m1 -c 'sse4_2' /proc/cpuinfo

# 检查 v3 支持 (AVX2)
grep -m1 -c 'avx2' /proc/cpuinfo
```
如果输出为 `1`，则您的 CPU 支持该级别。

**为了安全兼容的选择**，坚持使用 `mihomo-linux-amd64-v1-alpha-XXXXXXX.gz`。

---

## 下载后

```bash
# 解压
gunzip mihomo-linux-amd64-v1-alpha-0317d9f.gz

# 赋予执行权限
chmod +x mihomo-linux-amd64-v1-alpha-0317d9f

# 运行
./mihomo-linux-amd64-v1-alpha-0317d9f
```

参考资料：

- [MetaCubeX/mihomo Releases - GitHub](https://github.com/MetaCubeX/mihomo/releases)
- [Mihomo Official Docs](https://wiki.metacubex.one/en/startup/)