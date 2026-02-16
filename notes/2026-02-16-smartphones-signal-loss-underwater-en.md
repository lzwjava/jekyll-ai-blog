---
audio: false
generated: true
image: false
lang: en
layout: post
title: Smartphones Lose Signal Underwater Fast
translated: false
type: note
---

Question: How do electromagnetic waves behave in water, and what happens to a smartphone's signal if thrown into water inside a bag?

Answer: 

Electromagnetic (EM) waves, including radio waves used by smartphones (cell signals, Wi-Fi, Bluetooth), behave very differently in water compared to air due to **absorption** and **attenuation** caused by water's electrical properties.

### Behavior of EM Waves in Water
- Water (especially salty seawater) is a **conductive medium**, which causes rapid energy loss in EM waves.
- Higher frequency waves (like those used by modern phones) experience **much stronger attenuation** than lower frequency waves.
- Key factors:
  - **Seawater** (high conductivity ~4 S/m): Extremely high attenuation.
  - **Fresh water** (low conductivity ~0.01 S/m): Much lower attenuation, but still significant for phone frequencies.
- Attenuation increases sharply with frequency:
  - At cell phone frequencies (typically 700 MHz – 2.6 GHz for 4G/5G) and Wi-Fi/Bluetooth (2.4 GHz or 5 GHz), attenuation is very high.
  - In seawater, attenuation at 2.4 GHz can exceed **700 dB per meter** — meaning the signal drops to almost nothing after just a few centimeters.
  - In fresh water, attenuation is lower (around 1–several dB/m at these frequencies), but still severe enough to block signals quickly.

Lower frequencies (like ELF/VLF used by submarines) penetrate much farther, but consumer devices like smartphones cannot use those.

### Smartphone Signal When Thrown into Water (e.g., in a Bag)
Modern smartphones use high-frequency radio waves for cellular, Wi-Fi, and Bluetooth — all of which are heavily attenuated by water.

- **Practical outcome** — Almost no usable signal underwater:
  - In **seawater** (ocean, sea): Signal is lost within **centimeters** (often <10–20 cm) of the surface. Even just below the surface, connection fails.
  - In **fresh water** (pool, lake, river): Slightly better penetration, but still typically lost within **10–50 cm** depth (sometimes a bit more in very shallow submersion or near the surface with good alignment).
  - Experiments and reports show smartphones lose cell signal, Wi-Fi, and Bluetooth almost immediately when fully submerged — even waterproof phones cannot maintain a connection underwater without special techniques.
- A protective bag (e.g., waterproof pouch) doesn't help with signal propagation — it may keep the phone dry and functional internally, but the EM waves still cannot penetrate the surrounding water effectively to reach cell towers or Wi-Fi routers.
- Very shallow submersion (just a few cm, antenna near surface) might allow weak/intermittent signal in fresh water under ideal conditions, but this is unreliable and not practical.

In summary: Throwing a smartphone (even in a waterproof bag) into water will cause it to **quickly lose all wireless signal** (cellular, Wi-Fi, data) in both fresh and salt water. The phone might still work internally (screen, apps, etc.) if waterproof, but it will be offline until brought back near or above the surface.

References:  

- [https://en.wikipedia.org/wiki/Electromagnetic_absorption_by_water](https://en.wikipedia.org/wiki/Electromagnetic_absorption_by_water)
- [https://www.researchgate.net/figure/Attenuation-experienced-by-EM-signals-in-fresh-and-seawater-for-different-frequencies_fig1_302259776](https://www.researchgate.net/figure/Attenuation-experienced-by-EM-signals-in-fresh-and-seawater-for-different-frequencies_fig1_302259776)
- [https://www.scirp.org/journal/paperinformation?paperid=5906](https://www.scirp.org/journal/paperinformation?paperid=5906)
- [https://electronics.howstuffworks.com/would-a-cell-phone-work-on-a-submerged-submarine.htm](https://electronics.howstuffworks.com/would-a-cell-phone-work-on-a-submerged-submarine.htm)
- [https://underwatermessaging.cs.washington.edu/underwater_comms.pdf](https://underwatermessaging.cs.washington.edu/underwater_comms.pdf)