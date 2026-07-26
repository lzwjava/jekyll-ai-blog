---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在PowerToys中交换Caps Lock和Ctrl键
translated: true
type: note
---

问题：**在 PowerToys 中，如何在 Windows 上交换大写锁定键和控制键？**

答案：

使用 **PowerToys 键盘管理器** → **重映射按键**。PowerToys 支持通过创建两个映射来交换按键。（[Microsoft Learn][1]）

步骤：

1. 打开 **PowerToys**
2. 进入：

```
键盘管理器
    → 重映射按键
```

3. 点击：

```
+ 添加按键重映射
```

4. 添加以下两个映射：

| 按键       | 映射为         |
| ---------- | -------------- |
| Caps Lock  | 左 Ctrl        |
| 左 Ctrl    | Caps Lock      |

示例：

```
Caps Lock  →  Ctrl（左）
Ctrl（左） → Caps Lock
```

5. 点击 **确定** / **应用**

PowerToys 会提示某个按键正在被重新分配。确认该操作。（[Microsoft Learn][1]）

6. 确保：

```
PowerToys 设置
    → 常规
    → 开机自启动 = 开启
```

因为键盘管理器需要在 PowerToys 运行时才能工作。（[GitHub][2]）

对于程序员来说，更常见的设置是：

```
Caps Lock → Ctrl
左 Ctrl → Ctrl（保持正常）
```

因为 Caps Lock 在人体工学位置上更适合执行 `Ctrl+C`、`Ctrl+V`、`Ctrl+A`、终端快捷键、Vim、Emacs 等操作。

如果你需要**真正的硬件级交换**（在 Windows 启动前、BIOS、Linux 等环境中生效），请使用键盘固件工具（如 QMK/VIA）或注册表扫描码映射，而不是 PowerToys。

[1]: https://learn.microsoft.com/en-us/windows/powertoys/keyboard-manager?utm_source=chatgpt.com "使用 PowerToys 键盘管理器重映射按键和快捷键 | Microsoft Learn"
[2]: https://github.com/microsoft/PowerToys/wiki/Keyboard-Manager-Overview/c339bd7b3fa4bc152bbb8fcf2f96a696076ecc84?utm_source=chatgpt.com "键盘管理器概述 · microsoft/PowerToys Wiki · GitHub"
