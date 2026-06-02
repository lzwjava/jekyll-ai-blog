---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于线性代数的图像压缩技术
translated: true
type: note
---

图像压缩是数字图像处理中的基础任务，旨在减小图像存储大小的同时保持其视觉质量。实现这一目标的有效方法之一是运用线性代数，特别是奇异值分解（SVD）。该技术能让我们以更紧凑的形式表示图像矩阵，在保留本质特征的同时有效舍弃次要信息。

以下Python代码演示了如何使用SVD压缩图像。该过程包括将图像分解为组成分量，通过仅保留最重要的特征子集来压缩这些分量，然后重建压缩后的图像。这种方法可同时应用于灰度图像和彩色图像，为减小图像尺寸提供了灵活且数学严谨的解决方案。

```python
import numpy as np
from PIL import Image
import argparse
import os

def compress_image(image_path, compression_factor=0.1):
    # 打开图像并转换为numpy数组
    img = Image.open(image_path)
    img_array = np.array(img, dtype=float)

    # 判断图像类型（灰度/彩色）
    if len(img_array.shape) == 2:  # 灰度图像
        # 对图像数组执行SVD
        U, S, Vt = np.linalg.svd(img_array, full_matrices=False)

        # 通过保留前k个奇异值进行压缩
        k = int(compression_factor * min(img_array.shape))
        S_compressed = np.diag(S[:k])
        U_compressed = U[:, :k]
        Vt_compressed = Vt[:k, :]

        # 重建压缩图像
        img_compressed = np.dot(U_compressed, np.dot(S_compressed, Vt_compressed))
    else:  # 彩色图像
        # 分别对每个通道执行SVD
        img_compressed = np.zeros_like(img_array)
        for i in range(img_array.shape[2]):  # 遍历每个通道
            channel = img_array[:, :, i]
            U, S, Vt = np.linalg.svd(channel, full_matrices=False)

            # 压缩通道并保留前k个奇异值
            k = int(compression_factor * min(channel.shape))
            S_compressed = np.diag(S[:k])
            U_compressed = U[:, :k]
            Vt_compressed = Vt[:k, :]

            # 重建压缩通道
            img_compressed[:, :, i] = np.dot(U_compressed, np.dot(S_compressed, Vt_compressed))

    # 将数值限制在0-255范围内并转换回uint8类型
    img_compressed = np.clip(img_compressed, 0, 255).astype(np.uint8)

    # 通过添加'_compressed'后缀生成输出路径
    file_name, file_extension = os.path.splitext(image_path)
    output_path = f"{file_name}_compressed{file_extension}"

    # 保存压缩图像
    compressed_img = Image.fromarray(img_compressed)
    compressed_img.save(output_path)

    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="使用SVD压缩图像")
    parser.add_argument("input_file", help="输入图像文件路径")
    parser.add_argument("--compression_factor", type=float, default=0.1, help="压缩系数（默认值：0.1）")
    args = parser.parse_args()

    output_file = compress_image(args.input_file, args.compression_factor)
    print(f"压缩图像已保存为：{output_file}")

```
