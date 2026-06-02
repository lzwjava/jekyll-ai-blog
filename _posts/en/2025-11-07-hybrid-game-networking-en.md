---
audio: false
generated: true
image: false
lang: en
layout: post
model: moonshotai/kimi-k2-thinking
title: Hybrid Networking for Game Development
translated: false
type: note
---

You're right—Person B's explanation is spot-on.

It's **not redundant** because **selective reliability** gives game developers exactly what they need: fine-grained control over network behavior. Here's why this hybrid approach makes sense:

### The Trade-Off

- **TCP**: Guarantees delivery and order, but its retransmission and congestion control introduce latency—unacceptable for fast-paced games.
- **Plain UDP**: Fast and unordered, but completely unreliable—problematic for critical game events.

### Selective Reliability on UDP

Games can cherry-pick what needs guarantees and what doesn't:

**Reliable (Ordered, Acknowledged)**

- Player actions: shooting, ability activation
- Game state changes: item pickups, player death, score updates
- Cheat prevention: transaction verification

**Unreliable (Best-effort)**

- Position/rotation updates: newest packet supersedes old ones
- Voice chat: occasional loss is tolerable
- Particle effects, non-critical visual fluff

### Real-World Examples

- **Quake III Arena** (and many FPS games since)
- **ENet** library (popular in multiplayer indies)
- **RakNet** (used in *Minecraft* before Microsoft acquisition)

This approach avoids **head-of-line blocking** (where one lost packet stalls everything behind it) while ensuring critical data arrives. It's the best of both worlds for interactive, real-time applications where milliseconds matter.
