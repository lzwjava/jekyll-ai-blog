---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Mac Spotlight 缺少已安装应用
translated: true
type: note
---

Question: 为什么 Mac Spotlight 搜索无法找到已安装的应用程序（如 VLC），而是显示“Search App Store”？如何修复？

Answer:

## 为什么 Mac Spotlight 搜索无法找到您的已安装应用程序

这是一个非常常见且众所周知的 macOS 错误，尤其是在像 macOS Sequoia (15.x) 这样的更新之后。根本原因是 **corrupted or incomplete Spotlight index** — Spotlight 的内部数据库丢失了对您已安装应用程序的跟踪，因此它会回退到建议 App Store。

---

## 修复方法（按顺序尝试）

### ✅ 修复 1：检查 Spotlight 设置中“Applications”是否启用

1. 打开 **System Settings** → **Spotlight**
2. 确保搜索结果列表中 **Applications** 已选中
3. 即使已经选中 — **取消选中，然后重新选中**
4. **重启您的 Mac**

此切换技巧即可为许多用户解决问题。

---

### ✅ 修复 2：重建 Spotlight 索引（Apple 推荐）

这会强制 Spotlight 重新扫描您的 Applications 文件夹：

1. 转到 **System Settings → Spotlight → Search Privacy**（或“Spotlight Privacy”按钮）
2. 点击 **`+`** 按钮并添加您的 **Applications 文件夹**（或整个 `Macintosh HD`）
3. 等待几秒钟
4. 选中它并点击 **`–`** 删除
5. 点击 **Done**，然后退出 System Settings
6. 等待重新索引完成（您会在 Spotlight 中看到进度条）

---

### ✅ 修复 3：通过 Terminal 重建索引（更彻底）

打开 **Terminal**（在 `/Applications/Utilities/Terminal` 中找到）并运行：

```bash
sudo mdutil -E /
```

- 输入管理员密码时键入（输入时不会显示任何内容 — 这是正常的）
- 这会擦除并完全重建 Spotlight 索引
- 给予 15–30 分钟；即使在完全完成之前，应用程序也应该很快出现

---

### ✅ 修复 4：通过 Terminal 强制完全重新索引（核选项）

如果修复 3 无效，按顺序使用这两个命令：

```bash
sudo mdutil -Eai off
sudo mdutil -Eai on
```

然后重启您的 Mac。这会完全擦除并重建所有索引数据。

---

### ✅ 修复 5：手动打开应用程序一次

一些用户报告，在 **手动打开应用程序一次**（通过 Finder 或 Launchpad）后，它就会再次出现在 Spotlight 中。这是一个临时解决方法，不是真正的修复，但如果您赶时间则很有用。

---

## 总结表格

| 修复方法 | 难度 | 适用情况 |
|----------|------|----------|
| 切换“Applications”复选框 + 重启 | 简单 | 大多数情况 |
| 在 Search Privacy 中添加/移除文件夹 | 简单 | 大多数情况 |
| 在 Terminal 中运行 `sudo mdutil -E /` | 中等 | 持久问题 |
| `mdutil -Eai off/on` + 重启 | 中等 | 顽固情况 |
| 手动打开应用程序一次 | 快速临时方案 | 单个应用程序 |

---

## 为什么这个问题反复出现？

这是 **macOS Sequoia (15.x)** 和某些早期版本的已知错误。Spotlight 可能会丢失对第三方应用程序（如 VLC、Firefox 等）的索引，尤其是在 macOS 更新后或 Mac 在电池供电时进入睡眠状态。Apple 已在点版本中发布了部分修复，但某些用户的问题会重新出现。

References:

- [Apple Support – Rebuild the Spotlight Index](https://support.apple.com/en-us/102321)
- [Apple Community – Spotlight doesn't find some apps on Mac](https://discussions.apple.com/thread/255834181)
- [MacRumors Forum – Spotlight not showing apps in results](https://forums.macrumors.com/threads/spotlight-not-showing-apps-in-results.2442417/)
- [How-To Geek – Apps Not Showing in Spotlight on Your Mac](https://www.howtogeek.com/apps-not-showing-in-spotlight-on-your-mac/)
- [SuperEasyApps – How to Fix Spotlight Search on Mac](https://blog.supereasyapps.com/how-to-fix-spotlight-search-on-mac-spotlight-search-not-showing-apps/)
