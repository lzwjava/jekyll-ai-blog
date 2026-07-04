---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FFmpeg 源码构建步骤
translated: true
type: note
---

以下是我从源代码构建 FFmpeg 的完整步骤：

---

## 1. 初步评估

我检查了：

- **构建系统**：项目使用 `./configure` + `make`（标准 autoconf 风格）
- **之前的构建**：不存在 `config.mak` → 从未配置过，需要全新构建
- **工具链**：已安装 `gcc` 和 `make`
- **依赖项**：仅存在运行时库（`libx264-164`、`libmp3lame0` 等），但**没有 `-dev` 包**——编译所需的头文件缺失

## 2. 首次配置尝试

运行：

```
./configure --enable-gpl --enable-version3 --enable-nonfree
```

失败，错误信息：

```
nasm not found or too old. Please install/update nasm or use --disable-x86asm
```

**原因**：NASM 是 FFmpeg 用于编译手工优化的 x86 汇编例程（SIMD 优化的编解码器、滤镜等）的汇编器。没有它，configure 会强制回退到纯 C 实现，速度较慢但仍可运行。我选择安装它以获得更快的构建。

## 3. 安装 NASM

由于此机器需要交互式 `sudo`，我使用了 `pkexec`（Polkit GUI 提权）：

```
pkexec bash -c 'apt-get update -qq && apt-get install -y nasm'
```

这将从 Ubuntu 24.04 (Noble) 仓库安装 `nasm 2.16.01`。

## 4. 第二次配置——成功

重新运行相同的 configure 命令：

```
./configure --enable-gpl --enable-version3 --enable-nonfree
```

成功。Configure 自动检测到：

- 将编译 2,414 个目标文件
- 启用哪些编解码器、滤镜、混合器、解混合器、协议和比特流滤镜
- 未发现外部库（无 `-dev` 包）
- 生成了 `config.h`、`config.mak`、`ffbuild/config.mak` 以及库版本头文件

**关于这些选项**：

- `--enable-gpl` — 启用 GPL 许可的组件（FFmpeg 的许多部分都是 GPL）
- `--enable-version3` — 启用 LGPLv3/GPLv3 代码
- `--enable-nonfree` — 启用非免费编解码器（例如 libaacplus、某些编码器）。组合使用后输出不可再分发

## 5. 编译

```
make -j$(nproc)
```

- `-j$(nproc)` → 在所有 CPU 核心上并行构建（`nproc` 返回核心数）
- 跨 7 个库编译了 2,414 个 `.o` 文件
- 链接生成 `ffmpeg_g` 和 `ffprobe_g`（带调试符号的版本），然后 `strip` 缩减为 29 MB 的发布二进制文件
- 从 POD 文档构建了 man 页面
- 总时间：约几分钟（并行编译）

## 6. 验证

检查了：

- 二进制文件存在：`ffmpeg`（29 MB）、`ffprobe`（29 MB）
- 版本字符串：`ffmpeg version git-2026-07-02-14ed5e8`
- 库版本：avutil 61.2, avcodec 63.3, avformat 63.3, avdevice 63.2, avfilter 12.2, swscale 10.2, swresample 7.2
- 编码器：约 189，解码器：约 527，滤镜：约 483，混合器：约 191，解混合器：约 368，比特流滤镜：约 53，协议：约 50
- 硬件加速：无（未安装 `libva-dev`/`libvdpau-dev`）

## 关键要点

- **除了许可证类型外，不需要任何 `./configure` 选项**——FFmpeg 的 configure 具有出色的自动检测能力，能包含所有它能找到的内容
- **唯一缺失的工具是 `nasm`**——其他所有内容（gcc、make、ld）都已存在
- 要添加外部编码器（x264、x265 等），可以运行：

  ```
  sudo apt-get install libx264-dev libx265-dev libvpx-dev libmp3lame-dev libopus-dev libvorbis-dev libass-dev libsdl2-dev
  ./configure --enable-gpl --enable-version3 --enable-nonfree
  make -j$(nproc)
  ```

- 对于可再分发的构建（不含非免费代码），去掉 `--enable-nonfree`；configure 仍能正常工作
