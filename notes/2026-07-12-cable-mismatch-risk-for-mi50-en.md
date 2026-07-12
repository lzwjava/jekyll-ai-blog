---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cable Mismatch Risk for MI50
translated: false
type: note
---

Question: Does the cable-mismatch theory (CPU 8-pin vs PCIe 8-pin) specifically apply to the two 8-pin cables plugged into the AMD MI50, given that the RTX 4070 was previously powered via a 2×8-pin-to-12-pin adapter cable, while the MI50 uses two native 8-pin connectors directly?

Answer:

This distinction matters a lot — it changes which failure mode is most likely. Let me separate the two setups.

## RTX 4070 setup
`PSU 8-pin cable ×2 → adapter (2×8-pin in, 12-pin/12VHPWR out) → RTX 4070`

The RTX 4070 (non-Ti/Super reference design) uses a 12VHPWR (16-pin) connector. Since your CX650F/CX750F is an older ATX 2.x-generation unit without native 12VHPWR output, you're using the standard Nvidia/AIB-bundled adapter that converts two native 8-pin PCIe PSU cables into one 12VHPWR plug. That adapter's two input sockets are designed to accept **standard PCIe 8-pin pinout** — this is the same pinout your PSU's cables labeled "PCIe" (not "CPU") should provide.

## MI50 setup
`PSU 8-pin cable ×2 → MI50 (two native 8-pin sockets directly, no adapter)`

MI50 also expects standard PCIe 8-pin pinout on both inputs (confirmed spec: 2× 8-pin PCIe, 300W total).

## So — did you reuse the *same* cables, or different ones?

This is the key question I need you to answer, because it determines which failure mode applies:

**Case A — You unplugged the same two cables from the adapter and plugged those same connector ends directly into the MI50.**
If so, my cable-mislabeling theory becomes *less* likely, because those two cables already proved themselves as genuine PCIe-pinout cables (they were feeding a working adapter for the 4070). Unplugging them from the adapter and plugging the same 8-pin ends straight into MI50 is electrically equivalent to what the adapter itself was doing — no mismatch introduced there.

**Case B — You left the 4070's cables on the adapter and grabbed two *different*, previously-unused 8-pin cables from your PSU's cable bag to feed the MI50 directly.**
This is where the risk is real. If either of those "extra" cables is actually the PSU's **CPU/EPS-labeled cable** (used for the motherboard's CPU power header) rather than one of its **PCIe-labeled cables**, plugging it into the MI50 is exactly the mismatch scenario I described — same 8-pin shape, different internal pinout, and Corsair's own documentation is explicit that these are not interchangeable.

## If it's Case A, revise the hypothesis

If you truly reused the same proven-good cables, then the short is less likely to be a pinout mismatch and more likely one of these instead:

- **Connector seated off-by-one-pin or at an angle** — 8-pin PCIe connectors are keyed, but on a used/secondhand MI50 the socket or pins could be slightly worn, bent, or dirty (this card came from server/mining duty), letting a cable seat imperfectly and bridge adjacent pins.
- **Physical damage on the MI50 itself** — used compute cards from decommissioned servers sometimes have damaged VRM components from their prior life; a shorted MOSFET *on the card* could pull the fault back through the 8-pin lines into the PSU/board the instant power is applied.
- **A bent or shorted pin inside the 8-pin socket on the MI50** from shipping/handling, invisible without close inspection with a flashlight.

## What to check right now

1. Physically trace and confirm: at the **PSU end**, are the two cables you plugged into MI50 labeled "PCIe" or "CPU"? This one visual check resolves the ambiguity immediately.
2. If they're confirmed genuine PCIe cables, inspect the **MI50's two 8-pin sockets** closely (flashlight, magnifier) for bent pins, scorch marks, or debris — since the fault may live on the card itself, not the cabling.
3. Also inspect the **cable connector ends themselves** for a bent pin or a socket that didn't seat flush — a partially-inserted 8-pin connector can bridge pins intermittently and cause exactly this kind of buzzing-then-fail-to-boot behavior.

Either way, the diagnostic plan from before still holds: bench-test the motherboard bare-minimum with a different PSU to confirm whether the board itself is now damaged, before doing anything else.

References:

- [Can I use a PCI-e cable in the 8-pin motherboard plug? – Corsair](https://www.corsair.com/us/en/explorer/diy-builder/power-supply-units/can-i-use-a-pci-e-cable-in-the-8-pin-motherboard-plug/)
- [AMD Radeon Instinct MI50 GPU specs – ITCreations](https://www.itcreations.com/amd-gpu/amd-radeon-instinct-mi50-gpu)
