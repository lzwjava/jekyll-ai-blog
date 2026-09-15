---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 设备维修热成像技术
translated: true
type: note
---

问题：**如何获取热成像图片，它们对 GPU / 手机 / 笔记本电脑维修有多大用处？**

答案：**非常有用——但主要用于电源/热故障，而不是万能 X 光。** 热成像相机会给你一张空间的功率耗散分布图。

关键的思维模型是：

$$
P = V I = I^2R = \frac{V^2}{R}
$$

故障元件、短路的电源轨、损坏的 MOSFET、漏电的电容、损坏的 IC 等都会将电能转化为局部热量。热成像相机让你无需触碰主板就能看到**热量出现在哪里**。

![Image](https://images.openai.com/static-rsc-4/P73v6MC6zp_DzfbmsyxZ8_xMA7fYDMb7ZwbGKDR7ANWbYN8Tg5s11BIOdmfp6zlIq1Ji3NPsyJj4UkJB520xgx9ktXVDjDmU7BXtKQ6vcMjnpjTCHuqMzVNPEKDzNKzrcVb6tqa6-F-CiXK8nlO3Yg29Q6EJhCZvA1FB-J5rjEhjJFIcfgDlJ57BIkjneAAf?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/RIzkPptVXIggCsY5USK9MC-_4hJTCA8gcwslXy6ic-knLwl89IiEQlqh1wGJMOp8N6PMJxnNopAs8EPLRuDcIeinA5mdmaUzAXorEMb3uq72EOGURR8weo32Jz66CKfXoLz4AVmIA8o0a2xiO0Dtv1--bBRF6FxuxQ8LZdX_A9vrsfqStML1eXjaS-qIRHMK?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/X6xzI2kvMEAIXfx_nc77-MwL9uO8ZfjV4GDvaYHM21bjJ-3S0X_MVaTR_O9VbSEudL_6i4gxVE6U1-5Yn-8ZM1u1YkoGeHbOT7r8tlAtdAmcazJAjNu4VdL4pavOshg6lOdLqWj2oHgUed2wKOX2L8nPwdONtTPTlbZN67h1svnin_Mqn6KpRoBMU3zVbbwM?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/pF8_6QWJsiQix__JQPlXZVQU7-QX-Cbm7ByyuElSraijLjz-sOY81d23Mit8EugWF9YXUShQHbFmm8jI_6r6RxQA2G5rs7aSI49DhxiXfGc-5DACgSvPIF7hxajEd2cvtTDl4Esqgx-64-Dki1-BTv2S7iCtltJwI2t6V2LCDyaPoOVsnrn0yTSJsnD_wea0?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3Z3G7OfDVBjgmIGxmR7iBq0reqAJR2TcmRaAYFDsLSS49Ul6lBLNh2piIcB_qozRYg1t7IR4FdCDJ7eu0UBGXFTiVoj_x_Fx6nnFtlpPHyzpClfWS3D_NHJmycmN5k8BPxU_1HnCUV-dJ5_V5_YM4LfSRj-wLh9PJFvQ5UQaiLI1LWVSarECUjX7FYEW9IX8?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/_apHiPSCN1xMtmTD_-hDf1dRk3RZI9QwGsh-m9ATjeUF32X4-8zloYchM7AKCw5JLZ4YjB-ZHsaEjYg5_LShBySq3sUTd4lNV-b5OrSg23euyTAGrLIiZRopiAlMeChbzmE_uG1im-fKa1GnwbOIfNQ7LncA2dK-xNjKDzqrWEAavdKtF4kEN2H79YPnILFd?purpose=fullsize)

### 1. GPU 维修

这可能是最有趣的应用之一。

假设一个 GPU 具有：

```text
12V
 │
 ├── VRM ── GPU core
 │
 ├── memory VRM ── GDDR
 │
 └── other power rails
```

给主板通电并进行扫描。

正常：

```text
VRM      VRM       GPU
██       ██        █████
30°C     32°C      45°C
```

故障：

```text
VRM      VRM       GPU
██       🔥        █████
31°C     95°C      45°C
```

这立刻告诉你**哪个区域消耗了异常功率**。

例如：

* 短路的 MLCC → 微小的局部热点
* 损坏的 MOSFET → MOSFET 变得极热
* 坏的 VRM → 电感/MOSFET 区域异常发热
* GPU 核心漏电 → GPU 封装异常发热
* 损坏的内存电源轨 → 内存 VRM 变热
* 短路的电源轨 → 离短路位置最近的元件可能成为热特征

FLIR 特别提到 PCB 热成像对于发现过热元件、电源元件问题和走线损坏非常有用。([FLIR][1])

### 2. 手机主板维修

这是热成像变得**真正强大**的地方。

想象一下：

```text
手机无法开机

        ↓

台式电源
        ↓
电流 = 0.8 A
        ↓
热成像相机
        ↓
        🔥
       MLCC
        ↓
VDD 电源轨短路
```

与其逐一拆除 50 个电容，你通常可以：

1. 识别可疑的电源轨。
2. 向该电源轨注入一个**安全的、限流电压**。
3. 观察主板的温度变化。
4. 找到第一个发热的元件。
5. 移除/更换它。
6. 确认热特征消失。

这是一种极其有用的维修工作流程。

但有一个重要的限制：

**最热的元件不一定就是故障元件。**

热量可以通过铜平面、封装、焊料等传导。所以热成像给你的是一个**空间线索**，而不是因果关系的证明。

---

### 3. 笔记本电脑维修

同样适用于：

* 主板损坏
* 19 V 电源轨短路
* 5 V / 3.3 V 电源轨短路
* CPU/GPU VRM 问题
* CPU/GPU 过热
* 坏的 MOSFET
* 充电电路异常
* USB-C PD 故障
* 电池/充电问题
* 散热器接触不良
* 风扇/散热问题

例如：

```text
正常笔记本电脑：

CPU       VRM          GPU
🔥🔥       🔥           🔥🔥
70°C      50°C         65°C


故障：

CPU       VRM          GPU
🔥🔥       🔥🔥🔥🔥🔥    🔥🔥
70°C      110°C        65°C
              ↑
          需要调查
```

但请记住：**在正常负载下发热的元件不一定就是有故障的。** FLIR 明确警告，设备在负载下正常会发热；你需要知道正常的热模式应该是什么样的。([FLIR][2])

---

## 应该购买什么相机？

你不一定需要一台价值 5000 美元以上的专业热成像相机。

对于主板维修，我会考虑**手机连接式热成像相机**，特别是那些具有足够空间分辨率、能够看到单个元件的型号。

一个有趣的选择是 **HIKMICRO Mini2 V2**：

* 256 × 192 热分辨率
* <40 mK 热灵敏度
* 25 Hz
* -20°C 至 400°C
* USB-C / Lightning 版本
* 由手机供电
* 约 20 克

[HIKMICRO Mini2 V2 官方规格](https://www.hikmicrotech.com/en_us/industrial-products/mini2-v2-thermal-camera-phone-attachment/?utm_source=chatgpt.com)

对于**实际 PCB 维修**更有趣的是 **HIKMICRO Mini2Plus V2**，因为它具有手动对焦微距模式。HIKMICRO 声称在桌面支架配置下可以分辨约 **340 µm** 的物体，并特别提到了 PCB 元件。([Hikmicrotech][3])

对于维修来说，微距能力比拥有巨大的测温范围重要得多。

---

## 最重要的规格不是测温范围

对于主板维修，我会优先考虑：

```text
1. 空间分辨率
2. 热灵敏度 (NETD)
3. 微距 / 最小对焦距离
4. 手动对焦
5. 帧率
6. 图像/视频录制
7. PC/API 访问
8. 测温精度
```

你并不真正关心相机能否测量：

```text
-20 → 400°C
```

如果一颗 0.5 毫米的小电容只占用一个像素。

你关心的是：

```text
元件
   ↓
████████
████████   ← 足够的像素
████████
```

而不是：

```text
元件
   ↓
█
```

---

## 还有第二种技术更有意思

不要只拍摄热成像照片。

使用**动态给主板供电时的热成像视频**。

例如：

```python
while True:
    frame = thermal_camera.read()

    hotspot = detect_hotspot(frame)

    if hotspot.temperature > threshold:
        print(hotspot.position,
              hotspot.temperature)
```

然后你可以观察到：

```text
t=0.0s   24°C
t=0.5s   27°C
t=1.0s   35°C
t=1.5s   52°C
t=2.0s   78°C  ← 可疑
```

这种时间行为信息量非常大。

一个正常的 IC 可能看起来像：

```text
24 → 30 → 38 → 45°C
```

而短路可能看起来像：

```text
24 → 30 → 50 → 80 → 110°C
```

非常迅速。

---

## 这开启了一个有趣的 AI 应用

考虑到你在 agent/模型方面的工作，我不会把这仅仅视为**“买热成像相机 → 看图片”**。

我会构建：

```text
热成像相机
      │
      ▼
热成像视频
      │
      ▼
元件定位
      │
      ├── PCB 视觉图像
      │
      ├── 原理图
      │
      ├── 板图
      │
      └── 电气测量
      │
      ▼
LLM / 视觉模型
      │
      ▼
"可能的故障区域"
      │
      ▼
维修步骤
```

例如：

```text
热成像：
    U7200 = 91°C
    周围区域 = 31°C

万用表：
    VCORE = 0.4V

板图：
    U7200 → VCORE 稳压器

原理图：
    VCORE → GPU 核心

AI：

"U7200 是置信度最高的异常热源。
鉴于 VCORE 电阻为 0.8Ω，
最可能的故障是 VCORE 负载过大。
检查 U7200 MOSFET 和下游 MLCC。"
```

现在热成像变成了**自动化主板调试 agent 中的一个传感器**，而不仅仅是一台花哨的相机。

这可能有趣得多。

### 一个重要提醒

热成像图像不是普通的 RGB 照片。闪亮的铜/铝及其他低发射率表面可能会产生误导性的温度读数，因为它们会反射红外辐射。FLIR 建议特别注意发射率和反射温度；他们的 PCB 示例对塑料和金属使用了不同的发射率假设。([FLIR 支持中心][4])

因此，在维修工作中，首先要学会解读**相对热模式**；不要盲目相信“这个元件显示 83.2°C”。

参考资料：

* [FLIR — PCB 热故障排查](https://www.flir.com/fr-fr/support/training/thermography-training/webinars/see_the_heat_troubleshooting_pcb_electronic_product_design_with_thermal_imaging/?utm_source=chatgpt.com)
* [FLIR — 使用热成像进行电子产品测试](https://www.flir.com/globalassets/industrial/17-3553-ins-ets-brochure_final_v1_web.pdf?utm_source=chatgpt.com)
* [HIKMICRO Mini2 V2](https://www.hikmicrotech.com/en_us/industrial-products/mini2-v2-thermal-camera-phone-attachment/?utm_source=chatgpt.com)
* [HIKMICRO Mini2Plus V2 微距热成像相机](https://www.hikmicrotech.com/en/industrial-products/mini2plus-v2-thermal-camera-phone-attachment/?utm_source=chatgpt.com)
* [FLIR — 发射率与热测量](https://www.flir.com/discover/professional-tools/how-does-emissivity-affect-thermal-imaging/?utm_source=chatgpt.com)

[1]: https://www.flir.com/fr-fr/support/training/thermography-training/webinars/see_the_heat_troubleshooting_pcb_electronic_product_design_with_thermal_imaging/?utm_source=chatgpt.com "“See the Heat - Troubleshooting PCB & Electronic Product Design with Thermal Imaging Webinar | Flir"
[2]: https://www.flir.com/discover/professional-tools/thermal-camera-tips-to-avoid-common-home-inspection-mistakes/?utm_source=chatgpt.com "Thermal Cameras Tips to Avoid Common Home Inspection Mistakes | Flir"
[3]: https://www.hikmicrotech.com/en/industrial-products/mini2plus-v2-thermal-camera-phone-attachment/?utm_source=chatgpt.com "HIKMICRO Mini2Plus V2 Infrared Smartphone Camera For ios And Android"
[4]: https://flir.custhelp.com/app/answers/detail/a_id/1283?utm_source=chatgpt.com "FLIR - ETS320 camera use with FLIR Tools"
