---
audio: false
generated: true
image: false
lang: en
layout: post
title: Friend Correct on Light Speed Invariance
translated: false
type: note
---

Question: Yin Wang claims that (1) making relative light speed equal to c in all directions via the Lorentz transformation is just "cooking the numbers" (凑答案) rather than a real physical/mathematical fact, and (2) Einstein only ever checked this for one direction of light, so a transformation that correctly gives c in every direction "doesn't exist, not even mathematically." A friend counters that c-invariance is the postulate, not something derived — do I agree with Yin Wang's math claim or the friend's framing?

Answer:

The friend is right on logical structure, and Yin Wang's specific mathematical claim is checkably false. This isn't a matter of interpretation — it's a computation you can run.

**The postulate direction (friend is correct)**

Special relativity's logical order is:

1. Postulate: `c` is the same in every inertial frame, in every direction (this + the relativity principle is the axiom, not a conclusion)
2. Derive the Lorentz transformation as *the unique* linear transformation consistent with that postulate
3. Time dilation, length contraction, relativity of simultaneity all *fall out* as consequences

Yin Wang's framing — "they twisted time and length until it produces c" — inverts this. It's not "twist until you get the answer you want"; the transformation is *derived* to satisfy the postulate, then you check (as a theorem, not a fitting exercise) that it's self-consistent for light from any angle. Those are different epistemic activities.

**The mathematical claim ("only one direction," "impossible in general") is false — verified computationally**

Take a photon emitted in frame S along an arbitrary unit direction $(n_x, n_y, n_z)$:

```python
x, y, z = c*nx*t, c*ny*t, c*nz*t   # arbitrary direction, not just x-axis
```

Boost to S′ (moving at v along x):

```python
gamma = 1/sqrt(1 - v**2/c**2)
tp = gamma*(t - v*x/c**2)
xp = gamma*(x - v*t)
yp = y
zp = z
```

Compute $u'_x, u'_y, u'_z$ via the chain rule ($u'_i = \frac{dx'_i/dt}{dt'/dt}$), then check $u_x'^2+u_y'^2+u_z'^2$:

```python
speed_sq = simplify(ux**2 + uy**2 + uz**2)
```

Substituting $n_x^2+n_y^2+n_z^2=1$ and checking numerically over random directions $(\theta,\phi)$ and random $v \in (-0.9c, 0.9c)$:

```
0.9999999999999998   # = c^2, for every random direction and velocity tried
1.0000000000000002
0.9999999999999999
...
```

Every trial returns exactly $c^2$. This is the standard relativistic velocity-addition result:

$$u_x' = \frac{u_x - v}{1-vu_x/c^2}, \quad u_y' = \frac{u_y}{\gamma(1-vu_x/c^2)}, \quad u_z' = \frac{u_z}{\gamma(1-vu_x/c^2)}$$

and it's a textbook fact that $u_x'^2+u_y'^2+u_z'^2=c^2$ whenever $u_x^2+u_y^2+u_z^2=c^2$, for *any* direction, not just the boost axis. This is equivalent to saying the Lorentz transformation preserves the null cone $-c^2t^2+x^2+y^2+z^2=0$ of Minkowski space — which is essentially the *definition* of a Lorentz transformation (it's the linear map preserving that quadratic form). So "does a transformation exist that keeps light speed c from every direction" isn't an open question or a coincidence — it's what a Lorentz transformation *is*, provably, in one page of algebra.

**On "Einstein only considered one direction" — checked against the 1905 paper, also false**

I searched Einstein's §5, "Composition of Velocities," and found he explicitly set up a point moving with both a ξ-component and an η-component (i.e., a general 2D, and by extension 3D, direction — not just along the boost axis), deriving:

$$x = \frac{t(w_\xi+v)}{1+vw_\xi/c^2}, \quad y = \frac{w_\eta t\sqrt{1-v^2/c^2}}{1+vw_\xi/c^2}$$

He only *specializes* to the parallel case afterward to get the famous addition formula $U=(v+w)/(1+vw/c^2)$, and from the general (transverse-inclusive) result he explicitly concluded that composing any velocity smaller than c with another smaller-than-c velocity stays below c, and that light's speed cannot be changed by composition with anything slower than light. So the "he never considered other directions" premise Yin Wang's argument depends on is factually wrong — it's the opposite of what section 5 does.

**On GPS ("relativity is fake there")**

This is also checkable and also wrong. The special-relativistic time dilation slows GPS satellite clocks by about 7,000 ns/day relative to ground clocks, while gravitational (general-relativistic) redshift speeds them up by about 46,000 ns/day, netting to roughly +39,000 ns/day — and general relativity has to be accounted for to hit the ~50 ns timing accuracy needed for 15 m positioning. Beyond the constant offset (which is pre-compensated by adjusting the on-board clock frequency before launch), the orbit-eccentricity-dependent relativistic correction still has to be computed using each satellite's actual orbital parameters and can't be pre-baked away. That correction is orbit-shape-dependent (not constant), so it can't be replaced by pure hyperboloid-intersection timing math without relativity — it's genuinely load-bearing, not cosmetic.

**Where Yin Wang has a legitimate point**

Separating the three claims matters:

1. "Length contraction/time dilation are conventions, not observable per se, and depend on simultaneity conventions" — this is a real, respectable position (Reichenbach's conventionality-of-simultaneity thesis). Worth engaging with seriously.
2. "The astronomical evidence for SR/GR is thin/hard to reproduce" — also a fair empirical-epistemology point worth scrutiny case by case (though it undersells things like muon decay in atmosphere, particle accelerator time dilation, and GPS itself, which are lab-reproducible daily, not one-off astronomical events).
3. "The math doesn't actually work for off-axis light, and Einstein never checked" — this is not a matter of interpretation, it's a specific computable claim, and it's false, both by direct symbolic/numeric derivation and by what's literally in the 1905 paper.

Claim 3 is the one doing the heavy lifting in his argument ("so a transformation with this property can't exist, not even mathematically") and it's the one that fails a five-minute sympy check. The interesting philosophical claims (1 and 2) don't need claim 3 to be true, and shouldn't be defended by leaning on a math error that a direct computation immediately falsifies.

References:

- [Composition of Velocities — reassessment of Einstein's 1905 paper (arXiv)](https://arxiv.org/pdf/physics/0612041)
- [A Discussion of Special Relativity — Einstein's 1905 §5 derivation (arXiv)](https://arxiv.org/pdf/1205.0221)
- [Special Relativity: A Centenary Perspective — GPS relativistic corrections (arXiv)](https://arxiv.org/pdf/gr-qc/0504085)
- [Neil Ashby, Relativity and the Global Positioning System, Physics Today](https://physicstoday.aip.org/features/relativity-and-the-global-positioning-system)
- [Yin Wang's Substack post](https://open.substack.com/pub/yinwang1/p/16d)
