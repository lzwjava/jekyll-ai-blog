---
audio: false
generated: true
image: false
lang: en
layout: post
title: "OpenDDE: Open Drug Discovery Engine"
translated: false
type: note
---

Question: Intro to `aurekaresearch/OpenDDE`

Answer:

[OpenDDE GitHub Repository](https://github.com/aurekaresearch/OpenDDE?utm_source=chatgpt.com) is an **open-source AI foundation model for drug discovery**, focused on **all-atom biomolecular modeling**. The project name means **Open Drug Discovery Engine**. It tries to make systems similar in spirit to Google DeepMind's AlphaFold 3-style models more open and usable. ([arXiv][1])

The core idea:

> Instead of only predicting protein structures, build a general molecular reasoning engine that can understand proteins, DNA, RNA, ligands, and their interactions.

([GitHub][2])

---

## 1. Background: why this matters

Traditional drug discovery:

```
Target protein
      |
      v
Find molecule candidates
      |
      v
Lab experiments
      |
      v
Optimize drug
      |
      v
Clinical trials
```

Very expensive:

* billions of dollars
* 10+ years
* high failure rate

AI changes the first stages:

```
Protein sequence
       +
Drug molecule
       |
       v
AI molecular model
       |
       +--> structure prediction
       +--> binding prediction
       +--> molecule design
       +--> optimization
```

OpenDDE tries to be this "foundation model" layer.

---

## 2. What does "all-atom biomolecular foundation model" mean?

Normal language models:

```
Text tokens
   |
Transformer
   |
next token prediction
```

Protein AI models:

```
Atoms / residues
        |
Geometric neural network
        |
3D molecular reasoning
        |
Structure / interaction prediction
```

A molecule is not a sequence only.

Example:

Protein:

```
M K V L S A ...
```

Sequence alone is 1D.

But the real object:

```
          O
          |
    C --- C
   /       \
 N         C
   \       /
    3D structure
```

The model needs to understand:

* distance between atoms
* angles
* chemical bonds
* symmetry
* physical constraints

---

## 3. Relationship with AlphaFold 3

OpenDDE explicitly builds on ideas/components from:

* AlphaFold 3
* OpenFold
* Protenix
* ColabFold

([GitHub][3])

The important evolution:

### AlphaFold 2

Mostly:

```
protein sequence
        |
        v
protein 3D structure
```

### AlphaFold 3 / OpenDDE

More general:

```
protein
DNA
RNA
small molecule ligand
ions
      |
      v
complex structure
```

Example:

Drug molecule:

```
     aspirin
        |
        v
protein binding pocket
        |
        v
predict interaction
```

---

## 4. Model architecture (high level)

The pipeline is roughly:

```
Input JSON
    |
    v
Sequence encoder
    |
    v
Atom-level representation
    |
    v
Geometric reasoning network
    |
    v
Diffusion / generative structure sampling
    |
    v
3D complex prediction
```

Similar to modern diffusion models:

```
noise structure
       |
       v
denoising network
       |
       v
valid molecular structure
```

---

## 5. Example usage

Install:

```bash
uv venv --python 3.11

source .venv/bin/activate

uv pip install \
  --torch-backend cu126 \
  "opendde[gpu]"

opendde doctor
```

([GitHub][4])

Run:

```bash
opendde pred \
  -i input.json \
  -o ./output \
  -n opendde_v1
```

([GitHub][4])

Input example:

```json
[
 {
  "name": "protein_test",
  "modelSeeds": [101],
  "sequences": [
    {
      "proteinChain": {
        "sequence": "ACDEFGHIK",
        "count": 1
      }
    }
  ]
 }
]
```

Output:

```
output/
 └── protein_test/
      └── predictions/
            structure.cif
```

---

## 6. Hardware requirements

This is not like running Qwen 7B.

It is much heavier.

Official support:

* NVIDIA CUDA 12.6
* GPU inference
* optional cuEquivariance kernels
* multi-GPU Fold-CP mode

([GitHub][4])

For large complexes:

```
GPU0
 |
GPU1
 |
GPU2
 |
GPU3

context parallel inference
```

They provide a 4-GPU mode:

```bash
torchrun \
 --nproc_per_node 4 \
 -m runner.batch_inference pred ...
```

([Hugging Face][5])

Your RTX 4070 12GB:

* good for learning
* probably not enough for serious production inference
* useful for reading code / small experiments

A realistic setup:

```
24GB GPU:
   small experiments

48GB GPU:
   useful

80GB A100/H100:
   serious workloads

multi GPU:
   large complexes
```

---

## 7. Why this project is interesting from an AI engineer perspective

It is a good example of the next wave:

Before:

```
LLM:
 text -> intelligence
```

Now:

```
Foundation models:

text
image
video
robotics
biology
chemistry
physics
```

Biology may become one of the biggest AI applications.

The pattern is similar:

GPT:

```
internet text
     |
large transformer
     |
reasoning
```

OpenDDE:

```
biological data
     |
geometric foundation model
     |
molecular reasoning
```

---

## 8. If you want to study the code

Good reading order:

```
README.md
   |
docs/inference_instructions.md
   |
input JSON format
   |
model code
   |
training paper
```

Repository:

[OpenDDE GitHub Repository](https://github.com/aurekaresearch/OpenDDE?utm_source=chatgpt.com)

Paper:

[Folding, Reasoning, and Scaling with Open-source Drug Discovery Engine](https://arxiv.org/abs/2607.03787?utm_source=chatgpt.com)

---

My view: OpenDDE is interesting because it shows **"foundation model" is escaping NLP**. The same scaling philosophy from GPT is moving into scientific domains: learn a representation of the world, then use it for prediction, generation, and optimization. For someone already training GPT/nanoGPT-style models, the conceptual jump is mainly from **token space → 3D geometric space**.

[1]: https://arxiv.org/abs/2607.03787?utm_source=chatgpt.com "Folding, Reasoning, and Scaling with Open-source Drug Discovery Engine"
[2]: https://github.com/aurekaresearch/OpenDDE?utm_source=chatgpt.com "GitHub - aurekaresearch/OpenDDE: An Open-source Drug Discovery Engine · GitHub"
[3]: https://github.com/aurekaresearch/OpenDDE/blob/main/README.md?utm_source=chatgpt.com "OpenDDE/README.md at main · aurekaresearch/OpenDDE · GitHub"
[4]: https://github.com/aurekaresearch/OpenDDE/blob/main/docs/inference_instructions.md?utm_source=chatgpt.com "OpenDDE/docs/inference_instructions.md at main · aurekaresearch/OpenDDE · GitHub"
[5]: https://huggingface.co/aurekaresearch/OpenDDE?utm_source=chatgpt.com "aurekaresearch/OpenDDE · Hugging Face"