---
audio: false
generated: true
lang: zh
layout: post
title: Ubuntu Linux 硬件信息
translated: true
type: note
---

要在 Ubuntu Linux 系统上获取笔记本电脑硬件的全面信息（内存、CPU 等），您可以使用终端命令和工具的组合。以下是获取详细系统信息的分步指南：

---

### 1. 查看 CPU 信息
获取 CPU 详细信息（处理器类型、速度、核心数等）：
- 打开终端（Ctrl + Alt + T）。
- 运行以下命令：
  ```bash
  lscpu
  ```
  - **输出**：显示 CPU 架构、核心数、线程数、时钟速度、缓存大小等。
- 如需更详细的 CPU 信息（包括型号名称）：
  ```bash
  cat /proc/cpuinfo
  ```
  - 查看 `model name`、`cpu MHz` 和 `cpu cores` 等字段。

---

### 2. 查看 RAM（内存）信息
查看总内存和已用内存：
- 运行：
  ```bash
  free -h
  ```
  - **输出**：以人类可读格式（如 GB 或 MB）显示总内存、已用内存和可用内存。
- 获取详细内存信息（如类型、速度和插槽）：
  ```bash
  sudo dmidecode -t memory
  ```
  - **输出**：提供物理内存的详细信息，如大小、类型（如 DDR4）、速度和插槽使用情况。需要 root 权限。

---

### 3. 查看存储（HDD/SSD）信息
获取存储设备详细信息：
- 运行：
  ```bash
  lsblk
  ```
  - **输出**：列出所有块设备（如 SSD、HDD）及其大小和挂载点。
- 获取磁盘详细信息：
  ```bash
  sudo fdisk -l
  ```
  - **输出**：显示磁盘分区和大小。需要 root 权限。
- 检查磁盘类型（如 HDD 或 SSD）和型号：
  ```bash
  sudo hdparm -I /dev/sda
  ```
  - 将 `/dev/sda` 替换为您的磁盘设备（使用 `lsblk` 查找）。

---

### 4. 查看 GPU（显卡）信息
获取显卡详细信息：
- 运行：
  ```bash
  lspci | grep -i vga
  ```
  或
  ```bash
  lspci | grep -i nvidia
  ```
  - **输出**：显示显卡型号（如 Intel、NVIDIA、AMD）。
- 获取更详细的 GPU 信息：
  ```bash
  glxinfo | grep "OpenGL renderer"
  ```
  - 需要安装 `mesa-utils` 包（如果未安装，请运行 `sudo apt install mesa-utils`）。
- 对于 NVIDIA GPU，使用：
  ```bash
  nvidia-smi
  ```
  - **输出**：显示 GPU 使用情况、驱动版本和显存（如果已安装 NVIDIA 驱动）。

---

### 5. 查看系统概览
获取系统全面概览（CPU、内存、主板等）：
- 运行：
  ```bash
  sudo lshw
  ```
  - **输出**：列出详细的硬件信息，包括 CPU、内存、存储等。使用 `sudo lshw -short` 可查看简洁版本。
- 或者安装并使用 `hardinfo` 图形界面：
  ```bash
  sudo apt install hardinfo
  hardinfo
  ```
  - **输出**：打开 GUI 显示详细系统信息（CPU、内存、存储、传感器等）。

---

### 6. 查看 BIOS/UEFI 和主板信息
获取 BIOS/UEFI 和主板详细信息：
- 运行：
  ```bash
  sudo dmidecode -t bios
  ```
  - **输出**：显示 BIOS 版本、供应商和发布日期。
- 获取主板详细信息：
  ```bash
  sudo dmidecode -t baseboard
  ```
  - **输出**：显示主板制造商、型号和序列号。

---

### 7. 查看操作系统和内核详细信息
验证 Ubuntu 版本和内核：
- 运行：
  ```bash
  lsb_release -a
  ```
  - **输出**：显示 Ubuntu 版本和发布详细信息。
- 获取内核信息：
  ```bash
  uname -r
  ```
  - **输出**：显示 Linux 内核版本。

---

### 8. 实时监控系统资源
实时监控 CPU、内存和进程使用情况：
- 运行：
  ```bash
  top
  ```
  或
  ```bash
  htop
  ```
  - **注意**：如果未安装 `htop`，请运行 `sudo apt install htop`。它提供更友好的用户界面。

---

### 9. 使用 `inxi` 生成全面系统报告
使用单个命令收集广泛的系统信息：
- 安装 `inxi`：
  ```bash
  sudo apt install inxi
  ```
- 运行：
  ```bash
  inxi -Fxz
  ```
  - **输出**：提供详细报告，包括 CPU、内存、GPU、存储、网络等。`-F` 标志生成完整报告，`-x` 添加额外细节，`-z` 过滤敏感信息。

---

### 示例输出（使用 `inxi -Fxz`）
```plaintext
系统：    主机: ubuntu-laptop 内核: 5.15.0-73-generic x86_64 位: 64 桌面: GNOME 42.0
           发行版: Ubuntu 22.04.2 LTS (Jammy Jellyfish)
机器：    类型: 笔记本电脑 系统: Dell 产品: Inspiron 15 版本: N/A 序列号: <filter>
           主板: Dell 型号: 0XYZ 序列号: <filter> UEFI: Dell 版本: 1.2.3 日期: 2023/05/10
CPU：      信息: 8核 型号: Intel Core i7-12700H 位: 64 类型: MT MCP 缓存: L2: 11.5 MiB
           速度: 2500 MHz 最小/最大: 400/4700 MHz 核心速度 (MHz): 1: 2500 2: 2400 ...
内存：     RAM: 总计: 15.5 GiB 已用: 3.2 GiB (20.6%)
           阵列-1: 容量: 32 GiB 插槽: 2 EC: 无
           设备-1: DIMM A 大小: 8 GiB 速度: 3200 MT/s 类型: DDR4
           设备-2: DIMM B 大小: 8 GiB 速度: 3200 MT/s 类型: DDR4
显卡：     设备-1: Intel Alder Lake-P 集成显卡 驱动: i915 版本: 内核
           设备-2: NVIDIA GA107M [GeForce RTX 3050 Mobile] 驱动: nvidia 版本: 535.54.03
           显示: x11 服务端: X.Org 版本: 1.21.1.4 驱动: X: 已加载: modesetting,nvidia
           OpenGL: 渲染器: Mesa Intel UHD Graphics (ADL-S GT2) 版本: 4.6 Mesa 23.0.4
驱动器：   本地存储: 总计: 512 GiB 已用: 120 GiB (23.4%)
           ID-1: /dev/nvme0n1 供应商: Samsung 型号: SSD 970 EVO Plus 500GB 大小: 512 GiB
...
```

---

### 注意事项
- 某些命令（如 `dmidecode`、`fdisk`）需要 root 权限（`sudo`）。
- 如果命令未安装（如 `inxi`、`htop`、`mesa-utils`），请使用 `sudo apt install <包名>` 安装。
- 如需图形化工具，可使用 `hardinfo` 或 Ubuntu 预装的 `gnome-system-monitor` 提供友好界面。
- 如需特定详细信息（如电池信息、网络适配器），请告知我，我可以提供额外命令。

如果您需要帮助解读输出或想重点关注特定组件，请随时告知！
