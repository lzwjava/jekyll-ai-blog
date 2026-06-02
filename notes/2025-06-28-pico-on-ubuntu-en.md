---
audio: false
generated: true
lang: en
layout: post
title: Setting Up Raspberry Pi Pico on Ubuntu
translated: false
type: note
---

To use a **Raspberry Pi Pico** on **Ubuntu**, you need to set up the development environment, install necessary software, and configure tools to program the Pico. The Pico supports programming in **MicroPython**, **C/C++**, or **CircuitPython**. Below, I outline the steps and software required for each approach, focusing on the most common setups.

### General Prerequisites

- **Raspberry Pi Pico** (or Pico W) with a USB cable (Micro-USB for Pico, USB-C for Pico 2).
- **Ubuntu** system (e.g., Ubuntu 20.04, 22.04, or later; these instructions assume a recent version like 24.04).
- Basic familiarity with the terminal.

### Option 1: Programming with MicroPython

MicroPython is the most beginner-friendly way to program the Pico. It’s a lightweight Python implementation designed for microcontrollers.

#### Software to Install

1. **MicroPython Firmware**
   - Download the latest MicroPython UF2 firmware file for the Raspberry Pi Pico from the [official MicroPython website](https://micropython.org/download/rp2-pico/) or the [Raspberry Pi Pico page](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).
   - For Pico W or Pico 2, ensure you select the appropriate firmware (e.g., `rp2-pico-w` for Pico W).

2. **Python 3**
   - Ubuntu typically includes Python 3 by default. Verify with:

     ```bash
     python3 --version
     ```

   - If not installed, install it:

     ```bash
     sudo apt update
     sudo apt install python3 python3-pip
     ```

3. **Thonny IDE** (Recommended for Beginners)
   - Thonny is a simple IDE for programming the Pico with MicroPython.
   - Install Thonny:

     ```bash
     sudo apt install thonny
     ```

   - Alternatively, use `pip` for the latest version:

     ```bash
     pip3 install thonny
     ```

4. **Optional: `picotool` (for advanced management)**
   - Useful for managing MicroPython firmware or inspecting the Pico.
   - Install `picotool`:

     ```bash
     sudo apt install picotool
     ```

#### Setup Steps

1. **Install MicroPython Firmware**
   - Connect the Pico to your Ubuntu machine via USB while holding the **BOOTSEL** button (this puts the Pico in bootloader mode).
   - The Pico appears as a USB storage device (e.g., `RPI-RP2`).
   - Drag and drop the downloaded MicroPython `.uf2` file onto the Pico’s storage. The Pico will reboot automatically with MicroPython installed.

2. **Configure Thonny**
   - Open Thonny: `thonny` in the terminal or via the application menu.
   - Go to **Tools > Options > Interpreter**.
   - Select **MicroPython (Raspberry Pi Pico)** as the interpreter.
   - Choose the correct port (e.g., `/dev/ttyACM0`). Run `ls /dev/tty*` in the terminal to identify the port if needed.
   - Thonny should now connect to the Pico, allowing you to write and run Python scripts.

3. **Test a Program**
   - In Thonny, write a simple script, e.g.:

     ```python
     from machine import Pin
     led = Pin(25, Pin.OUT)  # Onboard LED (GP25 for Pico)
     led.toggle()  # Toggle LED on/off
     ```

   - Click the **Run** button to execute the code on the Pico.

4. **Optional: Use `picotool`**
   - Verify the Pico’s status:

     ```bash
     picotool info
     ```

   - Ensure the Pico is connected and in bootloader mode if needed.

### Option 2: Programming with C/C++

For more advanced users, the Pico can be programmed in C/C++ using the official **Pico SDK**.

#### Software to Install

1. **Pico SDK and Toolchain**
   - Install the required tools for building C/C++ programs:

     ```bash
     sudo apt update
     sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential git
     ```

2. **Pico SDK**
   - Clone the Pico SDK repository:

     ```bash
     git clone -b master https://github.com/raspberrypi/pico-sdk.git
     cd pico-sdk
     git submodule update --init
     ```

   - Set the `PICO_SDK_PATH` environment variable:

     ```bash
     export PICO_SDK_PATH=~/pico-sdk
     echo 'export PICO_SDK_PATH=~/pico-sdk' >> ~/.bashrc
     ```

3. **Optional: Pico Examples**
   - Clone the Pico examples for reference:

     ```bash
     git clone -b master https://github.com/raspberrypi/pico-examples.git
     ```

4. **Visual Studio Code (Optional)**
   - For a better development experience, install VS Code:

     ```bash
     sudo snap install code --classic
     ```

   - Install the **CMake Tools** and **C/C++** extensions in VS Code.

#### Setup Steps

1. **Set Up a Project**
   - Create a new directory for your project, e.g., `my-pico-project`.
   - Copy a sample `CMakeLists.txt` from `pico-examples` or create one:

     ```cmake
     cmake_minimum_required(VERSION 3.13)
     include($ENV{PICO_SDK_PATH}/pico_sdk_init.cmake)
     project(my_project C CXX ASM)
     pico_sdk_init()
     add_executable(my_project main.c)
     pico_add_extra_outputs(my_project)
     target_link_libraries(my_project pico_stdlib)
     ```

   - Write a simple C program (e.g., `main.c`):

     ```c
     #include "pico/stdlib.h"
     int main() {
         const uint LED_PIN = 25;
         gpio_init(LED_PIN);
         gpio_set_dir(LED_PIN, GPIO_OUT);
         while (true) {
             gpio_put(LED_PIN, 1);
             sleep_ms(500);
             gpio_put(LED_PIN, 0);
             sleep_ms(500);
         }
     }
     ```

2. **Build and Flash**
   - Navigate to your project directory:

     ```bash
     cd my-pico-project
     mkdir build && cd build
     cmake ..
     make
     ```

   - This generates a `.uf2` file (e.g., `my_project.uf2`).
   - Hold the **BOOTSEL** button on the Pico, connect it via USB, and copy the `.uf2` file to the Pico’s storage:

     ```bash
     cp my_project.uf2 /media/$USER/RPI-RP2/
     ```

3. **Debugging (Optional)**
   - Install `openocd` for debugging:

     ```bash
     sudo apt install openocd
     ```

   - Use a debugger (e.g., another Pico as a debug probe) and run:

     ```bash
     openocd -f interface/raspberrypi-swd.cfg -f target/rp2040.cfg
     ```

### Option 3: Programming with CircuitPython

CircuitPython is another Python-based option, similar to MicroPython but with a focus on Adafruit’s ecosystem.

#### Software to Install

1. **CircuitPython Firmware**
   - Download the CircuitPython UF2 file for the Pico from the [Adafruit CircuitPython website](https://circuitpython.org/board/raspberry_pi_pico/).
   - For Pico W or Pico 2, select the appropriate firmware.

2. **Python 3 and Tools**
   - Same as for MicroPython (Python 3, Thonny, etc.).

#### Setup Steps

1. **Install CircuitPython Firmware**
   - Similar to MicroPython: hold **BOOTSEL**, connect the Pico, and copy the CircuitPython `.uf2` file to the Pico’s storage.
   - The Pico reboots as a USB drive named `CIRCUITPY`.

2. **Program with Thonny or a Text Editor**
   - Use Thonny as described in the MicroPython section, selecting **CircuitPython** as the interpreter.
   - Alternatively, edit `code.py` directly on the `CIRCUITPY` drive using any text editor.
   - Example `code.py`:

     ```python
     import board
     import digitalio
     import time
     led = digitalio.DigitalInOut(board.LED)
     led.direction = digitalio.Direction.OUTPUT
     while True:
         led.value = True
         time.sleep(0.5)
         led.value = False
         time.sleep(0.5)
     ```

### Additional Notes

- **Permissions**: If the Pico’s port (e.g., `/dev/ttyACM0`) isn’t accessible, add your user to the `dialout` group:

  ```bash
  sudo usermod -a -G dialout $USER
  ```

  Log out and back in to apply.

- **Pico W Considerations**: For the Pico W, ensure you use firmware specific to it (e.g., MicroPython with Wi-Fi support). Wi-Fi programming requires additional libraries, like `network` for MicroPython.

- **Pico 2**: The newer Raspberry Pi Pico 2 (with RP2350) may require updated firmware or SDK versions. Check the official Raspberry Pi documentation for compatibility.

- **Troubleshooting**:
  - If the Pico doesn’t appear in bootloader mode, double-check the USB cable (it must support data, not just power).
  - Run `lsusb` or `dmesg` to confirm the Pico is detected by Ubuntu.
  - For C/C++ builds, ensure the Pico SDK path is correctly set.

### Recommended Approach

- For **beginners**: Use **MicroPython with Thonny** for simplicity and quick setup.
- For **advanced users**: Use **C/C++ with the Pico SDK** for performance and low-level control.
- For **Adafruit ecosystem users**: Use **CircuitPython** if you plan to use Adafruit libraries or hardware.

If you have a specific project or programming preference, let me know, and I can tailor the instructions further!
