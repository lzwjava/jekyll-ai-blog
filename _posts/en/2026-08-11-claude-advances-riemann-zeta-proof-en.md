---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Advances Riemann Zeta Proof
translated: false
type: note
---

Question: Intro to Anthropic's Riemann zeta research.

Answer:

Anthropic used an advanced Claude research model to attack one of the most famous unsolved problems in mathematics: the **Riemann Hypothesis (RH)**. It did **not solve RH**, but during the attempt it reportedly found a significant improvement on a related mathematical problem: increasing the known lower bound for how many zeros of the Riemann zeta function lie on the critical line. ([Reddit][1])

The core idea is a good example of how AI may contribute to science:

> AI does not necessarily replace mathematicians by instantly proving legendary theorems; instead, it can search huge mathematical spaces, combine previous results, discover promising proof paths, and formalize arguments.

## 1. What is the Riemann zeta function?

The function is:

[
\zeta(s)=\sum_{n=1}^{\infty}\frac{1}{n^s}
]

where:

[
s=\sigma+it
]

is a complex number.

Example:

```
s = 0.5 + 14.1347i
```

The function maps a point in the complex plane to another complex value.

The famous connection:

[
\zeta(s)=\prod_p \frac{1}{1-p^{-s}}
]

where the product is over all prime numbers.

This is why primes are involved.

The zeta function is like a "frequency analyzer" for the distribution of primes.

---

## 2. What is the Riemann Hypothesis?

The zeta function has zeros:

[
\zeta(s)=0
]

Some are trivial:

[
s=-2,-4,-6,...
]

The interesting ones are inside:

[
0 < Re(s) < 1
]

This region is called the **critical strip**.

Riemann's hypothesis says:

[
\boxed{Re(s)=\frac12}
]

meaning:

all non-trivial zeros should lie exactly on the vertical line:

```
imaginary axis

     |
     |
     *
     |
     *
-----+---------------- real
    0.5
     |
     *
     |
```

Almost all computed zeros obey this, but nobody has proven it for infinity. ([arXiv][2])

---

## 3. Why is it important?

Because zeros control the "error term" in prime distribution.

The Prime Number Theorem says:

[
\pi(x)\approx \frac{x}{\log x}
]

meaning:

number of primes below x ≈ x/log(x)

But how accurate is this?

The location of zeta zeros determines the error.

If RH is true:

[
\pi(x)=Li(x)+O(\sqrt{x}\log x)
]

The uncertainty becomes much smaller.

Applications:

* number theory
* cryptography theory
* random matrix theory
* mathematical physics

---

## 4. What did Claude actually do?

Important distinction:

### It did NOT:

```
Claude -> solve Riemann Hypothesis
```

No.

### It did:

```
Claude
 |
 |-- read thousands of mathematical ideas
 |
 |-- generate proof attempts
 |
 |-- test approaches
 |
 |-- combine existing bounds
 |
 |-- discover a better argument
 |
 v

improved lower bound
```

The related problem:

Instead of proving:

[
100%
]

of zeros are on the critical line,

mathematicians ask:

[
\text{What percentage can we prove?}
]

Before this work:

[
41.6%
]

After:

[
67.2%
]

meaning:

> At least 67.2% of the non-trivial zeros are proven to lie on the critical line.

It is not RH, but it is meaningful progress. ([Reddit][1])

---

## 5. Why is this interesting for AI research?

This is close to the "AI scientist" vision.

Traditional workflow:

```
Human mathematician

idea
 |
paper
 |
proof
 |
verification
```

AI-assisted workflow:

```
LLM agent

read literature
      |
generate hypotheses
      |
run symbolic experiments
      |
search proof space
      |
formalize in Lean
      |
human verification
```

The bottleneck changes.

Before:

> "Can humans think of enough ideas?"

After:

> "Can we build systems that explore millions of mathematical ideas safely?"

---

## 6. Connection with LLM architecture

This problem is actually very aligned with modern agent systems.

A frontier math agent needs:

### Long context

Read:

* hundreds of papers
* old proofs
* definitions

### Tool usage

Examples:

```
Claude
 |
 +-- arxiv search
 |
 +-- Mathematica/Sage
 |
 +-- Lean theorem prover
 |
 +-- Python experiments
```

### Self-reflection loop

Something like:

```python
while not proven:
    idea = model.generate()
    
    result = verify(idea)

    if result.failed:
        critique = analyze_failure(result)
        model.update(critique)
```

Very similar to AlphaZero-style search.

---

## 7. The deeper AI implication

The interesting part is not "AI solved Riemann".

The interesting part:

For 100+ years, progress depended on a few exceptional mathematicians.

AI potentially changes this:

```
Before:

1 mathematician
+
10 years
=
1 breakthrough


Future:

1000 AI agents
+
1 month
=
search millions of approaches
```

The challenge becomes:

* verification
* creativity
* mathematical taste
* avoiding hallucinated proofs

This is why formal systems like Lean matter.

A future math agent probably looks like:

```
LLM
 +
retrieval
 +
computer algebra
 +
proof assistant
 +
search algorithm
```

rather than a single chatbot.

References:

* Anthropic Research overview ([Anthropic][3])
* Riemann Hypothesis numerical verification background ([arXiv][2])
* Riemann zeta function and prime distribution overview ([Nature][4])
* Discussion of Anthropic Claude Riemann attempt and 67.2% bound ([Reddit][1])

[1]: https://www.reddit.com/r/accelerate/comments/1vkv0l9/absolutely_insane_this_might_be_the_clearest/?utm_source=chatgpt.com "\"Absolutely insane. This might be the clearest glimpse yet of how AI will transform scientific discovery. Anthropic asked an unreleased version of Claude to take a real stab at the Riemann Hypothesis, one of the most famous unsolved problems in mathematics. It failed. But while failing, Claude...\""
[2]: https://arxiv.org/abs/2004.09765?utm_source=chatgpt.com "The Riemann hypothesis is true up to $3\cdot 10^{12}$"
[3]: https://www.anthropic.com/research?mon=51&utm_source=chatgpt.com "Research \ Anthropic"
[4]: https://www.nature.com/nature-index/topics/l4/analytic-number-theory-and-zeta-function-studies?utm_source=chatgpt.com "Analytic Number Theory and Zeta Function Studies | Algebra and Number Theory | Pure Mathematics | Physical sciences | Topics | Nature Index"