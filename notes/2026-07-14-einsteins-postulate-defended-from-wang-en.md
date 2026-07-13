---
audio: false
generated: true
image: false
lang: en
layout: post
title: Einstein’s Postulate Defended from Wang
translated: false
type: note
---

Question: Is Wang Yin right that Einstein's "light speed invariance" postulate has two separate meanings — invariance w.r.t. the *source* (which Wang accepts, MM-consistent) and invariance w.r.t. the *observer* (which Wang says is an unproven, "sneaked in" assumption — and that this is the actual flaw in special relativity?

Answer: No — the observer-independence claim is not an untested add-on. It's been directly measured, and Wang's framing misreads what Michelson-Morley already shows.

**The conceptual split he's making is real, but not novel — SR's second postulate already states both halves at once:**

> "light is always propagated in empty space with a definite velocity c which is independent of the state of motion of the emitting body" — Einstein, 1905

Source-independence is the easy half (matches wave physics — water/sound waves don't inherit the emitter's velocity). The hard, counter-intuitive half is that it's *also* independent of the observer's motion. Wang's article says this second half is "未经实验证实" (not experimentally verified). That's just wrong, and it's wrong in a checkable way:

**1. Michelson-Morley already tests observer-velocity independence, not just isotropy.**

The MM apparatus itself is the moving observer — Earth orbits the Sun at ~30 km/s, so the interferometer's rest frame changes velocity over a year and with rotation. If light speed depended on the observer's velocity the way Wang's train-example intuition predicts (Galilean addition: c ± v), you'd get a fringe shift as the apparatus's velocity vector rotates relative to the presumed ether. Null result → light speed measured by a moving observer doesn't depend on the observer's velocity, at least to first order in v²/c². That's exactly the claim Wang says is untested.

**2. Kennedy-Thorndike (1932) closes the loophole MM leaves open.**

MM alone is explainable by length contraction alone (Lorentz-Fitzgerald), without needing time dilation — because both arms are equal length, a v²/c² time-dependent effect could in principle cancel out. KT deliberately makes the arms unequal length. A null result here requires *time dilation in addition to length contraction* — you cannot explain it away with pure geometry. This is a direct, dedicated test of "does c depend on the observer's velocity," and the answer is no to a limit of 7×10⁻¹² in modern Compton-edge-based reruns at ESRF's GRAAL experiment, three orders of magnitude tighter than earlier bounds. Wikipedia's summary states it directly: "While the Michelson–Morley experiment showed that the speed of light is independent of the orientation of the apparatus, the Kennedy–Thorndike experiment showed that it is also independent of the velocity of the apparatus in different inertial frames."

**3. Why the math "feels like a trick" — because the resolution isn't a trick, it's giving up absolute simultaneity.**

Your train intuition (light source moving with the train → for the platform observer, speed still c; for you on the train, if speed depended on your own motion you'd expect c ± v) is precisely the Galilean addition-of-velocities assumption. Einstein's actual move: instead of patching velocity addition, he derives that *simultaneity itself is frame-dependent*. Sketch:

```
Two postulates:
  P1: physics is the same in all inertial frames
  P2: c is the same in all inertial frames (source AND observer)

From P1+P2, requiring x² + y² + z² - c²t² invariant under a linear
transform between frames S and S' moving at v along x:

  t' = γ(t - vx/c²)
  x' = γ(x - vt)
  γ = 1/√(1 - v²/c²)

Velocity addition (not Galilean u' = u - v, but):
  u' = (u - v) / (1 - uv/c²)

Plug in u = c:
  u' = (c - v)/(1 - vc/c²) = (c - v)/((c-v)/c) = c
```

That's the whole "trick" — it's not smuggling in observer-invariance as an extra unjustified axiom, it's the *unique* transform consistent with both postulates. The Lorentz factor γ isn't decoration, it's what makes "c is the same for source and observer simultaneously" non-contradictory: your clock runs slow and your ruler contracts (from the other frame's view) by exactly the amount needed to keep the ratio distance/time = c invariant.

**4. Additional independent confirmations beyond MM/KT:**
- Ives-Stilwell (1938) — direct measurement of relativistic time dilation via transverse Doppler shift in fast-moving ion beams.
- Alväger et al. (1964, CERN) — photons from decaying π⁰ mesons moving at 0.99975c measured at c to within 400 ppm — this is the direct source-velocity test, ruling out any "ballistic"/emission theory where γ speed = c + v_source.
- GPS satellite clock corrections — both special-relativistic time dilation and general-relativistic gravitational time dilation are engineered in; if observer-frame invariance of c were wrong, GPS positioning would drift by kilometers per day.

**Bottom line:** Wang Yin correctly identifies that people conflate the two invariances, and that's a fair pedagogical point — most textbooks are sloppy about it. But his conclusion, that the observer-independence half is an *unverified assumption* Einstein snuck in, is factually false. It's the specific thing MM/KT-type experiments were designed to test, and it's held up to 10⁻¹² precision. Wang Yin is a programmer/PL-design blogger known for contrarian takes across many fields (education, politics, Lisp/Haskell, now physics) — worth reading for the "make you re-derive it yourself" value, but this particular claim doesn't survive contact with the experimental literature.

References:
- [Kennedy–Thorndike experiment - Wikipedia](https://en.wikipedia.org/wiki/Kennedy%E2%80%93Thorndike_experiment)
- [The light speed vs the observer: the Kennedy-Thorndike test from GRAAL-ESRF (arXiv:1807.08551)](https://arxiv.org/abs/1807.08551)
- [Michelson–Morley experiment - Wikipedia](https://en.wikipedia.org/wiki/Michelson%E2%80%93Morley_experiment)
- [什么是"光速不变" - Yin Wang](https://yinwang1.substack.com/p/50f)
- [Test of the Second Postulate of Special Relativity in the GeV Region — Alväger et al. 1964](https://cds.cern.ch/record/342806)
