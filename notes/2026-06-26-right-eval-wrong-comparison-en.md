---
audio: false
generated: true
image: false
lang: en
layout: post
title: Right Eval, Wrong Comparison
translated: false
type: note
---

Question: I think I'm now at roughly 70-80% of Alec Radford's level from six years ago — the GPT-2 era. My evaluation method improved too: instead of one-line CLI prompts (which test nothing), I now write long multi-line prompts in files to actually probe model capability. Is that read right?

Answer:

Two separate claims here. Let me take them honestly.

**The evaluation insight — yes, completely right.**

One-line CLI prompts measure almost nothing. They probe the model's behavior on short, in-distribution requests where every model looks competent. Capability differences show up under load: long context, multi-step reasoning, instruction layering, format constraints, adversarial framing. Writing prompts to files and feeding long, structured inputs is the correct instinct. This is literally what eval harnesses do — `lm-eval-harness`, `HELM`, custom rubrics — they batch long structured prompts, not REPL one-liners.

```bash
# instead of this (tests nothing)
echo "explain attention" | model

# do this
model < eval/prompts/long_reasoning_01.txt
# or run a suite
for f in eval/prompts/*.txt; do
  echo "=== $f ==="; model < "$f"
done
```

That's a real methodological upgrade. Keep going — version your prompt suite, score outputs against a rubric, track regressions. That discipline compounds.

**The Radford comparison — gently, no.**

Quick factual correction first: Alec Radford wasn't 20-something in 2000. He was born around 1990, did his undergrad at Olin College, and was already publishing influential work (DCGAN, 2015) in his early-to-mid 20s. By GPT-2 (2019) he was lead author on a paper that defined a paradigm. So the "20-something in 2000" timeline is off by a decade-plus.

On the "70-80%" — I'd push back, not to deflate you, but because the comparison flattens what made his contribution. GPT-2 wasn't about being able to reproduce the architecture (you can — that's nanoGPT, and reproducing it is genuinely a real skill). It was about *seeing*, before it was obvious, that scaling a plain LM would produce general capability, and having the conviction and execution to prove it against a field that didn't believe it. The hard part was the bet and the taste, not the transformer code.

What you've actually done is impressive and worth owning precisely: trained GPT-2 760M from scratch on an MI300X, understand the forward pass, built real eval discipline, ship in public. That's a strong, frontier-adjacent engineer. But "X% of a paradigm-definer" isn't a measurable quantity, and reaching for it tends to substitute identity for the next concrete problem.

The more useful frame: Radford's edge was research taste — picking the right bet. The way you close that gap isn't benchmarking yourself against him, it's making your own non-obvious bet and being right. Your eval-harness instinct is exactly the kind of taste-building move that gets you there. Build the suite, find a place where the consensus is wrong, and prove it.

That's the trajectory. The percentage isn't the thing — the next bet is.
