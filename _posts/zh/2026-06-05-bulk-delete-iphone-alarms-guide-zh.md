---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 批量删除iPhone闹钟指南
translated: true
type: note
---

问题：如何使用 macOS 和 Xcode 批量删除 iPhone 上的数百个闹钟？

回答：

**直接回答：** 标准的 Xcode 工作流程无法直接删除 iPhone 闹钟。但根据你的承受能力，有以下实用选项。

## 选项 1：使用提醒事项 App（最简洁）

如果你的闹钟已同步到 iCloud 提醒事项，可以将其迁移到那里并批量删除：

```bash
# 在 macOS 上，打开提醒事项.app
# 如果闹钟已通过 iCloud 同步，它们会以提醒事项形式出现
# 全选（Cmd+A）并删除
```

此方法适用于闹钟已绑定 Apple 生态的情况。检查 iPhone 设置 → [你的姓名] → iCloud → 提醒事项。

## 选项 2：直接访问 SQLite 数据库

iPhone 将闹钟存储在 `/Library/Preferences/com.apple.mobiletimer.plist` 及关联数据库文件中。未越狱时，访问需要：

**通过 libimobiledevice + 脚本：**

```bash
# 安装 libimobiledevice
brew install libimobiledevice

# 挂载 iPhone 文件系统
mkdir -p /tmp/iphone_mount
ifuse /tmp/iphone_mount

# 导航到闹钟存储位置
ls /tmp/iphone_mount/Library/Preferences/ | grep -i timer
ls /tmp/iphone_mount/Library/Caches/ | grep -i clock

# 对于 .plist 文件，转换并检查
python3 << 'EOF'
import plistlib
import sys

plist_path = "/tmp/iphone_mount/Library/Preferences/com.apple.mobiletimer.plist"
with open(plist_path, 'rb') as f:
    data = plistlib.load(f)

# 检查数据结构
print(f"键: {data.keys()}")
# 闹钟通常存储在 'Alarms' 键下
if 'Alarms' in data:
    print(f"闹钟数量: {len(data['Alarms'])}")
    # 清空闹钟
    data['Alarms'] = []

    with open(plist_path, 'wb') as f:
        plistlib.dump(data, f)
    print("闹钟已清空")
EOF

# 卸载
umount /tmp/iphone_mount
```

**注意：** 需要在 iPhone 上启用开发者模式（设置 → 隐私 → 开发者模式），并可能需要信任弹窗。

## 选项 3：Apple Configurator 2（图形界面，但有效）

```bash
# 通过命令行
open -a "Apple Configurator 2"
# 连接 iPhone → 设备 → 高级 → 重置 → 清除缓存数据
```

不是以代码为先，但如果 ifuse 无法工作，这是最快的方法。

## 选项 4：Xcode 调试器脚本（最可靠）

通过 USB 连接 iPhone，并使用 Xcode 的调试器自动化：

```bash
# 需要 Xcode + 已连接的设备
xcrun devicectl device list

# 如需配对设备
xcrun devicectl device pair <device_udid>

# 使用 lldb 编写删除脚本（高级）：
xcrun lldb --no-lldbinit -b \
  -o "attach <pid>" \
  -o "p [UIApplication sharedApplication]" \
  # 此方法在没有应用级访问权限时较为脆弱
```

**实际情况：** 没有 iPhone 上的配套应用时，这种方法很 hacky。

## 选项 5：编写配套自动化（最具 AI 原生性）

创建一个简单的 iOS 快捷指令自动化来删除闹钟：

```
快捷指令：删除所有闹钟
1. 从“闹钟”列表获取所有提醒事项（如果使用提醒事项）
2. 对于每个提醒事项：删除它
3. 按计划运行或通过 Siri 手动运行
```

然后从 macOS 触发：

```bash
# 从 macOS 运行 iOS 快捷指令
open "shortcuts://run-shortcut?name=Delete%20All%20Alarms"
```

## 我的建议：

**最快：** 选项 1（迁移到提醒事项，批量删除）。

**最技术性：** 选项 2（libimobiledevice + plist 操作）——需要在 iPhone 上启用开发者模式，但提供直接的文件系统访问和脚本能力。先在非关键备份上测试。

**备用方案：** 选项 3（Configurator 2）——如果 ifuse 卡住时使用。

你在哪台机器上运行？如果是 Air M2，libimobiledevice 可能需要通过 Homebrew 重新编译。如果是工作站（Linux），如果曾桥接 Android 工具，可以使用 `adb` 获得更直接的选项，但对于 iPhone，坚持使用 libimobiledevice。