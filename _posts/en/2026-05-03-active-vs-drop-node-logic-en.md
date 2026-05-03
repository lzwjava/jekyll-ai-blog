---
audio: false
generated: true
image: false
lang: en
layout: post
title: ACTIVE vs DROP Node Logic Explained
translated: false
type: note
---

Here's the full picture:

## How ACTIVE vs DROP works

### The two key enums (`models.py:12-54`)

```python
class NodeStatus(str, Enum):
    ACTIVE = "ACTIVE"           # viable, can be expanded further
    PRUNED_BY_RULE = "PRUNED_BY_RULE"  # killed by hard physics rule
    PRUNED_BY_SLM = "PRUNED_BY_SLM"   # killed by soft scoring (reserved)

class NodeResultState(str, Enum):
    PASS = "PASS"    # survived this round
    DROP = "DROP"    # dead — won't be expanded
```

A node only gets `DROP` when **both** are set together:
```python
self.node.status = NodeStatus.PRUNED_BY_RULE
self.node.result_state = NodeResultState.DROP
self.node.fsm_state = FSMState.FINALIZED   # no further transitions
```

---

### Where DROP is triggered

**1. During `calculate` stage** (`builder.py:295-310`) — `tot_hard_rule_check` from `skills.py` returns `physical_violations`:
```python
if not hard_rule_result["passed"]:
    if physical_violations:
        → status = PRUNED_BY_RULE, result_state = DROP
```

**2. During `evaluate` stage** (`builder.py:396-416`) — the evaluation breakdown itself contains `hard_rule_violations`:
```python
if breakdown.hard_rule_violations:
    → status = PRUNED_BY_RULE, result_state = DROP
```

---

### What does NOT cause DROP

- **Low score** — the docstring at `builder.py:76` is explicit: *"Low scores never prune the node; they only reduce downstream expansion priority."* The node stays `ACTIVE`, just ranked lower.
- **Recoverable violations** — sent to `REFLECT` state for a retry instead of being dropped (`builder.py:317`).
- **Root node violations** — special-cased via `_bounce_root_rule_violations()` — gets a reflection attempt rather than immediate DROP.

---

**One-liner:** Only a hard physics rule violation (detected by `skills.py`) flips a node to `DROP`. Soft scores just affect expansion priority, leaving the node `ACTIVE`.