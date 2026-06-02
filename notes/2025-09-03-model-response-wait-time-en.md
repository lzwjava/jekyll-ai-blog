---
audio: false
generated: true
image: false
lang: en
layout: post
title: Calculating Model Response Wait Time
translated: false
type: note
---

We can work it out step by step.

From the record:

* **tokens\_completion** = 9532
* **throughput** isn’t shown here, but you asked “tokens ÷ tokens per second.”

The request has:

* `generation_time = 203477 ms` → 203.477 seconds
* `tokens_completion = 9532`

Now compute the actual throughput:

$$
\text{tokens per second} = \frac{9532}{203.477} \approx 46.8
$$

So the user needed to wait about **203 seconds (\~3 minutes 23 seconds)** for the response.

If you already know the model’s throughput (tokens/second), then the wait time is simply:

$$
\text{wait time} = \frac{\text{tokens\_completion}}{\text{tokens per second}}
$$

In this case, the log already gives both sides (time and tokens), so the calculation matches.

👉 Short answer: The user waited about **203 seconds (\~3 minutes 23 seconds)** for the 9532 tokens, at \~47 tokens/second.

Do you want me to also show you a **general formula** you can reuse for other logs (using latency, throughput, and token counts)?
