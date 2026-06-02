---
audio: false
generated: true
lang: en
layout: post
title: Linux System Information
translated: false
type: note
---

In Ubuntu, you can retrieve system information such as whether the system is 32-bit or 64-bit, the operating system version, the amount of RAM, and the disk size using the following commands. Below is a step-by-step guide:

### 1. Determine if the System is 32-bit or 64-bit

- **Command**: `uname -m`
- **Explanation**: This command displays the machine hardware name.
  - If the output is `x86_64`, your system is **64-bit**.
  - If the output is `i686` or `i386`, your system is **32-bit**.
- **Example Output**:

  ```
  x86_64
  ```

  This indicates a 64-bit system.

### 2. Get the Operating System (OS) Version

- **Command**: `lsb_release -a`
- **Explanation**: This command provides detailed information about the Linux Standard Base (LSB) and the distribution.
  - Look for the `Description` line to see the Ubuntu version.
- **Example Output**:

  ```
  No LSB modules are available.
  Distributor ID: Ubuntu
  Description:    Ubuntu 20.04.3 LTS
  Release:        20.04
  Codename:       focal
  ```

  Here, the OS is **Ubuntu 20.04.3 LTS**.

### 3. Get the RAM Size

- **Command**: `free -h`
- **Explanation**: This command shows memory usage in a human-readable format (e.g., GB or MB).
  - Look at the `total` column under the `Mem:` row to find the total installed RAM.
- **Example Output**:

  ```
              total        used        free      shared  buff/cache   available
  Mem:          15Gi       2.3Gi       9.5Gi       300Mi       3.8Gi        12Gi
  Swap:        2.0Gi         0B       2.0Gi
  ```

  In this case, the total RAM is **15 GB**.

### 4. Get the Disk Size

- **Command**: `lsblk -d -o NAME,SIZE`
- **Explanation**: This command lists all disk devices (excluding partitions) with their sizes.
  - The `-d` flag ensures only disk devices (e.g., `/dev/sda`) are shown, not their partitions.
  - Look for the disk name (e.g., `sda`) and its corresponding size.
- **Example Output**:

  ```
  NAME   SIZE
  sda    1T
  sdb    500G
  ```

  Here, the system has two disks: `/dev/sda` with a size of **1 terabyte** and `/dev/sdb` with **500 gigabytes**. If you have only one disk, it will typically be `sda`.

### Notes

- These commands use standard tools available in Ubuntu, requiring no additional installations.
- For disk size, if your system has multiple disks, the output will list all of them. Typically, `/dev/sda` is the primary disk.
- Run these commands in a terminal to see the results specific to your system.

With these commands, you can quickly gather the essential system information you need on your Ubuntu machine!
