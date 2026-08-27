---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quadro 410 without fan
translated: false
type: note
---

Question: What happens if you remove the fan from an NVIDIA Quadro 410 and plug it in?

Answer:

![Image](https://images.openai.com/static-rsc-4/DEoK1G2XdBPcnMVi6tx4dEGAhG00nIcy-IDyI2wKDIDH153xHeotRZifeAOr6j1PBfI4kh2j2_vWa7zVWG15-WvhHg_9y2hTdMpkBa7StCuKryB-tZxECwWLPPz21KsY1ZfXmljmzTYwA-amx1AEDGCVCa9Vs0g9UuF6sEVQw3jWIhIgJcnfh0VwF41T6tWC?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Ld0rnL0J79Ja8XVG0CucwlltB7m0d9jeNQMLBL8XZ7GQ80oq2USCrGrjOLu0AP4NP6b14l2fvfPlaLicH3qSii5gGy8nTT9uUU3SnPaSH2pKybedv7NAYVXhnrN42cHLjnAYUKomYGs6NnToA2kZY9DSRuCO38Ug0UAWsC4XqRQohTX7vViFPsbEZbfdkKux?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/otr-F_xmxkEsggWnpUUt2XMPEdJhmmdBa9PP5hILJH9V5RiJmXaQ26r9bWtRzhFnkkBG-kMtfGgXX0AHVA8INXPb29vlMtzoxWJYVxXt4JVXoB-vPDhK5_hwb-oblPKzB0tVk-l5-yIaIhurSHv8UXggKme1XGvLvtcFQzaC_R2I17Gs0eZ6u6S9GEvMcDM_?purpose=fullsize)

The Quadro 410 is a very low-power workstation GPU. It uses the **NVIDIA GK107 Kepler chip** and its TDP is around **38W**. The cooler is mostly a small heatsink + tiny fan because the chip is not very hot compared with modern GPUs.

If you remove the fan but keep the heatsink:

* **Idle / desktop:** probably works normally.
* **Light workload:** likely works for some time.
* **Heavy GPU load:** temperature will rise quickly and may throttle or crash.

The GPU itself has thermal protection:

1. Temperature rises.
2. Driver reduces clock speed (thermal throttling).
3. If it gets too hot (~90–100°C range), GPU shuts down to protect itself.

The exact behavior depends on airflow:

### Case 1: Fan removed, heatsink still attached, open air

Maybe OK.

Example:

```
GPU chip
  |
thermal paste
  |
metal heatsink
  |
room air
```

A 38W chip can sometimes survive because the heatsink can dissipate some heat passively.

### Case 2: Fan removed, no heatsink

Bad idea.

```
GPU chip
  |
  |
air only
```

The tiny silicon die has almost no surface area. It can reach dangerous temperatures very fast.

### Case 3: Fan removed but add a bigger heatsink

Actually a good experiment.

A large CPU heatsink or motherboard VRM heatsink can easily cool a Quadro 410:

```
Quadro 410 PCB
       |
thermal pad/paste
       |
large aluminum heatsink
       |
case airflow
```

Because 38W is small. Modern laptop CPUs often dissipate more.

For learning hardware, the Quadro 410 is a nice "safe" GPU to experiment with because:

* cheap
* low power
* simple PCB
* unlikely to instantly destroy itself
* you can observe thermal behavior

You can measure it with:

```bash
watch -n 1 nvidia-smi
```

and watch:

```
temperature
power draw
GPU clock
```

A fun experiment:

1. Run `glmark2` or a CUDA workload.
2. Remove fan power connector.
3. Watch temperature climb.
4. Observe throttling.

This is basically the same principle used when debugging failed GPU cards: many "dead" GPUs are actually cooling, VRAM, power delivery, or solder issues rather than the GPU core itself.
