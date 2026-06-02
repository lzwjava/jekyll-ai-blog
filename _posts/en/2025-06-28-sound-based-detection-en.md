---
audio: false
generated: true
lang: en
layout: post
title: Sound-Based Detection for Maytag Washing Machine
translated: false
type: note
---

Using sound to detect when your Maytag MHW8630HW washing machine stops is a viable alternative to the camera-based approach. By placing a sound sensor close to the washing machine, you can monitor the noise generated during operation (e.g., motor hum, water flow, or drum rotation) and detect when it stops, indicating the end of the wash cycle. Below, I’ll explain how to adapt the previous project to use a sound sensor instead of a camera, focusing on the hardware, algorithm, and code changes while keeping the Telegram notification system.

---

### Tech Stack

#### Hardware

1. **Arduino Board**:
   - **ESP32-CAM** (still usable) – Retains Wi-Fi for Telegram integration, though the camera is not needed.
   - Alternative: **ESP8266 NodeMCU** or **Arduino Uno** with an ESP8266 module for Wi-Fi (simpler if you don’t need the camera).
2. **Sound Sensor**:
   - **KY-038 Microphone Sound Sensor** or similar – Affordable, detects sound levels via an analog output.
   - Alternative: **MAX9814 Electret Microphone Amplifier** – More sensitive, with adjustable gain for better detection.
3. **Power Supply**:
   - 5V USB power adapter or battery pack for the ESP32 or other board.
4. **Mounting**:
   - Place the sound sensor close to the washing machine (e.g., taped to the side or top) where it can detect operational sounds but avoid direct water exposure.
   - Use a small enclosure to protect the sensor and board.
5. **Wi-Fi Router**:
   - For internet connectivity to send Telegram notifications.

#### Software

- **Arduino IDE**: For programming the ESP32 or other board.
- **Libraries**:
  - **Universal Arduino Telegram Bot Library** by Brian Lough – For Telegram integration.
  - **ArduinoJson** – For handling JSON data in Telegram API communication.
- **Telegram Bot**: Same as before, using BotFather to get a bot token and chat ID.
- **Programming Language**: C++ (Arduino sketch).

---

### Algorithm for Detecting Washing Machine Status with Sound

The sound sensor will detect the noise level produced by the washing machine. When the machine is running, it generates consistent sounds (e.g., motor, water, or drum). When it stops, the sound level drops significantly. The algorithm processes these sound levels to determine the machine’s status.

#### Detection Algorithm

1. **Sound Sampling**:
   - Continuously read the analog output from the sound sensor to measure noise levels.
2. **Signal Processing**:
   - **Averaging**: Calculate the average sound level over a short window (e.g., 1-2 seconds) to smooth out transient noises (e.g., a door slam).
   - **Thresholding**: Compare the average sound level to a predefined threshold. A high level indicates the machine is running, while a low level suggests it’s stopped.
3. **State Machine**:
   - Track the machine’s state (ON or OFF) based on sound levels.
   - If the sound level exceeds the threshold for several cycles, assume the machine is running.
   - If the sound level drops below the threshold and remains low for a set period (e.g., 5 minutes), assume the wash cycle is complete.
4. **Debouncing**:
   - Implement a delay (e.g., 5 minutes) to confirm the machine has stopped, avoiding false notifications during quiet phases (e.g., soaking or pauses in the cycle).
5. **Notification**:
   - When the machine is confirmed stopped, send a Telegram message (e.g., “Washing machine stopped! Time to hang up clothes.”).

#### Why Sound Detection?

- Sound detection is simpler than image processing, as it doesn’t require complex algorithms or high computational resources.
- It’s less sensitive to ambient light changes compared to camera-based detection.
- However, it may be affected by background noise (e.g., a loud TV), so placement and threshold tuning are critical.

---

### Implementation Guide

#### Step 1: Set Up the Telegram Bot

- Follow the same steps as in the original guide:
  - Create a bot using **@BotFather** to get a **Bot Token**.
  - Get your **Chat ID** using **@GetIDsBot** or by checking incoming messages.
  - Ensure Telegram is set up on your phone to receive notifications.

#### Step 2: Hardware Setup

1. **Choose a Sound Sensor**:
   - **KY-038**: Provides an analog output (0-1023 for ESP32’s 10-bit ADC) proportional to sound intensity. It also has a digital output, but analog is better for nuanced detection.
   - **MAX9814**: More sensitive, with adjustable gain via a potentiometer. Connect to an analog pin.
2. **Connect the Sound Sensor**:
   - For KY-038:
     - **VCC** to 5V (or 3.3V, depending on the board).
     - **GND** to GND.
     - **Analog Out (A0)** to an analog pin on the ESP32 (e.g., GPIO 4).
   - For MAX9814:
     - Similar connections, but adjust gain using the onboard potentiometer for optimal sensitivity.
3. **Position the Sensor**:
   - Place the sensor close to the washing machine (e.g., on the side or top) where it can detect motor or drum noise. Avoid areas with water exposure.
   - Test placement by monitoring sound levels during a wash cycle (use Serial Monitor to log values).
4. **Power the Board**:
   - Connect a 5V USB power adapter or battery pack to the ESP32 or other board.
   - Ensure stable power, as Wi-Fi communication requires consistent voltage.
5. **Mounting**:
   - Use a small enclosure or tape to secure the sensor and board, ensuring the microphone is exposed to capture sound.

#### Step 3: Software Setup

- **Arduino IDE**: Install as described in the original guide.
- **ESP32 Board Support**: Add the ESP32 board package via the Boards Manager (same URL as before).
- **Libraries**:
  - Install **Universal Arduino Telegram Bot Library** and **ArduinoJson** as described.
- **Wi-Fi**: Ensure the board can connect to your 2.4GHz Wi-Fi network.

#### Step 4: Write the Arduino Code

Below is a sample Arduino sketch for the ESP32 (or ESP8266) to detect sound levels and send Telegram notifications. This assumes a KY-038 sound sensor connected to GPIO 4.

```cpp
#include <WiFi.h>
#include <UniversalTelegramBot.h>
#include <ArduinoJson.h>

// Wi-Fi credentials
#define WIFI_SSID "your_wifi_ssid"
#define WIFI_PASSWORD "your_wifi_password"

// Telegram Bot credentials
#define BOT_TOKEN "your_bot_token"
#define CHAT_ID "your_chat_id"

// Sound sensor pin
#define SOUND_PIN 4 // GPIO 4 for analog input

// Sound detection parameters
#define SOUND_THRESHOLD 300 // Adjust based on testing (0-1023)
#define SAMPLE_WINDOW 2000 // 2 seconds for averaging
#define STOP_DELAY 300000 // 5 minutes in milliseconds

WiFiClientSecure client;
UniversalTelegramBot bot(BOT_TOKEN, client);

bool machineRunning = false;
unsigned long lastOnTime = 0;

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  // Configure Telegram client
  client.setInsecure(); // For simplicity; consider proper SSL in production

  // Set up sound sensor pin
  pinMode(SOUND_PIN, INPUT);
}

void loop() {
  // Sample sound level over a window
  unsigned long startMillis = millis();
  uint32_t totalSound = 0;
  uint16_t sampleCount = 0;

  while (millis() - startMillis < SAMPLE_WINDOW) {
    totalSound += analogRead(SOUND_PIN);
    sampleCount++;
    delay(10); // Small delay between samples
  }

  float avgSound = sampleCount > 0 ? (float)totalSound / sampleCount : 0;
  Serial.print("Average sound level: ");
  Serial.println(avgSound);

  // State machine
  if (avgSound > SOUND_THRESHOLD) {
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
2. **Tune `SOUND_THRESHOLD`**:
   - Run the washing machine and monitor sound levels via the Serial Monitor (`Serial.println(analogRead(SOUND_PIN));`).
   - Set `SOUND_THRESHOLD` to a value above ambient noise but below the machine’s operational noise (e.g., 200-500, depending on your setup).
3. **Adjust `SAMPLE_WINDOW`**:
   - A 2-second window (`2000` ms) smooths out transient noises. Increase if background noise causes false readings.
4. **Adjust `STOP_DELAY`**:
   - Set to `300000` (5 minutes) to avoid false notifications during quiet phases like soaking.

#### Step 6: Test and Deploy

1. **Upload the Code**:
   - Connect the ESP32 to your computer via a USB-to-serial adapter.
   - Select **ESP32 Wrover Module** (or **NodeMCU** for ESP8266) in Arduino IDE and upload the sketch.
2. **Test the System**:
   - Start the washing machine and monitor the Serial Monitor for sound levels and state changes.
   - Verify Telegram notifications when the machine stops.
3. **Fine-Tune**:
   - Adjust `SOUND_THRESHOLD` or `STOP_DELAY` if false positives/negatives occur.
   - Test in different conditions (e.g., with background noise) to ensure reliability.
4. **Permanent Installation**:
   - Secure the sensor and board in an enclosure near the machine, ensuring the microphone is exposed but protected from water.

---

### Advantages of Sound Detection

- **Simpler Processing**: No image processing, reducing computational load on the ESP32.
- **Cost-Effective**: Sound sensors like KY-038 are inexpensive (often under $5).
- **Non-Invasive**: No need to attach anything directly to the machine’s panel light.

### Challenges and Mitigations

- **Background Noise**: Household noises (e.g., TV, talking) may interfere. Mitigate by:
  - Placing the sensor close to the machine’s motor or drum.
  - Tuning `SOUND_THRESHOLD` to ignore ambient noise.
  - Using a directional microphone or adjusting gain on MAX9814.
- **Quiet Phases**: Some wash cycles have pauses (e.g., soaking). The `STOP_DELAY` ensures notifications are sent only after prolonged silence.
- **Water Exposure**: Ensure the sensor is in a water-resistant enclosure, as washing machines may have splashes or humidity.

### Optional Enhancements

- **Frequency Analysis**: If background noise is a persistent issue, analyze sound frequencies (e.g., motor hum at 50-200 Hz) using a Fast Fourier Transform (FFT) library like `arduinoFFT`. This requires more processing power and may not be feasible on a basic ESP32 without optimization.
- **Dual Sensors**: Combine sound and vibration sensors (e.g., SW-420) for redundancy. If both indicate the machine is off, confidence in the detection increases.
- **Battery Power**: For portability, use a rechargeable LiPo battery with a charging module (e.g., TP4056) instead of a USB adapter.

---

### Troubleshooting

- **No Sound Detection**: Check sensor wiring, test with Serial Monitor, and ensure the sensor is close to the machine’s noise source.
- **False Notifications**: Increase `STOP_DELAY` or adjust `SOUND_THRESHOLD` to filter out background noise or cycle pauses.
- **Wi-Fi Issues**: Verify 2.4GHz Wi-Fi credentials and signal strength near the machine.
- **No Telegram Messages**: Confirm bot token and chat ID, check Serial Monitor for errors.

This sound-based approach is simpler and more robust in varying light conditions compared to the camera-based method, making it ideal for a washing machine monitor. Let me know if you need help with specific steps, sensor calibration, or integrating additional features!
