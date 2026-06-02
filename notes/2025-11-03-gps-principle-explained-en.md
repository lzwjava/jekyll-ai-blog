---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GPS Positioning Principle Explained Simply
translated: false
type: note
---

### Today's Second Science Popularization Task: A Video Explaining the GPS Positioning System Principle

I recommend everyone watch this video that explains the principles of the GPS positioning system. However, there was a small issue with one of the images in it, so I made a quick fix.

The principle is actually quite straightforward—it only requires basic solid geometry knowledge to understand. It can be summed up in one sentence: "The intersection of four spheres is a single point." Now, I'll break down exactly how this applies:

1. GPS satellites (or ground base stations) transmit information that includes their "coordinates" at the time of transmission and a "timestamp." (Figure 1)

   - When the GPS receiver picks up this signal, it can calculate the distance \\( r_1 \\) from that satellite to itself using the timestamp: \\( r_1 = \\) speed of light × transmission time.

   - All positions at a distance \\( r_1 \\) from this satellite lie on a sphere with radius \\( r_1 \\). For simplicity, I'll call this the "equidistant sphere." Geometry tells us that the intersection of two spheres is a circle, so the intersection of this "equidistant sphere" with Earth is a circle (Figure 2a—it takes a bit of 3D visualization). Clearly, with just one satellite's signal, we can't pinpoint our exact location; we only know we're somewhere on that circle.

   If we receive signals from a second satellite with its position and distance, we can draw another sphere. The intersection of these two equidistant spheres with Earth—three spheres in total—gives the possible positions where we might be. This intersection is most likely just two points, but we don't know which one is correct. (Figure 2b)

   With a third satellite's position and distance, its equidistant sphere will most likely pass through one of those two points but not the other. This determines the receiver's coordinates on the ground. (Figure 2c)

   If we get a signal from a fourth satellite, its equidistant sphere will also pass through that same point. So, if we only need ground coordinates, the fourth satellite isn't strictly necessary. (Figure 2d)

All of this can really be boiled down to one key insight: the intersection of four spheres is a single point. The three equidistant spheres from the satellites, plus Earth itself (as the fourth sphere), intersect at a unique point—just one location.

Note that these signals don't have to come from satellites. Ground base stations with known coordinates can transmit the same type of signal (coordinates + timestamp), and the receiver can calculate its position in the exact same way—it's simply geometric intersection computation.

**Exercise 1:** In the second step, because there's typically a time difference between the receiver's clock and the GPS satellite's clock, you can't get the "transmission time" from just one signal. But if the same satellite sends two signals, you can eliminate this offset and calculate the transmission time. Try to figure out why on your own.

**Exercise 2a:** In the fourth step, I said the intersection of the two equidistant spheres and Earth is "most likely" just two points. In what special cases would this intersection be more than two points? What other shape might it take?

**Exercise 2b:** In the fifth step, I said the third satellite's equidistant sphere "most likely" passes through one of the two points but not the other. In what special cases would its equidistant sphere pass through both points at once?

**Exercise 3:** With signals from four satellites, you can not only calculate coordinates but also altitude (elevation). So why is the fourth satellite still useful?

**Exercise 4:** If we're relying entirely on ground base stations, we can calculate coordinates using signals from three stations. With a fourth base station's signal, can we calculate altitude? If so, what condition must the positions of these four base stations satisfy?

**Exercise 5:** If the setup in Exercise 4 is feasible, design a "ground-based GPS system" that doesn't use satellites at all but fully replicates the functionality of a satellite GPS system. It should meet the needs of everyday vehicle and pedestrian navigation, aviation, maritime travel, hiking, off-roading, and more. The system must be cost-effective, with expenses no higher than those of a satellite-based system.

[Original Post: GPS Principles](https://yinwang1.substack.com/p/gps)
