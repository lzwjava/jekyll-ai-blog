---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bandwidth Division in FDM Explained
translated: false
type: note
---

Question: In cases where the available bandwidth of a physical channel exceeds the bandwidth required by a single original signal, the total bandwidth of the physical channel can be divided into several sub-channels that are the same as (or slightly wider than) the bandwidth needed to transmit a single signal, with each sub-channel carrying one signal. This technique is called

A. Frequency Division Multiplexing  
B. Time Division Multiplexing  
C. Wavelength Division Multiplexing  
D. Space Division Multiplexing  

Your answer: B  
Correct answer: A  

Answer: 

The correct answer is **A. Frequency Division Multiplexing (频分多路复用, FDM)**.

**Explanation:**

Frequency Division Multiplexing (FDM) works by dividing the total available bandwidth of a physical channel into multiple smaller frequency bands (sub-channels). Each sub-channel occupies a different frequency range and carries one independent signal.  

This approach is used precisely when the channel bandwidth is much wider than what one signal requires. By assigning each signal to its own non-overlapping (or slightly guarded) frequency band, multiple signals can be transmitted simultaneously over the same physical medium without interfering with each other.

**Why the other options are incorrect:**

- **B. Time Division Multiplexing (时分多路复用, TDM)**  
  TDM divides the channel by **time**, not by frequency. Different signals take turns using the **entire bandwidth** during their assigned time slots. It does **not** split the bandwidth into sub-channels.

- **C. Wavelength Division Multiplexing (波分多路复用, WDM)**  
  WDM is similar in concept to FDM but is specifically used in **optical fiber** communication. It divides the optical spectrum (different wavelengths of light) rather than electrical frequency bands. While the principle is analogous, the standard term in general (especially non-optical) communication contexts for this description is FDM.

- **D. Space Division Multiplexing (空分多路复用, SDM)**  
  SDM uses physically separate paths (different cables, different antennas, different fibers in a bundle, MIMO spatial streams, etc.) to carry different signals. It does **not** involve dividing the bandwidth of a single physical channel.

**Summary**  
The technique described in the question — dividing the **total bandwidth** of one physical channel into several **frequency sub-bands**, each carrying one signal — is the classic definition of **Frequency Division Multiplexing (FDM)**.

Therefore, the correct choice is **A**.

References:  

- None (standard textbook concept in data communication and computer networks)