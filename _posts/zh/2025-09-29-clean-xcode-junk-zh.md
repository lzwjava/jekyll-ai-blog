---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 清理Xcode垃圾释放磁盘空间
translated: true
type: note
---

好问题 👍 Xcode（以及 iOS 模拟器）随着时间推移会积累大量垃圾——构建缓存、衍生数据、模拟器设备、设备支持文件、日志等。清理它们可以释放数 GB 空间。以下是系统化的清理方法：

---

### 1. 清理衍生数据（构建缓存）

这会移除旧的构建产物、中间文件和索引数据。

* 通过 **Xcode 图形界面**：
  `Xcode → Settings → Locations → Derived Data → 点击箭头图标 → 删除文件夹`
* 通过 **终端命令**：

  ```bash
  rm -rf ~/Library/Developer/Xcode/DerivedData/*
  ```

---

### 2. 清理模拟器数据

* 重置或删除模拟器内容：

  ```bash
  xcrun simctl erase all
  ```

  （会清除应用及数据，但保留设备定义）

* 移除所有未使用的模拟器设备（如果积累了大量旧版 iOS 模拟器）：

  ```bash
  xcrun simctl delete unavailable
  ```

* 删除所有模拟器设备（谨慎操作，将清除全部数据）：

  ```bash
  xcrun simctl delete all
  ```

* 手动删除占用空间较大的目录：

  ```bash
  rm -rf ~/Library/Developer/CoreSimulator/Devices/*
  ```

---

### 3. 移除旧版设备支持文件

当连接实体设备时，Xcode 会下载对应 iOS 版本的调试符号文件，这些文件会不断累积。

```bash
rm -rf ~/Library/Developer/Xcode/iOS\ DeviceSupport/*
```

---

### 4. 清理归档文件

通过 “Product → Archive” 生成的应用归档文件占用空间较大。

* 在 Xcode 归档管理器中操作：Organizer → Archives → 删除旧归档
* 或通过终端命令：

  ```bash
  rm -rf ~/Library/Developer/Xcode/Archives/*
  ```

---

### 5. 清理日志文件

```bash
rm -rf ~/Library/Developer/Xcode/DocumentationCache/*
rm -rf ~/Library/Developer/Xcode/ios device logs/*
rm -rf ~/Library/Logs/CoreSimulator/*
```

---

### 6. 清理衍生索引与模块缓存

```bash
rm -rf ~/Library/Developer/Xcode/DerivedDataModuleCache/*
```

---

### 7. 可选：完全重置

如果需要彻底重置 Xcode 相关缓存：

```bash
rm -rf ~/Library/Developer/Xcode/*
rm -rf ~/Library/Developer/CoreSimulator/*
```

（这将移除所有数据：模拟器、归档、衍生数据等。下次启动 Xcode 时会呈现“全新安装”状态）

---

⚠️ **注意事项**

* 执行这些命令前请确保退出 Xcode 和模拟器
* 可使用 `du -sh ~/Library/Developer/*` 查看哪些文件夹占用空间最大
* 有时在 Xcode 中执行 `Clean Build Folder` (`⇧⌘K`) 即可解决问题，但深度清理能释放更多空间

---

需要我为您提供一个**一键清理脚本**吗？可以一次性清理所有常见垃圾文件（支持可选参数配置）。
