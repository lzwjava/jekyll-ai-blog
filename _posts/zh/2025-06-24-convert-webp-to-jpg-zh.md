---
audio: false
generated: true
lang: zh
layout: post
title: 在Ubuntu中将WebP转换为JPG
translated: true
type: note
---

在 Ubuntu 系统中，你有多种优秀方案可将 WebP 格式转换为 JPG 格式，既支持命令行操作也提供图形界面工具。

## 命令行工具

这些工具通常对单文件或批量转换具有最佳灵活性和效率。

### 1. ImageMagick

ImageMagick 是功能强大的命令行图像处理套件，应用广泛。

* **安装方法：**

  ```bash
  sudo apt update
  sudo apt install imagemagick
  ```

* **单文件转换：**

  ```bash
  convert input.webp output.jpg
  ```

  若使用 ImageMagick v7+ 版本的 `magick` 命令：

  ```bash
  magick input.webp output.jpg
  ```

* **当前目录批量转换：**

  ```bash
  mogrify -format JPEG *.webp
  ```

  此命令会将当前目录所有 `.webp` 文件转换为同文件名 `.jpeg`（或 `.jpg`）格式。若需保存至独立目录：

  ```bash
  mkdir output_jpgs # 创建输出目录
  mogrify -format JPEG -path output_jpgs *.webp
  ```

### 2. `dwebp`（来自 `libwebp` 软件包）

`dwebp` 是专用于解码 WebP 图像的工具。

* **安装方法：**

  ```bash
  sudo apt update
  sudo apt install webp
  ```

* **单文件转换：**

  ```bash
  dwebp input.webp -o output.jpg
  ```

  虽然指定了 `.jpg` 输出格式，但 `dwebp` 通常输出 PPM 格式，需配合 ImageMagick 等工具转成标准 JPEG。若遇问题可先转 PNG 再转 JPG：

  ```bash
  dwebp input.webp -o output.png
  convert output.png output.jpg
  ```

### 3. `ffmpeg`

`ffmpeg` 主要处理音视频，但也支持图像格式转换。

* **安装方法：**

  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

* **单文件转换：**

  ```bash
  ffmpeg -i input.webp output.jpg
  ```

* **批量转换：**

  ```bash
  for file in *.webp; do ffmpeg -i "$file" "${file%.*}.jpg"; done
  ```

  该命令会遍历当前目录所有 `.webp` 文件并转换为同文件名 `.jpg` 格式（如 `image.webp` 转换为 `image.jpg`）。

## 图形界面工具

若偏好图形化操作，可选择以下工具：

### 1. GIMP（GNU 图像处理程序）

GIMP 是支持 WebP 格式的开源图像编辑器。

* **安装方法：**

  ```bash
  sudo apt update
  sudo apt install gimp
  ```

* **转换步骤：**
  1. 在 GIMP 中打开 WebP 图像（文件 > 打开）
  2. 选择 文件 > 导出为
  3. 在导出对话框的“选择文件类型（按扩展名）”下拉菜单中选择“JPEG 图像”
  4. 点击“导出”并根据需要调整质量参数

### 2. XnView MP / XnConvert

这是支持 WebP 格式的跨平台图像查看器和批量转换工具。

* **安装方法：**
  通常需要从官网下载 `.deb` 安装包，使用 `sudo dpkg -i <包名.deb>` 或图形化包管理器安装
* **转换流程（通用）：**
  1. 启动 XnView MP 或 XnConvert
  2. 添加待转换的 WebP 图像
  3. 选择 JPG 作为输出格式
  4. 调整质量、尺寸等参数
  5. 开始转换

### 3. Converseen

这是支持 WebP 的免费批量图像转换工具。

* **安装方法：** 可通过 Ubuntu 软件中心或 apt 仓库安装
* **转换方式：** 提供直观界面用于添加图像、选择输出格式并执行转换

## 如何选择转换方案？

* **快速单文件转换或自动化脚本处理：** 推荐使用命令行工具 `ffmpeg` 或 `ImageMagick`，效率极高
* **需可视化界面且需要图像编辑控制的偶尔转换：** GIMP 是理想选择
* **带图形界面的多文件批量转换：** XnView MP/XnConvert 或 Converseen 表现卓越

无论选择哪种方案，请确保提前安装所需软件包。
