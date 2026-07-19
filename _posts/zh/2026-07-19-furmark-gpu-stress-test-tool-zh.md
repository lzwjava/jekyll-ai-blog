---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FurMark GPU压力测试工具
translated: true
type: note
---

**问题：什么是 FurMark 1.39 GPU 测试工具？**

**回答：**

FurMark 是一款 **GPU 压力测试 / 老化测试工具**。它渲染一个非常繁重的“毛绒甜甜圈”OpenGL 场景，将 GPU 推至接近最大负载，主要用于测试：

* GPU 散热系统
* 热行为
* 电源稳定性
* GPU 核心稳定性
* 超频/降压稳定性
* 购买二手显卡时检查显卡状态

FurMark 1.39.x 是 Geeks3D 的较老一代版本。1.39.0 版于 2025 年发布；1.39.3.0 是后续的 1.39 分支版本。([MajorGeeks][1])

基本思路：

```
FurMark
   |
   v
生成极端的 GPU 工作负载
   |
   v
GPU 核心 -> 99%
VRAM -> 活跃
功耗 -> 接近 TDP 限制
温度 -> 最高
   |
   v
观察：
  - 崩溃？
  - 图像异常？
  - 过热？
  - 频率降频？
```

它被称为 **“GPU 烤机工具”**，因为它故意产生异常高的热负载。([MajorGeeks][1])

---

### 对于购买二手 RTX 3090 / 3060 / 7900 XT（你的情况）

FurMark 实际上很有用。

典型的二手测试流程：

1. 先运行 GPU-Z：

   * 检查 GPU 型号
   * VRAM 容量
   * BIOS
   * PCIe 链路

2. 运行 FurMark：

```
分辨率：1920x1080
MSAA：0x
持续时间：10-20 分钟
```

观察：

### 好的 RTX 3090 示例

```
GPU 使用率：       99%
功耗：           350W+
温度：           70-85°C
频率：          稳定
图像异常：      无
驱动崩溃：      无
```

### 坏卡迹象

```
温度：
95°C 以上

频率：
1800MHz -> 900MHz

屏幕：
彩色点
闪烁多边形
黑屏

驱动：
“NVIDIA 驱动已停止响应”
```

---

### 但 FurMark 不是真正的人工智能工作负载测试

对于你的 LLM/训练用途：

FurMark 测试：

```
图形渲染管线
OpenGL
着色器负载
热极限
```

它 **不** 测试：

```
CUDA
Tensor Core
VRAM ECC 行为
PyTorch 稳定性
长时间训练稳定性
```

对于 AI 显卡检查，我建议结合：

### 1. VRAM 测试

```
python -m pip install gpu-burn
gpu_burn 600
```

或

```
memtest_vulkan
```

### 2. CUDA 测试

```python
import torch

x = torch.randn(
    (20000,20000),
    device="cuda"
)

for i in range(100):
    y = x @ x
    torch.cuda.synchronize()

print("OK")
```

### 3. 真实 AI 工作负载

示例：

```
vllm serve Qwen3-32B
```

或

```
torchrun train.py
```

运行数小时。

---

对于你的二手显卡购买：

* **FurMark + GPU-Z + CUDA 测试** 是一个良好的最低要求。
* 对于 RTX 3090 特别地，还要检查：

  * 显存温度（GDDR6X 可能达到 100°C 以上）
  * 风扇噪音
  * 电源接口状况
  * BIOS 是否被修改用于挖矿

FurMark 只能告诉你“这张卡能承受烤机负载”，但不能保证显存健康。([TechPowerUp][2])

参考文献：

* FurMark GPU 压力测试概述 ([MajorGeeks][1])
* FurMark 版本历史/下载 ([TechPowerUp][2])

[1]: https://www.majorgeeks.com/files/details/furmark.htm?utm_source=chatgpt.com "下载 FurMark 1.39.3.0 - MajorGeeks"
[2]: https://www.techpowerup.com/download/furmark/?utm_source=chatgpt.com "Furmark 2.9.0 下载 | TechPowerUp"
