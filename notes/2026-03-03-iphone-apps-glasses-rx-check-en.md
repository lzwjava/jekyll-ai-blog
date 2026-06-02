---
audio: false
generated: true
image: false
lang: en
layout: post
title: iPhone Apps Measure Glasses Prescription Strength
translated: false
type: note
---

**Question: Can we use an iPhone camera to detect the prescription strength (diopters) of eyeglasses, such as reading glasses (+1.5D) or normal ones? If we have multiple pairs and don't know their strengths, is there an easy way to find out? Could we design an app that determines the degree based on the blur when the camera looks through the eyeglasses?**

**Answer:**

Yes, it is possible to measure the prescription strength (in diopters) of existing eyeglasses using an iPhone camera, and several apps already do this quite effectively without needing to build a new one from scratch.

The most practical and accurate existing methods do **not** primarily rely on analyzing "blur" in a general photo taken through the lens. Instead, they use computer vision techniques to:

- Photograph the lenses in a specific way (often with a reference object like a credit card for scale).
- Analyze lens magnification, distortion, prism effects, reflections, or edge patterns.
- Estimate sphere power (for nearsightedness/farsightedness), cylinder (astigmatism), axis, and sometimes add power.

Popular apps that do this include:

- **GlassesOn** (now also called The Framery in some versions) — Widely regarded as one of the best. It scans your glasses using the phone camera and gives prescription parameters with good accuracy (FDA/CE listed in some regions). Many users report results within 0.25–0.50 D of professional measurements.
- **GlassesUSA Prescription Scanner** — Free tool that uses the smartphone camera to scan glasses and read the prescription values.
- **Eyerim Lens Scan** — Similar lens-reading feature via smartphone camera.
- Specialized tools like the **My Call Bag Lensometer** (more for professionals) — Uses an Amsler grid viewed through the lens; AI analyzes distortion patterns to estimate sphere, cylinder, and axis.

These apps typically work best for single-vision lenses (including basic reading glasses like +1.5 D) and require you to follow on-screen instructions, such as placing the glasses on a table, using good lighting, and including a known-size object for calibration.

**Regarding a pure blur-based approach** (taking a photo through the glasses and measuring how much blur occurs):

- In theory, yes — a +1.5 D reading lens would cause noticeable defocus/blur when the camera tries to focus on a distant object through it (because the lens adds converging power).
- You could design an app that:
  - Displays a sharp target (e.g., text or grid) at a known distance.
  - Captures images with and without the lens in front of the camera.
  - Measures blur metrics (e.g., edge sharpness, Laplacian variance, or FFT-based focus measures).
  - Estimates diopter power based on how much defocus is introduced (using optics formulas like the lensmaker's equation or empirical calibration).
- However, this method would be less accurate and reliable in practice because:
  - iPhone cameras have very strong autofocus and stabilization.
  - Small lens decentration, tilt, astigmatism, or scratches create complex blur patterns.
  - It struggles with low powers (±0.50 D) or astigmatism.
  - Existing apps use more robust features (magnification/distortion) rather than pure blur for better precision.

**Easiest way right now (no coding needed):**

1. Download a free app like GlassesOn / The Framery or GlassesUSA Prescription Scanner from the App Store.
2. Follow the instructions to scan each pair of glasses (usually takes 1–3 minutes per pair).
3. Compare the results across your 3–5 pairs.

For very basic reading glasses (+1.00 to +3.50 D range), these apps usually give reliable sphere power estimates. Results are good enough for ordering similar replacement glasses online, though a professional optometrist exam is still recommended for precise vision care.

If you're interested in the research/DIY side, look into computer vision papers on "smartphone lensometer" or "autorefractor" — but consumer apps already solve this problem well.

**References:**

- [GlassesOn app official site](https://6over6.com/glasses-on)
- [GlassesUSA Prescription Scanner](https://www.healthline.com/health/how-to-find-out-what-prescription-your-glasses-are)
- [My Call Bag Lensometer concept](https://www.youtube.com/watch?v=SX0oIHR-CHQ)
- [Eyerim Lens Scan](https://www.prnewswire.com/news-releases/eyerim-introduces-lens-scan-an-online-way-of-getting-a-prescription-301352414.html)
