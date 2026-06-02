---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: UUIDs Ensure Global Uniqueness Without Coordination
translated: false
type: note
---

UUIDs can serve the purpose of globally unique identification without a central authority because they are designed with an enormous address space: 128 bits, providing about 3.4 × 10^38 possible values. This is vastly larger than the number of UUIDs that will ever be generated in practical scenarios across all systems worldwide. For version 4 UUIDs (the random ones, like the one you shared), 122 of those bits are filled with high-quality random data, making duplicates extremely unlikely.

As for collisions: Yes, in theory, it's possible for two UUIDs to be identical, but the probability is so low it's effectively zero for real-world use. This follows the "birthday paradox" in probability—collisions become more likely as the number of items grows, but even then:

- The chance of any two random version-4 UUIDs colliding is about 1 in 2.71 × 10^18.
- You'd need to generate roughly 4.8 × 10^18 UUIDs (that's every person on Earth owning about 600 million each) for a 50% chance of just *one* duplicate.
- For context, even generating 1 trillion (10^12) UUIDs gives a collision risk of around 1 in a billion or less.

Different UUID versions add safeguards: version 1 uses timestamps and MAC addresses, version 5 hashes names with namespaces, etc. But version 4's randomness alone ensures uniqueness in distributed systems, databases, or apps without coordination.

[What are the odds?](https://jhall.io/archive/2021/05/19/what-are-the-odds/)
[Universally unique identifier - Wikipedia](https://en.wikipedia.org/wiki/Universally_unique_identifier)
[How big is the chance to get a Java UUID.randomUUID collision?](https://stackoverflow.com/questions/24876188/how-big-is-the-chance-to-get-a-java-uuid-randomuuid-collision)
