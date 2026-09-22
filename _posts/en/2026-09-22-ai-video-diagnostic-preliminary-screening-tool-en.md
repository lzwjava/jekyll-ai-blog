---
audio: false
generated: true
image: false
lang: en
layout: post
title: "AI Video Diagnostic: Preliminary Screening Tool"
translated: false
type: note
---

Question: Is this video-based GPU diagnostic method (AI analysis of multimeter probing session) good? How does it hold up analytically?

Answer:

The method has real merit but also meaningful limitations. Here's a balanced breakdown:

---

**What the method does well**

- **Non-invasive triage** — feeding a video to an AI for a first-pass visual + meter reading survey is faster than manually documenting every frame. Good for a quick "is anything obviously wrong?" check.
- **Visual damage detection** — AI can reliably flag burned components, bulged caps, cracked ICs, and lifted pads from video if the lighting and resolution are adequate. 4K HEVC here is well-suited for that.
- **Audio analysis** — detecting beep codes or continuity tones from audio is a smart passive signal; zero beeps in this session is actually useful data.
- **Die identification** — correctly IDing the GA104 die from the PCB layout is a meaningful win that helps cross-reference known power rail maps.

---

**Where the method breaks down**

| Weakness | Why it matters here |
|---|---|
| Probe points not labeled | The 0.0 Ω readings are uninterpretable without knowing *which* rail they're on — ground-tied cap vs. shorted 12V rail are very different |
| Meter display unreadable in 3 frames | Critical data loss exactly where 8-pin PCIe input (the highest-risk area) was being probed |
| No powered rail checks | All readings were on unpowered board — you can't confirm dead shorts or leaky MOSFETs without live voltage measurements |
| Single DC voltage reading (0.00 V) | Expected on unpowered PCB, so carries zero diagnostic weight |
| AI can't confirm context | The report explicitly can't tell if a 0.0 Ω is normal ground or a fault — that gap is the core diagnostic limitation |

---

**Overall verdict**

This is a solid **preliminary screening tool**, not a conclusive diagnostic. The AI correctly concluded "no obvious fault visible" — which is a useful negative result, but not a green light. The method would be significantly more powerful if you:

1. **Label probe points** (tape + marker on PCB, or annotate the video)
2. **Keep the meter display fully in frame** the entire time
3. **Add powered-rail checks** on known GA104 test points (VDDC ~0.85–1.1 V, VMEM ~1.35 V, VDDCI ~0.9 V)
4. **State the symptom upfront** — the same readings mean completely different things depending on whether the card shows artifacts, no output, or no power

Think of this video-AI method as equivalent to a **visual inspection + continuity map** done by a technician who couldn't read their own notes in a few spots. Useful starting point; needs follow-up with structured probing to close the diagnosis.