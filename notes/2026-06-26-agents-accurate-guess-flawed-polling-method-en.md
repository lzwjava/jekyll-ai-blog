---
audio: false
generated: true
image: false
lang: en
layout: post
title: Agent’s Accurate Guess, Flawed Polling Method
translated: false
type: note
---

Looking at the transcript, the agent's estimates were systematically wrong — but in a revealing way.

The agent locked onto a rate early (~270 KB/s, then ~370 KB/s, then "~20MB/min") and kept re-deriving an ETA from each snapshot. The problem: it never validated that the SCP was actually still running versus stalled, and its "~X min remaining" numbers don't reconcile with each other.

Walk the actual data points:

```
114MB  "~22 min remaining"
136MB
157MB  "~15 min"
177MB  "~15 min"
187MB
208MB  "~13 min"
228MB  "~12 min"
247MB  "~11 min"
273MB  "~10 min"
325MB  "~7 min"
366MB  "~5 min"
```

From 114→366MB the throughput is real and roughly steady. Fit it: ~252MB transferred across the polls. If each poll is ~60s (the `wait proc 60.0s` cadence), that's ~11–12 polls ≈ 11–12 min for 252MB → **~21–22 MB/min**, i.e. ~360 KB/s. So the *rate* estimate ("~20MB/min") is actually correct and consistent.

The ETAs are where it goes wrong. At 114MB it said 22 min for the remaining 361MB → implies ~16MB/min. At 366MB it said 5 min for the remaining 109MB → implies ~22MB/min. The later estimates are right; the early one was pessimistic. But more importantly, the agent kept saying "I'll stop checking every minute" and then checked every minute anyway — the estimates never actually drove behavior.

So: **the rate guess is correct, the per-poll ETAs are noisy but converging toward the truth, and the transfer never finished in-frame** (cut off at 366/475MB ≈ 77%). At the observed ~22MB/min, the remaining 109MB takes ~5 min — so its *final* guess ("~5 min left") is the one that's actually accurate.

The real failure isn't the arithmetic, it's the loop: polling `ls -lh` once a minute to babysit an SCP is a waste of ~15 agent-turns. The AI-native version is to not poll at all — let scp's own progress meter or a single blocking wait do the job:

```bash
# instead of N× ssh ... ls -lh, just run scp in foreground with progress
scp root@<IP_ADDRESS>:/tmp/model.safetensors .
# or background it and wait once:
scp ... & SCP=$!; wait $SCP && echo "done"
```

Or if it's a pull from a remote you can't watch directly, poll on *completion*, not on size:

```bash
# block until file size stops changing, then report — one logical op, not 15
ssh root@<IP_ADDRESS> '
  prev=0
  while :; do
    cur=$(stat -c%s /tmp/model.safetensors 2>/dev/null || echo 0)
    [ "$cur" = "$prev" ] && [ "$cur" -gt 0 ] && break
    prev=$cur; sleep 30
  done
  echo "stable at $cur bytes"
'
```

Bottom line: the **guess (rate ~20MB/min, final ETA ~5min) is correct**; the **method (one-minute manual polling with re-narrated ETAs) is wrong** and burned context for no information gain.
