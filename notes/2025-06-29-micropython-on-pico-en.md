---
audio: false
generated: true
lang: en
layout: post
title: Upload MicroPython to Pico
translated: false
type: note
---

After flashing MicroPython onto your Raspberry Pi Pico (using the `.uf2` file as described), you can upload and run a simple MicroPython program using a tool like Thonny IDE, which is beginner-friendly and widely used for MicroPython development. Below are the steps to set up MicroPython and upload a simple program to your Pico.

---

### Prerequisites
1. **MicroPython Flashed**: You’ve already copied `RPI_PICO-20250415-v1.25.0.uf2` to the `RPI-RP2` drive, and the Pico has restarted (the `RPI-RP2` drive should no longer appear).
2. **USB Connection**: The Pico is connected to your computer via a USB cable that supports data transfer.
3. **Thonny IDE**: Install Thonny if you haven’t already:
   - **Linux**: Install Thonny using your package manager or download it from [thonny.org](https://thonny.org).
     ```bash
     sudo apt update
     sudo apt install thonny
     ```
   - Alternatively, use `pip`:
     ```bash
     pip install thonny
     ```
   - For Windows/macOS, download and install from [thonny.org](https://thonny.org).

---

### Step-by-Step Guide to Upload a Simple MicroPython Program

1. **Connect the Pico and Open Thonny**:
   - Plug your Pico into your computer’s USB port.
   - Open Thonny IDE.

2. **Configure Thonny for MicroPython**:
   - In Thonny, go to **Tools > Options > Interpreter** (or **Run > Select interpreter**).
   - Select **MicroPython (Raspberry Pi Pico)** from the interpreter dropdown.
   - If the Pico’s serial port (e.g., `/dev/ttyACM0` on Linux) doesn’t appear automatically:
     - Check available ports in the dropdown or run `ls /dev/tty*` in a terminal to identify the Pico’s port (usually `/dev/ttyACM0` or similar).
     - Select the correct port manually.
   - Click **OK** to save.

3. **Verify MicroPython is Running**:
   - In Thonny’s **Shell** (bottom panel), you should see a MicroPython REPL prompt like:
     ```
     >>>
     ```
   - Test it by typing a simple command, e.g.:
     ```python
     print("Hello, Pico!")
     ```
     Press Enter, and you should see the output in the Shell.

4. **Write a Simple MicroPython Program**:
   - In Thonny’s main editor, create a new file and write a simple program. For example, a program to blink the Pico’s onboard LED (on GPIO 25 for Pico, or "LED" for Pico W):
     ```python
     from machine import Pin
     import time

     # Initialize the onboard LED
     led = Pin(25, Pin.OUT)  # Use "LED" instead of 25 for Pico W

     # Blink the LED
     while True:
         led.on()           # Turn LED on
         time.sleep(0.5)    # Wait 0.5 seconds
         led.off()          # Turn LED off
         time.sleep(0.5)    # Wait 0.5 seconds
     ```
   - Note: If using a Pico W, replace `Pin(25, Pin.OUT)` with `Pin("LED", Pin.OUT)`.

5. **Save the Program to the Pico**:
   - Click **File > Save As**.
   - In the dialog, select **Raspberry Pi Pico** as the destination (not your computer).
   - Name the file `main.py` (MicroPython runs `main.py` automatically on boot) or another name like `blink.py`.
   - Click **OK** to save the file to the Pico’s filesystem.

6. **Run the Program**:
   - Click the green **Run** button (or press **F5**) in Thonny to execute the program.
   - Alternatively, if you saved it as `main.py`, reset the Pico (unplug and replug, or press the RESET button if available), and the program will run automatically.
   - You should see the onboard LED blinking every 0.5 seconds.

7. **Stop the Program** (if needed):
   - To stop the program, press **Ctrl+C** in Thonny’s Shell to interrupt the running script.
   - To remove `main.py` from auto-running, delete it from the Pico:
     - In Thonny, go to **View > Files**, select the Pico’s filesystem, right-click `main.py`, and choose **Delete**.

---

### Testing and Troubleshooting
- **No REPL Prompt**: If Thonny doesn’t show the MicroPython REPL:
  - Ensure the correct port is selected in the interpreter settings.
  - Verify MicroPython flashed correctly. If not, reflash the `.uf2` file as described earlier.
  - Check the USB cable (must support data) and try a different port.
- **LED Not Blinking**: Ensure the correct GPIO pin is used (`25` for Pico, `"LED"` for Pico W). If it still doesn’t work, test the LED with a simple REPL command:
  ```python
  from machine import Pin
  led = Pin(25, Pin.OUT)
  led.on()
  ```
- **File Not Saving**: Ensure Thonny is connected to the Pico and the interpreter is set to MicroPython (Raspberry Pi Pico).

---

### Additional Tips
- **Using Other Tools**: Besides Thonny, you can use `rshell` or `ampy` to manage files on the Pico:
  ```bash
  pip install rshell
  rshell --port /dev/ttyACM0
  cp blink.py /pyboard/main.py
  ```
- **More Example Programs**:
  - Read a button press (e.g., on GPIO 14):
    ```python
    from machine import Pin
    button = Pin(14, Pin.IN, Pin.PULL_UP)
    while True:
        print(button.value())
    ```
  - Control an external LED or other peripherals by adjusting the GPIO pin number.
- **Auto-Run**: Saving a file as `main.py` makes it run automatically on boot. Use `boot.py` for setup code that runs before `main.py`.

If you encounter specific issues (e.g., port detection, errors in Thonny, or hardware problems), or want to try a different program, let me know, and I’ll guide you further!
