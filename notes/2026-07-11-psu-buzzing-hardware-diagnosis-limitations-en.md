---
audio: false
generated: true
image: false
lang: en
layout: post
title: "PSU Buzzing: Hardware Diagnosis Limitations"
translated: false
type: note
---

Question: My PSU is buzzing/whining. I'm debating whether to take the workstation to a repair shop, call someone to come fix it, or keep debugging it myself. Isolating the PSU from the motherboard entirely is step one. I'm frustrated — AI is supposedly so capable, yet I'm hitting a wall here. Is it because hardware requires physical hands-on iteration (unlike software, where I can just read code and let AI run high-frequency experiments), and because AI right now is "just a better search engine" — a chatbot, not an agent that can physically act?

Answer:

Your diagnosis is correct, but let's be precise about *why*, because the precision matters for how you should actually use AI here.

**The core asymmetry: action loop closure**

In software, the loop is:

```
you: state hypothesis → AI: writes code → you: run it → observe stdout/exit code → feed back to AI → repeat
```

Every step in that loop is text-in, text-out. AI can literally execute the middle steps (via Claude Code, a REPL, whatever) with zero marginal cost per iteration. That's why you can do 50 experiments in an hour.

In hardware, the loop is:

```
you: state hypothesis → AI: suggests test → YOU physically do it (multimeter, disconnect, reseat) → YOU observe (smell, sound, voltage reading) → YOU report back in words → repeat
```

The AI is stuck outside the loop's actuation and sensing steps. It has no hands, no eyes, no ears, no nose. Every iteration costs you real time and now, potentially, real money (fried components). That's not a "chatbot vs agent" framing exactly — it's a **sensor/actuator gap**, not an intelligence gap. Even a perfect reasoning engine is bottlenecked by the fact that *you* are its only I/O device for the physical world, and you're slow, imprecise (compared to instrumentation), and each trial has nonzero destructive risk.

This is actually the same reason robotics has lagged pure LLM progress — Karpathy has talked about this: text/code is a domain where you can generate near-infinite verified rollouts cheaply (compiler, tests, execution = ground truth), while physical action requires either real robots (slow, expensive, risky) or simulation (sim-to-real gap). Your PSU debugging is a one-person, no-simulator, no-parallelization version of that same problem.

**Practically, for your PSU situation:**

You're right that most single actions won't cascade into destroying the whole rig. Isolating PSU from motherboard is the correct first move — standard PSU self-test:

```
# PSU paperclip test (isolate PSU, no motherboard involved)
# ATX 24-pin connector, looking at the connector face:
# Short the green wire (PS_ON, pin 15 or 16 depending on generation) to any black wire (GND)
# with the PSU unplugged, insert paperclip, then plug in and flip PSU switch
```

If it powers on and the fan spins *without buzzing* → PSU itself might be fine and the noise is coil whine triggered by load from the motherboard/GPU, not a PSU fault. If it still buzzes/whines standalone → that's very likely a failing capacitor or the switching regulator under electrical stress, and that's cheap to replace (PSU unit, ~200-300 CNY as you said) but NOT something to keep testing repeatedly — repeated power-on/off cycles on a failing PSU risk a voltage spike that fries your GPU or motherboard, which is the actual expensive failure mode.

Given your risk tolerance and that this is a 15k device: do the paperclip test once (5 minutes, zero motherboard risk), and based on that binary result, either swap the PSU yourself (it's the easiest hardware component to replace — no soldering, just screws and connectors) or if it's not the PSU, that's when you stop DIY-ing and call the technician, because now you're debugging an unknown fault on a motherboard/GPU you can't afford to iterate-and-fry.

**Where AI actually still helps here despite the gap:**

- It can narrow the *hypothesis space* fast (coil whine vs capacitor failure vs fan bearing — from your description of the sound) so your limited physical trials are higher-value
- It's read every PSU teardown/failure post-mortem ever written, so it's a better Bayesian prior generator than random forum searching
- It cannot substitute for the sensor data only your hands/ears/multimeter provide

So: yes — AI is a superb prior/hypothesis engine, bottlenecked to "smarter search + reasoning" the moment the loop requires physical actuation, until robotics + multimodal sensing closes that gap (which is exactly the kind of embodied-agent problem still unsolved industry-wide, not a Claude/GPT limitation specifically).
