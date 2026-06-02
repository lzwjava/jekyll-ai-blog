---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Xcode 磁盘空间不足修复指南
translated: true
type: note
---

我会搜索有关此 Xcode 错误的更多信息，以为您提供全面解释。让我搜索有关 Xcode 项目编译期间 SDK 错误的更具体信息。---

**问题：** 在 iOS Xcode 项目中，“Error while searching for Xcode SDK: No space left on device” 错误是什么意思？

**答案：**

## 错误解释

错误“Error while searching for Xcode SDK: No space left on device”表示在 Xcode 构建过程中，您的 Mac 硬盘可用磁盘空间已用尽。此错误发生在 Xcode 尝试将临时构建文件、中间构建数据或 SDK 相关文件写入磁盘时，但剩余存储空间不足。

## 根本原因

该错误通常由于以下原因发生：

1. **磁盘空间不足**：您的 Mac 存储已满或几乎已满，阻止 Xcode 写入必要的构建文件
2. **Xcode 缓存积累过多**：Xcode 的 DerivedData 文件夹包含中间构建文件、索引和日志，随着时间推移可能积累数 GB 甚至数百 GB 的数据
3. **设备支持文件**：为每个使用模拟器测试的 iOS 版本创建 iOS 设备支持文件夹，这些文件夹会随着时间显著积累
4. **模拟器缓存**：旧模拟器版本和缓存的模拟器数据会占用大量存储空间
5. **构建归档**：为每个发布版本生成的归档会随着时间积累到很大尺寸

## 解决方案

### 快速修复 - 清理 Xcode 缓存

最有效的解决方案是删除 Xcode 的缓存文件，这可以释放 50GB 或更多的磁盘空间：

1. **删除 Derived Data**：
   - 打开 Finder → 转到文件夹 (Cmd+Shift+G)
   - 粘贴：`~/Library/Developer/Xcode/DerivedData/`
   - 删除所有内容（安全删除 - Xcode 会重新生成它们）

2. **清除 Module Cache**：
   - 导航至：`~/Library/Developer/Xcode/DerivedData/ModuleCache`
   - 删除所有内容

3. **移除旧设备支持文件**：
   - 导航至：`~/Library/Developer/Xcode/iOS DeviceSupport/`
   - 删除您不再需要的 iOS 版本支持文件夹

4. **删除不必要的模拟器**：
   - 导航至：`~/Library/Developer/CoreSimulator/Devices/`
   - 移除您不使用的模拟器文件夹

5. **清除通用 Xcode 缓存**：
   - 导航至：`~/Library/Caches/com.apple.dt.Xcode`
   - 删除内容

### 使用 Terminal 命令

您可以使用 Terminal 移除 DerivedData：`rm -rf ~/Library/Developer/Xcode/DerivedData/*`

### 通过 Xcode 界面

您可以通过 Xcode 删除 derived data：Xcode → 偏好设置 → 位置 → Derived Data → 点击箭头 → 在 Finder 中显示

## 预防提示

- 定期清理 Xcode 缓存（建议每季度或每半年一次）
- 删除您不再需要的归档
- 移除您不再支持的 iOS 版本的模拟器文件
- 监控 Mac 的可用磁盘空间（开发时目标保持至少 20-50GB 可用空间）

清理后，重新构建您的项目。Xcode 将重新生成必要的缓存文件，首次构建可能需要更长时间，但后续构建将更快。

---

**参考资料：**

- https://macpaw.com/how-to/clear-xcode-cache
- https://www.swiftyplace.com/blog/how-to-clean-xcode-on-your-mac
- https://medium.com/@aykutkardes/understanding-and-fast-way-to-reduce-xcode-space-75e07acf6b1e
- https://medium.com/@nqtuan86/clean-mac-storage-for-xcodes-users-5fbb32239aa5
- https://medevel.com/clean-xcode-cache/
- https://dev.to/germanxp/cleaning-your-xcodes-garbage-2g6g
