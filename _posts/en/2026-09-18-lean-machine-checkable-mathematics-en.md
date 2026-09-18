---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Lean: Machine-Checkable Mathematics"
translated: false
type: note
---

Question: What is Lean math language?

Answer:

**Lean** is a formal programming language and theorem prover used to write **machine-checkable mathematics**. It lets humans express mathematical definitions, theorems, and proofs in a language that a computer can verify with a small trusted kernel.

Think of it as:

> Mathematics + Programming Language + Proof Checker

The core idea:

A normal math proof:

```
Theorem: If a + b = b + a, addition is commutative.
Proof: We know addition is commutative.
```

A Lean proof:

```lean
theorem add_comm_example (a b : Nat) : a + b = b + a := by
  exact Nat.add_comm a b
```

Lean checks every logical step.

---

## 1. Why was Lean created?

Traditional mathematics is written for humans:

```
Let x be a real number.
Clearly, x^2 >= 0.
Therefore...
```

Humans fill gaps using intuition.

Computers cannot. They need:

```
Definition
↓
Axioms
↓
Logical inference rules
↓
Proof object
```

Lean creates a **formal proof object** that can be verified.

This is useful for:

* proving mathematical theorems
* verifying software
* verifying hardware
* AI-generated reasoning evaluation

---

## 2. Lean is based on dependent type theory

The foundation is:

**Calculus of Inductive Constructions (CIC)**

The key idea:

> A proof is a program, and a theorem is a type.

Example:

```lean
theorem hello : 1 + 1 = 2 := by
  rfl
```

Here:

```
1 + 1 = 2
```

is a **type**.

The proof:

```
rfl
```

is a value inhabiting that type.

Similar to programming:

```python
def add(a,b):
    return a+b
```

In Lean:

```
theorem proof_of_statement : Statement := proof
```

---

## 3. Lean has a tiny trusted kernel

This is important.

Lean itself has many automation tools:

* tactics
* AI suggestions
* search
* simplifiers

But the final authority is the kernel.

Flow:

```
Human / AI
    |
    v
Generate proof
    |
    v
Lean kernel
    |
    v
Accept / Reject
```

The kernel is small enough to audit.

---

## 4. Example: proving arithmetic

Lean:

```lean
example : 2 + 3 = 5 := by
  norm_num
```

The tactic:

```
norm_num
```

generates a proof.

Kernel checks:

```
Is this proof valid?
YES
```

---

## 5. Lean vs normal programming

Python:

```python
x = 5
print(x + 1)
```

Question:

"Does this program run?"

Lean:

```lean
theorem square_nonnegative (x : Int) :
  x*x >= 0 := ...
```

Question:

"Is this mathematical statement proven?"

Different goal.

---

## 6. Why AI researchers care about Lean

Modern reasoning models use Lean because it gives **verifiable rewards**.

Normal LLM output:

```
Question:
Prove theorem X

LLM:
Here is a proof...
```

Problem:

How do we know it is correct?

With Lean:

```
LLM generates proof
        |
        v
Lean compiler
        |
        +---- valid → reward +1
        |
        +---- invalid → reward 0
```

This creates a reinforcement learning environment.

This is why Lean is important for:

* AlphaProof
* DeepMind mathematical reasoning research
* OpenAI theorem proving experiments
* RL for reasoning models

The reward is objective.

---

## 7. Lean ecosystem

Important projects:

* Lean 4 — current Lean version
* mathlib — huge community math library

mathlib contains formalized:

* algebra
* topology
* number theory
* analysis
* probability
* geometry

Example:

```lean
import Mathlib

example (x : ℝ) : x^2 ≥ 0 := by
  positivity
```

---

## 8. Relation to LLM reasoning

A normal chain-of-thought:

```
LLM:
Step 1...
Step 2...
Step 3...
(answer)
```

Cannot be trusted.

Lean-based reasoning:

```
LLM:
Generate Lean code

        ↓

Lean verifier

        ↓

Correct / Incorrect
```

So Lean becomes a **ground truth environment**.

The future direction:

```
LLM
 |
 | generates
 v
Lean proof
 |
 | verifies
 v
Mathematical truth
```

This is similar to how code execution gives LLMs a way to verify programming answers.

---

In one sentence:

**Lean is a programming language where mathematical statements become types and proofs become programs, allowing a computer to mechanically verify that the reasoning is correct.**
