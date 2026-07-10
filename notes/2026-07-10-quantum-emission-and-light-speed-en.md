---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quantum Emission and Light Speed
translated: false
type: note
---

Question: My friend refines the point: "light speed invariance" (光速不变) means that in any local reference frame — whether that of the emitter or the observer — a light beam is measured as constant `c`; this is a basic postulate. Going deeper, though, the emission process is a quantum process, while relativity describes the macroscopic world — these are different scales that haven't been unified, so there's some genuine tension here.

Answer:

The first part is correct and is exactly the content of the second postulate — both frames, emitter and observer, measure `c`. But the second move — "emission is quantum, relativity is macroscopic, quantum and relativistic physics aren't unified, so this creates tension for the postulate" — is a category error. It's conflating two very different open/closed problems in physics:

**What's actually unsolved:** General Relativity (gravity, curved spacetime) + Quantum Mechanics = quantum gravity. Genuinely unsolved. String theory, loop quantum gravity, etc. are attempts.

**What's actually solved and extremely well tested:** Special Relativity + Quantum Mechanics = relativistic Quantum Field Theory (QED, QCD, the full Standard Model). This is *not* an open problem. QFT is built from the ground up to be Lorentz-invariant — the Lagrangian for the electromagnetic field, `L = -¼F_μν F^μν`, is manifestly Lorentz-invariant before you even quantize it. Quantizing it (canonical quantization or path integral) doesn't introduce any tension with SR; it's how you get the photon as a massless spin-1 excitation of that field, with dispersion relation `E = pc` baked in — which *is* the statement "photon speed = c in every inertial frame." There's no seam between "quantum emission" and "relativistic propagation" here; they're two aspects of one Lorentz-invariant field theory.

**Concretely, why the quantum-ness of emission doesn't matter to the postulate:**

For any massless particle, the on-shell condition from Lorentz-invariant kinematics is:

```
E² = (pc)² + (m c²)²,  m = 0  ⟹  E = pc  ⟹  v_group = ∂E/∂p = c
```

This holds identically whether the photon comes from a classical antenna, an atomic transition (discrete quantum jump), or a particle decay. The "quantumness" of the emission event only affects *when* and *in what direction* a photon is emitted (governed by matrix elements / Fermi's golden rule) — it says nothing about the propagator's dispersion relation once the photon is on-shell and free. Quantization changes the *statistics of emission*, not the *kinematics of propagation*.

**And this isn't just theory — it's exactly what's been tested with quantum-emitted photons from ultra-relativistic sources:**

- Alvāger et al. (CERN, 1964): 20 GeV protons hit a target, producing neutral pions (π⁰) moving at `v/c ≥ 0.99975`. These pions decay via the genuinely quantum process π⁰ → γγ. If photon speed depended on source velocity (`c' = c + kv`, the Ritz/emission-theory prediction), photons from a source moving at 0.99975c should show a large, easily measurable deviation. Measured result: `(2.9977 ± 0.0004) × 10⁸ m/s`, matching the lab value of `c` and bounding `k < 10⁻⁴` at `v ≈ c` — one of the most stringent source-independence tests, precisely because the emission was a quantum decay near the speed of light, not a classical process.
- Filippas and Fox (1964) ran an equivalent π⁰ → γγ comparison and got the same null result independently.
- Ives–Stilwell used atomic transitions (canal-ray Doppler shift, hydrogen) — again a quantum emission process — to confirm relativistic time dilation, which is the observer-side half of the postulate.

So the empirical record already directly covers "does quantum emission break the invariance," and the answer is no — to parts in 10⁻⁴ or better even with sources moving at 99.975% of `c`.

**Where the friend's intuition is pointing at something real, just misapplied:** the unresolved SR/QM-vs-GR tension is real and deep (quantum gravity), but it's not "macro vs micro physics," it's specifically "curved spacetime dynamics vs quantum field theory in flat spacetime." SR + QM is not a frontier problem; it's the best-tested framework in all of physics (QED's prediction of the electron's anomalous magnetic moment agrees with experiment to ~10 significant figures). If you want to point your friend at the *actual* live seam, it's holography / AdS-CFT, string theory, loop quantum gravity — not "light emission is quantum so maybe `c`-invariance is shaky."

References:

- [Special Relativity: A Centenary Perspective (arXiv gr-qc/0504085) — CERN π⁰ decay photon speed test](https://arxiv.org/pdf/gr-qc/0504085)
- [Emission theory (relativity) - Wikipedia](https://en.wikipedia.org/wiki/Emitter_theory)
- [Kennedy–Thorndike experiment - Wikipedia](https://en.wikipedia.org/wiki/Kennedy%E2%80%93Thorndike_experiment)
