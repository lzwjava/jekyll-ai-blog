---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open-Source Transformer ASIC Design References
translated: false
type: note
---

Question: **What open-source projects are good references if I want to build something architecturally similar to Etched Sohu — a specialized AI inference accelerator / transformer ASIC?**

Answer:

Yes. If your goal is **“Etched, but open-source / researchable / hackable”**, I would not look for one single project. The useful stack is:

```text
                 Transformer / LLM
                       │
                 compiler/runtime
                       │
              ┌────────┴────────┐
              │                 │
           operator          scheduler
              │                 │
              └────────┬────────┘
                       │
                accelerator ISA
                       │
              ┌────────┴────────┐
              │                 │
          systolic/dataflow    SRAM
              │                 │
              └────────┬────────┘
                       │
                    HBM/DDR
                       │
                    NoC/SoC
                       │
                    RTL/ASIC
```

Etched's interesting part is that they co-design essentially this whole stack, rather than making another GPU. Their current description explicitly says they co-design **chips, racks, software, and manufacturing** for frontier inference. ([Etched][1])

### 1. Gemmini — probably the best starting point

Gemmini

[ucb-bar/gemmini](https://github.com/ucb-bar/gemmini?utm_source=chatgpt.com)

Gemmini is a **parameterizable systolic-array accelerator generator** written in Chisel and integrated with Chipyard. It gives you substantially more than RTL: accelerator architecture + ISA interface + compiler/software + simulation. ([GitHub][2])

Conceptually:

```text
RISC-V
  │
  │ custom instructions
  ▼
Gemmini
  │
  ├── DMA
  ├── scratchpad SRAM
  ├── systolic array
  ├── accumulator
  └── memory interface
```

This is extremely useful for understanding the fundamental question:

> **What should the hardware actually expose to an LLM runtime?**

For example, a simple accelerator could expose something like:

```c
matmul(
    A_addr,
    B_addr,
    C_addr,
    M, N, K
);
```

but a serious inference ASIC starts moving toward:

```text
load weights
load activations
attention(Q,K,V)
KV-cache read/write
GEMM
GEMM
activation
quantize
DMA
```

rather than exposing individual MACs.

---

### 2. Chipyard — build the entire ASIC prototype

[ucb-bar/chipyard](https://github.com/ucb-bar/chipyard?utm_source=chatgpt.com)

If Gemmini is the accelerator, **Chipyard is the laboratory in which you build the SoC around it**.

It provides:

* RISC-V cores
* accelerators
* memory systems
* NoC/interconnect
* RTL simulation
* FPGA simulation
* ASIC flow
* software generation

Chipyard explicitly integrates Gemmini and NVDLA and supports RTL simulation, FPGA-accelerated simulation, and VLSI flows. ([GitHub][3])

For someone actually trying to build an Etched-like prototype, I'd start:

```bash
git clone https://github.com/ucb-bar/chipyard
cd chipyard

# then add your own accelerator
#        ↓
# RISC-V + your transformer accelerator
#        ↓
# Chipyard
#        ↓
# Verilator / FPGA / ASIC flow
```

---

### 3. NVDLA — study a real open accelerator

NVIDIA NVDLA

[NVIDIA NVDLA](https://nvdla.org/?utm_source=chatgpt.com)

NVDLA is probably the most important reference if you want to understand **how a serious neural-network accelerator is actually decomposed**.

Unlike toy FPGA projects, NVDLA includes:

```text
RTL
 ↓
C model
 ↓
compiler
 ↓
runtime
 ↓
Linux driver
 ↓
test infrastructure
```

NVIDIA describes it as a scalable, configurable open architecture, with Verilog RTL, compiler, drivers, test benches and software. ([NVIDIA Deep Learning Accelerator][4])

The interesting thing is that NVDLA is **not transformer-specific**.

That's precisely why I'd study it alongside Etched:

```text
NVDLA
general DNN accelerator
        │
        ├── convolution
        ├── GEMM
        ├── activation
        └── pooling

Etched
transformer-specialized accelerator
        │
        ├── QKV
        ├── attention
        ├── KV cache
        ├── FFN
        └── decode/prefill
```

That difference is the architectural rabbit hole.

---

### 4. Apache TVM VTA — accelerator + compiler co-design

[apache/tvm-vta](https://github.com/apache/tvm-vta?utm_source=chatgpt.com)

VTA is particularly interesting because it treats the **compiler and accelerator as one system**.

```text
PyTorch / model
       ↓
      TVM
       ↓
VTA compiler
       ↓
accelerator instructions
       ↓
 FPGA hardware
```

It provides open hardware, simulator, driver/runtime and an end-to-end TVM compiler stack. ([GitHub][5])

This is closer to the actual Etched problem than simply designing a matrix-multiply unit.

Because the killer question is not:

> "Can my hardware do 100 TOPS?"

It's:

> **"Can the compiler turn an actual autoregressive decode loop into an efficient static schedule?"**

---

### 5. Tenstorrent — very relevant architectural reference

Tenstorrent

Tenstorrent is worth studying even though its chips aren't open-source in the same way as Gemmini/NVDLA.

The interesting part is the **programmable dataflow architecture + open software stack**.

Compared with the Etched philosophy:

```text
GPU:
programmable SIMD/SIMT

Tenstorrent:
programmable dataflow

Groq:
highly deterministic dataflow

Etched:
specialized transformer hardware
```

So I'd study Tenstorrent to understand the boundary between:

```text
fixed-function ASIC
        ↕
programmable accelerator
```

The `awesome-ai-hardware` project is also a useful index of these architectures, including Tenstorrent, Groq, Cerebras, Maia, TPU and Etched. ([GitHub][6])

---

### 6. VTA if you want FPGA → ASIC iteration

VTA is especially attractive if your plan is:

```text
Python model
     ↓
compiler
     ↓
FPGA
     ↓
measure
     ↓
change architecture
     ↓
FPGA
     ↓
ASIC
```

rather than immediately attempting a full ASIC.

For an individual/small team, this is much more realistic.

---

### 7. Tiny FPGA accelerator projects — useful for learning RTL

There are also small projects like:

[taitashaw/fpga-ai-accelerator](https://github.com/taitashaw/fpga-ai-accelerator?utm_source=chatgpt.com)

This one implements an **8×8 INT8 systolic array in SystemVerilog**, including SRAM, tiling, requantization, AXI interfaces, verification and FPGA deployment. ([GitHub][7])

This is useful because you can read the entire design in one sitting:

```text
rtl/
  systolic_array
  ├── PE
  ├── SRAM
  ├── DMA
  ├── tiler
  └── quantizer
```

That's much easier to digest before diving into a million-line accelerator codebase.

---

## What I'd actually study

If your objective is **“I want to understand/build an open-source mini-Etched”**, I'd use this sequence:

| Layer               | Project                | What to steal conceptually                 |
| ------------------- | ---------------------- | ------------------------------------------ |
| RTL                 | small FPGA accelerator | MAC / SRAM / DMA                           |
| Matrix engine       | **Gemmini**            | systolic architecture                      |
| SoC                 | **Chipyard**           | RISC-V + accelerator + memory              |
| DNN accelerator     | **NVDLA**              | production-style accelerator decomposition |
| Compiler            | **VTA/TVM**            | compiler ↔ hardware contract               |
| Dataflow            | **Tenstorrent**        | programmable spatial execution             |
| System architecture | **Etched**             | transformer-specific specialization        |

The key thing I'd **not** do is start by implementing a giant transformer ASIC.

Start with:

```text
                CPU
                 │
              command
                 │
                 ▼
        ┌─────────────────┐
        │ Transformer ACC │
        │                 │
        │ QKV GEMM        │
        │ Attention       │
        │ FFN GEMM        │
        │ RoPE            │
        │ KV cache        │
        └────────┬────────┘
                 │
              HBM/DDR
```

Then measure **tokens/sec/W**, not TOPS.

For autoregressive inference, a very useful first-principles model is:

```text
decode one token

        weight bytes
             +
       KV-cache bytes
             +
      activation bytes
             ↓
      memory bandwidth
             ↓
        token latency
```

That's why an Etched-style architecture is interesting: once you know the exact transformer computation you're willing to support, you can eliminate huge amounts of **general-purpose programmability**.

The open-source project I'd personally use as the **base skeleton is Chipyard + Gemmini**, then progressively replace the generic GEMM-centric accelerator with a transformer-specific dataflow engine.

I can also map out a **“mini Sohu” architecture you could actually prototype on an FPGA**—including the KV-cache SRAM layout, attention datapath, instruction set, and a minimal PyTorch → accelerator compiler path.

[1]: https://www.etched.com/?utm_source=chatgpt.com "Etched"
[2]: https://github.com/ucb-bar/gemmini?utm_source=chatgpt.com "GitHub - ucb-bar/gemmini: Berkeley's Spatial Array Generator · GitHub"
[3]: https://github.com/ucb-bar/chipyard/blob/main/README.md?plain=1&utm_source=chatgpt.com "chipyard/README.md at main · ucb-bar/chipyard · GitHub"
[4]: https://nvdla.org/?utm_source=chatgpt.com "NVIDIA Deep Learning Accelerator"
[5]: https://github.com/apache/tvm-vta?utm_source=chatgpt.com "GitHub - apache/tvm-vta: Open, Modular, Deep Learning Accelerator · GitHub"
[6]: https://github.com/ai-hpc/awesome-ai-hardware?utm_source=chatgpt.com "GitHub - ai-hpc/awesome-ai-hardware: AI accelerators, edge inference devices, compilers, runtimes, benchmarks, and research for building and evaluating machine-learning systems. · GitHub"
[7]: https://github.com/taitashaw/fpga-ai-accelerator?utm_source=chatgpt.com "GitHub - taitashaw/fpga-ai-accelerator: Open-source 8×8 INT8 systolic array inference accelerator — from RTL to bitstream · GitHub"