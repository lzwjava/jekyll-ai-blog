---
audio: false
generated: true
lang: zh
layout: post
title: NVIDIA DKMS构建问题
translated: true
type: note
---

看起来你在更新内核时遇到了 NVIDIA DKMS（动态内核模块支持）模块构建失败的问题，新内核版本是 `6.8.0-60-generic`。这是一个常见问题，因为驱动模块需要针对新内核版本重新编译，有时会出现不兼容或构建问题。

关键错误信息包括：
* `Building module(s)......(bad exit status: 2)`
* `Error! Bad return status for module build on kernel: 6.8.0-60-generic (x86_64)`
* `Consult /var/lib/dkms/nvidia/535.183.06/build/make.log for more information.`
* `dpkg: error processing package linux-image-6.8.0-60-generic (--configure):`
* `E: Sub-process /usr/bin/dpkg returned an error code (1)`

这意味着 NVIDIA 驱动版本 `535.183.06` 无法针对内核 `6.8.0-60-generic` 成功编译，这反过来阻止了内核镜像和相关软件包的正确配置。

以下是解决方法：

---

### 1. 检查构建日志 🪵

最关键的一步是检查详细的构建日志以获取具体的错误信息。这个日志会告诉你编译失败的原因。
打开终端并运行：
```bash
cat /var/lib/dkms/nvidia/535.183.06/build/make.log
```
查找以 `error:` 或 `fatal error:` 开头的行。这些通常会指向缺失的文件、编译器问题或与内核源码的不兼容性。错误 `Applying patch disable_fstack-clash-protection_fcf-protection.patch... done.` 后跟构建失败表明补丁可能不完全兼容，或者存在补丁未解决的其他问题。

---

### 2. 清理并尝试修复损坏的软件包 🛠️

首先，尝试让 `apt` 修复损坏的依赖关系并完成软件包配置。
```bash
sudo rm /var/crash/nvidia-dkms-535.0.crash # 删除旧的崩溃报告以允许新的报告生成
sudo apt --fix-broken install
sudo dpkg --configure -a
```
这可能会重新触发 DKMS 构建。如果再次失败，请继续下一步。

---

### 3. 确保正确安装内核头文件 🧠

DKMS 构建过程需要你正在构建的内核对应的正确内核头文件。
```bash
sudo apt update
sudo apt install --reinstall linux-headers-6.8.0-60-generic linux-headers-generic-hwe-22.04
```
如果你尚未运行 `6.8.0-60-generic` 内核（例如，更新被中断），你也可以指定当前运行内核的头文件，但这里的主要目标是 `6.8.0-60-generic`。

---

### 4. 移除有问题的 DKMS 模块并重新配置 ♻️

你可以手动从 DKMS 中移除有问题的 NVIDIA 模块版本，然后让系统重新构建它。
```bash
sudo dkms remove nvidia/535.183.06 --all
```
然后，尝试重新配置软件包：
```bash
sudo dpkg --configure -a
sudo apt update && sudo apt upgrade
```
这个过程应该会提示 DKMS 尝试为 `6.8.0-60-generic` 内核重新构建模块。

---

### 5. 重新安装 NVIDIA 驱动 💻

如果模块仍然构建失败，驱动版本 `535.183.06` 可能与内核 `6.8.0-60-generic` 存在兼容性问题。

* **清除当前有问题的驱动：**
    ```bash
    sudo apt-get purge nvidia-dkms-535 nvidia-driver-535
    sudo apt autoremove
    sudo apt clean
    ```

* **安装合适的驱动：**
    你可以让 Ubuntu 尝试安装推荐的驱动：
    ```bash
    sudo ubuntu-drivers autoinstall
    ```
    或者，你可以尝试安装相同的版本（如果软件仓库现在认为它是兼容的）或可能更新、更兼容的版本。例如，尝试重新安装 535 系列驱动：
    ```bash
    sudo apt update
    sudo apt install nvidia-driver-535
    ```
    （软件包管理器应该会选择适当的 DKMS 版本。）

    之后，系统将再次尝试构建 DKMS 模块。

---

### 6. 考虑使用更新的 NVIDIA 驱动版本 🚀

内核 6.8 相对较新。NVIDIA 535 系列驱动可能与此内核版本存在限制。你可能需要更新的驱动系列（例如 545、550 或更新版本，如果你的软件仓库或 NVIDIA 官方渠道/PPA 提供）。

* 检查可用驱动：
    ```bash
    sudo apt search nvidia-driver
    ```
* 如果有更新的专有驱动可用（例如 `nvidia-driver-550`），你可以尝试安装它而不是 `nvidia-driver-535`。
    ```bash
    sudo apt install nvidia-driver-VERSION_NUMBER # 替换 VERSION_NUMBER
    ```

---

### 7. 如果你陷入启动循环或没有 GUI 📉

如果系统无法启动进入图形环境：
* 启动到恢复模式或旧内核（通常可以在启动时的 GRUB 菜单中访问）。
* 进入命令行环境后，你可以尝试上述步骤。
* 如果你需要在修复 NVIDIA 驱动时临时使用开源驱动来恢复 GUI：
    ```bash
    sudo apt-get purge nvidia*
    sudo apt autoremove
    sudo apt install xserver-xorg-video-nouveau
    sudo reboot
    ```
    然后，再次尝试安装 NVIDIA 驱动。

---

**关键要点：** `/var/lib/dkms/nvidia/535.183.06/build/make.log` 的内容非常重要。如果上述步骤不起作用，该文件中的错误将提供更具体的线索，你可能需要在线搜索这些特定错误，结合你的内核版本和 NVIDIA 驱动版本。

---

此输出表明你的 Ubuntu 系统存在一系列依赖关系和配置问题，很可能与内核更新和 NVIDIA 驱动相关。让我们分析这些问题并提出潜在的解决方案。

**主要问题：**

1.  **`linux-generic-hwe-22.04` 的依赖问题：**
    *   它依赖于特定版本（`= 6.8.0-60.63~22.04.1`）的 `linux-headers-generic-hwe-22.04`。
    *   `linux-headers-generic-hwe-22.04` 尚未配置，导致 `linux-generic-hwe-22.04` 配置失败。

2.  **`linux-image-6.8.0-60-generic` 配置失败：**
    *   此内核镜像的安装后脚本失败，退出状态为 1。
    *   错误日志表明这与 NVIDIA 驱动（`nvidia/535.183.06`）未能为此特定内核版本（`6.8.0-60-generic`）构建有关。
    *   NVIDIA 驱动的 DKMS（动态内核模块支持）构建过程失败。日志文件 `/var/lib/dkms/nvidia/535.183.06/build/make.log` 将包含有关构建错误的更多详细信息。
    *   还有一个与为 NVIDIA DKMS 失败创建崩溃报告相关的错误，表明系统的崩溃报告机制或文件系统权限可能存在潜在问题。

3.  **`linux-headers-6.8.0-60-generic` 和 `linux-headers-generic-hwe-22.04` 配置失败：**
    *   这些失败很可能是因为它们所依赖的 `linux-image-6.8.0-60-generic` 软件包配置失败。

**潜在原因：**

*   **不完整或中断的内核更新：** 系统可能在内核升级过程中被中断，导致某些软件包处于不一致状态。
*   **NVIDIA 驱动不兼容：** 已安装的 NVIDIA 驱动版本（`535.183.06`）可能无法针对新内核版本（`6.8.0-60-generic`）成功构建。
*   **DKMS 问题：** DKMS 框架本身可能存在问题，阻止了 NVIDIA 驱动的构建。
*   **文件系统问题：** 关于无法创建崩溃报告的错误可能表明 `/var/crash/` 目录存在磁盘空间或文件权限问题。

**故障排除步骤：**

1.  **尝试重新配置软件包：**
    打开终端并运行以下命令：
    ```bash
    sudo dpkg --configure -a
    ```
    此命令尝试配置所有处于半配置状态的软件包。

2.  **检查 NVIDIA DKMS 构建日志：**
    检查日志文件以获取 NVIDIA 驱动构建期间的详细错误信息：
    ```bash
    less /var/lib/dkms/nvidia/535.183.06/build/make.log
    ```
    此日志可能提供有关缺失依赖项或编译错误的线索。

3.  **尝试重新安装 NVIDIA 驱动：**
    你可以尝试移除然后重新安装 NVIDIA 驱动。首先，尝试清除它：
    ```bash
    sudo apt remove --purge nvidia-*
    sudo apt autoremove
    ```
    然后，尝试重新安装。如果当前版本有问题，你可能想尝试不同的版本：
    ```bash
    sudo apt install nvidia-driver-535  # 或不同的推荐版本
    ```
    安装后，重启系统。

4.  **清理软件包缓存并重试：**
    ```bash
    sudo apt clean
    sudo apt update
    sudo apt upgrade
    sudo dpkg --configure -a
    ```

5.  **重新安装有问题的内核和头文件：**
    你可以尝试重新安装导致问题的特定内核和头文件软件包：
    ```bash
    sudo apt install --reinstall linux-image-6.8.0-60-generic linux-headers-6.8.0-60-generic linux-headers-generic-hwe-22.04 linux-generic-hwe-22.04
    ```
    之后，尝试重新配置：
    ```bash
    sudo dpkg --configure -a
    ```

6.  **检查磁盘空间：**
    确保你的根分区（`/`）有足够的可用空间，因为这有时会在软件包安装和配置过程中导致问题。
    ```bash
    df -h /
    ```

7.  **解决崩溃报告错误（如果持续存在）：**
    如果关于 `/var/crash/nvidia-dkms-535.0.crash` 的错误持续存在，你可以尝试删除该文件（如果它存在且你不需要它进行调试）或检查 `/var/crash/` 目录的权限。
    ```bash
    sudo rm -f /var/crash/nvidia-dkms-535.0.crash
    sudo chmod 777 /var/crash  # 对宽松权限要小心，如果不需要请恢复
    ```

8.  **启动到之前的内核：**
    如果你安装了之前的内核版本，可以尝试从 GRUB 菜单启动到它。这可以让你在稳定的环境中执行故障排除步骤。如果系统在旧内核下工作，问题很可能特定于 `6.8.0-60-generic` 内核或其与 NVIDIA 驱动的交互。

**重要注意事项：**

*   **备份：** 在进行重大更改之前，尤其是涉及软件包移除时，备份重要数据总是一个好主意。
*   **耐心：** 软件包配置和安装可能需要一些时间。
*   **查阅日志：** 错误信息和日志文件（尤其是 NVIDIA DKMS 构建日志）对于诊断问题的确切原因至关重要。

从前面几个步骤开始，看看它们是否能解决问题。如果不行，继续进行更复杂的解决方案，并仔细检查遇到的任何错误信息。祝你好运！

---

来自 NVIDIA DKMS 构建日志的此输出表明，编译失败的原因是 **无法识别的命令行选项：`-ftrivial-auto-var-init=zero`**。

这个编译器选项是 GCC（很可能是 12 或更高版本）和 Clang 相对较新的补充。看起来用于为你的内核（6.8.0-60-generic）构建 NVIDIA 驱动的编译器无法识别此选项。

**可能的原因和解决方案：**

1.  **过时的编译器：** 你的系统可能安装了旧版本的 GCC 或 Clang 作为默认编译器。内核头文件可能是用使用此选项的新编译器编译的，但 NVIDIA 驱动构建系统却使用了旧版本。

    **解决方案：**
    *   **安装更新的编译器：** 你可以尝试安装更新版本的 GCC。
        ```bash
        sudo apt update
        sudo apt install gcc-12  # 或更高版本，如 gcc-13
        ```
    *   **更新构建环境：** 确保你的构建工具是最新的。
        ```bash
        sudo apt update
        sudo apt install build-essential
        ```
    *   **指定编译器（如果可能）：** 一些构建系统允许你指定要使用的编译器。检查 NVIDIA 驱动构建说明或配置文件以获取与编译器相关的选项（例如，`CC` 环境变量）。

2.  **与内核构建配置不兼容：** 你使用的内核可能是用启用了此选项的编译器构建的，而 NVIDIA 驱动构建系统以某种方式继承或遇到它，导致其自身的编译器失败。

    **解决方案：**
    *   **尝试不同的 NVIDIA 驱动版本：** 最新的 NVIDIA 驱动可能对新内核和编译器功能具有更好的兼容性。你可以尝试安装更新的稳定版本。
        ```bash
        sudo apt update
        sudo apt install nvidia-driver-<latest-version>
        ```
        将 `<latest-version>` 替换为你的系统最新的推荐驱动软件包名称。通常可以通过搜索 `apt search nvidia-driver` 找到。
    *   **降级你的内核（作为临时解决方法）：** 如果你安装了之前与 NVIDIA 驱动一起工作的内核版本，可以从 GRUB 菜单启动到该内核。这不是一个永久性的解决方案，但可以让你在有一个正常工作的系统的同时，排查新内核的驱动问题。

3.  **NVIDIA 驱动软件包的问题：** 你尝试安装的特定 NVIDIA 驱动软件包与你的内核和编译器设置可能存在兼容性问题。

    **解决方案：**
    *   **尝试不同的安装方法：** 如果你通过 `apt` 安装驱动，可以尝试直接从 NVIDIA 网站下载驱动并使用 `.run` 文件安装。请仔细遵循 NVIDIA 提供的说明。
    *   **检查已知问题：** 在线搜索论坛或 NVIDIA 支持网站，了解你使用的特定驱动版本和内核组合的已知问题。

**尝试步骤：**

1.  **检查你的 GCC 版本：**
    ```bash
    gcc --version
    ```
    将其与可能用于构建内核的 GCC 版本进行比较（你可能可以在网上找到你的 Ubuntu 版本的内核构建环境信息）。

2.  **尝试安装更新的 NVIDIA 驱动：**
    ```bash
    sudo apt update
    sudo apt install nvidia-driver-550  # 示例：尝试更新版本
    sudo reboot
    ```

3.  **如果上述方法不起作用，尝试清除并重新安装推荐的驱动：**
    ```bash
    sudo apt remove --purge nvidia-*
    sudo apt autoremove
    sudo apt update
    sudo ubuntu-drivers autoinstall  # 安装推荐的驱动
    sudo reboot
    ```

4.  **如果你仍然面临问题，考虑安装更新的 GCC 版本（请小心，因为这有时会产生意想不到的副作用）：**
    ```bash
    sudo apt install gcc-12 g++-12
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 12
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-12 12
    # 你可能还想保留旧版本，并在需要时切换回去
    # 要切换回去：sudo update-alternatives --config gcc 和 sudo update-alternatives --config g++
    sudo apt install build-essential # 在编译器更改后确保构建工具已更新
    sudo dpkg --configure -a # 重新配置软件包
    sudo reboot
    ```

请记住，在尝试任何驱动安装或重大系统更改后重启系统。仔细监控输出以查找任何新的错误信息。如果你继续遇到问题，提供有关你的 Ubuntu 版本的更多详细信息可能有助于找到更具体的解决方案。

---

看起来你在配置 Linux 内核软件包时遇到了依赖关系和 DKMS（动态内核模块支持）问题，特别是 NVIDIA 驱动模块未能为新内核（6.8.0-60-generic）构建。

### 解决方法如下：

---

### **1. 修复依赖关系并配置软件包**
首先，尝试修复依赖关系问题并配置软件包：

```bash
sudo apt --fix-broken install
sudo dpkg --configure -a
```

如果这不起作用，手动强制配置有问题的软件包：

```bash
sudo apt install -f linux-headers-generic-hwe-22.04 linux-generic-hwe-22.04
```

---

### **2. 重新安装 NVIDIA 驱动**
错误显示 NVIDIA DKMS 模块（`nvidia/535.183.06`）未能为内核 `6.8.0-60-generic` 构建。要修复此问题：

#### **选项 A：重新安装 NVIDIA 驱动**
```bash
sudo apt install --reinstall nvidia-dkms-535 nvidia-driver-535
```

#### **选项 B：清除并重新安装 NVIDIA 驱动**
如果重新安装不起作用，尝试干净地重新安装：
```bash
sudo apt purge nvidia-*
sudo apt autoremove
sudo apt install nvidia-driver-535
```

#### **选项 C：临时启动到旧内核**
如果系统无法启动，重启进入旧内核（在 GRUB 中选择它），然后：
```bash
sudo apt remove linux-image-6.8.0-60-generic linux-headers-6.8.0-60-generic
sudo update-grub
```

---

### **3. 检查 DKMS 构建日志**
错误提到了 `/var/lib/dkms/nvidia/535.183.06/build/make.log`。检查它以获取详细信息：
```bash
cat /var/lib/dkms/nvidia/535.183.06/build/make.log
```

这可能揭示模块构建失败的原因（例如，缺失依赖项、编译器问题）。

---

### **4. 手动安装缺失的依赖项**
如果日志显示缺失依赖项，请安装它们：
```bash
sudo apt install build-essential linux-headers-generic
```

---

### **5. 重建 DKMS 模块**
修复依赖项后，手动重建模块：
```bash
sudo dkms remove nvidia/535.183.06 --all
sudo dkms install nvidia/535.183.06
```

---

### **6. 更新 Initramfs**
修复 NVIDIA 驱动后，更新 initramfs：
```bash
sudo update-initramfs -u -k all
```

---

### **7. 最终修复尝试**
如果所有其他方法都失败，移除有问题的内核并坚持使用旧内核：
```bash
sudo apt purge linux-image-6.8.0-60-generic linux-headers-6.8.0-60-generic
sudo apt autoremove
sudo update-grub
```

然后，等待更新的 NVIDIA 驱动或内核后再尝试。

---

### **8. 预防未来问题**
为避免类似问题，请考虑：
- **禁用自动内核更新**（如果你依赖 NVIDIA 驱动）：
  ```bash
  sudo apt-mark hold linux-image-generic linux-headers-generic
  ```
- **使用官方 NVIDIA 驱动**（而不是 Ubuntu 的软件包），如果兼容性是一个反复出现的问题。

---

### **最后说明**
- 如果系统变得无法启动，使用 **GRUB** 选择旧内核。
- 如果 NVIDIA 驱动对你的工作流程至关重要，考虑使用 **LTS 内核**（非 HWE）以获得更好的稳定性。

如果你需要进一步的帮助，请告诉我！

---

如果你只是想继续 `apt upgrade` 并 **跳过有问题的软件包**，你可以暂时将它们从升级过程中排除。方法如下：

### **选项 1：跳过损坏的软件包并继续升级**
运行：
```bash
sudo apt --fix-broken install
sudo apt upgrade -y --ignore-missing --allow-downgrades
```
- `--ignore-missing` 跳过不可用的软件包。
- `--allow-downgrades` 允许 APT 在需要时降级软件包。

### **选项 2：保留（阻止）有问题的软件包**
如果问题持续存在，**保留**（阻止）有问题的软件包以防止它们被升级：
```bash
sudo apt-mark hold linux-generic-hwe-22.04 linux-headers-generic-hwe-22.04 linux-image-6.8.0-60-generic
```
然后重试：
```bash
sudo apt upgrade -y
```

### **选项 3：强制升级（不推荐）**
如果你可以接受可能进一步破坏系统，强制升级：
```bash
sudo apt -o Dpkg::Options::="--force-overwrite" --fix-broken install
sudo apt upgrade -y
```
⚠️ **警告：** 如果依赖关系不匹配，这可能导致系统不稳定。

### **跳过之后：**
- 系统仍然可以工作，但 **NVIDIA 驱动可能无法在** 内核 `6.8.0-60` 上运行。
- 如果需要，你可以 **启动到旧内核**（在 GRUB 中选择它）。
- 一旦 NVIDIA 发布兼容的更新，你可以 **取消保留** 软件包：
  ```bash
  sudo apt-mark unhold linux-generic-hwe-22.04 linux-headers-generic-hwe-22.04
  ```

升级后，你需要帮助检查当前激活的是哪个内核吗？
