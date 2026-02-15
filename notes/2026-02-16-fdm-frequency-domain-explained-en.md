---
audio: false
generated: true
image: false
lang: en
layout: post
title: FDM Explained in Frequency Domain
translated: false
type: note
---

Question: In the frequency domain, the channel bandwidth is divided into multiple subchannels, and the original signal is modulated onto the carrier signals corresponding to these subchannels, thereby allowing multiple signals to be transmitted simultaneously on one channel. This channel multiplexing technique is called ( )

A Frequency Division Multiplexing (FDM)  
B Time Division Multiplexing (TDM)  
C Wavelength Division Multiplexing (WDM)  
D Code Division Multiplexing (CDM)  

Answer: A

Answer: 

The correct answer is **A. Frequency Division Multiplexing (FDM)**.

**Explanation:**

Frequency Division Multiplexing (FDM) is a multiplexing technique that works entirely in the **frequency domain**.  

The main idea of FDM is:

- The total available bandwidth of the channel is divided into several smaller, non-overlapping frequency bands (subchannels).
- Each data signal (or user) is modulated onto its own carrier frequency.
- These modulated signals are then combined and sent over the same physical medium at the same time.
- Because each signal occupies a different frequency range, they do not interfere with each other (as long as the bands are properly separated and guard bands are used).
- At the receiving end, bandpass filters are used to separate the different frequency bands and recover each individual signal.

**Quick comparison with other options:**

- **B. Time Division Multiplexing (TDM)**  
  Divides the channel into **time slots** — different signals take turns using the full bandwidth at different moments in time.

- **C. Wavelength Division Multiplexing (WDM)**  
  Similar in principle to FDM, but used specifically in **optical fiber** systems. It divides the optical spectrum (different wavelengths/colors of light) instead of electrical frequency bands.

- **D. Code Division Multiplexing (CDM) / CDMA**  
  All signals use the **same frequency band at the same time**, but each signal is multiplied by a unique spreading code. The receiver uses the same code to extract its desired signal (widely used in 3G mobile systems).

Only **FDM** matches the description of dividing the bandwidth into multiple subchannels in the frequency domain and transmitting multiple modulated signals simultaneously on different carrier frequencies.

Therefore, the correct answer is **A**.

References:  

- None (standard data communications concept, no specific external source required)