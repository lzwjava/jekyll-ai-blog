---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Repair and Custom Build Guide
translated: false
type: note
---

Question: How can I learn GPU hardware diagnosis and repair, or build my own minimal custom GPU?

Answer:

### Part 1: GPU Hardware Diagnosis & Board Repair Roadmap

Diagnosing and repairing graphics cards requires understanding power delivery rails, board schematics, and specialized test software.

**1. Essential Equipment & Safety**

* **Safety First:** Discharge high-voltage capacitors on the board before working. Always use an ESD safe workstation.
* **Tools Needed:** Digital Multimeter (DMM), Soldering Station, Hot Air Rework Station, Thermal Imager or Rosin Atomizer, Oscilloscope (for data signal line inspection), and Microscope.

**2. Standard Power Rail Initialization Sequence**
When a GPU powers on, its voltage rails must trigger in a specific order. Check resistance to ground first before applying power:

1. **12V & 3.3V PCIe / AUX:** Primary input power lines from the motherboard/PSU.
2. **5V Rail:** Powers internal logic ICs and PWM controllers.
3. **1.8V Rail:** Powers the GPU core logic registers and memory interface controls.
4. **VCORE (0.8V–1.1V):** Main voltage rail supplying high current to the GPU silicon.
5. **VMEM / VDDG (1.2V–1.35V):** Powers GDDR6/GDDR6X video memory.
6. **PEX / CWD (1.0V):** Powers the PCIe controller inside the GPU die.

**3. Software Diagnostic Tools**

* **MATS / MODS (NVIDIA):** A modular software utility used to run stress tests on VRAM channels and pinpoint failing memory chips (e.g., Identifying errors on Channel A1 or B0).
* **PyMemTest / Memory Diagnostic Tools (AMD):** Used for locating faulty memory ICs on Radeon GPUs.

---

### Part 2: How to Build a "Tiny GPU" (Silicon / FPGA / Hardware Design)

Building a custom GPU relies on digital logic design using Hardware Description Languages (HDL) like **Verilog** or **SystemVerilog**, then running it on an **FPGA** or fabricating physical silicon via open-source foundry shuttles.

**1. Define a Minimal Compute Architecture**

* Skip complex rasterization hardware (graphics pipelines) initially. Focus on a **GPGPU / SIMD Compute Engine** (matrix/vector math accelerator).
* **Core Components:**
* **Device Control Register & Dispatcher:** Manages kernel invocation signals.
* **ALUs (Arithmetic Logic Units):** Executes basic instructions (`ADD`, `MUL`, `LDR`, `STR`) across parallel threads.
* **Warp Scheduler & Register Files:** Schedules threads to run across available SIMD execution lanes.
* **Memory Controller:** Interfaces local register files with external SRAM/VRAM.



**2. Software Tools & Simulation Path**

* **Design & Simulation:** Write your design in Verilog using tools like **Icarus Verilog** (`iverilog`) and test execution traces with **Cocotb** or **Verilator**.
* **FPGA Prototyping:** Synthesize and deploy your code onto a development board (e.g., Xilinx Spartan-7 or Lattice iCE40) to verify physical execution.
* **ASIC Tape-out (Physical Chip):** Use open-source EDA tools (like **OpenLane**) and submit your design to **Tiny Tapeout** to have physical chips manufactured on nodes like SkyWater 130nm.

**3. Open-Source Reference Projects to Study**

* **`tiny-gpu` (by Adam Majmudar):** A open-source Verilog-based GPU implementation featuring SIMD parallelism, custom ISA, and kernel execution routines.
* **MIAOW / VeriGPU:** Open-source GPU designs providing deeper architectural complexity.
