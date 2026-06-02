---
audio: false
generated: true
lang: zh
layout: post
title: 修复TCMalloc错误
translated: true
type: note
---

错误信息“Cannot locate TCMalloc. Do you have tcmalloc or google-perftool installed on your system? (improves CPU memory usage)”表明您的 Linux 系统中未安装或未正确配置 Google gperftools 中的 TCMalloc 库。TCMalloc 是一种内存分配器，可提升性能并减少内存使用，特别是在 Stable Diffusion 等应用中。以下是解决此问题的方法：

### 解决 TCMalloc 错误的步骤

1. **安装 TCMalloc 和 Google Perftools**
   根据您的 Linux 发行版，使用相应的包管理器安装所需库。

   - **适用于 Ubuntu/Debian 系统**：

     ```bash
     sudo apt-get update
     sudo apt-get install libgoogle-perftools-dev libtcmalloc-minimal4 -y
     ```

     这将安装完整的 `libgoogle-perftools-dev`（包含 TCMalloc）和轻量版 `libtcmalloc-minimal4`。

   - **适用于 Fedora 系统**：

     ```bash
     sudo dnf install gperftools-libs -y
     ```

     这将安装必要的 TCMalloc 库。

   - **适用于 CentOS/RHEL 系统**：

     ```bash
     sudo yum install gperftools-libs -y
     ```

     如果默认仓库中没有该包，可能需要先启用 EPEL 仓库：

     ```bash
     sudo yum install epel-release
     sudo yum install gperftools-libs -y
     ```

2. **验证安装**
   安装后，检查 TCMalloc 是否已安装：

   ```bash
   dpkg -l | grep tcmalloc
   ```

   您应该会看到 `libtcmalloc-minimal4` 或类似的包。或者检查库路径：

   ```bash
   dpkg -L libgoogle-perftools-dev | grep libtcmalloc.so
   ```

   这将显示 TCMalloc 库的路径（例如 `/usr/lib/libtcmalloc.so.4`）。

3. **设置 LD_PRELOAD 环境变量**
   为确保应用程序使用 TCMalloc，请将 `LD_PRELOAD` 环境变量设置为指向 TCMalloc 库。可以临时或永久设置。

   - **临时设置（仅当前会话有效）**：
     在运行应用程序时设置 `LD_PRELOAD`：

     ```bash
     export LD_PRELOAD=/usr/lib/libtcmalloc.so.4
     ./launch.py
     ```

     如果步骤 2 中找到的路径不同，请将 `/usr/lib/libtcmalloc.so.4` 替换为实际路径。

   - **永久设置（适用于 Stable Diffusion 等）**：
     如果使用类似 `webui.sh` 的脚本（常见于 Stable Diffusion），请编辑脚本（例如 `webui-user.sh`）并添加：

     ```bash
     export LD_PRELOAD=libtcmalloc.so.4
     ```

     保存文件后重新运行脚本：

     ```bash
     ./webui.sh
     ```

     或者将其添加到 shell 配置文件中（例如 `~/.bashrc` 或 `~/.zshrc`）：

     ```bash
     echo 'export LD_PRELOAD=/usr/lib/libtcmalloc.so.4' >> ~/.bashrc
     source ~/.bashrc
     ```

4. **重新运行应用程序**
   安装 TCMalloc 并设置 `LD_PRELOAD` 后，重启应用程序：

   ```bash
   ./launch.py
   ```

   错误应不再出现，您可能会注意到内存使用或性能有所改善。

5. **故障排除**
   - **如果库路径不正确**：如果 `LD_PRELOAD` 失败（例如“无法打开共享对象文件”），请验证确切的库名称和路径：

     ```bash
     find /usr/lib -name "libtcmalloc*.so*"
     ```

     使用正确的路径更新 `LD_PRELOAD`（例如，如果使用轻量版则为 `libtcmalloc_minimal.so.4`）。
   - **如果错误仍然存在**：请确保安装的 TCMalloc 版本与您的系统兼容（在您的情况下是 glibc 2.35 和 GCC 11.4.0）。如果问题持续，请尝试从源码安装：

     ```bash
     git clone https://github.com/google/tcmalloc.git
     cd tcmalloc
     bazel build //tcmalloc:hello_main
     bazel run //tcmalloc:hello_main
     ```

     请参考 TCMalloc 快速入门指南获取详细说明。
   - **内存问题**：如果遇到分配失败或崩溃，请确保系统有足够内存，并且 TCMalloc 未与其他分配器冲突。

6. **可选：验证 TCMalloc 使用情况**
   要确认 TCMalloc 正在工作，可以运行简单的测试程序，或在应用程序运行时使用 `top` 或 `htop` 等工具检查内存使用情况。TCMalloc 通常会减少内存碎片并可能带来轻微的性能提升。

### 补充说明

- **为什么使用 TCMalloc？** TCMalloc 是一种高性能内存分配器，可减少 CPU 内存使用和碎片，特别是在像 Stable Diffusion 这样的多线程应用中。它不是必需的，但可以提升性能。
- **兼容性**：您的系统（glibc 2.35、Python 3.10.12、GCC 11.4.0）与最新的 TCMalloc 版本兼容，因此上述步骤应该有效。如果您使用自定义构建的应用程序，请确保其编译时支持 TCMalloc。
- **Stable Diffusion 上下文**：此错误经常出现在 AUTOMATIC1111 的 Stable Diffusion WebUI 中。上述步骤，特别是安装 `libgoogle-perftools-dev` 和设置 `LD_PRELOAD`，已知可以解决此问题。

如果您遇到特定错误或需要针对特定 Linux 发行版的帮助，请告诉我，我可以进一步调整说明！
