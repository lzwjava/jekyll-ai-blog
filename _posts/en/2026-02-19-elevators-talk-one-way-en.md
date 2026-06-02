---
audio: false
generated: true
image: false
lang: en
layout: post
title: Elevators Talk One Way at Once
translated: false
type: note
---

**Yes — in normal everyday use, elevators are half-duplex communication systems.**

Most people experience this without ever thinking about the term:

| Situation                          | Can you talk?          | Can the other side talk back at the same time? | Duplex type      |
|------------------------------------|------------------------|--------------------------------------------------|------------------|
| You press the intercom/alarm button inside the elevator | You speak              | Usually **no** (or very poor quality)           | Half-duplex      |
| Security / firefighter / technician speaks to you | They speak             | You usually cannot interrupt / talk simultaneously | Half-duplex      |
| Modern very high-end installations | Sometimes full duplex  | Rare                                            | (Full-duplex)    |

### Why most elevators are half-duplex

1. **Oldest and still most common system**: simple analog intercom using a single voice wire pair
   → physically impossible to do full-duplex without echo cancellers

2. **Cost-optimized 2-wire systems** (even many post-2000 installations)
   → They use "push-to-talk" style half-duplex operation (like old walkie-talkies or many cheap VoIP door phones)

3. **Acoustic reality inside small metal box**
   Even when the hardware technically allows full-duplex, echo + very high gain → howling/Larsen effect very easily → most manufacturers deliberately keep it half-duplex or add very aggressive echo suppression that basically makes it feel half-duplex anyway.

### You usually get full-duplex only when:

- Digital IP-based elevator emergency phone (new high-rise, hospitals, luxury buildings)
- System explicitly advertises "full-duplex communication"
- Uses decent acoustic echo cancellation (AEC) + noise suppression
- Often 4G/5G VoIP or SIP-based units installed after ~2018–2020

**TL;DR meme version most people would recognize:**

Elevator intercom:
You: "HELLO?? I'M STUCK BETWEEN 7 AND 8!!!"
Control room: "…hello can you hear me?"
You: (still holding button) "YES HELLO???"
Control room: (talking at same time) "please release the button so I can—"
→ both talking on top of each other → nobody understands anything → classic half-duplex pain

So yeah… elevator is half duplex. 😭
