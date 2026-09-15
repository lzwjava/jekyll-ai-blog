---
audio: false
generated: true
image: false
lang: en
layout: post
title: Thermal Imaging for Device Repair
translated: false
type: note
---

Question: **How do I get thermal images, and how useful are they for GPU / phone / laptop repair?**

Answer: **Very useful—but mainly for power/thermal faults, not as a universal X-ray.** A thermal camera gives you a spatial map of where electrical power is being dissipated.

The key mental model is:

$$
P = V I = I^2R = \frac{V^2}{R}
$$

A failed component, shorted rail, bad MOSFET, leaking capacitor, damaged IC, etc. can turn electrical power into localized heat. The thermal camera lets you see **where that heat is appearing** without touching the board.

![Image](https://images.openai.com/static-rsc-4/P73v6MC6zp_DzfbmsyxZ8_xMA7fYDMb7ZwbGKDR7ANWbYN8Tg5s11BIOdmfp6zlIq1Ji3NPsyJj4UkJB520xgx9ktXVDjDmU7BXtKQ6vcMjnpjTCHuqMzVNPEKDzNKzrcVb6tqa6-F-CiXK8nlO3Yg29Q6EJhCZvA1FB-J5rjEhjJFIcfgDlJ57BIkjneAAf?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/RIzkPptVXIggCsY5USK9MC-_4hJTCA8gcwslXy6ic-knLwl89IiEQlqh1wGJMOp8N6PMJxnNopAs8EPLRuDcIeinA5mdmaUzAXorEMb3uq72EOGURR8weo32Jz66CKfXoLz4AVmIA8o0a2xiO0Dtv1--bBRF6FxuxQ8LZdX_A9vrsfqStML1eXjaS-qIRHMK?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/X6xzI2kvMEAIXfx_nc77-MwL9uO8ZfjV4GDvaYHM21bjJ-3S0X_MVaTR_O9VbSEudL_6i4gxVE6U1-5Yn-8ZM1u1YkoGeHbOT7r8tlAtdAmcazJAjNu4VdL4pavOshg6lOdLqWj2oHgUed2wKOX2L8nPwdONtTPTlbZN67h1svnin_Mqn6KpRoBMU3zVbbwM?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/pF8_6QWJsiQix__JQPlXZVQU7-QX-Cbm7ByyuElSraijLjz-sOY81d23Mit8EugWF9YXUShQHbFmm8jI_6r6RxQA2G5rs7aSI49DhxiXfGc-5DACgSvPIF7hxajEd2cvtTDl4Esqgx-64-Dki1-BTv2S7iCtltJwI2t6V2LCDyaPoOVsnrn0yTSJsnD_wea0?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3Z3G7OfDVBjgmIGxmR7iBq0reqAJR2TcmRaAYFDsLSS49Ul6lBLNh2piIcB_qozRYg1t7IR4FdCDJ7eu0UBGXFTiVoj_x_Fx6nnFtlpPHyzpClfWS3D_NHJmycmN5k8BPxU_1HnCUV-dJ5_V5_YM4LfSRj-wLh9PJFvQ5UQaiLI1LWVSarECUjX7FYEW9IX8?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/_apHiPSCN1xMtmTD_-hDf1dRk3RZI9QwGsh-m9ATjeUF32X4-8zloYchM7AKCw5JLZ4YjB-ZHsaEjYg5_LShBySq3sUTd4lNV-b5OrSg23euyTAGrLIiZRopiAlMeChbzmE_uG1im-fKa1GnwbOIfNQ7LncA2dK-xNjKDzqrWEAavdKtF4kEN2H79YPnILFd?purpose=fullsize)

### 1. GPU repair

This is probably one of the most interesting applications.

Suppose a GPU has:

```text
12V
 │
 ├── VRM ── GPU core
 │
 ├── memory VRM ── GDDR
 │
 └── other power rails
```

You power the board and scan it.

Normal:

```text
VRM      VRM       GPU
██       ██        █████
30°C     32°C      45°C
```

Faulty:

```text
VRM      VRM       GPU
██       🔥        █████
31°C     95°C      45°C
```

That immediately tells you **which region is consuming abnormal power**.

For example:

* shorted MLCC → tiny localized hotspot
* failed MOSFET → MOSFET gets extremely hot
* bad VRM → inductor/MOSFET area heats abnormally
* GPU core leakage → GPU package heats unusually
* damaged memory power rail → memory VRM becomes hot
* shorted power rail → component nearest the short may become the thermal signature

FLIR specifically describes PCB thermal imaging as useful for finding overheating components, power-component problems, and trace damage. ([FLIR][1])

### 2. Phone motherboard repair

This is where thermal imaging becomes **really powerful**.

Imagine:

```text
Phone won't boot

        ↓

Bench PSU
        ↓
Current = 0.8 A
        ↓
Thermal camera
        ↓
        🔥
       MLCC
        ↓
Shorted VDD rail
```

Instead of removing 50 capacitors one by one, you can often:

1. Identify the suspicious power rail.
2. Inject a **safe, current-limited voltage** into that rail.
3. Watch the board thermally.
4. Find the first component that heats.
5. Remove/replace it.
6. Verify that the thermal signature disappears.

That's an extremely useful repair workflow.

But there is an important limitation:

**The hottest component isn't necessarily the failed component.**

Heat can propagate through copper planes, packages, solder, etc. So thermal imaging gives you a **spatial clue**, not proof of causality.

---

### 3. Laptop repair

Also useful for:

* dead motherboard
* shorted 19 V rail
* shorted 5 V / 3.3 V rail
* CPU/GPU VRM problems
* overheating CPU/GPU
* bad MOSFET
* abnormal charging circuit
* USB-C PD failures
* battery/charging problems
* poor heatsink contact
* fan/cooling problems

For example:

```text
Normal laptop:

CPU       VRM          GPU
🔥🔥       🔥           🔥🔥
70°C      50°C         65°C


Fault:

CPU       VRM          GPU
🔥🔥       🔥🔥🔥🔥🔥    🔥🔥
70°C      110°C        65°C
              ↑
          investigate
```

But remember: **a hot component under normal load isn't automatically defective.** FLIR explicitly warns that equipment under load normally gets hot; you need to know what the normal thermal pattern should look like. ([FLIR][2])

---

## What camera should you buy?

You don't necessarily need a $5,000+ professional thermal camera.

For board repair, I'd look at **phone-connected thermal cameras**, especially one with enough spatial resolution to see individual components.

One interesting option is the **HIKMICRO Mini2 V2**:

* 256 × 192 thermal resolution
* <40 mK thermal sensitivity
* 25 Hz
* -20°C to 400°C
* USB-C / Lightning variants
* phone-powered
* ~20 g

[HIKMICRO Mini2 V2 official specs](https://www.hikmicrotech.com/en_us/industrial-products/mini2-v2-thermal-camera-phone-attachment/?utm_source=chatgpt.com)

More interesting for **actual PCB repair** is the **HIKMICRO Mini2Plus V2**, because it has a manual-focus macro mode. HIKMICRO claims it can resolve objects down to about **340 µm** with its desk-stand configuration and specifically mentions PCB components. ([Hikmicrotech][3])

That macro capability is much more relevant to repair than having a huge temperature range.

---

## The most important spec isn't temperature range

For board repair, I'd prioritize:

```text
1. Spatial resolution
2. Thermal sensitivity (NETD)
3. Macro / minimum focus distance
4. Manual focus
5. Frame rate
6. Image/video recording
7. PC/API access
8. Temperature measurement accuracy
```

You don't really care whether the camera can measure:

```text
-20 → 400°C
```

if a tiny 0.5 mm capacitor occupies only one pixel.

You care about whether:

```text
component
   ↓
████████
████████   ← enough pixels
████████
```

rather than:

```text
component
   ↓
█
```

---

## There's a second technique that's even more interesting

Don't just take thermal photos.

Use **thermal video while dynamically powering the board**.

For example:

```python
while True:
    frame = thermal_camera.read()

    hotspot = detect_hotspot(frame)

    if hotspot.temperature > threshold:
        print(hotspot.position,
              hotspot.temperature)
```

Then you can observe:

```text
t=0.0s   24°C
t=0.5s   27°C
t=1.0s   35°C
t=1.5s   52°C
t=2.0s   78°C  ← suspicious
```

That temporal behavior is extremely informative.

A normal IC might look like:

```text
24 → 30 → 38 → 45°C
```

while a short can look like:

```text
24 → 30 → 50 → 80 → 110°C
```

very quickly.

---

## And this opens an interesting AI application

Given your agent/model work, I wouldn't think of this as merely **"buy thermal camera → look at pictures."**

I'd build:

```text
thermal camera
      │
      ▼
thermal video
      │
      ▼
component localization
      │
      ├── PCB visual image
      │
      ├── schematic
      │
      ├── boardview
      │
      └── electrical measurements
      │
      ▼
LLM / vision model
      │
      ▼
"Likely fault region"
      │
      ▼
repair procedure
```

For example:

```text
Thermal:
    U7200 = 91°C
    surrounding area = 31°C

Multimeter:
    VCORE = 0.4V

Boardview:
    U7200 → VCORE regulator

Schematic:
    VCORE → GPU core

AI:

"U7200 is the highest-confidence abnormal
heat source. Given VCORE resistance of 0.8Ω,
the likely fault is excessive VCORE loading.
Check U7200 MOSFETs and downstream MLCCs."
```

Now thermal imaging becomes **one sensor in an automated board-debugging agent**, rather than just a fancy camera.

That's potentially much more interesting.

### One important caveat

Thermal images aren't ordinary RGB photos. Shiny copper/aluminum and other low-emissivity surfaces can produce misleading temperature readings because they reflect infrared radiation. FLIR recommends paying particular attention to emissivity and reflected temperature; their PCB example uses different emissivity assumptions for plastic vs. metal. ([FLIR Support Center][4])

So for repair work, learn to interpret **relative thermal patterns** first; don't blindly trust "this component says 83.2°C."

References:

* [FLIR — PCB thermal troubleshooting](https://www.flir.com/fr-fr/support/training/thermography-training/webinars/see_the_heat_troubleshooting_pcb_electronic_product_design_with_thermal_imaging/?utm_source=chatgpt.com)
* [FLIR — Electronics testing with thermal imaging](https://www.flir.com/globalassets/industrial/17-3553-ins-ets-brochure_final_v1_web.pdf?utm_source=chatgpt.com)
* [HIKMICRO Mini2 V2](https://www.hikmicrotech.com/en_us/industrial-products/mini2-v2-thermal-camera-phone-attachment/?utm_source=chatgpt.com)
* [HIKMICRO Mini2Plus V2 macro thermal camera](https://www.hikmicrotech.com/en/industrial-products/mini2plus-v2-thermal-camera-phone-attachment/?utm_source=chatgpt.com)
* [FLIR — Emissivity and thermal measurement](https://www.flir.com/discover/professional-tools/how-does-emissivity-affect-thermal-imaging/?utm_source=chatgpt.com)

[1]: https://www.flir.com/fr-fr/support/training/thermography-training/webinars/see_the_heat_troubleshooting_pcb_electronic_product_design_with_thermal_imaging/?utm_source=chatgpt.com "“See the Heat - Troubleshooting PCB & Electronic Product Design with Thermal Imaging Webinar | Flir"
[2]: https://www.flir.com/discover/professional-tools/thermal-camera-tips-to-avoid-common-home-inspection-mistakes/?utm_source=chatgpt.com "Thermal Cameras Tips to Avoid Common Home Inspection Mistakes | Flir"
[3]: https://www.hikmicrotech.com/en/industrial-products/mini2plus-v2-thermal-camera-phone-attachment/?utm_source=chatgpt.com "HIKMICRO Mini2Plus V2 Infrared Smartphone Camera For ios And Android"
[4]: https://flir.custhelp.com/app/answers/detail/a_id/1283?utm_source=chatgpt.com "FLIR - ETS320 camera use with FLIR Tools"
