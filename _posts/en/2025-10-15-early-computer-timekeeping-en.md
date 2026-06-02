---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Early Computer Timekeeping Before Unix
translated: false
type: note
---

Yeah, you're spot on—long before Unix timestamps in the 1970s, we had these hulking early machines like ENIAC (I think you meant that instead of ANNIC; it was the Electronic Numerical Integrator and Computer from 1945), the Altair 8800 (the 1975 kit that kicked off the PC revolution, where Bill Gates and Paul Allen hacked together that famous BASIC interpreter over teletype), and John von Neumann's foundational ideas (like his 1945 EDVAC report that birthed the stored-program concept influencing everything after).

But "handling time" back then? Nothing like our seconds-since-epoch elegance. These beasts didn't have real-time clocks (RTCs) for dates or wall-clock time baked in—they were all about raw computation cycles, not scheduling your dentist appointment. Time was super basic: mostly internal clocks for syncing operations, or software hacks like loop counters for delays. No persistent memory for "now it's October 15, 2025." Let's break it down quick for each, from the number-crunching angle.

### ENIAC (1945): Pulse Trains and a Master Clock
This 30-ton monster was programmed by plugging in cables and flipping switches—no code storage, just wiring for math problems like ballistics tables. Time handling was all hardware-timed:
- **Clock basics**: A central "cycling unit" oscillator pumped out pulses at 100,000 per second (every 10 microseconds). Everything synced to these—like a heartbeat for the vacuum tubes.
- **Operation timing**: An addition took 20 pulses (200 microseconds, or 1/5,000th of a second). Loops or delays? You'd wire repeaters or counters manually; no software timers.
- **Real-world time?** Zilch. It ran ballistic calcs in 30 seconds that took analog machines 15 minutes, but "time" meant cycle counts, not calendars. Von Neumann consulted on it but pushed for stored programs to make timing more flexible.

From a numbers view: Think of it as fixed-rate ticks (100kHz), where you'd tally pulses for "how long" a calc ran—kinda like crude seconds, but you'd have to count 'em by hand if debugging.

### Altair 8800 (1975): Crystal Clock and DIY Delays
The Altair was the first "personal" computer—a blinky box with an Intel 8080 chip, no keyboard or screen at first (just switches and LEDs). Gates' 4K BASIC loaded via tape, letting hobbyists poke around.
- **Clock basics**: A 2 MHz crystal oscillator drove the CPU—steady ticks at 2 million cycles/second for fetching/executing instructions.
- **Timing tricks**: No built-in clock for dates; you'd add a "Time Clock" accessory board (88-ACC) for basic interrupts or counters. Otherwise, software loops: e.g., a FOR-NEXT loop in BASIC to burn cycles for delays (like `FOR I=1 TO 1000: NEXT I` for a rough "pause").
- **BASIC's take**: Early Altair BASIC had no TIME$ function (that came later in Microsoft BASIC). Time was relative—count instructions or hook external hardware like a real-time clock chip (rare add-on).

Numbers-wise: At 2 MHz, one instruction might take 4-20 cycles, so a 1-second delay? Loop ~2 million times. Brutal, but it taught us efficiency.

### Von Neumann's Architecture (1945+): Cycles as the Universal Tick
Von Neumann didn't build hardware (that was IAS machine in 1952), but his blueprint—CPU, memory, I/O all talking via a bus—set the stage. Time? All about synchronized cycles.
- **Clock role**: A master clock (crystal or otherwise) pulses to fetch-decode-execute instructions. Each cycle (rising/falling edge) advances the state—no overlap, pure serial.
- **Time rep**: Instructions took fixed cycles (e.g., add in 1-4 ticks), so "time" was cycle counts. For delays, branch on counters; real clocks were external (like wall plugs or manual resets).
- **Legacy**: This bottleneck (data/instructions sharing the bus) still haunts us—AI hates it 'cause moving data takes way more cycles than crunching.

In equation terms: Total time = (instructions × cycles/instr) / clock freq. For IAS (von Neumann-inspired): ~1 MHz clock, so 1 million ops/sec tops—your 1.76B seconds? That'd be ~55 years of non-stop IAS churning, but it'd melt first.

These setups were wild precursors to Unix's epoch—time as a counter, but you built it yourself. If you wanna dive deeper (like code snippets for Altair delays), hit me!

[ENIAC Wikipedia](https://en.wikipedia.org/wiki/ENIAC)
[A Report on the ENIAC](https://ftp.arl.army.mil/mike/comphist/46eniac-report/chap1.html)
[Electronic Computing Circuits of the ENIAC](https://archive.computerhistory.org/resources/text/Knuth_Don_X4100/PDF_index/k-8-pdf/k-8-r5367-1-ENIAC-circuits.pdf)
[Organization of the Altair 8800](https://ubuntourist.codeberg.page/Altair-8800/part-2.html)
[MITS Altair 8800 Brochure](https://vtda.org/docs/computing/MITS/MITS_Altair8800ComputerSystem_Brochure.pdf)
[Von Neumann Architecture - Wikipedia](https://en.wikipedia.org/wiki/Von_Neumann_architecture)
[In a simple Von Neumann architecture, what exactly is a clock cycle?](https://www.quora.com/In-a-simple-Von-Neumann-architecture-what-exactly-is-a-clock-cycle)
