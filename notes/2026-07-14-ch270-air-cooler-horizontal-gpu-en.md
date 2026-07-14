---
audio: false
generated: true
image: false
lang: en
layout: post
title: "CH270: Air Cooler, Horizontal GPU"
translated: false
type: note
---

Question: With the Deepcool CH270 (vertical mATX, rear-connector support, 360mm AIO compatible) locked in, what cooling do I actually buy?

Answer:

The CH270's headline features — vertical GPU riser, 360mm AIO support — don't change the two fundamentals from earlier: R5 5600 needs a modest air cooler, and the MI50 needs its own dedicated shroud fan since it has no cooling of its own. What changes is how they fit *this specific case's* airflow path.

**CPU: skip the 360mm AIO temptation, go air.**

65-88W boost load on a 5600 doesn't need liquid cooling — that headroom is there for people running 105W+ chips. An AIO adds a pump failure point and cost for zero real gain here, and in a vertical case, radiator/pump orientation and tubing bend radius add complexity you don't need.

- **Pick:** Thermalright Peerless Assassin 120 SE (~¥100-150) or ID-Cooling SE-224-XT, same as before — confirm clearance against CH270's side panel spec if it's a windowed vertical case (usually 165-170mm CPU cooler height is fine on this model)

**GPU: the vertical GPU mount changes your shroud fan orientation — check this before buying.**

This is the part specific to CH270. Vertical GPU mounting (via riser cable) typically rotates the card 90°, which changes which direction is "up" for airflow relative to the case's front/side intake. Your MI50 shroud fan needs to draw from wherever the case's fresh intake air actually is post-rotation, not just "front to back" like a standard horizontal mount.

- **Before ordering the shroud:** confirm whether you're actually using CH270's vertical GPU riser or mounting the MI50 horizontally in the standard PCIe slot. If vertical, the card's side panel (normally facing right/left in standard orientation) now faces up/out toward the case's side intake — your shroud duct direction should match that.
- If you mount MI50 **horizontally** (standard slot, skip the vertical riser) — simpler, shroud design stays as discussed, standard front-to-back case airflow feeds it directly. This is the safer option unless you specifically want the aesthetic of vertical GPU display, since the vertical riser mainly benefits GPUs with side-exhaust blower designs, not custom-shrouded compute cards like this.
- **Fan/shroud pick:** unchanged from before — 40mm 12V blower matched to MI50's onboard header spec, mounted in a printed shroud (Thingiverse/MakerWorld designs referenced earlier)

**Case fans:** CH270 likely ships with 1-2 fans stock — add front intake if it doesn't already have 2-3x120/140mm, since that's what feeds both the CPU cooler and (if horizontal) the GPU shroud. Check the box contents; if it only ships with a rear exhaust fan, add 2x front intake fans (~¥80-100 total, any basic 120mm PWM set).

**My recommendation:** mount the MI50 horizontally in the standard slot, skip the vertical riser gimmick for this card, air-cool the CPU with the Peerless Assassin 120 SE, and keep the 360mm AIO mount unused — you don't need it and it adds no value for this workload.
