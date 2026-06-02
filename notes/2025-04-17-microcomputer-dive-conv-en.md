---
audio: true
layout: post
title: Microcomputer Dive - Conversation
type: note
---

A: I’ve been revisiting microcomputer architecture lately. Can we start by comparing von Neumann and Harvard architectures?

B: Absolutely! Von Neumann uses a single bus for both data and instructions, which can cause bottlenecks. Harvard separates them, enabling parallel fetches—common in DSPs and microcontrollers. Which use case interests you more?

A: Embedded systems, actually. Harvard seems dominant there. But how do modern hybrids like modified Harvard architectures bridge the gap?

B: Great question! Hybrids use split caches (L1 for instructions/data) but a unified memory space. Take ARM Cortex-M: it’s Harvard-like for speed but simplifies programming. Trade-offs?

A: Trade-offs indeed. Unified memory eases development but sacrifices throughput. Do you think RISC-V’s flexibility could disrupt this space?

B: Potentially! RISC-V’s modular ISA lets designers add Harvard-like features per application. For IoT edge devices, that’s a game-changer. But ARM’s ecosystem is entrenched. What’s your take?

A: Ecosystems are sticky, but RISC-V’s open-source model could accelerate niche optimizations. Shifting gears—how critical is DMA in modern microcontrollers?

B: Crucial! Offloading data transfers (e.g., ADC to memory) saves CPU cycles. STM32’s DMA even handles peripheral-to-peripheral transfers. Ever worked with circular DMA buffers?

A: Yes, for audio processing. But configuring burst modes was tricky. How does DMA prioritize requests when multiple peripherals compete?

B: Priority is typically hardware-configurable. NXP’s MCUs use weighted round-robin, while some TI parts allow dynamic reprioritization. Interrupt latency becomes a factor—ever measured it?

A: Only empirically. Speaking of interrupts, how do RTOSes like FreeRTOS handle nested ISRs differently from bare-metal?

B: RTOSes add layers: context saving, scheduler invocations post-ISR. FreeRTOS’s ‘FromISR’ APIs manage this safely. But bare-metal ISRs are leaner—trade-off between complexity and control.

A: Makes sense. For hard real-time systems, would you ever recommend a superloop over an RTOS?

B: Only for trivial systems! Superloops struggle with multi-rate tasks. A properly tuned RTOS with priority inheritance avoids priority inversion. Zephyr’s recent improvements are worth exploring.

A: Zephyr’s device tree model is intriguing. How does it compare to Linux’s for embedded use?

B: Linux’s DT is heavyweight for microcontrollers. Zephyr’s Kconfig + devicetree strikes a balance—static configuration reduces runtime overhead. Ever ported a driver across both?

A: Not yet, but I’ve seen Zephyr’s GPIO API abstracts hardware quirks well. What’s your view on memory-mapped vs. port-mapped I/O for micros?

B: Memory-mapped dominates now—unified addressing simplifies compilers. x86’s legacy port I/O lingers for backward compatibility. ARM’s MMIO even handles bit-banding for atomic access!

A: Bit-banding’s a lifesaver for shared variables! But what about emerging non-volatile RAM like MRAM? Could it disrupt the memory hierarchy?

B: MRAM’s persistence + speed is promising, but cost/endurance lags. For now, it’s niche—think spacecraft logging. NVDIMMs might hit micros sooner. Ever benchmarked FRAM vs. Flash?

A: Yes—FRAM’s write speed blows Flash away, but density’s an issue. Switching to interfaces: is SPI losing ground to I3C in sensor hubs?

B: I3C’s multi-drop and in-band interrupts are compelling, but SPI’s simplicity keeps it alive. MEMS sensors still default to SPI. Have you tried I3C’s dynamic addressing?

A: Not yet—my current project uses QSPI for external NOR Flash. Speaking of storage, how does eMMC compare to SD cards for industrial temps?

B: eMMC’s soldered reliability trumps SD’s connectors in vibration-prone environments. But SD’s removable for field updates. SLC NAND remains king for longevity. Ever hit wear-leveling bugs?

A: Once—a bad FTL implementation bricked a logger. Let’s talk security: how are micros handling Spectre/Meltdown mitigations?

B: Cortex-M33’s TrustZone helps, but timing attacks still haunt caches. Silicon vendors are adding speculative execution barriers. Rust’s borrow checker could prevent some exploits—are you adopting it?

A: Experimentally—the learning curve’s steep. Back to hardware: any thoughts on RISC-V’s vector extensions for DSP workloads?

B: RVV’s modularity is brilliant! It’s like ARM NEON but scalable. For tinyML, it could displace proprietary DSP cores. Seen any benchmarks vs. Cadence Tensilica?

A: Not yet, but I’m eyeing a RISC-V + RVV MCU for motor control. Which brings me to PWM peripherals—how crucial is dead-time insertion in hardware?

B: Vital for H-bridges! Software timers can’t match nanosecond precision of dedicated blocks. ST’s HRTIM is overkill for most, though. Ever used a CPLD for custom PWM?

A: Once—synchronized 16 channels for LED matrices. But modern MCUs like the RP2040’s PIO are stealing that niche. How programmable is too programmable?

B: PIO’s a game-changer! But debugging state machines gets hairy. XMOS’s xCORE still wins for hard real-time multi-cores. Where do you draw the line between MCU and FPGA?

A: When latency demands sub-microsecond determinism, FPGAs rule. But Lattice’s iCE40 + RISC-V soft cores blur the lines. Ever tried Chisel for hardware/software co-design?

B: Chisel’s productivity boost is unreal—generating Verilog from Scala saves months. But the toolchain’s still maturing. Speaking of trends, how will chiplet-based micros evolve?

A: Chiplets could let us mix-and-match RISC-V cores with analog chiplets. But interposer costs must drop. TSMC’s 3D fabric is promising. Will we see open-source chiplets?

B: Google’s OpenMPW hints at it! But EDA tools remain a barrier. Meanwhile, analog’s still a dark art—how’s your team handling mixed-signal validation?

A: Lots of SPICE + Python co-simulation. But back to digital: any thoughts on memristor-based micros for neuromorphic computing?

B: Still lab curiosities—variability kills yield. But for edge AI, analog compute-in-memory arrays (like Mythic’s) are closer to production. Ever benchmarked them against quantized NN accelerators?

A: Not yet, but I’m skeptical about analog’s precision. Shifting to power: how low can subthreshold CMOS designs realistically go?

B: Ambiq’s Apollo4 hits ~6µA/MHz! But leakage dominates below 28nm. Energy harvesting’s the next frontier—Ever used a PMIC like the BQ25504?

A: Yes—solar + supercaps for a weather station. But MPPT algorithms need tuning. Final question: will quantum co-processors ever integrate with micros?

B: Decades away for anything practical. But cryo-CMOS interfaces are being researched! For now, I’m more excited about photonic interconnects in microservers. Thanks for the deep dive!
