---
audio: false
generated: true
lang: en
layout: post
title: Raspberry Pi Pico LED Button Setup
translated: false
type: note
---

To set up a Raspberry Pi Pico to run the provided MicroPython code, which controls an LED based on a button press, follow these steps:

### Hardware Requirements

- **Raspberry Pi Pico** (or Pico W)
- **LED** (with an appropriate current-limiting resistor, e.g., 220–330 ohms)
- **Pushbutton switch**
- **Jumper wires**
- **Breadboard** (optional, for easier connections)
- **USB cable** (to connect the Pico to your computer)

### Hardware Setup

1. **Connect the LED**:
   - Connect the LED's anode (longer leg) to **GPIO 25** (physical pin 30) on the Pico.
   - Connect the LED's cathode (shorter leg) to a **ground (GND)** pin (e.g., physical pin 3) through a 220–330 ohm resistor to limit current.

2. **Connect the Button**:
   - Connect one side of the pushbutton to **GPIO 14** (physical pin 19).
   - Connect the other side of the button to a **3.3V** pin (e.g., physical pin 36, 3V3(OUT)).
   - The code uses an internal pull-down resistor (`Pin.PULL_DOWN`), so no external pull-down resistor is needed. When the button is pressed, GPIO 14 will read HIGH (1); when not pressed, it will read LOW (0).

3. **Verify Connections**:
   - Ensure all connections are secure. Use a breadboard or direct wiring, and double-check that the LED polarity is correct and the resistor is properly placed.
   - Refer to the Pico pinout diagram (available online or in the Pico datasheet) to confirm pin assignments.

### Software Setup

1. **Install MicroPython on the Pico**:
   - Download the latest MicroPython UF2 firmware for the Raspberry Pi Pico from the [official MicroPython website](https://micropython.org/download/rp2-pico/).
   - Connect the Pico to your computer via a USB cable while holding the **BOOTSEL** button.
   - The Pico will appear as a USB drive (RPI-RP2). Drag and drop the downloaded `.uf2` file onto this drive.
   - The Pico will automatically reboot with MicroPython installed.

2. **Set Up a Development Environment**:
   - Install a MicroPython-compatible IDE, such as **Thonny** (recommended for beginners):
     - Download and install Thonny from [thonny.org](https://thonny.org).
     - In Thonny, go to **Tools > Options > Interpreter**, select **MicroPython (Raspberry Pi Pico)**, and choose the appropriate port (e.g., `COMx` on Windows or `/dev/ttyACM0` on Linux/macOS).
   - Alternatively, you can use tools like `rshell`, `ampy`, or Visual Studio Code with the MicroPython extension.

3. **Upload and Run the Code**:
   - Copy the provided code into a file named `main.py`:

     ```python
     from machine import Pin
     import time

     led = Pin(25, Pin.OUT)
     button = Pin(14, Pin.IN, Pin.PULL_DOWN)

     while True:
         if button.value():
             led.on()
         else:
             led.off()
         time.sleep(0.05)
     ```

   - In Thonny:
     - Open a new file, paste the code, and save it to the Pico as `main.py` (MicroPython automatically runs `main.py` on boot).
     - Click the **Run** button or press **F5** to upload and execute the code.
   - Alternatively, use `ampy` to upload the file:

     ```bash
     ampy --port /dev/ttyACM0 put main.py
     ```

     Replace `/dev/ttyACM0` with your Pico’s port.

4. **Test the Program**:
   - Once the code is uploaded, the LED should turn on when the button is pressed and turn off when released. The `time.sleep(0.05)` adds a 50ms delay to debounce the button and reduce CPU load.

### Troubleshooting

- **LED doesn’t light up**:
  - Check LED polarity (anode to GPIO 25, cathode to GND via resistor).
  - Verify the GPIO pin (25) matches the code and physical connection.
  - Ensure the LED and resistor are functional (test with a multimeter or another circuit).
- **Button doesn’t work**:
  - Confirm GPIO 14 is connected correctly and the button connects to 3.3V when pressed.
  - Check that `Pin.PULL_DOWN` is appropriate; if the button is wired differently (e.g., to GND), adjust the code to use `Pin.PULL_UP` and reverse the logic (`if not button.value()`).
- **Code doesn’t run**:
  - Ensure MicroPython is installed correctly.
  - Verify the file is saved as `main.py` on the Pico.
  - Check the USB connection and port settings in your IDE.

### Notes

- The code assumes the button connects GPIO 14 to 3.3V when pressed. If your button connects to GND instead, modify the code to use `Pin.PULL_UP` and reverse the logic:

  ```python
  button = Pin(14, Pin.IN, Pin.PULL_UP)
  while True:
      if not button.value():  # Button pressed = LOW
          led.on()
      else:
          led.off()
      time.sleep(0.05)
  ```

- If you experience button bounce (flickering LED), increase the `time.sleep` value or implement software debouncing.
- For a Pico W, the setup is identical, but ensure you’re using the correct GPIO pins, as the pinout is the same.

If you need further clarification or help with specific issues, let me know!
