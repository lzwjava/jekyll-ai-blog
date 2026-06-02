---
audio: false
generated: true
lang: en
layout: post
title: System Information on macOS
translated: false
type: note
---

To get system information on your macOS, you can use several built-in tools and commands. Here are some methods to retrieve various types of system information:

### 1. **System Information Utility**

The System Information app provides a comprehensive overview of your Mac's hardware and software.

- Open **Spotlight Search** by pressing `Cmd + Space` and type "System Information," then press Enter.
- Alternatively, you can open it from the **Apple menu** > **About This Mac** > **System Report**.

### 2. **About This Mac**

This provides a quick overview of your Mac's specifications.

- Click the **Apple menu** in the top-left corner of the screen.
- Select **About This Mac**. This will show basic information like the macOS version, processor, memory, and serial number.

### 3. **Terminal Commands**

You can use the Terminal to get detailed system information using various commands.

- Open **Terminal** from `Applications` > `Utilities` > `Terminal` or by searching for it in Spotlight.

#### Basic System Information

```sh
system_profiler SPHardwareDataType
```

#### Detailed System Information

```sh
system_profiler
```

#### CPU Information

```sh
sysctl -n machdep.cpu.brand_string
```

#### Memory Information

```sh
sysctl hw.memsize
```

#### Disk Usage

```sh
df -h
```

#### Network Information

```sh
ifconfig
```

#### Battery Information (for laptops)

```sh
pmset -g batt
```

#### List of Installed Software

```sh
ls /Applications
```

#### macOS Version

```sh
sw_vers
```

#### User Information

```sh
id
```

#### List of Running Processes

```sh
ps aux
```

#### List of Installed Brew Packages

```sh
brew list
```

#### List of Installed Pip Packages

```sh
pip list
```

#### List of Installed Gem Packages

```sh
gem list
```

### 4. **Activity Monitor**

This app provides real-time information about your Mac's CPU, memory, energy, disk, and network usage.

- Open **Activity Monitor** from `Applications` > `Utilities` > `Activity Monitor` or by searching for it in Spotlight.

### 5. **Disk Utility**

This app provides information about your storage devices.

- Open **Disk Utility** from `Applications` > `Utilities` > `Disk Utility` or by searching for it in Spotlight.

### 6. **Third-Party Tools**

There are also third-party applications like **iStat Menus** and **CoconutBattery** that provide detailed system information and monitoring capabilities.

By using these methods, you can gather a wide range of system information on your macOS.
