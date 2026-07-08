---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Salt Inhibition: Water Activity, Not Percentage"
translated: false
type: note
---

Question: How is the commonly cited "10–15% salt inhibits bacteria" figure actually measured — as salt-in-water concentration, and does temperature matter? It's not simply "a cup of water with salt added," is it?

Answer:

You're right to be skeptical — that "10–15%" number is not salt-mass-per-total-food-weight, and it's not measured the way people imagine (dissolve X g salt in a cup of water). The real variable is **water activity (aw)**, not salt percentage per se.

**What aw actually is**

```
aw = p / p0
```
where `p` is the vapor pressure of water in the food/solution and `p0` is the vapor pressure of pure water at the same temperature. It's the equilibrium relative humidity (ERH) divided by 100 — measured with a hygrometer-style water activity meter (chilled-mirror dew point or capacitance sensor) that equilibrates a sealed headspace above the sample and reads the RH at that temperature. Multiplication of water activity by 100 gives the equilibrium relative humidity in percent. It is NOT measured by weighing salt into a cup of water — that's just the model people use to *predict* aw via Raoult's law-type curves, then confirm empirically per sample.

**Why salt % alone is a bad proxy**

A 13 wt.% NaCl solution has a water activity of ~0.91, which is low enough to suppress growth of most "ordinary" bacteria — but that's 13% *in a solution where all the water is free water*. In actual food (meat, fish), only part of the total water is "free" — the rest is bound to proteins/polysaccharides and doesn't count toward aw. A portion of the total water content present in food is strongly bound to specific sites and does not act as a solvent, including hydroxyl groups of polysaccharides and carbonyl/amino groups of proteins. So the same 13% salt-by-weight gives a *different* aw in a ham than in brine, because the denominator (available water) differs. This is why food scientists express it as **water-phase salt (WPS)**:

```python
WPS = salt_mass / (salt_mass + water_mass) * 100   # % salt in the water phase only, not total food mass
```

not `salt_mass / total_food_mass`. Your yesterday's-pan situation is exactly this ambiguity — you don't know the WPS of whatever thin film of liquid is left in the pan, because it depends on how much moisture evaporated overnight, how much fat is coating it (fat doesn't dilute salt the way water does), and whether the salt is evenly distributed or crystallized out in patches.

**The actual thresholds** (this is where it gets non-binary):

| Organism class | aw floor |
|---|---|
| Most spoilage bacteria | ~0.90 |
| Most "ordinary" bacteria generally | ~0.91 |
| *S. aureus*, anaerobic | 0.91 |
| *S. aureus*, aerobic (matters — it can grow in an open pan!) | 0.86 |
| Most yeasts | ~0.88 |
| Molds | as low as ~0.65 |
| FDA "non-potentially-hazardous" cutoff | 0.85 |

So "10–15% salt" is really shorthand for "aw somewhere around 0.86–0.91," and *S. aureus* — the organism people actually worry about with leftover ham/cured fish residue — has a lower floor when exposed to air (aerobic), which is precisely the condition of an open pan sitting overnight. That's a meaningfully worse case than the anaerobic number most people quote.

**Temperature's role — it's a separate axis, not folded into the % figure**

aw thresholds are usually reported at 25°C and don't shift dramatically with temperature over normal kitchen ranges, but temperature controls *growth rate*, not the aw cutoff itself. This is hurdle technology: aw near the inhibition boundary + refrigeration temperature together suppress growth even where either alone wouldn't. A pan left at room temperature overnight in summer in Guangzhou gives bacteria much more doubling time than the same pan in a 4°C fridge, even at identical salt residue.

**The actual failure modes in your scenario**

1. Low aw only *stops growth*, it doesn't kill anything already present — low water activity merely slows bacterial growth; as soon as harmful microorganisms in low water activity are returned to higher water activity, they regain mobility. If you then cook something less salty in the same pan, any surviving organisms are back in a permissive environment.
2. *S. aureus* pre-formed enterotoxin is heat-stable — even if you kill the bacteria by reheating, toxin already produced overnight isn't destroyed by normal cooking temps. This is the actual food-safety risk, and it's independent of whether the salt matched the "10-15%" folk number.
3. Uneven distribution: your pan residue isn't a homogeneous brine — some spots (bottom, meat-adhered scraps) may sit well under the WPS needed, and those are exactly where growth restarts.

So: not wrong that it's "roughly" 10-15%, but the real story is water-phase salt (not gross weight), the organism-specific and oxygen-dependent aw floor, and that low-aw stalls rather than kills — none of which is captured by "dissolve salt in a cup of water."

References:

- [Water Activity and its Role in Food Preservation — UC Master Food Preserver](https://ucanr.edu/program/uc-master-food-preserver-program/article/water-activity-and-its-role-food-preservation)
- [Water Activity (aw) in Foods — FDA](https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-technical-guides/water-activity-aw-foods)
- [Water Activity's Role in Food Safety and Quality — Food Safety Magazine](https://www.food-safety.com/articles/4420-water-activitye28099s-role-in-food-safety-and-quality)
- [Food Safety With Water Activity — culinarycrush](https://www.culinarycrush.biz/all/food-safety-with-water-activity)
