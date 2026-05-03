---
audio: false
generated: true
image: false
lang: en
layout: post
title: Planning Models in Autonomous Driving
translated: false
type: note
---

Question: What is a “planning model” (规划模型) in the autonomous driving industry?

Answer:

In autonomous driving, a **planning model (规划模型)** is the part of the system that decides **“what the car should do next”** given the current situation.

A typical autonomous driving system is divided into three main modules:

1. **Perception (感知)** → understand the environment (cars, pedestrians, lanes)
2. **Prediction (预测)** → predict what other agents will do
3. **Planning (规划)** → decide the ego vehicle’s behavior and trajectory

The **planning model** sits at the core of decision-making.

---

## 1. What exactly does a planning model do?

It takes inputs like:

* Detected objects (cars, pedestrians)
* Predicted trajectories of others
* Map information (lanes, traffic lights)

And outputs:

* A **driving decision** (e.g., stop, follow, overtake)
* A **trajectory** (a sequence of future positions)

---

## 2. Two levels of planning

### (1) Behavior planning (行为规划)

High-level decisions:

* Should I stop at this light?
* Should I change lanes?
* Should I yield to pedestrians?

This is often rule-based or learned (ML/RL).

---

### (2) Motion planning (轨迹规划)

Low-level trajectory generation:

* Generate a smooth, safe path
* Respect constraints (speed, curvature, collision avoidance)

This is usually optimization-based.

---

## 3. Common technical approaches

### Rule-based planning

* If-else logic, state machines
* Example: “if red light → stop”

Pros: interpretable
Cons: brittle, hard to scale

---

### Optimization-based planning

Formulated as a mathematical problem:

* Minimize:

  * deviation from lane
  * jerk (smoothness)
  * collision risk

* Subject to constraints:

  * vehicle dynamics
  * safety distances

Typical methods:

* MPC (Model Predictive Control)
* trajectory optimization

---

### Learning-based planning (ML / LLM-style trends)

* Use neural networks to directly output trajectories or decisions
* End-to-end models (e.g., imitation learning)

Examples:

* Predict future trajectory from camera input
* Reinforcement learning for driving policy

---

## 4. A simple conceptual pipeline

```
Environment → Perception → Prediction → Planning → Control
                                          ↓
                                  Planned trajectory
```

The planning model is the **“brain” that turns understanding into action**.

---

## 5. A concrete example

Scenario: You approach a pedestrian crossing.

* Perception: detects a pedestrian
* Prediction: estimates they may cross
* Planning model:

  * decides: “slow down and stop”
  * generates a smooth braking trajectory

---

## 6. Why planning is hard

Because it must balance:

* Safety (no collision)
* Comfort (smooth driving)
* Efficiency (not too slow)
* Legality (traffic rules)
* Interaction (with humans!)

This makes it a **multi-objective, real-time decision problem**.

---

## 7. In industry job terms

If someone says:

> “从事规划模型研发工作”

It usually means they work on:

* trajectory generation algorithms
* decision-making logic
* ML-based planning models
* simulation & evaluation of driving policies

---

## Key intuition

You can think of it like:

* Perception = eyes
* Prediction = intuition about others
* **Planning = decision + intention**

---

If you want, I can break down a real planning algorithm (e.g., MPC or end-to-end planning) step by step like an exam-style explanation.