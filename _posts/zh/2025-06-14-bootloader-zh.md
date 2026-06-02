---
audio: false
generated: true
lang: zh
layout: post
title: 烧录引导程序
translated: true
type: note
---

为 Arduino Uno R3 烧录引导程序在微控制器（ATmega328P）空白、损坏或需要更换时是必需的操作。该过程会向芯片写入与 Arduino IDE 通信并运行草图所需的固件。以下是使用常见方法烧录引导程序的逐步指南。

---

### **准备工作**

- **Arduino Uno R3**（需烧录引导程序的目标板，搭载 ATmega328P）
- **编程器**：以下任选其一：
  - 另一块正常工作的 Arduino 开发板（如额外的 Uno R3）作为 "Arduino as ISP"
  - 专用编程器如 **USBasp**、**AVRISP mkII** 或 **Atmel-ICE**
- **Arduino IDE**（从 [arduino.cc](https://www.arduino.cc/en/software) 下载）
- **跳线**（使用 Arduino 作 ISP 时需准备）
- **USB 数据线**（用于连接编程器或 Arduino 至电脑）

---

### **方法一：使用另一块 Arduino（Arduino 作 ISP）**

此方法使用第二块 Arduino 开发板（如另一块 Uno R3）作为在线系统编程器（ISP）来烧录引导程序。

#### **操作步骤**

1. **准备编程器 Arduino**：
   - 将作为编程器的 Arduino 通过 USB 连接至电脑
   - 打开 Arduino IDE，进入 **文件 > 示例 > 11.ArduinoISP > ArduinoISP**，将此草图上传至编程器 Arduino，使其转换为 ISP 模式

2. **连接开发板**：
   - 按以下方式将编程器 Arduino 连接至目标 Arduino Uno R3（需烧录引导程序的设备）：
     - **编程器 Arduino** → **目标 Arduino Uno R3**：
       - 5V → 5V
       - GND → GND
       - 引脚 10 → Reset
       - 引脚 11 → 引脚 11 (MOSI)
       - 引脚 12 → 引脚 12 (MISO)
       - 引脚 13 → 引脚 13 (SCK)
   - 若目标 Uno R3 配备 **ICSP 接口**，可直接使用跳线连接对应 ICSP 引脚（MOSI、MISO、SCK、VCC、GND、Reset）

3. **配置 Arduino IDE**：
   - 在 Arduino IDE 中进入 **工具 > 开发板**，选择 **Arduino Uno**（对应目标 Uno R3）
   - 进入 **工具 > 编程器**，选择 **Arduino as ISP**
   - 确保在 **工具 > 端口** 中选择了编程器 Arduino 的正确端口

4. **烧录引导程序**：
   - 进入 **工具 > 烧录引导程序**
   - IDE 将使用编程器 Arduino 向目标 Uno R3 的 ATmega328P 刷写引导程序，该过程可能持续约一分钟
   - 成功后将显示“引导程序烧录完成”提示。若报错请检查连接并确认编程器 Arduino 正在运行 ArduinoISP 草图

5. **测试目标板**：
   - 断开编程器 Arduino 与跳线
   - 通过 USB 将目标 Uno R3 连接至电脑
   - 上传简单测试草图（如 **文件 > 示例 > 01.基础 > Blink**）验证引导程序是否正常工作

---

### **方法二：使用专用 ISP 编程器（如 USBasp）**

若使用 USBasp 等专用编程器，操作更简便且稳定性更高。

#### **操作步骤**

1. **连接编程器**：
   - 通过 USB 将 USBasp（或同类编程器）连接至电脑
   - 使用 6 针 ICSP 线缆将编程器连接至目标 Arduino Uno R3 的 **ICSP 接口**，注意接口方向（ICSP 接口的第 1 针通常标有圆点或凹槽）

2. **配置 Arduino IDE**：
   - 打开 Arduino IDE
   - 进入 **工具 > 开发板**，选择 **Arduino Uno**
   - 进入 **工具 > 编程器**，选择对应编程器（如 **USBasp** 或 **AVRISP mkII**）
   - 在 **工具 > 端口** 中选择正确端口（部分编程器无需选择端口）

3. **烧录引导程序**：
   - 进入 **工具 > 烧录引导程序**
   - IDE 将使用编程器刷写引导程序，过程约需 10-30 秒
   - 出现“引导程序烧录完成”提示即表示成功。若失败请检查连接并确认编程器已被电脑识别

4. **测试开发板**：
   - 断开编程器
   - 通过 USB 连接 Uno R3 至电脑，上传测试草图（如 Blink）验证功能

---

### **故障排除提示**

- **错误信息**：若出现“avrdude: stk500_getsync()”或“not in sync”等错误，请检查：
  - 所有物理连接（跳线或 ICSP 线缆）
  - 编程器 Arduino 是否正在运行 ArduinoISP 草图（方法一）
  - IDE 中是否选择了正确的编程器
- **驱动问题**：使用 USBasp 等编程器时，确保已安装对应驱动（如在 Windows 系统可使用 Zadig 工具）
- **空白微控制器**：若 ATmega328P 为新芯片或空白芯片，需在引脚 9 和 10（XTAL1/XTAL2）连接外部 16 MHz 晶振及两个 22pF 电容（Uno R3 板上未预装时）
- **供电检查**：确保目标板在编程过程中持续供电（通过 USB 或 VIN 引脚）

---

### **补充说明**

- **为何需要烧录引导程序**：引导程序使 Arduino Uno R3 能通过 USB 与 Arduino IDE 通信以上传草图。缺少引导程序则开发板无法响应 USB 上传指令
- **引导程序类型**：Uno R3 使用 **Optiboot 引导程序**，该程序体积紧凑且相比旧版引导程序支持更快速的上传
- **更换微控制器**：若需更换 ATmega328P，请确认使用 ATmega328P-PU（DIP 封装）以匹配 Uno R3 的插座。SMD 版本需进行高阶焊接操作
- **替代工具**：也可使用 **AVRDUDE** 或 **PlatformIO** 烧录引导程序，但 Arduino IDE 对初学者最为友好

若需任何步骤的详细说明或特定编程器的协助，请随时告知！
