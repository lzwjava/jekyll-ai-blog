---
audio: false
generated: true
image: false
lang: en
layout: post
title: LED Polarity on Motherboards
translated: false
type: note
---

Question: Why do motherboards have separate Power LED+ and Power LED− pins instead of just one?

Answer: Because LEDs are **polarized components** — they only allow current to flow in one direction. This is fundamental electronics:

- **Power LED+** is the **anode** (positive terminal) — current enters here
- **Power LED−** is the **cathode** (negative terminal) — current exits here

If you connect the LED backwards (reversed polarity), it simply **won't light up** (and in some cases can be damaged). So the motherboard exposes both pins explicitly to let you orient the connector correctly.

**Why not just one pin?**
A single pin can't complete a circuit on its own. Every circuit needs both a source (+) and a return path (−/ground). The two pins together form the complete loop:

```
Motherboard 3.3V → LED+ → [LED lights up] → LED− → Ground
```

Some motherboards do simplify this with a **single 3-pin or combined header**, but they still internally have both + and − connections — they're just physically consolidated.

**Practical tip:** If your front-panel power LED doesn't light up, try **flipping the connector 180°** — polarity is the most common cause.

References:

- [How LEDs Work – Polarity Explained](https://learn.sparkfun.com/tutorials/polarity/diode-and-led-polarity)
- [Motherboard Front Panel Header Guide](https://www.tomshardware.com/reviews/motherboard-front-panel-connectors,2312.html)
