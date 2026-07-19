---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Vertical AI Application Moat
translated: false
type: note
---

Your reply is actually pointing at a pretty important distinction in the AI application stack:

* **Domain model ≠ domain application**
* **Vertical intelligence layer ≠ vertical foundation model**

For health/fitness, building a "health LLM" or "medical foundation model" from scratch is usually not the best startup opportunity unless you have massive data, clinical partnerships, and capital. The base models are improving so fast that many vertical models become a thin layer.

But **health AI agents/apps** are very interesting because the hard part is not only language understanding. It is:

```
User data
  ↓
Wearables / Apple Health / lab reports / food logs
  ↓
Personal health state model
  ↓
Reasoning + recommendation agent
  ↓
Daily actions + feedback loop
  ↓
Better personalization
```

The moat is the **closed loop**, not the model.

For example:

```
AI Meal Agent
    photo of food
        ↓
    vision model estimates ingredients/calories
        ↓
    user preference + goals + history
        ↓
    nutrition advice
        ↓
    next meal recommendation

Fitness Agent
    Apple Watch data
        ↓
    sleep + HRV + exercise load
        ↓
    training plan adjustment
        ↓
    user feedback
        ↓
    adaptation
```

The interesting engineering problems are:

1. **Data integration**

   * Apple HealthKit
   * Garmin/Fitbit/Oura
   * glucose monitors
   * lab reports

2. **Personal memory**

   * "You usually sleep badly after late dinner"
   * "Your running pace improved after strength training"

3. **Agent behavior**

   * not waiting for questions
   * proactively nudging at the right moment

4. **Evaluation**

   * did the recommendation actually improve health outcomes?

This is very different from "train a medical GPT".

A good analogy:

* 1990s: building a compiler was hard; building apps on top of compilers created huge companies.
* 2020s: foundation models are becoming the "compiler layer".
* The opportunity is often the intelligent workflow/application layer.

The same pattern applies to many fields:

```
Foundation model
        ↓
Agent framework
        ↓
Vertical workflow
        ↓
Personalized data loop
        ↓
User value
```

So your observation is close: **vertical AI apps are attractive; vertical foundation models are much harder to justify unless they own unique data.**

A company like PureOne is basically betting that the future "health assistant" is not a chatbot you ask once, but an agent that continuously knows your state and helps you make thousands of small decisions. That direction makes sense.
