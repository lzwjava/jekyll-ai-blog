---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 系统状态与优化方案
translated: true
type: note
---

以下是您的系统状态和优化计划：

---

## 系统健康状况

| 指标 | 数值 |
|---|---|
| **内存 (RAM)** | 16 GB (Apple Silicon) |
| **已用内存** | 7.5 GB / 16 GB — **已使用 47%** |
| **交换内存** | 已使用 218 MB — 低，健康 |
| **CPU** | 大部分时间空闲（突发时 < 5%） |
| **用户进程数** | **476** — 相当高 |
| **可用磁盘空间** | 54 GB |

---

## 主要内存消耗者

| 应用 | 内存 | 备注 |
|---|---|---|
| **Safari WebContent (x5)** | **约 3.0 GB** | 每个标签页对应一个独立的 WebKit 进程。TabsKiller 会限制此数量。 |
| **Safari** (主进程) | 315 MB | |
| **微信 + WeChatAppEx** | **513 MB** | 对于聊天应用来说占用较重 |
| **Python (x2)** | 292 MB | 其中一个占 11% CPU — 检查正在运行什么 |
| **Zed** | 143 MB | |
| **WindowServer** | 110 MB | macOS 合成器 |
| **GitHub Desktop** | 109 MB | |
| **Finder** | 65 MB | |
| **Ghostty** | 93 MB | |
| **mihomo** (代理) | 36 MB | |

---

## 建议（按影响排序）

### 1. TabsKiller 已经有效 — 检查设置

你说它保持 10 个标签页。每个关闭的标签页 = 释放一个约 300-800 MB 的 WebContent 进程。这是你最大的调节杠杆。

### 2. 释放 Safari WebContent 内存

这 5 个进程占用 **3 GB**，是你最大的内存占用点。打开 TabsKiller 弹出窗口，确认 `maxTabs` 已设置为你想要的值。另外考虑：

- Safari → 设置 → 标签页 → 设置"关闭标签页时" → "自动关闭"
- Safari → 开发 → 清空缓存（如果开启了开发菜单）

### 3. 微信清理

微信 + WeChatAppEx = **513 MB**。如果你不使用小程序 (WeChatAppEx)，可以减少占用：

- 微信 → 设置 → 通用 → 如果不需后台运行，取消勾选"关闭窗口时保持微信在后台运行"
- 或者在不聊天时完全退出

### 4. Python 进程

两个 Python 3.11 进程使用 **292 MB**，其中一个占 **11% CPU**。检查正在运行什么：

```bash
# 查找启动它们的进程
ps aux | grep -m2 python
```

如果是闲置的 Jupyter 内核或卡住的脚本，结束它。

### 5. mihomo 代理

仅占用 36 MB / 0.9% CPU — 正常，无需操作。

### 6. 通用清理（快速见效）

```bash
# 清空系统缓存（安全）
sudo purge

# Brew 清理
brew cleanup -s

# 清空用户日志
rm -rf ~/Library/Caches/* 2>/dev/null

# 检查启动代理（登录时启动的服务）
brew services list
```

### 7. 磁盘 — 54 GB 可用并非危急，但值得关注

```bash
# 查找大文件
du -sh ~/Library/Caches ~/Downloads ~/.Trash 2>/dev/null
```

---

**总结：** 你最大的收益来自 (1) TabsKiller 保持标签页 ≤ 10（每个避免的标签页 ≈ 节省 500 MB），以及 (2) 不在使用时关闭微信可节省约 500 MB。两者合计可释放约 1.5 GB 空间，使你在 16 GB 内存下无需使用交换内存。
