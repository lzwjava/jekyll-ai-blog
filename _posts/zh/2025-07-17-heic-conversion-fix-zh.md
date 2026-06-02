---
audio: false
generated: true
lang: zh
layout: post
title: 修复Pillow的HEIC支持错误
translated: true
type: note
---

错误提示 `cannot identify image file` 表明 Pillow 无法读取 HEIC 文件，可能由以下原因导致：

1. **缺少 `libheif` 库**：Pillow 需要 `libheif` 来处理 HEIC 文件，可能未在系统中安装或配置不当。
2. **HEIC 文件损坏或不兼容**：HEIC 文件可能已损坏，或格式不被 Pillow 支持。
3. **Pillow 版本问题**：尽管 Pillow 9.0.0+ 支持 HEIC，但可能存在配置问题或版本过旧。

鉴于您使用的是 macOS（根据之前的输出），我将提供一个修复后的 Python 脚本，其中包含额外的错误处理和日志记录功能，用于诊断问题。同时，我也会指导您安装 `libheif` 并验证 Pillow 的 HEIC 支持。如果 Pillow 持续失败，脚本将包含一个备用方案，使用已安装的 `ImageMagick` 进行 HEIC 转换。

### 修复步骤

#### 1. 安装 `libheif`

Pillow 依赖 `libheif` 来支持 HEIC。使用 Homebrew 安装：

```bash
brew install libheif
```

安装后，重新安装 Pillow 以确保其与 `libheif` 链接：

```bash
pip uninstall pillow
pip install pillow
```

#### 2. 验证 Pillow 的 HEIC 支持

检查 Pillow 是否能处理 HEIC 文件：

```bash
python -c "from PIL import features; print(features.check_feature('heic'))"
```

- 如果输出 `True`，表示 Pillow 支持 HEIC。
- 如果输出 `False` 或错误，说明 `libheif` 未正确配置，或 Pillow 未启用 HEIC 支持。

#### 3. 检查文件完整性

确保 HEIC 文件未损坏。尝试在 macOS 的预览等查看器中打开其中一个文件（例如 `IMG_5988.HEIC`）。如果无法打开，文件可能已损坏，需要重新导出或获取新副本。

#### 4. 更新后的 Python 脚本

更新后的脚本：

- 使用 Pillow 进行 HEIC 转换，并改进了错误处理。
- 当 Pillow 读取 HEIC 文件失败时，回退到使用已安装的 `ImageMagick`。
- 将详细错误记录到文件 `conversion_errors.log` 中，便于调试。
- 支持 `.heic` 和 `.heif` 扩展名。
- 将输出 JPG 压缩至约 500KB。

```python
import os
import argparse
import subprocess
import logging
from PIL import Image
from datetime import datetime

# 设置日志记录
logging.basicConfig(
    filename="conversion_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 解析命令行参数
parser = argparse.ArgumentParser(description="Convert HEIC images to JPG and compress to ~500KB.")
parser.add_argument("input_dir", help="Directory containing HEIC files")
args = parser.parse_args()

# 定义输入和输出目录
input_dir = args.input_dir.rstrip(os.sep)
output_dir = input_dir + "_compressed"
target_size_kb = 500  # 目标文件大小（KB）

# 创建输出目录（如果不存在）
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def get_file_size(file_path):
    """返回文件大小（KB）。"""
    return os.path.getsize(file_path) / 1024

def convert_with_imagemagick(heic_path, jpg_path):
    """回退到使用 ImageMagick 进行 HEIC 到 JPG 转换。"""
    try:
        subprocess.run(
            ["magick", heic_path, "-quality", "85", jpg_path],
            check=True, capture_output=True, text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"ImageMagick failed for {heic_path}: {e.stderr}")
        return False
    except FileNotFoundError:
        logging.error("ImageMagick not installed. Install it with 'brew install imagemagick'.")
        return False

def convert_heic_to_jpg(heic_path, jpg_path, quality=85):
    """将 HEIC 转换为 JPG 并压缩至接近目标大小。"""
    try:
        # 优先尝试 Pillow
        image = Image.open(heic_path)
        if image.mode != "RGB":
            image = image.convert("RGB")

        # 以初始质量保存为 JPG
        image.save(jpg_path, "JPEG", quality=quality)

        # 调整质量以接近目标大小
        current_size = get_file_size(jpg_path)
        low, high = 10, 100
        while low <= high and abs(current_size - target_size_kb) > 10:
            quality = (low + high) // 2
            image.save(jpg_path, "JPEG", quality=quality)
            current_size = get_file_size(jpg_path)
            if current_size > target_size_kb:
                high = quality - 1
            else:
                low = quality + 1
        return True
    except Exception as e:
        logging.error(f"Pillow failed for {heic_path}: {e}")
        # 回退到 ImageMagick
        return convert_with_imagemagick(heic_path, jpg_path)

# 处理输入目录中的所有 HEIC 文件
for filename in os.listdir(input_dir):
    if filename.lower().endswith((".heic", ".heif")):
        heic_path = os.path.join(input_dir, filename)
        jpg_filename = os.path.splitext(filename)[0] + ".jpg"
        jpg_path = os.path.join(output_dir, jpg_filename)

        try:
            if convert_heic_to_jpg(heic_path, jpg_path):
                print(f"Converted {filename} to {jpg_filename}, size: {get_file_size(jpg_path):.2f} KB")
            else:
                print(f"Error processing {filename}: Conversion failed (check conversion_errors.log)")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            logging.error(f"General error for {heic_path}: {e}")

print("Batch conversion complete! Check conversion_errors.log for any issues.")
```

### 使用方法

1. **保存脚本**：
   将代码保存为 `photo_compress.py`，放在 `scripts/media/` 目录中。

2. **安装依赖**：
   - 确保 Pillow 已安装：

     ```bash
     pip install --upgrade pillow
     ```

   - 安装 `libheif`：

     ```bash
     brew install libheif
     ```

   - 可选：安装 ImageMagick 作为备用方案：

     ```bash
     brew install imagemagick
     ```

3. **运行脚本**：

   ```bash
   python scripts/media/photo_compress.py ./assets/images/yuebei
   ```

   - 这将处理 `assets/images/yuebei` 中的所有 `.heic` 和 `.heif` 文件。
   - 输出的 JPG 文件保存在 `assets/images/yuebei_compressed` 中。
   - 错误将记录到当前目录的 `conversion_errors.log` 文件中。

4. **检查日志**：
   如果有文件转换失败，请查看 `conversion_errors.log` 获取详细错误信息。

### 额外故障排除

- **如果 Pillow 仍然失败**：
  - 验证 `libheif` 是否正确安装并链接：

    ```bash
    pkg-config --modversion libheif
    ```

    如果失败，请重新安装 `libheif` 和 Pillow。
  - 手动测试单个文件：

    ```python
    from PIL import Image
    img = Image.open("./assets/images/yuebei/IMG_5988.HEIC")
    print("Image opened successfully")
    ```

    如果失败，文件可能已损坏或是不受支持的 HEIC 变体。

- **文件损坏**：
  - 尝试使用 ImageMagick 手动转换一个文件：

    ```bash
    magick ./assets/images/yuebei/IMG_5988.HEIC test.jpg
    ```

    如果失败，文件可能已损坏。

- **ImageMagick 备用方案**：
  - 如果 Pillow 持续失败，脚本将尝试使用已安装的 ImageMagick。
  - 安装 `jpegoptim` 以获得更好的压缩控制：

    ```bash
    brew install jpegoptim
    ```

    运行脚本后，压缩输出文件：

    ```bash
    for i in ./assets/images/yuebei_compressed/*.jpg; do jpegoptim --size=500k "$i"; done
    ```

### 参考资料

- [Pillow 文档](https://pillow.readthedocs.io/en/stable/)
- [ImageMagick](https://imagemagick.org/)
- [libheif](https://github.com/strukturag/libheif)
- [jpegoptim](https://github.com/tjko/jpegoptim)

如果问题仍然存在，请分享 `conversion_errors.log` 的内容或任何新的错误信息，我将提供进一步帮助！
