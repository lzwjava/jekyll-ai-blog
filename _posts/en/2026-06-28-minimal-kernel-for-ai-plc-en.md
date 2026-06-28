---
audio: false
generated: true
image: false
lang: en
layout: post
title: Minimal Kernel for AI PLC
translated: false
type: note
---

Question: Linux has become too bloated. Could there be a minimal kernel that just runs agents with networking — and is an "AI PLC motherboard" a viable idea?

Answer:

Two separate ideas here. Let me take them in order, because the first one is real and the second one is more interesting than it sounds.

## 1. "Minimal kernel + agents + networking"

You're right that Linux is enormous — ~40M LOC, most of which is drivers you'll never touch. But you don't need to fork Linux to get what you want. The "agent runtime as the OS" idea already has several converging paths:

**Path A — Unikernel.** Compile your agent + a minimal network stack + a libos into a single bootable image. No syscall boundary, no general-purpose kernel.

```
# Unikraft: build a unikernel that boots straight into your Rust/C agent binary
git clone https://github.com/unikraft/unikraft
# kraft build --target qemu/x86_64
# boots in ~10ms, image is single-digit MB, only the network driver + lwIP you need
```

The mental model: your agent *is* PID 1, and there is no PID 2. lwIP gives you TCP/IP in ~40KB. This is genuinely "smallest kernel that does networking + runs one program."

**Path B — Rust no_std on bare metal.** If you want to actually learn the layer Karpathy-style, write the kernel. `bootloader` + `x86_64` crates get you to a running `_start` in a weekend, and `smoltcp` is a pure-Rust TCP/IP stack that runs without an allocator.

```rust
// smoltcp: a complete TCP/IP stack in ~15k LOC, no_std, no heap required
// This is the whole "networking" half of your minimal OS
use smoltcp::iface::{Config, Interface};
use smoltcp::wire::{IpAddress, IpCidr};
// device = your NIC driver (virtio-net is ~200 LOC to bring up under QEMU)
// Then: agent reads bytes off a socket, calls out to an inference endpoint, done.
```

The honest constraint: the moment your agent needs to run a *local* LLM, you're back to needing CUDA/ROCm/Vulkan drivers, which is exactly the 30M LOC you were trying to escape. So the clean version is: **minimal kernel runs the agent loop + networking, inference happens over the wire** (remote API or a separate accelerator node). The kernel never needs a GPU driver at all.

**Path C — Linux but stripped.** `tinyconfig` + buildroot gets a bootable Linux under 5MB. Less pure, but you keep the driver ecosystem when you eventually need it.

The interesting frontier idea, the one that fits your AI-native bias: an OS where the **scheduler is an agent**, not a fixed algorithm. Processes submit intent; an LLM-in-the-loop policy decides ordering/resource allocation. That's a research direction (see AIOS below), not a product yet, but it's the version of "agent + minimal kernel" that's actually novel rather than just "small Linux."

## 2. The "AI PLC motherboard"

This is the better idea, and it's worth being precise about *why*.

A PLC (programmable logic controller) is the brain of industrial automation — factory lines, HVAC, water treatment. The market is dominated by Siemens (S7), Rockwell/Allen-Bradley, Mitsubishi. The programming model is frozen in the 1980s: ladder logic, IEC 61131-3, scan-cycle execution. Engineers literally draw relay diagrams. It is the most un-AI-native corner of computing that exists, and it moves billions of dollars.

The thesis "put an AI/agent layer on PLC hardware" is real, but the naive version fails for a hard reason: **PLCs are hard-real-time and safety-rated.** A scan cycle must complete deterministically in 1–10ms, every cycle, forever. An LLM cannot be in that loop — non-deterministic latency, and a hallucination on a control output can kill someone or wreck a machine. SIL-2/SIL-3 certification exists precisely to forbid that.

So the viable architecture is a **two-tier split**, which actually maps perfectly onto your minimal-kernel idea:

```
┌─────────────────────────────────────────────┐
│  Tier 2: Agent plane (your minimal-kernel box)│
│  - LLM/agent: anomaly detection, optimization,│
│    natural-language config, predictive maint.  │
│  - Soft real-time, networked, can be remote    │
│  - Proposes setpoints, never directly actuates │
└───────────────┬─────────────────────────────┘
                │ supervised, rate-limited, bounded commands
┌───────────────▼─────────────────────────────┐
│  Tier 1: Deterministic control plane          │
│  - Classic PLC scan loop / RTOS               │
│  - Hard real-time, certified, dumb-but-safe    │
│  - Enforces safety envelope on Tier-2 commands │
└─────────────────────────────────────────────┘
```

This is exactly where the market is moving and where there's a real opening:

- **Edge AI on the controller.** Siemens already ships the S7-1500 TM NPU module and "Industrial Edge"; Beckhoff TwinCAT runs on x86 and added ML inference runtimes. So the incumbents have validated the demand but bolted it on awkwardly. A clean-sheet board where the AI plane is first-class, not an add-on card, is a genuine wedge.
- **The agent's real job isn't control — it's the human interface and the optimization layer.** "Why did line 3 stop?" → agent reads the tag database, the historian, the alarm log, answers in natural language. "Reduce energy use without dropping throughput" → agent runs the optimization, proposes new setpoints, the deterministic tier validates and applies. That's defensible value the incumbents are bad at.
- **Hardware is commoditized.** An AI-PLC board = an industrial SoC (NXP i.MX, or a RISC-V part) + an NPU + ruggedized I/O + a real-time core. Many SoCs already ship a Cortex-M real-time core *alongside* the Cortex-A application cores on one die — so your two-tier split is one chip: RTOS on the M-core, your minimal agent kernel on the A-core. That's the unlock.

Where it gets hard, in order: safety certification (slow, expensive, the real moat the incumbents hold), industrial sales cycles (12–24 months, conservative buyers), and field reliability (20-year deployment lifetimes, not move-fast-and-break-things). This is not a fast-iteration consumer play — it's the opposite of your usual loop.

But strategically it fits your situation unusually well: it's AI-native, it's a domain incumbents are structurally bad at, the hardware is cheap, and a single person with agents can prototype the software tier on a $50 dev board. The right first experiment isn't a board — it's the **agent layer running against a simulated or cheap real PLC** (OpenPLC is open source, runs on a Raspberry Pi, speaks Modbus). Prove the agent plane delivers value over a real industrial protocol before touching silicon.

Minimal first build:

```bash
# OpenPLC runtime on a Pi/VM = your deterministic tier, free
git clone https://github.com/thiagoralves/OpenPLC_v3
# Speaks Modbus TCP. Your agent connects as a Modbus master:
pip install pymodbus
```

```python
from pymodbus.client import ModbusTcpClient
c = ModbusTcpClient("<IP_ADDRESS>", port=502)
# Agent loop: read process tags, reason, propose bounded setpoint writes
regs = c.read_holding_registers(0, count=10).registers
# -> feed regs + alarm context to LLM -> get proposed action
# -> clamp to safety envelope -> c.write_register(addr, clamped_value)
```

That's the whole thesis in 20 lines: the AI never touches the safety loop, it reasons over the process and proposes bounded actions. Build *that* convincingly and the "AI PLC motherboard" becomes a hardware packaging decision, not a research risk.

References:

- [Unikraft](https://github.com/unikraft/unikraft)
- [smoltcp — Rust TCP/IP stack](https://github.com/smoltcp-rs/smoltcp)
- [Writing an OS in Rust (Phil Opp)](https://os.phil-opp.com/)
- [AIOS: LLM Agent Operating System](https://github.com/agiresearch/AIOS)
- [OpenPLC Project](https://www.openplcproject.com/)
- [Siemens S7-1500 TM NPU](https://www.siemens.com/global/en/products/automation/systems/industrial/plc/simatic-s7-1500/ai.html)
