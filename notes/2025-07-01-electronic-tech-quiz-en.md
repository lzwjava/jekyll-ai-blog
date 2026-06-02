---
audio: false
generated: true
lang: en
layout: post
title: Electronic Technology Self-Study Quiz
translated: false
type: note
---

Below is a sample quiz designed for a self-study exam based on the provided outline for *Fundamentals of Electronic Technology (III)*, edited by Wen Xidong and published by Economic Science Press. The quiz covers key concepts from analog electronics, digital electronics, and practical applications, tailored to test foundational understanding suitable for a self-study exam in China. The questions are a mix of multiple-choice, short-answer, and problem-solving formats to reflect typical exam styles.

---

### Sample Quiz: Fundamentals of Electronic Technology (III)

**Self-Study Exam**
**Instructions**: Answer all questions. Show your work for problem-solving questions. Each question is worth the indicated points. Total: 100 points.

---

#### Part I: Analog Electronics (40 points)

1. **Multiple Choice: Circuit Analysis (5 points)**
   Which of the following correctly describes Kirchhoff’s Voltage Law (KVL)?
   a) The sum of currents entering a node equals the sum of currents leaving it.
   b) The sum of voltage drops around a closed loop equals zero.
   c) The total resistance in a series circuit is the sum of individual resistances.
   d) The voltage across parallel branches is different.
   **Answer**: b) The sum of voltage drops around a closed loop equals zero.

2. **Short Answer: Amplifier Configurations (10 points)**
   Briefly explain the difference between the Common Emitter (CE) and Common Collector (CC) configurations of a BJT amplifier in terms of their input/output characteristics and typical applications.
   **Sample Answer**:
   - **CE Configuration**: High voltage gain, moderate input impedance, and inverted output. Used in applications requiring amplification, such as audio amplifiers.
   - **CC Configuration**: Unity voltage gain, high input impedance, low output impedance, non-inverted output. Often used as a buffer or impedance matching stage.

3. **Problem Solving: Operational Amplifiers (15 points)**
   An inverting op-amp circuit has a feedback resistor \\( R_f = 10 \, \text{k}\Omega \\) and an input resistor \\( R_{\text{in}} = 2 \, \text{k}\Omega \\). The input voltage is \\( V_{\text{in}} = 1 \, \text{V} \\).
   a) Calculate the output voltage \\( V_{\text{out}} \\).
   b) What is the gain of the circuit?
   **Solution**:
   a) For an inverting op-amp, \\( V_{\text{out}} = -\left(\frac{R_f}{R_{\text{in}}}\right) V_{\text{in}} = -\left(\frac{10 \, \text{k}\Omega}{2 \, \text{k}\Omega}\right) \cdot 1 \, \text{V} = -5 \, \text{V} \\).
   b) Gain \\( A = -\frac{R_f}{R_{\text{in}}} = -\frac{10}{2} = -5 \\).

4. **Multiple Choice: DC Power Supplies (10 points)**
   What is a key advantage of a switching regulator over a linear regulator?
   a) Lower cost
   b) Higher efficiency
   c) Simpler design
   d) Better voltage regulation
   **Answer**: b) Higher efficiency

---

#### Part II: Digital Electronics (40 points)

5. **Multiple Choice: Logic Gates (5 points)**
   Which logic gate produces an output of 1 only when all inputs are 0?
   a) AND
   b) OR
   c) NOR
   d) XOR
   **Answer**: c) NOR

6. **Short Answer: Combinational Logic (10 points)**
   Describe the function of a multiplexer and provide one practical application.
   **Sample Answer**: A multiplexer selects one of several input signals and forwards it to a single output based on select lines. It acts like a data selector. **Application**: Used in communication systems to route multiple data streams onto a single channel.

7. **Problem Solving: Sequential Logic (15 points)**
   Design a 3-bit binary up-counter using JK flip-flops. Provide the state table and describe the operation for one clock cycle starting from state 010 (binary 2).
   **Solution**:
   - **State Table**:
     | Present State (Q2 Q1 Q0) | Next State (Q2 Q1 Q0) | JK Inputs (J2 K2 | J1 K1 | J0 K0) |
     |-------------------------|-----------------------|-----------------------|
     | 010                     | 011                   | 0 0 | 0 0 | 1 1 |
   - **Operation**: From state 010, on the next clock cycle, Q0 toggles (0 → 1), Q1 and Q2 remain unchanged, resulting in 011 (binary 3). J0 = K0 = 1 to toggle Q0; others are don’t-care or 0.

8. **Multiple Choice: Programmable Logic Devices (10 points)**
   Which of the following is a characteristic of an FPGA?
   a) Fixed logic structure
   b) Reprogrammable logic blocks and interconnects
   c) Only supports analog circuits
   d) Cannot be programmed using HDL
   **Answer**: b) Reprogrammable logic blocks and interconnects

---

#### Part III: Practical Applications (20 points)

9. **Short Answer: Simulation Tools (10 points)**
   Explain the role of simulation tools like Multisim in the design of electronic circuits. Why are they useful for students learning *Fundamentals of Electronic Technology*?
   **Sample Answer**: Multisim allows students to design, simulate, and test circuits virtually before building them, reducing errors and costs. It helps visualize circuit behavior (e.g., voltage, current) and experiment with parameters, enhancing understanding of concepts like amplifiers and logic circuits.

10. **Problem Solving: Mixed-Signal Systems (10 points)**
    A temperature monitoring system uses an analog sensor outputting 0–5 V and a digital display via a 3-bit ADC. If the ADC’s reference voltage is 5 V, calculate the voltage step size and the digital output for a sensor reading of 3.75 V.
    **Solution**:
    - Step size = \\( \frac{V_{\text{ref}}}{2^n} = \frac{5 \, \text{V}}{2^3} = 0.625 \, \text{V} \\).
    - Digital output = \\( \text{floor}\left(\frac{3.75}{0.625}\right) = \text{floor}(6) = 110 \\) (binary).

---

### Notes for Self-Study Exam Preparation in China

- **Structure**: The quiz is designed to align with the self-study exam format in China, which often emphasizes theoretical understanding, problem-solving, and practical applications. Questions are balanced to test memory, analysis, and design skills.
- **Study Tips**:
  - Focus on mastering fundamental laws (e.g., Ohm’s, Kirchhoff’s) and their applications.
  - Practice designing basic circuits (e.g., amplifiers, counters) using standard components.
  - Use simulation tools like Multisim or Proteus to verify designs.
  - Review semiconductor characteristics and logic gate operations thoroughly.
- **Resources**: The textbook *Fundamentals of Electronic Technology (III)* by Wen Xidong (Economic Science Press) is the primary resource. Supplement with online tutorials or platforms like Coursera for circuit simulations and HDL basics.
- **Exam Context**: Self-study exams in China, such as those administered by the National Education Examinations Authority (NEEA), require disciplined preparation. Past papers (if available) and chapter exercises from the textbook are critical for success.

If you’d like additional questions, specific topics emphasized, or a focus on lab-related questions, let me know! I can also provide a more detailed answer key or tailor the quiz for a specific exam format.
