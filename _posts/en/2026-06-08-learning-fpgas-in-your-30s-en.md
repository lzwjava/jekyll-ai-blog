---
audio: false
generated: true
image: false
lang: en
layout: post
title: Learning FPGAs in Your 30s
translated: false
type: note
---

Question: Is it too late to learn electronics/electrical engineering in my 30s to understand and build GPU chips and FPGA designs?

---

**Answer:**

No, it's not too late. But I need to be blunt: the path splits here, and they're very different difficulty curves.

## GPU Chip Design vs. FPGA: Two Different Mountains

**GPU chip design** (actual silicon) requires:

- Transistor physics, CMOS fundamentals, circuit design
- VLSI (very large-scale integration) at 5nm/3nm nodes
- EDA tools (Cadence, Synopsys) — expensive, multi-million dollar licenses
- Deep understanding of memory hierarchies, power delivery, thermal management
- 5-7 years minimum to get competent at real fab-level chip design

This is the hard path. Modern GPU chips like Apple's M3 integrate over 25 billion transistors on a single die using 3nm processes. The gap between "I understand how GPUs work algorithmically" (which you do) and "I can design GPU logic that synthesizes to gates that route to silicon" is enormous.

**FPGA design** is 10x more accessible:

- FPGA programming now emphasizes high-level synthesis (HLS) — behavioral-level programming in C/C++ rather than low-level RTL
- You can iterate in weeks on real hardware
- The Zero-to-ASIC curriculum now includes AI-assisted design tools and allows submission to TinyTapeout for actual chip fabrication
- The barrier to entry is 3-6 months, not years

## Why You Should Probably Go FPGA First

Your existing knowledge is actually a *disadvantage* if you target GPU design directly. You know GPUs from the compute perspective — caches, memory access patterns, kernel execution — but you don't know:

- How transistors actually switch at nanosecond timescales
- Timing closure and setup/hold violations
- Place-and-route tools and design rule checking
- Power distribution, clock trees, signal integrity

FPGA lets you skip the physics and jump straight to *design and iteration*. You write Verilog/SystemVerilog (or C++ via HLS), synthesize to LUTs and routing fabric, and ship to actual hardware. This is closer to your vibe — code fast, test, iterate.

For AI acceleration specifically — which is your real use case — FPGA is powerful:

- Amazon AWS F1 FPGAs accelerate inference
- FPGAs have become integral to deep neural network acceleration, delivering low-latency, high-throughput solutions for AI workloads
- You can implement custom memory bandwidth optimization, fixed-point quantization paths, custom activations — things that matter for inference at scale

## The Realistic Learning Path

**6 months to functional FPGA designs:**

1. **Digital logic basics** (2-3 weeks) — gates, flip-flops, FSMs, timing. FPGAacademy provides free tutorials and laboratory exercises progressing from simple operations (LEDs, switches) to advanced topics like state machines, counters, and simple processors.

2. **Verilog / SystemVerilog** (4-6 weeks) — this is your HDL. Syntax is simple; thinking in hardware is the hard part. Start with a basic ALU, then a simple CPU pipeline. Actually build and simulate.

3. **FPGA tools** (Vivado, Quartus) — 1-2 weeks of tutorials, then learn by doing.

4. **Real projects** (3-4 months):
   - Implement a RISC-V CPU on an FPGA board (Arty A7, Nexys, etc.)
   - Build a neural network inference accelerator (matrix multiply, pooling, activation)
   - Submit to TinyTapeout for actual ASIC fabrication — you get real silicon

**Concrete resources:**

- "Verilog for an FPGA Engineer with Xilinx Vivado Design Suite" on Udemy covers fundamentals to advanced projects
- University of Colorado Boulder's FPGA specialization on Coursera (free audit)
- GitHub: `nandland/fpga-serial`, `tinytapeout` community designs, OpenROAD for physical design
- Buy a dev board (~$100): Arty A7 or Nexys

## If You Actually Want GPU Chip Design

Don't dismiss it, just understand the commitment:

1. **First 1 year**: CMOS fundamentals, digital circuits (transistor-level). Read "CMOS VLSI Design" by Weste & Harris. This is different from your GPU knowledge — you'll learn why wires have resistance, why clocks are hard, how to avoid race conditions.

2. **Year 2-3**: Synthesis, place-and-route, using Cadence or OpenROAD. UCSC Silicon Valley Extension offers courses in front-end and back-end ASIC design using Cadence, OpenROAD, Siemens, and Synopsys tools.

3. **Year 4+**: Actual chip projects. Consider UT Austin's new ASIC Design Lab course and the upcoming Master of Science in Semiconductor Science and Engineering, or similar programs.

The bottleneck isn't age — it's that nobody builds a GPU in a garage. You'd need to work at a chip company (NVIDIA, AMD, Apple, Graphcore) or academia to touch real GPU design. FPGA is the self-taught path.

## The Honest Take

You're 30+ with 12 years of engineering experience and have trained models on MI300X GPUs. You have the mathematical depth, the systems thinking, and the discipline.

**FPGA is absolutely doable.** 6-12 months from zero to shipping real inference accelerators. This compounds your GPU knowledge — you'll understand memory bandwidth, latency, quantization in ways that make you a better ML engineer *and* hardware designer.

**GPU chip design is possible but expensive in time.** It's not a weekend project; it's a 3-5 year commitment. Worth considering only if you want to work at a fab-tier company or in chip design research.

My suggestion: Start FPGA in parallel with your AI work. Build a small quantized LLM accelerator on an Arty A7 (NeuralEngine-style). That gives you real hardware experience, a portfolio project, and teaches you whether you actually want to go deeper into silicon design or if your real passion is AI optimization at the software/firmware level.

---

References:

- FPGA Development Productivity with HLS (Georgia Tech 2025)
- FPGAacademy course materials
- NYU Tandon BASICS program - democratizing chip design
- UCSC Silicon Valley VLSI Design Certificate
- UT Austin ASIC Design and Semiconductor Science programs
