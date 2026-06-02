---
audio: false
generated: true
lang: en
layout: post
title: VSCode for Raspberry Pi Pico MicroPython
translated: false
type: note
---

Yes, you can use Visual Studio Code (VSCode) to write, upload, and run MicroPython programs on your Raspberry Pi Pico, similar to how you would with Thonny. VSCode is a powerful editor, and with the right extensions and tools, it can handle MicroPython development effectively. Below is a step-by-step guide to set up VSCode for uploading a simple MicroPython program to your Pico, assuming MicroPython is already flashed (as you’ve done with the `.uf2` file).

---

### Prerequisites

1. **MicroPython Flashed**: Your Pico has MicroPython installed (e.g., from the `RPI_PICO-20250415-v1.25.0.uf2` file).
2. **VSCode Installed**: Download and install VSCode from [code.visualstudio.com](https://code.visualstudio.com) if you haven’t already.
3. **Python Installed**: Install Python (required for MicroPython tools) via:

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

4. **USB Connection**: The Pico is connected to your computer via a data-capable USB cable.

---

### Step-by-Step Guide to Use VSCode for MicroPython on Raspberry Pi Pico

1. **Install Required VSCode Extensions**:
   - Open VSCode.
   - Go to the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X` on macOS).
   - Install the following extensions:
     - **Python** (by Microsoft): For Python and MicroPython syntax highlighting and IntelliSense.
     - **Pico-W-Go** (optional but recommended): A dedicated extension for Raspberry Pi Pico development with MicroPython. Search for “Pico-W-Go” and install it.
       - Note: Pico-W-Go simplifies file transfers and REPL access but requires additional setup (described below).
     - Alternatively, you can use general-purpose extensions like **Remote-SSH** or **Serial Monitor** if you prefer manual control.

2. **Set Up Pico-W-Go (Recommended)**:
   - **Install Dependencies**: Pico-W-Go requires `pyserial` and `esptool`. Install them via pip:

     ```bash
     pip3 install pyserial esptool
     ```

   - **Configure Pico-W-Go**:
     - Open VSCode’s Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`).
     - Type and select **Pico-W-Go > Configure Project**.
     - Follow the prompts to set up your project:
       - Choose the Pico’s serial port (e.g., `/dev/ttyACM0`). Run `ls /dev/tty*` in a terminal to find it.
       - Select MicroPython as the interpreter.
       - Create a new project folder or use an existing one.
     - Pico-W-Go creates a workspace with a `.picowgo` configuration file.

3. **Write a Simple MicroPython Program**:
   - In VSCode, create a new file (e.g., `main.py`) in your project folder.
   - Write a simple program, like blinking the onboard LED:

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

   - Save the file (`Ctrl+S` or `Cmd+S`).

4. **Upload the Program to the Pico**:
   - **Using Pico-W-Go**:
     - Ensure the Pico is connected and the correct port is selected (check in `Pico-W-Go > Configure Project` if needed).
     - Open the Command Palette (`Ctrl+Shift+P`).
     - Select **Pico-W-Go > Upload Project to Pico**.
     - This uploads all files in your project folder (e.g., `main.py`) to the Pico’s filesystem.
     - If you named the file `main.py`, it will run automatically on boot.
   - **Manual Upload with `rshell`** (if not using Pico-W-Go):
     - Install `rshell`:

       ```bash
       pip3 install rshell
       ```

     - Connect to the Pico:

       ```bash
       rshell --port /dev/ttyACM0
       ```

     - Copy the file to the Pico:

       ```bash
       cp main.py /pyboard/main.py
       ```

     - Exit `rshell` with `exit`.

5. **Run and Test the Program**:
   - **Using Pico-W-Go**:
     - Open the Command Palette and select **Pico-W-Go > Run**.
     - This executes the current file or opens the REPL for manual commands.
     - You should see the LED blinking if using the example above.
   - **Using VSCode’s Terminal or REPL**:
     - Open the REPL with Pico-W-Go (`Pico-W-Go > Open REPL`) or use `rshell`:

       ```bash
       rshell --port /dev/ttyACM0 repl
       ```

     - Test commands directly, e.g.:

       ```python
       from machine import Pin
       led = Pin(25, Pin.OUT)
       led.on()
       ```

     - Press `Ctrl+C` to stop a running program in the REPL.
   - If the file is `main.py`, reset the Pico (unplug and replug, or press the RESET button) to run it automatically.

6. **Debug and Manage Files**:
   - **Pico-W-Go**: Use **Pico-W-Go > Download Project from Pico** to retrieve files from the Pico or **Pico-W-Go > Delete All Files** to clear the filesystem.
   - **rshell**: List files with:

     ```bash
     rshell ls /pyboard
     ```

     Delete files with:

     ```bash
     rshell rm /pyboard/main.py
     ```

   - Check program output in the VSCode terminal or REPL.

---

### Alternative: Manual Workflow Without Pico-W-Go

If you prefer not to use Pico-W-Go, you can manage MicroPython development manually:

1. Write your code in VSCode and save it as `main.py`.
2. Use `ampy` (another MicroPython tool) to upload:

   ```bash
   pip3 install adafruit-ampy
   ampy --port /dev/ttyACM0 put main.py
   ```

3. Access the REPL with a terminal tool like `minicom` or `screen`:

   ```bash
   screen /dev/ttyACM0 115200
   ```

   Press `Ctrl+C` to stop a running program and enter the REPL.

---

### Troubleshooting

- **Port Not Found**: Run `ls /dev/tty*` to verify the Pico’s port (e.g., `/dev/ttyACM0`). Ensure the Pico is connected and MicroPython is flashed.
- **Pico-W-Go Errors**: Check that `pyserial` and `esptool` are installed and the correct port is selected. Restart VSCode if needed.
- **Program Not Running**: Ensure the file is saved as `main.py` for auto-execution, or run it manually via the REPL or `ampy run main.py`.
- **LED Not Blinking**: Verify the GPIO pin (`25` for Pico, `"LED"` for Pico W). Test in the REPL:

  ```python
  from machine import Pin
  led = Pin(25, Pin.OUT)
  led.on()
  ```

---

### Advantages of VSCode Over Thonny

- Better code editing features (e.g., IntelliSense, Git integration, customizable workflows).
- Supports larger projects with multiple files.
- Pico-W-Go provides a Thonny-like experience but with VSCode’s power.

### Limitations

- Setup is slightly more complex than Thonny.
- REPL integration may feel less seamless compared to Thonny’s all-in-one interface.

If you need help with specific VSCode settings, installing tools, or writing more complex MicroPython programs, let me know!
