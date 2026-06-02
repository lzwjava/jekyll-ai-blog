---
audio: false
generated: true
lang: en
layout: post
title: Kirchhoff's Laws with Arduino
translated: false
type: note
---

Using an Arduino to verify Kirchhoff’s Laws—specifically Kirchhoff’s Current Law (KCL) and Kirchhoff’s Voltage Law (KVL)—is a great way to blend electronics theory with hands-on experimentation. KCL states that the total current entering a junction equals the total current leaving it, while KVL states that the sum of voltage drops around a closed loop equals the supplied voltage. Here’s how you can design simple circuits and use an Arduino to measure currents and voltages to confirm these laws.

Since Arduino can’t directly measure current, we’ll infer it by measuring voltage across resistors (using Ohm’s Law: \\( I = V/R \\)), and it can measure voltage via its analog pins (0–5V range). Below, I’ll outline two experiments—one for KCL and one for KVL—with step-by-step instructions, wiring, and code.

---

### **Experiment 1: Verifying Kirchhoff’s Current Law (KCL)**

#### **Objective**

Demonstrate that the current entering a node equals the current leaving it.

#### **Circuit Setup**

- **Components:**
  - Arduino (e.g., Uno)
  - 3 resistors (e.g., R1 = 330Ω, R2 = 470Ω, R3 = 680Ω)
  - Breadboard and jumper wires
  - 5V power source (Arduino’s 5V pin)
- **Wiring:**
  - Connect Arduino 5V to a node (call it Node A).
  - From Node A, connect R1 to GND (branch 1).
  - From Node A, connect R2 to GND (branch 2, parallel with R1).
  - From Node A, connect R3 to GND (branch 3, parallel with R1 and R2).
  - Use Arduino analog pins to measure voltage across each resistor:
    - A0 across R1 (one probe at Node A, other at GND).
    - A1 across R2.
    - A2 across R3.
- **Note:** GND is the common reference point.

#### **Theory**

- Total current from 5V to Node A (\\( I_{in} \\)) splits into \\( I_1 \\), \\( I_2 \\), and \\( I_3 \\) through R1, R2, and R3.
- KCL: \\( I_{in} = I_1 + I_2 + I_3 \\).
- Measure voltage across each resistor, then calculate current: \\( I = V/R \\).

#### **Arduino Code**

```cpp
void setup() {
  Serial.begin(9600); // Start serial communication
}

void loop() {
  // Read voltages (0-1023 maps to 0-5V)
  int sensorValue1 = analogRead(A0); // Voltage across R1
  int sensorValue2 = analogRead(A1); // Voltage across R2
  int sensorValue3 = analogRead(A2); // Voltage across R3

  // Convert to voltage (5V reference, 10-bit ADC)
  float V1 = sensorValue1 * (5.0 / 1023.0);
  float V2 = sensorValue2 * (5.0 / 1023.0);
  float V3 = sensorValue3 * (5.0 / 1023.0);

  // Resistor values (in ohms)
  float R1 = 330.0;
  float R2 = 470.0;
  float R3 = 680.0;

  // Calculate currents (I = V/R)
  float I1 = V1 / R1;
  float I2 = V2 / R2;
  float I3 = V3 / R3;

  // Total current entering node (assuming Vsource = 5V)
  float totalResistance = 1.0 / ((1.0/R1) + (1.0/R2) + (1.0/R3)); // Parallel
  float Iin = 5.0 / totalResistance;

  // Output results
  Serial.print("I1 (mA): "); Serial.println(I1 * 1000);
  Serial.print("I2 (mA): "); Serial.println(I2 * 1000);
  Serial.print("I3 (mA): "); Serial.println(I3 * 1000);
  Serial.print("Iin (mA): "); Serial.println(Iin * 1000);
  Serial.print("Sum of I1+I2+I3 (mA): "); Serial.println((I1 + I2 + I3) * 1000);
  Serial.println("---");

  delay(2000); // Wait 2 seconds
}
```

#### **Verification**

- Open the Serial Monitor (Ctrl+Shift+M in Arduino IDE, set to 9600 baud).
- Compare \\( I_{in} \\) (calculated from total resistance) to \\( I_1 + I_2 + I_3 \\). They should be approximately equal, verifying KCL.
- Small discrepancies may arise from resistor tolerances or Arduino ADC precision.

---

### **Experiment 2: Verifying Kirchhoff’s Voltage Law (KVL)**

#### **Objective**

Show that the sum of voltage drops around a closed loop equals the supply voltage.

#### **Circuit Setup**

- **Components:**
  - Arduino
  - 2 resistors (e.g., R1 = 330Ω, R2 = 470Ω)
  - Breadboard and jumper wires
  - 5V power source (Arduino’s 5V pin)
- **Wiring:**
  - Connect 5V to R1.
  - Connect R1 to R2.
  - Connect R2 to GND.
  - Measure voltages:
    - A0 across the whole loop (5V to GND) to confirm supply voltage.
    - A1 across R1 (5V to junction of R1 and R2).
    - A2 across R2 (junction to GND).
- **Note:** Use a voltage divider setup; ensure voltages don’t exceed 5V (Arduino’s limit).

#### **Theory**

- KVL: \\( V_{source} = V_{R1} + V_{R2} \\).
- Measure each voltage drop and check if they sum to the source voltage (5V).

#### **Arduino Code**

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  // Read voltages
  int sensorValueSource = analogRead(A0); // Across 5V to GND
  int sensorValueR1 = analogRead(A1);     // Across R1
  int sensorValueR2 = analogRead(A2);     // Across R2

  // Convert to voltage
  float Vsource = sensorValueSource * (5.0 / 1023.0);
  float VR1 = sensorValueR1 * (5.0 / 1023.0);
  float VR2 = sensorValueR2 * (5.0 / 1023.0);

  // Output results
  Serial.print("Vsource (V): "); Serial.println(Vsource);
  Serial.print("VR1 (V): "); Serial.println(VR1);
  Serial.print("VR2 (V): "); Serial.println(VR2);
  Serial.print("VR1 + VR2 (V): "); Serial.println(VR1 + VR2);
  Serial.println("---");

  delay(2000);
}
```

#### **Verification**

- In the Serial Monitor, check that \\( V_{source} \approx V_{R1} + V_{R2} \\).
- For R1 = 330Ω and R2 = 470Ω in series, expect \\( V_{R1} \approx 2.1V \\) and \\( V_{R2} \approx 2.9V \\) (based on voltage divider: \\( V_{R1} = 5 \cdot \frac{R1}{R1+R2} \\)), summing to ~5V.

---

### **Tips and Considerations**

- **Precision:** Arduino’s 10-bit ADC (0–1023) has a resolution of ~4.9mV, so expect minor errors. Use a multimeter to cross-check if needed.
- **Safety:** Keep voltages below 5V and currents low to avoid damaging the Arduino.
- **Scaling:** For more complex circuits, add more resistors or use external sensors (e.g., INA219 for direct current measurement).
- **Debugging:** If results don’t match, verify resistor values, connections, and GND consistency.

These experiments simplify real-world conditions but effectively demonstrate Kirchhoff’s Laws. Want to tweak these setups or need help with a specific part (like wiring or code)? Let me know!
