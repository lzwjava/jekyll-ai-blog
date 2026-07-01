---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 手动安装规避npm的Camoufox
translated: true
type: note
---

# 手动安装 Camoufox 以绕过缓慢的 npm 下载

**问题：** 在 `@askjo/camofox-browser` 上执行 `npm install` 时，因尝试下载约 627 MB 的浏览器二进制文件而停滞。

**解决方法：** 将二进制文件直接放入 `camoufox-js` 已寻找的缓存目录中。

---

## 步骤 1 — 确认你的系统架构

```bash
uname -m
```

| 输出 | 架构 | 需下载的 Zip 文件 |
| -------- | ------ | ---------------- |
| `x86_64` | Intel/AMD Linux | `camoufox-146.0.1-alpha.25-lin.x86_64.zip` |
| `aarch64` | ARM64 / Apple M / Pi | `camoufox-146.0.1-alpha.25-lin.arm64.zip` |
| `arm64` | macOS Apple Silicon | `camoufox-146.0.1-alpha.50-mac.arm64.zip` |

---

## 步骤 2 — 下载 Zip 文件

请从 **daijro/camoufox** 的发布页面获取，而不是 apify/camoufox-js（那只是一个 JS 封装器，不包含二进制文件）。

---

## 步骤 3 — 解压到缓存目录

```bash
mkdir -p ~/.cache/camoufox
cd ~/.cache/camoufox
unzip -o /path/to/camoufox-146.0.1-alpha.25-lin.x86_64.zip
```

缓存目录的位置在 `camoufox-js` 中是硬编码的：

| 操作系统 | 路径 |
| ---- | ------ |
| Linux | `~/.cache/camoufox/` |
| macOS | `~/Library/Caches/camoufox/` |
| Windows | `%LOCALAPPDATA%\camoufox\camoufox\Cache\` |

---

## 步骤 4 — 创建 `version.json`

Zip 文件不包含此文件 —— 官方安装程序会写入它。没有它，`camoufox-js` 会拒绝识别二进制文件。

解压后运行二进制文件以查找版本：

```bash
$ ~/.cache/camoufox/camoufox --version
Camoufox Camoufox 146.0.1-beta.25
```

在最后一个连字符处拆分：

```json
// ~/.cache/camoufox/version.json
{"version":"146.0.1","release":"beta.25"}
```

---

## 步骤 5 — 验证

```bash
$ ls ~/.cache/camoufox/
camoufox  camoufox-bin  camoufox.cfg  browser/  fonts/  libxul.so  omni.ja  version.json ...

$ ~/.cache/camoufox/camoufox --version
Camoufox Camoufox 146.0.1-beta.25
```

---

## 步骤 6 — 无需下载即可安装

```bash
cd ~/projects/camofox-browser
npm install --ignore-scripts   # 跳过缓慢的 postinstall 脚本
npm start                      # 立即启动
```

---

## 为什么这样做有效

`camoufox-js` 调用 `installedVerStr()` → `Version.fromPath()`，它会检查：

1. `~/.cache/camoufox/` 存在且不为空
2. `~/.cache/camoufox/version.json` 存在且有效
3. 版本在支持的范围内

如果全部通过 → 返回缓存目录路径作为浏览器位置。无需下载。

---

## 注意事项

> Zip 文件名为 `alpha.25`，但二进制文件自报为 `beta.25`。请始终使用二进制文件自身 `--version` 输出的结果作为 version.json 字段的值。

---

已保存到 `memory/2026-04-11.md`。
