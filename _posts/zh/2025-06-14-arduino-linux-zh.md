---
audio: false
generated: true
lang: zh
layout: post
title: 在Ubuntu系统上安装Arduino IDE
translated: true
type: note
---

在 Ubuntu Linux 系统上安装 Arduino IDE，请按照以下步骤操作：

1. **下载 Arduino IDE**：
   - 访问 Arduino 官方网站 [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software)。
   - 在 "Arduino IDE" 部分，选择 "Linux 64 位" 下载选项（或适合您系统的版本，例如树莓派选择 Linux ARM 版本）。

2. **解压下载的文件**：
   - 下载的文件是压缩格式 `.tar.xz`（例如 `arduino-1.8.19-linux64.tar.xz`）。
   - 打开终端并进入下载目录（例如 `cd ~/Downloads`）。
   - 使用以下命令解压文件：

     ```bash
     tar -xf arduino-*.tar.xz
     ```

   - 这将创建一个类似 `arduino-1.8.19` 的文件夹。

3. **移动到合适目录（可选）**：
   - 如需系统级访问，可将解压的文件夹移至 `/opt`（需要超级用户权限）：

     ```bash
     sudo mv arduino-1.8.19 /opt/arduino
     ```

4. **运行安装脚本**：
   - 进入 Arduino 文件夹：

     ```bash
     cd /opt/arduino
     ```

   - 运行安装脚本：

     ```bash
     sudo ./install.sh
     ```

   - 这将创建桌面快捷方式并设置必要的权限。

5. **将用户加入 dialout 组**：
   - 为通过串口访问 Arduino 板，需将用户加入 `dialout` 组：

     ```bash
     sudo usermod -a -G dialout $USER
     ```

   - 注销后重新登录，或重启系统使组变更生效。

6. **启动 Arduino IDE**：
   - 若已运行 `install.sh` 脚本，可通过应用程序菜单或搜索 "Arduino IDE" 启动。
   - 也可直接从终端运行：

     ```bash
     /opt/arduino/arduino
     ```

7. **更新 Arduino 板权限（如需要）**：
   - 连接 Arduino 时确保系统识别（如 `/dev/ttyACM0` 或 `/dev/ttyUSB0`）。
   - 若遇权限问题，设置正确权限：

     ```bash
     sudo chmod a+rw /dev/ttyACM0
     ```

   - 将 `/dev/ttyACM0` 替换为实际端口。

8. **验证安装**：
   - 通过 USB 连接 Arduino 板。
   - 打开 IDE，进入 **工具 > 开发板** 选择 Arduino 型号（如 Arduino Uno）。
   - 进入 **工具 > 端口** 选择端口（如 `/dev/ttyACM0`）。
   - 尝试上传示例程序（如 **文件 > 示例 > 01.Basics > Blink**）确认功能正常。

**替代方案：通过 Snap 或 Flatpak 安装**：

- **Snap**：

  ```bash
  sudo snap install arduino
  ```

- **Flatpak**：

  ```bash
  sudo flatpak install flathub cc.arduino.ArduinoIDE
  ```

- 这些方法简化安装，但可能在权限或板卡识别方面存在限制。

**注意事项**：

- 确保已安装 Java（Arduino IDE 依赖 Java环境）：

  ```bash
  sudo apt update
  sudo apt install default-jre
  ```

- 需要最新版本或故障排除时，请查阅 Arduino 论坛或[官方文档](https://www.arduino.cc/en/Guide/Linux)。

若遇问题，请告知您的 Ubuntu 版本或具体错误信息以便针对性协助！

---

既然您的 Arduino Uno 已在 Ubuntu 系统的 Arduino IDE 中识别，且您希望使用无需面包板或外部元件的简单示例，这里提供一个使 Arduino Uno 板上 LED（连接至数字引脚 13）闪烁的基础程序。此示例无需额外硬件。

```cpp
void setup() {
  // 初始化设置代码，仅运行一次：
  pinMode(LED_BUILTIN, OUTPUT); // 将板上 LED 引脚（引脚13）设置为输出模式
}

void loop() {
  // 主循环代码，重复运行：
  digitalWrite(LED_BUILTIN, HIGH); // 点亮 LED
  delay(1000);                     // 等待 1 秒
  digitalWrite(LED_BUILTIN, LOW);  // 熄灭 LED
  delay(1000);                     // 等待 1 秒
}
```

### 运行方法

1. 打开 Arduino IDE。
2. 将以上代码复制粘贴到 IDE 中。
3. 确保 Arduino Uno 已通过 USB 连接并被识别：
   - 进入 **工具 > 开发板** 选择 **Arduino Uno**。
   - 进入 **工具 > 端口** 选择对应端口（如 `/dev/ttyACM0` 或 `/dev/ttyUSB0`）。
4. 点击 **上传** 按钮（右箭头图标）编译程序并上传至 Arduino Uno。
5. 上传完成后，板上 LED（标有 "L" 的指示灯）将以 1 秒间隔持续闪烁。

### 程序功能

- 在 `setup()` 中，`pinMode` 函数配置板上 LED 引脚为输出模式。
- 在 `loop()` 中，`digitalWrite` 函数控制 LED 亮（`HIGH`）灭（`LOW`），`delay` 函数在状态切换间实现 1 秒延时，形成闪烁效果。

### 注意事项

- Arduino Uno 在引脚 13 集成 LED，无需外接元件。
- 若 LED 未闪烁，请检查端口选择或板卡连接。可添加串口调试功能：在 `setup()` 中加入 `Serial.begin(9600);`，在 `loop()` 中加入 `Serial.println("Blink");` 后打开 **串口监视器**（工具 > 串口监视器）查看输出。
- 如需调整闪烁速度，修改 `delay(1000)` 参数（如 `delay(500)` 可加快闪烁）。

若遇到问题或需要其他简单示例，请随时告知！

---

错误信息表明在 Ubuntu 系统上传程序到 Arduino Uno 时出现权限问题。Arduino IDE 因权限不足无法访问串口 `/dev/ttyUSB0`。以下是解决方案：

### 解决方案：修复串口权限

1. **将用户加入 `dialout` 组**：
   - Ubuntu 中 `dialout` 组通常控制串口访问权限。将用户加入该组：

     ```bash
     sudo usermod -a -G dialout $USER
     ```

   - 执行后需注销重新登录，或重启系统使变更生效：

     ```bash
     sudo reboot
     ```

2. **验证端口**：
   - 重启后重新连接 Arduino Uno 并打开 Arduino IDE。
   - 进入 **工具 > 端口** 确保已选择 `/dev/ttyUSB0`（部分 Arduino 板可能为 `/dev/ttyACM0`）。若未显示端口，请检查 USB 连接或更换数据线/接口。

3. **临时修改端口权限（可选）**：
   - 若加入用户组后问题仍存，可手动设置端口权限（此为临时方案，重启后权限重置）：

     ```bash
     sudo chmod a+rw /dev/ttyUSB0
     ```

   - 如端口不同请替换 `/dev/ttyUSB0`（例如 `/dev/ttyACM0`）。

4. **重新尝试上传**：
   - 在 Arduino IDE 中点击 **上传** 按钮上传程序（如之前的 LED 闪烁程序）。
   - 若上传成功，Arduino Uno 板上 LED 应开始闪烁。

### 额外故障排除

- **检查 Arduino 板与数据线**：
  - 确保 Arduino Uno 通过 USB 正确连接且被 Ubuntu 识别。运行以下命令查看连接设备：

    ```bash
    ls /dev/tty*
    ```

    连接板卡时查找 `/dev/ttyUSB0` 或 `/dev/ttyACM0`。
  - 若板卡未识别，尝试更换 USB 数据线或接口。

- **确认开发板与端口设置**：
  - 在 Arduino IDE 中确认 **工具 > 开发板** 设置为 **Arduino Uno**。
  - 若未显示 `/dev/ttyUSB0`，可尝试重新插拔板卡后查看 **工具 > 端口**。

- **以 Root 权限运行 Arduino IDE（临时方案）**：
  - 若上述步骤无效，可使用超级用户权限运行 IDE 绕过权限问题（不建议长期使用）：

    ```bash
    sudo arduino
    ```

    若 IDE 执行文件未在系统 PATH 中，请替换 `arduino` 为实际路径（如 `/opt/arduino/arduino`）。

- **检查冲突软件**：
  - 其他软件（如盲文显示器驱动 `brltty`）可能干扰串口。若已安装可移除：

    ```bash
    sudo apt remove brltty
    ```

- **驱动问题**：
  - 部分 Arduino 兼容板使用 CH340/CH341 芯片需安装驱动：

    ```bash
    sudo apt install linux-modules-extra-$(uname -r)
    ```

    随后重新连接板卡。

### 确认修复

权限问题解决后，重新尝试上传闪烁程序：

```cpp
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}
```

若问题依旧存在，请提供新错误信息或在终端运行 `ls -l /dev/ttyUSB0` 并提供输出以便进一步诊断。

---

检测到您在 Ubuntu 系统使用 Arduino IDE 向 Arduino Uno 上传程序时遇到问题。您提供的错误信息为：

```
avrdude: ser_open(): can't open device "/dev/ttyUSB0": Permission denied
Failed uploading: uploading error: exit status 1
```

该错误表明 Arduino IDE 缺乏访问 Arduino Uno 所连接串口（`/dev/ttyUSB0`）的必要权限。这是 Linux 系统（如 Ubuntu）因串口访问管理机制导致的常见问题。以下为逐步解决指南。

---

### 解决方案：修复串口权限问题

#### 1. 将用户加入 `dialout` 组

Ubuntu 中 `dialout` 组控制串口访问权限。需将用户加入该组以解决权限问题。

- 按 `Ctrl + Alt + T` 打开终端。
- 运行以下命令：

  ```bash
  sudo usermod -a -G dialout $USER
  ```

- 此命令将当前用户加入 `dialout` 组。`$USER` 变量自动获取当前用户名。

#### 2. 注销后重新登录

为使组变更生效，需注销当前会话后重新登录。亦可重启系统。

- **注销后重新登录**：
  - 保存所有正在进行的工作。
  - 点击 Ubuntu 桌面右上角用户名，选择"注销"。
  - 使用用户名和密码重新登录。
- **重启系统（可选）**：
  - 在终端运行：

    ```bash
    sudo reboot
    ```

  - 等待系统重启完成。

#### 3. 验证串口

重新登录后，确保系统正确识别 Arduino Uno。

- 重新将 Arduino Uno 连接至 USB 接口。
- 打开 Arduino IDE。
- 进入菜单 **工具 > 端口**，检查是否列出并选中 `/dev/ttyUSB0`（部分 Arduino 板可能显示 `/dev/ttyACM0`）。
- 若未显示端口：
  - 重新插拔 Arduino Uno。
  - 检查 USB 连接或更换数据线/接口。

#### 4. 重新上传程序

选择正确端口后，重新尝试上传程序：

```cpp
void setup() {
  pinMode(LED_BUILTIN, OUTPUT); // 设置板上 LED 引脚（引脚13）为输出模式
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH); // 点亮 LED
  delay(1000);                     // 等待 1 秒
  digitalWrite(LED_BUILTIN, LOW);  // 熄灭 LED
  delay(1000);                     // 等待 1 秒
}
```

- 点击 Arduino IDE 中的 **上传** 按钮（右箭头图标）。
- 若成功，Arduino Uno 板上 LED 应开始闪烁（亮 1 秒、灭 1 秒）。

---

### 额外故障排除

若上述步骤未解决问题，请尝试以下补充检查：

#### 检查组成员身份

验证用户是否已加入 `dialout` 组：

- 在终端运行：

  ```bash
  groups $USER
  ```

- 在输出中查找 `dialout`。若未找到，请重复步骤 1 并确保注销/重新登录或重启。

#### 临时权限修复（不建议长期使用）

如需快速解决，可手动修改串口权限：

- 运行：

  ```bash
  sudo chmod a+rw /dev/ttyUSB0
  ```

- 然后重新尝试上传。注意：此方案为临时性，拔插 Arduino 或重启后权限将重置。

#### 检查冲突软件

部分软件（如盲文显示器驱动 `brltty`）可能干扰串口。可移除该软件：

- 运行：

  ```bash
  sudo apt remove brltty
  ```

- 重新连接 Arduino 后再次尝试。

#### 验证 Arduino 连接

确保 Ubuntu 识别您的 Arduino：

- 运行：

  ```bash
  ls /dev/tty*
  ```

- 连接 Arduino 时查找 `/dev/ttyUSB0` 或 `/dev/ttyACM0`。若未显示，请检查 USB 数据线或接口。

#### 以 Root 权限运行 Arduino IDE（临时方案）

作为最后手段，可使用超级用户权限运行 IDE：

- 关闭 Arduino IDE。
- 打开终端并运行：

  ```bash
  sudo arduino-ide
  ```

- 若需指定路径请替换 `arduino-ide`（例如 `/home/lzw/arduino-ide_2.3.6_Linux_64bit/arduino-ide`）。
- 重新尝试上传。请避免常规使用此方法，因其存在安全隐患。

---

### 确认修复

完成这些步骤后，您的程序应能成功上传，Arduino Uno 板上 LED 将按预期闪烁。若问题仍然存在，请提供以下补充信息：

- `ls -l /dev/ttyUSB0` 的输出（用于检查权限）。
- Arduino IDE 的任何新错误信息。

若需进一步协助，请随时告知！
