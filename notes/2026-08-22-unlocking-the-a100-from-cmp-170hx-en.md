---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unlocking the A100 from CMP 170HX
translated: false
type: note
---

I've explored the whole codebase. Here's the **why it can unlock** explanation.

## The core claim

The CMP 170HX and the A100 datacenter GPU are the **same GA100 silicon die**. The restriction is not missing hardware — it's artificial: OTP fuses burned at the factory and a firmware-enforced **Platform Lock Manager (PLM)** that rejects certain register writes. This project doesn't add anything; it finds a way to make the chip's *own* firmware unlock its *own* registers on hardware you own.

## The root cause — a boot-time bug

The key is a bug in the Falcon BootROM (the GSP secure-boot processor), verified by the emulator in `tests/test_bootrom_bug.py`:

1. The driver loads the GSP firmware ELF, which contains a plain `.fwsignature_ga100` section.
2. **The bug:** the BootROM copies that section's content into DMEM (its own data/program memory) at offset `0x800` **before** it verifies the AES-decrypted HMAC signature. So code can run in a context (HS-mode) that supposedly requires a valid signature.
3. Because the patched code executes *before* signature verification, the exploit **doesn't even need the AES key** — the verification that would stop it happens too late.

## The injection — a 63KB ROP chain

Since the section is executed as code before being validated, the project replaces its content with a hand-built ROP (return-oriented programming) chain. `build.py` / `fill_payload()` constructs a 63KB buffer (`0xF800`) full of a NOP pattern with a 24-DWORD ROP chain placed at known offsets, with canaries (`0xc0deca7e`) and runtime-filled slots for the target BAR0 address and value.

The ROP chain's job is a single primitive: **write one 32-bit value to one BAR0 address**. The BAR0 (base address register) region is where the GPU's PLM registers live, and the emulator confirms the mechanism (the `mpopaddret` gadget pops `value/addr/RA` off the DMEM stack and issues the write).

## Opening the lock — four PLM writes

The reason the whole chip is locked to 10GB is that the Platform Lock Manager blocks `CFG1` (HBM geometry) / `LMR` (memory rank) / `SS0/SS1` (compute speed) writes until it's unlocked. That unlock isn't one register — the code opens **4 PLM registers** in sequence (`plm_table` in `constants.yaml`):

- `WPR_CFG`, `FBPA`, `WPR`, `FEAT`

Each requires re-patching the signature section with a fresh ROP payload targeting that address, reloading the driver to trigger the BootROM, and confirming the write "stuck". Only after all 4 PLMs are open will the HBM controller accept the real unlock values.

## The unlock itself — turning features on

With the PLM opened, the pipeline writes (via BAR0, `bar0.py` → memory-mapped `/sys/bus/pci/devices/.../resource0`):

| Address | Value | Effect |
|---|---|---|
| `SS0 / SS1` | `0x88888888`, `0x00000008` | **Compute**: removes the SM clock cap → full A100 throughput |
| `CFG1` | `0x02669000` | Memory geometry: changes the per-stack strap so all the physically-present HBM2e is addressed |
| `LMR` | `0x00000028A` | Memory rank config |

Decoding `CFG1` (`decode_cfg1`): the `strap` field (0x66) for `strap=0x66 → 8GB/stack`, `feature=0x90 → 5 stacks`, so 5×8GB = **40GB** in the verified target (80GB uses the same cfg and is unverified).

Crucially, these memory values just tell the controller to use all the HBM2e that's already physically wired in — the "capacities" P weren't removed; they were just hidden by the strap/lock.

## Why it stays stealthy and why it persists

After the unlock writes, `pipeline.py` **restores the original GSP signature** from a backup so the driver doesn't detect tampering, then reloads normally — the unlocked state persists through the driver session.

It's **volatile** (lost on power cycle / driver reload), so a systemd daemon (`daemon/watchdog.py`) re-applies it every second and after every boot or driver reload.

## Bottom line

It can unlock because:
1. **Same hardware** — CMP100HX = A100 silicon, so the physical 16GB HBM stacks and compute units are all present.
2. **A firmware ordering bug** lets unsigned code execute in a privileged HS-mode before signature verification.
3. **A minimal ROP payload** can then perform arbitrary BAR0 writes.
4. **The PLM gates** its own unlock via 4 registers; once opened, the real memory/compute unlock values (community-verified) are written.
5. The lock is ultimately **software/configuration**, not hardware — so changing those registers reveals full capability.

One caveat: several of the feature unlocks (PCIe v4, NVLink, ECC) are explicitly documented as *unverified community guesses* — the compute and memory unlocks are the solid, verified part.
