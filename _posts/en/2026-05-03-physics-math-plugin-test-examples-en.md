---
audio: false
generated: true
image: false
lang: en
layout: post
title: Physics and Math Plugin Test Examples
translated: false
type: note
---

The math/physics skills are already built — it's a rich SymPy-backed layer covering mechanics, EM, QM, fluids, relativity, optics, etc.

---

**"Math plugins"** here means those skills in `skills.py` — they're already made. The system uses them as deterministic checks alongside LLM reasoning.

---

**Good test problems to try** (matching what the system is designed for):

1. **Simple sum** — `Calculate the sum 1+2+3+...+100` (you already tried this)

2. **Physics — projectile** — `A ball is launched at 45° with initial speed 20 m/s. Find the range.`

3. **Relativity** — `A spaceship travels at 0.8c for 10 years ship-time. How far does it travel in the Earth frame?`

4. **Optics** — `Light of wavelength 500nm passes through a double slit separated by 0.1mm. Find the fringe spacing on a screen 1m away.`

5. **Energy** — `A 2kg block slides down a frictionless ramp of height 5m. Find its speed at the bottom.`

Try **#2 or #5** — they're clean enough to get a full tree but non-trivial enough to show branch diversity. Paste one as the **problem statement** when creating a new session.