---
audio: false
generated: true
image: false
lang: en
layout: post
title: "OpenFold: Faithful AlphaFold2 Reproduction"
translated: false
type: note
---

Here's what OpenFold is:

---

**OpenFold** — a faithful, trainable PyTorch reproduction of DeepMind's **AlphaFold 2** (protein structure prediction).

Built by the AlQuraishi Laboratory at Columbia/Harvard. The repo has ~159 stars contributors and is actively maintained (recent NVIDIA contributions for cuEquivariance support).

**What it does:** Given a protein amino acid sequence, predicts its 3D atomic structure. This is the same problem AlphaFold 2 solved — arguably the biggest AI breakthrough in biology.

**Architecture (from the code):**

The `AlphaFold` class in `openfold/model/model.py` implements Algorithm 2 from the AlphaFold 2 paper, with these key components:

1. **Input Embedders** (`embedders.py`) — embed amino acid sequences + MSA (multiple sequence alignments) + templates into pair/representation tensors. Supports monomer, multimer, and a "preembedding" mode.

2. **Evoformer** (`evoformer.py`, ~1278 lines) — the core trunk. Stacks of:
   - MSA row/column attention (with pair bias, global attention option)
   - Triangle multiplication (outgoing/incoming) — fused CUDA variants exist
   - Triangle attention (starting/ending node)
   - Outer product mean (MSA → pair representation)
   - Pair transitions, MSA transitions
   - Gradient checkpointing + chunking for memory efficiency

3. **Structure Module** (`structure_module.py`) — IPA (Invariant Point Attention) that generates 3D atom coordinates from the pair/representation tensors. Uses SE(3)-equivariant operations.

4. **Heads** (`heads.py`) — auxiliary outputs: pLDDT confidence, distogram, predicted aligned error (PAE), masked MSA.

5. **Loss** (`utils/loss.py`) — FAPE (Frame Aligned Point Error), auxiliary distogram/angle losses, pLDDT loss.

**Training:** `train_openfold.py` wraps it in a PyTorch Lightning module (`OpenFoldWrapper`) with:
   - DeepSpeed ZeRO / DDP strategies
   - EMA (exponential moving average) of weights
   - AlphaFold-specific LR scheduler
   - Multi-chain permutation alignment (for multimer)
   - WandB logging
   - Weight import from both JAX (original DeepMind) and OpenFold checkpoints

**Infrastructure:**
   - CUDA extensions in `setup.py` — custom kernels for attention, triangle operations
   - cuEquivariance integration (NVIDIA)
   - TensorRT inference support (`utils/tensorrt_utils.py`)
   - DeepSpeed integration for distributed training
   - Data pipeline in `openfold/data/` — handles mmCIF, PDB, MSA generation
   - Amber relaxation (`np/relax/`) — physics-based energy minimization of predicted structures

**Key files:**
   - `openfold/config.py` — model configs (monomer, multimer, different sizes)
   - `openfold/model/` — all neural network modules (15 files)
   - `openfold/utils/` — loss, geometry (SO(3)/SE(3)), import weights, checkpointing
   - `openfold/data/` — data loading, transforms, alignment preprocessing
   - `scripts/` — preprocessing scripts for alignments, embeddings, data caches

This is a substantial ML codebase (~50k+ lines) implementing one of the most complex AI architectures in production. The recent commits focus on NVIDIA optimizations (cuEquivariance for the triangle operations, TRT inference).
