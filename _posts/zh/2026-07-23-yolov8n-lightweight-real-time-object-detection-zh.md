---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'YOLOv8n: 轻量级实时目标检测'
translated: true
type: note
---

YOLOv8n 代表 **YOLOv8 Nano**，是 Ultralytics 开发的 YOLOv8 系列中**最小且最快**的模型。它专为在计算能力有限的设备（如嵌入式系统、边缘设备、Raspberry Pi、NVIDIA Jetson 主板和移动硬件）上进行**实时物体检测**而设计。([Ultralytics 文档][1])

以下是名称的含义：

* **YOLO** = *You Only Look Once*，用于物体检测的深度学习模型系列。
* **v8** = YOLO 架构的第八代。
* **n** = **Nano**，表示最小的模型变体。

YOLOv8 系列包含多种模型尺寸：

| 模型 | 尺寸 | 速度 | 准确率 | 典型用途 |
| ------- | ---------- | -------------- | ------ | -------------------------------- |
| YOLOv8n | Nano | ⭐⭐⭐⭐⭐ 最快 | ⭐⭐⭐ | 边缘设备、实时应用 |
| YOLOv8s | Small | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 通用检测 |
| YOLOv8m | Medium | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 平衡性能 |
| YOLOv8l | Large | ⭐⭐ | ⭐⭐⭐⭐⭐ | 高精度应用 |
| YOLOv8x | Extra Large | ⭐ | ⭐⭐⭐⭐⭐+ | 最高精度 |

### YOLOv8n 能做什么？

YOLOv8n 可以针对多种计算机视觉任务进行训练：

* 物体检测（汽车、人、动物等）
* 实例分割
* 图像分类
* 姿态估计
* 物体跟踪（结合跟踪算法）([Ultralytics 文档][1])

### 为什么选择 YOLOv8n？

优点：

* 非常快的推理速度（实时性能）
* 模型体积小（易于部署）
* 内存占用更低
* 尽管尺寸紧凑，但准确率良好
* 非常适合嵌入式与物联网应用

缺点：

* 准确率低于 YOLOv8m、YOLOv8l 或 YOLOv8x 等更大模型
* 可能漏检非常小或难以检测的物体

### Python 使用示例

```python
from ultralytics import YOLO

# 加载 Nano 模型
model = YOLO("yolov8n.pt")

# 对图像进行物体检测
results = model("image.jpg")

# 显示结果
results[0].show()
```

### 典型应用场景

* 交通监控
* 人脸与人体检测
* 自主机器人
* 无人机视觉
* 智能监控摄像头
* 制造质量检测

总之，**YOLOv8n 是 YOLOv8 的轻量级（"Nano"）版本**，针对**速度和效率**进行了优化。当你需要在计算资源有限的硬件上实现实时检测时，它通常是最佳选择；而更大的变体则更适合在最大化检测精度更重要的场景下使用。([Ultralytics 文档][1])

[1]: https://docs.ultralytics.com/models/yolov8?utm_source=chatgpt.com "探索 Ultralytics YOLOv8"
