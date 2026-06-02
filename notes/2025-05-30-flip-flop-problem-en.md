---
audio: false
generated: true
lang: en
layout: post
title: JK Flip-Flop Experiment and State Table
translated: false
type: note
---

The image contains a description in Chinese about a JK flip-flop, a type of flip-flop circuit used in digital electronics, followed by a state transition table.

### Translation:
**42. JK Flip-Flop Experiment - One Pulse Trigger Clock**
- Objective: Understand the working principle and characteristics of a JK flip-flop.
- Equipment: JK flip-flop module, pulse generator, power supply, connecting wires, etc.

**Figure 42 State Transition Table**

| Q₂ⁿ | Q₁ⁿ | Q₀ⁿ | Q₂ⁿ⁺¹ | Q₁ⁿ⁺¹ | Q₀ⁿ⁺¹ | Z |
|-----|-----|-----|-------|-------|-------|---|
| 0   | 0   | 0   | 0     | 0     | 1     | 0 |
| 0   | 0   | 1   | 0     | 1     | 0     | 0 |
| 0   | 1   | 0   | 0     | 1     | 1     | 0 |
| 0   | 1   | 1   | 1     | 0     | 0     | 0 |
| 1   | 0   | 0   | 0     | 0     | 0     | 1 |

### Answer:
The table represents the state transition of a 3-bit JK flip-flop where Q₂ⁿ, Q₁ⁿ, and Q₀ⁿ are the current states, and Q₂ⁿ⁺¹, Q₁ⁿ⁺¹, and Q₀ⁿ⁺¹ are the next states after a clock pulse. The output Z is 1 only when the current state is 100, indicating a specific condition or output signal. This behavior is typical of a JK flip-flop, which can hold, set, reset, or toggle its state based on the inputs (J and K) and clock pulse.


Let’s break down the JK flip-flop state transition table and explain its behavior in detail.

### Overview of a JK Flip-Flop
A JK flip-flop is a type of sequential logic circuit used in digital electronics to store a single bit of data. It has two inputs, J and K, a clock input (CLK), and two outputs, Q (the current state) and Q' (the complement of Q). The JK flip-flop is an improvement over the SR flip-flop because it eliminates the "invalid" state (when both inputs are 1). Its behavior is as follows:

- **J = 0, K = 0**: No change (Q stays the same).
- **J = 0, K = 1**: Reset (Q becomes 0).
- **J = 1, K = 0**: Set (Q becomes 1).
- **J = 1, K = 1**: Toggle (Q flips to the opposite state).

The table in the image represents a system with three JK flip-flops (Q₂, Q₁, Q₀), forming a 3-bit state machine, where Q₂ⁿ, Q₁ⁿ, and Q₀ⁿ are the current states, and Q₂ⁿ⁺¹, Q₁ⁿ⁺¹, and Q₀ⁿ⁺¹ are the next states after a clock pulse. Z is an output signal based on the current state.

### State Transition Table Explanation
The table shows how the system transitions between states and when the output Z is activated. Let’s analyze each row:

| Q₂ⁿ | Q₁ⁿ | Q₀ⁿ | Q₂ⁿ⁺¹ | Q₁ⁿ⁺¹ | Q₀ⁿ⁺¹ | Z |
|-----|-----|-----|-------|-------|-------|---|
| 0   | 0   | 0   | 0     | 0     | 1     | 0 |
| 0   | 0   | 1   | 0     | 1     | 0     | 0 |
| 0   | 1   | 0   | 0     | 1     | 1     | 0 |
| 0   | 1   | 1   | 1     | 0     | 0     | 0 |
| 1   | 0   | 0   | 0     | 0     | 0     | 1 |

#### Row 1: State 000 → 001, Z = 0
- **Current State (Q₂ⁿ, Q₁ⁿ, Q₀ⁿ)**: 000 (decimal 0)
- **Next State (Q₂ⁿ⁺¹, Q₁ⁿ⁺¹, Q₀ⁿ⁺¹)**: 001 (decimal 1)
- **Z Output**: 0
- **Explanation**: The system starts at state 000. After a clock pulse, Q₀ toggles from 0 to 1 (likely because J₀ = 1, K₀ = 1), while Q₁ and Q₂ remain 0 (possibly J₁ = 0, K₁ = 0; J₂ = 0, K₂ = 0). Z is 0, indicating the output condition isn’t met.

#### Row 2: State 001 → 010, Z = 0
- **Current State**: 001 (decimal 1)
- **Next State**: 010 (decimal 2)
- **Z Output**: 0
- **Explanation**: From state 001, Q₀ toggles from 1 to 0 (J₀ = 1, K₀ = 1), Q₁ toggles from 0 to 1 (J₁ = 1, K₁ = 1), and Q₂ stays 0. Z remains 0.

#### Row 3: State 010 → 011, Z = 0
- **Current State**: 010 (decimal 2)
- **Next State**: 011 (decimal 3)
- **Z Output**: 0
- **Explanation**: From state 010, Q₀ toggles from 0 to 1 (J₀ = 1, K₀ = 1), Q₁ stays 1, and Q₂ stays 0. Z is still 0.

#### Row 4: State 011 → 100, Z = 0
- **Current State**: 011 (decimal 3)
- **Next State**: 100 (decimal 4)
- **Z Output**: 0
- **Explanation**: From state 011, Q₀ toggles from 1 to 0, Q₁ toggles from 1 to 0, and Q₂ toggles from 0 to 1 (J₂ = 1, K₂ = 1). Z remains 0.

#### Row 5: State 100 → 000, Z = 1
- **Current State**: 100 (decimal 4)
- **Next State**: 000 (decimal 0)
- **Z Output**: 1
- **Explanation**: From state 100, Q₂ toggles from 1 to 0, Q₁ stays 0, and Q₀ stays 0. The output Z is 1, indicating that the state 100 triggers the output condition (possibly Z = Q₂ AND NOT Q₁ AND NOT Q₀).

### System Behavior
- **State Sequence**: The system cycles through states in this order: 000 → 001 → 010 → 011 → 100 → 000, and repeats. This is a 5-state sequence (out of 8 possible states for 3 bits), suggesting a specific configuration of J and K inputs for each flip-flop.
- **Output Z**: Z is 1 only when the current state is 100. This could represent a condition where the system signals completion of a cycle or a specific event (e.g., a counter reaching a certain value).

### Practical Interpretation
This JK flip-flop setup appears to be a modulo-5 counter (since it cycles through 5 states:  Hawkins). The counter increments with each clock pulse, and the output Z signals when the state 100 is reached before resetting to 000. Such circuits are used in digital systems for counting, frequency division, or generating specific sequences.

### Summary
The JK flip-flop circuit in the table functions as a 3-bit state machine with a 5-state cycle (000 → 001 → 010 → 011 → 100 → 000). The output Z is 1 only in state 100, likely indicating a specific event or reset condition. The transitions are governed by the JK inputs, which are configured to produce this sequence.
