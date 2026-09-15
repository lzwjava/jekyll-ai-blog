---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flight Testing as an Engineering System
translated: false
type: note
---

Question: You’re asking whether a flight-control company should systematically capture field testing—not just notebook notes—so that the company accumulates durable operational knowledge that new engineers can actually learn from.

Answer: **Yes. In fact, I’d treat this as an engineering system, not just “record some videos.”**

For something like a DJI-style flight-control / drone company, the valuable knowledge is often **procedural and visual**:

* What does a normal test look like?
* What does a dangerous oscillation look/sound like?
* What did the operator do immediately before the failure?
* What telemetry was showing at the same moment?
* What environmental conditions existed?
* Which debugging steps worked?
* Which “obvious” fixes turned out to be wrong?
* What does an experienced test engineer notice that a new engineer doesn't?

A notebook captures **what someone remembers**.
A video captures **what actually happened**.
Telemetry captures **what the machine was doing**.
Photos capture **the physical configuration/environment**.

The real value comes from putting them together.

### I would build a "flight test case" around every meaningful test

For example:

```text
flight-tests/
  2026-09-15/
    FT-2026-0915-037/
      manifest.yaml
      briefing.md
      preflight/
        aircraft.jpg
        propellers.jpg
        wiring.jpg
        payload.jpg
      video/
        ground-camera.mp4
        onboard-camera.mp4
      telemetry/
        flight.ulg
        flight.csv
      audio/
        radio.wav
      photos/
        site-01.jpg
        aircraft-after-flight.jpg
      debrief.md
      incidents.md
      analysis/
        plots.png
        analysis.ipynb
```

And `manifest.yaml` contains the machine-readable context:

```yaml
test_id: FT-2026-0915-037
aircraft: A17
firmware: fc-2.8.14
controller: position-controller-v4
battery: B204
operator: engineer-042

objective:
  - validate position hold after controller change

environment:
  wind_mps: 7.2
  temperature_c: 23
  location: TEST_SITE_A

software_changes:
  - "increase yaw damping from 0.12 to 0.15"

result: PASS_WITH_NOTES
```

Then the debrief shouldn't be a giant essay. Something like:

```markdown
# FT-2026-0915-037

## Objective
Validate position hold after yaw damping change.

## Result
PASS_WITH_NOTES

## What happened

00:00:00 - preflight
00:03:21 - takeoff
00:04:10 - position hold enabled
00:04:17 - small yaw oscillation begins
00:04:23 - oscillation disappears
00:06:02 - landing

## Observations

- Yaw response is noticeably faster than previous firmware.
- Small oscillation appears only during first transition.
- No safety issue observed.

## Evidence

- `video/ground-camera.mp4`
- `telemetry/flight.ulg`
- `photos/aircraft-after-flight.jpg`

## Engineer interpretation

Likely transient caused by the new damping parameter interacting
with the position-hold transition.

## Follow-up

Repeat with:
- 4 m/s wind
- 10 m/s wind
- old firmware as control

## Lessons

Do not judge the parameter solely from steady-state behavior.
The transition is where the new behavior appears.
```

Now you've created something much more powerful than "John wrote in his notebook that the drone was weird."

### The important thing: synchronize everything by time

This is where I think the system becomes genuinely valuable.

Imagine a future engineer asks:

> "Why did we stop using controller v4.2?"

Instead of searching Slack for three hours:

```text
Controller v4.2
       │
       ├── 17 flight tests
       │
       ├── 3 anomalies
       │
       ├── FT-2025-0821-014
       │       ├── video.mp4
       │       ├── telemetry.ulg
       │       ├── photos/
       │       └── debrief.md
       │
       └── conclusion
             "unstable during high-wind transition"
```

They can literally watch the failure while looking at the telemetry.

That is **organizational memory**.

### And don't only record failures

This is a subtle but important point.

You want:

```text
GOOD flight
BAD flight
EDGE CASE
RECOVERY
NORMAL PROCEDURE
EXPERIMENT
```

Otherwise the knowledge base becomes a museum of disasters.

A new engineer needs to see:

> "This is what a correct preflight looks like."

as well as:

> "This is what an incorrect one looks like."

Video is particularly good for **tacit knowledge**.

For example, an experienced engineer might say:

> "The motor sounds slightly wrong."

That's almost useless as text.

But if you have:

```text
normal_motor.wav
vs
bearing_problem_001.wav
```

and an experienced engineer explains:

> "Listen around 00:13. This harmonic wasn't present in the normal run."

you've converted tacit knowledge into something teachable.

### I'd actually capture 4 layers

Think of the company's knowledge as:

```text
                 COMPANY KNOWLEDGE
                        │
          ┌─────────────┼─────────────┐
          │             │             │
       MACHINE       HUMAN          CONTEXT
          │             │             │
      telemetry       video       environment
      logs            voice       configuration
      sensors         actions     photos
      firmware        decisions   test setup
          │             │             │
          └─────────────┼─────────────┘
                        │
                    TEST CASE
                        │
                  ENGINEERING
                   CONCLUSION
                        │
                   KNOWLEDGE
```

The **test case** is the atomic unit.

Not:

```text
random videos/
random photos/
random PDFs/
random Notion pages/
```

but:

```text
test case
  ├── machine evidence
  ├── human evidence
  ├── environmental evidence
  ├── conclusion
  └── follow-up
```

### Then put an AI layer on top

This is especially interesting for an AI-native company.

Once you have thousands of these:

```text
10,000 flights
50,000 hours of video
10 TB telemetry
thousands of incident reports
firmware history
hardware revisions
test procedures
```

you can build an internal engineering agent.

Engineer:

> "Have we ever seen this yaw oscillation before?"

Agent:

```text
Found 23 related flight tests.

Most similar:
  FT-2026-0412-008
  similarity: 0.91

Observed behavior:
  yaw oscillation during position-hold transition

Relevant configuration:
  firmware 2.7.x
  wind 6–8 m/s

Resolution:
  reduced transition gain by 12%

Evidence:
  00:04:17–00:04:31 in ground video
  telemetry channels yaw_rate / desired_yaw_rate

Related engineers:
  ...
```

That's when your "record everything" philosophy turns into a **compounding engineering asset**.

The key is **don't confuse storage with knowledge management**.

Recording 10,000 videos into an S3 bucket isn't knowledge.

The pipeline should be:

```text
TEST
 ↓
CAPTURE
 ↓
SYNC
 ↓
ANNOTATE
 ↓
DEBRIEF
 ↓
LINK TO HARDWARE/FIRMWARE/CONFIG
 ↓
STORE
 ↓
INDEX
 ↓
SEARCH
 ↓
AI RETRIEVAL
 ↓
NEW ENGINEER
 ↓
KNOWLEDGE COMPOUNDS
```

And there's another major benefit: **people leaving the company don't take the entire organization's memory with them.**

That is probably one of the highest-ROI things a hardware/robotics company can build early.

I can also sketch a concrete **"flight-test knowledge system" architecture**—camera + telemetry + storage + metadata schema + automatic video/telemetry indexing + RAG/agent layer—using mostly open-source components.
