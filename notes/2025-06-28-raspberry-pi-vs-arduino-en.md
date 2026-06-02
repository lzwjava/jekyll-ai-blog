---
audio: false
generated: true
lang: en
layout: post
title: Raspberry Pi vs. Arduino for Washing Machine Monitoring with Telegram Alerts
translated: false
type: note
---

Using a Raspberry Pi instead of an Arduino (like the ESP32-CAM) for detecting when your Maytag MHW8630HW washing machine stops and sending a Telegram notification is a viable alternative, offering more processing power and flexibility at the cost of increased complexity and power consumption. Below, I’ll compare the Raspberry Pi approach with the Arduino solution, outline other microcontroller options, and provide a detailed guide for implementing the system with a Raspberry Pi. I’ll also discuss alternative approaches (e.g., other hardware or sensors) to ensure a comprehensive response.

---

### Comparison: Raspberry Pi vs. Arduino vs. Other Options

| **Feature**                | **Raspberry Pi**                                                                 | **Arduino (ESP32-CAM)**                                                  | **Other Options (e.g., NodeMCU, ESP8266)**                              |
|----------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------|-------------------------------------------------------------------------|
| **Processing Power**       | High (quad-core CPU, 1-8GB RAM) – Supports advanced image processing, OpenCV.    | Limited (dual-core, 520KB SRAM) – Basic image processing only.           | Very limited – Not suitable for camera-based processing.                 |
| **Camera Support**         | Easy with USB webcams or Pi Camera Module (e.g., 8MP Pi Camera v2).             | Built-in OV2640 (2MP) camera, but lower resolution and quality.          | Requires external camera module, complex to integrate.                  |
| **Wi-Fi**                 | Built-in (most models, e.g., Pi 4, Zero 2 W).                                   | Built-in (ESP32-CAM).                                                  | Built-in (e.g., ESP8266), but no native camera support.                 |
| **Programming**            | Python, OpenCV, versatile but requires OS setup (Raspberry Pi OS).              | C++ in Arduino IDE, simpler for beginners.                              | C++ or Lua (e.g., NodeMCU), limited libraries for image processing.     |
| **Power Consumption**      | Higher (~2.5W for Pi Zero, ~5-10W for Pi 4).                                    | Lower (~1-2W for ESP32-CAM).                                           | Lowest (~0.5-1W for ESP8266).                                          |
| **Cost**                   | $10 (Pi Zero W) to $35+ (Pi 4) + $15 for Pi Camera.                            | ~$10 (ESP32-CAM with camera).                                          | ~$5-10 (ESP8266/NodeMCU) + sensor costs.                               |
| **Ease of Setup**          | Moderate (OS setup, Python coding).                                             | Easy (Arduino IDE, single sketch).                                      | Easy for simple sensors, complex for cameras.                           |
| **Best Use Case**          | Advanced image processing, flexible for future expansions (e.g., ML models).    | Simple, low-cost light detection with Telegram integration.             | Non-camera solutions (e.g., vibration or current sensors).              |

**Raspberry Pi Advantages**:
- Superior image processing with OpenCV for robust light detection.
- Easier to debug and expand (e.g., add a web interface or multiple sensors).
- Supports higher-quality cameras for better accuracy in varying light conditions.

**Raspberry Pi Disadvantages**:
- Requires more setup (OS installation, Python environment).
- Higher power consumption, less ideal for battery-powered setups.
- More expensive than ESP32-CAM.

**Other Options**:
- **NodeMCU/ESP8266**: Suitable for non-camera solutions (e.g., using a vibration sensor or current sensor). Limited processing power makes camera integration impractical.
- **Vibration Sensor**: Detects machine vibrations instead of the panel light. Simple but may miss subtle cycle changes.
- **Current Sensor**: Measures power draw (e.g., ACS712 module) to detect when the machine stops. Non-invasive but requires electrical setup.

---

### Raspberry Pi Implementation Guide

#### Tech Stack
**Hardware**:
1. **Raspberry Pi**:
   - **Raspberry Pi Zero 2 W** ($15, compact, Wi-Fi enabled) or **Raspberry Pi 4** ($35+, more powerful).
2. **Camera**:
   - **Raspberry Pi Camera Module v2** ($15, 8MP) or a USB webcam.
3. **Power Supply**:
   - 5V USB-C (Pi 4) or micro-USB (Pi Zero) with 2-3A output.
4. **Mounting**:
   - Enclosure or adhesive mount to position the camera facing the washing machine’s panel light.

**Software**:
1. **OS**: Raspberry Pi OS (Lite for efficiency, Full for easier setup).
2. **Programming Language**: Python.
3. **Libraries**:
   - **OpenCV**: For image processing to detect the panel light.
   - **python-telegram-bot**: For Telegram notifications.
   - **picamera2** (for Pi Camera) or **fswebcam** (for USB webcam).
4. **Telegram Bot**: Same setup as Arduino (use BotFather for bot token and chat ID).

#### Algorithm
The algorithm is similar to the Arduino approach but leverages OpenCV for more robust image processing:
1. **Image Capture**: Use the Pi Camera or webcam to capture images periodically (e.g., every 10 seconds).
2. **Region of Interest (ROI)**: Define a rectangle around the panel light in the image.
3. **Image Processing**:
   - Convert to grayscale.
   - Apply Gaussian blur to reduce noise.
   - Use adaptive thresholding to detect the bright panel light against the background.
   - Calculate the average pixel intensity in the ROI or count bright pixels.
4. **State Machine**:
   - If the ROI is bright (light ON), mark the machine as running.
   - If the ROI is dark (light OFF) for 5 minutes, mark the machine as stopped and send a Telegram notification.
5. **Debouncing**: Implement a 5-minute delay to confirm the machine has stopped.

#### Implementation Steps
1. **Set Up the Raspberry Pi**:
   - Download and flash **Raspberry Pi OS** (Lite or Full) to an SD card using Raspberry Pi Imager.
   - Connect the Pi to Wi-Fi by editing `/etc/wpa_supplicant/wpa_supplicant.conf` or using the GUI.
   - Enable the camera interface via `raspi-config` (Interfacing Options > Camera).

2. **Install Dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-opencv python3-picamera2 python3-pip
   pip3 install python-telegram-bot
   ```

3. **Position the Camera**:
   - Mount the Pi Camera or USB webcam to face the washing machine’s panel light.
   - Test the camera with:
     ```bash
     libcamera-still -o test.jpg
     ```
     or for USB webcam:
     ```bash
     fswebcam test.jpg
     ```

4. **Python Script**:
Below is a sample Python script for the Raspberry Pi to detect the panel light and send Telegram notifications.

```python
import cv2
import numpy as np
from picamera2 import Picamera2
import telegram
import asyncio
import time

# Telegram bot configuration
BOT_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"
bot = telegram.Bot(token=BOT_TOKEN)

# Camera configuration
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration(main={"size": (640, 480)}))
picam2.start()

# ROI configuration (adjust based on camera view)
ROI_X, ROI_Y, ROI_WIDTH, ROI_HEIGHT = 200, 150, 50, 50
THRESHOLD = 150  # Brightness threshold (0-255)
STOP_DELAY = 300  # 5 minutes in seconds

machine_running = False
last_on_time = 0

async def send_telegram_message(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

def is_light_on(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # Extract ROI
    roi = gray[ROI_Y:ROI_Y+ROI_HEIGHT, ROI_X:ROI_X+ROI_WIDTH]
    # Calculate average brightness
    avg_brightness = np.mean(roi)
    return avg_brightness > THRESHOLD

async def main():
    global machine_running, last_on_time
    while True:
        # Capture image
        frame = picam2.capture_array()
        # Check if light is on
        if is_light_on(frame):
            if not machine_running:
                machine_running = True
                print("Machine is ON")
            last_on_time = time.time()
        else:
            if machine_running and (time.time() - last_on_time > STOP_DELAY):
                machine_running = False
                print("Machine stopped")
                await send_telegram_message("Washing machine stopped! Time to hang up clothes.")
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    asyncio.run(main())
```

5. **Customize the Script**:
   - Replace `BOT_TOKEN` and `CHAT_ID` with your Telegram credentials.
   - Adjust `ROI_X`, `ROI_Y`, `ROI_WIDTH`, `ROI_HEIGHT` by capturing a test image and analyzing it with a tool like GIMP or Python to locate the panel light.
   - Tune `THRESHOLD` based on test images (higher for brighter lights).
   - Modify `STOP_DELAY` if needed.

6. **Run the Script**:
   ```bash
   python3 washer_monitor.py
   ```
   - Run in the background with `nohup python3 washer_monitor.py &` or use a systemd service for reliability.

7. **Test and Deploy**:
   - Start the washing machine and monitor the script’s output.
   - Verify Telegram notifications.
   - Secure the Pi and camera in a permanent setup.

---

### Other Alternatives
1. **Vibration Sensor**:
   - **Hardware**: Use a vibration sensor (e.g., SW-420) with an ESP8266 or Raspberry Pi.
   - **Setup**: Attach the sensor to the washing machine to detect vibrations.
   - **Algorithm**: Monitor for sustained absence of vibrations (e.g., 5 minutes) to detect when the machine stops.
   - **Pros**: Simple, low-cost, unaffected by ambient light.
   - **Cons**: May miss cycles with long pauses (e.g., soaking).
   - **Code Example (ESP8266)**:
     ```cpp
     #include <ESP8266WiFi.h>
     #include <UniversalTelegramBot.h>
     #define VIBRATION_PIN D5
     #define BOT_TOKEN "your_bot_token"
     #define CHAT_ID "your_chat_id"
     WiFiClientSecure client;
     UniversalTelegramBot bot(BOT_TOKEN, client);
     bool machineRunning = false;
     unsigned long lastVibrationTime = 0;
     void setup() {
       pinMode(VIBRATION_PIN, INPUT);
       WiFi.begin("ssid", "password");
       while (WiFi.status() != WL_CONNECTED) delay(500);
       client.setInsecure();
     }
     void loop() {
       if (digitalRead(VIBRATION_PIN)) {
         machineRunning = true;
         lastVibrationTime = millis();
       } else if (machineRunning && (millis() - lastVibrationTime > 300000)) {
         machineRunning = false;
         bot.sendMessage(CHAT_ID, "Washing machine stopped!", "");
       }
       delay(1000);
     }
     ```

2. **Current Sensor**:
   - **Hardware**: Use an ACS712 current sensor with an ESP8266 or Raspberry Pi.
   - **Setup**: Non-invasively clamp the sensor around the washing machine’s power cord.
   - **Algorithm**: Detect when current drops below a threshold (e.g., <0.5A) for 5 minutes.
   - **Pros**: Accurate, non-invasive.
   - **Cons**: Requires electrical knowledge, calibration for the machine’s power draw.

3. **Microphones**:
   - **Hardware**: Use a microphone module (e.g., KY-038) with a Raspberry Pi.
   - **Algorithm**: Analyze sound levels to detect when the machine’s noise stops.
   - **Pros**: Non-visual, works in low-light conditions.
   - **Cons**: Sensitive to ambient noise, requires signal processing.

---

### Recommendation
- **Raspberry Pi**: Best for robust image processing and future expandability. Use if you’re comfortable with Python and want high reliability in varying light conditions.
- **Arduino (ESP32-CAM)**: Best for a low-cost, simple setup. Ideal if you want minimal configuration and are okay with basic image processing.
- **Vibration or Current Sensor**: Best for non-camera solutions, especially if the panel light is unreliable (e.g., dim or obscured). Use with ESP8266 for simplicity.
- **Microphone**: Less reliable due to ambient noise, but viable as a secondary sensor.

For your two-story house, the Raspberry Pi or ESP32-CAM with a camera is ideal since you’re on the second floor and need reliable remote notifications via Telegram. The Raspberry Pi offers better accuracy for light detection, while the ESP32-CAM is cheaper and simpler to deploy. If you prefer a non-camera approach, a vibration sensor with an ESP8266 is the easiest alternative.

Let me know if you want a deeper dive into any specific approach, need help with setup, or want code for an alternative sensor!
