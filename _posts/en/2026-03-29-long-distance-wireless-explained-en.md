---
audio: false
generated: true
image: false
lang: en
layout: post
title: Long Distance Wireless Communication Explained
translated: false
type: note
---

Question: How should I understand the statement about sending a Wi-Fi signal from Guangzhou to Dongguan and using PPPoE for decoding, along with the mention of licensed U and V bands?

Answer:

This statement mixes Wi-Fi theory, long-range wireless, and regulatory considerations:

1. **Long-distance Wi-Fi (Guangzhou → Dongguan):**

   * The straight-line distance is roughly 70–80 km. Standard Wi-Fi (2.4 GHz or 5 GHz) cannot cover this distance with normal equipment because of path loss, obstacles, and regulatory power limits.
   * **Line-of-sight (LoS)** and very high-gain antennas (directional dishes) are essential for any hope of long-distance links.

2. **PPPoE “decoding”:**

   * PPPoE (Point-to-Point Protocol over Ethernet) is a network protocol for encapsulating PPP frames over Ethernet. Here, the speaker probably means using PPPoE to establish a “point-to-point” logical connection over a long wireless link.
   * In theory, if you had a very strong directional link, PPPoE could carry your Internet traffic over it, but this is purely logical—it doesn’t magically extend signal range.

3. **Licensed U and V frequency bands:**

   * These are microwave or millimeter-wave frequency bands that often require a government license.
   * Using these bands can give higher power allowances and less interference, making long-distance links feasible.
   * But **unlicensed use is illegal** and limited in time/power. So you can’t just broadcast constantly at high power without a license.

**In short:** The person is saying: “With standard Wi-Fi you can’t reach Dongguan from Guangzhou. If you had high-power equipment and a licensed frequency (like U/V band), theoretically you could set up a point-to-point connection using protocols like PPPoE—but only legally and safely under regulatory limits.”

This is more about **regulatory physics than typical home Wi-Fi**.

If you want, I can calculate the **theoretical maximum range for 2.4 GHz Wi-Fi with directional antennas**, just to see if it’s even remotely feasible. Do you want me to do that?
