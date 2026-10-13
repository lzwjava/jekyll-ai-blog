---
audio: false
generated: true
image: false
lang: en
layout: post
title: ZeRO Stage 3 Implemented and Tested
translated: false
type: note
---

Done. **ZeRO stage 3 is implemented, tested, and committed.** Final state: `45 passed, 2 skipped` (was 36+2), example trains & resumes with `--zero 3` on 1 and 2 ranks.

## What was built

**Design** — stage 3 partitions *everything*, reusing the existing stage-2 gradient path:

| State | Between steps (resident) | During compute |
| --- | --- | --- |
| fp32 masters | `1/N` shard only | transient full buffer per group at gather, freed immediately |
| Adam moments | `1/N` (as stage 1/2) | — |
| gradients | `1/N` reduce-scattered shard | full flat buffer lives only from flatten → reduce-scatter |
| model params | flat `1/N` placeholder slice per param | full tensors, all-gathered on the first `engine(x)` of a window |

Lifecycle: `engine(x)` → `gather_parameters()` (one all-gather + fp32→fp16 cast per group) → fwd/bwd → boundary: flatten → reduce-scatter → **free grads** → clip (exact, shard sums-of-squares) → Adam on shard → **free params** (placeholders refreshed from updated masters).

## Files

- **`minispeed/flat.py`** — `partition_params` / `materialize_params` / `dematerialize_params`, `master_range`, coverage-aware overlap copies (works for full params *and* partial placeholders), lazy/freable grad buffer
- **`minispeed/zero/stage_3.py`** *(new)* — `ZeROStage3Optimizer`: gather/free/sync + stage-2 reduce, drops the full grad buffer after reduce-scatter
- **`minispeed/zero/__init__.py`** — `build_zero_optimizer` factory
- **`minispeed/engine.py`** — partition at init, lazy gather in `forward`, free after every boundary (including overflow skips), gather-aware `state_dict`/`load_state_dict`, new `gather` timer
- **`minispeed/checkpoint.py`** — gathers around save/load, restores params to their pre-load state
- **`minispeed/config.py`** — stage 3 accepted; `stage3_gather_16bit_weights_on_model_save: false` rejected (layout always writes full weights); offload still fails fast
- **Tests** — new `test_zero3.py` (6 tests: stage3≡stage0, gather/free lifecycle, partition roundtrip, overflow skip, checkpoint replay, eval re-gather); stage 3 added to `test_distributed`, `test_gpu` (gloo/CUDA fp32+fp16), `test_config`
- **README / example / docstrings** updated (features table, "ZeRO in four lines", step diagram, limitations)

## Bugs caught while testing

1. Placeholder indexing assumed `p.data` covers the whole param — fixed with `_pdata_range()` coverage-aware windows.
2. `dematerialize_params` produced negative sizes for params outside a rank's shard — guarded.
3. **Real gotcha**: the example's rank-0-only sampling demo deadlocked, because a stage-3 forward is *collective* — fixed the example and documented the caveat in the README.

Two commits: `b839f9d` (feature) and `9afccd9` (sampling fix). Working tree clean.
