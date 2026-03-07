---
audio: false
generated: true
image: false
lang: en
layout: post
title: Folded Binary Code in Voice PCM
translated: false
type: note
---

Question: In a PCM system, the 3-bit natural binary and 3-bit folded binary encoding rules are shown in Table 31. Fill in the values at positions ①, ②, ③, and ④. List the characteristics of folded binary coding, and analyze why folded binary code is mostly used in voice signal PCM systems.

Answer:

## Part 1: Filling in the Encoding Table

The standard 3-bit encoding table for PCM is as follows:

| Quantization Level | Signal Polarity | Natural Binary Code | Folded Binary Code |
|---|---|---|---|
| +3 | Positive | 111 | **① 111** |
| +2 | Positive | 110 | **② 101** |
| +1 | Positive | 101 | 110 |
| 0+ | Positive | 100 | 100 |
| 0− | Negative | 011 | 000 |
| −1 | Negative | 010 | **③ 001** |
| −2 | Negative | 001 | **④ 011** |
| −3 | Negative | 000 | 010 |

**Answers:**
- ① = `111`
- ② = `101`
- ③ = `001`
- ④ = `011`

---

## Part 2: Characteristics of Folded Binary Code

The folded binary code uses the leftmost (most significant) bit as a **sign/polarity bit** (1 = positive, 0 = negative), and the remaining bits represent magnitude. Its key characteristics are:

**1. The MSB is the polarity bit; codes are mirror-symmetric around zero.**
The code table is "folded" symmetrically around the zero level. If the negative codes were folded over on top of the positive codes, they would match perfectly — hence the name "folded binary."

**2. Signals with the same absolute value (but opposite polarity) share the same magnitude bits.**
The folded binary code (FBC) uses the MSB as a sign bit, and then counts out from the origin in both the positive and negative directions with the remaining bits. Codewords equidistant from the origin are identical (except for the sign bit). This means the encoder can apply the same quantization process to both positive and negative signals with equal magnitude.

**3. Bit errors in small signals have a smaller impact.**
Because small signals are encoded near the zero boundary (low magnitude bits), a single-bit error in a small-signal codeword shifts the decoded value by only a small amount — the impact is minor compared to a bit error in a large-signal codeword.

---

## Part 3: Why Folded Binary Code is Used in Voice PCM Systems

The two reasons work together:

**Reason 1: Voice signals have a high probability of being small-amplitude signals.**
In real telephone and voice communications, the signal amplitude is low most of the time. Large amplitude excursions (loud sounds) occur much less frequently than small-amplitude signals (quiet speech, pauses, and background). Statistically, voice signals concentrate near zero level.

**Reason 2: Folded binary code minimizes the impact of bit errors on small signals.**
With a folded binary code, adjacent quantization levels near zero differ by only one bit in the magnitude portion. Therefore, when a transmission error (bit flip) occurs in the lower magnitude bits — which correspond to small signals — the decoded error is small and the perceptual degradation to voice quality is minimal.

**Combined effect:** Since voice signals are predominantly small in amplitude, and folded binary code protects small signals most effectively against bit errors, using folded binary coding in voice PCM systems results in significantly **better perceived audio quality** under noisy channel conditions compared to natural binary coding.

> In summary: folded binary code is preferred because it matches the statistical nature of voice (mostly small amplitudes) with robust error resilience exactly where it matters most — near zero signal levels.

References:

- [PCM Folded Binary Code – SlideShare](https://www.slideshare.net/SubaShree87/pcmpart-1pptx)
- [Folded Binary Code (FBC) – UCSB ECE](https://courses.ece.ucsb.edu/ECE146/146B_S09Gibson/LogPCM.pdf)
- [Telecomms Principles – PCM](https://www.technologyuk.net/telecommunications/telecom-principles/pulse-code-modulation.shtml)