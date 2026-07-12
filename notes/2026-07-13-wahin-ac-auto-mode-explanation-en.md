---
audio: false
generated: true
image: false
lang: en
layout: post
title: WAHIN AC Auto Mode Explanation
translated: false
type: note
---

Question: How does the "auto" mode work on a WAHIN air conditioner remote control?

Answer:

I couldn't find a WAHIN-specific manual online (WAHIN/华凌 is a Midea sub-brand, and their manuals aren't well indexed), so here's how AUTO mode works in general — WAHIN follows the same standard logic as virtually every split/window AC on the market, since these units use the same generic microcontroller reference designs (often from the same OEM firmware suppliers Midea uses across brands).

**Core logic:**

```
loop every ~few seconds:
    room_temp = read_sensor()
    if room_temp > set_temp + hysteresis:
        mode = COOL  # compressor runs, blows cold air
    elif room_temp < set_temp - hysteresis:
        mode = HEAT  # (only on heat-pump models; reverses refrigerant cycle)
    else:
        compressor = OFF
        fan = LOW / intermittent  # just circulates air

    fan_speed = AUTO  # unit picks speed based on |room_temp - set_temp|
```

Key things you can't override in AUTO mode:

1. **No manual mode selection** — you can't force COOL/HEAT/DRY/FAN; the unit picks based on the temperature delta.
2. **No manual fan speed** — the FAN button is usually disabled or does nothing meaningful in AUTO; the compressor/fan logic is fully automatic (this matches what YMGI's manual describes: when selecting auto mode, the air conditioner will operate to factory settings, and the set temperature can't be adjusted and will not appear on the display — though some brands, like Samsung, do let you tweak the setpoint in AUTO).
3. **Hysteresis band** — there's a dead zone (typically 1–2°C around the setpoint) to prevent the compressor from short-cycling. Once the room drifts outside that band, the compressor kicks back on — this matches the general pattern where the compressor turns off once desired temperature is reached, and turns back on once the temperature deviates from the setpoint again.
4. **Heat-pump units** will flip refrigerant flow direction to switch between cooling and heating automatically, non-heat-pump (cooling-only) units will just alternate between COOL and FAN.

**Practical note for you:** if you want deterministic behavior (e.g., for automating your AC via an IR blaster + ESP32/Home Assistant, which fits your agentic/CLI-tooling instincts), don't use AUTO — capture the raw IR codes for explicit COOL/16°C/fan-high etc. instead. AUTO mode's actual thresholds aren't in the IR protocol at all; the decision-making happens in the indoor unit's firmware, not the remote, so you can't introspect or override the hysteresis logic from the remote side. If you want, I can show you how to sniff and replay WAHIN's IR codes with an ESP32 + IRremoteESP8266 to build deterministic automation instead of relying on its AUTO black box.

References:

- [Air Conditioner Remote Controls & AC Settings: Your Ultimate Guide](https://cielowigle.com/blog/air-conditioner-remote-control-ac-settings/)
- [YMGI Remote Control Features & Functions Manual](http://ymgigroup.com/wp-content/uploads/2018/10/YMGI-59-4-remote-users-manual.pdf)
- [Samsung: How do I use the remote control of my air conditioner?](https://www.samsung.com/latin_en/support/home-appliances/how-do-i-use-the-remote-control-of-my-air-conditioner/)
