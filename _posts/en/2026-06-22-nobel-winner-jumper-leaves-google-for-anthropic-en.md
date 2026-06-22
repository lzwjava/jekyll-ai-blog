---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nobel Winner Jumper Leaves Google for Anthropic
translated: false
type: note
---

**Question:** What happened with the Nobel Prize winner leaving Google for Anthropic? What's the context around AlphaFold and its creator? And what would it take to build a "zhiwei-fold" — a personal protein structure prediction model?

**Answer:**

## The Person: Demis Hassabis → No, It's John Jumper

The Nobel Prize winner your friend is referring to is almost certainly **John Jumper** — co-creator of AlphaFold 2, who shared the 2024 Nobel Prize in Chemistry with Demis Hassabis and David Baker.Confirmed. Big news, fresh (June 19, 2026). Here's the full picture:

---

## What Actually Happened

John Jumper served as VP/Engineering Fellow at Google DeepMind for nearly nine years. In June 2026, he announced he would leave to join Anthropic after a break.

Jumper shared half the 2024 Nobel Prize in Chemistry with Hassabis for developing AlphaFold2. The other half went to David Baker for computational protein design. AlphaFold2 has been used by more than two million scientists across 190 countries, accelerating research on malaria vaccines, cancer treatments, and drug-resistant bacteria.

Your friend's read is correct — this is a talent signal, not just a personnel move.

---

## Why This Matters (Your Friend's Core Point Is Right)

One day before Jumper's announcement, Noam Shazeer — co-author of "Attention Is All You Need" and co-lead of Gemini — left for OpenAI. Google lost the architects of its two defining AI-for-science achievements in one week.

According to SignalFire's 2025 State of Talent Report, engineers at DeepMind were nearly 11 times more likely to leave for Anthropic than the reverse. Andrej Karpathy also joined Anthropic's pre-training team in May 2026.

Neither prestige nor money seems to be the issue — Shazeer left despite a deal reportedly worth billions. If that can't hold the people who built the company's most celebrated achievements, the problem may not be compensation.

The signal: Anthropic's mission density is beating Google's resources as a recruiting tool.

---

## AlphaFold: Does It Touch the Masses?

You're right that it's not consumer-facing, but the impact is real:

The AlphaFold team released 214 million protein structure predictions as of January 2024. Drug discovery pipelines at pharma companies use it. It compressed decades of structural biology work into a freely queryable database. You don't feel it directly, but the malaria vaccine researchers do.

Yin Wang's framing (Nobel/Turing prizes don't mean much intrinsically) is philosophically coherent — prizes lag the actual insight by years and reward legibility over depth. But AlphaFold is a rare case where the prize actually matches a real, verifiable breakthrough with measurable downstream use.

---

## zhiwei-fold: What Would It Take?

This is the interesting part. Here's a realistic path for you in the next 6 months:

### What AlphaFold2 Actually Is (Architecture)

```
Input: amino acid sequence (L residues)
  → Multiple Sequence Alignment (MSA) via Jackhmmer/HHblits
  → Pair representation + MSA representation
  → Evoformer (48 blocks): attention over residue pairs + MSA rows/cols
  → Structure module: invariant point attention (IPA) on 3D frames
Output: 3D coordinates per residue + pLDDT confidence
```

The key insight: protein folding is a **geometric attention problem** over evolutionary co-variation signals. The MSA encodes which residues co-evolved → which residues are spatially close.

### Minimal Entry Point

You don't need to retrain AlphaFold2 from scratch. Start here:

```python
# ESMFold — single-sequence folding, no MSA needed
# Meta's model, much simpler operationally
pip install fair-esm

import esm
model, alphabet = esm.pretrained.esmfold_v1()
model.eval().cuda()

sequence = "MKTIIALSYIFCLVFA"  # example
with torch.no_grad():
    output = model.infer_pdb(sequence)

with open("output.pdb", "w") as f:
    f.write(output)
```

ESMFold trades MSA complexity for a large protein language model (ESM-2, 3B params). Good starting point on your RTX 4070.

### Realistic zhiwei-fold Roadmap

| Phase | Task | Hardware | Timeline |
|-------|------|----------|----------|
| 1 | Run ESMFold inference on custom sequences | RTX 4070 | Week 1 |
| 2 | Fine-tune ESM-2 embeddings on a domain-specific protein dataset (e.g. antimicrobial peptides) | RTX 4070 | Month 1 |
| 3 | Train a lightweight structure head on top (GVP-GNN or IPA) | MI300X | Month 2-3 |
| 4 | Dataset: UniProt + PDB + AlphaFold DB filtered subset | Any | Ongoing |
| 5 | Evaluation: TM-score vs experimental PDB structures | Any | Per iteration |

### Key Datasets

```bash
# AlphaFold DB (subset)
wget https://ftp.ebi.ac.uk/pub/databases/alphafold/latest/UP000005640_9606_HUMAN_v4.tar

# PDB structures
rsync -rlpt -v -z --delete \
  rsync.rcsb.org::ftp_data/structures/divided/pdb/ ./pdb/

# UniRef50 for ESM pretraining data
wget https://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref50/uniref50.fasta.gz
```

### The nanoGPT analogy

You already know nanoGPT. Think of zhiwei-fold as:

- **Tokenizer** → amino acid vocabulary (20 standard AAs + specials)
- **Embedding** → ESM-2 protein language model (your "pretrained weights")
- **Transformer** → Evoformer (pairwise attention, not just sequence attention)
- **Head** → structure module outputting 3D frames instead of logits

The fundamental difference from GPT: you're predicting **geometry** (rotation matrices + translations per residue), not token distributions. The loss is FAPE (Frame Aligned Point Error) rather than cross-entropy.

---

## Bottom Line

Your friend's social read is correct — Jumper leaving is a gravitational signal about Anthropic's trajectory, not just a résumé shuffle. For you: the protein folding space is genuinely approachable. ESMFold runs on consumer GPUs, the datasets are public, and your MI300X (192GB HBM3) is more than enough to fine-tune ESM-2 3B. zhiwei-fold in 6 months is realistic if you treat it like you treated nanoGPT — start with inference, understand the architecture, then train a small version from a meaningful subset.

References:

- [John Jumper Wikipedia](https://en.wikipedia.org/wiki/John_M._Jumper)
- [AlphaFold Nobel Laureate Joins Anthropic — TechTimes](https://www.techtimes.com/articles/318754/20260620/alphafold-nobel-laureate-john-jumper-joins-anthropic-after-nine-years-deepmind.htm)
- [John Jumper Leaves DeepMind for Anthropic — The Next Web](https://thenextweb.com/news/john-jumper-nobel-deepmind-leaves-anthropic-alphafold)
- [ESMFold GitHub](https://github.com/facebookresearch/esm)
- [AlphaFold DB](https://alphafold.ebi.ac.uk/)
