---
audio: false
generated: true
lang: zh
layout: post
title: Arduino问题
translated: true
type: note
---

您遇到的错误信息表明 Arduino IDE（通过 `avrdude`）无法与您的 Arduino 板通信以上传草图。`stk500_recv(): programmer is not responding` 和 `stk500_getsync(): not in sync: resp=0x00` 错误通常指向计算机与 Arduino 之间的通信问题。由于您使用的是 `/dev/ttyUSB0`（如您之前的查询所示），这表明是 USB 转串口连接，很可能是 Arduino Uno 或带有独立 USB 转串口芯片（例如 CH340、FT232R）的兼容板。

以下是逐步排查和解决问题的指南，以及上传成功后如何验证和监视日志。

### 理解错误

- **草图大小**：草图使用 2678 字节（占 32,256 字节的 8%）和 314 字节 RAM（占 2048 字节的 15%），这在 Arduino 的限制范围内，因此代码本身不是问题。
- **错误原因**：`stk500` 错误意味着 `avrdude`（用于上传草图的工具）无法与 Arduino 的引导加载程序建立连接。这可能是由于：
  - 端口或开发板设置不正确。
  - 物理连接问题（线缆、USB 端口或开发板）。
  - `/dev/ttyUSB0` 的权限问题。
  - USB 转串口芯片的驱动程序问题。
  - 引导加载程序或开发板故障。

### 故障排除步骤

按照以下步骤解决问题：

1. **验证开发板和端口设置**
   - 在 Arduino IDE 中：
     - 转到 `工具 > 开发板`，确保选择了正确的开发板（例如，对于 Uno 或兼容板，选择 "Arduino Uno"）。
     - 转到 `工具 > 端口`，确认选择了 `/dev/ttyUSB0`。如果未列出，则可能未检测到 Arduino。
   - 在终端中运行 `ls /dev/ttyUSB*` 以确认端口存在。如果端口缺失，则系统未检测到 Arduino。
   - 如果出现多个端口（例如 `/dev/ttyUSB1`），请尝试每一个。

2. **检查 `/dev/ttyUSB0` 的权限**
   - 您之前 `ls -alrt /dev/ttyUSB0` 的输出显示 `crw-rw---- 1 root dialout`，意味着只有 `root` 和 `dialout` 组可以访问该端口。
   - 确保您的用户在 `dialout` 组中：

     ```bash
     groups
     ```

     如果未列出 `dialout`，请添加您的用户：

     ```bash
     sudo usermod -a -G dialout $USER
     ```

     注销并重新登录（或重启）以使更改生效。
   - 或者，以 root 身份运行 Arduino IDE（不推荐长期使用）：

     ```bash
     sudo arduino
     ```

   - 如果权限正确但问题仍然存在，请继续下一步。

3. **检查物理连接**
   - **USB 线缆**：确保您使用的是**数据 USB 线缆**，而不是仅充电线缆。一些廉价线缆不支持数据传输。
   - **USB 端口**：尝试计算机上的其他 USB 端口或其他计算机。
   - **Arduino 开发板**：检查生命迹象（例如，电源 LED 亮起，或如果之前的草图正在运行，则 LED 闪烁）。如果开发板无响应，则可能已损坏或未通电。
   - **重置开发板**：在上传时短暂按下 Arduino 上的重置按钮。这会强制引导加载程序重新启动，有助于与 `avrdude` 同步。

4. **检查 USB 转串口驱动程序**
   - 由于您在 Linux 上并使用 `/dev/ttyUSB0`，您的开发板可能使用 USB 转串口芯片，如 CH340/CH341、FT232R 或 ATmega16U2。
   - 验证驱动程序是否已安装：

     ```bash
     lsmod | grep usbserial
     ```

     您应该看到类似 `ch341`、`ftdi_sio` 或类似的模块。
   - 如果未检测到端口，请安装常见芯片的驱动程序：

     ```bash
     sudo apt-get install linux-modules-extra-$(uname -r)
     ```

   - 对于 CH340/CH341 芯片，您可能需要特定的驱动程序。检查设备是否被识别：

     ```bash
     dmesg | grep usb
     ```

     查找提及 `ch341`、`ftdi` 或 USB 设备的行。如果未出现任何内容，则芯片可能不受支持，或者开发板/线缆有故障。

5. **强制进入引导加载程序模式**
   - 一些 Arduino 开发板在快速按下重置按钮两次时会进入引导加载程序模式。尝试此操作：
     1. 按下重置按钮两次（您可能会看到板载 LED 快速闪烁）。
     2. 立即在 Arduino IDE 中开始上传。
   - 这确保引导加载程序在上传尝试期间处于活动状态。

6. **使用最简草图测试**
   - 为了排除先前草图的问题，尝试上传一个最简草图：

     ```cpp
     void setup() {
       Serial.begin(9600);
       pinMode(LED_BUILTIN, OUTPUT);
     }
     void loop() {
       Serial.println("Test");
       digitalWrite(LED_BUILTIN, HIGH);
       delay(1000);
       digitalWrite(LED_BUILTIN, LOW);
       delay(1000);
     }
     ```

   - 如果此草图上传成功，则问题可能与先前的草图有关（鉴于其大小正常，可能性不大）。

7. **检查硬件问题**
   - 如果上述步骤均失败，则 Arduino 的引导加载程序或 USB 转串口芯片可能已损坏，或者开发板可能已损坏。
   - 如果可用，请使用另一个 Arduino 开发板进行测试。
   - 如果您怀疑是引导加载程序问题，则可能需要使用 ISP 编程器或将另一个 Arduino 作为 ISP 重新刷新引导加载程序。

### 上传成功后查看日志

解决上传问题并上传修改后的 Fibonacci 草图（来自先前的回复）后，您可以查看日志：

1. **Arduino IDE 串口监视器**：
   - 上传后，转到 `工具 > 串口监视器` 或按 `Ctrl+Shift+M`。
   - 将波特率设置为 **9600**（与代码中的 `Serial.begin(9600)` 匹配）。
   - 您应该看到类似以下的输出：

     ```
     Starting Fibonacci LED Blink...
     Index: 0, Delay: 0s, Direction: Forward
     Index: 1, Delay: 1s, Direction: Forward
     ...
     ```

2. **终端程序（minicom 或 screen）**：
   - 使用 `minicom`：

     ```bash
     minicom -D /dev/ttyUSB0 -b 9600
     ```

     按 `Ctrl+A`，然后按 `X` 退出。
   - 或使用 `screen`：

     ```bash
     screen /dev/ttyUSB0 9600
     ```

     按 `Ctrl+A`，然后按 `\` 退出。
   - 确保您的用户在 `dialout` 组中以避免权限问题。

3. **验证端口**：
   - 如果 `/dev/ttyUSB0` 不起作用，请检查 `dmesg` 以找到正确的端口：

     ```bash
     dmesg | grep tty
     ```

     查找类似 `[1234.567890] usb 1-1: ch341-uart converter now attached to ttyUSB0` 的行。

### 日志输出示例

如果上传成功，您将看到类似以下的日志：

```
Starting Fibonacci LED Blink...
Index: 0, Delay: 0s, Direction: Forward
Index: 1, Delay: 1s, Direction: Forward
Index: 2, Delay: 1s, Direction: Forward
Index: 3, Delay: 2s, Direction: Forward
...
Switching to Backward
Index: 7, Delay: 13s, Direction: Backward
...
```

### 额外提示

- **详细上传输出**：在 Arduino IDE 中，转到 `文件 > 首选项`，勾选“在上传过程中显示详细输出”，然后再次尝试上传。这可能会提供有关失败的更多线索。
- **开发板克隆或非标准芯片**：如果您使用的是非官方 Arduino（例如带有 CH340 芯片的开发板），请确保驱动程序已安装且开发板类型匹配（例如，在某些情况下，即使对于克隆板，也选择 "Arduino Uno"）。
- **重置时序**：如果开发板有自动重置问题，请在 IDE 状态栏显示“正在上传...”时手动按下重置按钮。

### 如果问题仍然存在

如果这些步骤均无效，请提供：

- 确切的 Arduino 开发板型号（例如 Uno、Mega 或克隆板）。
- 插入 Arduino 后 `dmesg | grep usb` 的输出。
- 开发板的电源 LED 或其他 LED 是否亮起。
- 尝试不同 USB 线缆或计算机的结果。

这将有助于缩小问题是硬件、驱动程序还是配置问题。现在，请从检查端口、权限和线缆开始，因为这些是最常见的原因。

---

根据您提供的日志，您似乎在使用 Arduino IDE 在 Linux 上调试和上传草图到 Arduino 开发板时遇到了问题。以下是逐步排查和解决这些问题的指南：

---

### **1. 解决调试错误**

- **问题**：日志中反复显示 `arduino:avr:uno` 开发板“不支持调试”。
- **解释**：Arduino Uno 在 Arduino IDE 中不支持调试功能。调试仅在特定开发板上可用，例如 Arduino Zero 或 MKR 系列。
- **解决方案**：
  - 如果您尝试调试草图，需要切换到支持调试的开发板（例如 Arduino Zero 或 MKR 系列）。
  - 如果您并非有意调试，只是想上传草图，此错误不会阻止上传。您可以忽略它，专注于下面的上传问题。确保您没有意外点击 IDE 中的“开始调试”选项。

---

### **2. 解决上传端口检测问题**

- **问题**：日志显示“上传端口检测失败”和“用户中止”错误，表明 IDE 无法可靠检测或访问串行端口 (`/dev/ttyUSB0`)。
- **解释**：这可能是由于权限问题、设置不正确或物理连接问题，这在 Linux 系统上很常见。
- **解决方案**：

#### **检查 `/dev/ttyUSB0` 的权限**

- 在 Linux 上，Arduino IDE 需要权限访问串行端口，这些端口通常由 `dialout` 组所有。
- **步骤**：
  1. 检查您的用户是否在 `dialout` 组中：

     ```bash
     groups
     ```

     在输出中查找 `dialout`。
  2. 如果未列出，将您的用户添加到该组：

     ```bash
     sudo usermod -a -G dialout $USER
     ```

  3. 注销并重新登录（或重启）以使更改生效。
  4. 重新连接 Arduino，并检查 `/dev/ttyUSB0` 是否出现在 IDE 的 `工具 > 端口` 下。

#### **验证开发板和端口设置**

- 确保 IDE 配置正确：
  - 转到 `工具 > 开发板`，选择 **Arduino Uno**（如果您使用其他开发板，请选择正确的开发板）。
  - 转到 `工具 > 端口`，选择 **/dev/ttyUSB0**。如果未列出，请继续下一步。

#### **检查物理连接**

- **步骤**：
  1. 确认 Arduino 通过**数据 USB 线缆**连接（不是仅充电线缆）。一些线缆仅提供电源，无法用于上传。
  2. 尝试计算机上的其他 USB 端口或不同线缆，以排除硬件问题。
  3. 确保 Arduino 已通电（电源 LED 应亮起）。
  4. 运行以下命令检查端口是否被检测到：

     ```bash
     ls /dev/ttyUSB*
     ```

     如果 `/dev/ttyUSB0` 未出现，则系统未识别开发板（请参阅下面的“检查驱动程序问题”）。

---

### **3. 排查上传失败问题**

- **问题**：“用户中止”消息表明上传过程被中断或无法与开发板同步。
- **解决方案**：

#### **上传期间手动重置**

- 有时 Arduino 的引导加载程序需要手动重置以与 IDE 同步。
- **步骤**：
  1. 在 IDE 中，点击**上传**按钮（右箭头图标）。
  2. 当“正在编译草图...”消息变为“正在上传...”时，按下并释放 Arduino 上的**重置按钮**。
  3. 这确保开发板准备好接收草图。

#### **检查驱动程序问题**

- 如果未检测到 `/dev/ttyUSB0`，可能存在驱动程序问题，特别是对于使用 CH340/CH341 等芯片而非标准 FTDI 或 ATmega16U2 的克隆板。
- **步骤**：
  1. 插入 Arduino 后，运行：

     ```bash
     dmesg | grep usb
     ```

     查找提及 `ch341`、`ftdi` 或类似 USB 转串口驱动程序的代码行。
  2. 如果未出现任何内容，或出现错误，您可能需要安装驱动程序：
     - 对于 CH340/CH341 芯片（克隆板常见）：

       ```bash
       sudo apt-get install linux-modules-extra-$(uname -r)
       ```

     - 重新插入 Arduino，并使用 `ls /dev/ttyUSB*` 再次检查。
  3. 如果仍未检测到端口，则您的开发板或线缆可能有故障。

#### **尝试最简草图**

- 使用简单草图测试以隔离问题：
  - 打开 IDE，转到 `文件 > 示例 > 01.Basics > Blink`。
  - 上传此草图。如果成功，问题可能出在您的原始草图上。

---

### **4. 额外故障排除提示**

- **启用详细输出**：
  - 在 IDE 中转到 `文件 > 首选项`，勾选**在上传过程中显示详细输出**。
  - 这在上传尝试时提供更详细的错误消息，有助于定位问题。
- **监视串行输出**：
  - 上传成功后，使用串口监视器（`工具 > 串口监视器`）检查草图的输出（例如 `Serial.println` 语句）。
  - 或者，使用终端程序：

    ```bash
    minicom -D /dev/ttyUSB0 -b 9600
    ```

    将波特率（例如 9600）与您草图 `Serial.begin()` 中的波特率匹配。

---

### **修复总结**

- **调试**：Arduino Uno 不支持调试。如需调试，请使用支持的开发板；对于上传，可忽略此错误。
- **权限**：将您的用户添加到 `dialout` 组以访问 `/dev/ttyUSB0`。
- **端口检测**：确保 `/dev/ttyUSB0` 在 `工具 > 端口` 下列出，且开发板已物理连接。
- **上传同步**：在上传期间按下重置按钮以帮助引导加载程序同步。

如果您按照这些步骤操作后仍然遇到问题，请尝试不同的 Arduino 开发板或线缆，或在 Arduino 论坛上寻求帮助，并提供您的设置详情（例如开发板类型、Linux 发行版和确切错误）。请告诉我进展如何！
