---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 示波器基本介绍与用途
translated: true
type: note
---

**问：什么是示波器？**

**答：**

![Image](https://images.openai.com/static-rsc-4/LEfBgCBVsu0-UxUIFjJ59WV6tneLZN5qfv73bw6kYydr5WWwd2IWTPkJU8Q8QItkVInEGPetL6QYmp_rhTqABef3FJx1CxAlA_PrPE2bTxC6p_b5sxazc0Kq24UTYV_lfrOrWWXfRWe2x2BbCiLQfL_Nmd41pmqlQO_5SNLTjw5aa0bsD_xOpnTIHAks8HNB9?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/cJM-1UTRcdv2Z_4mFWaLox2N2ywUB2S6JOeed1VNHM5J-Sg6_5uUzdzy4YxKSmj8sk5cX94a-G6YYuxXeUO-_PUXdMFl2IhEaPm0DunYHBbXT3A8XbLpXsp35pkrDBWD_yM1ULo3jsWg6rDKaYWALN2-xz8f79Zd8Ssa8YTZxSoI5KzqQ5F3u-7hPCvYZfIm?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/KS0Do3WMB3szi4J3DDcindSUHQbTRQjrOgPj0_JCSHyD0KJMA1UfpDUdPcN3ORZP_7ZChPLGVNCzKer3B5Ji6goHp_5_uOoX4LIFHtSEs8WJIeH3vN-eIDTleYktEOlu7F0VTY9qwMi8s2mbk8Edkko4EeerHokmVJSZN6j1baL5yhD-E6SBiTaIVSgAMRe4?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/GwDXX3tH9GJDzrIdZZxyrQPlSH4imz2sJz2HIdaWl5vWSLDle6qR88iNIJsryRhp_uZXkcJBdzakAHuZ42Lwmat8S0aWc22dMe1PGic7GbVoo9tKTCfOTfV6Sfgx-W65R83tVCavvnmFe8Zn2ltw8ahRiCNVAhaTkdXhV8hZqwbNwqelF0h86qOEmrBnYiV2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/T8dZE8IodlkYQISYr1guzz76609gJ3BRvekuL4WtTKZlmV8uWWE_G8ITQcu11uLoMpiNV47Z2aISiwipGLZR-Ucb1NGM7qjoYDRbV_5OaJPKP8qpiGVRjYqMQdqr05xRN1dlfmK0a62DouCtZunfq7Bwrh1lUO9_q1JR7KMKg4nQE7TCA-EJwmo_W8hkfRnf?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/NiDqOwf64CJO4DHk2vep6vsbM36a4kG5l1zQfhasc-V3CxNR_9awphYbU9sss7tqPgBRXvnawxD5AY_4_J38VF1MvwzNNO77RtuL_epFuuTtRExA4sFK2gFBnGHjLjWV-1JcZgtJ7bmeDrUOzGOsZALQNe1ymVIawwT0LwL0YUToplnLsqb6y6_KHWgBIn-_?purpose=fullsize)

**示波器**是一种实验室仪器，它能让你**以波形形式随时间观察电信号**。

万用表显示的是单个数值：

```
电压 = 3.3V
电流 = 0.5A
电阻 = 10Ω
```

示波器显示的是**信号的形状**：

```
电压
  |
5V|       ┌───┐     ┌───┐
  |       │   │     │   │
0V|───────┘   └─────┘   └──── 时间
```

你可以看到：

* 电压变化
* 频率
* 噪声
* 毛刺
* 时序问题
* 通信信号

---

## 基本原理

示波器包含：

```
电路信号
      |
      v
 示波器探头
      |
      v
 ADC（模拟 → 数字）
      |
      v
 内存缓冲器
      |
      v
 显示波形
```

现代示波器本质上就是：

```
高速ADC + 计算机 + 显示器
```

关键参数：

### 1. 带宽

它能测量的信号速度。

例如：

* 20 MHz 示波器 → 适用于Arduino/简单电子电路
* 100 MHz → 常见爱好/专业入门级
* 1 GHz及以上 → 高速CPU、PCIe、DDR信号

100 MHz的示波器无法准确观测500 MHz的信号。

---

### 2. 采样率

每秒测量的次数。

例如：

```
1 GS/s = 每秒10亿次采样
```

对于100 MHz的信号，每个周期需要几个采样点。

---

### 3. 通道数

同时测量多少个信号：

* 1个通道：观测一个信号
* 2个通道：比较时钟与数据
* 4个通道：调试复杂系统

---

## 常见的应用场景

### Arduino / ESP32调试

例如：

ESP32发送PWM：

```
GPIO引脚

0V  ____      ____
       |____|
       1ms  1ms
```

示波器显示：

* PWM频率是否正确？
* 占空比是否正确？
* 是否存在噪声？

---

### 调试电源问题

你的电路板随机复位。

万用表：

```
3.3V
```

看起来正常。

示波器：

```
3.3V ──────────
          |
          ↓
       1.8V尖峰
```

你发现了一个持续20微秒的电压跌落。

---

### 串行通信

UART：

```
TX：

101101001011
```

示波器可以显示：

* 波特率
* 信号完整性
* 电压电平

对于SPI：

```
CLK  ─+-+-+-+-+
MOSI ─01011010
```

---

### CPU/GPU硬件

工程师使用示波器进行：

* DDR内存信号
* PCIe通道
* USB信号
* VRM供电
* 时钟电路

例如，调试一块GPU板卡：

```
12V电源
 |
 VRM
 |
 GPU核心电压
```

示波器可以看到：

```
1.0V 电源轨：

1.00V ─────────
       ↑
     纹波/噪声
```

---

## 示波器 vs 逻辑分析仪

两者有所重叠但不同。

### 示波器

测量**模拟真实情况**：

```
电压波形

0V ----/\----/\----
```

适用于：

* 电源
* 噪声
* 模拟电路
* 信号质量

### 逻辑分析仪

仅能看数字0/1：

```
0 1 1 0 1 0
```

适用于：

* 协议
* UART
* SPI
* I2C

便宜的逻辑分析仪：

```
$10 USB逻辑分析仪
```

便宜的示波器：

```
$200-500
```

---

## 对于你的人工智能+硬件实验

鉴于你正在玩：

* ESP32
* GPU
* 自定义硬件
* 服务器

当你从以下阶段推进时，示波器会变得非常有用：

```
软件调试
        |
        v
固件调试
        |
        v
电气调试
```

例如：

ESP32 + 传感器：

```
Python代码 ❌
固件 ❌
GPIO电压？
信号时序？
电源噪声？
```

示波器回答了最后这些问题。

一个适合初学者的原型设计示波器：

* 100 MHz带宽
* 1 GS/s采样率
* 2个通道

例如：

* Rigol DS1054Z
* Siglent Technologies SDS1104X-E

其思路类似于在软件中使用 `gdb`：
**调试器让你看到程序状态；示波器让你看到电气状态。**
