---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 快速掌握 ADB 命令
translated: true
type: note
---

ADB 是一个功能强大的命令行工具，让你能够与 Android 设备进行通信。它是 Android SDK Platform Tools 的一部分，对于开发者、高级用户以及任何想要深度控制其 Android 设备的人来说都是必不可少的。

## Installing ADB

**Windows/Mac/Linux：**
从 Android 开发者网站下载 Platform Tools 并将文件夹添加到系统 PATH 中。你可以通过在终端运行 `adb version` 来验证安装是否成功。

## Core Concepts

ADB 采用 client-server 架构，包含三个组成部分：client（在你的电脑上运行）、daemon/server（在 Android 设备上运行）以及 server 进程（管理 client 与 daemon 之间的通信）。

## Essential Commands

**Device Connection & Management**

`adb devices` - 列出所有已连接的设备及其序列号和连接状态。添加 `-l` 可查看包括设备型号在内的更详细信息。

`adb connect <ip_address>:5555` - 通过 WiFi 连接到设备（需要初始 USB 设置以启用 wireless debugging）。

`adb disconnect` - 断开与无线设备的连接。

`adb kill-server` - 终止 ADB server 进程。在 ADB 无响应时非常有用。

`adb start-server` - 手动启动 ADB server。

**Working with Multiple Devices**

当连接了多个设备时，你需要指定目标设备：

`adb -s <serial_number> <command>` - 使用序列号将命令发送到特定设备。

`adb -d <command>` - 以唯一连接的 USB 设备为目标。

`adb -e <command>` - 以唯一运行的 emulator 为目标。

## File Operations

`adb push <local_path> <device_path>` - 将文件从电脑复制到设备。例如：`adb push photo.jpg /sdcard/Pictures/`

`adb pull <device_path> <local_path>` - 将文件从设备复制到电脑。例如：`adb pull /sdcard/Documents/file.txt ./`

`adb pull <device_path>` - 如果未指定本地路径，则 pull 到当前目录。

## Shell Access

`adb shell` - 在设备上打开一个交互式 shell，让你能够通过命令行访问 Android 系统。

`adb shell <command>` - 在设备上执行单个命令而不打开交互式会话。例如：`adb shell ls /sdcard/`

**Useful Shell Commands：**

`adb shell pm list packages` - 列出所有已安装的包。添加 `-3` 仅查看第三方应用，`-s` 查看系统应用。

`adb shell pm path <package_name>` - 显示应用的安装路径。

`adb shell dumpsys battery` - 显示电池信息。

`adb shell wm size` - 显示或设置屏幕分辨率。

`adb shell wm density` - 显示或设置屏幕密度 (DPI)。

## App Management

`adb install <path_to_apk>` - 安装 APK 文件。添加 `-r` 替换安装并保留数据，`-g` 授予所有权限。

`adb uninstall <package_name>` - 卸载应用。添加 `-k` 以保留数据和缓存目录。

`adb shell pm clear <package_name>` - 清除所有应用数据（相当于设置中的“清除数据”）。

`adb shell am start -n <package_name>/<activity_name>` - 启动特定的 app activity。

`adb shell am force-stop <package_name>` - 强制停止应用程序。

## Logging & Debugging

`adb logcat` - 实时显示设备的日志输出。这对于调试至关重要。

`adb logcat -c` - 清除日志缓冲区。

`adb logcat -d > log.txt` - 将整个日志转储到文件中。

`adb logcat *:E` - 仅显示错误消息（优先级：V=Verbose, D=Debug, I=Info, W=Warning, E=Error, F=Fatal）。

`adb logcat -s TAG_NAME` - 按特定标签过滤日志。

`adb bugreport <path>` - 生成一个包含日志、系统信息和诊断数据的完整 bug report ZIP 文件。

## System Control

`adb reboot` - 正常重启设备。

`adb reboot bootloader` - 重启进入 bootloader/fastboot 模式。

`adb reboot recovery` - 重启进入 recovery 模式。

`adb root` - 以 root 权限重启 ADB daemon（仅适用于已 root 的设备或 emulator）。

`adb remount` - 将 /system 分区重新挂载为可写（需要 root）。

## Screen Interaction

`adb shell input text "your text"` - 输入文本（对自动化很有用）。

`adb shell input keyevent <keycode>` - 模拟按键。常用代码：3=Home, 4=Back, 26=Power, 24=Volume Up, 25=Volume Down。

`adb shell input tap <x> <y>` - 在特定坐标模拟屏幕点击。

`adb shell input swipe <x1> <y1> <x2> <y2> <duration>` - 模拟滑动操作。

`adb shell screencap /sdcard/screenshot.png` - 截取屏幕截图并保存到设备。

`adb shell screenrecord /sdcard/demo.mp4` - 录制屏幕（Ctrl+C 停止）。添加 `--time-limit <seconds>` 设置时长。

## Backup & Restore

`adb backup -all -f backup.ab` - 创建所有应用和数据的完整备份。添加 `-apk` 以包含 APK 文件，`-nosystem` 以排除系统应用。

`adb restore backup.ab` - 从备份文件恢复。

## Port Forwarding

`adb forward tcp:<local_port> tcp:<device_port>` - 将本地端口转发到设备端口。例如：`adb forward tcp:8080 tcp:8080`

`adb reverse tcp:<device_port> tcp:<local_port>` - 反向端口转发（设备到电脑）。

## Advanced Usage

**Sideload Updates：**
`adb sideload <update.zip>` - 从 recovery 模式安装 OTA 更新或 custom ROMs。

**Working with System Properties：**
`adb shell getprop` - 列出所有系统属性。

`adb shell setprop <property> <value>` - 设置系统属性（通常需要 root）。

**Database Access：**
`adb shell "run-as <package_name> cat databases/database.db" > local_copy.db` - 复制应用数据库以便检查。

## Common Troubleshooting

如果无法检测到设备，请检查“开发者选项”中是否启用了 USB debugging，尝试不同的 USB 线缆/端口，确保安装了正确的驱动程序 (Windows)，或者运行 `adb kill-server` 然后运行 `adb start-server`。

对于 "unauthorized" 错误，请检查设备屏幕上的授权提示，并确保勾选“始终允许通过这台计算机”。

ADB 是一个极其强大的工具，为 Android 开发、测试、自动化和定制开启了广泛的可能性。上述命令涵盖了大多数常见用例，但通过 `adb help` 和 `adb shell` 命令还可以获得更多专业选项。
