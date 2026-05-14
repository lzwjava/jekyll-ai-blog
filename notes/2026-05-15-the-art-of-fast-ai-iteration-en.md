---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Art of Fast AI Iteration
translated: false
type: note
---

Here's an English version of the satire, based on Wang Yin's original essay and adapted to mock AI engineers who obsess over training medium-sized models with slow iteration cycles.

---

**Why Some AI Engineers Can't *Really* Train Models**  
— In the spirit of Wang Yin

Talk to certain AI engineers about training, and you'll notice a strange pattern:  
They keep talking about "200M parameter models" that take "days to see results."  
You suggest starting with something much smaller—say, 20M or 5M parameters—where you can iterate every hour or two. They say: "That's too small. The final model needs to be big."

They have only two modes:

1. **Practice = running official examples / copying someone else's full training script.**  
   Data, hyperparameters, model architecture—all "textbook form." One run takes two or three days.  
   They don't dare change anything in between, because changing a few lines of code means waiting days to see the effect.  
   This is like table tennis players who only ever rally down the same line, at the same speed, with the same spin. **They've never practiced real, chaotic, corner-hitting table tennis.**

2. **Match = full training + full evaluation.**  
   They start keeping score (accuracy, loss curves) immediately. When they lose, they get discouraged.  
   Because each iteration is so slow, they never take risks or try wild new ideas.  
   They make the same mistake twice—and by the time the results come back three days later, they've forgotten what they even tried.

You suggest: **First, iterate fast on a tiny model—one to two hours per experiment. Get really good at *inference* first, because inference and training share the same core GPT code. If you can master inference, training isn't far behind.**

They freeze. "I've never trained like that…"

Then you realize: they've never played "no scoring, but real" table tennis.  
What they call "experiments" are either rallying (running canned scripts) or formal matches (waiting days for full training).  

**Real research is like that kind of table tennis: every point is a real fight. You don't keep score, but you go all out. You try shots into the corners. You fail fast. You learn.**

And yet they complain: "Large model training is too slow. Iteration takes forever. At this rate, we'll never finish."

— But they refuse to first understand inference, gradient flow, and model behavior on small, fast setups.

**That's why they can never *really* train models.**

---

If you want an even shorter, punchier version (for Twitter / LinkedIn / team chat), let me know and I'll condense it further.