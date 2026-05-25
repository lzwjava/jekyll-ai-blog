---
audio: false
generated: true
image: false
lang: en
layout: post
title: Undercorrection for Near Work Strategy
translated: false
type: note
---

**Question:** Is the "undercorrection by 1.50D for screens, full correction for driving" two-glasses strategy valid? And is the claim that holding your phone at arm's length and it being "just barely clear" the right calibration signal — leading to 25-50 degree reduction per year?

**Answer:**

The core mechanism being described is **Axel Tokovinin / Todd Becker / Endmyopia-style "active focus"** — the idea that chronic overcorrection drives axial elongation, and that working at the edge of clarity (just barely clear, not crystal clear) provides a stimulus for the eye to either stabilize or slightly reverse.

Let me give you a first-principles breakdown.

---

## The Optics

Your prescription is in diopters. 1D = focus at 1/D meters.

If your distance correction is -5.00D, your far point is 20cm. With -3.50D (undercorrected by 1.50D), your far point shifts:

```
far_point = 1 / 3.50 = ~28.6 cm
```

For screen work at ~50-60cm, you need:
```
accommodation_needed = 1/0.5 - 3.5 = 2.0 - 3.5 = -1.5D of accommodation
```

With full correction (-5.00D) at 50cm, you'd need 2D of accommodation — not zero. With -3.50D, you need ~0.5D. The point isn't zero accommodation — it's *not straining past your comfortable range*.

The "arm's length test" (phone at ~60-70cm, just barely clear) is a reasonable proxy for calibrating your undercorrected glasses to your actual near-work distance. If it's crystal clear at 70cm, you're still overcorrected for that distance.

---

## What the Evidence Actually Says

**What's established:**
- Chronic hyperopic defocus (overcorrection) accelerates axial elongation in animal models (chick, primate) — very robust data
- Myopic defocus (undercorrection) has protective/slowing effects in animal models
- Outdoor time and reduced near work slow progression — solid epidemiological evidence

**What's contested:**
- Whether these mechanisms transfer cleanly to adult humans (most axial elongation slows naturally post-~21)
- The specific magnitude: "25-50 degrees per year reduction" is anecdotal, not RCT-backed
- The Endmyopia community has self-reported data, not blinded clinical trials

**What's probably happening when people report improvement:**
1. Genuine small axial length reduction (rare in adults, but documented in some ortho-K studies)
2. Reduced ciliary muscle spasm → pseudomyopia resolution (real, can be 0.25-0.75D)
3. Measurement variability (autorefractors have ±0.25D noise)
4. Corneal reshaping from contact lens wear

For someone who has had stable myopia for years, item 2 (pseudomyopia/ciliary spasm) is the most plausible mechanism for reported "reduction." True axial shortening in adults is not well-documented outside ortho-K.

---

## The Two-Glasses Strategy — Is It Sound?

**Yes, the ergonomic logic is solid regardless of whether you believe in reversal:**

| Context | Correction | Rationale |
|---|---|---|
| Driving / cinema / distance | Full Rx | Legal requirement, safety |
| Phone / computer (40-70cm) | -1.25 to -1.75D less | Reduces strain, no overcorrection at near |

This is actually standard optometry advice for high myopes doing heavy screen work — many ODs will prescribe a separate "computer pair."

The risk is **if you undercorrect too aggressively**, you strain to see, which is worse. The calibration signal ("just barely clear at arm's length") is reasonable but you should fine-tune per your actual working distance.

---

## Practical Calibration (First Principles)

```python
# Your actual working distance determines needed correction
working_distance_m = 0.55  # your monitor distance
needed_power = 1 / working_distance_m  # = 1.82D of correction needed for emmetrope

# If your Rx is -5.00D:
full_rx = -5.00
undercorrected = -(needed_power)  # -1.82D lens would put your far point at 55cm
# In practice: full_rx + 1.50 = -3.50D is a reasonable approximation
screen_rx = full_rx + 1.50  # = -3.50D

# Verification: far point with screen_rx
far_point = 1 / abs(screen_rx)  # = 28.6cm
# At 55cm you need: 1/0.55 - 1/far_point accommodation
# = 1.82 - 3.5 = you need to accommodate past your far point → won't work this way

# Correct calculation:
# With lens of power L, and eye needing P diopters to be emmetropic:
# Effective vergence at distance d: L + 1/d must = P
# So comfortable if |L + 1/d| ≤ |P| (not straining beyond far point)
```

The simple rule: **your undercorrected lens power should be approximately `-(1/working_distance)`** for zero accommodation at that distance, which is comfortable but not stimulating. For slight active focus stimulus, go slightly less (by 0.25-0.50D).

---

## Bottom Line

- The two-glasses strategy is **ergonomically sound** and low-risk
- 25-50D/year reduction in adults is **optimistic but not impossible** — mostly pseudomyopia resolution
- The arm's length calibration is a **reasonable heuristic** — if just barely clear at 55-65cm, that's about right
- Don't expect axial reversal; do expect **reduced progression and less strain**
- Your 100D reduction over 3 years is plausible as pseudomyopia + measurement variance, not necessarily axial shortening

The strategy is worth doing for comfort alone. The reversal claims are a bonus that may or may not materialize.