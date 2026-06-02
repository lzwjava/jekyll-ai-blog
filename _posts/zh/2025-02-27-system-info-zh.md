---
audio: false
generated: true
lang: zh
layout: post
title: macOS 系统信息
translated: true
type: note
---

要获取 macOS 的系统信息，您可以使用多种内置工具和命令。以下是获取各类系统信息的方法：

### 1. **系统信息工具**
系统信息应用提供 Mac 硬件与软件的全面概览。

- 按下 `Cmd + Space` 打开 **聚焦搜索**，输入“系统信息”后按回车键。
- 或者通过 **苹果菜单** > **关于本机** > **系统报告** 打开。

### 2. **关于本机**
这里提供 Mac 配置规格的快速概览。

- 点击屏幕左上角的 **苹果菜单**。
- 选择 **关于本机**。这里会显示基础信息，包括 macOS 版本、处理器、内存和序列号。

### 3. **终端命令**
您可以使用终端通过各类命令获取详细系统信息。

- 通过 `应用程序` > `实用工具` > `终端` 打开终端，或在聚焦搜索中查找。

#### 基础系统信息
```sh
system_profiler SPHardwareDataType
```

#### 详细系统信息
```sh
system_profiler
```

#### 处理器信息
```sh
sysctl -n machdep.cpu.brand_string
```

#### 内存信息
```sh
sysctl hw.memsize
```

#### 磁盘使用情况
```sh
df -h
```

#### 网络信息
```sh
ifconfig
```

#### 电池信息（适用于笔记本电脑）
```sh
pmset -g batt
```

#### 已安装软件列表
```sh
ls /Applications
```

#### macOS 版本信息
```sh
sw_vers
```

#### 用户信息
```sh
id
```

#### 运行进程列表
```sh
ps aux
```

#### 已安装的 Brew 软件包列表
```sh
brew list
```

#### 已安装的 Pip 软件包列表
```sh
pip list
```

#### 已安装的 Gem 软件包列表
```sh
gem list
```

### 4. **活动监视器**
该应用实时显示 Mac 的 CPU、内存、能耗、磁盘和网络使用情况。

- 通过 `应用程序` > `实用工具` > `活动监视器` 打开，或在聚焦搜索中查找。

### 5. **磁盘工具**
该应用提供存储设备的相关信息。

- 通过 `应用程序` > `实用工具` > `磁盘工具` 打开，或在聚焦搜索中查找。

### 6. **第三方工具**
还有如 **iStat Menus** 和 **CoconutBattery** 等第三方应用程序，可提供详细的系统信息和监控功能。

通过以上方法，您可以收集到 macOS 系统的各类信息。
