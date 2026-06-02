---
audio: false
generated: true
lang: zh
layout: post
title: 基尔霍夫定律与Arduino应用
translated: true
type: note
---

使用 Arduino 验证基尔霍夫定律——特别是基尔霍夫电流定律（KCL）和基尔霍夫电压定律（KVL）——是融合电子学理论与动手实验的绝佳方式。KCL 指出，流入节点的总电流等于流出节点的总电流；而 KVL 则指出，闭合回路中电压降的总和等于电源电压。下面将介绍如何设计简单电路，并使用 Arduino 测量电流和电压来验证这些定律。

由于 Arduino 无法直接测量电流，我们将通过测量电阻两端的电压（使用欧姆定律：\\( I = V/R \\))来间接计算电流，并通过其模拟引脚（0-5V 范围）测量电压。接下来，我将概述两个实验——一个用于 KCL，一个用于 KVL——包含分步说明、接线图和代码。

---

### **实验一：验证基尔霍夫电流定律（KCL）**

#### **目标**
证明流入节点的电流等于流出节点的电流。

#### **电路设置**
- **组件：**
  - Arduino（例如 Uno）
  - 3 个电阻（例如 R1 = 330Ω，R2 = 470Ω，R3 = 680Ω）
  - 面包板和跳线
  - 5V 电源（Arduino 的 5V 引脚）
- **接线：**
  - 将 Arduino 的 5V 引脚连接到一个节点（称为节点 A）。
  - 从节点 A 连接 R1 到 GND（支路 1）。
  - 从节点 A 连接 R2 到 GND（支路 2，与 R1 并联）。
  - 从节点 A 连接 R3 到 GND（支路 3，与 R1 和 R2 并联）。
  - 使用 Arduino 模拟引脚测量每个电阻两端的电压：
    - A0 跨接 R1（一个探针在节点 A，另一个在 GND）。
    - A1 跨接 R2。
    - A2 跨接 R3。
- **注意：** GND 是公共参考点。

#### **理论**
- 从 5V 流入节点 A 的总电流（\\( I_{in} \\)）分成 \\( I_1 \\)、\\( I_2 \\) 和 \\( I_3 \\)，分别通过 R1、R2 和 R3。
- KCL：\\( I_{in} = I_1 + I_2 + I_3 \\)。
- 测量每个电阻两端的电压，然后计算电流：\\( I = V/R \\)。

#### **Arduino 代码**
```cpp
void setup() {
  Serial.begin(9600); // 启动串行通信
}

void loop() {
  // 读取电压值（0-1023 映射到 0-5V）
  int sensorValue1 = analogRead(A0); // R1 两端的电压
  int sensorValue2 = analogRead(A1); // R2 两端的电压
  int sensorValue3 = analogRead(A2); // R3 两端的电压

  // 转换为电压值（5V 参考电压，10 位 ADC）
  float V1 = sensorValue1 * (5.0 / 1023.0);
  float V2 = sensorValue2 * (5.0 / 1023.0);
  float V3 = sensorValue3 * (5.0 / 1023.0);

  // 电阻值（单位：欧姆）
  float R1 = 330.0;
  float R2 = 470.0;
  float R3 = 680.0;

  // 计算电流（I = V/R）
  float I1 = V1 / R1;
  float I2 = V2 / R2;
  float I3 = V3 / R3;

  // 流入节点的总电流（假设电源电压为 5V）
  float totalResistance = 1.0 / ((1.0/R1) + (1.0/R2) + (1.0/R3)); // 并联电阻
  float Iin = 5.0 / totalResistance;

  // 输出结果
  Serial.print("I1 (mA): "); Serial.println(I1 * 1000);
  Serial.print("I2 (mA): "); Serial.println(I2 * 1000);
  Serial.print("I3 (mA): "); Serial.println(I3 * 1000);
  Serial.print("Iin (mA): "); Serial.println(Iin * 1000);
  Serial.print("I1+I2+I3 之和 (mA): "); Serial.println((I1 + I2 + I3) * 1000);
  Serial.println("---");

  delay(2000); // 等待 2 秒
}
```

#### **验证**
- 打开串行监视器（在 Arduino IDE 中按 Ctrl+Shift+M，波特率设置为 9600）。
- 比较 \\( I_{in} \\)（根据总电阻计算得出）与 \\( I_1 + I_2 + I_3 \\)。它们应大致相等，从而验证 KCL。
- 微小差异可能源于电阻容差或 Arduino ADC 精度。

---

### **实验二：验证基尔霍夫电压定律（KVL）**

#### **目标**
证明闭合回路中电压降的总和等于电源电压。

#### **电路设置**
- **组件：**
  - Arduino
  - 2 个电阻（例如 R1 = 330Ω，R2 = 470Ω）
  - 面包板和跳线
  - 5V 电源（Arduino 的 5V 引脚）
- **接线：**
  - 将 5V 连接到 R1。
  - 将 R1 连接到 R2。
  - 将 R2 连接到 GND。
  - 测量电压：
    - A0 跨接整个回路（5V 到 GND）以确认电源电压。
    - A1 跨接 R1（5V 到 R1 和 R2 的连接点）。
    - A2 跨接 R2（连接点到 GND）。
- **注意：** 使用分压器设置；确保电压不超过 5V（Arduino 的限制）。

#### **理论**
- KVL：\\( V_{source} = V_{R1} + V_{R2} \\)。
- 测量每个电压降，并检查它们的总和是否等于电源电压（5V）。

#### **Arduino 代码**
```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  // 读取电压值
  int sensorValueSource = analogRead(A0); // 5V 到 GND 之间的电压
  int sensorValueR1 = analogRead(A1);     // R1 两端的电压
  int sensorValueR2 = analogRead(A2);     // R2 两端的电压

  // 转换为电压值
  float Vsource = sensorValueSource * (5.0 / 1023.0);
  float VR1 = sensorValueR1 * (5.0 / 1023.0);
  float VR2 = sensorValueR2 * (5.0 / 1023.0);

  // 输出结果
  Serial.print("Vsource (V): "); Serial.println(Vsource);
  Serial.print("VR1 (V): "); Serial.println(VR1);
  Serial.print("VR2 (V): "); Serial.println(VR2);
  Serial.print("VR1 + VR2 (V): "); Serial.println(VR1 + VR2);
  Serial.println("---");

  delay(2000);
}
```

#### **验证**
- 在串行监视器中，检查 \\( V_{source} \approx V_{R1} + V_{R2} \\)。
- 对于串联的 R1 = 330Ω 和 R2 = 470Ω，预期 \\( V_{R1} \approx 2.1V \\) 和 \\( V_{R2} \approx 2.9V \\)（基于分压公式：\\( V_{R1} = 5 \cdot \frac{R1}{R1+R2} \\)），总和约为 5V。

---

### **提示与注意事项**
- **精度：** Arduino 的 10 位 ADC（0-1023）分辨率约为 4.9mV，因此可能存在微小误差。如有需要，可使用万用表进行交叉检查。
- **安全：** 保持电压低于 5V，电流较低，以避免损坏 Arduino。
- **扩展：** 对于更复杂的电路，可以添加更多电阻或使用外部传感器（例如 INA219 用于直接电流测量）。
- **调试：** 如果结果不匹配，请检查电阻值、连接和 GND 的一致性。

这些实验简化了实际条件，但有效地演示了基尔霍夫定律。想要调整这些设置或需要特定部分（如接线或代码）的帮助吗？请告诉我！
