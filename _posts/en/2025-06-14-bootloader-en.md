---
audio: false
generated: true
lang: en
layout: post
title: Burning a Bootloader
translated: false
type: note
---

Burning a bootloader onto an Arduino Uno R3 is necessary if the microcontroller (ATmega328P) is blank, corrupted, or needs to be replaced. This process programs the chip with the firmware required to communicate with the Arduino IDE and run sketches. Below is a step-by-step guide to burn the bootloader using common methods.

---

### **Requirements**
- **Arduino Uno R3** (the target board with the ATmega328P to be programmed).
- **Programmer**: One of the following:
  - Another working Arduino board (e.g., another Uno R3) as an "Arduino as ISP."
  - A dedicated programmer like **USBasp**, **AVRISP mkII**, or **Atmel-ICE**.
- **Arduino IDE** (download from [arduino.cc](https://www.arduino.cc/en/software)).
- **Jumper wires** (if using Arduino as ISP).
- **USB cable** (for connecting the programmer or Arduino to your computer).

---

### **Method 1: Using Another Arduino (Arduino as ISP)**

This method uses a second Arduino board (e.g., another Uno R3) as an In-System Programmer (ISP) to burn the bootloader.

#### **Steps**
1. **Prepare the Programmer Arduino**:
   - Connect the second Arduino (the programmer) to your computer via USB.
   - Open the Arduino IDE, go to **File > Examples > 11.ArduinoISP > ArduinoISP**, and upload this sketch to the programmer Arduino. This turns it into an ISP.

2. **Connect the Boards**:
   - Wire the programmer Arduino to the target Arduino Uno R3 (the one needing the bootloader) as follows:
     - **Programmer Arduino** → **Target Arduino Uno R3**:
       - 5V → 5V
       - GND → GND
       - Pin 10 → Reset
       - Pin 11 → Pin 11 (MOSI)
       - Pin 12 → Pin 12 (MISO)
       - Pin 13 → Pin 13 (SCK)
   - Alternatively, if the target Uno R3 has an **ICSP header**, connect the corresponding ICSP pins (MOSI, MISO, SCK, VCC, GND, Reset) directly using jumper wires.

3. **Set Up the Arduino IDE**:
   - In the Arduino IDE, go to **Tools > Board** and select **Arduino Uno** (for the target Uno R3).
   - Go to **Tools > Programmer** and select **Arduino as ISP**.
   - Ensure the correct port for the programmer Arduino is selected under **Tools > Port**.

4. **Burn the Bootloader**:
   - Go to **Tools > Burn Bootloader**.
   - The IDE will use the programmer Arduino to flash the bootloader onto the target Uno R3’s ATmega328P. This may take a minute.
   - If successful, you’ll see a “Done burning bootloader” message. If there’s an error, double-check connections and ensure the programmer Arduino is running the ArduinoISP sketch.

5. **Test the Target Board**:
   - Disconnect the programmer Arduino and wires.
   - Connect the target Uno R3 to your computer via USB.
   - Upload a simple sketch (e.g., Blink from **File > Examples > 01.Basics > Blink**) to confirm the bootloader works.

---

### **Method 2: Using a Dedicated ISP Programmer (e.g., USBasp)**

If you have a dedicated programmer like USBasp, the process is simpler and often more reliable.

#### **Steps**
1. **Connect the Programmer**:
   - Connect the USBasp (or similar programmer) to your computer via USB.
   - Connect the programmer to the target Arduino Uno R3’s **ICSP header** using a 6-pin ICSP cable. Ensure correct orientation (pin 1 is marked with a dot or notch on the ICSP header).

2. **Set Up the Arduino IDE**:
   - Open the Arduino IDE.
   - Go to **Tools > Board** and select **Arduino Uno**.
   - Go to **Tools > Programmer** and select your programmer (e.g., **USBasp** or **AVRISP mkII**).
   - Select the correct port under **Tools > Port** (if applicable, some programmers don’t require port selection).

3. **Burn the Bootloader**:
   - Go to **Tools > Burn Bootloader**.
   - The IDE will use the programmer to flash the bootloader. This takes about 10-30 seconds.
   - A “Done burning bootloader” message indicates success. If it fails, check connections and ensure the programmer is recognized by your computer.

4. **Test the Board**:
   - Disconnect the programmer.
   - Connect the Uno R3 to your computer via USB and upload a test sketch (e.g., Blink) to verify functionality.

---

### **Troubleshooting Tips**
- **Error Messages**: If you get errors like “avrdude: stk500_getsync()” or “not in sync,” check:
  - All connections (wires or ICSP cable).
  - The programmer Arduino is running the ArduinoISP sketch (Method 1).
  - The correct programmer is selected in the IDE.
- **Driver Issues**: For USBasp or other programmers, ensure drivers are installed (e.g., Zadig for USBasp on Windows).
- **Blank Microcontroller**: If the ATmega328P is new or blank, it may need an external 16 MHz crystal and two 22pF capacitors connected to pins 9 and 10 (XTAL1/XTAL2) if not already present on the Uno R3 board.
- **Power Supply**: Ensure the target board is powered (via USB or VIN) during programming.

---

### **Additional Notes**
- **Why Burn a Bootloader?**: The bootloader allows the Arduino Uno R3 to communicate with the Arduino IDE over USB for uploading sketches. Without it, the board won’t respond to USB uploads.
- **Bootloader Type**: The Uno R3 uses the **Optiboot bootloader**, which is compact and supports faster uploads compared to older bootloaders.
- **Replacing the Microcontroller**: If you’re replacing the ATmega328P, ensure it’s an ATmega328P-PU (DIP package) for the Uno R3’s socket. SMD versions require advanced soldering.
- **Alternative Tools**: You can also use **AVRDUDE** or **PlatformIO** for burning the bootloader, but the Arduino IDE is the easiest for beginners.

If you need clarification on any step or help with a specific programmer, let me know!
