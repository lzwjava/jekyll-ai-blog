---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Introduction to the Prisoner’s Dilemma
translated: false
type: note
---

Question: What is the Prisoner's Dilemma?

Answer:

The **Prisoner's Dilemma** is a fundamental concept in game theory that illustrates a situation where two rational individuals, acting in their own self-interest, may not cooperate, even though cooperation would lead to a better collective outcome.

### Classic Scenario

Two suspects (Prisoner A and Prisoner B) are arrested and interrogated separately for a crime. The prosecutors offer each a deal:

- If **both prisoners stay silent** (cooperate with each other), they each get a light sentence: **1 year in prison**.
- If **one confesses** (defects) while the other stays silent, the confessor goes **free** (0 years), and the silent one gets a heavy sentence: **3 years**.
- If **both confess** (defect), they each get a moderate sentence: **2 years**.

This setup creates the following payoff matrix (lower numbers are better, representing years in prison):

|                  | B Stays Silent (Cooperate) | B Confesses (Defect) |
|------------------|----------------------------|----------------------|
| **A Stays Silent (Cooperate)** | A: 1 year<br>B: 1 year    | A: 3 years<br>B: 0 years |
| **A Confesses (Defect)**       | A: 0 years<br>B: 3 years  | A: 2 years<br>B: 2 years |

### Key Insight

- For each prisoner individually, **confessing (defecting) is the dominant strategy**: No matter what the other does, confessing yields a better personal outcome (0 or 2 years vs. 1 or 3 years).
- However, if both follow this rational self-interest, they both confess and get **2 years each**—a worse outcome than if both had cooperated (1 year each).
- Thus, mutual cooperation is collectively better, but individual rationality leads to mutual defection.

### Broader Implications

The Prisoner's Dilemma models many real-world conflicts, such as:

- Arms races between nations
- Environmental issues (e.g., overfishing or pollution)
- Business pricing wars
- Social dilemmas like vaccination or tax compliance

It explains why cooperation can be difficult to achieve even when it benefits everyone, and it has influenced fields like economics, political science, evolutionary biology, and ethics.

In repeated versions of the game (iterated Prisoner's Dilemma), strategies like "Tit for Tat" (cooperate first, then mirror the opponent's previous move) can promote sustained cooperation.
