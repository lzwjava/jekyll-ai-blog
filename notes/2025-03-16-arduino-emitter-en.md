---
audio: false
generated: true
lang: en
layout: post
title: Building a Common-Emitter Amplifier using an Arduino
translated: false
type: note
---

Building a Common-Emitter (CE) Amplifier using an Arduino is an interesting project, but it’s worth clarifying the roles: the Arduino itself won’t act as the amplifier (it’s a digital microcontroller), but it can serve as a signal source or measurement tool for a CE amplifier circuit built with a bipolar junction transistor (BJT). A CE amplifier is a classic analog circuit that uses an NPN or PNP transistor to amplify a small input signal, offering moderate voltage gain and current gain.

Here, I’ll guide you through designing a basic NPN-based CE amplifier, using the Arduino to generate an input signal (via PWM) and measure the output. This setup will demonstrate amplification while leveraging Arduino’s capabilities.

---

### **Overview of a Common-Emitter Amplifier**

- **Purpose:** Amplifies a small AC signal (e.g., audio or a sine wave).
- **Key Features:**
  - Transistor operates in the active region.
  - Input signal applied to the base, output taken from the collector.
  - Voltage gain determined by resistor ratios and transistor properties.
- **Components:**
  - NPN transistor (e.g., 2N3904 or BC547)
  - Resistors (for biasing and load)
  - Capacitors (for coupling AC signals)
  - Arduino (signal source and measurement)

---

### **Step 1: Design the Circuit**

#### **Components Needed**

- NPN transistor (e.g., 2N3904)
- Resistors: R1 = 47kΩ, R2 = 10kΩ (biasing), RC = 1kΩ (collector), RE = 220Ω (emitter)
- Capacitors: C1 = 10µF (input coupling), C2 = 10µF (output coupling), CE = 100µF (emitter bypass, optional for higher gain)
- Arduino (e.g., Uno)
- Breadboard, jumper wires
- Power supply (Arduino’s 5V pin or external 9V, adjusted as needed)

#### **Circuit Schematic**

```
Vcc (5V) ---- R1 ----+---- RC ---- Collector (C)
             47kΩ     |     1kΩ          |
                      |                  |
Base (B) --- C1 -----+                  |
            10µF     |                  |
Arduino PWM (Pin 9)  R2                 |
                     10kΩ              Output --- C2 ---- To Arduino A0
                      |                  |         10µF
                      |                  |
                      +---- RE ---- Emitter (E) --- CE (optional) --- GND
                           220Ω                   100µF
                      |
                     GND
```

- **Biasing (R1, R2):** Sets the transistor’s operating point.
- **RC:** Collector resistor for output signal.
- **RE:** Emitter resistor for stability.
- **C1, C2:** Block DC, pass AC signals.
- **CE (optional):** Bypasses RE for higher AC gain.

#### **Operating Point**

- Goal: Bias the transistor in the active region (e.g., VCE ≈ 2.5V for 5V supply).
- Voltage divider (R1, R2): \\( V_B = V_{CC} \cdot \frac{R2}{R1 + R2} = 5 \cdot \frac{10k}{47k + 10k} \approx 0.88V \\).
- \\( V_E = V_B - V_{BE} \approx 0.88 - 0.7 = 0.18V \\).
- \\( I_E = \frac{V_E}{RE} = \frac{0.18}{220} \approx 0.82 \, \text{mA} \\).
- \\( V_C = V_{CC} - I_C \cdot RC \approx 5 - 0.82 \cdot 1k \approx 4.18V \\).
- \\( V_{CE} = V_C - V_E \approx 4.18 - 0.18 = 4V \\) (good for 5V supply).

---

### **Step 2: Use Arduino as Signal Source**

#### **Arduino’s Role**

- Generate a small AC signal using PWM (Pulse Width Modulation) on a pin like 9 (which supports PWM).
- Filter the PWM to approximate a sine wave with a simple RC low-pass filter (optional).

#### **Code to Generate a Signal**

```cpp
const int pwmPin = 9; // PWM output pin

void setup() {
  pinMode(pwmPin, OUTPUT);
  // Set PWM frequency (optional, default is ~490 Hz)
}

void loop() {
  // Simulate a sine wave with PWM (0-255 range)
  for (int i = 0; i < 360; i += 10) {
    float sineValue = sin(radians(i)); // Sine wave from -1 to 1
    int pwmValue = 127 + 127 * sineValue; // Scale to 0-255
    analogWrite(pwmPin, pwmValue);
    delay(10); // Adjust for frequency (e.g., ~100 Hz here)
  }
}
```

- **Output:** ~0–5V PWM signal, centered at 2.5V with ~2.5V peak-to-peak.
- **C1:** Removes the DC offset, passing only the AC component (~1.25V peak) to the base.

#### **Optional Filter**

Add a 1kΩ resistor and 0.1µF capacitor in series from Pin 9 to GND, tapping the signal before C1, to smooth PWM into a rough sine wave.

---

### **Step 3: Measure the Output**

#### **Arduino Measurement**

- Connect the amplifier output (after C2) to A0.
- Use the Arduino to read the amplified signal and display it via Serial Monitor.

#### **Code to Measure and Display**

```cpp
const int inputPin = A0; // Measure output here

void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(inputPin); // 0-1023 maps to 0-5V
  float voltage = sensorValue * (5.0 / 1023.0);
  Serial.print("Output Voltage (V): ");
  Serial.println(voltage);
  delay(100); // Adjust sampling rate
}
```

#### **Expected Gain**

- Voltage gain \\( A_v = -\frac{RC}{RE} = -\frac{1k}{220} \approx -4.5 \\) (negative due to phase inversion).
- Input: ~1.25V peak (after coupling).
- Output: ~4.5 × 1.25 = 5.625V peak (but clipped at 5V due to supply limit).

---

### **Step 4: Build and Test**

#### **Assembly**

1. Wire the circuit on a breadboard as per the schematic.
2. Upload the signal generation code to Arduino and connect Pin 9 to C1.
3. Power the circuit via 5V from Arduino (or use 9V with adjusted resistors).
4. Upload the measurement code and open Serial Monitor (9600 baud).

#### **Verification**

- **Input Signal:** ~1–2V peak-to-peak after C1 (use a multimeter or oscilloscope if available).
- **Output Signal:** Should be larger (e.g., 4–5V peak-to-peak) and inverted.
- Check VCE (~2–4V) with a multimeter to ensure active region operation.

---

### **Tips and Troubleshooting**

- **Gain Too Low:** Add CE (100µF) across RE to boost AC gain (removes RE’s degeneration).
- **Clipping:** If output exceeds 5V, reduce input amplitude (adjust PWM range) or increase Vcc (e.g., 9V external supply).
- **Noise:** PWM is square-ish; a better sine wave (via external generator or filter) improves results.
- **Transistor Specs:** Ensure 2N3904 handles currents (Ic < 200mA, safe here).

This setup demonstrates a CE amplifier’s core behavior—voltage amplification—while integrating Arduino for signal generation and analysis. Want to tweak the gain, add a speaker for audio, or refine the signal? Let me know!
