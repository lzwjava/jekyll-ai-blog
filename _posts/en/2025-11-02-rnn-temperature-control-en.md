---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Controlling RNN Text Generation Temperature
translated: false
type: note
---

### Understanding Temperature in RNN Sampling

In recurrent neural networks (RNNs) for text generation—like those Andrej Karpathy explores in his famous blog post on character-level language models—temperature is a hyperparameter that tweaks how "random" or "predictable" the generated text feels. It's applied during the sampling step, where the RNN predicts the next character (or token) based on the previous ones. Without temperature control, generation can be too rigid (always picking the most likely next character, leading to boring loops) or too wild (pure randomness). Temperature strikes a balance by softening the model's probability distribution over possible next characters.

#### Quick Math Behind It

The RNN outputs *logits* (raw, unnormalized scores) for each possible next character. These get turned into probabilities using the softmax function:

\\[
p_i = \frac{\exp(\text{logit}_i / T)}{\sum_j \exp(\text{logit}_j / T)}
\\]

- \\(T\\) is the temperature (typically between 0.1 and 2.0).
- When \\(T = 1\\), it's standard softmax: probabilities reflect the model's "natural" confidence.
- You then *sample* the next character from this distribution (e.g., via multinomial sampling) instead of always picking the highest-probability one (greedy decoding).

This sampling happens iteratively: feed the chosen character back as input, predict the next, and repeat to generate a sequence.

#### Low Temperature: Repetitive but Safe

- **Effect**: \\(T < 1\\) (e.g., 0.5 or near 0) *sharpens* the distribution. High-confidence predictions get even higher probabilities, while low ones get squashed toward zero.
- **Output**: The text stays "safe" and coherent but quickly becomes repetitive. The model sticks to the most probable paths, like getting trapped in a loop.
- **Example from Karpathy's post** (generating Paul Graham-style essays): At very low temperature, it spits out something like:
  > “is that they were all the same thing that was a startup is that they were all the same thing that was a startup is that they were all the same thing that was a startup is that they were all the same”

  It's confident and grammatically sound but lacks creativity—think infinite echoes of the training data.

#### High Temperature: Creative but Erratic

- **Effect**: \\(T > 1\\) (e.g., 1.5 or 2.0) *flattens* the distribution. Probabilities become more uniform, giving underdogs (less likely characters) a better shot.
- **Output**: More diverse and inventive text, but it veers into nonsense, spelling errors, or wild tangents. The model explores rare paths, which can spark originality but at the cost of coherence.
- **Example from Karpathy**: Higher temps yield varied essays with fresh phrasing, but "at cost of more mistakes (e.g. spelling mistakes, etc.)." It's like the RNN is brainstorming freely—fun for poetry or sci-fi, risky for factual writing.

#### Why It Matters in RNNs

RNNs (or LSTMs in Karpathy's setup) are autoregressive: each prediction builds on the last, so small biases in sampling compound over long sequences. Temperature lets you tune exploration vs. exploitation:

- Use low \\(T\\) for reliable, on-brand text (e.g., product descriptions).
- Crank it up for brainstorming or artistic generation (e.g., surreal stories).
- Experiment in code: Karpathy's vanilla RNN repo includes a temperature slider—try it on Shakespeare samples to see the shift from bland sonnets to chaotic verse.

In essence, temperature isn't "learning" anything new; it's just dialing the RNN's creativity knob during inference. Low keeps it chill and predictable; high unleashes the chaos.

[The Unreasonable Effectiveness of Recurrent Neural Networks](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)
