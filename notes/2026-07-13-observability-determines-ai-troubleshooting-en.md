---
audio: false
generated: true
image: false
lang: en
layout: post
title: Observability Determines AI Troubleshooting
translated: false
type: note
---

Question: For hardware/software/daily-life troubleshooting, is writing a complete incident description and prompt more important for AI assistance, while software issues can be delegated to Claude Code/Hermes to inspect source code?

Answer:

Yes. The key difference is **observability**.

For software issues, AI agents like Claude Code or Hermes have direct access to the "ground truth":

```
source code
logs
stack traces
git history
tests
runtime environment
```

They can do:

```
read code
↓
trace execution path
↓
find bug location
↓
modify code
↓
run tests
```

Example:

```
Bug:
API returns 500 when user uploads a 20MB image.

Agent can:
- grep endpoint
- inspect controller
- inspect middleware
- reproduce
- patch code
```

The agent has the evidence.

---

For hardware / mechanical / daily-life problems, AI usually does NOT have direct sensors.

Example:

"Computer doesn't boot"

AI cannot see:

* motherboard LED status
* cable connection
* PSU behavior
* smell/noise
* physical damage
* exact BIOS screen

So the quality depends heavily on the **incident report**.

A good hardware prompt is basically a debugging ticket.

Structure:

```
1. Goal
What should happen?

2. Actual behavior
What happens instead?

3. Timeline
When did it start?

4. Environment
Hardware/software/version/location

5. Recent changes
What changed before failure?

6. Evidence
Photos, videos, logs, measurements

7. Experiments already tried
What worked / failed?

8. Constraints
What tools are available?
```

Example:

Bad prompt:

```
My PC cannot boot. Help.
```

AI has almost no information.

Good prompt:

```
Problem:
Desktop PC powers on but no display.

Hardware:
- MSI MAG B760M Mortar WiFi motherboard
- Intel i9-13900KF
- RTX 4070
- DDR5 32GB
- Corsair 750W PSU

Timeline:
Worked normally for 2 years.
Yesterday after moving the PC, it stopped displaying.

Symptoms:
- CPU fan spins
- GPU fans spin briefly
- EZ Debug LED:
  CPU light off
  DRAM light on

Tests:
1. Removed GPU, tried integrated graphics
2. Reseated RAM
3. Tried one RAM stick
4. Cleared CMOS

Question:
Based on these symptoms, what is the most likely failure order?
```

Now AI can reason like an engineer:

```
DRAM LED + reseat failed
↓
check RAM compatibility
↓
check motherboard slot
↓
check memory training
↓
possible CPU memory controller
```

---

For mechanical / real-world problems, the same principle applies.

Example:

Bad:

```
Car makes noise.
```

Good:

```
Car:
Toyota Corolla 2018

Noise:
- metallic clicking
- only when turning left
- disappears above 40 km/h
- started after hitting pothole

Question:
What components should I inspect first?
```

Now the AI can perform differential diagnosis.

---

The general pattern:

```
Software debugging:
AI gets raw data directly
(code/logs)

Hardware debugging:
Human must become the sensor
(description/photos/videos)
```

A useful mental model:

```
Software agent:
       AI
        |
   source code
        |
      bug


Hardware:
      AI
       |
 human observation
       |
 physical system
       |
      fault
```

For hardware, the prompt is not just communication. It is the **data acquisition layer**.

This is similar to machine learning:

```
Bad prompt = bad dataset
Good prompt = high-quality training sample
```

The better the input representation, the better the diagnosis.

A strong workflow is:

```
Physical problem
    ↓
collect evidence
    ↓
write structured incident report
    ↓
ask AI for hypothesis ranking
    ↓
perform cheapest/safest test
    ↓
update evidence
    ↓
repeat
```

This is basically applying software debugging methodology to the physical world.
