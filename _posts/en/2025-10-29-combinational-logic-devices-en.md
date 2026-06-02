---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Combinational Logic Devices Overview
translated: false
type: note
---

### Overview

The video from "The Learning Circuit" explains combinational logic devices, which generate outputs based only on current inputs (no memory of past states). It covers four key types: multiplexers (MUX), demultiplexers (DEMUX), encoders, and decoders. These are essential for signal routing, data compression/expansion, and digital control in electronics.

### Multiplexers (MUX)

- **Purpose**: Like a digital switchboard—selects one of many inputs to send to a single output, controlled by select lines.
- **Basic Example (74LS157 Quad 2-to-1 MUX)**:
  - 4 channels, each with inputs A and B, select pin (S), and enable pin (E).
  - S high: Selects A inputs; S low: Selects B inputs.
  - E low: Enables output; E high: Disables (outputs go low).
- **Larger Examples**:
  - 4-to-1 MUX: 2 select lines choose from 4 inputs.
  - 8-to-1 MUX: 3 select lines; only one input passes through.
- **Tip**: General form is \\(2^n\\)-to-1, where \\(n\\) is select lines.

### Demultiplexers (DEMUX)

- **Purpose**: Opposite of MUX—routes one input to one of many outputs, based on select lines.
- **Basic Example (1-to-2 DEMUX)**:
  - One select line (S): S low → input to Y0; S high → input to Y1.
- **General Rule**: \\(1\\)-to-\\(2^n\\) outputs, matching MUX's select lines (e.g., 2 selects → 4 outputs).

### Encoders

- **Purpose**: Compresses multiple inputs into a coded (e.g., binary) output.
- **Basic Binary Encoder**:
  - Example: 4 inputs → 2-bit binary output (e.g., input 3 active → output 11).
  - Issue: Multiple active inputs can cause conflicts (ambiguous output).
- **Priority Encoder** (Fixes Conflicts):
  - Assigns priority (highest first overrides others).
  - Example (8-input, active-low): Input 7 (highest) active → output 111, ignores lower inputs.
  - No inputs active → output 000.

### Decoders

- **Purpose**: Expands coded input into multiple outputs (e.g., activates specific lines).
- **Basic Binary Decoder**:
  - Like a DEMUX: Binary input selects one output (e.g., 2-bit input 10 → activates output 2).
- **BCD to 7-Segment Decoder**:
  - 4-bit BCD input (0–9) → Controls 7 LED segments for digit display.
  - Examples: "0" lights 6 segments; "1" lights 2 (right-side bars).
- **BCD to Decimal Decoder**:
  - 4-bit input → Activates one of 10 outputs (for digits 0–9).

### Key Takeaways

- **MUX/DEMUX**: Data routers (traffic directors).
- **Encoders**: More inputs than outputs (data compression, like zipping).
- **Decoders**: More outputs than inputs (data expansion, like unzipping).
- All are "combinational"—output changes instantly with inputs, no clocks or storage.

[How Combinational Logic Devices Work - The Learning Circuit](https://www.youtube.com/watch?v=gsmB7J72Tgc)
