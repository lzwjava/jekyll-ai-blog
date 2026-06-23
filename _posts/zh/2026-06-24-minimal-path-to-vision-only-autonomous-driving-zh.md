---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 纯视觉自动驾驶的最简路径
translated: true
type: note
---

**问题：** 探索类特斯拉/openpilot的端到端自动驾驶（纯视觉、无激光雷达、在可获取硬件上运行）的最小可行路径是什么？

**答案：**

你的思路完全正确。让我来分解一下。

## openpilot的架构（它真的是端到端吗？）

openpilot是**部分**端到端的。它有两个主要神经网络：

```
摄像头帧 → [Supercombo模型] → 行驶轨迹 + 车道线 + 前车
轨迹 → [横向/纵向控制器] → 转向/油门/刹车
```

`Supercombo`模型是一个CNN+transformer混合模型（自2022年左右采用Vision Transformer骨干网络）。但**控制层仍然是经典的**——PID/MPC控制器将轨迹转换为执行器指令。

所以：**感知是学习的，控制是经典的**。不像特斯拉最新的FSD v12那样完全端到端，后者直接输出执行器指令。

**特斯拉FSD v12**（2024年）是真正的端到端转变——视频输入，转向/油门输出，大规模transformer。Wayve、NVIDIA DriveE2E类似。

**小鹏/理想汽车**——是的，它们都在2023-2024年左右转向了基于transformer的端到端感知，类似于学术界的UniAD/VAD架构。

---

## 你的最小可行探索路径

你不需要一辆车。以下是阶梯：

### 第1级：纯软件——复现openpilot的感知

```python
# 使用comma.ai的数据集（comma2k19，约33小时驾驶数据）
# https://github.com/commaai/comma2k19

# 在驾驶视频上运行supercombo ONNX模型
import onnxruntime as ort
import numpy as np

session = ort.InferenceSession("supercombo.onnx")
# 输入：[batch, 12, 128, 256] — 2帧，YUV420
# 输出：轨迹，车道线，前车
```

comma.ai 发布了模型权重。你可以在任何行车记录仪视频上运行推理。

### 第2级：手机作为传感器（你的想法——非常好）

```
手机摄像头 → 帧捕获 → MobileNet/YOLO → 车道线检测 + 深度
           → 简单路径规划 → 显示叠加层
```

这正是**手机上的openpilot**实验所做的。有一些`openpilot-on-laptop`仓库。手机提供：

- 30fps摄像头
- IMU（陀螺仪/加速度计）——对运动估计至关重要
- GPS

### 第3级：智辉君路线——自动驾驶自行车/小车

智辉君使用了一辆自行车，搭载：

- 树莓派 / Jetson Nano
- 摄像头
- 舵机用于转向

最低硬件配置：

```
Jetson Orin Nano ($250)
+ USB摄像头或Pi摄像头
+ RC车底盘（约$50）
+ PWM舵机控制器
```

这实际上是最好的学习路径——你能获得真实的执行反馈。

### 第4级：真正的端到端（你最终应努力构建的方向）

```python
# 输入：摄像头帧序列（类似特斯拉）
# 输出：[转向角，油门，刹车]

# 架构：视频Transformer（类似Gato/RT-2）
class E2EDriver(nn.Module):
    def __init__(self):
        self.backbone = ViT(...)       # 帧编码器
        self.temporal = Transformer(...)  # 序列建模
        self.head = MLP(out=3)         # 转向，油门，刹车

    def forward(self, frames):  # [B, T, C, H, W]
        tokens = self.backbone(frames)
        context = self.temporal(tokens)
        return self.head(context[:, -1])  # 最后一个token
```

先基于模仿学习（BC）训练，然后加入DAgger或RLHF。

---

## 数据

关键瓶颈是数据，而非模型架构：

- **comma2k19** — 免费，33小时，美国高速
- **nuScenes** — 多传感器，适合研究
- **Waymo开放数据集** — 高质量
- **你自己的行车记录仪** — 对你的用例最相关

---

## 推荐探索技术栈

```
第1阶段（本周）：
  - 下载comma2k19
  - 在样本帧上运行supercombo.onnx
  - 可视化轨迹输出

第2阶段（下个月）：
  - 搭建手机→帧流→笔记本电脑推理管线
  - 使用ONNX或torch实现车道线检测

第3阶段（硬件）：
  - RC车 + Jetson Orin Nano
  - 用自己的驾驶数据训练小型模仿学习模型
  - 闭环：摄像头→模型→舵机
```

---

## 需要阅读的关键论文

- **UniAD** (2023) — "Planning-oriented Autonomous Driving"，NeurIPS最佳论文
- **VAD** — 面向端到端的向量化场景表示
- **Wayve GAIA-1** — 驾驶生成式世界模型
- **特斯拉FSD v12博客** — 端到端执行器级控制

---

你的直觉是对的——在廉价平台上实现纯视觉端到端正是特斯拉的哲学，也是最具学习性的路径。对于你这样的水平，RC车/自动驾驶自行车确实是真正的最小可行实验（MVE）。在玩具上闭环感知→行动回路，比阅读10篇论文能学到更多东西。

**参考资料：**

- [comma.ai supercombo模型](https://github.com/commaai/openpilot)
- [comma2k19数据集](https://github.com/commaai/comma2k19)
- [UniAD论文](https://arxiv.org/abs/2212.10156)
- [笔记本电脑上的openpilot实验](https://github.com/commaai/openpilot/tree/master/tools)
