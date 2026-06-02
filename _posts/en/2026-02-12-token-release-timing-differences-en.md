---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Token Release Timing Differences Explained
translated: false
type: note
---

Question: Although both FDDI and IEEE 802.5 use the token passing protocol, what is the key difference in how they handle token regeneration after frame transmission?

Answer:

The correct answer is **C. In the FDDI protocol, the sending station can immediately send a new token after finishing transmission of its frame, while in IEEE 802.5, the new token is sent only after the frame's leading edge returns to the sending station.**

**Detailed explanation:**

Both FDDI and IEEE 802.5 are token ring protocols, but they implement **token release timing** differently, which significantly affects performance, especially at high speeds.

- **IEEE 802.5 (classic Token Ring)**
  - Uses **"delayed token release"** or **"token after frame return"** policy.
  - The transmitting station keeps the token (does not release a new one) until it receives its own frame back (specifically, until it sees the beginning of its own transmitted frame returning to it).
  - Only after the frame header returns does the station release a new free token.
  - This ensures that only one frame is circulating on the ring at a time (single-token mode).
  - This conservative approach reduces the risk of frame collisions but limits throughput, especially on large rings or at high speeds.

- **FDDI (Fiber Distributed Data Interface)**
  - Uses **"immediate token release"** or **"early token release"**.
  - As soon as the transmitting station finishes sending its frame (i.e., after transmitting the last bit of the frame trailer), it **immediately** generates and releases a new free token.
  - It does **not** wait for the frame to come back around the ring.
  - This allows multiple frames to be circulating on the ring simultaneously (multiple-token operation), greatly improving efficiency and throughput — especially important for FDDI’s 100 Mbps speed and large possible ring size (up to 100 km and 500 stations per ring, 1000 with dual ring).
  - FDDI can support **synchronous** and **asynchronous** traffic and uses a timed token rotation protocol (TTRT) to guarantee bandwidth and latency.

**Summary of the key difference:**

| Feature                          | IEEE 802.5 (Token Ring)                  | FDDI                                      |
|----------------------------------|------------------------------------------|-------------------------------------------|
| Token release timing             | After frame header returns to sender     | Immediately after finishing frame transmission |
| Multiple frames on ring at once? | No (single token/frame)                  | Yes (multiple tokens/frames possible)     |
| Best suited for                  | Lower speed (4/16 Mbps), smaller rings   | High speed (100 Mbps), larger rings       |

**Why the other options are incorrect:**

- **A**: Wrong — IEEE 802.5 does **not** release the token immediately.
- **B**: Wrong — FDDI does **not** wait for the frame to return; only 802.5 does.
- **D**: Wrong — FDDI does **not** generate the new token while still sending the frame; it releases immediately **after** finishing the frame.

**Memory tip:**
FDDI = Fast → "Finish frame → Free token immediately"
802.5 = Slow & safe → "Wait until frame comes back → then free token"

References:

- None (standard comparison between IEEE 802.5 Token Ring and ANSI X3T9.5 / ISO 9314 FDDI specifications)
