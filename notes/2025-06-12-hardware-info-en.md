---
audio: false
generated: true
lang: en
layout: post
title: Ubuntu Linux Hardware Info
translated: false
type: note
---

To get comprehensive information about your laptop's hardware (RAM, CPU, etc.) on an Ubuntu Linux system, you can use a combination of terminal commands and tools. Below is a step-by-step guide to retrieve detailed system information:

---

### 1. Check CPU Information

To get details about your CPU (processor type, speed, cores, etc.):

- Open a terminal (Ctrl + Alt + T).
- Run the following command:

  ```bash
  lscpu
  ```

  - **Output**: Displays CPU architecture, number of cores, threads, clock speed, cache sizes, etc.
- For more detailed CPU information, including model name:

  ```bash
  cat /proc/cpuinfo
  ```

  - Look for fields like `model name`, `cpu MHz`, and `cpu cores`.

---

### 2. Check RAM (Memory) Information

To view the total and used RAM:

- Run:

  ```bash
  free -h
  ```

  - **Output**: Shows total, used, and free memory in a human-readable format (e.g., GB or MB).
- For detailed memory information (e.g., type, speed, and slots):

  ```bash
  sudo dmidecode -t memory
  ```

  - **Output**: Provides details about physical memory, such as size, type (e.g., DDR4), speed, and slot usage. Requires root privileges.

---

### 3. Check Storage (HDD/SSD) Information

To get details about your storage devices:

- Run:

  ```bash
  lsblk
  ```

  - **Output**: Lists all block devices (e.g., SSD, HDD) with their sizes and mount points.
- For detailed information about disks:

  ```bash
  sudo fdisk -l
  ```

  - **Output**: Shows disk partitions and sizes. Requires root privileges.
- To check disk type (e.g., HDD or SSD) and model:

  ```bash
  sudo hdparm -I /dev/sda
  ```

  - Replace `/dev/sda` with your disk device (find it using `lsblk`).

---

### 4. Check GPU (Graphics Card) Information

To find details about your graphics card:

- Run:

  ```bash
  lspci | grep -i vga
  ```

  or

  ```bash
  lspci | grep -i nvidia
  ```

  - **Output**: Displays the graphics card model (e.g., Intel, NVIDIA, AMD).
- For more detailed GPU information:

  ```bash
  glxinfo | grep "OpenGL renderer"
  ```

  - Requires the `mesa-utils` package (`sudo apt install mesa-utils` if not installed).
- For NVIDIA GPUs, use:

  ```bash
  nvidia-smi
  ```

  - **Output**: Shows GPU usage, driver version, and VRAM (if NVIDIA drivers are installed).

---

### 5. Check System Overview

For a comprehensive overview of your system (CPU, RAM, motherboard, etc.):

- Run:

  ```bash
  sudo lshw
  ```

  - **Output**: Lists detailed hardware information, including CPU, RAM, storage, and more. Use `sudo lshw -short` for a concise version.
- Alternatively, install and use `hardinfo` for a graphical interface:

  ```bash
  sudo apt install hardinfo
  hardinfo
  ```

  - **Output**: Opens a GUI showing detailed system information (CPU, RAM, storage, sensors, etc.).

---

### 6. Check BIOS/UEFI and Motherboard Information

To get BIOS/UEFI and motherboard details:

- Run:

  ```bash
  sudo dmidecode -t bios
  ```

  - **Output**: Shows BIOS version, vendor, and release date.
- For motherboard details:

  ```bash
  sudo dmidecode -t baseboard
  ```

  - **Output**: Displays motherboard manufacturer, model, and serial number.

---

### 7. Check Operating System and Kernel Details

To verify your Ubuntu version and kernel:

- Run:

  ```bash
  lsb_release -a
  ```

  - **Output**: Shows Ubuntu version and release details.
- For kernel information:

  ```bash
  uname -r
  ```

  - **Output**: Displays the Linux kernel version.

---

### 8. Monitor System Resources in Real-Time

To monitor CPU, RAM, and process usage in real-time:

- Run:

  ```bash
  top
  ```

  or

  ```bash
  htop
  ```

  - **Note**: Install `htop` if not present (`sudo apt install htop`). It provides a more user-friendly interface.

---

### 9. Comprehensive System Report with `inxi`

For a single command that gathers extensive system information:

- Install `inxi`:

  ```bash
  sudo apt install inxi
  ```

- Run:

  ```bash
  inxi -Fxz
  ```

  - **Output**: Provides a detailed report including CPU, RAM, GPU, storage, network, and more. The `-F` flag gives a full report, `-x` adds extra details, and `-z` filters sensitive information.

---

### Example Output (Using `inxi -Fxz`)

```plaintext
System:    Host: ubuntu-laptop Kernel: 5.15.0-73-generic x86_64 bits: 64 Desktop: GNOME 42.0
           Distro: Ubuntu 22.04.2 LTS (Jammy Jellyfish)
Machine:   Type: Laptop System: Dell product: Inspiron 15 v: N/A serial: <filter>
           Mobo: Dell model: 0XYZ serial: <filter> UEFI: Dell v: 1.2.3 date: 05/10/2023
CPU:       Info: 8-core model: Intel Core i7-12700H bits: 64 type: MT MCP cache: L2: 11.5 MiB
           Speed: 2500 MHz min/max: 400/4700 MHz Core speeds (MHz): 1: 2500 2: 2400 ...
Memory:    RAM: total: 15.5 GiB used: 3.2 GiB (20.6%)
           Array-1: capacity: 32 GiB slots: 2 EC: None
           Device-1: DIMM A size: 8 GiB speed: 3200 MT/s type: DDR4
           Device-2: DIMM B size: 8 GiB speed: 3200 MT/s type: DDR4
Graphics:  Device-1: Intel Alder Lake-P Integrated Graphics driver: i915 v: kernel
           Device-2: NVIDIA GA107M [GeForce RTX 3050 Mobile] driver: nvidia v: 535.54.03
           Display: x11 server: X.Org v: 1.21.1.4 driver: X: loaded: modesetting,nvidia
           OpenGL: renderer: Mesa Intel UHD Graphics (ADL-S GT2) v: 4.6 Mesa 23.0.4
Drives:    Local Storage: total: 512 GiB used: 120 GiB (23.4%)
           ID-1: /dev/nvme0n1 vendor: Samsung model: SSD 970 EVO Plus 500GB size: 512 GiB
...
```

---

### Notes

- Some commands (e.g., `dmidecode`, `fdisk`) require root privileges (`sudo`).
- If a command is not installed (e.g., `inxi`, `htop`, `mesa-utils`), install it using `sudo apt install <package-name>`.
- For a graphical tool, `hardinfo` or `gnome-system-monitor` (pre-installed on Ubuntu) can provide a user-friendly interface.
- If you need specific details (e.g., battery info, network adapters), let me know, and I can provide additional commands.

Let me know if you need help interpreting the output or want to focus on a specific component!
