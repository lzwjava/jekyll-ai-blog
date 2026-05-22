---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hardware Always Blocks Explained
translated: false
type: note
---

**Question:** What does `always` mean in Verilog? Is it like a for loop? What does `posedge` mean?

**Answer:**

Good questions — these are the core mental model shifts.

---

## `always` — NOT a for loop

A for loop runs once and exits. `always` **never exits. Ever.** It's more like:

```python
# Software analogy
while True:
    if condition_changed:
        recompute_output()
```

But even that's wrong because it implies sequential checking. In hardware, `always` means:

> **"This circuit is physically wired up and reacts instantly whenever its inputs change."**

There is no loop. There is no iteration. The hardware just... exists. And responds.

```verilog
always @(*) begin
    out = a & b;   // whenever a or b changes, out updates INSTANTLY
end
```

This synthesizes to a single AND gate. No loop. No clock. Just a wire and a gate sitting there, always active.

---

## Two Flavors of `always`

### Flavor 1: `always @(*)` — Combinational

```verilog
always @(*) begin
    out = a & b;
end
```

```
a ──┐
    ├─[AND]── out
b ──┘
```

`@(*)` means "trigger when ANY input changes." This is purely physical — electricity flows, output updates in nanoseconds. No clock involved.

### Flavor 2: `always @(posedge clk)` — Sequential

```verilog
always @(posedge clk) begin
    q <= d;
end
```

This only updates on a clock edge. This is a **flip-flop** — the fundamental memory element in all digital chips.

---

## `posedge` — Positive Edge

A clock signal looks like this:

```
clk:  0──┐  ┌──┐  ┌──┐  ┌──
         │  │  │  │  │  │
         └──┘  └──┘  └──┘

         ↑     ↑     ↑
       posedge posedge posedge   ← fires here
```

`posedge clk` = the **exact moment the clock goes from 0 → 1.**

`negedge clk` = the exact moment clock goes from 1 → 0.

So:

```verilog
always @(posedge clk) begin
    count <= count + 1;
end
```

Means: **"Exactly once per clock tick, increment count."** Between ticks — nothing happens. The value is frozen.

---

## Side by Side

```verilog
// COMBINATIONAL — like a pure function, no memory
always @(*) begin
    sum = a + b;    // updates instantly when a or b changes
end

// SEQUENTIAL — like a variable that only updates on tick
always @(posedge clk) begin
    sum <= a + b;   // updates only on clock rising edge
end
```

The difference in hardware:

```
Combinational:          Sequential:
                        
a ──┐                   a ──┐
    ├─[ADDER]── sum         ├─[ADDER]──[D flip-flop]── sum
b ──┘                   b ──┘              ↑
                                         clk
```

The flip-flop is the box that "catches" the value on each clock edge and holds it until the next edge.

---

## The Clock is Everything

In a real chip running at 3 GHz:

```
posedge fires 3,000,000,000 times per second
         ↑
         Every time this fires, ALL sequential always blocks
         in the entire chip update simultaneously
```

MI300X runs its compute units at ~2.1 GHz. Every posedge, thousands of `always @(posedge clk)` blocks fire in parallel across the chip. That's the machine.

---

## Concrete Analogy for You

Think of it like an event loop but physical:

```
always @(*)        →  reactive: like Vue/React re-rendering when state changes
always @(posedge)  →  clocked:  like setInterval(fn, 0.33ns) — fires 3B times/sec
```

Except there's no JS engine. No scheduler. It's just transistors switching.