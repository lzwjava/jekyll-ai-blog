---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Linux内核模块化机制解析
translated: true
type: note
---

### 理解 Linux 中的模块化

Linux 的模块化主要指的是 Linux 内核的设计，其本质上是**单体内核**（所有核心组件在单一地址空间中运行以提高效率），但通过**可加载内核模块**实现了模块化。这使您能够在运行时动态添加或移除内核功能——如设备驱动程序、文件系统或网络协议——而无需重启或重新编译整个内核。这是一种混合方法，在性能和灵活性之间取得平衡，使 Linux 能够高度适应不同的硬件和使用场景。

可以将其想象成乐高积木：内核是基础结构，但您可以根据需要安装（加载）或移除（卸载）部件，从而保持系统的精简和可定制性。Linux 中的大多数设备驱动程序都是以这种方式实现的，这就是为什么 Linux 能够支持庞大的硬件生态系统而不会导致核心内核臃肿的原因。

#### 模块化为何重要

- **灵活性**：仅加载所需内容（例如，连接到网络时加载 Wi-Fi 驱动程序）。
- **效率**：通过避免永久包含未使用的代码来减少内存占用。
- **可维护性**：更容易更新或调试单个组件，而无需触及整个系统。
- **稳定性**：一个模块中的故障在一定程度上是隔离的，尽管不如微内核（如 MINIX 中的内核）那样严格。

正如您在我们之前的聊天中提到的那样，这种设计帮助 Linux 延续了数十年——它比僵化的单体内核更容易演进。

#### 内核模块的工作原理

内核模块是用 C 语言编写的已编译目标文件（扩展名为 `.ko`），使用内核头文件和 kbuild 系统。它们必须与您的内核版本匹配（使用 `uname -r` 检查）。

一个基本的模块包括：

- **初始化**：一个用 `module_init()` 标记的函数，在加载时运行（例如，注册驱动程序）。
- **清理**：一个用 `module_exit()` 标记的函数，在卸载时运行（例如，释放资源）。
- **元数据**：用于许可和作者信息的宏，如 `MODULE_LICENSE("GPL")`。

以下是一个简单的示例模块 (`hello.c`)，用于打印消息：

```c
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/module.h>

MODULE_DESCRIPTION("A simple hello module");
MODULE_AUTHOR("You");
MODULE_LICENSE("GPL");

static int __init hello_init(void) {
    printk(KERN_INFO "Hello, Linux modularity!\n");
    return 0;  // Success
}

static void __exit hello_exit(void) {
    printk(KERN_INFO "Goodbye from the module!\n");
}

module_init(hello_init);
module_exit(hello_exit);
```

要编译它（需要安装内核头文件，例如在基于 Debian 的系统上通过 `apt install linux-headers-$(uname -r)` 安装）：

- 创建一个 `Makefile`：

  ```
  obj-m += hello.o
  KDIR := /lib/modules/$(shell uname -r)/build
  all:
      make -C $(KDIR) M=$(PWD) modules
  clean:
      make -C $(KDIR) M=$(PWD) clean
  ```

- 运行 `make` 生成 `hello.ko`。
- 使用 `sudo insmod hello.ko` 加载（或使用 `sudo modprobe hello` 进行依赖项处理）。
- 检查日志：`dmesg | tail`（您将看到 "Hello" 消息）。
- 卸载：`sudo rmmod hello`（在 `dmesg` 中看到 "Goodbye"）。

来自 `printk` 的消息会发送到内核环缓冲区 (`dmesg`) 或 `/var/log/kern.log`。

#### 实践中的模块管理

使用以下命令（来自 `kmod` 包；如果需要，请安装：在 RHEL 上使用 `sudo yum install kmod` 或在 Ubuntu 上使用 `sudo apt install kmod`）。

| 操作 | 命令 | 描述/示例 |
|--------|---------|---------------------|
| **列出已加载模块** | `lsmod` | 显示名称、大小、使用计数和依赖项。<br>示例：`lsmod \| grep bluetooth`（过滤蓝牙模块）。 |
| **模块信息** | `modinfo <name>` | 详细信息，如版本、描述。<br>示例：`modinfo e1000e`（用于 Intel 网络驱动程序）。 |
| **加载模块** | `sudo modprobe <name>` | 加载模块及其依赖项（优于 `insmod`，后者需要完整路径）。<br>示例：`sudo modprobe serio_raw`（原始串行输入）。 |
| **卸载模块** | `sudo modprobe -r <name>` | 卸载模块及其依赖项（如果需要，先卸载依赖项）。<br>示例：`sudo modprobe -r serio_raw`。使用 `lsmod` 检查使用情况。 |
| **自动生成依赖项** | `sudo depmod -a` | 更新 `/lib/modules/$(uname -r)/modules.dep` 以供 modprobe 使用。 |

模块位于 `/lib/modules/$(uname -r)/kernel/`。避免卸载正在使用的模块（例如，活跃的驱动程序）以防止崩溃。

#### 使模块持久化

更改在重启后不会永久保留：

- **在启动时加载**：添加到 `/etc/modules-load.d/myfile.conf`（每行一个模块）。<br>示例：`echo "hello" \| sudo tee /etc/modules-load.d/hello.conf`。
- **黑名单（阻止加载）**：添加到 `/etc/modprobe.d/blacklist.conf`。<br>示例：

  ```
  blacklist bad_module
  install bad_module /bin/false
  ```

  然后重新生成 initramfs：`sudo dracut -f` 并重启。

#### 常见陷阱和提示

- **版本不匹配**：模块必须与您的内核匹配——更新后重新编译。
- **依赖项**：`modprobe` 会处理它们；使用 `modinfo --depends <name>` 检查。
- **调试**：使用 `pr_debug` 获取详细日志（通过 `echo 8 > /proc/sys/kernel/printk` 启用）。
- 在虚拟机中开始实验，以避免破坏您的系统。

这种设置就是为什么 Linux 在实践中感觉是“模块化”的——它不是完整的微内核，但模块系统模拟了微内核以实现可扩展性。要动手实践，请尝试加载真实的驱动程序，如用于 FAT 文件系统的 `vfat`。

[内核模块实验文档](https://linux-kernel-labs.github.io/refs/heads/master/labs/kernel_modules.html)
[在 Medium 上理解内核模块](https://medium.com/@arashjafariwork/understanding-kernel-modules-enhancing-flexibility-in-operating-systems-ed348807ed7b)
[红帽内核管理指南](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/kernel_administration_guide/chap-documentation-kernel_administration_guide-working_with_kernel_modules)
