---
audio: false
generated: true
image: false
lang: en
layout: post
title: Relativity's Second Postulate Verified
translated: false
type: note
---

Question: Yin Wang's substack post ("什么是'光速不变'") argues that Einstein's relativity relies on two logically distinct claims — (1) light speed is independent of the *source's* motion, and (2) light speed is independent of the *observer's* motion — and that (2) is an unverified, counter-intuitive assumption analogous to how sound/water-wave speed *does* change relative to a moving observer. Is he right?

Answer:

He's right about the logical distinction, wrong about the empirical status of claim (2). This is a very old objection (it's essentially the historical fight between Einstein's postulate and Ritz's "emission theory" from 1908-1913), and it was settled by experiment, not by philosophy. Let me break down where the argument holds and where it breaks.

**What he gets right**

The two postulates really are logically independent, and Einstein's 1905 paper does need both:

- Source-independence: `c` doesn't depend on the emitter's velocity.
- Frame-independence (Lorentz invariance): `c` measured by *any* inertial observer is `c`, regardless of the observer's velocity relative to the source or relative to some hypothetical rest frame.

Sound and water waves only satisfy the first, not the second — because they have a physical medium (air, water) that defines a preferred rest frame. Relative to a moving observer, wave speed *does* shift, exactly as Yin Wang describes (and as you'd derive from simple Galilean addition: `v_relative = v_wave - v_observer`).

**Where he's factually wrong**

His claim is: "the observer-independence of light speed 未经实验证实" (unverified by experiment). This is false — it is arguably the *more* rigorously tested of the two postulates, not the less tested one. The reason it feels untested to a casual reader is that people usually only cite Michelson-Morley for "no ether," but there's a specific chain of experiments built to isolate exactly the observer-motion question:

| Experiment | What it isolates | Result |
| --- | --- | --- |
| Michelson-Morley (1887) | Does light speed depend on the *direction* the observer/apparatus is moving through space (Earth's orbital velocity)? | Null — no directional dependence found |
| Kennedy-Thorndike (1932, modern optical-cavity versions) | Does light speed depend on the *magnitude* of the observer's velocity (using unequal arm lengths so Earth's changing orbital speed through the year would show up)? | Directly tests whether light speed is independent of the velocity of the apparatus in different inertial frames; modern resonator versions constrain violations to parts in 10⁻¹⁷–10⁻¹⁸ |
| Ives-Stilwell (1938, modern storage-ring versions) | Transverse Doppler / time dilation as seen by a moving observer relative to a source | Confirms relativistic Doppler formula, which *is* observer-frame invariance under a different guise |
| De Sitter double-star (1913) + Brecher (1977) X-ray version | Source-velocity dependence specifically (rules out `c' = c + kv` emission theories) | De Sitter showed Ritz's variable-speed-of-light theory would have predicted binary star orbits appearing more eccentric than observed, and this was confirmed by Brecher in 1977 |

So Michelson–Morley + Kennedy–Thorndike together are *precisely* the pair of experiments that test "does the observer's own motion change the measured speed of light" — MM tests directional dependence, KT tests magnitude dependence. Recent GRAAL-ESRF work using accelerated 6 GeV electrons pushed the Kennedy-Thorndike bound to an accuracy better than existing KT-limits by three orders of magnitude, yielding 7.1×10⁻¹². Both null-result classes are consistent with SR to extraordinary precision, and inconsistent with any Galilean-style "medium-relative" picture.

**Why the intuition fails**

Your intuition (and Yin Wang's) about sound is correct *because sound has a medium*. The entire content of relativity's second postulate is the claim "light in vacuum has no medium" — i.e., there's no preferred rest frame to be moving relative to. Michelson-Morley is literally the experiment that checks this: if there were an aether, Earth's ~30 km/s orbital motion through it should show up as a seasonal, direction-dependent shift in interferometer fringes. It doesn't, to 1 part in 10¹⁷ in modern rotating-resonator versions.

**The math, not just the wave analogy**

Under a Galilean transform, velocities add linearly:

```python
def galilean_velocity_add(u, v):
    # observer moving at v, wave/object moving at u in ground frame
    return u - v  # naive subtraction, matches sound intuition

print(galilean_velocity_add(343, 343))  # sound: 0 relative speed if you match its speed
```

Under a Lorentz transform, they don't — and light speed is a fixed point of the transformation regardless of `v`:

```python
def lorentz_velocity_add(u, v, c=299792458):
    # relativistic velocity addition formula
    return (u - v) / (1 - u*v/c**2)

c = 299792458
for v in [0, 1e7, 1e8, 2.9e8]:          # observer velocities, up to near-c
    print(v, lorentz_velocity_add(c, v, c))
# -> always prints c, no matter what v is
```

That invariance under boost isn't an assumption bolted onto the theory for convenience — it's the direct algebraic consequence of deriving the Lorentz transform from "laws of physics look the same in every inertial frame" + "light speed is `c` in at least one frame," and then requiring self-consistency (this is literally the derivation in Einstein's 1905 §3, and it's what MM/KT experimentally validate). If postulate 2 were false, you'd expect `lorentz_velocity_add` to return something other than `c` depending on `v`, exactly like the Galilean case does for sound — and that's the specific thing Kennedy-Thorndike-type experiments have ruled out to 10⁻¹⁷ precision.

**Bottom line**

Yin Wang's conceptual move — separating "independent of source" from "independent of observer" — is a genuinely useful pedagogical clarification that most popularizations blur. But his specific factual claim, that the observer-independence is untested, is wrong; it's the more heavily and more precisely tested half of the two postulates, via a distinct family of experiments (MM, KT, Ives-Stilwell) built for exactly that purpose, going all the way to modern optical-resonator tests at the 10⁻¹⁷–10⁻¹⁸ level. This is the kind of claim in his newsletter series you should stress-test against primary experimental literature, not just his internal reasoning about Einstein's paper — the paper's internal logic and its experimental confirmation are two separate questions, and he's conflating "I find this hard to derive cleanly from Einstein's exposition" with "this is unverified."

References:

- [Kennedy–Thorndike experiment - Wikipedia](https://en.wikipedia.org/wiki/Kennedy%E2%80%93Thorndike_experiment)
- [The light speed vs the observer: Kennedy-Thorndike test from GRAAL-ESRF (arXiv)](https://arxiv.org/abs/1807.08551)
- [De Sitter double star experiment - Wikipedia](https://en.wikipedia.org/wiki/De_Sitter_double_star_experiment)
- [Emission theory (relativity) - Wikipedia](https://en.wikipedia.org/wiki/Emitter_theory)
- [Yin Wang, 什么是"光速不变"](https://yinwang1.substack.com/p/50f)
