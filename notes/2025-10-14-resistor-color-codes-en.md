---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Reading Resistor Color Codes
translated: false
type: note
---

### Understanding Resistor Color Codes

Resistors are small electronic components that limit the flow of electrical current, and their resistance value (measured in ohms, Ω) is often indicated by colored bands on their body. These bands follow a standardized color code system. Most resistors have 4, 5, or 6 bands, but 4- and 5-band types are the most common. Always read the bands from left to right, starting with the band closest to one end (the "reading end"). The tolerance band (often gold or silver) is usually on the right side—if you're unsure, rotate the resistor so any metallic band is on the right.

#### Color Code Chart

Each color represents a digit (0-9) for the significant figures, or a multiplier (power of 10) to scale the value. Here's the standard mapping:

| Color    | Digit Value | Multiplier (Power of 10) |
|----------|-------------|---------------------------|
| Black   | 0           | ×10⁰ (1)                 |
| Brown   | 1           | ×10¹ (10)                |
| Red     | 2           | ×10² (100)               |
| Orange  | 3           | ×10³ (1,000)             |
| Yellow  | 4           | ×10⁴ (10,000)            |
| Green   | 5           | ×10⁵ (100,000)           |
| Blue    | 6           | ×10⁶ (1,000,000)         |
| Violet  | 7           | ×10⁷ (10,000,000)        |
| Gray    | 8           | ×10⁸ (100,000,000)       |
| White   | 9           | ×10⁹ (1,000,000,000)     |
| Gold    | -           | ×10⁻¹ (0.1)              |
| Silver  | -           | ×10⁻² (0.01)             |

#### Tolerance Bands

The final band(s) indicate the tolerance (precision of the resistance value):

- Brown: ±1%
- Red: ±2%
- Green: ±0.5%
- Blue: ±0.25%
- Violet: ±0.1%
- Gray: ±0.05%
- Gold: ±5%
- Silver: ±10%
- No band: ±20%

#### How to Read a 4-Band Resistor

1. Identify the first two bands as the significant digits (e.g., brown-black = 10).
2. The third band is the multiplier—multiply the digits by this power of 10 (e.g., red = ×100, so 10 × 100 = 1,000 Ω).
3. The fourth band is the tolerance (e.g., gold = ±5%).

**Example**: Brown (1), black (0), red (×100), gold (±5%) = 10 × 100 = 1,000 Ω ±5% (or 1 kΩ).

#### How to Read a 5-Band Resistor

These offer higher precision with an extra significant digit.

1. Identify the first three bands as significant digits (e.g., brown-black-red = 102).
2. The fourth band is the multiplier (e.g., orange = ×1,000, so 102 × 1,000 = 102,000 Ω).
3. The fifth band is the tolerance (e.g., brown = ±1%).

**Example**: Brown (1), black (0), red (2), orange (×1,000), brown (±1%) = 102 × 1,000 = 102,000 Ω ±1% (or 102 kΩ).

#### Notes

- For 6-band resistors, the first five bands follow the 5-band pattern, and the sixth indicates temperature coefficient (how resistance changes with heat, e.g., brown = 100 ppm/°C).
- If bands are faded or unclear, use a multimeter to measure the actual resistance.
- Zero-ohm resistors (jumpers) may have a single black band.

[How To Read Resistor Color Codes | Arrow.com](https://www.arrow.com/en/research-and-events/articles/resistor-color-code)
[RESISTOR COLOR CODE GUIDE (PDF)](https://neurophysics.ucsd.edu/courses/physics_120/resistorcharts.pdf)
