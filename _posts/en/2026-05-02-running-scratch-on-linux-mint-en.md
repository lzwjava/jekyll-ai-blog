---
audio: false
generated: true
image: false
lang: en
layout: post
title: Running Scratch Programs on Linux Mint
translated: false
type: note
---

Question: How do I use Scratch on Linux Mint like in the picture, and why does clicking/dragging blocks not make it run?

Answer:

What you’re seeing in the image is the Scratch Desktop interface running on Linux Mint. It works the same as on Windows/macOS — Linux support is fine.

The key idea is: **dragging blocks does nothing until you “run” the program.**

---

## 1. How Scratch actually runs

In Scratch (programming language), blocks don’t execute immediately. You must start a script using an **event block**.

### The most common way

Look for this block:

* **“when green flag clicked”** (Events category)

Then:

1. Drag **“when green flag clicked”** into the workspace
2. Attach your movement blocks under it
3. Click the **green flag above the stage (top-right area)**

👉 That green flag is the “Run” button.

---

## 2. Why your current blocks don’t move anything

From your screenshot, it looks like you only have blocks like:

* `move 10 steps`
* `turn 15 degrees`

But they are **floating separately**, not attached to a trigger.

So Scratch ignores them.

---

## 3. Minimal working example (try this)

Build this:

```
when green flag clicked
repeat 10
    move 10 steps
    turn 15 degrees
```

Then click the green flag.

You should immediately see the sprite move.

---

## 4. Common mistakes (very important)

### ❌ No “event block”

Nothing runs without:

* green flag clicked
* key pressed
* sprite clicked

### ❌ Blocks not connected

Blocks must snap together like LEGO.

### ❌ Sprite not selected

Make sure you’re editing the correct sprite (bottom-right panel).

---

## 5. Keyboard testing (optional)

Try this too:

```
when space key pressed
move 10 steps
```

Then press **Spacebar** on keyboard.

---

## 6. Linux Mint note

Scratch Desktop on Linux Mint behaves normally. If UI opens but feels unresponsive:

* Make sure you are using **Scratch Desktop (not browser offline cache)**
* Check GPU acceleration if animations lag
* Ensure window is fully focused when clicking green flag

---

## 7. Quick mental model

Think of Scratch like this:

> Blocks = instructions
> Event block = “start signal”
> Green flag = “power button”

Without the power button, nothing executes.

---

If you want, I can help you build a first real project (like a moving game character or simple game loop) step by step.
