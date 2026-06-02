---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: ESP32-CAM紧凑型开发板概览
translated: true
type: note
---

### 什么是 ESP32-CAM？

ESP32-CAM 是乐鑫科技推出的一款紧凑型低成本开发板，集成了高性能 ESP32 微控制器与摄像头模块。该板专为物联网项目设计，特别适用于图像采集、视频流传输和计算机视觉应用。"CAM" 指的是板载 OV2640 摄像头传感器，最高支持 200 万像素（1600x1200）分辨率。

#### 核心特性

- **处理器与连接性**：搭载双核 ESP32 芯片（Xtensa LX6 架构，主频最高 240 MHz），配备 520KB SRAM 和 4MB PSRAM。支持 Wi-Fi（802.11 b/g/n）与双模蓝牙（经典模式与低功耗模式）。
- **摄像头**：采用 OV2640 CMOS 图像传感器，配备可调焦镜头，支持 JPEG、BMP 和灰度图像格式。
- **功耗与尺寸**：工作电压 3.3V（可通过稳压器支持 5V），拍摄时功耗低于 200mA，尺寸仅 27x40.5x4.5毫米，非常适合嵌入式项目。
- **I/O 接口**：提供 10 个 GPIO 引脚（部分与摄像头复用）、microSD 卡槽用于存储，支持通过扩展连接传感器。
- **编程开发**：兼容 Arduino IDE、ESP-IDF 和 MicroPython，可通过 GitHub 上的 esp32-camera 等库实现图像处理与流媒体功能。

#### 典型应用场景

- **DIY 安防摄像头**：通过 Wi-Fi 向手机或浏览器传输实时视频流，支持运动检测功能。
- **图像识别**：结合 TensorFlow Lite 等 AI 工具实现物体检测。
- **监控系统**：远程拍照、延时摄影或野生动物监测相机。
- **原型开发**：机器人、智能家居设备或增强现实实验。

该开发板因价格亲民（通常低于 10 美元）和易于部署而深受创客欢迎，但初学者可能需要 USB 转串口适配器进行初始编程。如需更高质量视频，可选择 ESP32-S3-CAM 等新型号，但原版 ESP32-CAM 仍是简单项目的首选方案。

#### 参考资源

- [ESP32-CAM 摄像头模块亚马逊页面](https://www.amazon.com/HiLetgo-ESP32-CAM-Development-Bluetooth-Raspberry/dp/B07RXPHYNM)
- [乐鑫 ESP32-Camera GitHub 代码库](https://github.com/espressif/esp32-camera)
- [M5Stack ESP32-CAM 文档](https://docs.m5stack.com/en/unit/esp32cam)
- [Instructables：基于 ESP32-CAM 的超低成本安防摄像头](https://www.instructables.com/Super-Cheap-Security-Camera-With-ESP32-cam/)
- [DFRobot ESP32-CAM 数据手册（PDF）](https://media.digikey.com/pdf/Data%2520Sheets/DFRobot%2520PDFs/DFR0602_Web.pdf)
