---
audio: false
generated: true
image: false
lang: en
layout: post
title: Guangzhou 3D LED Illusion Secrets
translated: false
type: note
---

Question: How is the large 3D-effect screen on the Renfeng Building in Tianhe, China implemented, where ads sometimes show animals like elephants coming out of the building? What software is used to play these ads? Is it OBS?

Answer:

The large screen on Renfeng Building (仁丰大厦) in Tianhe District, Guangzhou, China, is a massive outdoor **naked-eye 3D LED display** covering about 1,403 square meters. It was upgraded to support striking naked-eye 3D effects around 2022, making it one of Guangzhou's landmark "screen kings" in the Tianhe Road business district.

These intriguing 3D effects — where animals (like elephants), spaceships, pandas, dragons, mechanical hands, or other objects appear to burst out of or leap from the building — are **not true holographic projections** but optical illusions created through:

- **Screen structure**: The display often uses an L-shaped, curved, or right-angle (90°) configuration that wraps around the building's corner or facade. This physical curvature is key to the depth illusion.
- **Content design**: Videos are specially produced using 3D animation software (e.g., Blender, Cinema 4D, Maya, or After Effects with plugins). Creators apply deformation mapping and perspective tricks so objects seem to extend far beyond the screen plane when viewed from specific angles (usually the main pedestrian/viewing directions).
- **Naked-eye 3D principle**: It relies on **binocular disparity** and motion parallax. Each eye sees a slightly different perspective due to the angled/curved screen layout, and the brain combines them into a strong sense of depth and protrusion — no glasses required. High-resolution LED modules (e.g., P6 or finer) and precise alignment enhance the realism.

This technique became very popular in China starting around 2020–2022, with famous examples in Chengdu (e.g., Taikoo Li IFS screens with giant pandas or tigers leaping out), Shanghai, and Guangzhou (including Renfeng Building and nearby spots like Guangzhou Design City or Xinda Xin Department Store).

For playback, professional **media server systems** and dedicated playback software are used, not consumer tools like OBS Studio (which is mainly for live streaming and lacks robust support for warped/mapped 3D content on huge irregular LED walls).

Common professional solutions in China for these large naked-eye 3D setups include:

- NovaStar (very widely used for LED control; their Taurus/ VX series media players + V-Can or NovaLCT software handle scheduling, warping, and high-bitrate 4K/8K playback).
- Colorlight, Linsn, or Huidu systems for sending cards and receiving cards.
- Specialized 3D playback software such as:
  - Disguise (d3)
  - Notch
  - TouchDesigner
  - Custom media servers from companies like Resolume (less common for huge outdoor screens)
  - Chinese platforms like LEDshowT, ViPlex, or proprietary systems from integrators (e.g., Yaham, Unit LED, or RAVLED)

These systems support content mapping to non-rectangular/curved surfaces, synchronization across multiple sections, brightness/color calibration, and scheduled ad rotation. The 3D content is pre-rendered as a regular 2D video file but designed with the exact viewing perspective in mind, so it "pops out" correctly from the intended spots on the street.

In short: the magic comes mostly from clever content creation + angled screen geometry, played back via professional LED media servers and control software — far more advanced and reliable than OBS.

References:

- [https://www.yaham.com/guangzhou-led-display-king-was-born-naked-eye-3d-big-screen-debut.html](https://www.yaham.com/guangzhou-led-display-king-was-born-naked-eye-3d-big-screen-debut.html)
- [https://www.unit-led.com/3d-billboard-china](https://www.unit-led.com/3d-billboard-china)
- [https://www.doitvision.com/outdoor-naked-eye-3d-screens](https://www.doitvision.com/outdoor-naked-eye-3d-screens)
- [https://ledscreenfactory.com/3d-led-display-complete-guide](https://ledscreenfactory.com/3d-led-display-complete-guide)
