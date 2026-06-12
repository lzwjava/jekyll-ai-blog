---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPS Fix Mystery Explained
translated: false
type: note
---

**Question:** Yin Wang claims his in-flight observation — phone GPS fix over Europe but not over Asia — proves GPS satellites don't exist and positioning comes from ground-based long-wave stations. What do you think?

**Answer:**

I'll be direct, because you value truth-seeking over deference to idols: Yin Wang is a brilliant PL thinker, but this post is wrong, and the observation he describes has a mundane, well-understood explanation. The Europe-works/Asia-fails asymmetry doesn't even weakly support the ground-station hypothesis — it's almost certainly **ephemeris expiry plus cold-start failure under weak signal**, which is one of the most common GNSS receiver behaviors there is.

**Why the fix worked over Europe**

A GPS receiver needs two things: signal lock on ≥4 satellites, and the **ephemeris** (precise orbital parameters) for each. Ephemeris is broadcast in the navigation message at **50 bits/second** — it takes ~30 seconds of *continuous, clean* lock per satellite to download. But ephemeris stays valid for ~4 hours, and phones cache it. Phones also cache the almanac (coarse orbits, valid for weeks) and use A-GPS to pre-download ephemeris over the network before you ever board.

So on the Europe leg, his phone likely had **fresh cached ephemeris** from before takeoff (or from airport WiFi). With valid ephemeris, a receiver only needs ~1 second of code-phase lock to compute pseudoranges — it can tolerate the weak, attenuated signal leaking through cabin windows. Fast fix, continuously updating. Exactly what he saw.

**Why it failed over Asia**

Hours later, the cached ephemeris had expired. Now the phone needs a **cold/warm start**: demodulate 50 bps navigation data from scratch, requiring ~30s of uninterrupted lock per satellite at decent C/N₀. Inside a metal fuselage, away from the window, signals are 15–25 dB attenuated and multipath-ridden — enough to *track* a known satellite, not enough to *decode* the nav message. Result: "无法定位," repeatedly. The default-location dot on the equator off Africa is just (0°, 0°) — Null Island, the classic uninitialized lat/lng.

Note the elegant part: this explanation predicts the *exact* asymmetry he observed — works early in the flight, fails late — with zero new physics.

**Why the long-wave ground-station theory fails on its own terms**

GPS L1 is 1575.42 MHz, λ ≈ 19 cm — microwave. It doesn't diffract around a fuselage; it enters through windows and bounces around the cabin (windows are large relative to 19 cm). His "must be long wave" inference assumes signals can't reach a phone away from the window, but reflections handle that fine. Meanwhile, actual long-wave systems (eLoran, ~100 kHz) give ~10–100 m accuracy *at best* with dedicated antennas — a phone has no antenna remotely capable of receiving 100 kHz, physically. And a ground-station network "covering European airspace but not Asia" would somehow need to produce Doppler shifts and geometry consistent with transmitters moving at 3.9 km/s in 20,200 km orbits, which brings me to:

**The falsifiable experiment (the part that matters)**

You don't have to trust anyone. Raw GNSS measurements are exposed on Android:

```java
// Android GnssMeasurement API — per-satellite raw data
// svid, Cn0DbHz, PseudorangeRateMetersPerSecond (= Doppler), state
```

Easiest path: install **GPSTest** (open source, barbeau/gpstest on GitHub) and look at the Doppler column. You'll see ±4 kHz shifts on L1, varying smoothly as satellites rise and set over ~6 hours — exactly the signature of MEO orbits, impossible for any stationary ground transmitter (a ground station would give Doppler proportional only to *your* velocity).

Or go full first-principles with a $30 RTL-SDR on your RTX 4070 box:

```bash
# Capture L1 and decode the actual navigation message yourself
rtl_sdr -f 1575420000 -s 2048000 -g 40 gps_l1.bin
# Feed into gnss-sdr — it will acquire PRNs, decode ephemeris,
# and output your position from raw RF. No Google, no OS, no trust.
gnss-sdr --config_file=gps_l1_rtlsdr.conf
```

You can then take the decoded ephemeris, propagate the orbits, and predict *when each satellite rises over your horizon in Guangzhou tomorrow* — and verify the prediction against tomorrow's capture. A ground-station conspiracy can't survive that loop: you'd be decoding orbital elements that correctly predict future signal geometry from physics.

There's a lesson here that fits your philosophy better than the post does: first-principles thinking means *running the experiment that could prove you wrong*, not interpreting ambiguous observations to confirm a prior. Yin Wang had a phone capable of dumping per-satellite Doppler in his pocket and didn't look. Respect the PL work; verify the physics claims yourself — you have all the hardware to do it this weekend.

**References:**

- [Android GnssMeasurement docs](https://developer.android.com/reference/android/location/GnssMeasurement)
- [gnss-sdr — open-source GNSS software-defined receiver](https://gnss-sdr.org/)
- [GPSTest (open source Android GNSS tool)](https://github.com/barbeau/gpstest)
- [GPS Interface Control Document IS-GPS-200 (nav message, 50 bps, ephemeris)](https://www.gps.gov/technical/icwg/)
