---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Mastering ADB Commands Quickly
translated: false
type: note
---

ADB is a versatile command-line tool that lets you communicate with Android devices. It's part of the Android SDK Platform Tools and is essential for developers, power users, and anyone who wants deeper control over their Android device.

## Installing ADB

**Windows/Mac/Linux:**
Download the Platform Tools from the Android developer website and add the folder to your system PATH. You can verify installation by running `adb version` in your terminal.

## Core Concepts

ADB uses a client-server architecture with three components: a client (runs on your computer), a daemon/server (runs on the Android device), and a server process (manages communication between client and daemon).

## Essential Commands

**Device Connection & Management**

`adb devices` - Lists all connected devices with their serial numbers and connection state. Add `-l` for more detailed information including the device model.

`adb connect <ip_address>:5555` - Connects to a device over WiFi (requires initial USB setup to enable wireless debugging).

`adb disconnect` - Disconnects from a wireless device.

`adb kill-server` - Terminates the ADB server process. Useful when ADB becomes unresponsive.

`adb start-server` - Manually starts the ADB server.

**Working with Multiple Devices**

When multiple devices are connected, you need to specify which one to target:

`adb -s <serial_number> <command>` - Directs commands to a specific device using its serial number.

`adb -d <command>` - Targets the only connected USB device.

`adb -e <command>` - Targets the only running emulator.

## File Operations

`adb push <local_path> <device_path>` - Copies files from your computer to the device. Example: `adb push photo.jpg /sdcard/Pictures/`

`adb pull <device_path> <local_path>` - Copies files from the device to your computer. Example: `adb pull /sdcard/Documents/file.txt ./`

`adb pull <device_path>` - Pulls to your current directory if no local path is specified.

## Shell Access

`adb shell` - Opens an interactive shell on the device, giving you command-line access to the Android system.

`adb shell <command>` - Executes a single command on the device without opening an interactive session. Example: `adb shell ls /sdcard/`

**Useful Shell Commands:**

`adb shell pm list packages` - Lists all installed packages. Add `-3` for third-party apps only, `-s` for system apps.

`adb shell pm path <package_name>` - Shows the installation path of an app.

`adb shell dumpsys battery` - Displays battery information.

`adb shell wm size` - Shows or sets screen resolution.

`adb shell wm density` - Shows or sets screen density (DPI).

## App Management

`adb install <path_to_apk>` - Installs an APK file. Add `-r` to reinstall while keeping data, `-g` to grant all permissions.

`adb uninstall <package_name>` - Uninstalls an app. Add `-k` to keep the data and cache directories.

`adb shell pm clear <package_name>` - Clears all app data (equivalent to "Clear Data" in settings).

`adb shell am start -n <package_name>/<activity_name>` - Launches a specific app activity.

`adb shell am force-stop <package_name>` - Force stops an application.

## Logging & Debugging

`adb logcat` - Displays the device's log output in real-time. This is crucial for debugging.

`adb logcat -c` - Clears the log buffer.

`adb logcat -d > log.txt` - Dumps the entire log to a file.

`adb logcat *:E` - Shows only error messages (priorities: V=Verbose, D=Debug, I=Info, W=Warning, E=Error, F=Fatal).

`adb logcat -s TAG_NAME` - Filters logs by a specific tag.

`adb bugreport <path>` - Generates a comprehensive bug report ZIP file containing logs, system information, and diagnostic data.

## System Control

`adb reboot` - Reboots the device normally.

`adb reboot bootloader` - Reboots into bootloader/fastboot mode.

`adb reboot recovery` - Reboots into recovery mode.

`adb root` - Restarts ADB daemon with root permissions (only works on rooted devices or emulators).

`adb remount` - Remounts the /system partition as writable (requires root).

## Screen Interaction

`adb shell input text "your text"` - Types text (useful for automation).

`adb shell input keyevent <keycode>` - Simulates key presses. Common codes: 3=Home, 4=Back, 26=Power, 24=Volume Up, 25=Volume Down.

`adb shell input tap <x> <y>` - Simulates a screen tap at specific coordinates.

`adb shell input swipe <x1> <y1> <x2> <y2> <duration>` - Simulates a swipe gesture.

`adb shell screencap /sdcard/screenshot.png` - Takes a screenshot and saves it to the device.

`adb shell screenrecord /sdcard/demo.mp4` - Records the screen (Ctrl+C to stop). Add `--time-limit <seconds>` to set duration.

## Backup & Restore

`adb backup -all -f backup.ab` - Creates a full backup of all apps and data. Add `-apk` to include APK files, `-nosystem` to exclude system apps.

`adb restore backup.ab` - Restores from a backup file.

## Port Forwarding

`adb forward tcp:<local_port> tcp:<device_port>` - Forwards a local port to a device port. Example: `adb forward tcp:8080 tcp:8080`

`adb reverse tcp:<device_port> tcp:<local_port>` - Reverse port forwarding (device to computer).

## Advanced Usage

**Sideload Updates:**
`adb sideload <update.zip>` - Installs OTA updates or custom ROMs from recovery mode.

**Working with System Properties:**
`adb shell getprop` - Lists all system properties.

`adb shell setprop <property> <value>` - Sets a system property (usually requires root).

**Database Access:**
`adb shell "run-as <package_name> cat databases/database.db" > local_copy.db` - Copies app databases for inspection.

## Common Troubleshooting

If devices aren't detected, check USB debugging is enabled in Developer Options, try different USB cables/ports, ensure proper drivers are installed (Windows), or run `adb kill-server` then `adb start-server`.

For "unauthorized" errors, check your device screen for the authorization prompt and make sure to select "always allow from this computer."

ADB is an incredibly powerful tool that opens up extensive possibilities for Android development, testing, automation, and customization. The commands above cover most common use cases, but there are many more specialized options available through `adb help` and `adb shell` commands.
