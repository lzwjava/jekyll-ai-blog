---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: PIL Pillow图像处理指南
translated: true
type: note
---

### 什么是 PIL/Pillow？

PIL 最初是 Python Imaging Library 的缩写，但现在以 Pillow 包（一个现代分支）的形式维护。在代码中你需要以 `PIL` 名称导入，但需要通过 pip 安装 Pillow。它用于在 Python 中打开、处理和保存图像文件。支持 JPEG、PNG、GIF、BMP 等多种格式。

### 安装

要使用 PIL，请安装 Pillow：

```bash
pip install pillow
```

### 基本导入与使用

安装后，在 Python 脚本中这样导入：

```python
from PIL import Image
```

无需使用 `import PIL.Image`——这会直接导入 Image 模块。

### 常用图像操作

以下是基础操作示例。假设你的目录中有一个名为 `example.jpg` 的图像文件。

#### 1. 打开图像

```python
image = Image.open('example.jpg')  # 打开图像文件
image.show()  # 显示图像（在支持图像查看器的系统上有效）
```

#### 2. 获取图像信息

```python
print(image.format)  # 例如 'JPEG'
print(image.size)    # 元组：(宽度, 高度)
print(image.mode)    # 例如彩色图像的 'RGB'
```

#### 3. 调整图像尺寸

```python
resized = image.resize((800, 600))  # 调整为 800x600 像素
resized.save('resized_example.jpg')  # 保存调整后的图像
```

#### 4. 转换格式

```python
image.convert('L').save('grayscale_example.png')  # 转换为灰度图并保存为 PNG
```

#### 5. 旋转图像

```python
rotated = image.rotate(90)  # 顺时针旋转 90 度
rotated.save('rotated_example.jpg')
```

#### 6. 裁剪图像

```python
left, top, right, bottom = 100, 100, 300, 300  # 定义裁剪区域 (x1, y1, x2, y2)
cropped = image.crop((left, top, right, bottom))
cropped.save('cropped_example.jpg')
```

#### 7. 应用滤镜（需额外导入）

使用滤镜需要导入 `ImageFilter`：

```python
from PIL import ImageFilter
blurred = image.filter(ImageFilter.BLUR)  # 应用模糊滤镜
blurred.save('blurred_example.jpg')
```

### 进阶示例：批量处理多张图像

```python
import os
from PIL import Image

# 将文件夹中所有 JPEG 图像调整为 200x200
input_folder = 'images/'
output_folder = 'resized_images/'
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith('.jpg'):
        image = Image.open(os.path.join(input_folder, filename))
        resized = image.resize((200, 200))
        resized.save(os.path.join(output_folder, filename))
```

### 提示与注意事项

- **错误处理**：对无效文件使用 try-except，例如 `try: image = Image.open('file.jpg')`
- **内存效率**：处理大图像后使用 `image.close()` 释放内存
- **文档参考**：访问 [pillow.readthedocs.io](https://pillow.readthedocs.io/en/stable/) 查看绘图、文字添加或 EXIF 数据处理等完整功能
- **依赖项**：在某些系统环境中，Pillow 可能需要安装系统库（如 libjpeg），若遇到问题请参考安装指南

如果你有具体任务或错误信息，提供更多细节可获得针对性帮助！
