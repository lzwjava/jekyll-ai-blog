---
audio: false
generated: true
lang: en
layout: post
title: Installing Arduino IDE on Ubuntu
translated: false
type: note
---

To install the Arduino IDE on Ubuntu Linux, follow these steps:

1. **Download the Arduino IDE**:
   - Visit the official Arduino website at [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software).
   - Under the "Arduino IDE" section, select the "Linux 64 bits" download option (or the appropriate version for your system, e.g., Linux ARM for Raspberry Pi).

2. **Extract the Downloaded File**:
   - The downloaded file is a compressed `.tar.xz` archive (e.g., `arduino-1.8.19-linux64.tar.xz`).
   - Open a terminal and navigate to the download directory (e.g., `cd ~/Downloads`).
   - Extract the file using:
     ```bash
     tar -xf arduino-*.tar.xz
     ```
   - This creates a folder like `arduino-1.8.19`.

3. **Move to an Appropriate Directory (Optional)**:
   - For system-wide access, move the extracted folder to `/opt` (requires superuser privileges):
     ```bash
     sudo mv arduino-1.8.19 /opt/arduino
     ```

4. **Run the Installation Script**:
   - Navigate to the Arduino folder:
     ```bash
     cd /opt/arduino
     ```
   - Run the installation script:
     ```bash
     sudo ./install.sh
     ```
   - This creates a desktop shortcut and sets up the necessary permissions.

5. **Add Your User to the Dialout Group**:
   - To access the Arduino board via the serial port, add your user to the `dialout` group:
     ```bash
     sudo usermod -a -G dialout $USER
     ```
   - Log out and back in, or reboot for the group change to take effect.

6. **Launch the Arduino IDE**:
   - If you ran the `install.sh` script, you can launch the IDE from the application menu or by searching for "Arduino IDE."
   - Alternatively, run it directly from the terminal:
     ```bash
     /opt/arduino/arduino
     ```

7. **Update Permissions for the Arduino Board (if needed)**:
   - When connecting your Arduino, ensure it’s detected (e.g., `/dev/ttyACM0` or `/dev/ttyUSB0`).
   - If you encounter permission issues, set the correct permissions:
     ```bash
     sudo chmod a+rw /dev/ttyACM0
     ```
   - Replace `/dev/ttyACM0` with the appropriate port.

8. **Verify Installation**:
   - Connect your Arduino board via USB.
   - Open the IDE, go to **Tools > Board** and select your Arduino model (e.g., Arduino Uno).
   - Go to **Tools > Port** and select the port (e.g., `/dev/ttyACM0`).
   - Try uploading a sample sketch (e.g., **File > Examples > 01.Basics > Blink**) to confirm everything works.

**Alternative: Install via Snap or Flatpak**:
- **Snap**:
  ```bash
  sudo snap install arduino
  ```
- **Flatpak**:
  ```bash
  sudo flatpak install flathub cc.arduino.ArduinoIDE
  ```
- These methods simplify installation but may have limitations with permissions or board detection.

**Notes**:
- Ensure you have Java installed, as the Arduino IDE requires it. Install it if needed:
  ```bash
  sudo apt update
  sudo apt install default-jre
  ```
- For the latest version or troubleshooting, check the Arduino forums or the [official documentation](https://www.arduino.cc/en/Guide/Linux).

If you encounter issues, let me know your Ubuntu version or specific error for tailored help!

---

Since your Arduino Uno is detected in the Arduino IDE on Ubuntu and you want a simple example without using a breadboard or external components, here's a basic sketch that blinks the built-in LED on the Arduino Uno (connected to digital pin 13). This requires no extra hardware.

```cpp
void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT); // Set the built-in LED pin (pin 13) as output
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(LED_BUILTIN, HIGH); // Turn the LED on
  delay(1000);                     // Wait for 1 second
  digitalWrite(LED_BUILTIN, LOW);  // Turn the LED off
  delay(1000);                     // Wait for 1 second
}
```

### How to Run It:
1. Open the Arduino IDE.
2. Copy and paste the above code into the IDE.
3. Ensure your Arduino Uno is connected via USB and detected:
   - Go to **Tools > Board** and select **Arduino Uno**.
   - Go to **Tools > Port** and select the port (e.g., `/dev/ttyACM0` or `/dev/ttyUSB0`).
4. Click the **Upload** button (right arrow icon) to compile and upload the sketch to your Arduino Uno.
5. Once uploaded, the built-in LED (labeled "L" on the board) should blink on for 1 second, then off for 1 second, repeatedly.

### What It Does:
- In `setup()`, the `pinMode` function configures the built-in LED pin as an output.
- In `loop()`, the `digitalWrite` function turns the LED on (`HIGH`) and off (`LOW`), with `delay` pausing for 1 second between each state, creating a blinking effect.

### Notes:
- No external components are needed since the Arduino Uno has a built-in LED on pin 13.
- If the LED doesn’t blink, double-check the port selection or ensure the board is properly connected. You can also open the **Serial Monitor** (Tools > Serial Monitor) to debug if you add `Serial.begin(9600);` in `setup()` and print messages like `Serial.println("Blink");` in `loop()`.
- If you want to modify the blink speed, adjust the `delay(1000)` values (e.g., `delay(500)` for faster blinking).

Let me know if you run into issues or want another simple example!

---

The error message indicates a permission issue when trying to upload the sketch to your Arduino Uno on Ubuntu. The Arduino IDE cannot access the serial port `/dev/ttyUSB0` due to insufficient permissions. Here’s how to fix it:

### Solution: Fix Serial Port Permissions

1. **Add Your User to the `dialout` Group**:
   - The `dialout` group typically controls access to serial ports in Ubuntu. Add your user to this group:
     ```bash
     sudo usermod -a -G dialout $USER
     ```
   - After running this, log out and log back in, or reboot your system for the change to take effect:
     ```bash
     sudo reboot
     ```

2. **Verify the Port**:
   - After rebooting, reconnect your Arduino Uno and open the Arduino IDE.
   - Go to **Tools > Port** and ensure `/dev/ttyUSB0` (or `/dev/ttyACM0` for some Arduino boards) is selected. If no port appears, check the USB connection or try a different cable/port.

3. **Temporarily Change Port Permissions (Optional)**:
   - If the issue persists after adding your user to the `dialout` group, you can manually set permissions for the port (this is a temporary fix, as permissions reset on reboot):
     ```bash
     sudo chmod a+rw /dev/ttyUSB0
     ```
   - Replace `/dev/ttyUSB0` with the correct port if it’s different (e.g., `/dev/ttyACM0`).

4. **Try Uploading Again**:
   - In the Arduino IDE, click the **Upload** button to upload your sketch (e.g., the blinking LED sketch from before).
   - If it uploads successfully, you should see the built-in LED on your Arduino Uno start blinking.

### Additional Troubleshooting

- **Check the Arduino Board and Cable**:
  - Ensure the Arduino Uno is properly connected via USB and recognized by Ubuntu. Run this command to list connected devices:
    ```bash
    ls /dev/tty*
    ```
    Look for `/dev/ttyUSB0` or `/dev/ttyACM0` when the board is plugged in.
  - Try a different USB cable or port if the board isn’t detected.

- **Verify Board and Port Settings**:
  - In the Arduino IDE, confirm that **Tools > Board** is set to **Arduino Uno**.
  - If `/dev/ttyUSB0` doesn’t appear, try **Tools > Port** after unplugging and replugging the board.

- **Run Arduino IDE as Root (Temporary Workaround)**:
  - If the above steps don’t work, you can run the IDE with superuser privileges to bypass permission issues (not recommended long-term):
    ```bash
    sudo arduino
    ```
    Replace `arduino` with the path to your Arduino IDE executable if it’s not in your system’s PATH (e.g., `/opt/arduino/arduino`).

- **Check for Conflicting Software**:
  - Other software (e.g., `brltty`, a braille display driver) can interfere with serial ports. Remove it if installed:
    ```bash
    sudo apt remove brltty
    ```

- **Driver Issues**:
  - Some Arduino clones use the CH340/CH341 chip, requiring a driver. Install it if needed:
    ```bash
    sudo apt install linux-modules-extra-$(uname -r)
    ```
    Then, reconnect the board.

### Confirm Fix
Once the permissions are resolved, try uploading the previous blink sketch again:
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

If you still face issues, share the new error message or run `ls -l /dev/ttyUSB0` in the terminal and provide the output to help diagnose further.

---

It seems you're encountering an issue while trying to upload a sketch to your Arduino Uno using the Arduino IDE on Ubuntu. The error message you provided is:

```
avrdude: ser_open(): can't open device "/dev/ttyUSB0": Permission denied
Failed uploading: uploading error: exit status 1
```

This error indicates that the Arduino IDE does not have the necessary permissions to access the serial port (`/dev/ttyUSB0`) where your Arduino Uno is connected. This is a common issue on Linux systems like Ubuntu due to how serial port access is managed. Below is a step-by-step guide to fix this problem.

---

### Solution: Fix Serial Port Permission Issue

#### 1. Add Your User to the `dialout` Group
In Ubuntu, the `dialout` group controls access to serial ports. To resolve the permission issue, you need to add your user to this group.

- Open a terminal by pressing `Ctrl + Alt + T`.
- Run the following command:
  ```bash
  sudo usermod -a -G dialout $USER
  ```
- This command adds your current user to the `dialout` group. The `$USER` variable automatically uses your username.

#### 2. Log Out and Log Back In
For the group change to take effect, you need to log out of your current session and log back in. Alternatively, you can reboot your system.

- **To log out and log back in:**
  - Save any open work.
  - Click on your username in the top-right corner of the Ubuntu desktop and select "Log Out."
  - Log back in with your username and password.
- **To reboot (optional):**
  - Run this command in the terminal:
    ```bash
    sudo reboot
    ```
  - Wait for your system to restart.

#### 3. Verify the Serial Port
After logging back in, ensure your Arduino Uno is properly recognized by the system.

- Reconnect your Arduino Uno to the USB port.
- Open the Arduino IDE.
- Go to **Tools > Port** in the menu and check if `/dev/ttyUSB0` (or `/dev/ttyACM0` for some Arduino boards) is listed and selected.
- If the port doesn’t appear:
  - Unplug and replug the Arduino Uno.
  - Check the USB connection or try a different cable/port.

#### 4. Upload the Sketch Again
With the correct port selected, try uploading your sketch again:

```cpp
void setup() {
  pinMode(LED_BUILTIN, OUTPUT); // Set the built-in LED pin (pin 13) as output
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH); // Turn the LED on
  delay(1000);                     // Wait for 1 second
  digitalWrite(LED_BUILTIN, LOW);  // Turn the LED off
  delay(1000);                     // Wait for 1 second
}
```

- Click the **Upload** button (the right arrow icon) in the Arduino IDE.
- If successful, the built-in LED on your Arduino Uno should start blinking (on for 1 second, off for 1 second).

---

### Additional Troubleshooting
If the above steps don’t resolve the issue, try these additional checks:

#### Check Group Membership
Verify that your user is part of the `dialout` group:
- Run this command in the terminal:
  ```bash
  groups $USER
  ```
- Look for `dialout` in the output. If it’s missing, repeat Step 1 and ensure you log out/in or reboot.

#### Temporary Permission Fix (Not Recommended Long-Term)
If you need a quick fix, you can manually change the permissions of the serial port:
- Run:
  ```bash
  sudo chmod a+rw /dev/ttyUSB0
  ```
- Then try uploading again. Note: This is temporary and will reset after unplugging the Arduino or rebooting.

#### Check for Conflicting Software
Some software, like `brltty` (a braille display driver), can interfere with serial ports. To remove it:
- Run:
  ```bash
  sudo apt remove brltty
  ```
- Reconnect your Arduino and try again.

#### Verify the Arduino Connection
Ensure Ubuntu recognizes your Arduino:
- Run:
  ```bash
  ls /dev/tty*
  ```
- Look for `/dev/ttyUSB0` or `/dev/ttyACM0` when the Arduino is plugged in. If it’s missing, check your USB cable or port.

#### Run Arduino IDE as Root (Temporary Workaround)
As a last resort, you can run the IDE with superuser privileges:
- Close the Arduino IDE.
- Open a terminal and run:
  ```bash
  sudo arduino-ide
  ```
- Replace `arduino-ide` with the correct command or path if needed (e.g., `/home/lzw/arduino-ide_2.3.6_Linux_64bit/arduino-ide`).
- Try uploading again. Avoid using this method regularly, as it’s less secure.

---

### Confirm the Fix
After following these steps, your sketch should upload successfully, and the LED on your Arduino Uno should blink as expected. If you still encounter issues, please provide additional details, such as:
- The output of `ls -l /dev/ttyUSB0` (to check permissions).
- Any new error messages from the Arduino IDE.

Let me know if you need further assistance!
