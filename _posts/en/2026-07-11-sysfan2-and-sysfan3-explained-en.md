---
audio: false
generated: true
image: false
lang: en
layout: post
title: SYS_FAN2 and SYS_FAN3 Explained
translated: false
type: note
---

Question: What do the SYS_FAN2 and SYS_FAN3 headers mean on this MSI motherboard?

Answer:

`SYS_FAN2` and `SYS_FAN3` are two of four **4-pin system/chassis fan headers** (`SYS_FAN1~4`) on the board, used to power and control case fans — as opposed to `CPU_FAN1` (CPU cooler) and `PUMP_FAN1` (AIO pump).

**Pinout (4-pin):**

| Pin | PWM Mode | DC Mode |
| --- | --- | --- |
| 1 | Ground | Ground |
| 2 | +12V | Voltage Control |
| 3 | Sense (RPM feedback) | Sense |
| 4 | Speed Control Signal | NC |

**Electrical/mode specs:**

| Connector | Default mode | Max current | Max power |
| --- | --- | --- | --- |
| `CPU_FAN1` | PWM | 2A | 24W |
| `PUMP_FAN1` | PWM | 3A | 36W |
| `SYS_FAN1~4` | **DC mode** | 2A | 24W |

Key detail: `SYS_FAN1~4` default to **DC mode**, not PWM. That means MSI controls their speed by varying the 12V rail voltage (pin 2), not via a PWM duty-cycle signal on pin 4. If you plug in a 4-pin PWM fan expecting pin-4 PWM control, it may just spin at a fixed/near-max speed until you flip it to PWM mode.

**Where to change this:** BIOS → Hardware Monitor panel, per-fan setting to switch between DC/PWM mode and enable/disable Smart Fan (temperature-curve) control. If a 3-pin DC-only fan is plugged into a header left in PWM mode (or vice versa), speed control won't behave correctly — always match the fan's actual signal type to the header mode in BIOS.

**Physical location:** on this board's layout, `SYS_FAN1` sits near the bottom edge (below `JCI1`), and `SYS_FAN2`/`SYS_FAN3` are clustered near the right-side USB headers (`JUSB1`/`JUSB2`), with `SYS_FAN4` up near the DIMM slots/`ATX_PWR1` area — so which physical fan you cable to which header is mostly about cable routing/reach, not a functional difference (all four are equivalent DC-mode headers).

References:

- [MSI MAG B760M MORTAR WIFI II User Guide (PDF)](https://gzhls.at/blob/ldb/8/2/2/3/f5692b3e4562b5b05ac5b7fe142b249bca4e.pdf)
- [MSI MAG Series Motherboard User Guide](https://manuals.plus/m/253c081013a7d1d08c025f4e32d8538557f50913ffc8b0ccddc406969d425e32)
