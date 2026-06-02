---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: NVIDIA GPU Performance Evolution Compared
translated: false
type: note
---

### NVIDIA GPUs: 2010 DirectX 11 Flagships vs. Modern RTX Cards

Around 2010, NVIDIA's top consumer graphics cards supporting DirectX 11 were the **GeForce GTX 480** (launched March 2010, first DX11 card) and **GTX 580** (November 2010, fastest of the era). These were based on the Fermi architecture, with 480–512 CUDA cores, 1.5 GB GDDR5 memory, and ~250W TDP.

Modern comparisons: **RTX 3090** (Ampere, 2020), **RTX 4070** (Ada Lovelace, 2023), and **RTX 4090** (Ada Lovelace, 2022). **No RTX 4090 Ti was ever released**—it was rumored in 2023 but canceled, with no updates even into 2025.

#### FP32 TFLOPS (Theoretical Peak Single-Precision Performance)
This measures raw shader compute power (higher = better theoretical FLOPS).

| GPU          | Architecture | FP32 TFLOPS | Multiplier vs. GTX 480 |
|--------------|--------------|-------------|-------------------------|
| GTX 480     | Fermi       | 1.345      | 1x                     |
| GTX 580     | Fermi 2.0   | 1.581      | 1.18x                  |
| RTX 4070    | Ada         | 29.15      | 21.7x                  |
| RTX 3090    | Ampere      | 35.58      | 26.5x                  |
| RTX 4090    | Ada         | 82.58      | 61.4x                  |

Modern cards deliver **20–60x** the raw FLOPS, thanks to massive core counts (5,888–16,384 shaders), higher clocks, and architectural efficiency.

#### Real-World Performance (Relative to RTX 4090 = 100%)
- **TechPowerUp Relative Performance**: Average across 1,000+ games/benchmarks (1080p/1440p rasterization-focused). Newer architectures excel more in real workloads due to better scheduling, caching, and features like DLSS/RT.
- **PassMark G3D Mark**: Aggregate synthetic benchmark (average user-submitted scores).

| GPU          | TechPowerUp Relative (RTX 4090 = 100%) | PassMark G3D Mark (Avg) | Multiplier vs. GTX 480 (PassMark) |
|--------------|----------------------------------------|--------------------------|-----------------------------------|
| GTX 480     | 6%                                    | ~4,075                  | 1x                               |
| GTX 580     | ~7%                                   | ~4,500                  | ~1.1x                            |
| RTX 4070    | 53%                                   | ~26,900                 | ~6.6x                            |
| RTX 3090    | 58%                                   | ~26,600                 | ~6.5x                            |
| RTX 4090    | 100%                                  | ~38,400                 | ~9.4x                            |

- **Key Insights**:
  - **Theoretical FLOPS overstates gains**: Real performance is "only" **10–17x** faster for RTX 4090 vs. 2010 cards, due to Fermi's inefficiencies (poor caching, high power/heat).
  - In modern games (1440p/4K, DX12 Ultimate, ray tracing): Multipliers are **20–50x+** higher, as old cards struggle with VRAM limits (1.5 GB vs. 12–24 GB) and lack RT/DLSS.
  - Power efficiency: RTX 4090 (450W) is ~4x more perf/W than GTX 480 (250W).
  - Gaming example: In 2010 titles, GTX 480 hit ~60 FPS 1080p high. RTX 4090 does 4K ultra + RT at 200+ FPS today.

**References**:
- [TechPowerUp GTX 480 Specs](https://www.techpowerup.com/gpu-specs/geforce-gtx-480.c268)
- [TechPowerUp GTX 580 Specs](https://www.techpowerup.com/gpu-specs/geforce-gtx-580.c270)
- [TechPowerUp RTX 3090 Specs](https://www.techpowerup.com/gpu-specs/geforce-rtx-3090.c3622)
- [TechPowerUp RTX 4070 Specs](https://www.techpowerup.com/gpu-specs/geforce-rtx-4070.c3924)
- [TechPowerUp RTX 4090 Specs](https://www.techpowerup.com/gpu-specs/geforce-rtx-4090.c3889)
- [PassMark Video Card Benchmarks](https://www.videocardbenchmark.net)
