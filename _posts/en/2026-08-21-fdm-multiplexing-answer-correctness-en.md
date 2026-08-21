---
audio: false
generated: true
image: false
lang: en
layout: post
title: FDM Multiplexing Answer Correctness
translated: false
type: note
---

Question: Is the answer to this multiplexing question correct, and can you explain why?

Answer: Yes, **A (Frequency Division Multiplexing, FDM)** is correct.

The question describes dividing channel bandwidth into multiple sub-channels **in the frequency domain**, then modulating the original signal onto the carrier signal of each sub-channel so that multiple signals can be transmitted simultaneously on one channel. This is exactly the definition of FDM.

Here's why the other options are wrong:

- **B — TDM (Time Division Multiplexing):** Divides the channel in the **time domain**, allocating different time slots to different signals.
- **C — WDM (Wavelength Division Multiplexing):** A special form of FDM used in **optical fiber** communications, where different wavelengths of light carry different signals.
- **D — CDM (Code Division Multiplexing):** Assigns each signal a unique **orthogonal code**, allowing all signals to share the same frequency and time simultaneously.

The key phrase in the question is *"在频域内将信道带宽划分为多个子信道"* ("dividing channel bandwidth into multiple sub-channels **in the frequency domain**"), which directly points to FDM.

---

References:
- [Frequency-Division Multiplexing – Wikipedia](https://en.wikipedia.org/wiki/Frequency-division_multiplexing)
- [Multiplexing Techniques Overview – GeeksforGeeks](https://www.geeksforgeeks.org/multiplexing-channel-sharing-in-computer-network/)
