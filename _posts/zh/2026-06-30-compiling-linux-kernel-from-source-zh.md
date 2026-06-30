---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从源代码编译Linux内核
translated: true
type: note
---

问题：如何从源代码编译 Linux 内核？

答案：

```bash
# 1. 获取源代码（主线版本或稳定标签）
git clone --depth 1 --branch v6.12 \
  https://github.com/torvalds/linux.git
cd linux

# 2. 安装构建依赖（Ubuntu）
sudo apt install -y build-essential libncurses-dev bison flex \
  libssl-dev libelf-dev bc dwarves zstd

# 3. 从当前运行内核的配置开始（快速路径）
cp /boot/config-$(uname -r) .config
make olddefconfig          # 用默认值填充新符号
# 或：make menuconfig       # 终端界面调整选项
# 或：make defconfig        # 从零开始使用架构默认配置

# 4. 构建（使用所有核心）
make -j$(nproc)            # 构建 vmlinux + 模块

# 5a. 仅构建内核镜像
make -j$(nproc) bzImage    # -> arch/x86/boot/bzImage

# 5b. 安装（模块 + 镜像 + initramfs + grub）
sudo make modules_install   # -> /lib/modules/<版本>/
sudo make install           # -> /boot，更新 initramfs 和 grub
```

关键选项：

- `make -j$(nproc)` — 并行构建；完整内核约需 5–30 分钟，取决于配置和核心数。在您的 192GB MI300X 机器上会很快；在 M2 Air 上使用 `tinyconfig` 构建更合理。
- `localmodconfig` — 仅构建当前加载的模块（`lsmod`），大幅缩短构建时间：
  ```bash
  make localmodconfig
  ```
- `O=` — 外部构建目录，保持源代码目录整洁：
  ```bash
  make O=../build defconfig
  make O=../build -j$(nproc)
  ```
- `CC=clang LLVM=1` — 使用 Clang/LLVM 而非 GCC 构建。
- `make clean`（保留配置）/ `make mrproper`（同时清除配置）。

用于快速迭代的最小配置（例如学习、QEMU 启动）：

```bash
make tinyconfig
make -j$(nproc)
# 在不影响真实系统的情况下启动：
qemu-system-x86_64 -kernel arch/x86/boot/bzImage \
  -append "console=ttyS0" -nographic
```

如果只想构建单个模块或子系统，可以构建对应子目录：

```bash
make -j$(nproc) drivers/net/        # 末尾斜杠表示构建目录
make M=drivers/mydriver modules     # 外部/独立模块
```

您的目标是什么——启动自定义内核、构建单个驱动程序，还是研究内部机制？配置策略差异很大（完整发行版配置 vs. `tinyconfig` + QEMU）。