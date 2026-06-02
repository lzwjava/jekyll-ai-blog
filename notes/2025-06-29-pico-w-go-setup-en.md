---
audio: false
generated: true
lang: en
layout: post
title: VSCode Pico-W-Go for MicroPython
translated: false
type: note
---

Using the **Raspberry Pi Pico** extension in Visual Studio Code (VSCode) is an excellent choice for MicroPython development on your Raspberry Pi Pico, as it provides a streamlined workflow similar to Thonny but within VSCode’s powerful editing environment. The extension you’re likely referring to is **Pico-W-Go** (or a similar extension like **Pico-Go**), which is specifically designed for Raspberry Pi Pico and Pico W development with MicroPython. Below, I’ll guide you through setting up and using the **Pico-W-Go** extension (the most popular and maintained option) to upload a simple MicroPython program to your Pico, assuming MicroPython is already flashed (from the `RPI_PICO-20250415-v1.25.0.uf2` file you used).

---

### Prerequisites
1. **MicroPython Flashed**: Your Pico has MicroPython installed, as you’ve already flashed it.
2. **VSCode Installed**: Ensure VSCode is installed ([code.visualstudio.com](https://code.visualstudio.com)).
3. **Python Installed**: Required for Pico-W-Go dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
4. **USB Connection**: The Pico is connected via a data-capable USB cable.

---

### Step-by-Step Guide to Using the Raspberry Pi Pico (Pico-W-Go) Extension in VSCode

1. **Install the Pico-W-Go Extension**:
   - Open VSCode.
   - Go to the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X` on macOS).
   - Search for **Pico-W-Go** and install it (developed by Paul Obermeier and others).
   - Note: If you meant a different extension (e.g., Pico-Go), let me know, but Pico-W-Go is the most commonly used for Pico MicroPython development.

2. **Install Pico-W-Go Dependencies**:
   - Pico-W-Go requires `pyserial` and `esptool` for serial communication and flashing:
     ```bash
     pip3 install pyserial esptool
     ```
   - Ensure these are installed in your Python environment (use `pip3 list` to verify).

3. **Configure Pico-W-Go**:
   - Open the Command Palette in VSCode (`Ctrl+Shift+P` or `Cmd+Shift+P`).
   - Type and select **Pico-W-Go > Configure Project**.
   - Follow the prompts:
     - **Serial Port**: Select the Pico’s port (e.g., `/dev/ttyACM0`). Find it by running:
       ```bash
       ls /dev/tty*
       ```
       Look for `/dev/ttyACM0` or similar, which appears when the Pico is connected.
     - **Interpreter**: Choose MicroPython (Raspberry Pi Pico).
     - **Project Folder**: Select or create a folder for your project (e.g., `~/PicoProjects/MyProject`).
   - Pico-W-Go creates a `.picowgo` configuration file in your project folder to store settings.

4. **Write a Simple MicroPython Program**:
   - In VSCode, open your project folder (File > Open Folder).
   - Create a new file named `main.py` (MicroPython runs `main.py` automatically on boot).
   - Add a simple program, e.g., to blink the onboard LED:
     ```python
     from machine import Pin
     import time

     led = Pin(25, Pin.OUT)  # Use "LED" for Pico W
     while True:
         led.on()
         time.sleep(0.5)
         led.off()
         time.sleep(0.5)
     ```
   - Save the file (`Ctrl+S`).

5. **Upload the Program to the Pico**:
   - Ensure the Pico is connected and the correct port is selected (re-run **Pico-W-Go > Configure Project** if needed).
   - Open the Command Palette (`Ctrl+Shift+P`).
   - Select **Pico-W-Go > Upload Project to Pico**.
     - This uploads all files in your project folder (e.g., `main.py`) to the Pico’s filesystem.
   - Alternatively, to upload a single file:
     - Right-click `main.py` in the VSCode file explorer.
     - Select **Pico-W-Go > Upload File to Pico**.
   - The file transfers to the Pico, and if it’s `main.py`, it will run automatically on boot.

6. **Run and Test the Program**:
   - **Automatic Execution**: If you uploaded `main.py`, reset the Pico (unplug and replug, or press the RESET button if available). The LED should start blinking.
   - **Manual Execution**:
     - Open the Command Palette and select **Pico-W-Go > Run**.
     - This executes the current file on the Pico.
   - **Use the REPL**:
     - Open the Command Palette and select **Pico-W-Go > Open REPL**.
     - The REPL appears in VSCode’s terminal, where you can test commands:
       ```python
       from machine import Pin
       led = Pin(25, Pin.OUT)
       led.on()
       ```
     - Press `Ctrl+C` to stop a running program in the REPL.

7. **Manage Files on the Pico**:
   - **List Files**: Use **Pico-W-Go > Download Project from Pico** to view or retrieve files from the Pico’s filesystem.
   - **Delete Files**: Open the Command Palette and select **Pico-W-Go > Delete All Files** to clear the Pico’s filesystem, or use the REPL:
     ```python
     import os
     os.remove('main.py')
     ```
   - **Check Output**: Program output (e.g., `print` statements) appears in the REPL or VSCode’s terminal if configured.

---

### Troubleshooting
- **Port Not Detected**:
  - Run `ls /dev/tty*` to confirm the Pico’s port (e.g., `/dev/ttyACM0`).
  - Ensure the USB cable supports data transfer and try a different port.
  - Reconfigure the port in **Pico-W-Go > Configure Project**.
- **Upload Fails**:
  - Verify `pyserial` and `esptool` are installed (`pip3 list`).
  - Check that MicroPython is running (REPL should be accessible).
  - Reflash MicroPython if needed by re-entering BOOTSEL mode and copying the `.uf2` file.
- **LED Not Blinking**:
  - Confirm the correct GPIO pin (`25` for Pico, `"LED"` for Pico W).
  - Test in the REPL:
    ```python
    from machine import Pin
    led = Pin(25, Pin.OUT)
    led.on()
    ```
- **Pico-W-Go Commands Missing**: Ensure the extension is installed and activated. Restart VSCode if needed.

---

### Advantages of Pico-W-Go in VSCode
- **Integrated Workflow**: Combines code editing, file management, and REPL access in VSCode.
- **Advanced Features**: Leverages VSCode’s Git integration, extensions, and customization.
- **Cross-Platform**: Works on Linux, Windows, and macOS.

### Limitations Compared to Thonny
- Setup is slightly more involved (e.g., installing `pyserial`, configuring the port).
- REPL integration may feel less seamless than Thonny’s all-in-one interface.
- Less beginner-friendly for first-time MicroPython users.

---

### Alternative Extensions
If you meant a different extension (e.g., **Pico-Go**), note that Pico-Go is an older alternative to Pico-W-Go and may have fewer features or updates. The setup is similar, but Pico-W-Go is recommended for its active development and support for both Pico and Pico W. If you’re using another specific extension, please clarify, and I can tailor the instructions.

---

### Example Workflow
1. Install Pico-W-Go and dependencies.
2. Configure the project with the correct serial port (`/dev/ttyACM0`).
3. Write and save `main.py` with the LED blink code.
4. Use **Pico-W-Go > Upload Project to Pico** to upload.
5. Reset the Pico or use **Pico-W-Go > Run** to see the LED blink.
6. Use the REPL to test or debug interactively.

If you need help with specific Pico-W-Go commands, another program example, or troubleshooting (e.g., port issues, extension errors), let me know!
