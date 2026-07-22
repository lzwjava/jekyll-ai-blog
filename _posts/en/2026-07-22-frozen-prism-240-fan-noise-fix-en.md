---
audio: false
generated: true
image: false
lang: en
layout: post
title: Frozen Prism 240 Fan Noise Fix
translated: false
type: note
---

Question: What if my Thermalright Frozen Prism 240 White ARGB AIO fans make non-stop noise?

Answer:

A **240 mm AIO should not produce loud, constant fan noise at idle**. Some fan noise is expected under load, but if it's running near maximum speed all the time, something is usually misconfigured or the system is genuinely hot.

Here are the most common causes, in order of likelihood:

| Cause                      | Symptoms                              | Fix                                            |
| -------------------------- | ------------------------------------- | ---------------------------------------------- |
| Fan curve set to 100%      | Constant loud airflow even at idle    | Configure PWM curve in BIOS                    |
| Fans connected incorrectly | Fans always at full speed             | Connect fans to CPU_FAN or CPU_OPT PWM headers |
| PWM disabled               | Fans ignore speed control             | Set header to PWM mode instead of DC           |
| High CPU temperature       | Fans constantly ramp                  | Check thermal paste, pump, CPU load            |
| Pump noise                 | High-pitched whine instead of airflow | Lower pump RPM if supported                    |
| Cheap stock fans           | Motor or bearing noise                | Replace fans                                   |

### 1. Configure a proper fan curve

Many motherboards default to aggressive cooling.

A reasonable curve:

```
CPU Temp    Fan Speed
30°C        20%
40°C        30%
50°C        45%
60°C        60%
70°C        80%
80°C        100%
```

With a modern CPU, this usually keeps the system nearly silent during web browsing or coding.

---

### 2. Check PWM mode

The Thermalright fans are **4-pin PWM**.

In BIOS:

```
CPU_FAN
    Mode = PWM
```

If the motherboard detects them as DC fans, they'll often stay much louder.

---

### 3. Pump speed

Most AIOs recommend:

```
Pump:
    60–100%
```

Some pumps become noisier around certain RPMs due to resonance.

Example:

```
100% -> quiet
70%  -> buzzing
50%  -> quiet
```

It's worth testing a few fixed speeds.

---

### 4. Thermalright stock fans

The included 120 mm fans are generally **good for the price**, but they're **not among the quietest**.

Compared to premium fans:

| Fan                      | Noise           |
| ------------------------ | --------------- |
| Thermalright stock       | decent          |
| Noctua NF-A12x25         | excellent       |
| be quiet! Silent Wings 4 | excellent       |
| Arctic P12 PWM PST       | excellent value |

Many people keep the radiator and replace only the fans later.

---

### 5. Check actual temperatures

If your CPU is

```
Idle: 30–45°C
```

but fans are spinning at 1800 RPM,

that's almost certainly a fan curve issue rather than a cooling issue.

If idle is

```
65–80°C
```

then investigate:

* cooler mounting pressure
* thermal paste
* pump operation
* plastic protective film left on the cold plate (surprisingly common)

---

### 6. What about this specific cooler?

The **Thermalright Frozen Prism 240 White ARGB** is generally considered a solid budget 240 mm AIO. Its cooling performance is competitive for its price, but acoustics are not its standout feature. The advertised maximum fan speed of **1850 RPM** means that if the fans spend much time near their maximum speed, you'll definitely hear them.

If your priority is **low noise**, you can:

* Use a gentler PWM fan curve.
* Enable motherboard fan hysteresis (to avoid rapid speed changes).
* Replace the stock radiator fans with quieter models while keeping the same radiator.

### How loud should it be?

With a correctly configured system:

* **Idle (desktop, coding):** nearly inaudible or a soft whoosh.
* **Compiling or gaming:** clearly audible but not distracting.
* **Stress tests (Cinebench, Prime95):** loud is normal because the fans may approach 1850 RPM.

If the cooler is **loud 100% of the time**, even when the CPU is cool and idle, that's not expected behavior and is usually caused by BIOS fan settings or an installation issue rather than the cooler itself.