---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Rotary Encoders Measure Rotation
translated: false
type: note
---

### What is a Rotary Encoder?

A **rotary encoder** is a type of electro-mechanical sensor used to detect and measure the angular position or rotation of a shaft (like in knobs, dials, or wheels) in mechanical devices. It converts rotational motion into digital or analog signals, allowing devices to track how much and in which direction something has turned. They're common in everything from volume knobs on audio equipment to steering wheels in robotics and industrial machinery.

#### Key Types
There are two main kinds, based on how they handle position tracking:

| Type              | Description | Best For |
|-------------------|-------------|----------|
| **Incremental**  | Outputs pulses (or "ticks") for each small change in rotation, counting steps relative to a starting point. Position is calculated by tracking these changes over time. | Gradual, continuous motion like scrolling wheels or motor feedback where absolute position isn't critical. |
| **Absolute**     | Provides a unique digital code for every possible angular position, so it knows the exact location even after power loss. | Precise applications like elevators or CNC machines where knowing the "home" position without resetting is essential. |

#### How It Works (Simplified)
- **Optical**: A light source shines through a patterned disk (with slots or marks) attached to the rotating shaft. A sensor detects interruptions in the light to generate signals.
- **Magnetic**: Uses magnets and Hall-effect sensors to detect changes in magnetic fields as the shaft turns.
- **Mechanical**: Older style with direct contacts, but less reliable due to wear.

The "gradual position changes" you mentioned align perfectly with incremental rotary encoders, as they excel at detecting smooth, incremental rotations without needing to reset.

If this isn't quite what you meant by "what is it?" (e.g., if you're thinking of a specific device or comparison), feel free to clarify!
