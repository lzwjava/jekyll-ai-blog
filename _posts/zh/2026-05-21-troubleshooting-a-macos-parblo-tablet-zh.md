---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS Parblo数位板故障排除
translated: true
type: note
---

好问题。以下是我运行的具体命令及其作用：

---

### 1. 查找应用 bundle

```
find /Applications /System/Applications ~/Applications -iname '*parblo*' -maxdepth 3
```

使用 `find` 配合 `-iname`（大小写不敏感的名称匹配）在三个标准应用目录中查找任何名为 `*parblo*` 的内容，最多深入 3 层目录。

---

### 2. 检查 launchd（自动启动服务）

```
launchctl list | grep -i parblo
```

`launchctl list` 显示所有已注册到 launchd 的用户空间服务。通过管道传给 `grep -i parblo` 过滤出与 Parblo 相关的内容。

```
sudo launchctl bootout gui/$(id -u) /Library/LaunchAgents/com.parblo.Tablet.plist
```

`bootout` 停止服务并从 launchd 中注销。`gui/$(id -u)` 指向当前用户的图形会话。路径是指定该服务的 plist 文件。

```
ls /Library/LaunchAgents /Library/LaunchDaemons -name '*parblo*'
```

`LaunchAgents` = 用户级自动启动；`LaunchDaemons` = 系统级（root）自动启动。

---

### 3. 检查二进制架构（Intel vs ARM）

```
file /Applications/ParbloTablet/.../ParbloTabletDriver
```

`file` 检查二进制的 Mach-O 头部，并告知是 `x86_64`（Intel）、`arm64`（Apple Silicon）还是包含两者的通用二进制。

---

### 4. 读取 Info.plist（版本、构建信息）

```
defaults read /Applications/.../Info.plist
```

以 JSON 格式输出整个 plist。我查看了 `CFBundleShortVersionString`（v3.7.1）、`DTXcode`（10.3）、`DTSDKName`（macosx10.14）和 `LSMinimumSystemVersion`（10.10）以了解构建的陈旧程度。

---

### 5. 检查 brew services

```
brew services info ollama  (针对 ollama)
brew services list | grep -i parblo  (针对 parblo)
```

显示 Homebrew 是否管理该服务以及其加载/运行状态。

---

### 6. 检查 USB / 连接的硬件

```
system_profiler SPUSBDataType | grep -A 10 -i 'parblo\|tablet\|drawing'
```

导出所有 USB 连接的设备，并搜索与数位板相关的条目。

---

### 7. 检查登录项（系统设置）

```
osascript -e 'tell application "System Events" to get the name of every login item'
```

通过 `osascript` 运行 AppleScript 查询 System Events，获取用户的登录项列表（即你在系统设置 > 通用 > 登录项中看到的列表）。

---

### 8. 检查环境变量

```
env | grep -i ollama
```

搜索所有环境变量中与 OLLAMA_（或 PARBLO_）相关的变量。

---

### 9. 检查监听端口

```
lsof -i :11434
lsof -i -P | grep -i parblo
```

`lsof -i :PORT` 显示特定端口上正在监听的内容（11434 = Ollama 默认端口）。`lsof -i -P` 加上 `-P` 禁用端口名称解析，以提高速度和准确性。

---

### 10. 检查内核与系统扩展（深层系统钩子）

```
kextstat | grep -i parblo
systemextensionsctl list | grep -i parblo
```

`kextstat` 列出已加载的内核扩展（非常深层，误删可能导致系统崩溃）。`systemextensionsctl` 显示更新类型的系统扩展（网络过滤器、DriverKit 驱动程序）。

---

### 11. 检查包收据

```
pkgutil --pkgs | grep -i parblo
ls /private/var/db/receipts/*parblo*
```

`pkgutil --pkgs` 列出系统安装器注册的所有包。收据也以 `.plist` 文件形式存储在 `/private/var/db/receipts/` 中。

---

### 12. 检查用户库缓存/配置位置

```
ls ~/Library/Preferences/com.parblo*
ls ~/Library/Caches/com.parblo*
ls ~/Library/Application\ Support/Parblo*
ls ~/Library/Containers/com.parblo*
ls ~/Library/Group\ Containers/*parblo*
ls ~/Library/Saved\ Application\ State/*parblo*
```

标准的 macOS 位置，应用在此存储数据——偏好设置、缓存、应用数据、沙盒容器、共享群组容器以及窗口状态。

---

### 13. 检查废纸篓

```
ls ~/.Trash/*parblo*
```

某些卸载程序仅将内容移至废纸篓，而非直接删除。

---

需要我详细讲解其中某一步吗？