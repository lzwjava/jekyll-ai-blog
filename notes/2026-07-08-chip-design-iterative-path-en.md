---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chip Design Iterative Path
translated: false
type: note
---

Question: Given my background (top-300 in Guangdong NOIP, then self-taught across Android/iOS/frontend/backend/English/AI), learning chip design shouldn't be hard for me either. Should I find real chip experts, do small iterative experiments across inference and training chips, and start with something as simple as a basic adder chip?

Answer:

Partial agreement, with one correction to the framing: chip design is not "another language to pick up" the way iOS→Android→backend was. Those are all software-on-von-Neumann-hardware transfers — same abstraction stack (compiler, OS, instruction set), different syntax. Digital IC design is a different physical stack: gates → standard cells → place-and-route → timing closure → DRC/LVS → GDSII → mask → fab. The learning curve isn't steep because the concepts are hard (an adder is trivial), it's steep because the *toolchain* has more failure modes than any software stack you've touched, and you can't `print`-debug silicon after tapeout.

That said, your instinct is directionally right and more achievable in 2026 than at any point in history. Here's why, and here's the actual path.

**Why an adder-first, iterative approach is correct**

You already think this way from nanochat/GPT-2-from-scratch: start with the smallest thing that can be end-to-end verified, then scale complexity. Same discipline applies to silicon:

1. Full adder in Verilog → simulate in `iverilog`/`cocotb`
2. Ripple-carry adder → same
3. Synthesize to gates (Yosys) → look at the netlist
4. Place-and-route on an open PDK (OpenROAD/LibreLane) → look at the actual layout
5. Submit to a real shuttle (Tiny Tapeout) → get silicon back

This mirrors exactly your GPT-2-from-scratch approach: don't jump to DeepSeek v4 MoE, build the smallest transformer that trains first.

**The toolchain that makes this actually feasible now**

This is the part worth knowing precisely, because five years ago this whole stack didn't exist as an accessible thing:

- **Yosys** — open-source RTL synthesis (Verilog → gate-level netlist)
- **OpenROAD / LibreLane** — automated place-and-route, targeting a no-human-in-the-loop 24h flow
- **Open PDKs** — SkyWater 130nm (Google-sponsored), GlobalFoundries 180nm, IHP SG13G2 130nm — these are the actual fab process design kits, open source, which is the part that used to require an NDA and six figures
- **Tiny Tapeout** — multi-project wafer shuttle service that tiles hundreds of tiny designs onto one shared die, dropping cost from ~$10k+ to low hundreds of dollars per project

Concretely: thanks to open-source EDA tools like LibreLane and OpenROAD, open-source PDKs from Google (SkyWater 130nm, GlobalFoundries 180nm, IHP 130nm), and low-cost shuttle programs like Tiny Tapeout that multiplex hundreds of designs onto shared chips, independent designers can now tape out custom ASICs without bankruptcy. There's a documented case of a solo engineer taping out a full BLAKE2s hashing accelerator on the SKY130A process entirely alone, and another building a small systolic array (the actual building block of a matmul/training accelerator) as a Tiny Tapeout submission, explicitly using shuttle programs as a harness while mastering the missing skills toward eventually taping out a chip fully independently.

Current shuttle status if you want to look at real timelines: Tiny Tapeout IHP 26a launched November 2025, closed submissions March 2026, with chips expected back September 2026 — so budget ~6-9 months from submission to physical chip in hand. There's also a SKY 26b shuttle that launched April 2026 and closed submissions May 2026. Note the IHP shuttles now come with restrictive loan terms (chip stays property of IHP, no commercial use, no reselling) — the SkyWater shuttles are the ones where you actually own what you make, so check terms per shuttle before committing a design to one.

**Where "inference chip" vs "training chip" breaks your plan**

Be honest with yourself about scope here, because this is where the analogy to your software stack transfer breaks down hardest:

- A **toy adder/ALU on Tiny Tapeout** — genuinely doable solo in weeks, real silicon back in months. Good learning project.
- A **real inference accelerator** (something that beats a CPU at INT8 matmul) — needs a systolic array, SRAM for weights, a memory interface, and enough area/power budget to be non-toy. Doable as a hobby-scale demonstrator (see the systolic array example above — 2x2 array, deliberately small to be a good shuttle citizen).
- A **training chip** — needs high-precision FP arithmetic, gradient accumulation, and crucially HBM-class memory bandwidth. This is not a solo weekend project or even a solo year project — it's the domain of Groq/Cerebras/Tenstorrent-scale teams, hundreds of millions in NRE (non-recurring engineering) cost for a real process node, and access to bleeding-edge (not open) PDKs. Your MI300X exposure gives you real intuition for *why* this is hard (HBM bandwidth, memory-compute ratio) — use that intuition to correctly size the gap between "toy ASIC" and "real training chip," don't let the surface-level narrative of "I learned iOS and Android, chips are just another domain" collapse that gap.

**Practical recommendation given your actual constraints (mortgage, 12-month service-company runway, no chip revenue path)**

Chip design is a legitimate 20%-energy product bet, not a Phase 1 revenue lever. There is currently no Guangzhou/GBA/HK client paying you to tape out ASICs — your paying skill surface is model training, fine-tuning, agent infra, LLM tooling. Treat chips the way you're treating nanochat: a compounding skill investment, sequenced behind revenue, not a pivot.

Concrete starting point I'd actually recommend this week:

```bash
# Yosys + a full adder, verified in simulation, on your RTX 4070 box or even the Air
sudo apt install yosys iverilog
mkdir chip-101 && cd chip-101
cat > adder.v << 'EOF'
module full_adder(input a, b, cin, output sum, cout);
  assign sum  = a ^ b ^ cin;
  assign cout = (a & b) | (cin & (a ^ b));
endmodule
EOF
yosys -p "read_verilog adder.v; synth; show" adder.v
```

Then follow the Tiny Tapeout Verilog template (basic Wokwi template if you want zero-friction, raw HDL if you want to actually learn the flow) and target the current open SKY shuttle. That's your "GPT-2 760M from scratch" equivalent for silicon — small, complete, end-to-end, real hardware out the other side.

References:

- [Tiny Tapeout](https://tinytapeout.com/)
- [BLAKE2s Hashing Accelerator: A Solo Tapeout Journey](https://essenceia.github.io/projects/blake2s_hashing_accelerator_a_solo_tapeout_journey/)
- [Two weeks until tapeout — systolic array project](https://essenceia.github.io/projects/two_weeks_until_tapeout/)
- [Tiny Tapeout IHP 26a shuttle status](https://tinytapeout.com/chips/ttihp26a/)
- [Tiny Tapeout SKY 26b shuttle status](https://tinytapeout.com/chips/ttsky26b/)
- [Tiny Tapeout IHP shuttle loan terms change](https://www.hackster.io/news/tiny-tapeout-opens-an-ihp-shuttle-for-your-open-source-chip-designs-but-beware-the-new-terms-77e0b292cae4)
