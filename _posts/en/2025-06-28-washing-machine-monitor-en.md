---
audio: false
generated: true
lang: en
layout: post
title: Smart Washing Machine Monitor with Arduino and Telegram Alerts
translated: false
type: note
---

To create a system that detects when your Maytag MHW8630HW washing machine stops (using its panel light as an indicator) and notifies you via a Telegram bot to hang up your clothes, you can use an Arduino with a camera module to monitor the machine’s status. Below is a detailed guide on the tech stack, hardware setup, algorithm, and implementation steps.

---

### Tech Stack
#### Hardware
1. **Arduino Board**:
   - **ESP32-CAM** (recommended) – Combines a microcontroller with a built-in OV2640 camera and Wi-Fi capability, perfect for image processing and Telegram integration.
   - Alternative: Arduino Uno + separate camera module (e.g., OV7670) and ESP8266 for Wi-Fi, but this is more complex to set up.
2. **Camera Module**:
   - OV2640 (included with ESP32-CAM) – 2MP camera sufficient for detecting the panel light.
3. **Light Sensor (Optional)**:
   - Photoresistor (LDR) or TSL2561 – To supplement camera-based light detection for redundancy or simpler setups.
4. **Power Supply**:
   - 5V USB power adapter or battery pack for the ESP32-CAM.
5. **Mounting**:
   - Small enclosure or 3D-printed case to hold the ESP32-CAM, with a clear view of the washing machine’s control panel.
6. **Wi-Fi Router**:
   - For the ESP32-CAM to connect to the internet and communicate with the Telegram bot.

#### Software
1. **Arduino IDE**:
   - For programming the ESP32-CAM.
2. **Libraries**:
   - **Universal Arduino Telegram Bot Library** by Brian Lough – For Telegram bot integration.
   - **ArduinoJson** – To handle JSON data for Telegram API communication.
   - **ESP32-CAM Camera Libraries** – Built-in libraries for capturing and processing images.
3. **Telegram Bot**:
   - Use BotFather on Telegram to create a bot and obtain a bot token and chat ID.
4. **Programming Language**:
   - C++ (Arduino sketch).
5. **Optional Tools**:
   - OpenCV (Python) for prototyping image processing algorithms on a computer before porting to Arduino (simplified for ESP32-CAM).

---

### Algorithm for Detecting Washing Machine Status
Since the Maytag MHW8630HW has a panel light that indicates when the machine is on, you can use the camera to detect this light. The algorithm will process images to determine if the light is on or off, indicating the machine’s status.

#### Detection Algorithm
1. **Image Capture**:
   - Periodically capture images of the washing machine’s control panel using the ESP32-CAM.
2. **Region of Interest (ROI) Selection**:
   - Define a specific area in the image where the panel light is located (e.g., a rectangular region around the power indicator).
3. **Image Processing**:
   - **Grayscale Conversion**: Convert the captured image to grayscale to simplify processing.
   - **Thresholding**: Apply a brightness threshold to detect the presence of the light. The panel light will produce a bright spot when on, compared to a darker area when off.
   - **Pixel Intensity Analysis**: Calculate the average pixel intensity in the ROI. A high intensity indicates the light is on, while a low intensity indicates it’s off.
4. **State Machine**:
   - Track the machine’s state (ON or OFF) based on consecutive readings.
   - If the light is detected as ON for several cycles, assume the machine is running.
   - If the light transitions to OFF and remains off for a set period (e.g., 5 minutes), assume the wash cycle is complete.
5. **Debouncing**:
   - Implement a delay (e.g., 5 minutes) to confirm the machine has stopped, avoiding false notifications during pauses in the wash cycle (e.g., soaking or filling).
6. **Notification**:
   - When the machine is confirmed stopped, send a Telegram message (e.g., “Washing machine stopped! Time to hang up clothes.”).

#### Why Not Use More Complex Algorithms?
- Advanced algorithms like machine learning (e.g., CNNs for object detection) are overkill for this task and resource-intensive for the ESP32-CAM’s limited processing power.
- Simple thresholding is sufficient since the panel light is a clear binary indicator (ON/OFF).

---

### Implementation Guide
#### Step 1: Set Up the Telegram Bot
1. **Create a Telegram Bot**:
   - Open Telegram, search for **@BotFather**, and start a chat.
   - Send `/newbot`, name your bot (e.g., “WasherBot”), and get the **Bot Token**.
   - Send `/start` to your bot and get your **Chat ID** using a service like `@GetIDsBot` or by checking incoming messages in your code.
2. **Install Telegram on Your Phone**:
   - Ensure you can receive messages from your bot.

#### Step 2: Hardware Setup
1. **Position the ESP32-CAM**:
   - Mount the ESP32-CAM in a small enclosure or with adhesive tape, facing the washing machine’s control panel.
   - Ensure the camera has a clear view of the panel light (test with a sample photo).
   - Secure the setup to avoid movement, as this could affect ROI consistency.
2. **Power the ESP32-CAM**:
   - Connect a 5V USB power adapter or battery pack to the ESP32-CAM’s 5V pin.
   - Ensure a stable power source, as the camera and Wi-Fi consume significant power.
3. **Optional Light Sensor**:
   - If using a photoresistor, connect it to an analog pin on the ESP32-CAM (e.g., GPIO 4) with a voltage divider circuit (e.g., 10kΩ resistor to ground).

#### Step 3: Software Setup
1. **Install Arduino IDE**:
   - Download and install the Arduino IDE from [arduino.cc](https://www.arduino.cc/en/software).
2. **Add ESP32 Board Support**:
   - In Arduino IDE, go to **File > Preferences**, add the following URL to Additional Boards Manager URLs:
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/master/package_esp32_index.json
     ```
   - Go to **Tools > Board > Boards Manager**, search for “ESP32,” and install the ESP32 package.
3. **Install Libraries**:
   - Install **Universal Arduino Telegram Bot Library**:
     - Download from [GitHub](https://github.com/witnessmenow/Universal-Arduino-Telegram-Bot) and add via **Sketch > Include Library > Add .ZIP Library**.
   - Install **ArduinoJson**:
     - Go to **Sketch > Include Library > Manage Libraries**, search for “ArduinoJson,” and install version 6.x.x.
4. **Configure Wi-Fi**:
   - Ensure your ESP32-CAM can connect to your home Wi-Fi network (2.4GHz, as 5GHz is not supported).

#### Step 4: Write the Arduino Code
Below is a sample Arduino sketch for the ESP32-CAM to detect the panel light and send Telegram notifications. This code assumes you’ve identified the ROI coordinates for the panel light.

```cpp
#include <WiFi.h>
#include <UniversalTelegramBot.h>
#include <ArduinoJson.h>
#include "esp_camera.h"

// Wi-Fi credentials
#define WIFI_SSID "your_wifi_ssid"
#define WIFI_PASSWORD "your_wifi_password"

// Telegram Bot credentials
#define BOT_TOKEN "your_bot_token"
#define CHAT_ID "your_chat_id"

// Camera configuration (for ESP32-CAM)
#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22

WiFiClientSecure client;
UniversalTelegramBot bot(BOT_TOKEN, client);

#define ROI_X 100 // Adjust based on camera view (x-coordinate of ROI)
#define ROI_Y 100 // y-coordinate of ROI
#define ROI_WIDTH 50 // Width of ROI
#define ROI_HEIGHT 50 // Height of ROI
#define THRESHOLD 150 // Brightness threshold (0-255)
#define STOP_DELAY 300000 // 5 minutes in milliseconds

bool machineRunning = false;
unsigned long lastOnTime = 0;

void setup() {
  Serial.begin(115200);

  // Initialize camera
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_GRAYSCALE; // Grayscale for simplicity
  config.frame_size = FRAMESIZE_QVGA; // 320x240
  config.jpeg_quality = 12;
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  // Configure Telegram client
  client.setInsecure(); // For simplicity; consider proper SSL in production
}

void loop() {
  // Capture image
  camera_fb_t *fb = esp_camera_framebuffer_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  // Calculate average brightness in ROI
  uint32_t totalBrightness = 0;
  uint16_t pixelCount = 0;
  for (int y = ROI_Y; y < ROI_Y + ROI_HEIGHT; y++) {
    for (int x = ROI_X; x < ROI_X + ROI_WIDTH; x++) {
      if (x < fb->width && y < fb->height) {
        totalBrightness += fb->buf[y * fb->width + x];
        pixelCount++;
      }
    }
  }
  esp_camera_framebuffer_return(fb);

  float avgBrightness = pixelCount > 0 ? (float)totalBrightness / pixelCount : 0;

  // State machine
  if (avgBrightness > THRESHOLD) {
    if (!machineRunning) {
      machineRunning = true;
      Serial.println("Machine is ON");
    }
    lastOnTime = millis();
  } else {
    if (machineRunning && (millis() - lastOnTime > STOP_DELAY)) {
      machineRunning = false;
      Serial.println("Machine stopped");
      bot.sendMessage(CHAT_ID, "Washing machine stopped! Time to hang up clothes.", "");
    }
  }

  delay(10000); // Check every 10 seconds
}
```

#### Step 5: Customize the Code
1. **Update Credentials**:
   - Replace `your_wifi_ssid`, `your_wifi_password`, `your_bot_token`, and `your_chat_id` with your actual values.
2. **Tune ROI and Threshold**:
   - Capture a test image using the ESP32-CAM (modify the code to save an image to an SD card or stream it).
   - Determine the ROI coordinates (`ROI_X`, `ROI_Y`, `ROI_WIDTH`, `ROI_HEIGHT`) by analyzing the image to focus on the panel light.
   - Adjust `THRESHOLD` based on test images (e.g., brighter when ON, darker when OFF).
3. **Adjust `STOP_DELAY`**:
   - Set to 300000 (5 minutes) to avoid false notifications during cycle pauses.

#### Step 6: Test and Deploy
1. **Upload the Code**:
   - Connect the ESP32-CAM to your computer via a USB-to-serial adapter (e.g., FTDI module).
   - Select **ESP32 Wrover Module** in Arduino IDE and upload the sketch.
2. **Test the System**:
   - Start the washing machine and monitor the Serial Monitor for state changes.
   - Verify Telegram notifications when the machine stops.
3. **Fine-Tune**:
   - Adjust ROI, threshold, or delay if false positives/negatives occur.
4. **Permanent Installation**:
   - Secure the ESP32-CAM in its enclosure and ensure a stable power supply.

---

### Alternative Approach: Light Sensor
If camera-based detection is too complex or unreliable (e.g., due to ambient light), use a photoresistor:
- **Setup**: Attach a photoresistor to the panel light (e.g., with tape) and connect it to an analog pin.
- **Code Modification**: Replace image processing with analog readings:
  ```cpp
  int lightValue = analogRead(A0); // Photoresistor on GPIO 4
  if (lightValue > 500) { // Adjust threshold
    machineRunning = true;
    lastOnTime = millis();
  } else if (machineRunning && (millis() - lastOnTime > STOP_DELAY)) {
    machineRunning = false;
    bot.sendMessage(CHAT_ID, "Washing machine stopped! Time to hang up clothes.", "");
  }
  ```
- **Pros**: Simpler, less resource-intensive.
- **Cons**: Requires physical attachment to the light, less flexible.

---

### Notes
- **Power Consumption**: The ESP32-CAM consumes significant power when using the camera and Wi-Fi. Ensure a reliable power source.
- **Ambient Light**: Camera-based detection may be affected by room lighting. Test in various conditions or use a light sensor for robustness.
- **Security**: The sample code uses `setInsecure()` for simplicity. For production, configure proper SSL certificates for Telegram communication.
- **References**: This approach is inspired by projects like the ESP32-CAM Telegram security system and laundry monitors using vibration sensors, adapted for light-based detection.[](https://www.instructables.com/Home-Security-System-Using-ESP32-CAM-and-Telegram-/)[](https://www.instructables.com/Arduino-Washer-Dryer-Alert-Push-Notification-to-Ph/)

---

### Troubleshooting
- **Camera Fails to Initialize**: Check wiring, ensure sufficient power, and verify camera configuration.
- **Wi-Fi Connection Issues**: Confirm 2.4GHz Wi-Fi and correct credentials.
- **No Telegram Messages**: Verify bot token and chat ID, check Serial Monitor for errors.
- **False Notifications**: Adjust `THRESHOLD` or `STOP_DELAY` to account for cycle pauses.

This solution leverages the ESP32-CAM’s capabilities for a cost-effective, non-invasive way to monitor your washing machine and notify you via Telegram. Let me know if you need help with specific steps or debugging!
