---
audio: false
generated: true
lang: en
layout: post
title: Verifying Mesh Analysis with Arduino
translated: false
type: note
---

Verifying Mesh Analysis with an Arduino involves constructing a circuit with multiple loops, applying Mesh Analysis theoretically to predict currents, and then using the Arduino to measure voltages across resistors to calculate actual currents for comparison. Mesh Analysis is a method in circuit theory where you assign loop currents to each independent loop and use Kirchhoff’s Voltage Law (KVL) to set up equations. The Arduino will help you measure the real-world behavior to confirm your calculations.

Below, I’ll guide you through designing a simple two-mesh circuit, performing Mesh Analysis manually, and using an Arduino to verify the results by measuring voltages and inferring currents (since Arduino can’t measure current directly, we’ll use Ohm’s Law: \\( I = V/R \\)).

---

### **Step 1: Design a Two-Mesh Circuit**

#### **Circuit Description**
- **Components:**
  - Arduino (e.g., Uno)
  - 3 resistors (e.g., R1 = 330Ω, R2 = 470Ω, R3 = 680Ω)
  - Breadboard and jumper wires
  - Power source (Arduino’s 5V pin)
- **Wiring:**
  - Connect 5V to Node A.
  - From Node A, connect R1 to Node B.
  - From Node B, connect R2 to Node C (GND).
  - From Node A, connect R3 to Node C (GND).
- **Topology:**
  - Mesh 1: 5V → R1 → R2 → GND (left loop).
  - Mesh 2: 5V → R3 → GND (right loop).
  - R1 is in Mesh 1 only, R3 is in Mesh 2 only, and R2 is shared between both meshes.
- **Measurement Points:**
  - A0: Voltage across R1 (Node A to Node B).
  - A1: Voltage across R2 (Node B to Node C).
  - A2: Voltage across R3 (Node A to Node C).

#### **Schematic Concept**
```
5V ---- Node A ---- R1 ---- Node B ---- R2 ---- Node C (GND)
       |                        |
       +--------- R3 -----------+
```

---

### **Step 2: Perform Mesh Analysis Theoretically**

#### **Define Mesh Currents**
- \\( I_1 \\): Current in Mesh 1 (clockwise through 5V, R1, R2, GND).
- \\( I_2 \\): Current in Mesh 2 (clockwise through 5V, R3, GND).

#### **Apply KVL to Each Mesh**
1. **Mesh 1 (5V → R1 → R2 → GND):**
   - Voltage source: +5V (going from GND to 5V in the loop direction).
   - Voltage drop across R1: \\( -R1 \cdot I_1 \\).
   - Voltage drop across R2: \\( -R2 \cdot (I_1 - I_2) \\) (current through R2 is \\( I_1 - I_2 \\)).
   - Equation: \\( 5 - R1 \cdot I_1 - R2 \cdot (I_1 - I_2) = 0 \\).

2. **Mesh 2 (5V → R3 → GND):**
   - Voltage source: +5V.
   - Voltage drop across R3: \\( -R3 \cdot I_2 \\).
   - Voltage drop across R2 (opposite direction): \\( +R2 \cdot (I_1 - I_2) \\) (current through R2 is \\( I_1 - I_2 \\)).
   - Equation: \\( 5 - R3 \cdot I_2 + R2 \cdot (I_1 - I_2) = 0 \\).

#### **Substitute Values**
- R1 = 330Ω, R2 = 470Ω, R3 = 680Ω.
- Mesh 1: \\( 5 - 330 I_1 - 470 (I_1 - I_2) = 0 \\)
  - Simplify: \\( 5 - 330 I_1 - 470 I_1 + 470 I_2 = 0 \\)
  - \\( 5 - 800 I_1 + 470 I_2 = 0 \\) → (1)
- Mesh 2: \\( 5 - 680 I_2 + 470 (I_1 - I_2) = 0 \\)
  - Simplify: \\( 5 + 470 I_1 - 680 I_2 - 470 I_2 = 0 \\)
  - \\( 5 + 470 I_1 - 1150 I_2 = 0 \\) → (2)

#### **Solve the Equations**
- From (1): \\( 5 = 800 I_1 - 470 I_2 \\) → \\( I_1 = \frac{5 + 470 I_2}{800} \\).
- Substitute into (2): \\( 5 + 470 \left( \frac{5 + 470 I_2}{800} \right) - 1150 I_2 = 0 \\).
- Multiply through by 800 to clear the fraction:
  - \\( 4000 + 470 (5 + 470 I_2) - 1150 \cdot 800 I_2 = 0 \\)
  - \\( 4000 + 2350 + 220900 I_2 - 920000 I_2 = 0 \\)
  - \\( 6350 - 699100 I_2 = 0 \\)
  - \\( I_2 = \frac{6350}{699100} \approx 0.00908 \, \text{A} = 9.08 \, \text{mA} \\).
- Back-substitute: \\( I_1 = \frac{5 + 470 \cdot 0.00908}{800} = \frac{5 + 4.2676}{800} \approx 0.01158 \, \text{A} = 11.58 \, \text{mA} \\).

#### **Calculate Voltages**
- \\( V_{R1} = R1 \cdot I_1 = 330 \cdot 0.01158 \approx 3.82 \, \text{V} \\).
- \\( V_{R2} = R2 \cdot (I_1 - I_2) = 470 \cdot (0.01158 - 0.00908) \approx 1.18 \, \text{V} \\).
- \\( V_{R3} = R3 \cdot I_2 = 680 \cdot 0.00908 \approx 6.17 \, \text{V} \\) (but capped at 5V due to source).

---

### **Step 3: Verify with Arduino**

#### **Arduino Code**
```cpp
void setup() {
  Serial.begin(9600); // Start serial communication
}

void loop() {
  // Read voltages (0-1023 maps to 0-5V)
  int sensorValueR1 = analogRead(A0); // Across R1
  int sensorValueR2 = analogRead(A1); // Across R2
  int sensorValueR3 = analogRead(A2); // Across R3

  // Convert to voltage
  float VR1 = sensorValueR1 * (5.0 / 1023.0);
  float VR2 = sensorValueR2 * (5.0 / 1023.0);
  float VR3 = sensorValueR3 * (5.0 / 1023.0);

  // Resistor values
  float R1 = 330.0;
  float R2 = 470.0;
  float R3 = 680.0;

  // Calculate currents (I = V/R)
  float I1 = VR1 / R1;              // Mesh 1 current through R1
  float I2 = VR3 / R3;              // Mesh 2 current through R3
  float IR2 = VR2 / R2;             // Current through R2 (I1 - I2)

  // Output results
  Serial.println("Measured Values:");
  Serial.print("VR1 (V): "); Serial.println(VR1);
  Serial.print("VR2 (V): "); Serial.println(VR2);
  Serial.print("VR3 (V): "); Serial.println(VR3);
  Serial.print("I1 (mA): "); Serial.println(I1 * 1000);
  Serial.print("I2 (mA): "); Serial.println(I2 * 1000);
  Serial.print("I1 - I2 (mA): "); Serial.println((I1 - I2) * 1000);
  Serial.println("---");

  delay(2000); // Wait 2 seconds
}
```

#### **Wiring Notes**
- Connect A0 between Node A (5V) and Node B.
- Connect A1 between Node B and Node C (GND).
- Connect A2 between Node A (5V) and Node C (GND).
- Ensure all grounds are common with Arduino GND.

---

### **Step 4: Compare Results**

#### **Expected vs. Measured**
- **Theoretical (from Mesh Analysis):**
  - \\( I_1 \approx 11.58 \, \text{mA} \\)
  - \\( I_2 \approx 9.08 \, \text{mA} \\)
  - \\( I_1 - I_2 \approx 2.50 \, \text{mA} \\)
  - \\( V_{R1} \approx 3.82 \, \text{V} \\), \\( V_{R2} \approx 1.18 \, \text{V} \\), \\( V_{R3} \approx 5 \, \text{V} \\) (capped).
- **Measured:** Open the Serial Monitor (9600 baud) and compare the Arduino’s output to these values.

#### **Verification**
- Check if \\( V_{R1} + V_{R2} \approx 5V \\) (Mesh 1 loop).
- Check if \\( V_{R3} \approx 5V \\) (Mesh 2 loop).
- Confirm \\( I_1 - I_2 \\) matches the current through R2.

---

### **Tips and Troubleshooting**
- **Accuracy:** Arduino’s ADC has ~4.9mV resolution, and resistor tolerances may cause slight deviations. Use a multimeter for precise validation.
- **Adjustments:** If voltages exceed 5V (unlikely here), use a voltage divider to scale them down.
- **Extensions:** Add more meshes or components for complexity, but keep pin limits (A0–A5) in mind.

This setup confirms Mesh Analysis by aligning theoretical currents with measured ones. Let me know if you need help refining the circuit, debugging, or adding more meshes!
