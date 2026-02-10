---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Measure Wi-Fi, Fix Zoom Lag Properly
translated: false
type: note
---

Question: What do you think about the importance of proper measurements when troubleshooting home Wi-Fi issues (such as Zoom lag in a duplex with a wireless repeater), rather than relying only on subjective feelings, and considering factors like different times of day?

Answer: 

Yes, you're 100% correct — **reliable, repeatable measurement is the single most important thing** when trying to improve or debug home networking, especially in a challenging environment like a two-floor duplex with a wireless repeater.

Subjective feelings ("it feels better", "Zoom is smoother now") are very misleading because:

- Human perception of delay is non-linear (50 ms extra lag is often barely noticeable, but 200–400 ms suddenly feels terrible)
- Placebo effect is strong
- Memory of "before" vs "after" is unreliable
- You tend to test right after making a change → during a temporarily quiet RF environment

### Why measurements matter more in this exact scenario

Your setup (floor 1 main router → wireless repeater on floor 2) is one of the most fragile common home network topologies:

- Every hop over Wi-Fi halves effective throughput in practice (even with good repeaters)
- 10 meters vertical + floor penetration usually means heavy signal attenuation (concrete/steel rebar can make it worse)
- 5 GHz has poor penetration → most repeaters fall back to 2.4 GHz for the uplink → low speed + high interference
- 2.4 GHz band is almost always congested in apartment buildings

Because of all these variables, small changes (moving router 1 meter, changing channel, time of day) can swing latency/jitter/packet loss dramatically.

### What actually helps (measurement-first mindset)

Here are the most useful measurements you should collect, roughly in order of priority for your Zoom lag problem:

1. **Actual application metrics during real meetings** (best signal of truth)
   - Use **Zoom statistics** (click the upward arrow during meeting → Statistics):
     - Network sending/receiving latency
     - Jitter
     - Packet loss %
     - Bandwidth used
   - Keep the Statistics window open and take screenshots every 2–3 minutes during different times of day

2. **Continuous ping + jitter measurement**
   - `ping -n 300 zoom.us` or better: ping to the nearest Zoom POP (you can find it via `pingzoom.net` or traceroute during meeting)
   - Even better: use **mtr** (WinMTR on Windows, mtr on macOS/Linux) to the Zoom server — shows packet loss and jitter hop by hop

3. **Wi-Fi link quality between repeater and main router**
   - Log into the **repeater's web interface** (usually 192.168.0.254 or similar) and check:
     - Signal strength (RSSI) of the connection to main router (aim for ≥ -65 dBm, ideally -55 or better)
     - Link rate (Mbps) — if it's stuck at 54 Mbps or 72 Mbps on 2.4 GHz, that's your bottleneck
     - Channel utilization / interference

4. **Speed & bufferbloat test at different times**
   - waveform.com/tools/bufferbloat or dslreports.com/speedtest
   - Run 5–10 times at peak evening hours vs early morning

5. **Simple repeatable throughput test between floors**
   - iperf3 between a wired PC on floor 1 and wireless PC on floor 2
   - Or just large file copy from NAS/PC on floor 1 to floor 2 laptop

### Quick thoughts on your attempts so far

- Moving main router out of cabinet → usually helps (reduces 3–8 dB attenuation)
- 10 m fiber + AP in bridge mode on floor 2 → should be dramatically better than repeater (if you actually did this wired backhaul)
- Coaxial MoCA → excellent choice if coax exists between floors (usually gives 400–900 Mbps reliable)
- Macao SIM card → very good for upload-sensitive applications like Zoom when mainland ISPs have poor international routing

If wired backhaul (fiber/MoCA/Ethernet) is possible and still has bad Zoom performance, then the problem is most likely:

- ISP → international routing / CGNAT / QoS throttling
- Apartment shared riser congestion
- Zoom server you connect to is far away

In that case measurements to international destinations (ping/ traceroute / iperf to US/EU servers) become even more important.

### Bottom line

You're thinking the right way: **feelings lie, numbers don't**.

The people who fix Wi-Fi problems fastest are usually the ones who obsessively collect before/after numbers instead of randomly trying configurations.

Keep measuring the same way (same Zoom call participants, same time window, same test target) — that's how you actually know whether a change helped.

References:  

- None (general networking knowledge and common troubleshooting practices)