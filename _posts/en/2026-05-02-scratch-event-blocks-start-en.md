---
audio: false
generated: true
image: false
lang: en
layout: post
title: Scratch Requires Event Blocks to Start
translated: false
type: note
---

Question: Why does clicking the run button in Scratch not make anything move, is it missing dependencies, should I try macOS instead, and am I remembering correctly that I need a yellow event block at the top?

Answer:

You’re basically on the right track — this is not a Linux problem and not a missing dependency issue.

## 1. It’s not Linux or installation-related

Scratch on Linux Mint works normally. The system doesn’t affect whether blocks run.

So:

* ❌ not a dependency problem
* ❌ not “macOS will fix it”
* ❌ not a broken runtime issue

If the interface opens and you see blocks, the engine is already fine.

---

## 2. The real reason nothing moves

In Scratch (programming language), blocks **do nothing unless triggered by an event block**.

So if you only placed:

* move 10 steps
* turn 15 degrees

👉 they are just “inactive instructions sitting there”

Nothing tells them to start.

---

## 3. Yes — your memory is correct

You need a **yellow event block** (Control/Events logic in Scratch UI):

Most common one:

* **“when green flag clicked”**

This must be:

* at the TOP of a stack
* connected like LEGO pieces

Example:

* when green flag clicked
  → move 10 steps
  → turn 15 degrees

Then click the green flag above the stage.

---

## 4. Why the run button feels like “nothing happens”

The green flag is not a generic “run all blocks” button.

It only:

* triggers scripts that start with event blocks

So without that starting block:

> pressing run = nothing is listening

---

## 5. macOS vs Linux idea

No need to switch systems here.

Scratch is:

* browser-based or Electron-based desktop app
* cross-platform identical behavior

So debugging on macOS won’t reveal anything new.

---

## 6. Your intuition is actually right

You already recalled the key concept:

> “there must be an event block at the top”

That is exactly the core mental model of Scratch:

* event → start
* stack → execution flow

---

## 7. Small practical tip

If you want to quickly verify everything works:

1. drag **“when green flag clicked”**
2. attach **move 10 steps**
3. click green flag

If sprite moves → system is 100% fine

---

## 8. About your thinking process

Your reasoning is actually close to how debugging works in real systems:

* suspect runtime issue
* suspect environment difference
* then realize it’s logic/trigger issue

That shift from “system problem” → “program flow problem” is the key skill here.

---

If you want, I can show you how to turn this into a tiny “game loop” (like auto-moving sprite + bounce + keyboard control).
