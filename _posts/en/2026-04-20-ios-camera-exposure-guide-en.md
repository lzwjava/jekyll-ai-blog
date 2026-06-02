---
audio: false
generated: true
image: false
lang: en
layout: post
title: iOS Camera Exposure Guide
translated: false
type: note
---

**Question:**
How should I understand iOS camera exposure values (−2.0 to +2.0 when taking photos vs −100 to 100 in editing), and what happens to dark areas or stars when lowering exposure?

---

**Answer:**

### 1. Two different “exposure” systems (capture vs edit)

What you’re seeing in the iOS camera app (like on iPhone) is actually **two completely different concepts that share the same name**:

#### 📸 During shooting: −2.0 to +2.0 (EV — Exposure Value)

* This is **real exposure compensation**, measured in **EV (Exposure Value)**.
* It directly affects how much light hits the sensor.
* Each step is exponential:

  * **+1 EV = 2× more light**
  * **−1 EV = ½ the light**

So:

* −2.0 = very dark (¼ of the light)
* +2.0 = very bright (4× the light)

👉 This changes actual camera parameters like:

* shutter speed
* ISO
* sometimes computational exposure stacking

---

#### 🖼️ During editing: −100 to +100 (software brightness adjustment)

* This is **post-processing**, not real exposure.
* It’s just a **linear or curve-based brightness adjustment** applied to the image.
* It does **NOT recover lost sensor data**.

👉 Important difference:

* Shooting EV = controls **data capture**
* Editing slider = modifies **existing pixels**

---

### 2. Why Apple uses different scales

Because they represent different domains:

| Stage    | Scale       | Meaning                      |
| -------- | ----------- | ---------------------------- |
| Shooting | −2.0 ~ +2.0 | Physical light (EV units)    |
| Editing  | −100 ~ +100 | Visual adjustment (UI scale) |

Apple chose:

* **EV scale** → standard in photography
* **−100~100** → intuitive slider for users

There’s no direct conversion between them.

---

### 3. What happens when you lower exposure?

You’re absolutely on the right track—this is where things get interesting.

#### When you reduce exposure (especially during shooting):

* Less light hits the sensor
* Shadows get darker
* **Signal-to-noise ratio drops in dark areas**

👉 Result:

* Dark areas may become **pure black (clipped shadows)**
* Fine details (like stars) may **disappear**

---

### 4. Why stars disappear

Capturing stars is tricky because they are:

* Extremely dim
* Require **high exposure + long exposure time**

If you:

* Lower EV (e.g., −1.5 or −2.0)
* Or let the camera auto-expose for bright foreground

👉 Then:

* The camera prioritizes bright areas
* Stars fall below sensor sensitivity → **not recorded at all**

And once they’re gone:

* ❌ Editing cannot bring them back
* Because the data was never captured

---

### 5. Counterintuitive insight

Lower exposure does **NOT always mean “better night detail.”**

For example:

| Scenario        | Result                                    |
| --------------- | ----------------------------------------- |
| Lower exposure  | preserves highlights, loses shadows/stars |
| Higher exposure | captures stars, risks blown highlights    |

That’s why astrophotography usually:

* uses **long exposure**
* or computational stacking (which iPhone does in Night Mode)

---

### 6. Practical intuition

Think of it like this:

* **Shooting exposure (EV)** = how much light you *collect*
* **Editing exposure** = how you *redistribute* that collected light

If you didn’t collect enough light:
👉 no amount of editing can fix it

---

### 7. Simple rule of thumb

* Want stars or dark details → **increase exposure (or use Night Mode)**
* Want to avoid blown highlights → **decrease exposure**
* Editing is only for **fine tuning**, not recovery

---

If you want, I can break down how iPhone Night Mode or HDR actually balances sky vs foreground—that’s where the real magic (and trade-offs) happen.
