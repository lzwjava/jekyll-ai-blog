---
audio: false
generated: true
lang: en
layout: post
title: How AlphaFold Works
translated: false
type: note
---

Let’s dive into how **AlphaFold**, developed by DeepMind, works—a groundbreaking AI system that predicts protein structures with remarkable accuracy. I’ll break it down into its core concepts, the problem it solves, its architecture, and the steps it takes to go from a protein’s amino acid sequence to a 3D structure. This will be comprehensive but digestible, with enough detail to satisfy curiosity without drowning in jargon.

---

### The Problem: Protein Folding

Proteins are the workhorses of life, made of chains of amino acids that fold into specific 3D shapes to perform their functions (e.g., enzymes, antibodies). The **protein folding problem** is figuring out how a sequence of amino acids (e.g., "AGHKL...") folds into its unique 3D structure, determined by physical and chemical interactions. Traditionally, this was solved experimentally (e.g., X-ray crystallography), which is slow and expensive, or computationally, which was inaccurate for complex proteins. AlphaFold changes that by predicting structures from sequences alone, rivaling experimental accuracy.

---

### AlphaFold’s Evolution

- **AlphaFold 1 (2018)**: Debuted at CASP13 (Critical Assessment of Structure Prediction), using a mix of machine learning and physics-based modeling. It was good but limited.
- **AlphaFold 2 (2020)**: A leap forward at CASP14, achieving near-experimental precision (median GDT_TS score ~90). It ditched much of the physics-based approach for a fully AI-driven system.
- **AlphaFold 3 (2024)**: Expands to predict protein-ligand interactions and other biomolecules, but we’ll focus on AlphaFold 2, as it’s the most documented and foundational.

---

### How AlphaFold (2) Works: The Big Picture

AlphaFold 2 takes an amino acid sequence and outputs a 3D structure by:
1. Leveraging **evolutionary data** to understand how sequences relate to structures.
2. Using a **deep learning architecture** to model spatial relationships.
3. Iteratively refining predictions to optimize the structure.

It’s built around two main components: an **Evoformer** (processing sequence and evolutionary data) and a **Structure Module** (building the 3D model). Let’s break it down step-by-step.

---

### Step 1: Input Data

AlphaFold starts with:
- **Amino Acid Sequence**: The protein’s primary structure (e.g., a string of 100 amino acids).
- **Multiple Sequence Alignment (MSA)**: A collection of related protein sequences from evolutionary databases (e.g., UniProt). This shows how the protein’s sequence varies across species, hinting at conserved regions critical to its structure.
- **Template Structures**: Known 3D structures of similar proteins (optional, from PDB), though AlphaFold 2 relies less on these than its predecessor.

The MSA is key—it reveals **coevolutionary patterns**. If two amino acids always mutate together, they’re likely close in the folded structure, even if far apart in the sequence.

---

### Step 2: The Evoformer

The Evoformer is a transformer-based neural network that processes the MSA and sequence data to build a rich representation of the protein. Here’s what it does:

1. **Pair Representation**:
   - Creates a matrix encoding relationships between every pair of amino acids (e.g., distance, interaction likelihood).
   - Initialized from MSA data: correlated mutations suggest spatial proximity.

2. **Sequence Representation**:
   - Tracks features of each amino acid (e.g., chemical properties, position in the chain).

3. **Attention Mechanism**:
   - Uses transformer-style attention to iteratively refine these representations.
   - “Rows” of the MSA (evolutionary sequences) and “columns” (positions in the protein) communicate via attention, capturing long-range dependencies.
   - Think of it as the AI asking: “Which amino acids influence each other, and how?”

4. **Output**:
   - A polished **pair representation** (a map of probable spatial relationships) and an updated sequence representation, ready for 3D modeling.

The Evoformer’s genius is distilling messy evolutionary data into a form that reflects physical constraints without explicitly simulating physics.

---

### Step 3: The Structure Module

The Structure Module takes the Evoformer’s output and constructs the 3D structure. It’s a geometric deep learning system that predicts atom positions (focusing on the protein backbone: Cα, N, C atoms). Here’s how:

1. **Initial Guess**:
   - Starts with a rough 3D frame for the protein, often random or based on Evoformer hints.

2. **Invariant Point Attention (IPA)**:
   - A novel attention mechanism that respects 3D geometry (rotations and translations don’t mess it up).
   - Updates atom positions by considering pairwise relationships from the Evoformer, ensuring physical plausibility (e.g., bond angles, distances).

3. **Iterative Refinement**:
   - Repeatedly adjusts the structure over multiple cycles.
   - Each cycle refines coordinates, guided by the pair representation and geometric constraints.

4. **Output**:
   - A set of 3D coordinates for all atoms in the protein backbone, plus side chains added later.

The Structure Module essentially “sculpts” the protein, turning abstract relationships into a concrete shape.

---

### Step 4: Confidence Scoring and Refinement

AlphaFold doesn’t just predict a structure—it tells you how confident it is:
- **pLDDT (Predicted Local Distance Difference Test)**: A per-residue confidence score (0-100). High scores (e.g., >90) indicate reliable predictions.
- **Recycling**: The model loops its output back into the Evoformer 3-5 times, refining predictions with each pass.
- **Final Touches**: Side chains are added using a simpler geometric method, as the backbone dictates their placement.

---

### Step 5: Training and Loss Function

AlphaFold 2 was trained on:
- **PDB Data**: ~170,000 known protein structures.
- **MSA Databases**: Billions of protein sequences.

The training loss combines:
- **FAPE (Frame-Aligned Point Error)**: Measures how well predicted atom positions match the true structure in a physically meaningful way.
- **Auxiliary Losses**: Enforce constraints like realistic bond lengths and clash avoidance.
- **Distogram Loss**: Ensures predicted pairwise distances align with reality (from AlphaFold 1’s heritage).

This end-to-end training lets AlphaFold learn both evolutionary patterns and structural rules implicitly.

---

### Key Innovations

1. **End-to-End Learning**: Unlike AlphaFold 1, which predicted distances then optimized them, AlphaFold 2 predicts the structure directly.
2. **Transformers and Geometry**: Evoformer’s attention and IPA blend sequence analysis with 3D reasoning.
3. **No Physics Engine**: It learns physical rules from data, avoiding slow simulations.

---

### How Accurate Is It?

At CASP14, AlphaFold 2 achieved a median GDT_TS score of 92.4 (out of 100), where >90 is considered experimental quality. For many proteins, it matches X-ray or cryo-EM results, though it struggles with disordered regions or novel folds lacking evolutionary data.

---

### Strengths

- **Speed**: Predicts structures in hours, not months.
- **Accuracy**: Rivals experimental methods for most proteins.
- **Scalability**: Handles proteins of varying sizes (though larger ones need more compute).

---

### Limitations

- **Disordered Regions**: Struggles with flexible, unstructured protein segments.
- **Novel Proteins**: Less accurate if no similar sequences exist in the MSA.
- **Static Structures**: Predicts one conformation, not dynamic behavior.
- **Compute Intensive**: Training and large predictions require hefty resources (e.g., TPUs).

---

### Applications

- **Drug Discovery**: Predicts target protein structures for designing drugs.
- **Biology Research**: Accelerates understanding of protein functions.
- **Synthetic Biology**: Guides protein engineering by predicting foldable designs.

---

### AlphaFold 3 (Brief Note)

Announced in 2024, AlphaFold 3 extends to protein-ligand binding and other molecules (e.g., DNA, RNA). It uses a diffusion model to refine predictions, but detailed mechanics are less public. Its core builds on AlphaFold 2’s foundation.

---

### Conclusion

AlphaFold 2 is a masterpiece of AI, blending evolutionary insights, transformer magic, and geometric finesse to solve a 50-year biology puzzle. It doesn’t simulate folding step-by-step like nature—it reverse-engineers the end result from data. Think of it as a super-smart cartographer mapping a protein’s 3D landscape from scattered clues.

If you’d like, I can dig deeper into the Evoformer’s attention mechanism, the math behind IPA, or even how to use AlphaFold’s open-source code (available on GitHub). What’s your next question?
