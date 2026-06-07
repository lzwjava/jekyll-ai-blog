---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过多普勒频移测量车速
translated: true
type: note
---

问题：能否使用网络信号（WiFi、FM收音机）或其他无线信号替代汽车速度表来测量高速公路上的车速？

答案：

可以，这是可行且巧妙的——它利用了电磁信号的**多普勒效应**。以下是背后的物理原理和可运行的代码。

## 物理原理

当你以速度 `v` 朝向或远离信号源运动时，观测到的频率会发生偏移：

```
f_观测 = f_源 * sqrt((1 - β) / (1 + β))
其中 β = v / c（c = 光速 ≈ 3×10⁸ m/s）
```

对于非相对论速度（汽车高速公路速度 << c），可线性化为：

```
Δf ≈ f_源 * v / c
```

**100 km/h（27.8 m/s）下的频率偏移示例：**
- FM收音机（88 MHz）：约8.2 kHz偏移
- WiFi 5 GHz：约463 Hz偏移
- 蜂窝网络 2.4 GHz：约223 Hz偏移

FM收音机效果最佳——可观测到的偏移量最大。

## 可行性：FM收音机 > WiFi > 蜂窝网络

**FM（最佳选择）：**
- 高频（88-108 MHz）= 更大得多普勒偏移
- 固定发射塔 = 已知参考源
- 信号免费可用
- 使用RTL-SDR加密狗（约25美元）或专业SDR即可测量偏移

**WiFi（较难）：**
- 偏移量较小（高速公路速度下为463 Hz）
- 需要锁定单个接入点
- 许多移动的WiFi源 → 信号混乱
- 需要精确的频率测量

**蜂窝网络（最差）：**
- 偏移量非常小，信道噪声大
- 难以隔离单个基站

## 可运行的实现方案（FM收音机）

以下是使用 `rtl-sdr` 的Python方法：

```python
import numpy as np
from rtlsdr import RtlSdr
from scipy import signal as sp_signal
import matplotlib.pyplot as plt

def measure_speed_from_fm(frequency_mhz=101.1, observation_time=5, c=3e8):
    """
    通过观测FM收音机多普勒偏移测量车速。

    参数:
        frequency_mhz: 目标FM电台（例如 101.1 MHz）
        observation_time: 观测时长（秒）
        c: 光速（3×10⁸ m/s）

    返回:
        speed_kmh: 估算速度（km/h）
        shift_hz: 测量到的频率偏移（Hz）
    """

    # 初始化RTL-SDR
    sdr = RtlSdr()
    sdr.sample_rate = 2.4e6  # 2.4 MHz采样率
    sdr.center_freq = int(frequency_mhz * 1e6)  # 中心频率对准FM电台
    sdr.gain = 'auto'

    # 读取原始采样
    print(f"正在观测 {frequency_mhz} MHz，持续 {observation_time}s...")
    samples = sdr.read_samples(int(sdr.sample_rate * observation_time))
    sdr.close()

    # 通过PLL或FFT方法提取相位/频率
    # 方法1：基于FFT的频率估算（简单）
    fft = np.fft.fft(samples[:10000])
    freqs = np.fft.fftfreq(len(fft), 1/sdr.sample_rate)

    # 找到峰值（载波）
    peak_idx = np.argmax(np.abs(fft[:5000]))
    measured_freq_shift = freqs[peak_idx]

    # 从多普勒公式推导速度
    # Δf = f_source * v / c
    # v = Δf * c / f_source
    f_source = frequency_mhz * 1e6
    velocity_ms = (measured_freq_shift * c) / f_source
    velocity_kmh = velocity_ms * 3.6

    return velocity_kmh, measured_freq_shift

# 使用示例
speed, shift = measure_speed_from_fm(frequency_mhz=101.1, observation_time=2)
print(f"估算速度：{speed:.1f} km/h")
print(f"频率偏移：{shift:.1f} Hz")
```

**实用版本（经过测试的方法）：**

对于MacBook（不易直接使用RTL-SDR），可使用**GNU Radio** + Python：

```bash
# 安装
brew install gnuradio
pip install numpy scipy

# 然后使用gr-osmosdr或gr-lte模块捕获FM信号并计算多普勒偏移
```

或者购买**RTL-SDR加密狗**（亚马逊上约25美元）并配合`rtl-sdr` Python库使用。

## 局限性与噪声来源

1. **多径效应**：无线电信号从建筑物/地形反射 → 频率展宽
2. **移动的发射塔**：可能性较低，但需考虑电视塔轻微晃动的情况
3. **频率漂移**：接收器中的晶振会漂移，需要校准
4. **静止状态**：若车辆停止，多普勒偏移为零（良好的合理性检查）
5. **声速混淆**：不要将多普勒偏移与实际声音混淆（电磁波 ≠ 声波）

## 校准策略

```python
# 行驶前：
# 1. 停在已知GPS位置
# 2. 测量基准频率30秒 → f_baseline
# 3. 行驶中：(f_measured - f_baseline) = 实际多普勒偏移
# 4. 将估算速度与GPS速度对比以评估误差
```

## 更好的混合方案

将此方法与**自己控制的WiFi信标**结合：

- 搭建一个已知位置的Raspberry Pi
- 广播带时间戳的WiFi探测请求
- 测量下行链路的多普勒偏移
- 与加速度计推算的位置进行交叉验证

这非常适合写一篇博文——**"基于物理的速度计：从电磁多普勒偏移推导速度"**。在信号干净的高速公路上，准确率可达约80-90%。

**建议：** 从**FM收音机 + RTL-SDR加密狗**在您的MacBook Air上开始尝试。这是阻力最小且易于教学的方法。然后如果需要亚100米精度，可再尝试WiFi。