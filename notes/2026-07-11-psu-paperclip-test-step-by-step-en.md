---
audio: false
generated: true
image: false
lang: en
layout: post
title: PSU Paperclip Test Step-by-Step
translated: false
type: note
---

Question: Walk me through exactly how to do the PSU paperclip test step by step, and what to do based on the result.

Answer:

**Before you start — safety basics**

- Unplug PSU from wall before doing any wiring/shorting. Only flip the switch ON after the paperclip is already inserted and PSU is plugged back in.
- Disconnect the PSU from everything else first: motherboard 24-pin, CPU 4/8-pin, all SATA/PCIe power cables, GPU power. The PSU should be a standalone unit, connected to nothing.
- Do this test on a non-conductive surface (not on a metal case panel).

**Step-by-step**

1. **Fully disconnect the PSU** from the case/motherboard. Pull it out if easy, or at minimum unplug the 24-pin ATX connector and every other cable from motherboard/GPU/drives. The PSU should have no load connected.

2. **Locate the 24-pin ATX connector** (the big one, the main motherboard power cable). Look at the plastic connector housing — pins are numbered, usually printed in tiny text on the plastic, or you can look up the pinout for your PSU brand.

3. **Identify two wires:**
   - **Green wire** = PS_ON# signal (pin 15 or 16 depending on 20 vs 24-pin layout)
   - **Any black wire** = Ground (there are several, any one works)

4. **Bridge them:**
   - Take a straightened paperclip (or a jumper wire, safer/more controlled)
   - Insert one end into the cavity holding the green wire pin, the other end into a cavity holding a black wire pin, on the connector face (not by piercing the wire insulation — insert into the connector housing itself where the pin socket is)
   - Make sure the two ends of the paperclip don't touch anything else metal

5. **Power on:**
   - Plug the PSU's power cable into the wall
   - Flip the PSU's rear power switch to ON (`I` position)
   - The fan should spin up immediately if the PSU is functional

6. **Observe carefully:**
   - Listen — does the buzzing/whining happen again?
   - Watch the fan — steady spin, no stutter?
   - Smell — any burning smell? (If yes, power off immediately, unplug, stop testing)
   - Feel — is it noticeably hot within the first 10-15 seconds? (Should not be, no load is applied)

7. **Power off:**
   - Flip switch OFF, unplug from wall, remove paperclip

**Interpreting the result**

| Result | Meaning | Next step |
|---|---|---|
| Fan spins clean, no buzz, no smell | PSU itself is likely healthy standalone | The buzzing you heard before was probably under *load* from motherboard/GPU — could be coil whine from GPU/VRM, or the PSU struggling under real load (which this test won't reveal since there's no load). Don't rule out PSU yet — see load test below. |
| Buzzing/whining happens even standalone, no load | PSU internal fault (capacitor, transformer coil, switching regulator) | Stop testing repeatedly. Replace the PSU — it's cheap (200-300 CNY) and physically easy: 4 screws mounting it to the case, then unplug/replug all connectors. No soldering needed. |
| Burning smell, smoke, or PSU doesn't power on at all | Dead/dangerous PSU | Stop immediately, don't reuse it, dispose of it, buy new PSU |

**If standalone test is clean but you want to isolate load-related buzzing:**

Do a *minimal load test* instead of full rebuild:
- Reconnect only: 24-pin to motherboard + CPU power connector + nothing else (no GPU, no drives, no RAM even if possible, or minimal RAM)
- Power on via the case's power button (not paperclip this time)
- If buzzing appears now but not in the fully standalone test → likely coil whine from motherboard VRMs or it's a genuine PSU-under-load issue, not resolvable by just isolating PSU
- If it's still silent → add components back one at a time (GPU next) until buzzing reappears — that tells you which component is drawing the noisy load

**Bottom line decision tree for you right now:**

1. Standalone paperclip test → 5 min, zero risk
2. Buzzes standalone → swap PSU yourself, done, cheap, low skill required
3. Silent standalone → do minimal-load test with just CPU+mobo → isolates whether it's PSU-under-load or a downstream component
4. If after 2 tests you still can't pin it down → that's the point to hand it to the shop, because now diagnosis requires equipment (multimeter, load tester) you probably don't have, and further blind trial-and-error risks the expensive parts (GPU, motherboard)
