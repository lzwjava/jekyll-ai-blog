---
audio: false
generated: true
image: false
lang: en
layout: post
title: B150M Power Connectors Overview
translated: false
type: note
---

Question: **What are the major power connectors on a motherboard like the MSI B150M PRO?**

Answer:

For a typical **B150M motherboard**, the main power connectors are:

```text
        PSU
         │
         ├── 24-pin ATX ──────────► Motherboard main power
         │
         └── 4/8-pin CPU EPS ─────► CPU power
```

### 1. 24-pin ATX — the main motherboard connector

Usually labeled:

```text
ATX_PWR1
JPWR1
ATX_PWR
```

It is the **large 24-pin connector** on the right edge of the board.

It supplies multiple rails:

* +12 V
* +5 V
* +3.3 V
* GND
* 5VSB
* PS_ON#
* PWR_OK

This is the connector you absolutely need for the motherboard to operate normally.

### 2. 4/8-pin CPU power — EPS12V

Usually near the CPU socket, labeled something like:

```text
CPU_PWR1
JPWR2
ATX12V
```

Typically:

```text
4-pin        or        8-pin
┌──────┐              ┌────────┐
│12V GND│              │12V GND │
│12V GND│              │12V GND │
└──────┘              └────────┘
```

This provides **12 V specifically for the CPU VRM**.

For your B150 + i5-6500 setup, you normally connect **both the 24-pin ATX and the CPU 4/8-pin connector**.

### 3. Front-panel connector is NOT a power-input connector

The `JFP1` connector you were looking for earlier is different:

```text
JFP1
 ├── Power Switch
 ├── Reset Switch
 ├── HDD LED
 └── Power LED
```

The **Power Switch pins only tell the motherboard to start**. They don't supply motherboard power.

So for bench testing:

```text
PSU
 │
 ├── 24-pin ATX ──► motherboard
 │
 └── CPU EPS ─────► CPU power

Then briefly short:
JFP1 PWR_SW pins
```

That simulates pressing the case's power button.

If you're debugging your **MSI B150M PRO**, I can also walk you through **every pin of the 24-pin ATX connector and what voltage you should measure with your multimeter/oscilloscope**.