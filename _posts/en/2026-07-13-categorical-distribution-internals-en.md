---
audio: false
generated: true
image: false
lang: en
layout: post
title: Categorical Distribution Internals
translated: false
type: note
---

Question: What does `torch.distributions.Categorical(logits=logits)` do internally?

Answer: It builds a categorical (discrete) distribution over `K` classes from unnormalized log-probabilities, and gives you `.sample()`, `.log_prob()`, `.entropy()`, `.probs` without you manually doing the softmax + sampling math.

**What it does under the hood:**

```python
import torch

logits = torch.tensor([2.0, 1.0, 0.1])  # unnormalized, any real numbers
dist = torch.distributions.Categorical(logits=logits)

# 1. probs are computed lazily via softmax, numerically stable
#    dist.probs = softmax(logits, dim=-1)
print(dist.probs)  # tensor([0.6590, 0.2424, 0.0986])

# 2. sampling uses Gumbel-max trick (not literal cumsum+search, though equivalent)
action = dist.sample()  # tensor(0), index into the K classes

# 3. log_prob is just log_softmax indexed at the sampled class
#    avoids computing softmax then log separately (log-sum-exp stability)
logp = dist.log_prob(action)  # = log_softmax(logits)[action]

# 4. entropy = -sum(p * log p), computed from log_softmax directly
ent = dist.entropy()
```

Source (simplified from `torch/distributions/categorical.py`):

```python
class Categorical(Distribution):
    def __init__(self, probs=None, logits=None):
        if logits is not None:
            self.logits = logits - logits.logsumexp(dim=-1, keepdim=True)  # normalize to log-probs
            self._param = self.logits
        # probs derived on demand: self.probs = self.logits.exp()

    def sample(self, sample_shape=torch.Size()):
        probs_2d = self.probs.reshape(-1, self._num_events)
        samples_2d = torch.multinomial(probs_2d, sample_shape.numel(), True).T
        return samples_2d.reshape(...)

    def log_prob(self, value):
        value = value.long().unsqueeze(-1)
        value, log_pmf = torch.broadcast_tensors(value, self.logits)
        value = value[..., :1]
        return log_pmf.gather(-1, value).squeeze(-1)
```

**Why `logits=` instead of `probs=`:**

- No manual softmax → no risk of `nan` from small denominators
- `log_prob` uses `log_softmax` internally (via `logsumexp` subtraction), which is the standard stable trick: `log_softmax(x) = x - logsumexp(x)` instead of `log(softmax(x))`
- This is exactly what you want feeding raw model output (last layer, pre-softmax) directly for RL policy gradients or LLM token sampling — you skip a redundant softmax→log round trip

**Typical use case (policy gradient / RL, which given your agent work you'll recognize):**

```python
logits = policy_net(state)          # raw output, shape [batch, num_actions]
dist = torch.distributions.Categorical(logits=logits)
action = dist.sample()              # sample an action
log_prob = dist.log_prob(action)    # for REINFORCE loss: -log_prob * reward
```

Same object type LLM sampling code uses under the hood conceptually — `logits` from the final linear layer, temperature-scaled, then categorical sampling for next-token generation.

References:

- [torch.distributions.Categorical docs](https://docs.pytorch.org/docs/stable/distributions.html#categorical)
- [categorical.py source](https://github.com/pytorch/pytorch/blob/main/torch/distributions/categorical.py)
