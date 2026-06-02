---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 手动清理Windows程序注册表
translated: true
type: note
---

问：如果在Windows中通过删除目录而非使用卸载程序的方式删除一个程序（例如Control-M），我们该如何查找并清理相关的注册表项？

答：

当你手动删除程序（仅移除其文件夹）时，Windows仍会保留**残留数据**——主要在注册表、启动项、服务和系统文件夹中。完全清理需要细致、分步进行。

---

## 1. 了解残留数据的位置

程序遗留痕迹的典型位置：

### 注册表路径

* `HKEY_CURRENT_USER\Software\...`
* `HKEY_LOCAL_MACHINE\SOFTWARE\...`
* `HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\...`（适用于64位系统上的32位应用）
* `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services`（适用于服务类程序如Control-M）

---

## 2. 使用注册表编辑器 (regedit)

### 分步操作：

1. 按 `Win + R`
2. 输入 `regedit`
3. 使用 **编辑 → 查找**（或按 `Ctrl + F`）
4. 搜索：
   * 程序名（如 `Control-M`）
   * 厂商名（如 BMC，如果相关）
5. 小心删除相关键值

👉 按 `F3` 跳转至下一个匹配项并重复。

⚠️ 请谨慎操作：
* 仅删除明确与该程序相关的条目
* 错误删除可能导致Windows或其他应用程序损坏

---

## 3. 检查已安装程序列表（残留条目）

即使文件已删除，程序可能仍显示在“程序和功能”中：

注册表位置：
* `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall`

如果程序仍列在其中但实际已不存在，可删除对应的键。

---

## 4. 移除服务（对于Control-M等工具很重要）

如果程序安装了Windows服务：

### 检查方法：
* 运行 `services.msc`
* 查找相关服务名称

### 通过命令行移除：
```bash
sc delete "服务名称"
```

或检查注册表：
* `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services`

---

## 5. 清理启动项

检查：
* 任务管理器 → 启动选项卡
* 注册表：
  * `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
  * `HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run`

---

## 6. 删除计划任务

1. 打开任务计划程序 (`taskschd.msc`)
2. 查找与该程序相关的任务
3. 删除它们

---

## 7. 清理残留文件

检查这些文件夹：
* `C:\Program Files\`
* `C:\Program Files (x86)\`
* `C:\ProgramData\`
* `C:\Users\<你的用户名>\AppData\Local\`
* `C:\Users\<你的用户名>\AppData\Roaming\`

---

## 8. 使用工具（更安全快捷）

相比于手动清理，可使用工具扫描残留：
* CCleaner（注册表清理器）
* Revo Uninstaller（深度扫描模式）
* Geek Uninstaller

这些工具：
* 扫描注册表与文件系统
* 检测残留条目
* 降低误删风险

---

## 9. 高级技巧（适用于专家）

使用：
* `Process Monitor`（来自Microsoft Sysinternals）
* 在删除前按进程名过滤（如果程序仍安装）
* 捕获所有注册表/文件交互记录

这能生成**程序使用的精确映射表**

---

## 核心要点

手动删除程序文件夹属于**不完整清理**，因为：
* Windows使用**分布式配置模型**（注册表 + 服务 + 计划任务）
* 安装程序通常将数据分散在系统各处

---

## 实用建议

如果程序已删除：
1. 尝试重新安装
2. 然后通过正确方式卸载
3. 使用Revo等工具进行深度清理

这通常比手动查找更快速安全。

---

如果你需要，我可以为你详细说明**Control-M实际清理清单**（这是一个包含服务、代理和端口的复杂企业级工具）。
